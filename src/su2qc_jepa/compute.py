"""Device selection and the measured unit costs used by the laptop runner (su2qc_jepa.localrun, decisions/004).

`pick_device()` returns "cuda" only when a CUDA device exists *and* the installed PyTorch has kernels for its
architecture *and* a tiny kernel actually runs; otherwise "cpu".  On the laptop this is always "cpu" (its GTX 1060
is a Pascal card that current PyTorch CUDA builds do not support); on Perlmutter it is "cuda".  Override with
SU2QC_DEVICE.  Routing (laptop or Perlmutter) lives in su2qc_jepa.localrun and scripts/run.py.
"""
from __future__ import annotations

import os
from pathlib import Path

import yaml

__all__ = ["pick_device", "load_compute", "estimate_hours"]


def pick_device(prefer: str = "auto") -> str:
    req = os.environ.get("SU2QC_DEVICE", prefer)
    if req == "cpu":
        return "cpu"
    try:
        import torch

        if torch.cuda.is_available():
            major, minor = torch.cuda.get_device_capability(0)
            arch = f"sm_{major}{minor}"
            if arch not in torch.cuda.get_arch_list():
                raise RuntimeError(f"PyTorch has no kernels for {arch} ({torch.cuda.get_device_name(0)})")
            (torch.ones(8, device="cuda") * 2).sum().item()
            return "cuda"
    except Exception as e:  # noqa: BLE001
        if req == "cuda":
            raise RuntimeError(f"SU2QC_DEVICE=cuda requested but CUDA is unusable: {e}") from e
    if req == "cuda":
        raise RuntimeError("SU2QC_DEVICE=cuda requested but no CUDA device")
    return "cpu"


def load_compute(path: str | Path = "configs/compute.yaml") -> dict:
    return yaml.safe_load(Path(path).read_text())


# Laptop cost model (seconds), measured on 2 CPU cores on 2 Oct 2026 and scaled by laptop_speedup
_UNIT_COST = {
    "dataset_per_traj": 0.006,  # 2,000 trajectories in 11.7 s
    "train_per_traj_epoch": 0.0022,  # 2.5 s per epoch for 1,137 training trajectories
    "twin_per_circuit": 18.0,  # 12-qubit density matrix, 4,000 shots: 6-30 s
}


def estimate_hours(job: str, laptop_speedup: float = 2.0, **kw) -> float:
    """Rough laptop wall-clock hours for a job: dataset(n_traj), train(n_train, epochs, seeds, configs), twin(n_circuits)."""
    if job == "dataset":
        s = kw["n_traj"] * _UNIT_COST["dataset_per_traj"]
    elif job == "train":
        s = kw["n_train"] * kw.get("epochs", 200) * kw.get("seeds", 1) * kw.get("configs", 1) * _UNIT_COST["train_per_traj_epoch"]
    elif job == "twin":
        s = kw["n_circuits"] * _UNIT_COST["twin_per_circuit"]
    else:
        raise ValueError(job)
    return s / laptop_speedup / 3600
