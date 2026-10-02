"""Training loop, probes, forecasting evaluation and baselines for Gauge-JEPA-P v2.

The forecasting task (gate J2): from the noisy observation at context step c (and the known
action sequence), predict the clean observables at later steps.  JEPA predicts latents and a
linear probe (ridge, fit on the training split) reads observables out of them.  Baselines
see exactly the same inputs: ridge regression, an autoregressive one-step model in
observation space rolled out, and a direct supervised MLP.
"""
from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import torch

from .jepa import GaugeJEPA, JEPAConfig, effective_rank

__all__ = ["TrainConfig", "prepare_tensors", "train_jepa", "fit_probe", "forecast_jepa", "baseline_ridge",
           "baseline_autoregressive", "baseline_supervised_mlp", "r2_score", "GROUND_NAMES"]

GROUND_NAMES = ("energy", "C_string", "P_meson", "P_baryonic", "flag")


@dataclass
class TrainConfig:
    epochs: int = 30
    batch_size: int = 64
    lr: float = 2e-3
    weight_decay: float = 1e-5
    seed: int = 0
    device: str = "cpu"
    log_every: int = 5


def _ground_targets(d: dict) -> np.ndarray:
    names = d["manifest"]["obs_names"]
    n_obs = d["manifest"]["n_obs"]
    tgt = d["tgt"]
    g = np.stack([d["energy"], tgt[..., names.index("C_string")], tgt[..., names.index("P_meson")],
                  tgt[..., names.index("P_baryonic")], d["ctx"][..., n_obs]], -1)
    return g


def prepare_tensors(d: dict, split: str, device: str = "cpu") -> dict[str, torch.Tensor]:
    idx = d[f"split_{split}"]
    n_obs = d["manifest"]["n_obs"]
    ctx = d["ctx"][idx]
    clean = ctx.copy()
    clean[..., :n_obs] = d["tgt"][idx]
    clean[..., n_obs] = 0.0  # clean target: exact expectation values, no flags
    f = lambda x: torch.tensor(x, dtype=torch.float32, device=device)
    return {"ctx": f(ctx), "clean": f(clean), "act": f(d["act"][idx]), "ground": f(_ground_targets(d)[idx]),
            "valid": torch.tensor(d["valid"][idx], device=device), "tgt": f(d["tgt"][idx])}


def train_jepa(d: dict, jcfg: JEPAConfig, tcfg: TrainConfig, out_dir: str | Path | None = None) -> tuple[GaugeJEPA, dict]:
    torch.manual_seed(tcfg.seed)
    gen = torch.Generator(device=tcfg.device).manual_seed(tcfg.seed)
    tr = prepare_tensors(d, "train", tcfg.device)
    va = prepare_tensors(d, "val", tcfg.device) if len(d["split_val"]) else None
    model = GaugeJEPA(jcfg).to(tcfg.device)
    opt = torch.optim.AdamW(model.parameters(), lr=tcfg.lr, weight_decay=tcfg.weight_decay)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=tcfg.epochs)
    n = tr["ctx"].shape[0]
    history = []
    t0 = time.time()
    for ep in range(tcfg.epochs):
        model.train()
        perm = torch.randperm(n, generator=torch.Generator().manual_seed(tcfg.seed + ep))
        agg: dict[str, float] = {}
        nb = 0
        for i in range(0, n, tcfg.batch_size):
            b = perm[i : i + tcfg.batch_size]
            losses = model.loss(tr["ctx"][b], tr["clean"][b], tr["act"][b], tr["ground"][b], tr["valid"][b], gen)
            opt.zero_grad()
            losses["total"].backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            for k, v in losses.items():
                agg[k] = agg.get(k, 0.0) + float(v.detach())
            nb += 1
        sched.step()
        rec = {k: v / nb for k, v in agg.items()}
        rec["epoch"] = ep + 1
        rec.update(diagnostics(model, va if va is not None else tr))
        history.append(rec)
        if (ep + 1) % tcfg.log_every == 0 or ep == tcfg.epochs - 1:
            print(f"epoch {ep + 1:3d} total {rec['total']:.4f} pred {rec['pred']:.4f} sigreg {rec['sigreg']:.4f} "
                  f"ground {rec['ground']:.4f} eff_rank {rec['eff_rank']:.2f} R2(energy) {rec['ground_r2'][0]:.3f} "
                  f"semigroup {rec.get('semigroup_resid', float('nan')):.2e}  ({time.time() - t0:.0f}s)")
    if out_dir is not None:
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        torch.save({"state_dict": model.state_dict(), "jcfg": asdict(jcfg), "tcfg": asdict(tcfg)}, out_dir / "model.pt")
        (out_dir / "history.json").write_text(json.dumps(history, indent=1))
    return model, {"history": history, "final": history[-1]}


