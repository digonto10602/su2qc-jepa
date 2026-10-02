"""Hard-core SU(2) Kogut-Susskind plaquette with two-colour staggered fermions.

Two independent constructions are provided and cross-checked in the tests:

* **Route A (vertex singlets, block tensors)** - `PlaquetteModel` builds the
  gauge-invariant (GI) basis as a configuration basis labelled by the four link
  spins and the four site occupations, with the colour structure fixed by the
  unique singlet at every vertex.  Hamiltonian matrix elements are computed by
  applying each term to the block tensor of a basis state.  Works for any j_max.
* **Route B (full gauge-redundant space)** - `FullSpaceOperators` builds every
  operator as a sparse matrix on the full link (x) matter space and lets the
  tests check (i) that H commutes with all Gauss-law generators, (ii) that the
  route-A basis vectors are annihilated by the generators and (iii) that
  Q^dag H Q reproduces route A.  Practical for j_max = 1/2 (160,000 states).

Units: H is measured in units of g_E (see conventions.Couplings).
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass, field

import numpy as np
import scipy.sparse as sp

from . import conventions as C
from .su2 import clebsch_gordan, m_values, spin_matrices

__all__ = ["LinkSpace", "MatterSpace", "PlaquetteModel", "FullSpaceOperators", "GIBasisState"]

HALF = 0.5


# ----------------------------------------------------------------------------
# Local spaces
# ----------------------------------------------------------------------------
class LinkSpace:
    """Electric basis |j, mL, mR> of one SU(2) link truncated at j_max."""

    def __init__(self, jmax: float):
        self.jmax = float(jmax)
        n = int(round(2 * self.jmax))
        self.js: list[float] = [k / 2 for k in range(n + 1)]
        self.states: list[tuple[float, float, float]] = []
        self.offset: dict[float, int] = {}
        self.block_dim: dict[float, int] = {}
        for j in self.js:
            self.offset[j] = len(self.states)
            ms = m_values(j)
            self.block_dim[j] = len(ms) ** 2
            for mL in ms:
                for mR in ms:
                    self.states.append((j, mL, mR))
        self.dim = len(self.states)
        self.index = {s: i for i, s in enumerate(self.states)}
        self._U_cache: dict[tuple[float, float], np.ndarray] = {}

    def j_of(self, i: int) -> float:
        return self.states[i][0]

    def casimir(self) -> np.ndarray:
        return np.array([j * (j + 1) for (j, _, _) in self.states])

    def U(self, alpha: float, beta: float) -> np.ndarray:
        """Matrix of U^{alpha beta} (alpha = left colour index, beta = right)."""
        key = (alpha, beta)
        if key in self._U_cache:
            return self._U_cache[key]
        M = np.zeros((self.dim, self.dim))
        for col, (j, mL, mR) in enumerate(self.states):
            for J in (j - HALF, j + HALF):
                if J < 0 or J > self.jmax + 1e-12:
                    continue
                ML, MR = mL + alpha, mR + beta
                if abs(ML) > J + 1e-12 or abs(MR) > J + 1e-12:
                    continue
                row = self.index.get((J, ML, MR))
                if row is None:
                    continue
                M[row, col] = (np.sqrt((2 * j + 1) / (2 * J + 1))
                               * clebsch_gordan(j, mL, HALF, alpha, J, ML)
                               * clebsch_gordan(j, mR, HALF, beta, J, MR))
        self._U_cache[key] = M
        return M

    def E(self, a: int, side: str) -> np.ndarray:
        """Gauss-law generator component a in {0,1,2} acting on the left (mL) or right (mR) index.

        Convention (frozen, verified by the commutator test): the left generator acts on mL
        as -(S^a)^T and the right generator acts on mR as +S^a, block-diagonally in j.
        """
        M = np.zeros((self.dim, self.dim), dtype=complex)
        for j in self.js:
            S = spin_matrices(j)[a]
            d = len(m_values(j))
            blk = np.kron(-S.T, np.eye(d)) if side == "L" else np.kron(np.eye(d), S)
            o = self.offset[j]
            M[o:o + d * d, o:o + d * d] = blk
        return M


class MatterSpace:
    """Four staggered two-colour fermion sites, eight Jordan-Wigner modes, 256 Fock states.

    Mode k = 2*v + c where c = 0 for colour m=-1/2 and c = 1 for colour m=+1/2.
    Fock index f has bit k set when mode k is occupied.
    """

    NMODES = 8
    DIM = 256

    def __init__(self):
        self.colours = m_values(HALF)  # [-0.5, +0.5]
        self._c = [self._annihilation(k) for k in range(self.NMODES)]
        self._cdag = [m.T.tocsr() for m in self._c]  # real matrices -> transpose is adjoint
        self.N_site = [sum(self.number(2 * v + c) for c in range(2)) for v in range(4)]
        self.site_N = np.zeros((4, self.DIM), dtype=int)
        for f in range(self.DIM):
            for v in range(4):
                self.site_N[v, f] = ((f >> (2 * v)) & 1) + ((f >> (2 * v + 1)) & 1)

    @staticmethod
    def _annihilation(k: int) -> sp.csr_matrix:
        rows, cols, vals = [], [], []
        for f in range(MatterSpace.DIM):
            if (f >> k) & 1:
                sign = (-1) ** bin(f & ((1 << k) - 1)).count("1")
                rows.append(f ^ (1 << k))
                cols.append(f)
                vals.append(float(sign))
        return sp.csr_matrix((vals, (rows, cols)), shape=(MatterSpace.DIM, MatterSpace.DIM))

    def mode(self, v: int, colour: float) -> int:
        return 2 * v + self.colours.index(colour)

    def c(self, v: int, colour: float) -> sp.csr_matrix:
        return self._c[self.mode(v, colour)]

    def cdag(self, v: int, colour: float) -> sp.csr_matrix:
        return self._cdag[self.mode(v, colour)]

    def number(self, k: int) -> sp.csr_matrix:
        return sp.diags([float((f >> k) & 1) for f in range(self.DIM)]).tocsr()

    def charge(self, v: int, a: int) -> sp.csr_matrix:
        """Q^a_v = sum_{alpha beta} c^dag_{v alpha} (S^a)_{alpha beta} c_{v beta}."""
        S = spin_matrices(HALF)[a]
        Q = sp.csr_matrix((self.DIM, self.DIM), dtype=complex)
        for ia, al in enumerate(self.colours):
            for ib, be in enumerate(self.colours):
                if abs(S[ia, ib]) > 1e-15:
                    Q = Q + S[ia, ib] * (self.cdag(v, al) @ self.c(v, be))
        return Q.tocsr()

    def fock_states_with(self, Nconf: tuple[int, ...]) -> list[int]:
        """Fock indices whose per-site occupations equal Nconf (ascending order)."""
        return [f for f in range(self.DIM) if all(self.site_N[v, f] == Nconf[v] for v in range(4))]


# ----------------------------------------------------------------------------
# Route A: gauge-invariant configuration basis from vertex singlets
# ----------------------------------------------------------------------------
# vertex -> ((link, side), (link, side)) in the order (prev, next) used by the notes:
# v0: (l1 tail? no) -- we store the two slots as they appear in the geometry.
VERTEX_SLOTS = (
    ((0, "L"), (1, "L")),  # v0: tail of la and tail of l1
    ((0, "R"), (3, "L")),  # v1: head of la and tail of l3
    ((3, "R"), (2, "R")),  # v2: head of l3 and head of l2
    ((2, "L"), (1, "R")),  # v3: tail of l2 and head of l1
)


@dataclass
class GIBasisState:
    jconf: tuple[float, float, float, float]
    Nconf: tuple[int, int, int, int]
    mult: int
    fock_idx: list[int]
    psi: np.ndarray  # shape (d0, d1, d2, d3, m) over local link states within each j and the matter block
    index: int = -1
    extra: dict = field(default_factory=dict)

    @property
    def label(self) -> tuple:
        return (self.jconf, self.Nconf, self.mult)


class PlaquetteModel:
    """Gauge-invariant basis and Hamiltonian of the single plaquette (route A)."""

    def __init__(self, jmax: float = 0.5):
        self.jmax = float(jmax)
        self.link = LinkSpace(self.jmax)
        self.matter = MatterSpace()
        self.basis: list[GIBasisState] = []
        self.by_label: dict[tuple, int] = {}
        self._build_basis()
        self.dim = len(self.basis)
        self._diag_cache: dict = {}
        self._H_terms_cache: dict = {}

    # -- vertex singlets ------------------------------------------------------
    def _local_null_space(self, v: int, jconf, Nv: int) -> np.ndarray:
        """Orthonormal basis of the singlet subspace at vertex v (columns), in the local
        basis ordered as (slot1 m, slot2 m, matter state)."""
        (l1, s1), (l2, s2) = VERTEX_SLOTS[v]
        j1, j2 = jconf[l1], jconf[l2]
        d1, d2 = len(m_values(j1)), len(m_values(j2))
        dm = {0: 1, 1: 2, 2: 1}[Nv]
        D = d1 * d2 * dm
        Ctot = np.zeros((D, D), dtype=complex)
        for a in range(3):
            S1 = spin_matrices(j1)[a]
            S2 = spin_matrices(j2)[a]
            E1 = -S1.T if s1 == "L" else S1
            E2 = -S2.T if s2 == "L" else S2
            Qm = spin_matrices(HALF)[a] if Nv == 1 else np.zeros((dm, dm))
            G = (np.kron(np.kron(E1, np.eye(d2)), np.eye(dm))
                 + np.kron(np.kron(np.eye(d1), E2), np.eye(dm))
                 + np.kron(np.kron(np.eye(d1), np.eye(d2)), Qm))
            Ctot += G @ G
        w, V = np.linalg.eigh(Ctot)
        null = V[:, w < 1e-9]
        # fix the arbitrary phase of each null vector: largest component real and positive
        for k in range(null.shape[1]):
            col = null[:, k]
            p = np.argmax(np.abs(col))
            null[:, k] = col * (abs(col[p]) / col[p])
        if null.size and np.max(np.abs(null.imag)) > 1e-10:
            raise RuntimeError("vertex singlet is not real after phase fixing; convention error")
        return null.real.reshape(d1, d2, dm, -1)

    def _build_basis(self):
        js = self.link.js
        for jconf in itertools.product(js, repeat=4):
            for Nconf in itertools.product((0, 1, 2), repeat=4):
                locals_ = []
                ok = True
                for v in range(4):
                    ns = self._local_null_space(v, jconf, Nconf[v])
                    if ns.shape[-1] == 0:
                        ok = False
                        break
                    locals_.append(ns)
                if not ok:
                    continue
                mults = [ns.shape[-1] for ns in locals_]
                fock_idx = self.matter.fock_states_with(Nconf)
                for mult_idx in itertools.product(*[range(m) for m in mults]):
                    # tensor with axes: (la_L, la_R, l1_L, l1_R, l2_L, l2_R, l3_L, l3_R, m0, m1, m2, m3)
                    t0 = locals_[0][..., mult_idx[0]]  # (la_L, l1_L, m0)
                    t1 = locals_[1][..., mult_idx[1]]  # (la_R, l3_L, m1)
                    t2 = locals_[2][..., mult_idx[2]]  # (l3_R, l2_R, m2)
                    t3 = locals_[3][..., mult_idx[3]]  # (l2_L, l1_R, m3)
                    T = np.einsum("abw,cdx,efy,ghz->acbhgfdewxyz", t0, t1, t2, t3)
                    # order: la_L=a, la_R=c, l1_L=b, l1_R=h, l2_L=g, l2_R=f, l3_L=d, l3_R=e, m0..m3
                    dims = [len(m_values(j)) ** 2 for j in jconf]
                    psi = T.reshape(dims[0], dims[1], dims[2], dims[3], -1)
                    # matter: local states per site are ordered (for N=1) as colours ascending; the Fock
                    # indices in fock_idx are ascending integers; map the product order to fock order.
                    psi = self._reorder_matter(psi, Nconf, fock_idx)
                    psi = psi / np.linalg.norm(psi)
                    st = GIBasisState(tuple(jconf), tuple(Nconf), len(self.basis), fock_idx, psi.astype(complex))
                    st.index = len(self.basis)
                    self.by_label[(st.jconf, st.Nconf, mult_idx)] = st.index
                    st.extra["mult_idx"] = mult_idx
                    self.basis.append(st)

    def _reorder_matter(self, psi: np.ndarray, Nconf, fock_idx: list[int]) -> np.ndarray:
        """Map the product-order matter axis (site0 state, site1 state, ...) to the ascending Fock order."""
        site_states = []
        for v in range(4):
            if Nconf[v] == 0:
                site_states.append([0])
            elif Nconf[v] == 2:
                site_states.append([3])
            else:
                site_states.append([1, 2])  # bit0 (m=-1/2) occupied -> 1 ; bit1 (m=+1/2) -> 2
        prod_fock = []
        for combo in itertools.product(*site_states):
            f = 0
            for v, s in enumerate(combo):
                f |= s << (2 * v)
            prod_fock.append(f)
        perm = [prod_fock.index(f) for f in fock_idx]
        return psi[..., perm]

    # -- labels and sectors -----------------------------------------------------
    def labels(self):
        return [(b.jconf, b.Nconf) for b in self.basis]

    def N_total(self) -> np.ndarray:
        return np.array([sum(b.Nconf) for b in self.basis])

    def sector(self, N: int) -> np.ndarray:
        return np.where(self.N_total() == N)[0]

    def find(self, jconf, Nconf, mult_idx=None) -> int:
        jconf = tuple(float(j) for j in jconf)
        Nconf = tuple(int(n) for n in Nconf)
        hits = [b.index for b in self.basis if b.jconf == jconf and b.Nconf == Nconf]
        if mult_idx is not None:
            hits = [i for i in hits if self.basis[i].extra["mult_idx"] == tuple(mult_idx)]
        if len(hits) != 1:
            raise KeyError(f"state {(jconf, Nconf)} has {len(hits)} matches")
        return hits[0]

    def excited_links(self) -> np.ndarray:
        return np.array([sum(1 for j in b.jconf if j > 0) for b in self.basis])

    # -- diagonal operators ----------------------------------------------------
    def casimir_diag(self, link: int) -> np.ndarray:
        return np.array([b.jconf[link] * (b.jconf[link] + 1) for b in self.basis])

    def density_diag(self, v: int) -> np.ndarray:
        return np.array([float(b.Nconf[v]) for b in self.basis])

    def electric_diag(self) -> np.ndarray:
        return sum(self.casimir_diag(l) for l in range(4))

    def mass_diag(self) -> np.ndarray:
        return sum(C.MASS_SIGN[v] * self.density_diag(v) for v in range(4))

    # -- term application (route A) ---------------------------------------------
    def _apply_term(self, st: GIBasisState, link_ops: dict[int, np.ndarray], B: sp.spmatrix | None):
        """Apply a product term (link operators on some links) x (matter operator B) to st.psi.
        Returns (tensor, link_full) where tensor has the full local dim D on touched link axes,
        the matter axis is 256 if B is given (else the block dim), and link_full marks touched links."""
        t = st.psi
        if B is not None:
            Bsub = B[:, st.fock_idx].toarray() if sp.issparse(B) else B[:, st.fock_idx]
            t = np.tensordot(t, Bsub.T, axes=([4], [0]))  # (..., 256)
        for l, A in link_ops.items():
            j = st.jconf[l]
            Asub = A[:, self.link.offset[j]:self.link.offset[j] + self.link.block_dim[j]]  # (D, dim_j)
            t = np.moveaxis(np.tensordot(Asub, t, axes=([1], [l])), 0, l)
        return t

    def _overlap(self, target: GIBasisState, t: np.ndarray, touched: set[int], matter_full: bool) -> complex:
        sl = []
        for l in range(4):
            if l in touched:
                j = target.jconf[l]
                o = self.link.offset[j]
                sl.append(slice(o, o + self.link.block_dim[j]))
            else:
                sl.append(slice(None))
        tt = t[tuple(sl)]
        if matter_full:
            tt = tt[..., target.fock_idx]
        return complex(np.vdot(target.psi, tt))

    def _hopping_terms(self):
        """List of (link_ops, B, coefficient-factor) for sum_l eta_l (psi^dag_tail U_l psi_head + h.c.)."""
        terms = []
        for l, (tail, head) in enumerate(C.LINK_ENDS):
            eta = C.LINK_ETA[l]
            for al in self.matter.colours:
                for be in self.matter.colours:
                    U = self.link.U(al, be)
                    B = (self.matter.cdag(tail, al) @ self.matter.c(head, be)).tocsr()
                    terms.append(({l: U}, B, eta))
                    # Hermitian conjugate: (c^dag_tail,al U^{al be} c_head,be)^dag = c^dag_head,be U^{al be}^dag c_tail,al
                    Bh = (self.matter.cdag(head, be) @ self.matter.c(tail, al)).tocsr()
                    terms.append(({l: U.T.conj()}, Bh, eta))
        return terms

    def _plaquette_terms(self):
        """Tr(U_sq) + h.c. with U_sq = U_a U_3 U_2^dag U_1^dag (loop v0->v1->v2->v3->v0)."""
        terms = []
        cols = self.matter.colours
        for al, be, ga, de in itertools.product(cols, repeat=4):
            ops = {0: self.link.U(al, be), 3: self.link.U(be, ga),
                   2: self.link.U(de, ga).T.conj(), 1: self.link.U(al, de).T.conj()}
            terms.append((ops, None, 1.0))
            opsh = {l: A.T.conj() for l, A in ops.items()}
            terms.append((opsh, None, 1.0))
        return terms

    def _term_matrix(self, terms) -> np.ndarray:
        M = np.zeros((self.dim, self.dim), dtype=complex)
        by_label: dict[tuple, list[int]] = {}
        for b in self.basis:
            by_label.setdefault((b.jconf, b.Nconf), []).append(b.index)
        for link_ops, B, coef in terms:
            touched = set(link_ops)
            for st in self.basis:
                t = self._apply_term(st, link_ops, B)
                # candidate targets: any label whose untouched links agree
                for (jc, Nc), idxs in by_label.items():
                    if any(jc[l] != st.jconf[l] for l in range(4) if l not in touched):
                        continue
                    if B is None and Nc != st.Nconf:
                        continue
                    for i in idxs:
                        val = self._overlap(self.basis[i], t, touched, B is not None)
                        if abs(val) > 1e-14:
                            M[i, st.index] += coef * val
        return M

    def hopping_matrix(self) -> np.ndarray:
        if "hop" not in self._H_terms_cache:
            self._H_terms_cache["hop"] = self._term_matrix(self._hopping_terms())
        return self._H_terms_cache["hop"]

    def plaquette_matrix(self) -> np.ndarray:
        if "plaq" not in self._H_terms_cache:
            self._H_terms_cache["plaq"] = self._term_matrix(self._plaquette_terms())
        return self._H_terms_cache["plaq"]

    def hamiltonian(self, coup: C.Couplings) -> np.ndarray:
        """Real symmetric Hamiltonian in the GI configuration basis, units of g_E."""
        H = (coup.cE * np.diag(self.electric_diag()) + coup.cM * np.diag(self.mass_diag())
             + coup.cH * self.hopping_matrix() + coup.cB * self.plaquette_matrix())
        if np.max(np.abs(H.imag)) > 1e-12:
            raise RuntimeError("Hamiltonian acquired an imaginary part; convention error")
        H = H.real
        if np.max(np.abs(H - H.T)) > 1e-10:
            raise RuntimeError("Hamiltonian is not symmetric; convention error")
        return 0.5 * (H + H.T)

    # -- route A basis as full-space sparse vectors (for route-B cross-checks) ----
    def full_space_vectors(self) -> sp.csc_matrix:
        D = self.link.dim
        rows, cols, vals = [], [], []
        for st in self.basis:
            dims = st.psi.shape
            offs = [self.link.offset[j] for j in st.jconf]
            it = np.ndindex(dims[0], dims[1], dims[2], dims[3])
            flat = st.psi.reshape(-1, dims[4])
            for n, (i0, i1, i2, i3) in enumerate(it):
                row_base = (((offs[0] + i0) * D + (offs[1] + i1)) * D + (offs[2] + i2)) * D + (offs[3] + i3)
                for mi, f in enumerate(st.fock_idx):
                    v = flat[n, mi]
                    if abs(v) > 1e-15:
                        rows.append(row_base * MatterSpace.DIM + f)
                        cols.append(st.index)
                        vals.append(v)
        return sp.csc_matrix((vals, (rows, cols)), shape=(D**4 * MatterSpace.DIM, self.dim))


# ----------------------------------------------------------------------------
# Route B: everything on the full gauge-redundant space (sparse)
# ----------------------------------------------------------------------------
class FullSpaceOperators:
    """Sparse operators on link^4 (x) matter for the commutator and projection checks."""

    def __init__(self, jmax: float = 0.5):
        self.link = LinkSpace(jmax)
        self.matter = MatterSpace()
        self.D = self.link.dim
        self.dim = self.D**4 * MatterSpace.DIM

    def _kron(self, link_ops: dict[int, np.ndarray], B: sp.spmatrix | None) -> sp.csr_matrix:
        mats = []
        for l in range(4):
            A = link_ops.get(l)
            mats.append(sp.identity(self.D, format="csr") if A is None else sp.csr_matrix(A))
        Bm = sp.identity(MatterSpace.DIM, format="csr") if B is None else sp.csr_matrix(B)
        out = mats[0]
        for m in mats[1:]:
            out = sp.kron(out, m, format="csr")
        return sp.kron(out, Bm, format="csr")

    def electric(self) -> sp.csr_matrix:
        H = sp.csr_matrix((self.dim, self.dim))
        for l in range(4):
            H = H + self._kron({l: np.diag(self.link.casimir())}, None)
        return H

    def mass(self) -> sp.csr_matrix:
        B = sp.csr_matrix((MatterSpace.DIM, MatterSpace.DIM))
        for v in range(4):
            B = B + C.MASS_SIGN[v] * self.matter.N_site[v]
        return self._kron({}, B)

    def hopping(self) -> sp.csr_matrix:
        H = sp.csr_matrix((self.dim, self.dim), dtype=complex)
        for l, (tail, head) in enumerate(C.LINK_ENDS):
            for al in self.matter.colours:
                for be in self.matter.colours:
                    U = self.link.U(al, be)
                    B = self.matter.cdag(tail, al) @ self.matter.c(head, be)
                    T = self._kron({l: U}, B)
                    H = H + C.LINK_ETA[l] * (T + T.conj().T)
        return H.tocsr()

    def plaquette(self) -> sp.csr_matrix:
        H = sp.csr_matrix((self.dim, self.dim), dtype=complex)
        cols = self.matter.colours
        for al, be, ga, de in itertools.product(cols, repeat=4):
            ops = {0: self.link.U(al, be), 3: self.link.U(be, ga),
                   2: self.link.U(de, ga).T.conj(), 1: self.link.U(al, de).T.conj()}
            T = self._kron(ops, None)
            H = H + T + T.conj().T
        return H.tocsr()

    def hamiltonian(self, coup: C.Couplings) -> sp.csr_matrix:
        return (coup.cE * self.electric() + coup.cM * self.mass()
                + coup.cH * self.hopping() + coup.cB * self.plaquette()).tocsr()

    def gauss(self, v: int, a: int) -> sp.csr_matrix:
        """G^a_v = sum_{links out of v} E^a_L + sum_{links into v} E^a_R + Q^a_v."""
        G = sp.csr_matrix((self.dim, self.dim), dtype=complex)
        for l, (tail, head) in enumerate(C.LINK_ENDS):
            if tail == v:
                G = G + self._kron({l: self.link.E(a, "L")}, None)
            if head == v:
                G = G + self._kron({l: self.link.E(a, "R")}, None)
        G = G + self._kron({}, self.matter.charge(v, a))
        return G.tocsr()

    def gauss_casimir_sum(self) -> sp.csr_matrix:
        Csum = sp.csr_matrix((self.dim, self.dim), dtype=complex)
        for v in range(4):
            for a in range(3):
                G = self.gauss(v, a)
                Csum = Csum + G @ G
        return Csum.tocsr()
