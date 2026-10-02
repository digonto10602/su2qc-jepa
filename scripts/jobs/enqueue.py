#!/usr/bin/env python
"""Queue a job for a remote worker (decisions/003).  Writes the next numbered jobs/NNN_<slug>.yaml; you then commit
and push it (`--push` does both).  The job runs at the current HEAD, which must already be on origin/main.

  python scripts/jobs/enqueue.py train "v1_base: 5 seeds, 200 epochs, masked" --prompt prompts/002 --time 04:00:00 \
      --step "python scripts/make_dataset.py --name main --n-traj 20000 --out data/main" \
      --step "python scripts/train_jepa.py --data data/main --name v1_base --epochs 200 --seeds 5 --masked" \
      --output runs/v1_base --output data/main/manifest.json --push
"""
import argparse
import subprocess
import sys

from su2qc_jepa.jobs import validate_job
from su2qc_jepa.repo.artifacts import new_artifact


def git(*a, check=True):
    r = subprocess.run(["git", *a], capture_output=True, text=True)
    if check and r.returncode:
        sys.exit(f"git {' '.join(a)} failed: {r.stderr.strip()}")
    return r.stdout.strip(), r.returncode


p = argparse.ArgumentParser()
p.add_argument("kind", choices=("train", "twin", "dataset", "eval", "check"))
p.add_argument("title")
p.add_argument("--where", default="perlmutter", choices=("perlmutter",))
p.add_argument("--step", action="append", required=True, help="'python scripts/<allowed>.py ...' (repeatable, run in order)")
p.add_argument("--output", action="append", default=[], help="path (file or folder) to publish back (repeatable)")
p.add_argument("--gpus", type=int, default=1)
p.add_argument("--time", default="04:00:00", help="wall-clock limit HH:MM:SS")
p.add_argument("--qos", default="shared")
p.add_argument("--prompt", help="prompt id that asked for this job, e.g. prompts/002")
p.add_argument("--milestone")
p.add_argument("--push", action="store_true", help="commit the job file and push to origin/main")
a = p.parse_args()

git("fetch", "-q", "origin")
head, _ = git("rev-parse", "HEAD")
_, rc = git("merge-base", "--is-ancestor", head, "origin/main", check=False)
if rc:
    sys.exit(f"HEAD {head[:8]} is not on origin/main - commit and push the code first, then enqueue")
data = {"kind": a.kind, "where": a.where, "commit": head, "prompt": a.prompt, "milestone": a.milestone,
        "steps": a.step, "outputs": a.output or ["runs"], "resources": {"gpus": a.gpus, "time": a.time, "qos": a.qos}}
probs = validate_job({"id": "jobs/000", "title": a.title, "author": "x", "created_utc": "x", **data})
if probs:
    sys.exit("invalid job: " + "; ".join(probs))
path = new_artifact(".", "jobs", a.title, author="claude-code", data=data)
print(path)
if a.push:
    git("add", str(path), "jobs/INDEX.md")
    git("commit", "-qm", f"job: {path.stem} ({a.kind} on {a.where})")
    git("push", "-q", "origin", "HEAD:main")
    print("pushed; the worker picks it up at its next tick. Check: python scripts/jobs/status.py")
else:
    print(f"next: git add {path} jobs/INDEX.md && git commit -m 'job: {path.stem}' && git push")
