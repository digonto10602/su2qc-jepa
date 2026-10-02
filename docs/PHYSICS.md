# Physics summary (derivation-level notes are the SU2QC physics-setup notes of 9 Sept 2026)

This package implements the hard-core SU(2) Kogut–Susskind plaquette with two-colour staggered fermions exactly as the notes define it; `src/su2qc_jepa/physics/conventions.py` is the frozen convention file. Everything below is asserted by `tests/test_physics.py`.

**Hilbert space.** Links $|j,m_L,m_R\rangle$ with $j\in\{0,\tfrac12\}$ (5 states; 14 at $j_{\max}=1$). Matter: two colours per vertex, Fock states $N=0$ (singlet), $N=1$ (doublet), $N=2$ (singlet "baryon"). Gauss's law at a vertex = the two adjacent link spins and the matter representation couple to a singlet; intertwiner multiplicity 1 for the plaquette. Counting by domain walls gives $82 = 32 + 48 + 2$; the generating function $2 + 20x^2 + 38x^4 + 20x^6 + 2x^8$ gives the $N$ sectors.

**Operators.** $\langle J M_L M_R|U^{\alpha\beta}|j m_L m_R\rangle = \sqrt{(2j+1)/(2J+1)}\,\langle j m_L;\tfrac12\alpha|J M_L\rangle\langle j m_R;\tfrac12\beta|J M_R\rangle$; left generator $-(S^a)^{\mathsf T}$ on $m_L$, right generator $+S^a$ on $m_R$; $Q^a_v=\psi_v^\dagger(\sigma^a/2)\psi_v$; Jordan–Wigner order $(v_0^-,v_0^+,\dots,v_3^+)$ with colour $=m\in\{-\tfrac12,+\tfrac12\}$.

**Hamiltonian (units of $g_E$).** $H=c_E\sum_\ell j_\ell(j_\ell+1)+c_M\sum_n(-1)^{n_x+n_y}N_n+c_H\sum_\ell(\eta_\ell\psi^\dagger_{\text{tail}}U_\ell\psi_{\text{head}}+\text{h.c.})+c_B\,\mathrm{Tr}(U_\square+U_\square^\dagger)$, $U_\square=U_aU_3U_2^\dagger U_1^\dagger$, $\eta=(+1,+1,+1,-1)$ on $(l_a,l_1,l_2,l_3)$.

**Named states** (links at $j=\tfrac12$; $N(v_0..v_3)$): S3 $(l_1,l_2,l_3)$, $(1,1,0,2)$; S1 $(l_a)$, $(1,1,0,2)$; MM $(l_1,l_3)$ or $(l_a,l_2)$, $(1,1,1,1)$; $B\bar B$ none, one even $N=2$ and one odd $N=0$; Loop all four, $(0,2,0,2)$; $\Omega_0$ none, $(0,2,0,2)$. Bare energies $2\mu+9/4$, $2\mu+3/4$, $4\mu+3/2$, $4\mu$, $3$, $0$ — degenerate pairs at $\mu^*=3/8$.

**Channels in $N=4$** (matter content only): pair 8, meson 2, baryonic 26, vacuum-matter 2; sub-projectors S3, S1, hopped (6), $B\bar B$ (4), antivac (1).

**Routes.** Route A: vertex singlets → block tensors → matrix elements by term application (any $j_{\max}$). Route B: full link$^4\otimes$matter space, sparse kron, Gauss generators, projection. Agreement 4e-16; $[G,H]=0$ exactly.

**Krylov chain.** Lanczos from S3 in the 38-state sector; $K=12$ reproduces $t\le3/g_E$ at P-A to 1.1e-4; $\beta_{27}\sim10^{-6}$ (effective dimension 27). One-hot encoding → XY chain; Strang circuits; KC-prep cascade.
