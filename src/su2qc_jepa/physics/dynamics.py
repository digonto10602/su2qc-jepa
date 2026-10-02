"""Exact real-time evolution and Lanczos/Krylov compression.

`evolve` uses an eigendecomposition of the (small, real symmetric) Hamiltonian.
`lanczos` returns the tridiagonal (alpha, beta) coefficients and the orthonormal
Krylov vectors Q_K obtained from a start vector, with full reorthogonalisation.
`krylov_error` quantifies the truncation error of propagating inside the
K-dimensional Krylov subspace against the exact evolution.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

__all__ = ["evolve", "lanczos", "Krylov", "krylov_error", "sector_restrict"]


def sector_restrict(H: np.ndarray, idx: np.ndarray) -> np.ndarray:
    return H[np.ix_(idx, idx)]


def evolve(H: np.ndarray, psi0: np.ndarray, times: np.ndarray) -> np.ndarray:
    """psi(t) = exp(-i H t) psi0 for each t; returns array (n_times, dim)."""
    w, V = np.linalg.eigh(H)
    c = V.T @ psi0
    phases = np.exp(-1j * np.outer(times, w))  # (nt, dim)
    return (phases * c) @ V.T


@dataclass
class Krylov:
    alpha: np.ndarray  # diagonal of the tridiagonal H_K (length K)
    beta: np.ndarray  # off-diagonal (length K-1)
    Q: np.ndarray  # (dim, K) orthonormal Krylov vectors; Q[:,0] is the start vector
    K_full: int  # dimension at which the Lanczos recursion terminated (beta ~ 0)

    @property
    def K(self) -> int:
        return len(self.alpha)

    def H_K(self) -> np.ndarray:
        return np.diag(self.alpha) + np.diag(self.beta, 1) + np.diag(self.beta, -1)

    def truncate(self, K: int) -> Krylov:
        return Krylov(self.alpha[:K], self.beta[:K - 1], self.Q[:, :K], self.K_full)

    def project(self, O: np.ndarray) -> np.ndarray:
        """O_K = Q^dag O Q for a (diagonal vector or full matrix) observable."""
        if O.ndim == 1:
            return self.Q.T @ (O[:, None] * self.Q)
        return self.Q.T @ O @ self.Q

    def coefficients(self, times: np.ndarray) -> np.ndarray:
        """Krylov-basis amplitudes c_k(t) = <k| exp(-i H_K t) |0>, shape (nt, K)."""
        e0 = np.zeros(self.K)
        e0[0] = 1.0
        return evolve(self.H_K(), e0, times)


def lanczos(H: np.ndarray, v0: np.ndarray, K: int | None = None, tol: float = 1e-10) -> Krylov:
    """Lanczos with full reorthogonalisation. Stops early when the recursion terminates."""
    n = H.shape[0]
    Kmax = n if K is None else min(K, n)
    Q = np.zeros((n, Kmax))
    alphas, betas = [], []
    q = v0 / np.linalg.norm(v0)
    Q[:, 0] = q
    k_full = Kmax
    for k in range(Kmax):
        w = H @ Q[:, k]
        a = Q[:, k] @ w
        alphas.append(a)
        w = w - a * Q[:, k] - (betas[-1] * Q[:, k - 1] if k > 0 else 0)
        # full reorthogonalisation (twice is enough)
        for _ in range(2):
            w = w - Q[:, :k + 1] @ (Q[:, :k + 1].T @ w)
        b = np.linalg.norm(w)
        if k == Kmax - 1:
            break
        if b < tol:
            k_full = k + 1
            Q = Q[:, :k + 1]
            break
        betas.append(b)
        Q[:, k + 1] = w / b
    return Krylov(np.array(alphas), np.array(betas), Q, k_full)


def krylov_error(H: np.ndarray, psi0: np.ndarray, times: np.ndarray, kr: Krylov, O_diag: np.ndarray | None = None):
    """Infidelity and observable error of the K-dim Krylov propagation versus exact evolution.

    Returns dict with 'infidelity' (nt,), 'obs_err' (nt, n_obs) if O_diag (n_obs, dim) given.
    """
    exact = evolve(H, psi0, times)  # (nt, dim)
    c = kr.coefficients(times)  # (nt, K)
    approx = c @ kr.Q.T  # (nt, dim)
    fid = np.abs(np.einsum("ti,ti->t", exact.conj(), approx)) ** 2
    out = {"infidelity": 1 - fid}
    if O_diag is not None:
        pe = np.abs(exact) ** 2 @ O_diag.T
        pa = np.abs(approx) ** 2 @ O_diag.T
        out["obs_err"] = pa - pe
    return out
