"""Resource-aware, self-healing execution on the laptop (decisions/004).

The laptop (64 GB RAM, 6-core i7-8750H, GTX 1060 Max-Q not used) is shared with other Claude sessions, so
every computation from this project goes through `scripts/run.py`, which uses this module to:

1. **classify** the command: heavy (estimated above `heavy_minutes` at the granted threads, or asks for a GPU)
   → always sent to Perlmutter through the job queue; light → may run here;
2. **admit** it only if the machine has room *now*: MemAvailable minus the request stays above a reserve kept
   for other programs, and the 1-minute load plus the requested threads leaves free cores; only one su2qc
   computation at a time across all sessions (a lock file).  If there is no room it waits (bounded), then
   sends the job to Perlmutter if it can be queued;
3. **run it capped**: lowest CPU/I/O priority, thread caps for every math library, a memory ceiling (cgroup via
   `systemd-run --user --scope` when available, otherwise an address-space limit), a wall-clock limit, and
   `oom_score_adj = 1000` so that under memory pressure the kernel kills this job, never another session;
4. **heal**: a resource failure (memory kill, address-space exhaustion, timeout) is retried once with a larger
   memory ceiling if the machine has room, otherwise the job is sent to Perlmutter; a program error (an
   ordinary exception) is not retried — it is a bug and is reported with the log tail.

Every attempt is appended to `.local_runs/ledger.jsonl` (git-ignored) with its probe, limits and outcome.
"""
from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

import yaml

__all__ = ["Probe", "probe", "Policy", "load_policy", "Request", "classify", "admit", "run_capped", "is_resource_failure",
           "RunResult", "heal_decision"]

OOM_PATTERNS = re.compile(r"MemoryError|Cannot allocate memory|cannot allocate memory|std::bad_alloc|out of memory|Killed", re.I)


@dataclass
class Probe:
    mem_total_gb: float
    mem_available_gb: float
    swap_free_gb: float
    logical_cpus: int
    load1: float
    utc: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))


def probe() -> Probe:
    info = {}
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            k, v = line.split(":", 1)
            info[k] = float(v.split()[0]) / 1024 / 1024  # kB -> GB
    except OSError:
        pass
    load1 = os.getloadavg()[0] if hasattr(os, "getloadavg") else 0.0
    return Probe(mem_total_gb=round(info.get("MemTotal", 0.0), 2), mem_available_gb=round(info.get("MemAvailable", 0.0), 2),
                 swap_free_gb=round(info.get("SwapFree", 0.0), 2), logical_cpus=os.cpu_count() or 1, load1=round(load1, 2))


@dataclass
class Policy:
    reserve_mem_gb: float = 16.0      # leave this much MemAvailable for other programs (scaled down on small machines)
    reserve_fraction: float = 0.25    # ... but never more than this fraction of total RAM
    default_mem_gb: float = 4.0
    max_mem_gb: float = 16.0          # never give one su2qc job more than this on the laptop
    default_threads: int = 2
    max_threads: int = 4
    free_cpus: int = 2                # load1 + threads must stay <= logical_cpus - free_cpus
    heavy_minutes: float = 20.0       # estimated laptop minutes above this -> Perlmutter
    max_wait_minutes: float = 20.0    # wait at most this long for room, then queue (or give up)
    poll_seconds: float = 30.0
    default_timeout_minutes: float = 40.0
    lock_path: str = "~/.cache/su2qc-jepa/compute.lock"


def load_policy(path: str | Path | None = None) -> Policy:
    path = path or os.environ.get("SU2QC_COMPUTE_CONFIG", "configs/compute.yaml")
    try:
        cfg = yaml.safe_load(Path(path).read_text()).get("laptop", {})
    except OSError:
        cfg = {}
    pol = Policy()
    for k in asdict(pol):
        if k in cfg:
            setattr(pol, k, type(getattr(pol, k))(cfg[k]))
    return pol


@dataclass
class Request:
    argv: list[str]
    mem_gb: float
    threads: int
    est_minutes: float | None
    needs_gpu: bool
    queueable: bool               # a single allowlisted `python scripts/<x>.py ...` step
    reason: str


# Per-script defaults (measured 2 Oct 2026 on 2 cores; memory peaks + generous margin)
_SCRIPT_MEM = {"train_jepa.py": 4.0, "run_twin.py": 3.0, "make_dataset.py": 2.0, "residual_eval.py": 3.0,
               "run_gate.py": 3.0, "hw_dry_run.py": 3.0, "smoke.sh": 4.0}


def _arg(argv: list[str], name: str, default=None, cast=float):
    if name in argv:
        i = argv.index(name)
        vals = []
        for v in argv[i + 1:]:
            if v.startswith("--"):
                break
            vals.append(v)
        if not vals:
            return True
        try:
            return cast(vals[0]) if len(vals) == 1 else [cast(x) for x in vals]
        except ValueError:
            return default
    return default


