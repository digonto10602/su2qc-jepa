#!/usr/bin/env python
"""The only way to run a computation for this project on the laptop (decisions/004).

  python scripts/run.py -- python -m pytest -q
  python scripts/run.py --name ds_main -- python scripts/make_dataset.py --name main --n-traj 20000 --out data/main
  python scripts/run.py --name v1_base -- python scripts/train_jepa.py --data data/main --name v1_base --epochs 200 --seeds 5 --masked
         (heavy -> queued for Perlmutter automatically; add --push to commit+push the job, otherwise it prints the command)

What it does: classify (heavy or GPU -> Perlmutter queue), wait for room on the laptop (memory reserve, free cores,
one su2qc computation at a time across all sessions), run capped (nice 19, idle I/O, thread caps, memory ceiling,
time limit, oom_score_adj 1000), and heal (one retry with more memory after a memory kill if there is room;
otherwise, or after a timeout, queue it for Perlmutter).  Program errors are not retried.

Exit codes: 0 done here | 10 queued for Perlmutter | 1 failed | 2 not run (no room and cannot be queued) | 3 bad usage
"""
import argparse
import fcntl
import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from su2qc_jepa.localrun import (  # noqa: E402
    admit,
    classify,
    heal_decision,
    is_heavy,
    ledger_append,
    load_policy,
    probe,
    run_capped,
)

p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
p.add_argument("--name", default=None, help="short name for logs and for the job if it is queued")
p.add_argument("--mem", type=float, help="memory request in GB (default per script)")
p.add_argument("--threads", type=int, help="CPU threads (default 2, max 4)")
p.add_argument("--est-minutes", type=float, help="override the laptop time estimate")
p.add_argument("--timeout-min", type=float, help="laptop wall-clock limit in minutes")
p.add_argument("--output", action="append", default=[], help="outputs to publish if queued (default: guessed)")
p.add_argument("--pm-time", default=None, help="Perlmutter wall-clock limit HH:MM:SS if queued (default from estimate)")
p.add_argument("--prompt", help="prompt id, recorded in a queued job")
p.add_argument("--no-queue", action="store_true", help="never queue; fail instead")
p.add_argument("--push", action="store_true", help="if queued: commit and push the job file")
p.add_argument("--dry", action="store_true", help="only print the decision")
p.add_argument("cmd", nargs=argparse.REMAINDER)
a = p.parse_args()
cmd = a.cmd[1:] if a.cmd[:1] == ["--"] else a.cmd
if not cmd:
    p.error("give the command after --")
if cmd[0] == "python":
    cmd[0] = sys.executable

pol = load_policy()
req = classify(cmd if cmd[0] != sys.executable else ["python", *cmd[1:]], pol, a.mem, a.threads, a.est_minutes)
req.argv = cmd
name = a.name or ("pytest" if "pytest" in cmd else Path(next((x for x in cmd if x.startswith("scripts/")), cmd[-1])).stem)
run_id = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()) + "-" + uuid.uuid4().hex[:6]
log = Path(".local_runs/logs") / f"{run_id}_{name}.log"
print(f"[run] {name}: {req.reason}; request {req.mem_gb:g} GB, {req.threads} threads")


def guess_outputs(argv):
    s = " ".join(argv)

    def val(flag):
        return argv[argv.index(flag) + 1] if flag in argv and argv.index(flag) + 1 < len(argv) else None

    if "train_jepa.py" in s and val("--name"):
        return [f"runs/{val('--name')}"] + ([f"{val('--data')}/manifest.json"] if val("--data") else [])
    if "make_dataset.py" in s and val("--out"):
        return [f"{val('--out')}/manifest.json", f"{val('--out')}/meta.json"]
    if "run_twin.py" in s and val("--name"):
        return [f"evidence/twin/{val('--name')}"]
    if "residual_eval.py" in s and val("--out"):
        return [val("--out")]
    return ["evidence"]


def dataset_step(argv):
    """If the command reads a dataset, rebuild it on Perlmutter from its manifest (same seed -> same data)."""
    if "--data" not in argv:
        return []
    d = Path(argv[argv.index("--data") + 1])
    m = d / "manifest.json"
    if not m.exists():
        return []
    c = json.loads(m.read_text())["config"]
    fams = " ".join(f["name"] for f in c["families"])
    starts = " ".join(c["starts"])
    return [f"python scripts/make_dataset.py --name {c['name']} --n-traj {c['n_traj']} --steps {c['n_steps_min']} {c['n_steps_max']} "
            f"--families {fams} --carrier {c['carrier']} --starts {starts} --quench-fraction {c['quench_fraction']} "
            f"--seed {c['seed']} --out {d}"]


