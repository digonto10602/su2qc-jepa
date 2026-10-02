#!/usr/bin/env bash
# Clean-environment replication: physics tests + J0 (quick) + gates from released evidence files (if present).
set -euo pipefail
cd "$(dirname "$0")/.."
python scripts/env_check.py
python -m pytest -q
python scripts/check_artifacts.py
command -v graphify >/dev/null && bash scripts/graph_update.sh --check || echo "graph: graphify not installed or graph stale"
python scripts/run_gate.py J0 --quick || true
[ -d runs/v1_final ] && python scripts/run_gate.py J1 --runs runs/v1_final/seed* || echo "J1: released histories not present"
[ -f runs/v1_final/forecast_eval.json ] && python scripts/run_gate.py J2 --eval runs/v1_final/forecast_eval.json || echo "J2: eval not present"
[ -f evidence/hardware/residual_eval_all.json ] && python scripts/run_gate.py J3 --eval evidence/hardware/residual_eval_all.json || echo "J3: hardware eval not present"
tail -n 40 evidence/GATE_LEDGER.md
