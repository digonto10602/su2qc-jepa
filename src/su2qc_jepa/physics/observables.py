"""Observables of the plaquette in the gauge-invariant configuration basis.

All primary observables are diagonal in this basis (densities, link Casimirs,
channel projectors), so one Z-basis measurement of any diagonal encoding gives
all of them.  The energy is the only non-diagonal observable.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from . import conventions as C
from .plaquette import PlaquetteModel

__all__ = ["ObservableSet", "named_states", "channel_masks"]


def named_states(model: PlaquetteModel) -> dict[str, int]:
    """Indices of the named states (physics-setup notes, section 5)."""
    h = 0.5
    names = {
        "vac": model.find((0, 0, 0, 0), C.VACUUM_N),
        "loop": model.find((h, h, h, h), C.VACUUM_N),
        "S3": model.find((0, h, h, h), (1, 1, 0, 2)),  # stretched string on l1,l2,l3
        "S1": model.find((h, 0, 0, 0), (1, 1, 0, 2)),  # short string on la
        "MM_a": model.find((0, h, 0, h), (1, 1, 1, 1)),  # two mesons on l1,l3
        "MM_b": model.find((h, 0, h, 0), (1, 1, 1, 1)),  # two mesons on la,l2
        "antivac": model.find((0, 0, 0, 0), (2, 0, 2, 0)),
    }
    return names


def channel_masks(model: PlaquetteModel) -> dict[str, np.ndarray]:
    """0/1 diagonal masks of the channel projectors on the full basis (physics-setup notes 6.1).

    Channels are defined by matter content only (inside the N = 4 sector):
      pair      : one even and one odd site at N = 1, the other two at vacuum occupation
      meson     : all four sites at N = 1
      vacmatter : matter at vacuum occupation everywhere (vac and loop)
      baryonic  : everything else in N = 4
    Sub-projectors: S3, S1, hopped (pair on the other three bonds), BBbar (flux-free
    baryon-antibaryon), antivac.
    """
    d = model.dim
    N = model.N_total()
    masks = {k: np.zeros(d) for k in ("pair", "meson", "vacmatter", "baryonic", "S3", "S1", "hopped", "BBbar", "antivac", "N4")}
    names = named_states(model)
    for b in model.basis:
        i = b.index
        if N[i] != 4:
            continue
        masks["N4"][i] = 1
        n = b.Nconf
        even_one = [v for v in C.EVEN_VERTICES if n[v] == 1]
        odd_one = [v for v in C.ODD_VERTICES if n[v] == 1]
        vac_rest = all(n[v] == C.VACUUM_N[v] for v in range(4) if n[v] != 1)
        if len(even_one) == 1 and len(odd_one) == 1 and vac_rest:
            masks["pair"][i] = 1
        elif all(x == 1 for x in n):
            masks["meson"][i] = 1
        elif tuple(n) == C.VACUUM_N:
            masks["vacmatter"][i] = 1
        else:
            masks["baryonic"][i] = 1
            # flux-free baryon-antibaryon: exactly one even site doubly occupied and one odd site empty
            even2 = sum(1 for v in C.EVEN_VERTICES if n[v] == 2)
            odd0 = sum(1 for v in C.ODD_VERTICES if n[v] == 0)
            if all(j == 0 for j in b.jconf) and even2 == 1 and odd0 == 1:
                masks["BBbar"][i] = 1
    masks["S3"][names["S3"]] = 1
    masks["S1"][names["S1"]] = 1
    masks["antivac"][names["antivac"]] = 1
    masks["hopped"] = masks["pair"] - masks["S3"] - masks["S1"]
    return masks


@dataclass
class ObservableSet:
    """Diagonal observables as vectors on the basis plus the derived quantities."""

    model: PlaquetteModel
    names: list[str]
    diag: np.ndarray  # (n_obs, dim)

    @classmethod
    def primary(cls, model: PlaquetteModel) -> ObservableSet:
        names, rows = [], []
        for v in range(4):
            names.append(f"N{v}")
            rows.append(model.density_diag(v))
        for l in range(4):
            names.append(f"C{C.LINK_NAMES[l]}")
            rows.append(model.casimir_diag(l))
        masks = channel_masks(model)
        for k in ("pair", "meson", "baryonic", "vacmatter", "S3", "S1", "hopped", "BBbar", "antivac"):
            names.append(f"P_{k}")
            rows.append(masks[k])
        names.append("C_string")
        rows.append(sum(model.casimir_diag(l) for l in C.STRING_LINKS) / len(C.STRING_LINKS))
        return cls(model, names, np.array(rows, dtype=float))

    def expectation(self, psi: np.ndarray) -> np.ndarray:
        """Expectation values for a state vector (or batch of states along axis 0)."""
        p = np.abs(psi) ** 2
        return p @ self.diag.T

    def from_counts(self, probs: np.ndarray) -> np.ndarray:
        """Expectation values from a probability vector over the basis."""
        return probs @ self.diag.T

    def index(self, name: str) -> int:
        return self.names.index(name)

    def derived(self, exp: np.ndarray) -> dict[str, np.ndarray]:
        """Derived quantities from a row (or rows) of expectation values."""
        g = lambda k: exp[..., self.index(k)]
        return {
            "string_survival": g("P_pair"),
            "intact_string": g("P_S3") + g("P_S1"),
            "breaking_fraction": g("P_meson") + g("P_baryonic"),
            "R_BM": g("P_BBbar") / np.maximum(g("P_meson"), 1e-12),
        }
