#!/usr/bin/env python
"""Show every queued job and its state on the `results` branch, and each worker's heartbeat (decisions/004, 006)."""
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

    hints = {"perlmutter": "On Perlmutter: scrontab -l; cat $SCRATCH/su2qc-worker/tick_errors.log",
             "desktop": "Is the desktop switched on? There: systemctl --user status su2qc-worker.timer; "
                        "journalctl --user -u su2qc-worker -n 50"}
    names = subprocess.run(["git", "ls-tree", "--name-only", "origin/results:_worker"], capture_output=True, text=True).stdout.split()
    workers = sorted({n[:-5] for n in names if n.endswith(".json")} | {r[1] for r in rows if r[3].startswith("QUEUED")})
    for w in workers or ["perlmutter"]:
        r = subprocess.run(["git", "show", f"origin/results:_worker/{w}.json"], capture_output=True, text=True)
        queued = [x[0] for x in rows if x[1] == w and x[3].startswith("QUEUED")]
        if r.returncode != 0:
            print(f"{w} worker: no heartbeat yet" + (f"; waiting jobs {queued}. {hints.get(w, '')}" if queued else ""))
            continue
        hb = json.loads(r.stdout)
        age = (_t.time() - hb["epoch"]) / 3600
        print(f"{w} worker heartbeat: {hb['utc']} ({age:.1f} h ago), node-hours used {hb['node_hours_used']}, "
              f"in flight {hb['in_flight']}")
        # an idle worker heartbeats every 12 h, a busy one hourly; the desktop may be switched off on purpose
        stale = (age > 2 and queued) or (age > 13 and w != "desktop")
        if stale:
            print(f"WARNING: the {w} worker looks stopped (no recent heartbeat)"
                  + (f" and jobs {queued} are waiting" if queued else "") + f". {hints.get(w, '')}")
