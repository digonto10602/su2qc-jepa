#!/usr/bin/env python
"""Pull-based job worker for Perlmutter (decisions/004).  One invocation = one "tick", started by scrontab.
`--mode local` exists for tests only.  It never pushes to `main`; it only pushes to the `results` branch.

Tick:
  1. take a lock (a second tick exits at once), fetch origin;
  2. read jobs/*.yaml on origin/main; keep those addressed to this worker (`where` == name or 'any'),
     valid, at a commit reachable from origin/main, with no status yet on origin/results;
  3. slurm mode: submit each new job with sbatch (cap per tick, node-hour budget); local mode: run at most
     one job, at low priority, with a time limit;
  4. for submitted Slurm jobs, poll sacct; when finished copy the declared outputs (size-capped) into
     results/<NNN>/outputs, write status.json and log.txt, commit and push to `results`.

  python scripts/worker/worker.py --name perlmutter --mode slurm --base $SCRATCH/su2qc-worker \
         --repo git@github-su2qc:digonto10602/su2qc-jepa.git --account m1234 --env-prefix /global/common/software/m1234/su2qc-jepa-env
Self-healing: TIMEOUT / OUT_OF_MEMORY / NODE_FAIL / PREEMPTED / BOOT_FAIL / LOST are resubmitted automatically (up to 3 attempts,
with doubled time or GPUs per su2qc_jepa.jobs.retry_resources); a corrupted clone is re-cloned; a failed tick logs to
tick_errors.log and the next tick retries; in-flight jobs are recovered from the results branch if local state is lost;
a heartbeat on results/_worker/perlmutter.json lets the laptop see that the worker is alive.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import shlex
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

import yaml

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[2] / "src"))
from su2qc_jepa.jobs import MAX_ATTEMPTS, MAX_OUTPUT_MB, parse_steps, retry_resources, validate_job  # noqa: E402

TERMINAL = {"COMPLETED", "FAILED", "CANCELLED", "TIMEOUT", "OUT_OF_MEMORY", "NODE_FAIL", "REFUSED", "PREEMPTED", "BOOT_FAIL",
            "DEADLINE", "LOST"}
LOST_AFTER_HOURS = 3.0  # sacct knows nothing about a submitted job for this long -> treat it as lost


def sh(*args, cwd=None, check=True, capture=True, env=None) -> str:
    r = subprocess.run(list(args), cwd=cwd, check=False, capture_output=capture, text=True, env=env)
    if check and r.returncode != 0:
        raise RuntimeError(f"command failed ({r.returncode}): {' '.join(args)}\n{r.stdout}\n{r.stderr}")
    return (r.stdout or "").strip()


def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def hms_to_hours(s: str) -> float:
    days = 0
    if "-" in s:
        d, s = s.split("-", 1)
        days = int(d)
    parts = [int(x) for x in s.split(":")]
    while len(parts) < 3:
        parts.insert(0, 0)
    return days * 24 + parts[0] + parts[1] / 60 + parts[2] / 3600


class Worker:
    def __init__(self, a):
        self.a = a
        self.base = Path(os.path.expandvars(os.path.expanduser(a.base))).resolve()
        self.main = self.base / "main"
        self.results = self.base / "results"
        self.runs = self.base / "runs"
        self.state_path = self.base / "state.json"
        self.base.mkdir(parents=True, exist_ok=True)
        self.runs.mkdir(exist_ok=True)
        self.state = json.loads(self.state_path.read_text()) if self.state_path.exists() else {}
        self.log_lines: list[str] = []

    def log(self, msg: str):
        line = f"[{now()}] {self.a.name}: {msg}"
        print(line, flush=True)
        self.log_lines.append(line)

    def save_state(self):
        self.state_path.write_text(json.dumps(self.state, indent=2))

    # -- git -------------------------------------------------------------------------------------
    def _fresh_clone(self, path: Path):
        if path.exists():
            if path == self.main:
                subprocess.run(["git", "worktree", "prune"], cwd=path, capture_output=True)
            shutil.rmtree(path, ignore_errors=True)
        sh("git", "clone", "-q", self.a.repo, str(path))

    def sync(self):
        """Fetch main and results; a corrupted clone is deleted and re-cloned once (self-repair)."""
        for path in (self.main, self.results):
            try:
                if not (path / ".git").exists():
                    self._fresh_clone(path)
                sh("git", "fetch", "-q", "origin", cwd=path)
                if path == self.main:
                    sh("git", "checkout", "-q", "--detach", "origin/main", cwd=path)
            except RuntimeError as e:
                self.log(f"repairing {path.name} clone after: {str(e).splitlines()[0]}")
                self._fresh_clone(path)
                sh("git", "fetch", "-q", "origin", cwd=path)
                if path == self.main:
                    sh("git", "checkout", "-q", "--detach", "origin/main", cwd=path)
        has_remote = sh("git", "ls-remote", "--heads", "origin", "results", cwd=self.results)
        if has_remote:
            sh("git", "checkout", "-q", "-B", "results", "origin/results", cwd=self.results)
        else:
            sh("git", "checkout", "-q", "--orphan", "results", cwd=self.results)
            sh("git", "rm", "-rfq", "--ignore-unmatch", ".", cwd=self.results)
            for p in self.results.iterdir():
                if p.name != ".git":
                    shutil.rmtree(p) if p.is_dir() else p.unlink()
            (self.results / "README.md").write_text("# results branch\n\nWritten only by the job workers (decisions/003). Never merge into main.\n")
            self.commit_push("results: initialise branch")

    def git_env(self) -> dict:
        ident = f"su2qc-worker-{self.a.name}"
        return {**os.environ, "GIT_AUTHOR_NAME": ident, "GIT_COMMITTER_NAME": ident,
                "GIT_AUTHOR_EMAIL": "worker@su2qc.invalid", "GIT_COMMITTER_EMAIL": "worker@su2qc.invalid"}

    def commit_push(self, msg: str):
        sh("git", "add", "-A", cwd=self.results)
        if not sh("git", "status", "--porcelain", cwd=self.results):
            return
        env = self.git_env()
        sh("git", "commit", "-qm", msg, cwd=self.results, env=env)
        if self.a.no_push:
            return
        for attempt in range(4):
            r = subprocess.run(["git", "push", "-q", "origin", "results"], cwd=self.results, capture_output=True, text=True)
            if r.returncode == 0:
                return
            # another worker pushed in between: replay our commits on top (paths are per-job, so no conflicts)
            sh("git", "fetch", "-q", "origin", cwd=self.results)
            sh("git", "rebase", "-q", "origin/results", cwd=self.results, env=env)
            time.sleep(2 * (attempt + 1))
        raise RuntimeError("could not push to results after 4 attempts")

    # -- jobs ------------------------------------------------------------------------------------
    def jobs(self) -> list[dict]:
        out = []
        for p in sorted((self.main / "jobs").glob("[0-9][0-9][0-9]_*.yaml")):
            j = yaml.safe_load(p.read_text()) or {}
            j["_num"] = p.name[:3]
            j["_file"] = p.name
            out.append(j)
        return out

    def status_of(self, num: str) -> dict | None:
        p = self.results / num / "status.json"
        return json.loads(p.read_text()) if p.exists() else None

    def write_status(self, num: str, st: dict, msg: str):
        d = self.results / num
        d.mkdir(parents=True, exist_ok=True)
        (d / "status.json").write_text(json.dumps(st, indent=2))
        self.commit_push(msg)

    def node_hours_used(self) -> float:
        tot = 0.0
        for p in self.results.glob("[0-9][0-9][0-9]/status.json"):
            st = json.loads(p.read_text())
            if st.get("worker") == self.a.name:
                tot += float(st.get("node_hours") or 0)
        return tot

    def eligible(self, j: dict) -> tuple[bool, str]:
        if j.get("where") not in (self.a.name, "any"):
            return False, "addressed to another worker"
        if self.status_of(j["_num"]) is not None or j["_num"] in self.state:
            return False, "already handled"
        probs = validate_job({k: v for k, v in j.items() if not k.startswith("_")}, expected_id=f"jobs/{j['_num']}")
        if probs:
            return False, "invalid: " + "; ".join(probs)
        r = subprocess.run(["git", "merge-base", "--is-ancestor", j["commit"], "origin/main"], cwd=self.main)
        if r.returncode != 0:
            return False, "commit not on origin/main"
        return True, ""

    def prepare(self, j: dict) -> Path:
        wd = self.runs / j["_num"]
        if wd.exists():
            subprocess.run(["git", "worktree", "remove", "--force", str(wd)], cwd=self.main, capture_output=True)
            shutil.rmtree(wd, ignore_errors=True)
        sh("git", "worktree", "add", "-q", "--detach", str(wd), j["commit"], cwd=self.main)
        steps = parse_steps(j["steps"])
        py = self.a.python or "python"
        lines = ["#!/bin/bash", "set -euo pipefail", f"cd {wd}", "export PYTHONHASHSEED=0 PYTHONPATH=$PWD/src"]
        if self.a.mode == "slurm":
            lines += ["module load conda", f"conda activate {self.a.env_prefix}", "export SU2QC_DEVICE=${SU2QC_DEVICE:-cuda}"]
            py = "python"
        else:
            lines += [f"export SU2QC_DEVICE=${{SU2QC_DEVICE:-auto}} SU2QC_THREADS={self.a.threads} OMP_NUM_THREADS={self.a.threads} "
                      f"MKL_NUM_THREADS={self.a.threads} OPENBLAS_NUM_THREADS={self.a.threads}"]
        lines.append(f'echo "job {j["id"]} commit {j["commit"][:8]} on $(hostname) at $(date -u)"')
        for argv in steps:
            argv = [py] + argv[1:]
            lines.append(shlex.join(argv))
        script = self.runs / f"{j['_num']}.sh"
        script.write_text("\n".join(lines) + "\n")
        script.chmod(0o755)
        return script

    def submit_slurm(self, j: dict, script: Path) -> str:
        res = j["resources"]
        args = ["sbatch", "--parsable", "-A", self.a.account, "-C", "gpu", "-q", res.get("qos", self.a.qos),
                "--gpus", str(res["gpus"]), "-t", res["time"], "-J", f"su2qc-{j['_num']}",
                "-o", str(self.runs / f"{j['_num']}.log"), "-c", str(res.get("cpus", 32)), str(script)]
        return sh(*args).split(";")[0]

    def run_local(self, j: dict, script: Path) -> tuple[str, float]:
        limit = hms_to_hours(j["resources"]["time"]) * 3600
        t0 = time.time()
        with open(self.runs / f"{j['_num']}.log", "w") as fh:
            cmd = ["nice", "-n", "10", "bash", str(script)]
            try:
                r = subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT, timeout=limit)
                state = "COMPLETED" if r.returncode == 0 else "FAILED"
            except subprocess.TimeoutExpired:
                state = "TIMEOUT"
        return state, (time.time() - t0) / 3600

    def collect(self, j: dict, state: str, hours: float, extra: dict, gpus_hours: float | None = None):
        num = j["_num"]
        wd = self.runs / num
        out_dir = self.results / num / "outputs"
        if out_dir.exists():
            shutil.rmtree(out_dir)
        copied, total, skipped = [], 0, []
        for rel in j["outputs"]:
            src = wd / rel
            files = [src] if src.is_file() else sorted(p for p in src.rglob("*") if p.is_file()) if src.exists() else []
            if not files:
                skipped.append(f"{rel} (missing)")
            for f in files:
                size = f.stat().st_size
                if f.suffix in (".npz",) or total + size > MAX_OUTPUT_MB * 1e6:
                    skipped.append(f"{f.relative_to(wd)} ({size / 1e6:.1f} MB, not published)")
                    continue
                dst = out_dir / f.relative_to(wd)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst)
                copied.append(str(f.relative_to(wd)))
                total += size
        logf = self.runs / f"{num}.log"
        tail = logf.read_text().splitlines()[-200:] if logf.exists() else []
        (self.results / num).mkdir(parents=True, exist_ok=True)
        (self.results / num / "log.txt").write_text("\n".join(tail) + "\n")
        gpus = int(j["resources"].get("gpus", 0))
        gh = gpus_hours if gpus_hours is not None else hours * gpus
        node_hours = round(gh / 4 if self.a.mode == "slurm" else 0.0, 3)
        st = {"id": j["id"], "state": state, "worker": self.a.name, "host": socket.gethostname(), "commit": j["commit"],
              "finished_utc": now(), "elapsed_hours": round(hours, 3), "node_hours": node_hours,
              "outputs": copied, "outputs_mb": round(total / 1e6, 2), "skipped": skipped, **extra}
        self.write_status(num, st, f"results: job {num} {state}")
        self.state.pop(num, None)
        self.save_state()
        subprocess.run(["git", "worktree", "remove", "--force", str(wd)], cwd=self.main, capture_output=True)
        self.log(f"job {num} {state} ({hours:.2f} h, {len(copied)} files, {total / 1e6:.1f} MB)")

    def poll_slurm(self, jobs_by_num: dict):
        for num, rec in list(self.state.items()):
            if num not in jobs_by_num or "slurm_id" not in rec:
                continue
            out = sh("sacct", "-j", rec["slurm_id"], "-X", "-n", "-P", "-o", "State,Elapsed", check=False)
            if not out:
                age_h = (time.time() - rec.get("submitted_epoch", time.time())) / 3600
                if age_h < LOST_AFTER_HOURS:
                    continue
                state, elapsed = "LOST", "0:00"
            else:
                state, elapsed = (out.splitlines()[0].split("|") + ["0:00"])[:2]
                state = state.split()[0]
            if state not in TERMINAL:
                if state != rec.get("last_state"):
                    rec["last_state"] = state
                    self.save_state()
                continue
            j = jobs_by_num[num]
            hours = hms_to_hours(elapsed)
            rec["hours_so_far"] = rec.get("hours_so_far", 0.0) + hours
            rec.setdefault("history", []).append({"slurm_id": rec["slurm_id"], "state": state, "hours": round(hours, 3),
                                                  "resources": rec.get("resources", j["resources"])})
            attempt = rec.get("attempt", 1)
            new_res = retry_resources(rec.get("resources", j["resources"]), state) if attempt < MAX_ATTEMPTS else None
            if new_res is not None:
                jj = dict(j, resources=new_res)
                sid = self.submit_slurm(jj, self.runs / f"{num}.sh")
                rec.update({"slurm_id": sid, "attempt": attempt + 1, "resources": new_res, "submitted_epoch": time.time(),
                            "last_state": "PENDING"})
                self.save_state()
                self.write_status(num, {"id": j["id"], "state": "SUBMITTED", "slurm_id": sid, "worker": self.a.name,
                                        "attempt": attempt + 1, "retry_reason": state, "resources": new_res,
                                        "history": rec["history"], "submitted_utc": now()},
                                  f"results: job {num} RETRY {attempt + 1} after {state}")
                self.log(f"job {num} {state} -> resubmitted as Slurm {sid} (attempt {attempt + 1}, {new_res})")
                continue
            self.collect(j, state, rec["hours_so_far"], {"slurm_id": rec["slurm_id"], "attempts": attempt,
                                                         "history": rec["history"]},
                         gpus_hours=sum(h["hours"] * int(h["resources"].get("gpus", 1)) for h in rec["history"]))

    def heartbeat(self, pending: int):
        """Push results/_worker/<name>.json when work is pending (at most hourly) or every 12 h otherwise."""
        p = self.results / "_worker" / f"{self.a.name}.json"
        last = json.loads(p.read_text()).get("epoch", 0) if p.exists() else 0
        due = (pending and time.time() - last > 3600) or time.time() - last > 12 * 3600
        if not due:
            return
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"worker": self.a.name, "host": socket.gethostname(), "utc": now(), "epoch": time.time(),
                                 "in_flight": sorted(self.state), "pending_seen": pending,
                                 "node_hours_used": round(self.node_hours_used(), 3)}, indent=2))
        self.commit_push(f"results: heartbeat {self.a.name}")

    def tick(self):
        self.sync()
        all_jobs = self.jobs()
        by_num = {j["_num"]: j for j in all_jobs}
        if self.a.mode == "slurm":
            # recover in-flight jobs from the results branch if local state was lost
            for num in by_num:
                st = self.status_of(num)
                if st and st.get("state") == "SUBMITTED" and st.get("worker") == self.a.name and num not in self.state:
                    self.state[num] = {"slurm_id": st["slurm_id"], "submitted_utc": st.get("submitted_utc"),
                                       "submitted_epoch": time.time(), "attempt": st.get("attempt", 1),
                                       "resources": st.get("resources") or by_num[num]["resources"],
                                       "history": st.get("history", [])}
            self.poll_slurm(by_num)
        new = 0
        for j in all_jobs:
            ok, why = self.eligible(j)
            if not ok:
                if why.startswith("invalid") or why.startswith("commit not"):
                    if j.get("where") in (self.a.name, "any") and self.status_of(j["_num"]) is None:
                        self.write_status(j["_num"], {"id": j.get("id"), "state": "REFUSED", "reason": why, "worker": self.a.name,
                                                      "finished_utc": now()}, f"results: job {j['_num']} REFUSED")
                        self.log(f"job {j['_num']} refused: {why}")
                continue
            if self.a.mode == "slurm":
                if new >= self.a.max_new:
                    break
                est = hms_to_hours(j["resources"]["time"]) * int(j["resources"]["gpus"]) / 4
                if self.node_hours_used() + est > self.a.budget_node_hours:
                    self.write_status(j["_num"], {"id": j["id"], "state": "REFUSED", "reason": "node-hour budget",
                                                  "worker": self.a.name, "finished_utc": now()}, f"results: job {j['_num']} REFUSED (budget)")
                    continue
                script = self.prepare(j)
                if self.a.dry_run:
                    self.log(f"dry run: would sbatch {script}")
                    continue
                sid = self.submit_slurm(j, script)
                self.state[j["_num"]] = {"slurm_id": sid, "submitted_utc": now(), "submitted_epoch": time.time(),
                                         "attempt": 1, "resources": j["resources"]}
                self.save_state()
                self.write_status(j["_num"], {"id": j["id"], "state": "SUBMITTED", "slurm_id": sid, "worker": self.a.name,
                                              "submitted_utc": now()}, f"results: job {j['_num']} SUBMITTED")
                self.log(f"job {j['_num']} submitted as Slurm {sid}")
                new += 1
            else:
                script = self.prepare(j)
                if self.a.dry_run:
                    self.log(f"dry run: would run {script}")
                    break
                self.state[j["_num"]] = {"local": True, "started_utc": now()}
                self.save_state()
                state, hours = self.run_local(j, script)
                self.collect(j, state, hours, {})
                break  # at most one local job per tick
        pending = sum(1 for j in all_jobs if j.get("where") in (self.a.name, "any") and self.status_of(j["_num"]) is None)
        self.heartbeat(pending + len(self.state))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--name", required=True, help="worker name used in jobs' `where:` (perlmutter)")
    p.add_argument("--mode", choices=("slurm", "local"), required=True)
    p.add_argument("--base", required=True, help="worker directory (clones, run worktrees, state)")
    p.add_argument("--repo", required=True, help="git URL with push rights to the results branch (deploy key)")
    p.add_argument("--account", default="", help="NERSC project (slurm mode)")
    p.add_argument("--qos", default="shared")
    p.add_argument("--env-prefix", default="", help="conda env prefix activated inside Slurm jobs")
    p.add_argument("--python", default="", help="python executable for local mode")
    p.add_argument("--threads", type=int, default=4, help="CPU threads for local jobs")
    p.add_argument("--budget-node-hours", type=float, default=50.0)
    p.add_argument("--max-new", type=int, default=2, help="max new Slurm submissions per tick")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--no-push", action="store_true", help="testing: commit results locally only")
    a = p.parse_args()
    if a.mode == "slurm" and not (a.account and a.env_prefix):
        p.error("slurm mode needs --account and --env-prefix")
    w = Worker(a)
    lock = open(w.base / "worker.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("another tick is running; exiting")
        return
    try:
        w.tick()
    except Exception as e:  # noqa: BLE001 - a failed tick must not leave anything half-done; the next tick retries
        import traceback

        with open(w.base / "tick_errors.log", "a") as fh:
            fh.write(f"[{now()}] {e!r}\n{traceback.format_exc()}\n")
        print(f"tick failed: {e!r} (see {w.base / 'tick_errors.log'}); the next tick will retry")
        sys.exit(1)
    finally:
        fcntl.flock(lock, fcntl.LOCK_UN)


if __name__ == "__main__":
    main()
