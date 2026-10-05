#!/usr/bin/env python
"""Compare two builds of a dataset through their fingerprints (data/trajectories.py: dataset_fingerprint).

Each side is a fingerprint.json file or a dataset folder (its fingerprint is computed from dataset.npz).
Reports, per array: whether the exact checksums agree, the largest difference of the per-trajectory sums and
of the sampled raw values, and which trajectories differ by more than --tol.
  python scripts/compare_fingerprints.py data/main evidence/J0_data/fingerprint_main_perlmutter.json --out evidence/J0_data/compare.json
"""
import argparse
import json
import subprocess
import time
from pathlib import Path

import numpy as np

from su2qc_jepa.data.trajectories import dataset_fingerprint

p = argparse.ArgumentParser()
p.add_argument("a")
p.add_argument("b")
p.add_argument("--tol", type=float, default=1e-12, help="a trajectory or sample 'differs' above this absolute difference")
p.add_argument("--out", default=None)
a = p.parse_args()


def load(src: str) -> dict:
    path = Path(src)
    if path.is_dir():
        z = np.load(path / "dataset.npz")
        return dataset_fingerprint({k: z[k] for k in ("ctx", "tgt", "act", "valid", "energy")})
    return json.loads(path.read_text())


fa, fb = load(a.a), load(a.b)
assert fa["seed"] == fb["seed"] and fa["n_sample"] == fb["n_sample"], "fingerprints made with different settings"
res = {}
for k in sorted(set(fa["arrays"]) | set(fb["arrays"])):
    x, y = fa["arrays"].get(k), fb["arrays"].get(k)
    if x is None or y is None or x["shape"] != y["shape"]:
        res[k] = {"comparable": False}
        continue
    assert x["sample_positions"] == y["sample_positions"]
    dr = np.abs(np.array(x["row_sums"]) - np.array(y["row_sums"]))
    ds = np.abs(np.array(x["sample_values"]) - np.array(y["sample_values"]))
    rows = np.where(dr > a.tol)[0]
    res[k] = {"comparable": True, "checksum_equal": x["checksum_sha256"] == y["checksum_sha256"],
              "max_abs_diff_row_sum": float(dr.max()), "rows_differing": int(len(rows)), "n_rows": int(len(dr)),
              "first_rows_differing": rows[:20].tolist(), "largest_row_diffs": np.sort(dr)[::-1][:5].tolist(),
              "max_abs_diff_sample": float(ds.max()), "samples_differing": int((ds > a.tol).sum()), "n_samples": int(len(ds))}
    print(f"{k:7s} checksum {'equal' if res[k]['checksum_equal'] else 'DIFFERENT'}; max |d row sum| {dr.max():.3e}; "
          f"rows > {a.tol:g}: {len(rows)}/{len(dr)}; max |d sample| {ds.max():.3e}; samples > {a.tol:g}: {(ds > a.tol).sum()}/{len(ds)}")
out = {"a": a.a, "b": a.b, "tol": a.tol, "arrays": res, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
       "commit": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()}
if a.out:
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(out, indent=1))
    print("wrote", a.out)