def queue(reason: str) -> int:
    if a.no_queue or not req.queueable:
        print(f"[run] cannot queue ({'--no-queue' if a.no_queue else 'not a single allowlisted script'}): {reason}")
        return 2
    import shlex

    step = shlex.join(["python", *req.argv[1:]] if req.argv[0] == sys.executable else req.argv)
    est_h = (req.est_minutes or 60) / 60 / 4  # A100 + more threads: rough 4x faster than the laptop estimate
    secs = int(min(max(2 * est_h, 0.5), 47.5) * 3600)
    pm_time = a.pm_time or f"{secs // 3600:02d}:{secs % 3600 // 60:02d}:00"
    enq = [sys.executable, "scripts/jobs/enqueue.py", "train" if "train_jepa" in step else "twin" if "twin" in step else "dataset"
           if "make_dataset" in step else "eval", f"{name}: {reason[:60]}", "--time", pm_time]
    for s in dataset_step(req.argv) + [step]:
        enq += ["--step", s]
    for o in (a.output or guess_outputs(req.argv)):
        enq += ["--output", o]
    if a.prompt:
        enq += ["--prompt", a.prompt]
    if a.push:
        enq.append("--push")
    print(f"[run] -> Perlmutter queue: {reason}")
    r = subprocess.run(enq, capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())
    ledger_append({"run_id": run_id, "name": name, "argv": req.argv, "decision": "queued", "reason": reason,
                   "enqueue_ok": r.returncode == 0, "enqueue_out": (r.stdout or r.stderr)[-400:]})
    return 10 if r.returncode == 0 else 1


if a.dry:
    print(json.dumps({"heavy": is_heavy(req, pol), "queueable": req.queueable, "est_minutes": req.est_minutes,
                      "mem_gb": req.mem_gb, "threads": req.threads, "probe": probe().__dict__}, indent=1))
    sys.exit(0)
if is_heavy(req, pol):
    sys.exit(queue(req.reason))

# wait for the cross-session lock and for room on the laptop
lock_path = Path(os.path.expanduser(pol.lock_path))
lock_path.parent.mkdir(parents=True, exist_ok=True)
lock = open(lock_path, "w")
deadline = time.time() + pol.max_wait_minutes * 60
why = ""
while True:
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        ok, why = admit(req, pol)
        if ok:
            break
        fcntl.flock(lock, fcntl.LOCK_UN)
    except BlockingIOError:
        why = "another su2qc computation is running on this laptop"
    if time.time() > deadline:
        sys.exit(queue(f"no room on the laptop for {pol.max_wait_minutes:.0f} min ({why})"))
    print(f"[run] waiting: {why}", flush=True)
    time.sleep(pol.poll_seconds)

timeout_s = (a.timeout_min or max(pol.default_timeout_minutes, 3 * (req.est_minutes or 0))) * 60
attempt = 1
try:
    while True:
        pr = probe()
        log = log.with_name(f"{run_id}_{name}_a{attempt}.log")
        mem_used = req.mem_gb  # heal_decision may raise req.mem_gb for the next attempt
        print(f"[run] attempt {attempt}: {why}; limits {mem_used:g} GB / {req.threads} threads / {timeout_s / 60:.0f} min; log {log}")
        res = run_capped(req.argv, mem_used, req.threads, timeout_s, log)
        action, reason = heal_decision(res, req, pol, attempt)
        ledger_append({"run_id": run_id, "attempt": attempt, "name": name, "argv": req.argv, "probe": pr.__dict__,
                       "mem_gb": mem_used, "threads": req.threads, "limiter": res.limiter, "returncode": res.returncode,
                       "seconds": res.seconds, "timed_out": res.timed_out, "oom": res.oom, "peak_rss_gb": res.peak_rss_gb,
                       "decision": action, "reason": reason, "log": str(log)})
        print(f"[run] exit {res.returncode} after {res.seconds:.0f} s (peak {res.peak_rss_gb} GB, limiter {res.limiter}) -> {action}: {reason}")
        if action == "done":
            sys.exit(0)
        if action == "retry":
            attempt += 1
            continue
        if action == "queue":
            fcntl.flock(lock, fcntl.LOCK_UN)
            sys.exit(queue(reason))
        print("[run] log tail:\n" + res.log_tail)
        sys.exit(1)
finally:
    try:
        fcntl.flock(lock, fcntl.LOCK_UN)
    except ValueError:
        pass
