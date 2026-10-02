"""Gate J3 - label-free hardware error signals (twin rehearsal or real hardware).

Input: residual_eval.json from scripts/residual_eval.py, one entry per (point, shots level) with the
signals jepa_twin, jepa_self, jepa_t0, raw_twin, flag_rate and the scoring label exact_error.

Pass logic (preregistered):
  * Spearman(jepa_twin, exact_error) >= residual_spearman_min at the low-shot level (default 512)
  * non-inferiority: Spearman(jepa_twin) >= Spearman(raw_twin) - noninferiority_margin at the low-shot level
  * AUROC of jepa_twin for separating arm A (nominal) from arm B (degraded) >= auroc_min at full shots
  * every baseline Spearman is reported (report-only rows)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from .ledger import GateResult, load_thresholds, write_gate

__all__ = ["run_j3", "spearman", "auroc"]

SIGNALS = ("jepa_twin", "jepa_self", "jepa_t0", "raw_twin", "flag_rate")


def spearman(x, y) -> float:
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 3:
        return float("nan")
    rx, ry = x[m].argsort().argsort(), y[m].argsort().argsort()
    return float(np.corrcoef(rx, ry)[0, 1])


def auroc(score, label) -> float:
    s, l = np.asarray(score, float), np.asarray(label, bool)
    m = np.isfinite(s)
    s, l = s[m], l[m]
    pos, neg = s[l], s[~l]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    gt = (pos[:, None] > neg[None, :]).mean()
    eq = (pos[:, None] == neg[None, :]).mean()
    return float(gt + 0.5 * eq)


def run_j3(eval_json: str | Path, thresholds_path: str = "configs/gates.yaml", evidence_dir: str = "evidence") -> GateResult:
    th = load_thresholds(thresholds_path)["J3_hardware"]
    res = GateResult("J3_hardware")
    pts = json.loads(Path(eval_json).read_text())["points"]
    levels = sorted(set(p["shots"] for p in pts))
    low = min(levels)
    full = max(levels)
    at = lambda lvl: [p for p in pts if p["shots"] == lvl]
    res.add("number of points (per shot level)", len(at(full)) >= th["min_points"], len(at(full)), th["min_points"], evidence=str(eval_json))
    table = {}
    for lvl in levels:
        P = at(lvl)
        e = [p["exact_error"] for p in P]
        table[lvl] = {s: spearman([p[s] for p in P], e) for s in SIGNALS}
    for s in SIGNALS:
        res.add_status(f"Spearman({s}, exact error) by shots", "PASS", {str(l): round(table[l][s], 3) for l in levels}, "report",
                       note="report-only row" if s != "jepa_twin" else "")
    rho_low = table[low]["jepa_twin"]
    res.add(f"Spearman(jepa_twin) at {low} shots", rho_low >= th["residual_spearman_min"], rho_low, th["residual_spearman_min"])
    margin = th.get("noninferiority_margin", 0.05)
    res.add(f"non-inferior to raw_twin at {low} shots", rho_low >= table[low]["raw_twin"] - margin,
            {"jepa_twin": round(rho_low, 3), "raw_twin": round(table[low]["raw_twin"], 3)}, f"jepa >= raw - {margin}")
    P = at(full)
    a = auroc([p["jepa_twin"] for p in P], [p["arm"] == "B" for p in P])
    res.add("AUROC jepa_twin separates arm B (degraded) from arm A", a >= th["auroc_min"], a, th["auroc_min"])
    a_raw = auroc([p["raw_twin"] for p in P], [p["arm"] == "B" for p in P])
    res.add_status("AUROC raw_twin (report only)", "PASS", a_raw, "report")
    days = sorted(set(p.get("day", 0) for p in pts))
    res.add("calibration days", len(days) >= th["calibration_days"], len(days), th["calibration_days"])
    write_gate(res, evidence_dir)
    return res
