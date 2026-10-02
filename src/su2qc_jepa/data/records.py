"""Measurement records and the observation estimator shared by all three sources.

A *record* is what a carrier returns for one (state, measurement setting): a
dictionary of bitstrings -> counts, plus metadata.  The *estimator* turns the
records of one time point into the observation vector o_t.  Exact states, the
Aer twin and the hardware all go through the same estimator, which is what
makes the three sources comparable.

Two carriers are supported:

* ``diagonal``: a Z-basis measurement of a diagonal encoding of the 82-state
  basis (this is how the exact source and the L12 twin look: every primary
  observable is a function of the measured configuration).  Records are counts
  over basis indices.  Flags are leakage flags (zero for the exact source).
* ``chain``: the Krylov-chain carrier (one-hot encoding of K Krylov vectors).
  Records are counts over K-bit strings for settings Z and X (optionally Y).
  Z gives the Krylov populations and the excitation flag; X gives the real
  parts of the Krylov coherences; together they give every physical observable
  through O_K = Q_K^T O Q_K (O diagonal in the configuration basis).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from ..physics.chain import sample_x_basis, sample_z_basis
from ..physics.dynamics import Krylov
from ..physics.observables import ObservableSet

__all__ = ["Record", "ObservationSpec", "estimate_diagonal", "estimate_chain", "sample_exact_diagonal",
           "sample_exact_chain", "SOURCES", "CARRIERS"]

SOURCES = ("exact", "twin", "hardware")
CARRIERS = ("diagonal", "chain")


@dataclass
class Record:
    setting: str  # 'Z', 'X', 'Y' or 'basis' (diagonal carrier)
    counts: dict[str, int]
    shots: int
    source: str
    carrier: str
    meta: dict = field(default_factory=dict)


@dataclass
class ObservationSpec:
    """Layout of the observation vector: observables, flag rate, source and carrier one-hots."""

    obs_names: list[str]

    @property
    def dim(self) -> int:
        return len(self.obs_names) + 1 + len(SOURCES) + len(CARRIERS)

    def assemble(self, obs_est: np.ndarray, flag_rate: float, source: str, carrier: str) -> np.ndarray:
        v = np.zeros(self.dim)
        n = len(self.obs_names)
        v[:n] = obs_est
        v[n] = flag_rate
        v[n + 1 + SOURCES.index(source)] = 1.0
        v[n + 1 + len(SOURCES) + CARRIERS.index(carrier)] = 1.0
        return v

    def split(self, v: np.ndarray) -> dict:
        n = len(self.obs_names)
        return {"obs": v[..., :n], "flag": v[..., n], "source": v[..., n + 1:n + 1 + len(SOURCES)],
                "carrier": v[..., n + 1 + len(SOURCES):]}


# ---------------------------------------------------------------------------
# Diagonal carrier
# ---------------------------------------------------------------------------
def sample_exact_diagonal(psi_full: np.ndarray, shots: int, rng: np.random.Generator) -> Record:
    """Multinomial sample of the configuration basis from an exact state on the full basis."""
    p = np.abs(psi_full) ** 2
    p = p / p.sum()
    draws = rng.multinomial(shots, p)
    counts = {str(i): int(n) for i, n in enumerate(draws) if n > 0}
    return Record("basis", counts, shots, "exact", "diagonal")


def estimate_diagonal(rec: Record, obs: ObservableSet, flagged: int = 0) -> tuple[np.ndarray, float]:
    """Observable estimates from basis-index counts; `flagged` = shots rejected by leakage flags."""
    probs = np.zeros(obs.model.dim)
    kept = 0
    for k, n in rec.counts.items():
        probs[int(k)] += n
        kept += n
    probs /= max(kept, 1)
    flag_rate = flagged / max(kept + flagged, 1)
    return obs.from_counts(probs), flag_rate


# ---------------------------------------------------------------------------
# Chain carrier
# ---------------------------------------------------------------------------
def _bits_from_key(key: str, K: int) -> np.ndarray:
    """Qiskit-style little-endian bitstring (qubit 0 rightmost) -> array of K bits indexed by qubit."""
    s = key.replace(" ", "")
    bits = np.array([int(ch) for ch in s[::-1]], dtype=np.int8)
    if len(bits) < K:
        bits = np.concatenate([bits, np.zeros(K - len(bits), dtype=np.int8)])
    return bits[:K]


def sample_exact_chain(c: np.ndarray, shots: int, rng: np.random.Generator, settings=("Z", "X")) -> list[Record]:
    """Exact-source records of the chain carrier for Krylov amplitudes c (length K)."""
    K = len(c)
    recs = []
    for s in settings:
        counts: dict[str, int] = {}
        if s == "Z":
            idx = sample_z_basis(c, shots, rng)
            for k in idx:
                key = "".join("1" if q == k else "0" for q in range(K))[::-1]
                counts[key] = counts.get(key, 0) + 1
        else:
            bits = sample_x_basis(c, shots, rng, s)
            for row in bits:
                key = "".join(str(b) for b in row)[::-1]
                counts[key] = counts.get(key, 0) + 1
        recs.append(Record(s, counts, shots, "exact", "chain"))
    return recs


def estimate_chain(records: list[Record], kr: Krylov, obs: ObservableSet, sector_idx: np.ndarray,
                   renormalise: bool = True) -> tuple[np.ndarray, float, dict]:
    """Observable estimates from chain records (Z and X; Y used if present as extra statistics).

    Returns (obs_est (n_obs,), flag_rate, extras) where extras holds the Krylov populations and
    the estimated real coherence matrix.  `sector_idx` maps the Krylov vectors (defined on the
    N=4 sector) to the full basis so that O_K = Q^T diag(O) Q can be formed.
    """
    K = kr.K
    recs = {r.setting: r for r in records}
    # --- Z: populations and flag
    z = recs["Z"]
    pops = np.zeros(K)
    kept = flagged = 0
    for key, n in z.counts.items():
        b = _bits_from_key(key, K)
        if b.sum() == 1:
            pops[int(np.argmax(b))] += n
            kept += n
        else:
            flagged += n
    p1 = kept / max(kept + flagged, 1)
    pops = pops / max(kept, 1)
    flag_rate = 1.0 - p1
    # --- X (and Y): real coherences 2 Re rho_kk' = <P_k P_k'> averaged over settings present
    R = np.zeros((K, K))
    nsets = 0
    for s in ("X", "Y"):
        if s not in recs:
            continue
        r = recs[s]
        tot = sum(r.counts.values())
        acc = np.zeros((K, K))
        for key, n in r.counts.items():
            b = _bits_from_key(key, K)
            sgn = 1.0 - 2.0 * b  # (+1 for bit 0, -1 for bit 1)
            acc += n * np.outer(sgn, sgn)
        acc /= max(tot, 1)
        R += acc
        nsets += 1
    if nsets:
        R /= nsets
        if renormalise and p1 > 0:
            R = R / p1  # sector renormalisation: coherences scaled by the single-excitation fraction
    rho_re = 0.5 * R
    np.fill_diagonal(rho_re, pops)
    # --- observables: O_K = Q^T diag(O) Q restricted to the sector
    Qs = kr.Q  # (dim_sector, K)
    est = np.zeros(len(obs.names))
    for i in range(len(obs.names)):
        Od = obs.diag[i, sector_idx]
        OK = Qs.T @ (Od[:, None] * Qs)
        est[i] = float(np.sum(OK * rho_re))
    return est, flag_rate, {"pops": pops, "rho_re": rho_re, "p1": p1}
