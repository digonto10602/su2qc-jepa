#!/usr/bin/env python
"""Copy a finished job's outputs from origin/results into the working tree, plus its status and log under
evidence/jobs/NNN/.  Never merges the results branch.   python scripts/jobs/fetch.py 003"""
import io
import json
import subprocess
import sys
import tarfile
from pathlib import Path

num = sys.argv[1].zfill(3)
force = "--force" in sys.argv
subprocess.run(["git", "fetch", "-q", "origin", "results"], check=True)
st = json.loads(subprocess.run(["git", "show", f"origin/results:{num}/status.json"], capture_output=True, text=True, check=True).stdout)
print(f"job {num}: {st['state']} on {st.get('worker')} ({st.get('elapsed_hours')} h, {st.get('node_hours')} node-h)")
if st["state"] != "COMPLETED" and not force:
    sys.exit(f"not COMPLETED - read the log: git show origin/results:{num}/log.txt   (use --force to fetch anyway)")
ev = Path("evidence/jobs") / num
ev.mkdir(parents=True, exist_ok=True)
(ev / "status.json").write_text(json.dumps(st, indent=2))
log = subprocess.run(["git", "show", f"origin/results:{num}/log.txt"], capture_output=True, text=True).stdout
(ev / "log.txt").write_text(log)
tar = subprocess.run(["git", "archive", "--format=tar", "origin/results", f"{num}/outputs"], capture_output=True)
n = 0
if tar.returncode == 0:
    with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
        for m in tf.getmembers():
            if not m.isfile():
                continue
            rel = Path(*Path(m.name).parts[2:])
            rel.parent.mkdir(parents=True, exist_ok=True)
            rel.write_bytes(tf.extractfile(m).read())
            n += 1
print(f"copied {n} output files into the working tree; status and log in {ev}/")
for s in st.get("skipped", []):
    print("  not published:", s)