def _manifest_ntrain(data_dir: str | None) -> int | None:
    if not data_dir:
        return None
    m = Path(data_dir) / "manifest.json"
    if m.exists():
        try:
            return int(json.loads(m.read_text())["splits"]["train"])
        except (KeyError, ValueError, json.JSONDecodeError):
            return None
    return None


def estimate_minutes(argv: list[str], threads: int) -> float | None:
    """Laptop minutes for the known scripts from the measured unit costs (2-core reference), else None."""
    from .compute import _UNIT_COST

    script = next((Path(a).name for a in argv if a.startswith("scripts/")), "")
    speed = max(1.0, threads / 2.0) ** 0.8  # sub-linear thread scaling
    if script == "make_dataset.py":
        n = _arg(argv, "--n-traj", 200)
        return n * _UNIT_COST["dataset_per_traj"] / speed / 60
    if script == "train_jepa.py":
        epochs = _arg(argv, "--epochs", 40)
        seeds = _arg(argv, "--seeds", 1)
        masked = 2 if "--masked" in argv else 1
        n_train = _manifest_ntrain(_arg(argv, "--data", None, str)) or 0.6 * 20000
        base = n_train * epochs * seeds * masked * _UNIT_COST["train_per_traj_epoch"]
        baselines = 120 + 0.2 * base  # ridge/AR/MLP baselines, measured to be a modest fraction
        return (base + baselines) / speed / 60
    if script == "run_twin.py":
        depths = _arg(argv, "--depths", [1, 2, 4, 6, 8])
        masses = _arg(argv, "--masses", [0.3, 0.375, 0.5])
        seeds = _arg(argv, "--seeds", 5)
        arms = 2
        nd = len(depths) if isinstance(depths, list) else 1
        nm = len(masses) if isinstance(masses, list) else 1
        n_circ = nd * nm * seeds * arms * 2
        return n_circ * _UNIT_COST["twin_per_circuit"] / speed / 60
    return None


def classify(argv: list[str], pol: Policy, mem_gb: float | None = None, threads: int | None = None,
             est_minutes: float | None = None) -> Request:
    from .jobs import parse_steps

    script = next((Path(a).name for a in argv if a.startswith("scripts/")), argv[0] if argv else "")
    threads = min(threads or pol.default_threads, pol.max_threads)
    mem = min(mem_gb or _SCRIPT_MEM.get(script, pol.default_mem_gb), pol.max_mem_gb)
    needs_gpu = any(x in argv for x in ("cuda", "GPU")) or os.environ.get("SU2QC_DEVICE") == "cuda"
    est = est_minutes if est_minutes is not None else estimate_minutes(argv, threads)
    try:
        parse_steps([shlex.join(argv)])
        queueable = True
    except ValueError:
        queueable = False
    if needs_gpu:
        reason = "needs a GPU (the laptop GPU is not used) -> Perlmutter"
    elif est is not None and est > pol.heavy_minutes:
        reason = f"estimated {est:.0f} min > {pol.heavy_minutes:.0f} min on the laptop -> Perlmutter"
    else:
        reason = f"light (estimate {'unknown' if est is None else f'{est:.1f} min'}) -> laptop if there is room"
    return Request(list(argv), mem, threads, est, needs_gpu, queueable, reason)


def is_heavy(req: Request, pol: Policy) -> bool:
    return req.needs_gpu or (req.est_minutes is not None and req.est_minutes > pol.heavy_minutes)


def admit(req: Request, pol: Policy, pr: Probe | None = None) -> tuple[bool, str]:
    pr = pr or probe()
    reserve = min(pol.reserve_mem_gb, pol.reserve_fraction * pr.mem_total_gb) if pr.mem_total_gb else pol.reserve_mem_gb
    if pr.mem_total_gb and pr.mem_available_gb - req.mem_gb < reserve:
        return False, (f"memory: {pr.mem_available_gb:.1f} GB available, request {req.mem_gb:.1f} GB would leave "
                       f"less than the {reserve:.1f} GB reserve")
    free = min(pol.free_cpus, max(0, pr.logical_cpus - req.threads))
    if pr.load1 + req.threads > pr.logical_cpus - free:
        return False, f"CPU: load {pr.load1:.2f} + {req.threads} threads > {pr.logical_cpus} - {free} free cores"
    return True, f"ok: {pr.mem_available_gb:.1f} GB available, load {pr.load1:.1f}/{pr.logical_cpus}"


@dataclass
class RunResult:
    returncode: int
    seconds: float
    timed_out: bool
    oom: bool
    peak_rss_gb: float | None
    log_tail: str
    limiter: str


def _limit_env(threads: int) -> dict:
    t = str(threads)
    return {**os.environ, "SU2QC_THREADS": t, "OMP_NUM_THREADS": t, "MKL_NUM_THREADS": t, "OPENBLAS_NUM_THREADS": t,
            "NUMEXPR_NUM_THREADS": t, "SU2QC_DEVICE": os.environ.get("SU2QC_DEVICE", "cpu"), "PYTHONHASHSEED": "0"}


