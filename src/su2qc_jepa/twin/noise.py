"""Noise models for the Aer twin.

Two sources: a synthetic Heron-like model (for development and for the J0/J3 simulator-only
checks) and a calibration snapshot of a real IBM backend (``NoiseModel.from_backend`` when a
backend object is available, or a saved properties JSON).  The twin is *calibrated*, not
*trusted*: the hardware residual (gate J3) is precisely a measurement of how far the twin is
from the device.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

__all__ = ["HeronLike", "heron_like_noise_model", "noise_model_from_backend", "save_noise_summary"]


@dataclass
class HeronLike:
    """Representative Heron r2 numbers (Open-plan devices, 2026); override from calibration data."""

    cz_error: float = 3.0e-3
    sx_error: float = 3.0e-4
    readout_01: float = 0.010  # P(read 1 | prepared 0)
    readout_10: float = 0.020  # P(read 0 | prepared 1)
    t1_us: float = 250.0
    t2_us: float = 150.0
    t_cz_ns: float = 70.0
    t_1q_ns: float = 30.0
    t_meas_ns: float = 1200.0


def heron_like_noise_model(K: int, p: HeronLike | None = None, line: list[int] | None = None):
    """Depolarising + thermal relaxation + readout noise on a line of K qubits (basis cz, rz, sx, x)."""
    from qiskit_aer.noise import NoiseModel, ReadoutError, depolarizing_error, thermal_relaxation_error

    p = p or HeronLike()
    line = line or list(range(K))
    nm = NoiseModel(basis_gates=["cz", "rz", "sx", "x"])
    t1, t2 = p.t1_us * 1e-6, min(p.t2_us, 2 * p.t1_us) * 1e-6
    e1 = depolarizing_error(p.sx_error, 1).compose(thermal_relaxation_error(t1, t2, p.t_1q_ns * 1e-9))
    for q in line:
        nm.add_quantum_error(e1, ["sx", "x"], [q])
        nm.add_readout_error(ReadoutError([[1 - p.readout_01, p.readout_01], [p.readout_10, 1 - p.readout_10]]), [q])
    e2 = depolarizing_error(p.cz_error, 2).compose(
        thermal_relaxation_error(t1, t2, p.t_cz_ns * 1e-9).tensor(thermal_relaxation_error(t1, t2, p.t_cz_ns * 1e-9)))
    for a, b in zip(line[:-1], line[1:]):
        nm.add_quantum_error(e2, ["cz"], [a, b])
        nm.add_quantum_error(e2, ["cz"], [b, a])
    return nm


def noise_model_from_backend(backend):
    """Calibrated twin from a live or fake IBM backend object (qiskit-ibm-runtime)."""
    from qiskit_aer.noise import NoiseModel

    return NoiseModel.from_backend(backend)


def save_noise_summary(path: str | Path, p: HeronLike, backend_name: str = "synthetic", extra: dict | None = None):
    d = {"backend": backend_name, "params": asdict(p)}
    if extra:
        d.update(extra)
    Path(path).write_text(json.dumps(d, indent=2))
