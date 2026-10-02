"""Trajectory generator: exact dynamics + emulated finite-shot observations + split manifest.

A trajectory is an initial gauge-invariant state followed by n actions.  An action
is one time step of duration dt at couplings (cM, cH, cB) (cE = 1 in units of g_E);
a mass quench is a trajectory whose cM changes at a given step.  Every time point
carries the clean exact observables (the JEPA target) and a finite-shot
observation (the JEPA context), built through the same estimator used for twin
and hardware records (see records.py).

Two coupling *families* are scanned, because the physics-setup measurements of
1 Oct 2026 showed that the mass dependence of the P-A window is weak while the
strong-coupling resonance at mu* = 3/8 is sharp:

* family "onfam"  - on-family points (cH, cB) = (1/(2 g_E), -1/(4 g_E^2)) with g_E scanned;
                    held out by g_E (the dynamics depend strongly on g_E, weakly on mu).
* family "strong" - strong-coupling points cH = |cB| = 0.02 (the P-S regime) with mu scanned
                    around the resonance; held out by mu.

Splits are by rule, never by row.  The manifest records every parameter and a
checksum of the arrays.
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np

from ..physics import conventions as C
from ..physics.dynamics import evolve, lanczos, sector_restrict
from ..physics.observables import ObservableSet, named_states
from ..physics.plaquette import PlaquetteModel
from .records import ObservationSpec, estimate_chain, estimate_diagonal, sample_exact_chain, sample_exact_diagonal

__all__ = ["DatasetConfig", "FamilyConfig", "generate_dataset", "load_dataset", "ACTION_DIM", "ONFAM", "STRONG"]

ACTION_DIM = 4  # (dt, cM, cH, cB)


@dataclass
class FamilyConfig:
    name: str
    # list of (cH, cB) pairs with a label (e.g. the g_E value) for the held-out rule
    ratios: tuple[tuple[float, float, float], ...]  # (label, cH, cB)
    masses: tuple[float, ...]
    dts: tuple[float, ...]
    heldout_by: str  # 'label' (ratio label, e.g. g_E) or 'mu'
    heldout: tuple[float, ...]
    val: tuple[float, ...]
    chain_K: int = 12
    weight: float = 1.0

    @staticmethod
    def onfamily(gEs=(1.0, 1.15, 1.3, 1.45, 1.6, 1.75, 2.0), masses=(0.15, 0.25, 0.375, 0.5, 0.65),
                 dts=(0.125, 0.25, 0.5), heldout=(1.3, 1.75), val=(1.45,), chain_K=12, weight=1.0) -> FamilyConfig:
        ratios = tuple((float(g), 1.0 / (2.0 * g), -1.0 / (4.0 * g * g)) for g in gEs)
        return FamilyConfig("onfam", ratios, tuple(masses), tuple(dts), "label", tuple(heldout), tuple(val), chain_K, weight)

    @staticmethod
    def strong(masses=(0.15, 0.2, 0.25, 0.3, 0.33, 0.375, 0.42, 0.45, 0.5, 0.575, 0.65), dts=(2.0, 4.0, 8.0),
               heldout=(0.3, 0.42, 0.5), val=(0.45,), chain_K=24, weight=1.0, cH=0.02) -> FamilyConfig:
        return FamilyConfig("strong", ((0.0, cH, -cH),), tuple(masses), tuple(dts), "mu", tuple(heldout), tuple(val), chain_K, weight)


ONFAM = FamilyConfig.onfamily()
STRONG = FamilyConfig.strong()


@dataclass
class DatasetConfig:
    n_traj: int = 200
    n_steps_min: int = 8
    n_steps_max: int = 12
    families: tuple[FamilyConfig, ...] = (ONFAM, STRONG)
    starts: tuple[str, ...] = ("S3", "S3", "S3", "S1", "random")
    quench_fraction: float = 0.2
    shots_choices: tuple[int, ...] = (256, 512, 1024, 4096)
    carrier: str = "diagonal"  # 'diagonal' or 'chain'
    chain_settings: tuple[str, ...] = ("Z", "X")
    seed: int = 20261005
    jmax: float = 0.5
    sector_N: int = 4
    name: str = "smoke"
    extra: dict = field(default_factory=dict)

    def to_json(self) -> dict:
        d = asdict(self)
        return json.loads(json.dumps(d, default=float))


def _checksum(arrays: dict[str, np.ndarray]) -> str:
    h = hashlib.sha256()
    for k in sorted(arrays):
        h.update(k.encode())
        h.update(np.ascontiguousarray(arrays[k]).tobytes())
    return h.hexdigest()


class _Cache:
    """Per-coupling Hamiltonians and Lanczos chains (chain carrier) in the N sector."""

    def __init__(self, model: PlaquetteModel, sector_idx: np.ndarray):
        self.model = model
        self.sector = sector_idx
        self.H: dict[tuple, np.ndarray] = {}
        self.kr: dict[tuple, object] = {}

    def hamiltonian(self, cM: float, cH: float, cB: float) -> np.ndarray:
        key = (round(cM, 8), round(cH, 8), round(cB, 8))
        if key not in self.H:
            self.H[key] = sector_restrict(self.model.hamiltonian(C.Couplings(1.0, cM, cH, cB)), self.sector)
        return self.H[key]

    def krylov(self, cM: float, cH: float, cB: float, psi0: np.ndarray, K: int):
        key = (round(cM, 8), round(cH, 8), round(cB, 8), hashlib.sha1(psi0.round(10).tobytes()).hexdigest(), K)
        if key not in self.kr:
            self.kr[key] = lanczos(self.hamiltonian(cM, cH, cB), psi0, K=K)
        return self.kr[key]


def _initial_state(start: str, model: PlaquetteModel, sector_idx: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    names = named_states(model)
    psi = np.zeros(len(sector_idx))
    loc = list(sector_idx)
    if start in ("S3", "S1"):
        psi[loc.index(names[start])] = 1.0
    elif start == "random":
        k = rng.integers(1, 4)
        idx = rng.choice(len(sector_idx), size=k, replace=False)
        amp = rng.normal(size=k)
        psi[idx] = amp / np.linalg.norm(amp)
    else:
        raise ValueError(start)
    return psi


def generate_dataset(cfg: DatasetConfig, out_dir: str | Path, verbose: bool = True) -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    rng = np.random.default_rng(np.random.SeedSequence(cfg.seed))
    model = PlaquetteModel(cfg.jmax)
    obs = ObservableSet.primary(model)
    spec = ObservationSpec(obs.names)
    sector_idx = model.sector(cfg.sector_N)
    cache = _Cache(model, sector_idx)
    T = cfg.n_steps_max
    n_obs = len(obs.names)
    ctx = np.zeros((cfg.n_traj, T + 1, spec.dim))
    tgt = np.zeros((cfg.n_traj, T + 1, n_obs))
    act = np.zeros((cfg.n_traj, T, ACTION_DIM))
    valid = np.zeros((cfg.n_traj, T + 1), dtype=bool)
    energy = np.zeros((cfg.n_traj, T + 1))
    meta = []
    fam_w = np.array([f.weight for f in cfg.families], float)
    fam_w /= fam_w.sum()
    for i in range(cfg.n_traj):
        traj_seed = int(rng.integers(0, 2**31 - 1))
        trng = np.random.default_rng(np.random.SeedSequence(traj_seed))
        fam = cfg.families[int(trng.choice(len(cfg.families), p=fam_w))]
        n_steps = int(trng.integers(cfg.n_steps_min, cfg.n_steps_max + 1))
        dt = float(trng.choice(fam.dts))
        mu = float(trng.choice(fam.masses))
        label, cH, cB = fam.ratios[int(trng.integers(len(fam.ratios)))]
        start = str(trng.choice(cfg.starts))
        shots = int(trng.choice(cfg.shots_choices))
        quench_step = int(trng.integers(2, n_steps - 1)) if (trng.random() < cfg.quench_fraction and n_steps > 3) else -1
        mu2 = float(trng.choice(fam.masses)) if quench_step > 0 else mu
        carrier = cfg.carrier
        if carrier == "chain" and (start != "S3" or quench_step > 0):
            carrier = "diagonal"  # chain records only for the hardware-relevant S3 trajectories
        psi = _initial_state(start, model, sector_idx, trng)
        kr = cache.krylov(mu, cH, cB, psi, fam.chain_K) if carrier == "chain" else None
        t_acc = 0.0
        for s in range(n_steps + 1):
            cM_now = mu2 if (quench_step > 0 and s > quench_step) else mu
            H = cache.hamiltonian(cM_now, cH, cB)
            full = np.zeros(model.dim, dtype=complex)
            full[sector_idx] = psi
            tgt[i, s] = obs.expectation(full)
            energy[i, s] = float(np.real(np.vdot(psi, H @ psi)))
            if carrier == "chain":
                c = kr.Q.T @ psi
                if np.sum(np.abs(c) ** 2) < 1 - 1e-6:
                    carrier = "diagonal"  # left the K-dimensional subspace: fall back and record it
            if carrier == "chain":
                recs = sample_exact_chain(c, shots, trng, cfg.chain_settings)
                est, flag, _ = estimate_chain(recs, kr, obs, sector_idx)
            else:
                est, flag = estimate_diagonal(sample_exact_diagonal(full, shots, trng), obs)
            ctx[i, s] = spec.assemble(est, flag, "exact", carrier)
            valid[i, s] = True
            if s < n_steps:
                cM_next = mu2 if (quench_step > 0 and s >= quench_step) else mu
                act[i, s] = (dt, cM_next, cH, cB)
                psi = evolve(cache.hamiltonian(cM_next, cH, cB), psi, np.array([dt]))[0]
                t_acc += dt
        meta.append({"traj": i, "seed": traj_seed, "family": fam.name, "label": label, "n_steps": n_steps, "dt": dt, "mu": mu,
                     "mu2": mu2, "cH": cH, "cB": cB, "start": start, "shots": shots, "quench_step": quench_step,
                     "carrier": carrier, "t_final": t_acc})
        if verbose and (i + 1) % max(1, cfg.n_traj // 10) == 0:
            print(f"  {i + 1}/{cfg.n_traj} trajectories  ({time.time() - t0:.1f} s)")
    # splits by rule
    held = np.zeros(cfg.n_traj, bool)
    val = np.zeros(cfg.n_traj, bool)
    for i, mt in enumerate(meta):
        fam = next(f for f in cfg.families if f.name == mt["family"])
        keys = (mt["label"],) if fam.heldout_by == "label" else (mt["mu"], mt["mu2"])
        held[i] = any(np.isclose(k, h) for k in keys for h in fam.heldout)
        val[i] = (not held[i]) and any(np.isclose(k, v) for k in keys for v in fam.val)
    train = ~held & ~val
    splits = {"train": np.where(train)[0], "val": np.where(val)[0], "test_heldout_mass": np.where(held)[0]}
    for fam in cfg.families:
        fm = np.array([mt["family"] == fam.name for mt in meta])
        splits[f"test_heldout_{fam.name}"] = np.where(held & fm)[0]
    arrays = {"ctx": ctx, "tgt": tgt, "act": act, "valid": valid, "energy": energy}
    np.savez_compressed(out_dir / "dataset.npz", **arrays, **{f"split_{k}": v for k, v in splits.items()})
    manifest = {
        "name": cfg.name, "config": cfg.to_json(), "obs_names": obs.names, "obs_dim": spec.dim, "n_obs": n_obs,
        "action_dim": ACTION_DIM, "n_traj": cfg.n_traj, "T": T, "splits": {k: int(len(v)) for k, v in splits.items()},
        "split_rule": "onfam: held out by g_E label; strong: held out by mu (incl. quench target); never by row",
        "checksum_sha256": _checksum(arrays), "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "wall_seconds": round(time.time() - t0, 1),
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    (out_dir / "meta.json").write_text(json.dumps(meta))
    if verbose:
        print(f"wrote {out_dir / 'dataset.npz'}  checksum {manifest['checksum_sha256'][:12]}  splits {manifest['splits']}")
    return out_dir


def load_dataset(path: str | Path) -> dict:
    path = Path(path)
    z = np.load(path / "dataset.npz")
    d = {k: z[k] for k in z.files}
    d["manifest"] = json.loads((path / "manifest.json").read_text())
    d["meta"] = json.loads((path / "meta.json").read_text())
    return d
