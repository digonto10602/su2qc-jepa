"""Job queue (decisions/003): job format, allowlist, and one end-to-end worker tick against a local git remote."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from su2qc_jepa.jobs import parse_steps, validate_job

ROOT = Path(__file__).resolve().parents[1]
SHA = "0" * 40


def good_job(**kw):
    j = {"id": "jobs/000", "title": "t", "author": "claude-code", "created_utc": "2026-10-02T00:00:00Z", "kind": "train",
         "where": "perlmutter", "commit": SHA, "steps": ["python scripts/train_jepa.py --data data/main --name x"],
         "outputs": ["runs/x"], "resources": {"gpus": 1, "time": "04:00:00"}}
    j.update(kw)
    return j


def test_valid_job_passes():
    assert validate_job(good_job(), expected_id="jobs/000") == []


@pytest.mark.parametrize("step", ["python scripts/hw_submit.py submit --confirm", "bash scripts/train_jepa.py",
                                  "python scripts/train_jepa.py; rm -rf ~", "python scripts/train_jepa.py && curl x",
                                  "python -c 'import os'", "python scripts/train_jepa.py > out"])
def test_allowlist_refuses(step):
    with pytest.raises(ValueError):
        parse_steps([step])


def test_validation_catches_bad_fields():
    probs = "\n".join(validate_job(good_job(where="moon", commit="abc", outputs=["../x"], resources={"gpus": 1, "time": "4h"})))
    assert "where" in probs and "commit" in probs and "output path" in probs and "HH:MM:SS" in probs


def _git(cwd, *a):
    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *a], cwd=cwd, check=True, capture_output=True, text=True).stdout


def test_worker_end_to_end_local(tmp_path):
    """Laptop queues a tiny dataset job; a local-mode worker runs it; results land on the `results` branch only."""
    origin = tmp_path / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", str(origin)], check=True)
    laptop = tmp_path / "laptop"

    def ignore(directory, names):
        skip = {"__pycache__", ".pytest_cache", ".ruff_cache", ".git"} | {n for n in names if n.endswith(".egg-info")}
        if Path(directory).resolve() == ROOT:
            skip |= {"data", "runs", "graphify-out", "evidence"}
        if Path(directory).resolve() == ROOT / "jobs":  # start from an empty queue: real job requests are not test input
            skip |= {n for n in names if n[:3].isdigit() and n.endswith(".yaml")}
        return [n for n in names if n in skip]

    shutil.copytree(ROOT, laptop, ignore=ignore)
    _git(laptop, "init", "-q", "-b", "main")
    _git(laptop, "add", "-A")
    _git(laptop, "commit", "-qm", "init")
    _git(laptop, "remote", "add", "origin", str(origin))
    _git(laptop, "push", "-q", "origin", "main")
    env = {**os.environ, "PYTHONPATH": str(laptop / "src"), "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    r = subprocess.run([sys.executable, "scripts/jobs/enqueue.py", "dataset", "tiny dataset", "--gpus", "0",
                        "--time", "00:05:00", "--step", "python scripts/make_dataset.py --name tiny --n-traj 4 --steps 2 2 --families onfam --out data/tiny",
                        "--output", "data/tiny/manifest.json", "--push"], cwd=laptop, env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    job = yaml.safe_load(next((laptop / "jobs").glob("000_*.yaml")).read_text())
    assert job["commit"] == _git(laptop, "rev-parse", "HEAD~1").strip()
    r = subprocess.run([sys.executable, str(laptop / "scripts/worker/worker.py"), "--name", "perlmutter", "--mode", "local",
                        "--base", str(tmp_path / "wk"), "--repo", str(origin), "--python", sys.executable, "--threads", "1"],
                       env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr + r.stdout
    assert "COMPLETED" in r.stdout
    r = subprocess.run([sys.executable, "scripts/jobs/fetch.py", "000"], cwd=laptop, env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr + r.stdout
    man = json.loads((laptop / "data/tiny/manifest.json").read_text())
    assert man["n_traj"] == 4 and len(man["checksum_sha256"]) == 64
    assert json.loads((laptop / "evidence/jobs/000/status.json").read_text())["state"] == "COMPLETED"
    authors = subprocess.run(["git", "log", "--format=%an", "main"], cwd=origin, capture_output=True, text=True).stdout.split()
    assert all(a == "t" for a in authors), "workers must never commit to main"
    results_authors = set(subprocess.run(["git", "log", "--format=%an", "results"], cwd=origin, capture_output=True, text=True).stdout.split())
    assert results_authors == {"su2qc-worker-perlmutter"}


def test_retry_rule():
    from su2qc_jepa.jobs import retry_resources

    assert retry_resources({"gpus": 1, "time": "04:00:00"}, "TIMEOUT")["time"] == "08:00:00"
    assert retry_resources({"gpus": 1, "time": "47:54:00"}, "TIMEOUT") is None
    assert retry_resources({"gpus": 1, "time": "04:00:00"}, "OUT_OF_MEMORY")["gpus"] == 2
    assert retry_resources({"gpus": 2, "time": "04:00:00"}, "OUT_OF_MEMORY") is None
    assert retry_resources({"gpus": 1, "time": "04:00:00"}, "NODE_FAIL") == {"gpus": 1, "time": "04:00:00"}
    assert retry_resources({"gpus": 1, "time": "04:00:00"}, "FAILED") is None


def test_worker_slurm_mode_resubmits_after_timeout(tmp_path):
    """Stand-in sbatch/sacct: the first submission ends in TIMEOUT, the worker resubmits with twice the time, the
    second run completes and is published with both attempts in its history."""
    origin = tmp_path / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", str(origin)], check=True)
    laptop = tmp_path / "laptop"

    def ignore(directory, names):
        skip = {"__pycache__", ".pytest_cache", ".ruff_cache", ".git"} | {n for n in names if n.endswith(".egg-info")}
        if Path(directory).resolve() == ROOT:
            skip |= {"data", "runs", "graphify-out", "evidence", ".local_runs"}
        if Path(directory).resolve() == ROOT / "jobs":  # start from an empty queue: real job requests are not test input
            skip |= {n for n in names if n[:3].isdigit() and n.endswith(".yaml")}
        return [n for n in names if n in skip]

    shutil.copytree(ROOT, laptop, ignore=ignore)
    for args in (("init", "-q", "-b", "main"), ("add", "-A"), ("commit", "-qm", "init"), ("remote", "add", "origin", str(origin)),
                 ("push", "-q", "origin", "main")):
        _git(laptop, *args)
    bin_ = tmp_path / "bin"
    bin_.mkdir()
    st = tmp_path / "slurm"
    st.mkdir()
    (bin_ / "sbatch").write_text(f"""#!/bin/bash