@torch.no_grad()
def diagnostics(model: GaugeJEPA, data: dict[str, torch.Tensor]) -> dict:
    model.eval()
    s = model.encode(data["clean"])[data["valid"]]
    er = effective_rank(s)
    g = model.ground(s).cpu().numpy()
    gt = data["ground"][data["valid"]].cpu().numpy()
    r2 = [r2_score(gt[:, i], g[:, i]) for i in range(g.shape[1])]
    # semigroup residual relative to the latent scale
    ctx, act, valid = data["ctx"], data["act"], data["valid"]
    T1 = ctx.shape[1]
    sc = model.encode(ctx)
    s0 = sc[:, : T1 - 2].reshape(-1, sc.shape[-1])
    a2 = torch.stack([act[:, t : t + 2] for t in range(T1 - 2)], 1).reshape(-1, 2, act.shape[-1])
    m = (valid[:, : T1 - 2] & valid[:, 2:]).reshape(-1)
    two = model.predict(s0[m], a2[m])[:, -1]
    comp = model.predict(model.predict(s0[m], a2[m][:, :1])[:, -1], a2[m][:, 1:])[:, -1]
    resid = float(((two - comp) ** 2).mean() / (two**2).mean().clamp_min(1e-12))
    # isotropy: ratio of smallest to largest latent variance
    var = s.var(0)
    return {"eff_rank": er, "ground_r2": r2, "semigroup_resid": resid, "isotropy": float(var.min() / var.max().clamp_min(1e-12))}


def r2_score(y: np.ndarray, yhat: np.ndarray) -> float:
    ss = float(((y - y.mean()) ** 2).sum())
    if ss < 1e-15:
        return float("nan")
    return 1.0 - float(((y - yhat) ** 2).sum()) / ss


@torch.no_grad()
def fit_probe(model: GaugeJEPA, data: dict[str, torch.Tensor], ridge: float = 1e-3) -> np.ndarray:
    """Ridge probe W (d+1, n_obs) from clean latents to clean observables, fit on the training split."""
    model.eval()
    s = model.encode(data["clean"])[data["valid"]].cpu().numpy()
    y = data["tgt"][data["valid"]].cpu().numpy()
    X = np.concatenate([s, np.ones((len(s), 1))], 1)
    W = np.linalg.solve(X.T @ X + ridge * np.eye(X.shape[1]), X.T @ y)
    return W


@torch.no_grad()
def forecast_jepa(model: GaugeJEPA, W: np.ndarray, data: dict[str, torch.Tensor], c: int) -> tuple[np.ndarray, np.ndarray]:
    """From the noisy context at step c predict clean observables at steps c+1..T.

    Returns (pred, truth) with shape (B, T-c, n_obs); invalid steps are NaN."""
    model.eval()
    ctx, act, valid, tgt = data["ctx"], data["act"], data["valid"], data["tgt"]
    s = model.encode(ctx[:, c])
    lat = model.predict(s, act[:, c:]).cpu().numpy()  # (B, T-c, d)
    X = np.concatenate([lat, np.ones(lat.shape[:2] + (1,))], -1)
    pred = X @ W
    truth = tgt[:, c + 1 :].cpu().numpy().copy()
    mask = valid[:, c + 1 :].cpu().numpy()
    pred[~mask] = np.nan
    truth[~mask] = np.nan
    return pred, truth


# ---------------------------------------------------------------------------
# Baselines (same inputs: noisy observations up to step c, actions for all steps)
# ---------------------------------------------------------------------------
def _flat_inputs(data: dict[str, torch.Tensor], c: int) -> np.ndarray:
    ctx = data["ctx"][:, : c + 1].cpu().numpy().reshape(len(data["ctx"]), -1)
    act = data["act"].cpu().numpy().reshape(len(data["ctx"]), -1)
    return np.concatenate([ctx, act], 1)


def baseline_ridge(train: dict[str, torch.Tensor], test: dict[str, torch.Tensor], c: int, ridge: float = 1e-2):
    Xtr, Xte = _flat_inputs(train, c), _flat_inputs(test, c)
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-8
    Xtr, Xte = (Xtr - mu) / sd, (Xte - mu) / sd
    Ytr = train["tgt"][:, c + 1 :].cpu().numpy()
    B, L, n = Ytr.shape
    Ytr = np.nan_to_num(Ytr.reshape(B, -1))
    Xtr1 = np.concatenate([Xtr, np.ones((len(Xtr), 1))], 1)
    W = np.linalg.solve(Xtr1.T @ Xtr1 + ridge * np.eye(Xtr1.shape[1]), Xtr1.T @ Ytr)
    Xte1 = np.concatenate([Xte, np.ones((len(Xte), 1))], 1)
    pred = (Xte1 @ W).reshape(len(Xte), L, n)
    truth = test["tgt"][:, c + 1 :].cpu().numpy().copy()
    mask = test["valid"][:, c + 1 :].cpu().numpy()
    pred[~mask] = np.nan
    truth[~mask] = np.nan
    return pred, truth


