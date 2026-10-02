#!/usr/bin/env python
"""Twin campaign for the chain carrier: couplings x depth ladder x arms x seeds -> records + residual inputs.

Writes evidence/twin/<name>/records.json (per point: settings, counts, ideal-circuit observables, exact
observables, twin estimates, flag rate) - the input for the twin residual study and for J3 rehearsal.
Example (fast):  python scripts/run_twin.py --name smoke --K 8 --depths 1 2 --shots 1000 --seeds 1
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np

from su2qc_jepa.data.records import estimate_chain
from su2qc_jepa.physics import conventions as C
from su2qc_jepa.physics.chain import ChainSpec, chain_amplitudes, cz_count
from su2qc_jepa.physics.dynamics import evolve, lanczos, sector_restrict
from su2qc_jepa.physics.observables import ObservableSet, named_states
from su2qc_jepa.physics.plaquette import PlaquetteModel
from su2qc_jepa.twin.noise import HeronLike, heron_like_noise_model
from su2qc_jepa.twin.run import TwinRunner, chain_point_records

p = argparse.ArgumentParser()
p.add_argument("--name", default="smoke")
p.add_argument("--K", type=int, default=12)
p.add_argument("--dt", type=float, default=0.375)
p.add_argument("--depths", type=int, nargs="+", default=(1, 2, 4, 6, 8))
p.add_argument("--masses", type=float, nargs="+", default=(0.3, 0.375, 0.5))
p.add_argument("--shots", type=int, default=4000)
p.add_argument("--seeds", type=int, default=5)
p.add_argument("--arms", nargs="+", default=("A", "B"), help="A: nominal noise; B: 2x CZ error (stands in for a worse arm/day)")
p.add_argument("--method", default="density_matrix")
p.add_argument("--device", default="CPU")
a = p.parse_args()

model = PlaquetteModel(0.5)
obs = ObservableSet.primary(model)
names = named_states(model)
N4 = model.sector(4)
out = Path("evidence/twin") / a.name
out.mkdir(parents=True, exist_ok=True)
points = []
t0 = time.time()
for mu in a.masses:
    coup = C.Couplings.on_family(2.0, mu, name=f"PA-mu{mu}")
    H4 = sector_restrict(model.hamiltonian(coup), N4)
    psi0 = np.zeros(len(N4))
    psi0[list(N4).index(names["S3"])] = 1
    kr = lanczos(H4, psi0, K=a.K)
    for arm in a.arms:
        params = HeronLike() if arm == "A" else HeronLike(cz_error=6e-3, readout_01=0.02, readout_10=0.04)
        for seed in range(a.seeds):
            runner = TwinRunner(heron_like_noise_model(a.K, params), method=a.method, master_seed=20261005 + seed, device=a.device)
            for r in a.depths:
                spec = ChainSpec.from_krylov(kr, a.K, a.dt, r)
                recs = chain_point_records(runner, spec, a.shots, salt=f"{a.name}-{mu}-{arm}-{seed}-{r}")
                est, flag, extra = estimate_chain(recs, kr, obs, N4)
                c_ideal = chain_amplitudes(spec)
                full_ideal = np.zeros(model.dim, dtype=complex)
                full_ideal[N4] = kr.Q @ c_ideal
                ideal = obs.expectation(full_ideal)
                full_exact = np.zeros(model.dim, dtype=complex)
                full_exact[N4] = evolve(H4, psi0, np.array([spec.t]))[0]
                exact = obs.expectation(full_exact)
                points.append({"mu": mu, "arm": arm, "seed": seed, "depth": r, "t": spec.t, "cz": cz_count(a.K, r, 2),
                               "flag_rate": flag, "p1": extra["p1"], "twin_est": est.tolist(), "ideal_circuit": ideal.tolist(),
                               "exact": exact.tolist(), "pops": extra["pops"].tolist(),
                               "records": [{"setting": rc.setting, "counts": rc.counts, "shots": rc.shots} for rc in recs]})
                print(f"mu={mu} arm={arm} seed={seed} r={r} cz={points[-1]['cz']} flag={flag:.3f} "
                      f"max|twin-ideal|={np.abs(est - ideal).max():.3f} ({time.time() - t0:.0f}s)")
json.dump({"name": a.name, "K": a.K, "dt": a.dt, "obs_names": obs.names, "points": points}, open(out / "records.json", "w"))
print("wrote", out / "records.json", "points:", len(points))
