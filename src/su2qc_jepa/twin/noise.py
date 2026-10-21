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

__all__ = ["HeronLike", "heron_like_noise_model", "noise_model_from_backend", "save_noise_summary", "line_noise_dict",
           "noise_model_from_dict", "degraded_noise_model", "save_line_noise_model", "load_line_noise_model"]


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


def line_noise_dict(noise_model, line: list[int]) -> dict:
    """The errors of a full-device noise model that act only on the qubits of `line`, renumbered 0..K-1 in line order
    (the chain circuits use qubit k for Krylov vector k).  Works on the model's public dictionary form, so the
    calibrated numbers themselves are untouched; errors that touch any qubit outside the line are dropped."""
    d = noise_model.to_dict(serializable=True)
    idx = {int(q): i for i, q in enumerate(line)}
    errors = []
    for e in d["errors"]:
        if "gate_qubits" not in e:  # an all-qubit error applies to the line as well
            errors.append(e)
            continue
        kept = [[idx[int(q)] for q in qs] for qs in e["gate_qubits"] if all(int(q) in idx for q in qs)]
        if kept and not e.get("noise_qubits"):
            errors.append({**e, "gate_qubits": kept})
    return {"errors": errors}


def noise_model_from_dict(d: dict):
    from qiskit_aer.noise import NoiseModel

    return NoiseModel.from_dict(d)


def degraded_noise_model(d: dict, cz_errors: list[float], factor: float = 2.0):
    """Arm B of the twin: the calibrated line model with every readout flip probability and every CZ error scaled by
    `factor` (an extra depolarising channel of the calibrated CZ error is composed onto each CZ; for two qubits a
    depolarising parameter lambda gives average gate infidelity 15 lambda / 16).  Stands in for a worse day."""
    from qiskit_aer.noise import depolarizing_error

    errors = []
    for e in d["errors"]:
        if e.get("type") == "roerror":
            probs = [[(1 - min(factor * (1 - row[i]), 1.0)) if j == i else min(factor * p, 1.0) for j, p in enumerate(row)]
                     for i, row in enumerate(e["probabilities"])]
            e = {**e, "probabilities": probs}
        errors.append(e)
    nm = noise_model_from_dict({"errors": errors})
    for k, err in enumerate(cz_errors):
        extra = depolarizing_error(min((factor - 1.0) * err * 16 / 15, 1.0), 2)
        for pair in ([k, k + 1], [k + 1, k]):
            nm.add_quantum_error(extra, ["cz"], pair, warnings=False)
    return nm


def save_line_noise_model(path: str | Path, backend, line: list[int], score: float, extra: dict | None = None) -> dict:
    """Write the calibrated line noise model of `backend` (built on the laptop, where the IBM token lives) as JSON:
    the renumbered error dictionary, the physical line, its calibration numbers and versions.  Queue workers load it
    with load_line_noise_model and never contact IBM."""
    import time

    import qiskit_aer

    from ..hardware.ibm import calibration_snapshot
    from .layout import edge_errors_from_backend

    cz, ro, _ = edge_errors_from_backend(backend)
    line_cz = [cz.get((a, b), cz.get((b, a))) for a, b in zip(line[:-1], line[1:])]
    snap = calibration_snapshot(backend)
    try:  # when the device itself measured this calibration (for a stored snapshot this is far older than the build)
        cal_date = str(backend.properties().last_update_date)
    except Exception:  # noqa: BLE001 - some backends expose no properties; record that rather than guess
        cal_date = None
    out = {"backend": backend.name, "calibration_measured": cal_date, "line": [int(q) for q in line], "line_score": float(score), "K": len(line),
           "line_cz_errors": line_cz, "line_readout_errors": [ro.get(q) for q in line],
           "line_qubits": {str(q): snap["qubits"].get(q, {}) for q in line},
           "calibration_read_utc": snap.get("taken_utc"), "built_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "qiskit_aer": qiskit_aer.__version__, "noise_model": line_noise_dict(noise_model_from_backend(backend), line),
           **(extra or {})}
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(out, default=float))
    return out


def load_line_noise_model(path: str | Path):
    """(arm A calibrated model, arm B degraded model, metadata) from a file written by save_line_noise_model."""
    d = json.loads(Path(path).read_text())
    nm = noise_model_from_dict(d["noise_model"])
    return nm, degraded_noise_model(d["noise_model"], d["line_cz_errors"]), {k: v for k, v in d.items() if k != "noise_model"}
