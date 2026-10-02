#!/usr/bin/env bash
# Kept for convenience: run any command through the resource-aware laptop runner, never queueing it.
#   bash scripts/safe_run.sh python -m pytest -q      ==  python scripts/run.py --no-queue -- python -m pytest -q
set -euo pipefail
cd "$(dirname "$0")/.."
exec python scripts/run.py --no-queue -- "$@"
