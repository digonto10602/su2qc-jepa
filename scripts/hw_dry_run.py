#!/usr/bin/env python
"""Hardware dry run: build the chain circuits for one calibration day, choose the qubit line from live
calibration data, transpile to the backend ISA, and write the manifest the human must approve.

Requires an IBM Quantum account saved with QiskitRuntimeService.save_account(...).
  python scripts/hw_dry_run.py --backend ibm_torino --K 12 --depths 1 2 4 8 --masses 0.3 0.375 0.5 --settings Z X --out evidence/hardware/day1
Use --fake to run against a FakeBackend (no account) for testing the path.
"""
import argparse
import json
from pathlib import Path

import numpy as np

from su2qc_jepa.hardware.ibm import dry_run
from su2qc_jepa.physics import conventions as C
from su2qc_jepa.physics.chain import ChainSpec, build_chain_circuit
from su2qc_jepa.physics.dynamics import lanczos, sector_restrict
from su2qc_jepa.physics.observables import named_states
from su2qc_jepa.physics.plaquette import PlaquetteModel
from su2qc_jepa.twin.layout import best_line, edge_errors_from_backend

p = argparse.ArgumentParser()
p.add_argument("--backend", default="ibm_torino")
p.add_argument("--fake", action="store_true")
p.add_argument("--K", type=int, default=12)
p.add_argument("--dt", type=float, default=0.375)
p.add_argument("--depths", type=int, nargs="+", default=(1, 2, 4, 8))
p.add_argument("--masses", type=float, nargs="+", default=(0.3, 0.375, 0.5))
p.add_argument("--settings", nargs="+", default=("Z", "X"))
p.add_argument("--shots", type=int, default=4000)
p.add_argument("--line", type=int, nargs="*", help="override the physical qubit line")
p.add_argument("--out", default="evidence/hardware/dry_run")
a = p.parse_args()

if a.fake:
    from qiskit_ibm_runtime.fake_provider import FakeTorino

    backend = FakeTorino()
else:
    from qiskit_ibm_runtime import QiskitRuntimeService

    backend = QiskitRuntimeService().backend(a.backend)

model = PlaquetteModel(0.5)
names = named_states(model)
N4 = model.sector(4)
circuits, labels = [], []
for mu in a.masses:
    H4 = sector_restrict(model.hamiltonian(C.Couplings.on_family(2.0, mu)), N4)
    psi0 = np.zeros(len(N4))
    psi0[list(N4).index(names["S3"])] = 1
    kr = lanczos(H4, psi0, K=a.K)
    for r in a.depths:
        spec = ChainSpec.from_krylov(kr, a.K, a.dt, r)
        for s in a.settings:
            circuits.append(build_chain_circuit(spec, s))
            labels.append({"mu": mu, "depth": r, "t": spec.t, "setting": s, "alpha": spec.alpha, "beta": spec.beta})
cz_err, ro_err, edges = edge_errors_from_backend(backend)
line, score = (a.line, None) if a.line else best_line(edges, cz_err, ro_err, a.K)
print("qubit line:", line, "score:", score)
summary = dry_run(circuits, backend, line, a.shots, a.out)
Path(a.out, "labels.json").write_text(json.dumps(labels, indent=1))
print(json.dumps({k: v for k, v in summary.__dict__.items() if k != "circuit_hashes"}, indent=1))
print(f"\nmanifest hash: {summary.manifest_hash}\nNext: a human copies this hash into configs/hardware_budget.yaml and sets approved: true.")