def _systemd_scope_ok() -> bool:
    """True only if a user scope can really enforce MemoryMax: systemd user manager running AND the cgroup-v2 memory
    controller delegated to it.  Without delegation systemd accepts MemoryMax but does not enforce it, so we fall back
    to the address-space limit instead of trusting a ceiling that is not there."""
    if not shutil.which("systemd-run") or not shutil.which("systemctl"):
        return False
    r = subprocess.run(["systemctl", "--user", "show-environment"], capture_output=True)
    if r.returncode != 0:
        return False
    uid = os.getuid()
    ctrl = Path(f"/sys/fs/cgroup/user.slice/user-{uid}.slice/user@{uid}.service/cgroup.controllers")
    try:
        return "memory" in ctrl.read_text().split()
    except OSError:
        return False


def _preexec():  # runs in the child before exec
    os.setsid()
    try:  # if the runner itself dies (session closed, killed), its job dies too: no orphan keeps memory after the lock is gone
        import ctypes

        ctypes.CDLL("libc.so.6", use_errno=True).prctl(1, signal.SIGTERM)  # PR_SET_PDEATHSIG
    except (OSError, AttributeError):
        pass
    try:
        os.nice(19)
    except OSError:
        pass
    try:
        Path("/proc/self/oom_score_adj").write_text("1000")  # kernel kills us first, never another session
    except OSError:
        pass


def run_capped(argv: list[str], mem_gb: float, threads: int, timeout_s: float, log_path: Path) -> RunResult:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    prefix: list[str] = []
    if shutil.which("ionice"):
        prefix += ["ionice", "-c", "3"]
    if _systemd_scope_ok():
        limiter = "cgroup"
        cmd = ["systemd-run", "--user", "--scope", "--quiet", "-p", f"MemoryMax={int(mem_gb * 1024)}M", "-p", "MemorySwapMax=0",
               "-p", f"CPUQuota={threads * 100}%", *prefix, *argv]
    elif shutil.which("prlimit"):
        limiter = "address-space"
        # 3x: Python/PyTorch reserve much more virtual address space than they touch (verified: 1x aborts torch import)
        cmd = ["prlimit", f"--as={int(mem_gb * 3 * 1024**3)}", *prefix, *argv]
    else:
        limiter = "none"
        cmd = [*prefix, *argv]
    t0 = time.time()
    timed_out = False
    before = os.wait4 if hasattr(os, "wait4") else None
    with open(log_path, "w") as fh:
        proc = subprocess.Popen(cmd, stdout=fh, stderr=subprocess.STDOUT, env=_limit_env(threads), preexec_fn=_preexec)
        peak = None
        try:
            if before:
                deadline = t0 + timeout_s
                while True:
                    pid, status, ru = os.wait4(proc.pid, os.WNOHANG)
                    if pid:
                        proc.returncode = os.waitstatus_to_exitcode(status)
                        peak = ru.ru_maxrss / 1024 / 1024  # kB -> GB (Linux)
                        break
                    if time.time() > deadline:
                        raise subprocess.TimeoutExpired(cmd, timeout_s)
                    time.sleep(0.2)
            else:
                proc.wait(timeout=timeout_s)
        except subprocess.TimeoutExpired:
            timed_out = True
            try:
                os.killpg(proc.pid, signal.SIGTERM)
                time.sleep(5)
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            proc.wait()
    tail = "\n".join(log_path.read_text(errors="replace").splitlines()[-40:])
    rc = proc.returncode
    oom = (rc in (-9, 137) and not timed_out) or bool(OOM_PATTERNS.search(tail) and rc != 0)
    return RunResult(rc, round(time.time() - t0, 1), timed_out, oom, None if peak is None else round(peak, 2), tail, limiter)


def is_resource_failure(r: RunResult) -> bool:
    return r.timed_out or r.oom


def heal_decision(r: RunResult, req: Request, pol: Policy, attempt: int, pr: Probe | None = None) -> tuple[str, str]:
    """What to do after an attempt: ('done'|'retry'|'queue'|'fail', why)."""
    if r.returncode == 0 and not r.timed_out:
        return "done", "completed"
    if not is_resource_failure(r):
        return "fail", f"program error (exit {r.returncode}) - not retried; read the log tail"
    if r.timed_out:
        return ("queue", "timed out on the laptop: heavier than estimated -> Perlmutter") if req.queueable else \
               ("fail", "timed out and cannot be queued (not a single allowlisted script)")
    # memory failure
    new_mem = min(req.mem_gb * 2, pol.max_mem_gb)
    if attempt == 1 and new_mem > req.mem_gb:
        req.mem_gb = new_mem
        ok, why = admit(req, pol, pr)
        if ok:
            return "retry", f"memory limit hit -> retry once with {new_mem:g} GB ({why})"
    if req.queueable:
        return "queue", "memory limit hit and no room for a larger limit on the laptop -> Perlmutter"
    return "fail", "memory limit hit and the command cannot be queued"


def ledger_append(entry: dict, path: str | Path = ".local_runs/ledger.jsonl"):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a") as fh:
        fh.write(json.dumps(entry) + "\n")
