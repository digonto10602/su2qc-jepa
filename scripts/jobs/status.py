#!/usr/bin/env python
"""Show every queued job and its state on the `results` branch (no connection to Perlmutter needed)."""
import json
import subprocess
from pathlib import Path

import yaml

subprocess.run(["git", "fetch", "-q", "origin"], check=False)
has = subprocess.run(["git", "rev-parse", "-q", "--verify", "origin/results"], capture_output=True).returncode == 0
rows = []
for p in sorted(Path("jobs").glob("[0-9][0-9][0-9]_*.yaml")):
    j = yaml.safe_load(p.read_text())
    num = p.name[:3]
    st = {}
    if has:
        r = subprocess.run(["git", "show", f"origin/results:{num}/status.json"], capture_output=True, text=True)
        if r.returncode == 0:
            st = json.loads(r.stdout)
    rows.append((num, j["where"], j["kind"], st.get("state", "QUEUED (no worker has picked it up yet)"),
                 st.get("elapsed_hours", ""), st.get("node_hours", ""), j["title"][:50]))
print(f"{'job':4} {'where':10} {'kind':6} {'state':40} {'hours':>6} {'node-h':>6}  title")
for r in rows:
    print(f"{r[0]:4} {r[1]:10} {r[2]:6} {r[3]:40} {str(r[4]):>6} {str(r[5]):>6}  {r[6]}")
if not has:
    print("(no results branch on origin yet: no worker has run)")
else:
    import time as _t

    r = subprocess.run(["git", "show", "origin/results:_worker/perlmutter.json"], capture_output=True, text=True)
    if r.returncode == 0:
        hb = json.loads(r.stdout)
        age = (_t.time() - hb["epoch"]) / 3600
        print(f"perlmutter worker heartbeat: {hb['utc']} ({age:.1f} h ago), node-hours used {hb['node_hours_used']}, "
              f"in flight {hb['in_flight']}")
        if age > 13 or (age > 2 and any(r[3].startswith("QUEUED") for r in rows)):
            print("WARNING: the worker looks stopped (no recent heartbeat). On Perlmutter: scrontab -l; "
                  "cat $SCRATCH/su2qc-worker/tick_errors.log")
    else:
        print("(no worker heartbeat yet)")
