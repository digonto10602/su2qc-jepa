"""Laptop runner (decisions/004): classification, admission, self-healing decisions, and a real capped run."""
import json
import os
import subprocess
import sys
from pathlib import Path

from su2qc_jepa.localrun import Policy, Probe, RunResult, admit, classify, heal_decision, is_heavy

ROOT = Path(__file__).resolve().parents[1]
POL = Policy()
LAPTOP = dict(mem_total_gb=62.7, swap_free_gb=0.0, logical_cpus=12)


def test_classification():
    big = classify(["python", "scripts/train_jepa.py", "--data", "data/main", "--name", "x", "--epochs", "200", "--seeds", "5", "--masked"], POL)
    assert is_heavy(big, POL) and big.queueable
    small = classify(["python", "scripts/make_dataset.py", "--name", "m", "--n-traj", "20000", "--out", "data/m"], POL)
    assert not is_heavy(small, POL) and small.queueable and small.est_minutes < 5
    gpu = classify(["python", "scripts/run_twin.py", "--name", "d", "--device", "GPU"], POL)
    assert is_heavy(gpu, POL)
    adhoc = classify(["python", "-c", "print(1)"], POL)
    assert not adhoc.queueable and not is_heavy(adhoc, POL)
    assert classify(["python", "scripts/train_jepa.py"], POL, threads=12).threads == POL.max_threads


def test_admission_on_the_64gb_laptop():
    req = classify(["python", "scripts/make_dataset.py", "--n-traj", "100", "--out", "d"], POL)
    assert admit(req, POL, Probe(mem_available_gb=50.0, load1=1.0, **LAPTOP))[0]
    ok, why = admit(req, POL, Probe(mem_available_gb=17.0, load1=1.0, **LAPTOP))
    assert not ok and "reserve" in why          # other sessions are using the memory
    ok, why = admit(req, POL, Probe(mem_available_gb=50.0, load1=9.5, **LAPTOP))
    assert not ok and "CPU" in why              # the machine is busy


def test_heal_decisions():
    req = classify(["python", "scripts/train_jepa.py", "--epochs", "2"], POL)
    oom = RunResult(137, 10, False, True, None, "Killed", "cgroup")
    action, _ = heal_decision(oom, req, POL, 1, Probe(mem_available_gb=50.0, load1=1.0, **LAPTOP))
    assert action == "retry" and req.mem_gb == 8.0
    assert heal_decision(oom, req, POL, 2, Probe(mem_available_gb=50.0, load1=1.0, **LAPTOP))[0] == "queue"
    timeout = RunResult(-15, 100, True, False, None, "", "cgroup")
    assert heal_decision(timeout, req, POL, 1)[0] == "queue"
    bug = RunResult(1, 3, False, False, 0.1, "ZeroDivisionError: division by zero", "cgroup")
    assert heal_decision(bug, req, POL, 1)[0] == "fail"
    assert heal_decision(RunResult(0, 3, False, False, 0.1, "", "cgroup"), req, POL, 1)[0] == "done"


def test_run_py_retries_after_memory_limit(tmp_path):
    """Real run: an allocation that exceeds the 0.5 GB request fails, the runner retries once with 1 GB and succeeds.
    The size depends on the limiter: a cgroup limit is exact; the fallback address-space limit is 3x the request."""
    from su2qc_jepa.localrun import _systemd_scope_ok

    alloc = 0.8e9 if _systemd_scope_ok() else 2.0e9
    cfg = tmp_path / "compute.yaml"
    cfg.write_text("laptop:\n  reserve_mem_gb: 0.5\n  free_cpus: 0\n  max_wait_minutes: 0.2\n  poll_seconds: 1\n"
                   f"  lock_path: {tmp_path}/lock\n")
    env = {**os.environ, "SU2QC_COMPUTE_CONFIG": str(cfg)}
    code = f"import numpy as np; a = np.ones(int({alloc} / 8)); print('ok', a.nbytes)"
    r = subprocess.run([sys.executable, str(ROOT / "scripts/run.py"), "--name", "memtest", "--mem", "0.5", "--threads", "1", "--",
                        "python", "-c", code], cwd=tmp_path, env=env, capture_output=True, text=True, timeout=300)
    out = r.stdout + r.stderr
    if "limiter none" in out:  # no prlimit and no systemd on this machine: nothing to test
        return
    assert r.returncode == 0, out
    assert "retry once with 1 GB" in out and "done" in out, out
    ledger = [json.loads(line) for line in (tmp_path / ".local_runs/ledger.jsonl").read_text().splitlines()]
    assert [e["decision"] for e in ledger] == ["retry", "done"]
    assert [e["mem_gb"] for e in ledger] == [0.5, 1.0], "the ledger must record the limit each attempt actually ran with"


def test_job_dies_with_the_runner(tmp_path):
    """If scripts/run.py is killed (session closed), its job must not live on as an orphan after the lock is released."""
    import signal
    import time

    cfg = tmp_path / "compute.yaml"
    cfg.write_text(f"laptop:\n  reserve_mem_gb: 0.5\n  free_cpus: 0\n  poll_seconds: 1\n  lock_path: {tmp_path}/lock\n")
    mark = f"orphan_marker_{os.getpid()}"
    r = subprocess.Popen([sys.executable, str(ROOT / "scripts/run.py"), "--name", "orphan", "--no-queue", "--threads", "1", "--",
                          "python", "-c", f"import time; x = '{mark}'; time.sleep(120)"], cwd=tmp_path,
                         env={**os.environ, "SU2QC_COMPUTE_CONFIG": str(cfg)}, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def jobs():
        found = []
        for d in os.listdir("/proc"):
            if d.isdigit():
                try:
                    cl = Path(f"/proc/{d}/cmdline").read_bytes().decode(errors="replace")
                except OSError:
                    continue
                if mark in cl and "run.py" not in cl:
                    found.append(int(d))
        return found

    for _ in range(60):
        if jobs():
            break
        time.sleep(0.5)
    assert jobs(), "the job never started"
    os.kill(r.pid, signal.SIGKILL)
    r.wait()
    for _ in range(20):
        if not jobs():
            break
        time.sleep(0.25)
    assert not jobs(), "the job outlived its runner"
