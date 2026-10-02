"""Gate J2 - forecasting on held-out couplings versus baselines (from runs/<name>/forecast_eval.json).

eval layout: {"mae": {family: {model: {"+4": {target: mae}, "+8": {...}}}}, "targets": [...], ...}
Families: "onfam" (held-out g_E) and "strong" (held-out masses near the resonance).  Each family
is gated separately; the gate passes when every family passes its rows.
"""
from __future__ import annotations

import json
from pathlib import Path

from .ledger import GateResult, load_thresholds, write_gate

__all__ = ["run_j2"]


def run_j2(eval_json: str | Path, thresholds_path: str = "configs/gates.yaml", evidence_dir: str = "evidence") -> GateResult:
    th = load_thresholds(thresholds_path)["J2_forecast"]
    res = GateResult("J2_forecast")
    ev = json.loads(Path(eval_json).read_text())
    targets = ev.get("targets", th["targets"])
    for fam, mae in ev["mae"].items():
        for step in th["eval_steps"]:
            key = f"+{step}"
            worst = max(mae["jepa"][key][k] for k in targets)
            res.add(f"[{fam}] JEPA MAE <= {th['mae_max']} at {key}", worst <= th["mae_max"], float(worst), th["mae_max"],
                    note="; ".join(f"{k}={mae['jepa'][key][k]:.3f}" for k in targets), evidence=str(eval_json))
            for b in th["must_beat_baselines"]:
                if b not in mae:
                    res.add_status(f"[{fam}] vs {b} at {key}", "NOT RUN", note="baseline missing")
                    continue
                wins = sum(1 for k in targets if mae["jepa"][key][k] <= th["beat_margin"] * mae[b][key][k])
                res.add(f"[{fam}] not worse than {b} on >= {th['beat_on_at_least']}/3 targets at {key}", wins >= th["beat_on_at_least"],
                        wins, th["beat_on_at_least"],
                        note="; ".join(f"{k}: jepa {mae['jepa'][key][k]:.3f} vs {b} {mae[b][key][k]:.3f}" for k in targets))
        if th.get("masked_mass_task"):
            if "jepa_masked" in mae:
                key = f"+{th['eval_steps'][-1]}"
                worst = max(mae["jepa_masked"][key][k] for k in targets)
                rw = max(mae["ridge_masked"][key][k] for k in targets) if "ridge_masked" in mae else float("nan")
                res.add_status(f"[{fam}] masked-coupling task at {key} (report only)", "PASS", {"jepa_masked": round(worst, 3), "ridge_masked": round(rw, 3)}, "report")
            else:
                res.add_status(f"[{fam}] masked-coupling task", "NOT RUN")
    write_gate(res, evidence_dir)
    return res
