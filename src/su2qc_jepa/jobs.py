"""Job requests for the Perlmutter worker — decisions/004 (queue introduced in decisions/003).

A job is a numbered YAML file `jobs/NNN_<slug>.yaml` on the `main` branch, written on the laptop by
`scripts/jobs/enqueue.py` and never edited afterwards.  A worker (scripts/worker/worker.py, started by
`scrontab` on Perlmutter) pulls `main`, runs jobs addressed to it at the
exact commit named in the file, and pushes status and outputs to the separate `results` branch:

    results/<NNN>/status.json      state, timings, node-hours, output sizes, worker host
    results/<NNN>/log.txt          last lines of the job's output
    results/<NNN>/outputs/<path>   the files listed under `outputs:` (e.g. runs/v1_base/...)

The laptop never connects to Perlmutter; the worker never pushes to `main`.

Safety: every command step must be `python scripts/<allowed>.py ...` with the script in
ALLOWED_SCRIPTS, so a worker only ever runs this repository's own entry points.
"""
from __future__ import annotations

import re
import shlex
from pathlib import Path

__all__ = ["ALLOWED_SCRIPTS", "WHERE", "KINDS", "REQUIRED", "validate_job", "parse_steps", "MAX_OUTPUT_MB", "MAX_ATTEMPTS",
           "retry_resources"]

ALLOWED_SCRIPTS = {"make_dataset.py", "train_jepa.py", "run_twin.py", "residual_eval.py", "run_gate.py", "env_check.py"}
WHERE = ("perlmutter",)  # the laptop runs light work itself through scripts/run.py (decisions/004)
KINDS = ("train", "twin", "dataset", "eval", "check")
REQUIRED = ("id", "title", "author", "created_utc", "kind", "where", "commit", "steps", "outputs", "resources")
MAX_OUTPUT_MB = 50.0
MAX_ATTEMPTS = 3            # first run + up to two automatic resubmissions
MAX_TIME_HOURS = 47.9       # shared QOS limit is 48 h
MAX_SHARED_GPUS = 2         # shared QOS: at most half a node


def _hms(h: float) -> str:
    s = int(round(h * 3600))
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"


def retry_resources(res: dict, state: str) -> dict | None:
    """Self-healing rule for a finished Slurm job: new resources for a resubmission, or None (do not retry).

    TIMEOUT -> double the wall-clock limit (cap 48 h); OUT_OF_MEMORY -> double GPUs and CPUs (cap 2 GPUs, i.e. twice the
    memory on the shared queue); NODE_FAIL / PREEMPTED / BOOT_FAIL / LOST -> same resources.  FAILED (a program error),
    CANCELLED and COMPLETED are never retried.
    """
    r = dict(res)
    if state == "TIMEOUT":
        h, m, sec = (int(x) for x in str(r["time"]).split(":"))
        cur = h + m / 60 + sec / 3600
        if cur >= MAX_TIME_HOURS:
            return None
        r["time"] = _hms(min(2 * cur, MAX_TIME_HOURS))
        return r
    if state == "OUT_OF_MEMORY":
        g = int(r.get("gpus", 1))
        if g >= MAX_SHARED_GPUS:
            return None
        r["gpus"] = min(2 * max(g, 1), MAX_SHARED_GPUS)
        r["cpus"] = 32 * r["gpus"]
        return r
    if state in ("NODE_FAIL", "PREEMPTED", "BOOT_FAIL", "LOST"):
        return r
    return None


_SHA = re.compile(r"^[0-9a-f]{40}$")


def parse_steps(steps: list[str]) -> list[list[str]]:
    """Split each step into argv and check it against the allowlist (raises ValueError)."""
    out = []
    for st in steps:
        argv = shlex.split(st)
        if len(argv) < 2 or argv[0] != "python" or not argv[1].startswith("scripts/"):
            raise ValueError(f"step must be 'python scripts/<name>.py ...': {st!r}")
        name = argv[1].split("/", 1)[1]
        if name not in ALLOWED_SCRIPTS:
            raise ValueError(f"script {name} not in the worker allowlist {sorted(ALLOWED_SCRIPTS)}")
        if any(ch in st for ch in (";", "&&", "||", "|", "`", "$(", ">", "<")):
            raise ValueError(f"shell operators are not allowed in a step: {st!r}")
        out.append(argv)
    return out


def validate_job(job: dict, expected_id: str | None = None, root: str | Path | None = None) -> list[str]:
    problems = []
    for k in REQUIRED:
        if k not in job or job[k] in (None, "", []):
            problems.append(f"job lacks '{k}'")
    if problems:
        return problems
    if expected_id and job["id"] != expected_id:
        problems.append(f"id '{job['id']}' != '{expected_id}'")
    if job["kind"] not in KINDS:
        problems.append(f"kind '{job['kind']}' not in {KINDS}")
    if job["where"] not in WHERE:
        problems.append(f"where '{job['where']}' not in {WHERE}")
    if not _SHA.match(str(job["commit"])):
        problems.append("commit must be a full 40-character git hash")
    try:
        parse_steps(job["steps"])
    except ValueError as e:
        problems.append(str(e))
    for o in job["outputs"]:
        if o.startswith("/") or ".." in Path(o).parts:
            problems.append(f"output path must be relative inside the repository: {o}")
    res = job["resources"]
    for k in ("gpus", "time"):
        if k not in res:
            problems.append(f"resources lacks '{k}'")
    if not re.match(r"^\d{1,2}:\d{2}:\d{2}$", str(res.get("time", ""))):
        problems.append("resources.time must be HH:MM:SS")
    return problems
