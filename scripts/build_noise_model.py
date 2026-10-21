#!/usr/bin/env python
"""Build the calibrated twin noise model of one IBM backend for the chain carrier (laptop only: needs the IBM account).

Chooses the best K-qubit line from the live calibration (twin/layout.best_line), takes NoiseModel.from_backend, keeps
only the errors on that line renumbered 0..K-1 (twin/noise.line_noise_dict), and writes
evidence/twin/<name>/noise_model.json with the line, its calibration numbers and versions.  Queue workers then run
`run_twin.py --noise-model evidence/twin/<name>/noise_model.json` and never contact IBM (CLAUDE.md section 5).
  python scripts/build_noise_model.py --backend ibm_fez --K 12 --name day0
  python scripts/build_noise_model.py --backend FakeTorino --fake --K 12 --name fake0     # offline test
"""
import argparse

from su2qc_jepa.twin.layout import best_line, edge_errors_from_backend
from su2qc_jepa.twin.noise import save_line_noise_model

p = argparse.ArgumentParser()
p.add_argument("--backend", required=True)
p.add_argument("--fake", action="store_true", help="use qiskit_ibm_runtime.fake_provider.<backend> (offline)")
p.add_argument("--K", type=int, default=12)
p.add_argument("--name", required=True)
p.add_argument("--line", type=int, nargs="+", help="use this physical line instead of the best one")
a = p.parse_args()

if a.fake:
    from qiskit_ibm_runtime import fake_provider

    backend = getattr(fake_provider, a.backend)()
else:
    from qiskit_ibm_runtime import QiskitRuntimeService

    backend = QiskitRuntimeService().backend(a.backend)
cz, ro, edges = edge_errors_from_backend(backend)
if a.line:
    assert len(a.line) == a.K, "the line must have K qubits"
    line = a.line
    score = sum(cz.get((x, y), cz.get((y, x), 1.0)) for x, y in zip(line[:-1], line[1:])) + sum(ro.get(q, 0.0) for q in line)
else:
    line, score = best_line(edges, cz, ro, a.K)
out = f"evidence/twin/{a.name}/noise_model.json"
d = save_line_noise_model(out, backend, line, score, extra={"source": "fake" if a.fake else "ibm", "name": a.name})
print(f"backend {d['backend']}  calibration measured {d['calibration_measured']}  line {d['line']}  score {d['line_score']:.4f}")
print("line CZ errors:", ", ".join(f"{e:.2e}" for e in d["line_cz_errors"]))
print("line readout errors:", ", ".join(f"{e:.2e}" for e in d["line_readout_errors"]))
print("wrote", out, "(", len(d["noise_model"]["errors"]) if "noise_model" in d else "", "errors )")
