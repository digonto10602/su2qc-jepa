"""Regression fingerprints of the plaquette model (physics-setup notes, section 10.1).

Every number asserted here is derived in docs/PHYSICS.md; a failure points at the step it violates.
"""
import numpy as np
import pytest

from su2qc_jepa.physics import conventions as C
from su2qc_jepa.physics.chain import (
    ChainSpec,
    chain_amplitudes,
    cz_count,
    sample_x_basis,
    sample_z_basis,
    x_basis_probabilities,
)
from su2qc_jepa.physics.dynamics import evolve, krylov_error, lanczos, sector_restrict
from su2qc_jepa.physics.observables import ObservableSet, channel_masks, named_states
from su2qc_jepa.physics.plaquette import FullSpaceOperators, PlaquetteModel


@pytest.fixture(scope="module")
def model():
    return PlaquetteModel(0.5)


def test_counts_sectors_degeneracies(model):
    assert model.dim == C.EXPECTED_DIM[0.5]
    N = model.N_total()
    assert tuple(int((N == n).sum()) for n in (0, 2, 4, 6, 8)) == C.EXPECTED_SECTORS[0.5]
    k = model.excited_links()
    assert tuple(int((k == n).sum()) for n in range(5)) == C.EXPECTED_ELECTRIC_DEGENERACY_HALF
    assert all(len(b.extra["mult_idx"]) == 4 and b.extra["mult_idx"] == (0, 0, 0, 0) for b in model.basis), "intertwiner multiplicity must be 1"


def test_channel_split(model):
    masks = channel_masks(model)
    for k, v in C.EXPECTED_CHANNEL_SPLIT_N4.items():
        assert int(masks[k].sum()) == v, k
    assert int(masks["BBbar"].sum()) == 4
    assert int(masks["hopped"].sum()) == 6
    assert int(masks["S3"].sum()) == 1 and int(masks["S1"].sum()) == 1
    # closure inside N = 4
    assert np.allclose(masks["pair"] + masks["meson"] + masks["baryonic"] + masks["vacmatter"], masks["N4"])


def test_named_state_energies_and_resonance(model):
    mu = C.RESONANCE_MU
    H = model.hamiltonian(C.POINT_PA)
    d = np.diag(H)
    n = named_states(model)
    e = lambda k: d[n[k]] - d[n["vac"]]
    assert np.isclose(e("S3"), 2 * mu + 9 / 4)
    assert np.isclose(e("S1"), 2 * mu + 3 / 4)
    assert np.isclose(e("MM_a"), 4 * mu + 3 / 2) and np.isclose(e("MM_b"), 4 * mu + 3 / 2)
    assert np.isclose(e("loop"), 3.0)
    assert np.isclose(e("antivac"), 8 * mu)
    # the three degeneracies S3/MM, S1/BBbar, S3/loop coincide at mu* = 3/8
    masks = channel_masks(model)
    bb = np.where(masks["BBbar"] > 0)[0]
    assert np.allclose(d[bb] - d[n["vac"]], 4 * mu)
    assert np.isclose(e("S3"), e("MM_a")) and np.isclose(e("S1"), d[bb[0]] - d[n["vac"]]) and np.isclose(e("S3"), e("loop"))


def test_hamiltonian_structure(model):
    hop = model.hopping_matrix()
    plq = model.plaquette_matrix()
    assert int((np.abs(hop) > 1e-12).sum()) == 288, "4 links x 36 disjoint real 2x2 blocks"
    assert int((np.abs(plq) > 1e-12).sum()) == 82, "41 disjoint pairs cover the whole space"
    assert np.allclose(hop, hop.T) and np.allclose(plq, plq.T)
    assert np.abs(hop.imag).max() == 0 and np.abs(plq.imag).max() == 0
    H = model.hamiltonian(C.POINT_PA)
    N = model.N_total()
    assert np.abs(H[np.ix_(N == 4, N != 4)]).max() == 0, "fermion number is conserved"


def test_two_routes_agree_and_gauss_law(model):
    F = FullSpaceOperators(0.5)
    Hf = F.hamiltonian(C.POINT_PA)
    worst = 0.0
    for v in range(4):
        for a in range(3):
            G = F.gauss(v, a)
            worst = max(worst, abs(G @ Hf - Hf @ G).max())
    assert worst < 1e-12
    Q = model.full_space_vectors()
    assert abs((Q.conj().T @ Q) - np.eye(model.dim)).max() < 1e-12
    assert abs(F.gauss_casimir_sum() @ Q).max() < 1e-12
    HB = (Q.conj().T @ Hf @ Q).toarray()
    HA = model.hamiltonian(C.POINT_PA)
    assert np.abs(HA - HB).max() < 1e-12
    P = Q @ Q.conj().T
    assert abs(Hf @ Q - P @ (Hf @ Q)).max() < 1e-12, "H leaves the physical subspace invariant"