n=$(ls {st} | grep -vc args); id=$((500 + n)); script="${{@: -1}}"
out=""; prev=""; for x in "$@"; do [ "$prev" = "-o" ] && out="$x"; prev="$x"; done
if [ "$n" = "0" ]; then echo TIMEOUT > {st}/$id; else bash "$script" > "$out" 2>&1 && echo COMPLETED > {st}/$id || echo FAILED > {st}/$id; fi
echo "$*" > {st}/$id.args; echo $id
""")
    (bin_ / "sacct").write_text(f"""#!/bin/bash
echo "$(cat {st}/$2)|00:30:00"
""")
    for name in ("module", "conda"):
        (bin_ / name).write_text("#!/bin/bash\ntrue\n")
    for f in bin_.iterdir():
        f.chmod(0o755)
    # keep the host's shell set-up out of the stand-in job: on Perlmutter, exported shell functions (BASH_FUNC_module%%,
    # BASH_FUNC_conda%%) and BASH_ENV re-define the real `module`/`conda`, which then shadow the stand-ins in bin_
    host = {k: v for k, v in os.environ.items() if not k.startswith("BASH_FUNC_") and k not in ("BASH_ENV", "ENV")}
    env = {**host, "PATH": f"{bin_}:{os.environ['PATH']}", "PYTHONPATH": str(laptop / "src"), "SU2QC_DEVICE": "cpu",
           "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    r = subprocess.run([sys.executable, "scripts/jobs/enqueue.py", "dataset", "tiny", "--time", "01:00:00",
                        "--step", "python scripts/make_dataset.py --name tiny --n-traj 4 --steps 2 2 --families onfam --out data/tiny",
                        "--output", "data/tiny/manifest.json", "--push"], cwd=laptop, env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    worker = [sys.executable, str(laptop / "scripts/worker/worker.py"), "--name", "perlmutter", "--mode", "slurm", "--base",
              str(tmp_path / "wk"), "--repo", str(origin), "--account", "m0000", "--env-prefix", "/none"]
    outs = [subprocess.run(worker, env=env, capture_output=True, text=True) for _ in range(3)]
    log = "\n".join(o.stdout + o.stderr for o in outs)
    assert all(o.returncode == 0 for o in outs), log
    assert "TIMEOUT -> resubmitted" in log and "COMPLETED" in log, log
    assert "-t 02:00:00" in (st / "501.args").read_text(), "retry must double the time limit"
    status = json.loads(subprocess.run(["git", "show", "results:000/status.json"], cwd=origin, capture_output=True, text=True).stdout)
    assert status["state"] == "COMPLETED" and status["attempts"] == 2 and [h["state"] for h in status["history"]] == ["TIMEOUT", "COMPLETED"]
