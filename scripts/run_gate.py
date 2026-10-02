#!/usr/bin/env python
"""Run a gate and append to evidence/GATE_LEDGER.md.
  python scripts/run_gate.py J0 --data data/smoke [--quick]
  python scripts/run_gate.py J1 --runs runs/smoke/seed0 runs/smoke/seed1
  python scripts/run_gate.py J2 --eval runs/smoke/forecast_eval.json
  python scripts/run_gate.py J3 --eval evidence/hardware/residual_eval.json
"""
import argparse
import sys

p = argparse.ArgumentParser()
p.add_argument("gate", choices=("J0", "J1", "J2", "J3"))
p.add_argument("--data")
p.add_argument("--runs", nargs="*")
p.add_argument("--eval")
p.add_argument("--quick", action="store_true")
p.add_argument("--chain-K", type=int, default=12)
a = p.parse_args()

if a.gate == "J0":
    from su2qc_jepa.gates.j0_data import run_j0

    res = run_j0(a.data, chain_K=a.chain_K, quick=a.quick)
elif a.gate == "J1":
    from su2qc_jepa.gates.j1_training import run_j1

    res = run_j1(a.runs or [])
elif a.gate == "J2":
    from su2qc_jepa.gates.j2_forecast import run_j2

    res = run_j2(a.eval)
else:
    from su2qc_jepa.gates.j3_hardware import run_j3

    res = run_j3(a.eval)
for r in res.rows:
    print(f"{r.status:8s} {r.name}: measured={r.measured} threshold={r.threshold} {r.note}")
print(f"== {res.gate}: {res.status}")
sys.exit(0 if res.status == "PASS" else 1)
