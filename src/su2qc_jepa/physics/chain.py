"""The Krylov-chain hardware carrier (one-hot / unary encoding of the Lanczos basis).

Given the tridiagonal Krylov Hamiltonian H_K = sum_k alpha_k |k><k| + sum_k beta_k (|k><k+1| + h.c.),
encode the K Krylov vectors as the K single-excitation states |k> = |0..010..0> of K qubits on a
line.  In the single-excitation sector
    |k><k|            -> n_k = (1 - Z_k)/2
    |k><k+1| + h.c.   -> (X_k X_{k+1} + Y_k Y_{k+1})/2
so H_K becomes a nearest-neighbour XY chain with site-dependent fields, and
exp(-i H_K t) is realised by a second-order (Strang) product formula whose
entangling cost is 2 CZ per bond per step on IBM hardware.

The circuit conserves the excitation number, so any shot outside the single-
excitation sector is a detectable error ("excitation flag"), the chain analogue
of the gauge-leakage flags of the L12 encoding.

`chain_sector_unitary` gives the exact K x K action of the *ideal* Trotter circuit
inside the single-excitation sector (no 2^K simulation needed), which is the
noiseless reference against which hardware and twin records are compared.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .dynamics import Krylov

__all__ = ["ChainSpec", "chain_sector_unitary", "chain_amplitudes", "cz_count", "trotter_error",
           "build_chain_circuit", "x_basis_probabilities", "sample_x_basis", "sample_z_basis"]


@dataclass(frozen=True)
class ChainSpec:
    alpha: tuple[float, ...]
    beta: tuple[float, ...]
    dt: float
    steps: int
    order: int = 2  # 1 = Lie-Trotter, 2 = Strang

    @property
    def K(self) -> int:
        return len(self.alpha)

    @property
    def t(self) -> float:
        return self.dt * self.steps

    @classmethod
    def from_krylov(cls, kr: Krylov, K: int, dt: float, steps: int, order: int = 2) -> ChainSpec:
        kk = kr.truncate(K)
        return cls(tuple(float(a) for a in kk.alpha), tuple(float(b) for b in kk.beta), float(dt), int(steps), int(order))


def _bond_rotation(K: int, k: int, theta: float) -> np.ndarray:
    """exp(-i theta h_k) in the single-excitation sector, h_k = |k><k+1| + h.c."""
    M = np.eye(K, dtype=complex)
    c, s = np.cos(theta), np.sin(theta)
    M[k, k] = c
    M[k + 1, k + 1] = c
    M[k, k + 1] = -1j * s
    M[k + 1, k] = -1j * s
    return M


def _layer(K: int, beta: np.ndarray, parity: int, factor: float, dt: float) -> np.ndarray:
    M = np.eye(K, dtype=complex)
    for k in range(parity, K - 1, 2):
        M = _bond_rotation(K, k, beta[k] * dt * factor) @ M
    return M


def chain_sector_unitary(spec: ChainSpec) -> np.ndarray:
    """Exact K x K unitary of the ideal Trotter circuit for one full evolution (all steps)."""
    K = spec.K
    alpha, beta = np.array(spec.alpha), np.array(spec.beta)
    if spec.order == 1:
        # Lie-Trotter: A then E then O (time order)
        step = _layer(K, beta, 1, 1.0, spec.dt) @ _layer(K, beta, 0, 1.0, spec.dt) @ np.diag(np.exp(-1j * alpha * spec.dt))
    else:
        # Strang, palindromic in time order: E/2, A/2, O, A/2, E/2  (even half-layers merge between steps)
        A = np.diag(np.exp(-1j * alpha * spec.dt / 2))
        E = _layer(K, beta, 0, 0.5, spec.dt)
        O = _layer(K, beta, 1, 1.0, spec.dt)
        step = E @ A @ O @ A @ E
    return np.linalg.matrix_power(step, spec.steps)


def chain_amplitudes(spec: ChainSpec) -> np.ndarray:
    """Krylov amplitudes c_k produced by the ideal circuit from |k=0>."""
    U = chain_sector_unitary(spec)
    return U[:, 0]


def trotter_error(kr: Krylov, K: int, dt: float, steps: int, order: int = 2) -> float:
    """Infidelity between the ideal Trotter circuit output and exp(-i H_K t)|0> for the truncated chain."""
    spec = ChainSpec.from_krylov(kr, K, dt, steps, order)
    c_tr = chain_amplitudes(spec)
    c_ex = kr.truncate(K).coefficients(np.array([spec.t]))[0]
    return float(1 - abs(np.vdot(c_ex, c_tr)) ** 2)


def cz_count(K: int, steps: int, order: int = 2) -> int:
    """Two-qubit (CZ) count on IBM hardware: 2 CZ per XX+YY rotation; adjacent half-layers merged."""
    bonds_even = len(range(0, K - 1, 2))
    bonds_odd = len(range(1, K - 1, 2))
    if order == 1:
        return 2 * steps * (bonds_even + bonds_odd)
    # Strang: E/2 O E/2 per step; consecutive E/2 E/2 merge -> (steps+1) even layers, steps odd layers
    return 2 * ((steps + 1) * bonds_even + steps * bonds_odd)


def build_chain_circuit(spec: ChainSpec, measure_basis: str = "Z"):
    """Qiskit circuit for the chain carrier. measure_basis in {'Z','X','Y'}; 'none' for no measurement."""
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import XXPlusYYGate

    K = spec.K
    qc = QuantumCircuit(K, K if measure_basis != "none" else 0)
    qc.x(0)  # |k=0> = first Krylov vector = the initial physical state
    alpha, beta = spec.alpha, spec.beta

    def z_layer(f):
        for k in range(K):
            if abs(alpha[k]) > 0:
                # n_k = (1-Z)/2 : exp(-i alpha n_k dt) = Rz(-alpha dt) up to a global phase
                qc.rz(-alpha[k] * spec.dt * f, k)

    def bond_layer(parity, f):
        for k in range(parity, K - 1, 2):
            # XXPlusYYGate(theta) = exp(-i theta/4 (XX+YY)) ; we need exp(-i beta dt f (XX+YY)/2) -> theta = 2 beta dt f
            qc.append(XXPlusYYGate(2 * beta[k] * spec.dt * f), [k, k + 1])

    if spec.order == 1:
        for _ in range(spec.steps):
            z_layer(1.0)
            bond_layer(0, 1.0)
            bond_layer(1, 1.0)
    else:
        # time order per step: E/2, A/2, O, A/2, E/2 ; consecutive E/2 E/2 are merged into one E layer
        bond_layer(0, 0.5)
        for s in range(spec.steps):
            z_layer(0.5)
            bond_layer(1, 1.0)
            z_layer(0.5)
            bond_layer(0, 1.0 if s < spec.steps - 1 else 0.5)
    if measure_basis == "X":
        qc.h(range(K))
    elif measure_basis == "Y":
        qc.sdg(range(K))
        qc.h(range(K))
    if measure_basis != "none":
        qc.measure(range(K), range(K))
    return qc


# ---------------------------------------------------------------------------
# Exact sampling of the ideal single-excitation state in the Z, X and Y bases
# ---------------------------------------------------------------------------
def sample_z_basis(c: np.ndarray, shots: int, rng: np.random.Generator) -> np.ndarray:
    """Z-basis outcomes for the state sum_k c_k |k>: returns the excited index per shot."""
    p = np.abs(c) ** 2
    p = p / p.sum()
    return rng.choice(len(c), size=shots, p=p)


def _phase_weights(K: int, basis: str) -> np.ndarray:
    """omega_k(x) for x in {0,1}: <x_k basis| 1_k> up to the common 1/sqrt2 and the |0> reference."""
    # For |+>,|-> : <x|1> = (+1, -1)/sqrt2 relative to <x|0> = (+1,+1)/sqrt2  -> ratio (+1,-1)
    # For |+i>,|-i>: <x|1> = (-i, +i)/sqrt2 relative to <x|0> = (+1,+1)/sqrt2 -> ratio (-i,+i)
    if basis == "X":
        return np.array([1.0, -1.0], dtype=complex)
    if basis == "Y":
        return np.array([-1j, 1j], dtype=complex)
    raise ValueError(basis)


def x_basis_probabilities(c: np.ndarray, basis: str = "X") -> np.ndarray:
    """Full 2^K probability vector of measuring sum_k c_k|k> in the X (or Y) basis; small K only."""
    K = len(c)
    w = _phase_weights(K, basis)
    probs = np.zeros(2**K)
    for x in range(2**K):
        bits = [(x >> k) & 1 for k in range(K)]
        amp = sum(c[k] * w[bits[k]] for k in range(K)) / np.sqrt(2**K)
        probs[x] = abs(amp) ** 2
    return probs


def sample_x_basis(c: np.ndarray, shots: int, rng: np.random.Generator, basis: str = "X") -> np.ndarray:
    """Exact sequential sampling of X- or Y-basis bitstrings for the single-excitation state.

    Uses the closed-form marginals P(x_1..x_j) = 2^{-j} (|a_j|^2 + R_j), where a_j = sum_{l<=j} c_l w(x_l)
    and R_j = sum_{l>j} |c_l|^2.  Returns an integer array (shots, K) of bits.
    """
    K = len(c)
    w = _phase_weights(K, basis)
    R = np.concatenate([np.cumsum((np.abs(c) ** 2)[::-1])[::-1][1:], [0.0]])  # R[j] = sum_{l>j} |c_l|^2
    out = np.zeros((shots, K), dtype=np.int8)
    a = np.zeros(shots, dtype=complex)
    prev = np.full(shots, 1.0)  # |a_{j-1}|^2 + R_{j-1} with R_{-1} = 1 (normalised c)
    for j in range(K):
        a0 = a + c[j] * w[0]
        a1 = a + c[j] * w[1]
        p0 = (np.abs(a0) ** 2 + R[j]) / (2 * prev)
        u = rng.random(shots)
        bit = (u > p0).astype(np.int8)
        out[:, j] = bit
        a = np.where(bit == 0, a0, a1)
        prev = np.where(bit == 0, np.abs(a0) ** 2 + R[j], np.abs(a1) ** 2 + R[j])
    return out


# ---------------------------------------------------------------------------
# KC-prep: direct preparation of a single-excitation state (Givens cascade), K-1 XY rotations
# ---------------------------------------------------------------------------
def prep_cascade_params(c: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Angles theta_k (k = 0..K-2) of XXPlusYY(theta_k, 0) on (k, k+1) and the final Rz phases phi_k.

    Moves amplitude down the chain from |0>: after step k qubit k keeps |c_k| and the remainder moves
    to qubit k+1 with the factor -i sin(theta/2); phases are repaired by one Rz layer at the end.
    """
    c = np.asarray(c, dtype=complex)
    K = len(c)
    thetas = np.zeros(K - 1)
    tilde = np.zeros(K, dtype=complex)
    A = 1.0 + 0j  # amplitude currently sitting on qubit k
    for k in range(K - 1):
        R = abs(A)
        ratio = min(1.0, abs(c[k]) / R) if R > 1e-15 else 1.0
        theta = 2 * np.arccos(ratio)
        thetas[k] = theta
        tilde[k] = A * np.cos(theta / 2)
        A = A * (-1j) * np.sin(theta / 2)
    tilde[K - 1] = A
    phis = np.angle(c) - np.angle(tilde)
    phis[np.abs(c) < 1e-15] = 0.0
    return thetas, phis


def build_chain_prep_circuit(c: np.ndarray, measure_basis: str = "Z"):
    """Qiskit circuit preparing sum_k c_k |k> (one-hot) with K-1 XX+YY rotations and one Rz layer."""
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import XXPlusYYGate

    c = np.asarray(c, dtype=complex)
    c = c / np.linalg.norm(c)
    K = len(c)
    thetas, phis = prep_cascade_params(c)
    qc = QuantumCircuit(K, K if measure_basis != "none" else 0)
    qc.x(0)
    for k in range(K - 1):
        if abs(thetas[k]) > 1e-12:
            qc.append(XXPlusYYGate(thetas[k], 0.0), [k, k + 1])
    for k in range(K):
        if abs(phis[k]) > 1e-12:
            qc.rz(phis[k], k)
    if measure_basis == "X":
        qc.h(range(K))
    elif measure_basis == "Y":
        qc.sdg(range(K))
        qc.h(range(K))
    if measure_basis != "none":
        qc.measure(range(K), range(K))
    return qc
