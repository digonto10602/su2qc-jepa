#!/usr/bin/env python
"""Cross-carrier check (prompts/003 step 4): does the encoder treat chain-carrier and twin-labelled records of a state like
the diagonal-carrier, exact-source records it was trained on?

The model (v1_final) was trained only on records labelled source=exact, carrier=diagonal.  The J3 twin and hardware
records are chain-carrier records (Krylov populations from Z, coherences from X) labelled source=twin/hardware.  For the
same exact states - the J3 twin regime: on-family g_E in {1.3, 1.75, 2.0}, mu in {0.3, 0.375, 0.5}, S3 start,
t = r * 0.375 / g_E for r = 1..8 - this script builds, at each shot level, two independent diagonal records and two
independent chain records (exact sampling, no device noise) and measures latent distances ||E(o) - E(o')||:
  noise_diag    diagonal vs diagonal (the shot-noise scale the model knows)
  noise_chain   chain vs chain
  cross         diagonal vs chain                           (estimator + carrier label)
  label_carrier the same chain estimates labelled chain vs diagonal  (the carrier one-hot alone)
  label_source  the same diagonal estimates labelled exact vs twin   (the source one-hot alone)
  twin_vs_train chain estimates labelled twin/chain vs diagonal estimates labelled exact/diagonal (what J3 compares)
  err_diag, err_chain  a noisy record vs the clean exact record of the same state
and the observation-space analogues of the noise terms.  Distances far above noise_diag mean the encoder sees the chain
or twin records as off-distribution.
  python scripts/cross_carrier_check.py --model evidence/runs/v1_final/seed0/model.pt --out evidence/twin/cross_carrier/cross_carrier.json
"""
import argparse
import json
import subprocess
import time
from pathlib import Path

import numpy as np
import torch

from su2qc_jepa.data.records import (
    ObservationSpec,
    estimate_chain,
    estimate_diagonal,
    sample_exact_chain,
    sample_exact_diagonal,
)
from su2qc_jepa.models.jepa import GaugeJEPA, JEPAConfig
from su2qc_jepa.physics import conventions as C
from su2qc_jepa.physics.dynamics import evolve, lanczos, sector_restrict
from su2qc_jepa.physics.observables import ObservableSet, named_states
from su2qc_jepa.physics.plaquette import PlaquetteModel

p = argparse.ArgumentParser()
p.add_argument("--model", required=True)
p.add_argument("--out", required=True)
p.add_argument("--K", type=int, default=12)
p.add_argument("--dt", type=float, default=0.375)
p.add_argument("--depths", type=int, nargs="+", default=list(range(1, 9)))
p.add_argument("--gE", type=float, nargs="+", default=(1.3, 1.75, 2.0))
p.add_argument("--masses", type=float, nargs="+", default=(0.3, 0.375, 0.5))
p.add_argument("--shots", type=int, nargs="+", default=(512, 4000))
p.add_argument("--seed", type=int, default=20261028, help="master seed (SeedSequence), one child per state and shot level")
a = p.parse_args()

ck = torch.load(a.model, map_location="cpu", weights_only=False)
net = GaugeJEPA(JEPAConfig(**ck["jcfg"]))
net.load_state_dict(ck["state_dict"])
net.eval()
phys = PlaquetteModel(0.5)
obs = ObservableSet.primary(phys)
spec = ObservationSpec(obs.names)
names = named_states(phys)
N4 = phys.sector(4)
psi0 = np.zeros(len(N4))
psi0[list(N4).index(names["S3"])] = 1.0


def z(o):
    with torch.no_grad():
        return net.encode(torch.tensor(o, dtype=torch.float32).unsqueeze(0))[0].numpy()


def dist(o1, o2):
    return float(np.linalg.norm(z(o1) - z(o2)))


states = [(g, mu, r) for g in a.gE for mu in a.masses for r in a.depths]
children = iter(np.random.SeedSequence(a.seed).spawn(len(states) * len(a.shots)))
rows = []
t0 = time.time()
for g, mu, r in states:
    H4 = sector_restrict(phys.hamiltonian(C.Couplings.on_family(g, mu)), N4)
    kr = lanczos(H4, psi0, K=a.K)
    psi = evolve(H4, psi0, np.array([r * a.dt]))[0]
    full = np.zeros(phys.dim, dtype=complex)
    full[N4] = psi
    c = kr.Q.T @ psi
    exact = obs.expectation(full)
    o_exact = spec.assemble(exact, 0.0, "exact", "diagonal")
    for shots in a.shots:
        rng = np.random.default_rng(next(children))
        dg = [estimate_diagonal(sample_exact_diagonal(full, shots, rng), obs) for _ in range(2)]
        ch = [estimate_chain(sample_exact_chain(c, shots, rng), kr, obs, N4)[:2] for _ in range(2)]
        od = [spec.assemble(e, f, "exact", "diagonal") for e, f in dg]
        oc = [spec.assemble(e, f, "exact", "chain") for e, f in ch]
        rows.append({
            "gE": g, "mu": mu, "depth": r, "t": r * a.dt, "shots": shots,
            "noise_diag": dist(od[0], od[1]), "noise_chain": dist(oc[0], oc[1]), "cross": dist(od[0], oc[0]),
            "label_carrier": dist(oc[0], spec.assemble(ch[0][0], ch[0][1], "exact", "diagonal")),
            "label_source": dist(od[0], spec.assemble(dg[0][0], dg[0][1], "twin", "diagonal")),
            "twin_vs_train": dist(od[0], spec.assemble(ch[0][0], ch[0][1], "twin", "chain")),
            "err_diag": dist(od[0], o_exact), "err_chain": dist(oc[0], o_exact),
            "obs_noise_diag": float(np.linalg.norm(dg[0][0] - dg[1][0])), "obs_noise_chain": float(np.linalg.norm(ch[0][0] - ch[1][0])),
            "obs_err_chain": float(np.linalg.norm(ch[0][0] - exact)), "obs_err_diag": float(np.linalg.norm(dg[0][0] - exact)),
        })

keys = ["noise_diag", "noise_chain", "cross", "label_carrier", "label_source", "twin_vs_train", "err_diag", "err_chain",
        "obs_noise_diag", "obs_noise_chain", "obs_err_diag", "obs_err_chain"]
summary = {}
for shots in a.shots:
    R = [x for x in rows if x["shots"] == shots]
    ref = float(np.median([x["noise_diag"] for x in R]))
    summary[str(shots)] = {k: {"median": float(np.median([x[k] for x in R])), "p90": float(np.percentile([x[k] for x in R], 90)),
                               "median_over_noise_diag": float(np.median([x[k] for x in R]) / ref) if not k.startswith("obs_") else None}
                           for k in keys}
out = {"what": "cross-carrier latent distances (prompts/003 step 4)", "model": a.model, "K": a.K, "dt": a.dt, "gE": list(a.gE),
       "masses": list(a.masses), "depths": list(a.depths), "shots": list(a.shots), "master_seed": a.seed, "n_states": len(states),
       "summary": summary, "rows": rows, "seconds": round(time.time() - t0, 1),
       "commit": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
       "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
Path(a.out).parent.mkdir(parents=True, exist_ok=True)
Path(a.out).write_text(json.dumps(out, indent=1))
for shots, s in summary.items():
    print(f"shots {shots}: " + "  ".join(f"{k}={v['median']:.3g}" + (f" ({v['median_over_noise_diag']:.2g}x)" if v["median_over_noise_diag"] else "")
                                         for k, v in s.items()))
print("wrote", a.out)
