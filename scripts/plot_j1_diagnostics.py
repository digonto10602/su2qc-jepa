#!/usr/bin/env python
"""J1 diagnostics figure: effective rank, grounding R2 and semigroup residual vs epoch for each ablation rung.

Reads runs/<rung>/seed<k>/history.json (unmasked seeds only); one line per rung = mean over seeds, band = min..max.
Dashed grey lines are the J1 thresholds from configs/gates.yaml.  Writes the PNG and a JSON of the plotted
final-epoch values next to it (same stem) so every number in the figure is traceable.
  python scripts/plot_j1_diagnostics.py --out figures/NNN_x.png --rungs v1_base v1_wsigreg2 ...
"""
import argparse
import json
import subprocess
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import yaml  # noqa: E402

from su2qc_jepa.models.train import GROUND_NAMES  # noqa: E402

# categorical slots 1-7 of the dataviz reference palette (validated light mode); line styles as secondary encoding
COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7"]
STYLES = ["-", "--", "-.", ":", (0, (5, 1)), (0, (3, 1, 1, 1, 1, 1)), (0, (1, 2))]

p = argparse.ArgumentParser()
p.add_argument("--out", required=True)
p.add_argument("--rungs", nargs="+", required=True)
p.add_argument("--runs-dir", default="runs")
a = p.parse_args()

th = yaml.safe_load(Path("configs/gates.yaml").read_text())["J1_training"]
panels = [("eff_rank", "effective rank", th["effective_rank_min"])]
panels += [(f"r2:{i}", f"grounding $R^2$ ({g.replace('_', ' ')})", th["grounding_r2_min"][g]) for i, g in enumerate(GROUND_NAMES[:4])]
panels += [("semigroup_resid", "semigroup residual (relative)", th["semigroup_residual_max"])]


def series(h, key):
    if key.startswith("r2:"):
        return np.array([r["ground_r2"][int(key[3:])] for r in h])
    return np.array([r[key] for r in h])


fig, axes = plt.subplots(2, 3, figsize=(13, 7.2), constrained_layout=True)
summary = {"commit": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(), "rungs": {}}
for j, rung in enumerate(a.rungs):
    dirs = sorted(d for d in (Path(a.runs_dir) / rung).glob("seed*") if d.name[4:].isdigit())
    hs = [json.loads((d / "history.json").read_text()) for d in dirs]
    if not hs:
        print(f"skip {rung}: no seed*/history.json")
        continue
    n = min(len(h) for h in hs)
    ep = np.arange(1, n + 1)
    summary["rungs"][rung] = {"seeds": [d.name for d in dirs], "epochs": n}
    for ax, (key, label, thr) in zip(axes.flat, panels):
        y = np.stack([series(h[:n], key) for h in hs])
        ax.plot(ep, y.mean(0), color=COLORS[j % 7], ls=STYLES[j % 7], lw=2, label=rung)
        if len(hs) > 1:
            ax.fill_between(ep, y.min(0), y.max(0), color=COLORS[j % 7], alpha=0.15, lw=0)
        summary["rungs"][rung][key] = {"final_min": float(y[:, -1].min()), "final_max": float(y[:, -1].max()),
                                       "final_mean": float(y[:, -1].mean())}
for ax, (key, label, thr) in zip(axes.flat, panels):
    ax.axhline(thr, color="#888888", ls="--", lw=1)
    ax.set_title(label, fontsize=11)
    ax.set_xlabel("epoch")
    ax.grid(alpha=0.25, lw=0.5)
    if key == "semigroup_resid":
        ax.set_yscale("log")
    elif key.startswith("r2:"):
        lo = min([summary["rungs"][r][key]["final_min"] for r in summary["rungs"]] + [thr])
        ax.set_ylim(max(lo - 0.05, -0.1), 1.005)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
axes.flat[0].legend(fontsize=8, frameon=False)
fig.suptitle("J1 training diagnostics (validation split; mean over seeds, band = min..max; dashed = J1 threshold)", fontsize=11)
out = Path(a.out)
fig.savefig(out, dpi=150)
out.with_suffix(".json").write_text(json.dumps(summary, indent=1))
print("wrote", out, "and", out.with_suffix(".json"))
