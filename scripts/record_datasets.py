#!/usr/bin/env python
"""Record dataset checksums and split sizes in evidence/J0_data/datasets.json (prompts/001 step 7).

    python scripts/run.py -- python scripts/record_datasets.py data/main data/chain_onfam data/chain_strong

The array checksum is recomputed from dataset.npz with the generator's own rule and must equal the manifest's;
these checksums are frozen (CLAUDE.md section 3) and are what a Perlmutter rebuild from the same seed is compared to.
"""
import argparse
import hashlib
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

from su2qc_jepa.data.trajectories import _checksum

p = argparse.ArgumentParser()
p.add_argument("datasets", nargs="+")
p.add_argument("--out", default="evidence/J0_data/datasets.json")
a = p.parse_args()


def git(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


rows, ok = {}, True
for d in map(Path, a.datasets):
    man = json.loads((d / "manifest.json").read_text())
    with np.load(d / "dataset.npz") as z:
        arrays = {k: z[k] for k in z.files}
    recomputed = _checksum(arrays)
    match = recomputed == man["checksum_sha256"]
    ok &= match
    cfg = man["config"]
    rows[man["name"]] = {
        "path": str(d), "n_traj": man["n_traj"], "T": man["T"], "obs_dim": man["obs_dim"], "carrier": cfg.get("carrier"),
        "families": [f["name"] for f in cfg["families"]], "seed": cfg.get("seed"), "splits": man["splits"],
        "split_rule": man.get("split_rule"), "checksum_sha256": man["checksum_sha256"], "checksum_recomputed_match": match,
        "npz_file_sha256": hashlib.sha256((d / "dataset.npz").read_bytes()).hexdigest(),
        "generated_utc": man.get("generated_utc"), "wall_seconds": man.get("wall_seconds"),
    }
    print(f"{man['name']:14s} n={man['n_traj']:6d} checksum {man['checksum_sha256'][:12]} {'match' if match else 'MISMATCH'} "
          f"splits {man['splits']}")

out = Path(a.out)
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps({"status": "PASS" if ok else "FAIL", "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                           "commit": git("rev-parse", "HEAD"), "dirty": bool(git("status", "--porcelain", "--untracked-files=no")),
                           "machine": platform.node(), "command": " ".join([Path(sys.argv[0]).name, *sys.argv[1:]]),
                           "datasets": rows}, indent=1) + "\n")
print(f"== datasets: {'PASS' if ok else 'FAIL'} -> {out}")
sys.exit(0 if ok else 1)
