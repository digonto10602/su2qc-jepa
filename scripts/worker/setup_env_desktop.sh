#!/usr/bin/env bash
# ONE-TIME, run ON THE DESKTOP (Linux, RTX 3070) from a clone of the repository (docs/DESKTOP.md step 1):
#   git clone https://github.com/digonto10602/su2qc-jepa.git ~/su2qc-setup
#   bash ~/su2qc-setup/scripts/worker/setup_env_desktop.sh
# Creates the Python environment the desktop worker uses, installs a CUDA build of PyTorch and this package, checks that
# PyTorch can really use the GPU, and runs the fast tests (including the CUDA case of the device test).
# Re-run it after a `git pull` that changed pyproject.toml (it only installs what is missing or changed).
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
ENV_PREFIX="${SU2QC_ENV_PREFIX:-$HOME/.su2qc-jepa-env}"

command -v nvidia-smi >/dev/null || { echo "nvidia-smi not found: install the NVIDIA driver first"; exit 1; }
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader

if command -v conda >/dev/null; then
  [ -d "$ENV_PREFIX" ] || conda create -y --prefix "$ENV_PREFIX" python=3.12
  PY="$ENV_PREFIX/bin/python"
else
  # no conda: a plain virtual environment (needs python3 >= 3.10 with the venv module)
  [ -d "$ENV_PREFIX" ] || python3 -m venv "$ENV_PREFIX"
  PY="$ENV_PREFIX/bin/python"
fi
"$PY" -m pip install --upgrade pip
"$PY" -m pip install torch                     # PyPI's default Linux wheel is a CUDA build; it supports sm_86 (RTX 30xx)
"$PY" -m pip install -e "$REPO[ml,dev]"

# the GPU must be usable by PyTorch, not just visible (a missing kernel architecture fails here, not in a job)
"$PY" - <<'PYCHECK'
import torch
assert torch.cuda.is_available(), "torch.cuda.is_available() is False: driver too old for this PyTorch CUDA build?"
cap = "sm_%d%d" % torch.cuda.get_device_capability(0)
assert cap in torch.cuda.get_arch_list(), f"PyTorch has no kernels for {cap}: {torch.cuda.get_arch_list()}"
print("GPU ok:", torch.cuda.get_device_name(0), cap, "torch", torch.__version__, "cuda", torch.version.cuda,
      "sum check", (torch.ones(8, device="cuda") * 2).sum().item())
PYCHECK

cd "$REPO"
SU2QC_DEVICE=cuda "$PY" scripts/env_check.py | grep -E '"torch_device_used"|"cuda"|"torch"' || true
"$PY" -m pytest -q -rs                          # the CUDA case of test_training_and_baselines_run_on_device must PASS here
echo
echo "env ready: $ENV_PREFIX    next: bash $REPO/scripts/worker/install_desktop.sh"
