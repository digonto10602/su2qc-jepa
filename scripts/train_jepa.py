#!/usr/bin/env python
"""Train Gauge-JEPA-P v2 on a dataset, fit the probe, evaluate forecasting against baselines.

Forecasting task: context = noisy observation at step c (and the known actions), targets = clean
observables at steps c+4 and c+8 (t = 2 and 3 in units of 1/g_E for dt = 0.25).  Evaluated per
coupling family on its held-out split.  Writes runs/<name>/seed<k>/{model.pt,history.json} and
runs/<name>/forecast_eval.json (the J2 input).
  python scripts/train_jepa.py --data data/smoke --name smoke --epochs 20 --seeds 1 --context-steps 4
"""
import argparse
import json
import os
from pathlib import Path

import numpy as np
import torch

from su2qc_jepa.compute import pick_device
from su2qc_jepa.data.trajectories import load_dataset
from su2qc_jepa.models.jepa import JEPAConfig
from su2qc_jepa.models.train import (
    TrainConfig,
    baseline_autoregressive,
    baseline_ridge,
    baseline_supervised_mlp,
    fit_probe,
    forecast_jepa,
    prepare_tensors,
    train_jepa,
)

p = argparse.ArgumentParser()
p.add_argument("--data", required=True)
p.add_argument("--name", default="run")
p.add_argument("--epochs", type=int, default=40)
p.add_argument("--seeds", type=int, default=1)
p.add_argument("--latent", type=int, default=16)
p.add_argument("--w-sigreg", type=float, default=0.5)
p.add_argument("--w-ground", type=float, default=1.0)
p.add_argument("--ema-target", type=float, default=None, help="EMA target encoder with stop-gradient, decay tau (e.g. 0.996)")
p.add_argument("--curriculum-epochs", type=int, default=0, help="train this many epochs on horizons (1, 2) first, then all")
p.add_argument("--master-seed", type=int, default=20261005, help="per-seed training seeds are spawned from this (SeedSequence)")
p.add_argument("--context-steps", type=int, default=4, help="context step index c")
p.add_argument("--eval-steps", type=int, nargs="+", default=(4, 8), help="steps after the context at which to score")
p.add_argument("--device", default=None, help="cpu | cuda; default: su2qc_jepa.compute.pick_device() (CPU unless a usable GPU exists)")
p.add_argument("--threads", type=int, default=None, help="CPU threads for torch (laptop: 6)")
p.add_argument("--baseline-epochs", type=int, default=100)
p.add_argument("--masked", action="store_true", help="also train/evaluate with the coupling columns (cM, cH, cB) hidden")
a = p.parse_args()
a.device = a.device or pick_device()
a.threads = a.threads or (int(os.environ['SU2QC_THREADS']) if os.environ.get('SU2QC_THREADS') else None)
if a.threads:
    torch.set_num_threads(a.threads)
print(f"device: {a.device}, torch threads: {torch.get_num_threads()}")

d = load_dataset(a.data)
names = d["manifest"]["obs_names"]
targets = ("P_baryonic", "P_meson", "C_string")
sel = [names.index(k) for k in targets]
out = Path("runs") / a.name
out.mkdir(parents=True, exist_ok=True)
families = [k.replace("split_test_heldout_", "") for k in d if k.startswith("split_test_heldout_") and k != "split_test_heldout_mass"]
c = a.context_steps
# independent per-seed integers from one recorded master seed (CLAUDE.md section 5: no adjacent integer seeds)
train_seeds = [int(ss.generate_state(1)[0]) for ss in np.random.SeedSequence(a.master_seed).spawn(a.seeds)]
(out / "args.json").write_text(json.dumps({**vars(a), "train_seeds": train_seeds}, indent=1))


def mae_table(pred, truth):
    e = np.nanmean(np.abs(pred - truth), axis=0)  # (L, n_obs)
    tab = {}
    for k in a.eval_steps:
        i = k - 1
        tab[f"+{k}"] = {t: float(e[i, j]) for t, j in zip(targets, sel)} if 0 <= i < e.shape[0] else {t: float("nan") for t in targets}
    return tab


def mask_couplings(data):
    m = {k: v.clone() for k, v in data.items()}
    m["act"][..., 1:] = 0.0
    return m


tr = prepare_tensors(d, "train", a.device)
tests = {fam: prepare_tensors(d, f"test_heldout_{fam}", a.device) for fam in families if len(d[f"split_test_heldout_{fam}"])}
mae: dict = {}
jepa_tabs = {fam: [] for fam in tests}
masked_tabs = {fam: [] for fam in tests}
for s in range(a.seeds):
    jcfg = JEPAConfig(obs_dim=d["manifest"]["obs_dim"], latent_dim=a.latent, w_sigreg=a.w_sigreg, w_ground=a.w_ground,
                      ema_target=a.ema_target)
    tcfg = TrainConfig(epochs=a.epochs, seed=train_seeds[s], device=a.device, curriculum_epochs=a.curriculum_epochs)
    model, info = train_jepa(d, jcfg, tcfg, out / f"seed{s}")
    W = fit_probe(model, tr)
    for fam, te in tests.items():
        jepa_tabs[fam].append(mae_table(*forecast_jepa(model, W, te, c)))
    if a.masked:
        dm = dict(d)
        dm["act"] = d["act"].copy()
        dm["act"][..., 1:] = 0.0
        model_m, _ = train_jepa(dm, jcfg, tcfg, out / f"seed{s}_masked")
        Wm = fit_probe(model_m, mask_couplings(tr))
        for fam, te in tests.items():
            masked_tabs[fam].append(mae_table(*forecast_jepa(model_m, Wm, mask_couplings(te), c)))


def avg(tabs):
    return {k: {t: float(np.mean([tab[k][t] for tab in tabs])) for t in targets} for k in tabs[0]}


for fam, te in tests.items():
    mae[fam] = {"jepa": avg(jepa_tabs[fam]), "ridge": mae_table(*baseline_ridge(tr, te, c)),
                "autoregressive": mae_table(*baseline_autoregressive(tr, te, c, epochs=a.baseline_epochs)),
                "supervised_mlp": mae_table(*baseline_supervised_mlp(tr, te, c, epochs=2 * a.baseline_epochs))}
    if a.masked:
        mae[fam]["jepa_masked"] = avg(masked_tabs[fam])
        mae[fam]["ridge_masked"] = mae_table(*baseline_ridge(mask_couplings(tr), mask_couplings(te), c))
ev = {"mae": mae, "n_test": {fam: int(len(d[f"split_test_heldout_{fam}"])) for fam in tests}, "context_step": c, "eval_steps": list(a.eval_steps),
      "dataset": d["manifest"]["name"], "checksum": d["manifest"]["checksum_sha256"], "seeds": a.seeds, "targets": list(targets),
      "master_seed": a.master_seed, "train_seeds": train_seeds}
(out / "forecast_eval.json").write_text(json.dumps(ev, indent=2))
print(json.dumps(mae, indent=1))
print("wrote", out / "forecast_eval.json")