def test_dynamics_reproduce_preliminary_expectation(model):
    """Physics-setup notes 8.1 at g_E = 1, mu = 3/8: P_baryonic ~ 0.43, 0.73, 0.82 at t = 1, 2, 3."""
    obs = ObservableSet.primary(model)
    n = named_states(model)
    N4 = model.sector(4)
    H4 = sector_restrict(model.hamiltonian(C.POINT_G1), N4)
    psi0 = np.zeros(len(N4))
    psi0[list(N4).index(n["S3"])] = 1
    psi_t = evolve(H4, psi0, np.array([1.0, 2.0, 3.0]))
    full = np.zeros((3, model.dim), dtype=complex)
    full[:, N4] = psi_t
    ex = obs.expectation(full)
    pb = ex[:, obs.index("P_baryonic")]
    assert np.allclose(pb, [0.43, 0.73, 0.82], atol=0.01)
    assert ex[:, obs.index("P_meson")].max() < 0.04
    assert ex[:, obs.index("P_S1")].max() < 0.02
    assert abs(ex[-1, obs.index("C_string")] - 0.24) < 0.01


def test_krylov_dimension_window_PA(model):
    n = named_states(model)
    N4 = model.sector(4)
    H4 = sector_restrict(model.hamiltonian(C.POINT_PA), N4)
    psi0 = np.zeros(len(N4))
    psi0[list(N4).index(n["S3"])] = 1
    kr = lanczos(H4, psi0)
    obs = ObservableSet.primary(model)
    times = np.linspace(0, 3.0, 25)
    err12 = np.abs(krylov_error(H4, psi0, times, kr.truncate(12), obs.diag[:, N4])["obs_err"]).max()
    assert err12 < 1e-3, "K = 12 must reproduce the P-A window t <= 3/g_E to 1e-3"
    assert kr.beta[26] < 1e-3, "effective Krylov dimension ~27 (beta_27 small) at P-A"


def test_chain_circuit_matches_sector_unitary():
    pytest.importorskip("qiskit")
    from qiskit.quantum_info import Statevector

    from su2qc_jepa.physics.chain import build_chain_circuit

    spec = ChainSpec((0.3, 0.9, 0.2, 0.1, 0.5, 0.2), (0.7, 0.4, 0.6, 0.1, 0.9), 0.3, 5, 2)
    qc = build_chain_circuit(spec, "none")
    sv = Statevector(qc).data
    amps = np.array([sv[1 << k] for k in range(spec.K)])
    c = chain_amplitudes(spec)
    ph = np.vdot(c, amps) / abs(np.vdot(c, amps))
    assert np.abs(amps / ph - c).max() < 1e-12
    assert abs(np.sum(np.abs(amps) ** 2) - 1) < 1e-12, "excitation number conserved"
    assert cz_count(12, 8, 2) == 188 and cz_count(12, 1, 2) == 34


def test_samplers():
    rng = np.random.default_rng(1)
    c = np.array([0.6, 0.3j, -0.4, 0.2 + 0.1j, 0.3, -0.2j])
    c = c / np.linalg.norm(c)
    for basis in ("X", "Y"):
        probs = x_basis_probabilities(c, basis)
        bits = sample_x_basis(c, 100000, rng, basis)
        ints = (bits * (1 << np.arange(6))).sum(1)
        emp = np.bincount(ints, minlength=64) / len(ints)
        assert 0.5 * np.abs(emp - probs).sum() < 0.02
        est = np.mean((-1.0) ** (bits[:, 1] + bits[:, 4]))
        assert abs(est - 2 * np.real(np.conj(c[1]) * c[4])) < 0.02
    z = sample_z_basis(c, 100000, rng)
    assert np.abs(np.bincount(z, minlength=6) / 1e5 - np.abs(c) ** 2).max() < 0.01


@pytest.mark.slow
def test_jmax1_counts():
    m1 = PlaquetteModel(1.0)
    assert m1.dim == C.EXPECTED_DIM[1.0]
    N = m1.N_total()
    assert tuple(int((N == n).sum()) for n in (0, 2, 4, 6, 8)) == C.EXPECTED_SECTORS[1.0]


def test_chain_prep_cascade():
    pytest.importorskip("qiskit")
    from qiskit.quantum_info import Statevector

    from su2qc_jepa.physics.chain import build_chain_prep_circuit

    rng = np.random.default_rng(5)
    for K in (4, 12):
        c = rng.normal(size=K) + 1j * rng.normal(size=K)
        c /= np.linalg.norm(c)
        sv = Statevector(build_chain_prep_circuit(c, "none")).data
        amps = np.array([sv[1 << k] for k in range(K)])
        ph = np.vdot(c, amps) / abs(np.vdot(c, amps))
        assert np.abs(amps / ph - c).max() < 1e-12
        assert sum(1 for g in build_chain_prep_circuit(c, "none").data if g.operation.name == "xx_plus_yy") == K - 1
