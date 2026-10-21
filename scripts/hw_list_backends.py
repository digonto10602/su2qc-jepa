#!/usr/bin/env python
"""List the IBM Quantum backends this account can use, with what matters for the chain carrier.

Per backend: qubits, processor family, two-qubit gate name, median two-qubit and readout errors, pending jobs, and the
best K-qubit line (twin/layout.best_line: lowest summed CZ + readout error) with its score.  Laptop only (needs the
saved IBM account; queue workers never contact IBM).  Writes evidence/hardware/backends_<UTC>.json.
  python scripts/hw_list_backends.py --K 12
  python scripts/hw_list_backends.py --fake        # offline: Qiskit's fake Heron backends, for testing the path
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np

from su2qc_jepa.twin.layout import best_line, edge_errors_from_backend

p = argparse.ArgumentParser()
p.add_argument("--K", type=int, default=12)
p.add_argument("--fake", action="store_true")
p.add_argument("--out-dir", default="evidence/hardware")
a = p.parse_args()

if a.fake:
    from qiskit_ibm_runtime.fake_provider import FakeFez, FakeKingston, FakeMarrakesh, FakeTorino

    backends = [FakeTorino(), FakeFez(), FakeMarrakesh(), FakeKingston()]
    source = "fake"
else:
    from qiskit_ibm_runtime import QiskitRuntimeService

    service = QiskitRuntimeService()
    backends = service.backends(operational=True, simulator=False)
    source = f"ibm ({getattr(service, 'channel', '?')})"

rows = []
for b in backends:
    cz, ro, edges = edge_errors_from_backend(b)
    gate = next((g for g in ("cz", "ecr", "cx") if g in b.target.operation_names), None)
    line, score = best_line(edges, cz, ro, a.K) if edges else ([], float("nan"))
    try:
        pending = b.status().pending_jobs
    except Exception:  # noqa: BLE001 - fake backends and some plans do not report a queue
        pending = None
    proc = getattr(b, "processor_type", None) or {}
    rows.append({"name": b.name, "num_qubits": b.num_qubits, "processor": proc.get("family") if isinstance(proc, dict) else str(proc),
                 "two_qubit_gate": gate, "median_2q_error": float(np.median(list(cz.values()))) if cz else None,
                 "median_readout_error": float(np.median(list(ro.values()))) if ro else None, "pending_jobs": pending,
                 "best_line": [int(q) for q in line], "best_line_score": float(score)})
rows.sort(key=lambda r: r["best_line_score"])
print(f"{'backend':16} {'qubits':>6} {'gate':>4} {'med 2q err':>10} {'med RO err':>10} {'queue':>6} {'best ' + str(a.K) + '-line score':>18}")
for r in rows:
    med2q = f"{r['median_2q_error']:.2e}" if r["median_2q_error"] is not None else "-"
    medro = f"{r['median_readout_error']:.2e}" if r["median_readout_error"] is not None else "-"
    print(f"{r['name']:16} {r['num_qubits']:>6} {str(r['two_qubit_gate']):>4} {med2q:>10} {medro:>10} {str(r['pending_jobs']):>6} {r['best_line_score']:>18.4f}")
stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
out = Path(a.out_dir) / (f"backends_{stamp}.json" if not a.fake else f"backends_fake_{stamp}.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps({"source": source, "K": a.K, "utc": stamp, "backends": rows}, indent=1))
print("wrote", out)
