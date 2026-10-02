"""Frozen conventions for the hard-core SU(2) Kogut-Susskind plaquette with
two-colour staggered fermions.  These follow the SU2QC physics-setup notes
(9 Sept 2026) so that every number produced here can be compared with the
project's verified `su2qc` code.  Do not edit without a new ADR in docs/.

Geometry (one square plaquette, open boundaries):

    v3=(0,1) ---l2---> v2=(1,1)
       ^                 ^
       |l1               |l3
       |                 |
    v0=(0,0) ---la---> v1=(1,0)

Links are stored in the order (la, l1, l2, l3) = indices (0, 1, 2, 3).
Loop orientation for the plaquette: U_sq = U_a U_3 U_2^dag U_1^dag.
Staggered phases: eta_x = 1, eta_y(n) = (-1)^{n_x}; product around the loop = -1.
Jordan-Wigner mode order: (v0-, v0+, v1-, v1+, v2-, v2+, v3-, v3+) where the
colour index is the magnetic number m in {-1/2, +1/2} of the fundamental.
"""
from __future__ import annotations

from dataclasses import dataclass

VERTICES = ((0, 0), (1, 0), (1, 1), (0, 1))  # v0, v1, v2, v3
LINK_NAMES = ("la", "l1", "l2", "l3")
# link -> (tail vertex, head vertex)
LINK_ENDS = ((0, 1), (0, 3), (3, 2), (1, 2))
# staggered phase eta_l per link: x-links +1, y-links (-1)^{n_x of the tail}
LINK_ETA = (1.0, 1.0, 1.0, -1.0)  # la: x from (0,0); l1: y from (0,0); l2: x from (0,1); l3: y from (1,0)
# staggered mass sign (-1)^{n_x+n_y} per vertex
MASS_SIGN = (1.0, -1.0, 1.0, -1.0)
EVEN_VERTICES = (0, 2)
ODD_VERTICES = (1, 3)
# vacuum occupation per vertex (even: 0, odd: 2)
VACUUM_N = (0, 2, 0, 2)
# plaquette loop as a sequence of (link, forward?) steps starting at v0
PLAQUETTE_LOOP = ((0, True), (3, True), (2, False), (1, False))
STRING_LINKS = (1, 2, 3)  # the three-link path l1, l2, l3 used by the stretched string S3

# Regression fingerprints (derived in the physics-setup notes, section 4)
EXPECTED_DIM = {0.5: 82, 1.0: 152}
EXPECTED_SECTORS = {0.5: (2, 20, 38, 20, 2), 1.0: (3, 36, 74, 36, 3)}
EXPECTED_ELECTRIC_DEGENERACY_HALF = (16, 16, 18, 16, 16)
EXPECTED_CHANNEL_SPLIT_N4 = {"pair": 8, "meson": 2, "baryonic": 26, "vacmatter": 2}
RESONANCE_MU = 3.0 / 8.0


@dataclass(frozen=True)
class Couplings:
    """Four-coefficient Hamiltonian in units of g_E (electric quantum).

    H/g_E = cE * sum_l j_l(j_l+1) + cM * sum_n (-1)^{n_x+n_y} N_n
          + cH * sum_l (eta_l psi^dag U psi + h.c.) + cB * Tr(U_sq + U_sq^dag)
    On-family values: (cE, cM, cH, cB) = (1, mu, 1/(2 g_E), -1/(4 g_E^2)).
    """

    cE: float = 1.0
    cM: float = 0.375
    cH: float = 0.25
    cB: float = -0.0625
    name: str = "custom"

    @classmethod
    def on_family(cls, gE: float, mu: float, name: str = "") -> Couplings:
        return cls(cE=1.0, cM=mu, cH=1.0 / (2.0 * gE), cB=-1.0 / (4.0 * gE**2), name=name or f"gE={gE},mu={mu}")

    def as_tuple(self) -> tuple[float, float, float, float]:
        return (self.cE, self.cM, self.cH, self.cB)


# Coupling points used by the project (physics-setup notes, section 8.2).
# P-A: the v0.5.0 window g^2 = 4, m = 0.75  ->  g_E = 2, mu = 3/8  (ratio 1 : 0.25 : 0.0625)
POINT_PA = Couplings.on_family(gE=2.0, mu=RESONANCE_MU, name="P-A")
# P-S: the Sufian benchmark w = g_B = 1, g_E = 50, m = 18.75  ->  (1, 3/8, 0.02, -0.02 * sign)
# NOTE: the sign of cB follows our magnetic-term convention (negative); the magnitude is 0.02.
POINT_PS = Couplings(cE=1.0, cM=RESONANCE_MU, cH=0.02, cB=-0.02, name="P-S")
# A weak-coupling-side point used for the coupling scan (g_E = 1 on-family)
POINT_G1 = Couplings.on_family(gE=1.0, mu=RESONANCE_MU, name="gE=1")

POINTS = {"P-A": POINT_PA, "P-S": POINT_PS, "gE=1": POINT_G1}
