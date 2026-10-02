"""SU(2) building blocks: spin matrices and Clebsch-Gordan coefficients.

Everything here is plain NumPy; spins are given as floats (0, 0.5, 1, ...).
The Clebsch-Gordan coefficient uses the Racah closed form, which is exact for
the small spins used in this package (j <= 2 in practice).
"""
from __future__ import annotations

from fractions import Fraction
from functools import cache
from math import factorial, sqrt

import numpy as np

__all__ = ["spin_matrices", "clebsch_gordan", "m_values", "is_half_int"]


def is_half_int(x: float) -> bool:
    return abs(2 * x - round(2 * x)) < 1e-12


def m_values(j: float) -> list[float]:
    """Magnetic quantum numbers m = -j, -j+1, ..., +j (ascending)."""
    twoj = int(round(2 * j))
    return [(-twoj + 2 * k) / 2 for k in range(twoj + 1)]


def spin_matrices(j: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (Sx, Sy, Sz) for spin j in the basis ordered as m_values(j)."""
    ms = m_values(j)
    d = len(ms)
    sz = np.diag(ms).astype(complex)
    sp = np.zeros((d, d), dtype=complex)
    for a, ma in enumerate(ms):
        for b, mb in enumerate(ms):
            if abs(ma - mb - 1) < 1e-12:  # <ma| S+ |mb> with ma = mb + 1
                sp[a, b] = sqrt(j * (j + 1) - mb * (mb + 1))
    sm = sp.conj().T
    sx = (sp + sm) / 2
    sy = (sp - sm) / (2j)
    return sx, sy, sz


def _fact(n: Fraction | int | float) -> int:
    n = Fraction(n)
    if n.denominator != 1 or n < 0:
        raise ValueError(f"factorial of non-integer or negative: {n}")
    return factorial(int(n))


@cache
def _cg_cached(j1: Fraction, m1: Fraction, j2: Fraction, m2: Fraction, J: Fraction, M: Fraction) -> float:
    if m1 + m2 != M:
        return 0.0
    if J < abs(j1 - j2) or J > j1 + j2:
        return 0.0
    if abs(m1) > j1 or abs(m2) > j2 or abs(M) > J:
        return 0.0
    if (j1 + j2 + J).denominator != 1:
        return 0.0
    pref = Fraction(2 * J + 1) * Fraction(_fact(J + j1 - j2) * _fact(J - j1 + j2) * _fact(j1 + j2 - J), _fact(j1 + j2 + J + 1))
    pref *= Fraction(_fact(J + M) * _fact(J - M) * _fact(j1 - m1) * _fact(j1 + m1) * _fact(j2 - m2) * _fact(j2 + m2))
    total = Fraction(0)
    k = 0
    while True:
        args = [j1 + j2 - J - k, j1 - m1 - k, j2 + m2 - k, J - j2 + m1 + k, J - j1 - m2 + k]
        if any(a < 0 for a in args[:3]) and k > 0 and all(a < 0 for a in args[:3]):
            break
        if all(a >= 0 for a in args):
            den = _fact(k) * _fact(args[0]) * _fact(args[1]) * _fact(args[2]) * _fact(args[3]) * _fact(args[4])
            total += Fraction((-1) ** k, den)
        k += 1
        if k > 2 * (j1 + j2) + 2:
            break
    val = float(total) * sqrt(float(pref))
    return val


def clebsch_gordan(j1: float, m1: float, j2: float, m2: float, J: float, M: float) -> float:
    """Clebsch-Gordan coefficient <j1 m1; j2 m2 | J M> (Condon-Shortley phase)."""
    return _cg_cached(Fraction(j1).limit_denominator(2), Fraction(m1).limit_denominator(2),
                      Fraction(j2).limit_denominator(2), Fraction(m2).limit_denominator(2),
                      Fraction(J).limit_denominator(2), Fraction(M).limit_denominator(2))
