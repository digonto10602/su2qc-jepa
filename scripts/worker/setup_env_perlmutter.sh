#!/usr/bin/env bash
# ONE-TIME, run ON PERLMUTTER from a clone of the repository (docs/PERLMUTTER.md step 1):
#   git clone https://github.com/digonto10602/su2qc-jepa.git ~/su2qc-setup
#   bash ~/su2qc-setup/scripts/worker/setup_env_perlmutter.sh m1234
# Creates the conda env in /global/common/software/<project> (NERSC's recommended place for envs used by jobs),
# installs CUDA PyTorch + qiskit-aer-gpu + this package, and runs the fast tests.
set -euo pipefail
ACCOUNT="${1:?usage: setup_env_perlmutter.sh <NERSC project, e.g. m1234>}"
# GPU jobs may need the project's GPU account (e.g. m1234_g); the software folder is always the bare project (m1234)
ENV_PREFIX="${SU2QC_ENV_PREFIX:-/global/common/software/${ACCOUNT%_g}/su2qc-jepa-env}"
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
module load conda
[ -d "$ENV_PREFIX" ] || conda create -y --prefix "$ENV_PREFIX" python=3.12
conda activate "$ENV_PREFIX"
pip install --upgrade pip
pip install torch                       # CUDA build; A100 is supported
pip install -e "$REPO[ml,dev]" qiskit-aer-gpu
cd "$REPO"
python scripts/env_check.py || true     # on a login node there is no GPU; jobs run on GPU nodes
python -m pytest -q
echo "env ready: $ENV_PREFIX   next: bash $REPO/scripts/worker/install_perlmutter.sh $ACCOUNT"
