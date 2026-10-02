#!/usr/bin/env python
"""Residual evaluation (J3 input) on twin-campaign or hardware records.

Label-free error signals computed per point (coupling mu, arm, day/seed, depth r), at the full shot
count and at subsampled shot counts (the records keep raw counts, so subsampling is exact):

  jepa_twin   = || E(o_point) - E(o_ref) ||        latent distance to the reference twin record (arm A, seed 0)
  jepa_self   = || E(o_point) - P(E(o_shallow), a) ||  prediction from the shallowest record of the same series
  jepa_t0     = || E(o_point) - P(E(o_exact_0), a) ||  prediction from the exact initial observation (pasted-plan definition)
  raw_twin    = || obs_point - obs_ref ||          observation-space distance to the reference twin (baseline)
  flag_rate   = excitation-flag rate                (baseline)
Label used only for scoring:
  exact_error = || obs_point - obs_exact(t) ||     (continuous-time exact observables)

  python scripts/residual_eval.py --model runs/smoke/seed0/model.pt --records evidence/twin/smoke/records.json \
      --out evidence/twin/smoke/residual_eval.json --shots-levels 0 512
"""
import argparse
import json
from pathlib import Path

import numpy as np
import torch

from su2qc_jepa.data.records import ObservationSpec, Record, estimate_chain
from su2qc_jepa.models.jepa import GaugeJEPA, JEPAConfig
from su2qc_jepa.physics import conventions as C
from su2qc_jepa.physics.dynamics import lanczos, sector_restrict
from su2qc_jepa.physics.observables import ObservableSet, named_states
from su2qc_jepa.physics.plaquette import PlaquetteModel

p = argparse.ArgumentParser()
p.add_argument("--model", required=True)
p.add_argument("--records", required=True)
p.add_argument("--out", required=True)
p.add_argument("--source", default="twin", choices=("twin", "hardware"))
p.add_argument("--reference", help="records.json of the reference twin (defaults to arm A / seed 0 of --records)")
p.add_argument("--shots-levels", type=int, nargs="+", default=(0, 512), help="0 = all shots")
p.add_argument("--seed", type=int, default=0)
a = p.parse_args()

ck = torch.load(a.model, map_location="cpu", weights_only=False)
model = GaugeJEPA(JEPAConfig(**ck["jcfg"]))
model.load_state_dict(ck["state_dict"])
model.eval()
rec = json.load(open(a.records))
ref = json.load(open(a.reference)) if a.reference else rec
spec = ObservationSpec(rec["obs_names"])
model_phys = PlaquetteModel(0.5)
obs = ObservableSet.primary(model_phys)
names = named_states(model_phys)
N4 = model_phys.sector(4)
rng = np.random.default_rng(a.seed)
K, dt = rec["K"], rec["dt"]
kr_cache = {}


def krylov(mu):
    if mu not in kr_cache:
        H4 = sector_restrict(model_phys.hamiltonian(C.Couplings.on_family(2.0, mu)), N4)
        psi0 = np.zeros(len(N4))
        psi0[list(N4).index(names["S3"])] = 1
        kr_cache[mu] = lanczos(H4, psi0, K=K)
    return kr_cache[mu]


def subsample(counts, n):
    keys = list(counts)
    w = np.array([counts[k] for k in keys], float)
    draw = rng.multinomial(n, w / w.sum())
    return {k: int(c) for k, c in zip(keys, draw) if c > 0}


def estimate(point, n_shots):
    recs = []
    for r in point["records"]:
        counts = r["counts"] if n_shots == 0 else subsample(r["counts"], n_shots)
        recs.append(Record(r["setting"], counts, sum(counts.values()), a.source, "chain"))
    est, flag, _ = estimate_chain(recs, krylov(point["mu"]), obs, N4)
    return est, flag


def encode(v):
    return model.encode(torch.tensor(v, dtype=torch.float32).unsqueeze(0))


def exact_t0_obs():
    full = np.zeros(model_phys.dim, dtype=complex)
    full[names["S3"]] = 1.0
    return obs.expectation(full)


series = {}
for pt in rec["points"]:
    series.setdefault((pt["mu"], pt["arm"], pt.get("seed", 0), pt.get("day", 0)), []).append(pt)
ref_points = {(pt["mu"], pt["depth"]): pt for pt in ref["points"] if pt["arm"] == "A" and pt.get("seed", 0) == 0}
o_t0 = spec.assemble(exact_t0_obs(), 0.0, "exact", "chain")
points = []
with torch.no_grad():
    for key, pts in series.items():
        pts = sorted(pts, key=lambda q: q["depth"])
        shallow = pts[0]
        for n_shots in a.shots_levels:
            est_sh, flag_sh = estimate(shallow, n_shots)
            o_sh = spec.assemble(est_sh, flag_sh, a.source, "chain")
            for pt in pts:
                est, flag = estimate(pt, n_shots)
                o_pt = spec.assemble(est, flag, a.source, "chain")
                r = int(pt["depth"])
                act = torch.tensor([[dt, pt["mu"], 0.25, -0.0625]] * r, dtype=torch.float32).unsqueeze(0)
                s_pt = encode(o_pt)
                s_t0 = model.predict(encode(o_t0), act)[:, -1]
                r_sh = r - int(shallow["depth"])
                s_self = model.predict(encode(o_sh), act[:, :r_sh])[:, -1] if r_sh > 0 else encode(o_sh)
                refp = ref_points.get((pt["mu"], pt["depth"]))
                if refp is not None:
                    est_ref, flag_ref = estimate(refp, n_shots)
                    o_ref = spec.assemble(est_ref, flag_ref, "twin", "chain")
                    jepa_twin = float(torch.linalg.norm(s_pt - encode(o_ref)))
                    raw_twin = float(np.linalg.norm(est - est_ref))
                else:
                    jepa_twin = raw_twin = float("nan")
                points.append({"mu": pt["mu"], "arm": pt["arm"], "seed": pt.get("seed", 0), "day": pt.get("day", pt.get("seed", 0)),
                               "depth": r, "shots": n_shots or pt["records"][0]["shots"],
                               "jepa_twin": jepa_twin, "jepa_self": float(torch.linalg.norm(s_pt - s_self)),
                               "jepa_t0": float(torch.linalg.norm(s_pt - s_t0)), "raw_twin": raw_twin, "flag_rate": flag,
                               "exact_error": float(np.linalg.norm(est - np.array(pt["exact"]))),
                               "ideal_error": float(np.linalg.norm(est - np.array(pt["ideal_circuit"])))})
Path(a.out).write_text(json.dumps({"points": points, "model": a.model, "records": a.records, "reference": a.reference or a.records}, indent=1))
print("wrote", a.out, "points:", len(points))
