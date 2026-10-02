"""Gate J1 - training health from history.json files (one per seed)."""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from ..models.train import GROUND_NAMES
from .ledger import GateResult, load_thresholds, write_gate

__all__ = ["run_j1"]


def run_j1(run_dirs: list[str | Path], thresholds_path: str = "configs/gates.yaml", evidence_dir: str = "evidence") -> GateResult:
    th = load_thresholds(thresholds_path)["J1_training"]
    res = GateResult("J1_training")
    finals = []
    for rd in run_dirs:
        h = json.loads((Path(rd) / "history.json").read_text())
        finals.append(h[-1])
        has_nan = any((isinstance(v, float) and math.isnan(v)) for rec in h for v in rec.values() if isinstance(v, float))
        res.add(f"no NaN ({Path(rd).name})", not has_nan, has_nan, False)
    er = [f["eff_rank"] for f in finals]
    res.add("effective rank (min over seeds)", min(er) >= th["effective_rank_min"], float(min(er)), th["effective_rank_min"],
            note=f"per seed: {np.round(er, 2).tolist()}")
    for i, g in enumerate(GROUND_NAMES[:4]):
        r2 = [f["ground_r2"][i] for f in finals]
        res.add(f"grounding R2 {g} (min over seeds)", min(r2) >= th["grounding_r2_min"][g], float(min(r2)), th["grounding_r2_min"][g])
    sg = [f.get("semigroup_resid", float("nan")) for f in finals]
    res.add("semigroup residual (max over seeds)", max(sg) <= th["semigroup_residual_max"], float(max(sg)), th["semigroup_residual_max"])
    res.add("number of seeds", len(finals) >= th["seeds"], len(finals), th["seeds"])
    write_gate(res, evidence_dir)
    return res
