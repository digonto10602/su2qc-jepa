#!/usr/bin/env bash
# End-to-end smoke pipeline (CPU, ~5 minutes): dataset -> JEPA -> gates J0/J1/J2 -> twin -> residual -> J3.
# Every artefact lands under data/smoke, runs/smoke, evidence/.  Thresholds are NOT expected to pass at smoke scale;
# the point is that every path runs and writes evidence.
set -euo pipefail
cd "$(dirname "$0")/.."
python scripts/make_dataset.py --name smoke --n-traj 300 --steps 12 12 --families onfam --quench-fraction 0.15 --out data/smoke
python scripts/train_jepa.py --data data/smoke --name smoke --epochs 15 --seeds 1 --context-steps 4 --baseline-epochs 30
python scripts/run_gate.py J0 --data data/smoke --quick || true
python scripts/run_gate.py J1 --runs runs/smoke/seed0 || true
python scripts/run_gate.py J2 --eval runs/smoke/forecast_eval.json || true
python scripts/run_twin.py --name smoke --K 8 --depths 1 2 4 --masses 0.3 0.375 --shots 1000 --seeds 2
python scripts/residual_eval.py --model runs/smoke/seed0/model.pt --records evidence/twin/smoke/records.json --out evidence/twin/smoke/residual_eval.json
python scripts/run_gate.py J3 --eval evidence/twin/smoke/residual_eval.json || true
echo "smoke pipeline finished; see evidence/GATE_LEDGER.md"
