#!/usr/bin/env python
"""Information ceilings for the J1 grounding rows: how well can ANY function of one clean observation
predict each grounding target?  Also the effective rank of the clean observations themselves.

The grounding heads read a latent that the encoder computes from ONE observation vector (18 observables +
flag + one-hots).  If a target is not determined by that vector, no encoder can reach R2 = 1 for it.  The
energy <psi|H(c_M, c_H, c_B)|psi> contains the hopping and plaquette expectation values, which are
off-diagonal in the configuration basis and are not observables of the record, and it depends on the
trajectory's couplings, which the encoder does not see.  This script measures the ceiling with flexible
regressors (fit on the training split, scored on the validation split, the split J1 uses):
  ridge (linear), k-nearest neighbours, gradient-boosted trees, an MLP;
each (a) from the clean observation alone and (b) with the step's couplings (c_M, c_H, c_B) appended.
  python scripts/j1_ceiling.py --data data/main --out evidence/J1_training/ceiling.json
"""
import argparse
import json
import subprocess
import time
from pathlib import Path

import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

from su2qc_jepa.data.trajectories import load_dataset
from su2qc_jepa.models.train import GROUND_NAMES, _ground_targets, r2_score

p = argparse.ArgumentParser()
p.add_argument("--data", required=True)
p.add_argument("--out", required=True)
p.add_argument("--seed", type=int, default=20261005, help="master seed (SeedSequence) for the stochastic regressors")
a = p.parse_args()

d = load_dataset(a.data)
n_obs = d["manifest"]["n_obs"]
g_all = _ground_targets(d)
act = d["act"]
# couplings in force at step s: c_M changes after a quench, act[:, s-1] holds the coupling of the step into s
coup = np.concatenate([act[:, :1, 1:], act[:, :, 1:]], 1)  # (N, T+1, 3); s = 0 uses the first action
seeds = [int(s.generate_state(1)[0]) for s in np.random.SeedSequence(a.seed).spawn(2)]


def rows(split):
    idx = d[f"split_{split}"]
    v = d["valid"][idx]
    clean = d["ctx"][idx].copy()
    clean[..., :n_obs] = d["tgt"][idx]
    clean[..., n_obs] = 0.0
    return clean[v], coup[idx][v], g_all[idx][v][:, :4]


Xtr, Ctr, Ytr = rows("train")
Xva, Cva, Yva = rows("val")


def eff_rank(X):
    Xc = X - X.mean(0)
    s = np.linalg.svd(Xc, compute_uv=False)
    q = s / s.sum()
    q = q[q > 0]
    return float(np.exp(-(q * np.log(q)).sum())), (s**2 / (s**2).sum()).tolist()


std = StandardScaler().fit(Xtr[:, :n_obs])
er_raw, sp_raw = eff_rank(Xva[:, :n_obs])
er_std, sp_std = eff_rank(std.transform(Xva[:, :n_obs]))

models = {
    "ridge": lambda: Ridge(alpha=1e-6),
    "knn5": lambda: KNeighborsRegressor(n_neighbors=5, weights="distance"),
    "gbt": lambda: HistGradientBoostingRegressor(max_iter=600, learning_rate=0.08, random_state=seeds[0]),
    "mlp": lambda: MLPRegressor(hidden_layer_sizes=(128, 128), max_iter=60, early_stopping=True, random_state=seeds[1]),
}
res = {}
t0 = time.time()
for inp, (A, B) in {"obs": (Xtr[:, :n_obs], Xva[:, :n_obs]),
                    "obs+couplings": (np.c_[Xtr[:, :n_obs], Ctr], np.c_[Xva[:, :n_obs], Cva])}.items():
    sc = StandardScaler().fit(A)
    A, B = sc.transform(A), sc.transform(B)
    for j, g in enumerate(GROUND_NAMES[:4]):
        for name, mk in models.items():
            m = mk().fit(A, Ytr[:, j])
            r2 = r2_score(Yva[:, j], m.predict(B))
            res.setdefault(inp, {}).setdefault(g, {})[name] = r2
            print(f"{inp:14s} {g:11s} {name:6s} R2 = {r2:.5f}  ({time.time() - t0:.0f}s)", flush=True)

out = {
    "what": "R2 ceilings of grounding targets from one clean observation (validation split); effective rank of clean observations",
    "data": a.data, "checksum": d["manifest"]["checksum_sha256"], "n_train_rows": int(len(Xtr)), "n_val_rows": int(len(Xva)),
    "master_seed": a.seed, "regressor_seeds": seeds,
    "commit": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
    "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "r2": res,
    "best_r2_from_obs": {g: max(res["obs"][g].values()) for g in GROUND_NAMES[:4]},
    "best_r2_from_obs_and_couplings": {g: max(res["obs+couplings"][g].values()) for g in GROUND_NAMES[:4]},
    "clean_obs_effective_rank": {"raw": er_raw, "standardised": er_std,
                                 "variance_fractions_standardised": sp_std},
}
Path(a.out).parent.mkdir(parents=True, exist_ok=True)
Path(a.out).write_text(json.dumps(out, indent=1))
print(json.dumps({k: out[k] for k in ("best_r2_from_obs", "best_r2_from_obs_and_couplings", "clean_obs_effective_rank")}, indent=1))
print("wrote", a.out)