def baseline_autoregressive(train: dict[str, torch.Tensor], test: dict[str, torch.Tensor], c: int, epochs: int = 200,
                            hidden: int = 128, seed: int = 0):
    """One-step model in observation space: (o_t, a_t) -> o_{t+1}^clean, rolled out from the noisy o_c."""
    torch.manual_seed(seed)
    n_obs = train["tgt"].shape[-1]
    obs_dim = train["ctx"].shape[-1]
    act_dim = train["act"].shape[-1]
    net = torch.nn.Sequential(torch.nn.Linear(obs_dim + act_dim, hidden), torch.nn.GELU(), torch.nn.Linear(hidden, hidden),
                              torch.nn.GELU(), torch.nn.Linear(hidden, n_obs))
    opt = torch.optim.Adam(net.parameters(), lr=2e-3)
    ctx, act, tgt, valid = train["ctx"], train["act"], train["tgt"], train["valid"]
    # training pairs from both noisy and clean inputs
    clean = train["clean"]
    X = torch.cat([torch.cat([ctx[:, :-1], act], -1), torch.cat([clean[:, :-1], act], -1)], 0).reshape(-1, obs_dim + act_dim)
    Y = torch.cat([tgt[:, 1:], tgt[:, 1:]], 0).reshape(-1, n_obs)
    M = torch.cat([valid[:, :-1] & valid[:, 1:]] * 2, 0).reshape(-1)
    X, Y = X[M], Y[M]
    for _ in range(epochs):
        perm = torch.randperm(len(X))
        for i in range(0, len(X), 256):
            b = perm[i : i + 256]
            loss = torch.nn.functional.mse_loss(net(X[b]), Y[b])
            opt.zero_grad()
            loss.backward()
            opt.step()
    with torch.no_grad():
        o = test["ctx"][:, c].clone()
        preds = []
        for t in range(c, test["act"].shape[1]):
            nxt = net(torch.cat([o, test["act"][:, t]], -1))
            preds.append(nxt)
            o = o.clone()
            o[:, :n_obs] = nxt
            o[:, n_obs] = 0.0
        pred = torch.stack(preds, 1).cpu().numpy()
    truth = test["tgt"][:, c + 1 :].cpu().numpy().copy()
    mask = test["valid"][:, c + 1 :].cpu().numpy()
    pred[~mask] = np.nan
    truth[~mask] = np.nan
    return pred, truth


def baseline_supervised_mlp(train: dict[str, torch.Tensor], test: dict[str, torch.Tensor], c: int, epochs: int = 300,
                            hidden: int = 256, seed: int = 0):
    """Direct regression from (o_0..o_c, all actions) to all later clean observables."""
    torch.manual_seed(seed)
    Xtr = torch.tensor(_flat_inputs(train, c), dtype=torch.float32)
    Xte = torch.tensor(_flat_inputs(test, c), dtype=torch.float32)
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-8
    Xtr, Xte = (Xtr - mu) / sd, (Xte - mu) / sd
    Ytr = torch.nan_to_num(train["tgt"][:, c + 1 :]).reshape(len(Xtr), -1)
    net = torch.nn.Sequential(torch.nn.Linear(Xtr.shape[1], hidden), torch.nn.GELU(), torch.nn.Linear(hidden, hidden),
                              torch.nn.GELU(), torch.nn.Linear(hidden, Ytr.shape[1]))
    opt = torch.optim.Adam(net.parameters(), lr=1e-3, weight_decay=1e-5)
    for _ in range(epochs):
        perm = torch.randperm(len(Xtr))
        for i in range(0, len(Xtr), 128):
            b = perm[i : i + 128]
            loss = torch.nn.functional.mse_loss(net(Xtr[b]), Ytr[b])
            opt.zero_grad()
            loss.backward()
            opt.step()
    with torch.no_grad():
        pred = net(Xte).reshape(len(Xte), -1, train["tgt"].shape[-1]).cpu().numpy()
    truth = test["tgt"][:, c + 1 :].cpu().numpy().copy()
    mask = test["valid"][:, c + 1 :].cpu().numpy()
    pred[~mask] = np.nan
    truth[~mask] = np.nan
    return pred, truth
