"""Gauge-JEPA-P v2: classical encoder + action-conditioned predictor + SIGReg + grounding heads.

Definitions (plain words):
* encoder  E_theta : observation o_t (noisy, finite shots)  -> latent s_t in R^d
* predictor P_phi  : (s_t, a_t, ..., a_{t+k-1})             -> predicted latent for time t+k
* JEPA loss        : || P_phi(s_t, a) - E_theta(o^clean_{t+k}) ||^2 ; the target is the encoder
                     of the *clean* future observation (exact expectation values), never the
                     observation itself.  No moving-average target: collapse is prevented by SIGReg.
* SIGReg           : LeJEPA's sketched isotropic Gaussian regulariser - random 1-D projections of
                     the latent batch are pushed toward N(0,1) with an Epps-Pulley characteristic-
                     function statistic.  (arXiv:2511.08544)
* grounding heads  : linear maps from the latent to known physical quantities (energy, string
                     Casimir, channel weights, flag rate), used in training only, so the latent is
                     identifiable and encoder/predictor cannot co-adapt into a trivial code.
* semigroup loss   : P(s, [a, a]) ~ P(P(s, [a]), [a]) - the predictor must compose like time evolution.
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F

__all__ = ["JEPAConfig", "GaugeJEPA", "sigreg_loss", "effective_rank"]


@dataclass
class JEPAConfig:
    obs_dim: int
    action_dim: int = 4
    latent_dim: int = 16
    hidden: int = 128
    action_embed: int = 32
    n_ground: int = 5  # energy, C_string, P_meson, P_baryonic, flag
    horizons: tuple[int, ...] = (1, 2, 4, 8)
    w_pred: float = 1.0
    w_sigreg: float = 0.05
    w_ground: float = 1.0
    w_semigroup: float = 0.1
    sigreg_projections: int = 64
    dropout: float = 0.0


class MLP(nn.Module):
    def __init__(self, din: int, hidden: int, dout: int, dropout: float = 0.0):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(din, hidden), nn.LayerNorm(hidden), nn.GELU(), nn.Dropout(dropout),
                                 nn.Linear(hidden, hidden), nn.LayerNorm(hidden), nn.GELU(), nn.Linear(hidden, dout))

    def forward(self, x):
        return self.net(x)


class ActionPredictor(nn.Module):
    """GRU over action tokens, initialised from the latent; returns the latent after each action."""

    def __init__(self, latent_dim: int, action_dim: int, action_embed: int, hidden: int):
        super().__init__()
        self.embed = nn.Sequential(nn.Linear(action_dim, action_embed), nn.GELU(), nn.Linear(action_embed, action_embed))
        self.init = nn.Linear(latent_dim, hidden)
        self.gru = nn.GRU(action_embed, hidden, batch_first=True)
        self.out = nn.Linear(hidden, latent_dim)
        self.skip = nn.Linear(latent_dim, latent_dim)

    def forward(self, s: torch.Tensor, actions: torch.Tensor) -> torch.Tensor:
        """s: (B, d); actions: (B, k, action_dim) -> (B, k, d) latents after 1..k actions."""
        h0 = torch.tanh(self.init(s)).unsqueeze(0)
        y, _ = self.gru(self.embed(actions), h0)
        return self.out(y) + self.skip(s).unsqueeze(1)


def sigreg_loss(z: torch.Tensor, n_proj: int = 64, t_grid: int = 17, generator: torch.Generator | None = None) -> torch.Tensor:
    """Sketched isotropic Gaussian regulariser (Epps-Pulley on random 1-D projections).

    For each random unit direction u, the empirical characteristic function of u.z over the batch
    is compared with exp(-t^2/2) on a grid of t in [-3, 3]; the mean squared discrepancy is returned.
    Minimising it pushes the latent distribution toward N(0, I) and rules out collapse.
    """
    B, d = z.shape
    u = torch.randn(d, n_proj, device=z.device, generator=generator)
    u = u / u.norm(dim=0, keepdim=True)
    proj = z @ u  # (B, n_proj)
    t = torch.linspace(-3.0, 3.0, t_grid, device=z.device)
    arg = proj.unsqueeze(-1) * t  # (B, n_proj, T)
    re = torch.cos(arg).mean(0)
    im = torch.sin(arg).mean(0)
    target = torch.exp(-0.5 * t**2)
    w = torch.exp(-0.5 * t**2)  # weight concentrating on small |t|
    return (((re - target) ** 2 + im**2) * w).sum(-1).mean() / w.sum()


def effective_rank(z: torch.Tensor) -> float:
    """exp(entropy of normalised singular values) of the centred latent batch."""
    zc = z - z.mean(0, keepdim=True)
    s = torch.linalg.svdvals(zc.double())
    p = s / s.sum().clamp_min(1e-12)
    p = p[p > 0]
    return float(torch.exp(-(p * p.log()).sum()))


class GaugeJEPA(nn.Module):
    def __init__(self, cfg: JEPAConfig):
        super().__init__()
        self.cfg = cfg
        self.encoder = MLP(cfg.obs_dim, cfg.hidden, cfg.latent_dim, cfg.dropout)
        self.predictor = ActionPredictor(cfg.latent_dim, cfg.action_dim, cfg.action_embed, cfg.hidden)
        self.ground = nn.Linear(cfg.latent_dim, cfg.n_ground)
        self.obs_norm = nn.BatchNorm1d(cfg.obs_dim, affine=False)

    def encode(self, o: torch.Tensor) -> torch.Tensor:
        shape = o.shape
        z = self.encoder(self.obs_norm(o.reshape(-1, shape[-1])))
        return z.reshape(*shape[:-1], self.cfg.latent_dim)

    def predict(self, s: torch.Tensor, actions: torch.Tensor) -> torch.Tensor:
        return self.predictor(s, actions)

    def loss(self, ctx: torch.Tensor, clean: torch.Tensor, act: torch.Tensor, ground: torch.Tensor,
             valid: torch.Tensor, generator: torch.Generator | None = None) -> dict[str, torch.Tensor]:
        """ctx/clean: (B, T+1, obs_dim); act: (B, T, action_dim); ground: (B, T+1, n_ground); valid: (B, T+1)."""
        B, T1, _ = ctx.shape
        s_ctx = self.encode(ctx)  # noisy context latents
        s_tgt = self.encode(clean)  # clean target latents (same encoder, no stop-gradient; SIGReg guards collapse)
        losses = {}
        pred_terms, n_terms = 0.0, 0
        for k in self.cfg.horizons:
            if k >= T1:
                continue
            s0 = s_ctx[:, : T1 - k].reshape(-1, self.cfg.latent_dim)
            a = torch.stack([act[:, t : t + k] for t in range(T1 - k)], 1).reshape(-1, k, self.cfg.action_dim)
            tgt = s_tgt[:, k:].reshape(-1, self.cfg.latent_dim)
            m = (valid[:, : T1 - k] & valid[:, k:]).reshape(-1)
            if m.sum() == 0:
                continue
            p = self.predict(s0[m], a[m])[:, -1]
            pred_terms = pred_terms + F.mse_loss(p, tgt[m])
            n_terms += 1
        losses["pred"] = pred_terms / max(n_terms, 1)
        zall = torch.cat([s_ctx[valid], s_tgt[valid]], 0)
        losses["sigreg"] = sigreg_loss(zall, self.cfg.sigreg_projections, generator=generator)
        losses["ground"] = F.mse_loss(self.ground(s_tgt[valid]), ground[valid]) + F.mse_loss(self.ground(s_ctx[valid]), ground[valid])
        # semigroup consistency on random pairs of consecutive actions
        if T1 > 2:
            s0 = s_ctx[:, : T1 - 2].reshape(-1, self.cfg.latent_dim)
            a2 = torch.stack([act[:, t : t + 2] for t in range(T1 - 2)], 1).reshape(-1, 2, self.cfg.action_dim)
            m = (valid[:, : T1 - 2] & valid[:, 2:]).reshape(-1)
            if m.sum() > 0:
                two = self.predict(s0[m], a2[m])[:, -1]
                one = self.predict(s0[m], a2[m][:, :1])[:, -1]
                comp = self.predict(one, a2[m][:, 1:])[:, -1]
                losses["semigroup"] = F.mse_loss(two, comp)
        losses["total"] = (self.cfg.w_pred * losses["pred"] + self.cfg.w_sigreg * losses["sigreg"]
                           + self.cfg.w_ground * losses["ground"] + self.cfg.w_semigroup * losses.get("semigroup", torch.zeros(())))
        return losses
