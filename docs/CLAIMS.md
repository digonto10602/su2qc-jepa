# Claims ledger — every substantive statement, its status and its evidence

Status vocabulary: MEASURED / PROVEN / PROPOSED / UNVERIFIED / VOID / EMULATED.

| # | Claim | Status | Evidence |
|---|---|---|---|
| C1 | 82 gauge-invariant states, sectors 2/20/38/20/2, degeneracies 16/16/18/16/16; 152 at $j_{\max}=1$ | PROVEN (tests) | `tests/test_physics.py`, `evidence/J0_data/` |
| C2 | Routes A and B agree to 4e-16; Gauss law exact | PROVEN (tests) | `tests/test_physics.py::test_two_routes_agree_and_gauss_law` |
| C3 | $g_E=1$ dynamics table of the physics notes reproduced | MEASURED | `tests/test_physics.py::test_dynamics_reproduce_preliminary_expectation` |
| C4 | $K=12$ Krylov chain reproduces the P-A window to 1.1e-4 | MEASURED | J0 row D4 |
| C5 | KC-Trotter costs 34/56/100/188 CZ for $r=1,2,4,8$ at $K=12$; circuits equal the sector unitary | PROVEN (tests) | `tests/test_physics.py::test_chain_circuit_matches_sector_unitary` |
| C6 | Mass dependence weak on-family, sharp at strong coupling | MEASURED | PLAN App. B.3 (to be re-emitted as `evidence/J0_data/mass_dependence.json` in M1) |
| C7 | JEPA v1 meets H1 | UNVERIFIED | J1 |
| C8 | JEPA forecasting meets H2 | UNVERIFIED | J2 |
| C9 | Label-free residual meets H3 | UNVERIFIED | J3 |
| C10 | Depth extrapolation on hardware (H4) | UNVERIFIED | M5 |
| C11 | Resonance on hardware (H5) | UNVERIFIED | M6 |
| C13 | Numbered-artifact conventions hold; the committed code graph is structurally fresh | PROVEN (checks) | `scripts/check_artifacts.py`, `scripts/graph_update.sh --check`, CI |
| C12 | All noisy numbers so far | EMULATED | no hardware job has ever been submitted from this repository |
