#!/usr/bin/env python
"""Hashes frozen by the preregistration (docs/PREREGISTRATION.md, tag prereg-2026-10-16).

* sha256 of configs/gates.yaml (the file's bytes);
* the array checksum of each dataset (data/<name>/manifest.json, the generator's own rule) and, if present,
  the fingerprint file's sha256;
* the model configuration hash: sha256 of the canonical JSON (sorted keys) of the JEPAConfig and the
  TrainConfig of a trained run, with the per-run seed and the device removed (they are not configuration).
  python scripts/prereg_hashes.py --run runs/v1_confirm/seed0 --out evidence/prereg/hashes.json
"""
import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path

import torch

p = argparse.ArgumentParser()
p.add_argument("--run", required=True, nargs="+", help="trained run folders holding model.pt; all must share one configuration")
p.add_argument("--datasets", nargs="+", default=["main", "chain_onfam", "chain_strong"])
p.add_argument("--out", required=True)
a = p.parse_args()


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def config_of(run: str) -> dict:
    ck = torch.load(Path(run) / "model.pt", map_location="cpu", weights_only=False)
    return {"JEPAConfig": ck["jcfg"], "TrainConfig": {k: v for k, v in ck["tcfg"].items() if k not in ("seed", "device")}}


configs = [json.dumps(config_of(r), sort_keys=True, separators=(",", ":")) for r in a.run]
assert len(set(configs)) == 1, "the runs do not share one configuration"
canon = configs[0]
config = json.loads(canon)
out = {
    "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "commit": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
    "gates_yaml_sha256": sha(Path("configs/gates.yaml").read_bytes()),
    "model_config": config,
    "model_config_canonical_json": canon,
    "model_config_sha256": sha(canon.encode()),
    "model_config_source": [str(Path(r) / "model.pt") for r in a.run],
    "datasets": {},
}
for name in a.datasets:
    d = Path("data") / name
    man = json.loads((d / "manifest.json").read_text())
    fp = d / "fingerprint.json"
    out["datasets"][name] = {"checksum_sha256": man["checksum_sha256"], "n_traj": man["n_traj"], "splits": man["splits"],
                             "seed": man["config"]["seed"],
                             "fingerprint_sha256": sha(fp.read_bytes()) if fp.exists() else None}
Path(a.out).parent.mkdir(parents=True, exist_ok=True)
Path(a.out).write_text(json.dumps(out, indent=1))
print(json.dumps({k: out[k] for k in ("gates_yaml_sha256", "model_config_sha256")}, indent=1))
print({k: v["checksum_sha256"][:12] for k, v in out["datasets"].items()})
print("wrote", a.out)
