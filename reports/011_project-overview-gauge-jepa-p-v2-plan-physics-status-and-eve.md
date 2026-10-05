---
id: reports/011
title: 'Project overview: Gauge-JEPA-P v2 plan, physics, status and every number to date (5 Oct 2026)'
series: reports
created_utc: '2026-10-05T21:38:49Z'
author: claude-code
milestone: M2
status: done
supersedes: null
superseded_by: null
---

# Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)

**Repository:** https://github.com/digonto10602/su2qc-jepa (public) · **Researcher:** Digonto · **Written:** 2026-10-05, 21:40 UTC, at commit `12ad4df` plus fetched Perlmutter results · **Active plan:** `plans/001` · **Prompt in force:** `prompts/002` (M2), follow-up `prompts/010`

---

## 0. How to read this document

This document is self-contained. It summarises the project's plan, the physics, the methods, the infrastructure, every session so far and every number measured so far. It is meant to be read by a person, or by another AI assistant asked to explain the project.

Conventions used throughout:
- **Status words** (the project uses only these): PASS, FAIL, PARTIAL, NOT RUN, VOID for gates; MEASURED, PROVEN (by tests), PROPOSED, UNVERIFIED, EMULATED for claims. **EMULATED** means "from simulation of a noisy device, not from a real device". **No job has ever been run on real quantum hardware in this project; every noisy number is EMULATED.**
- **Units:** energies in units of $g_E$ (the electric energy quantum, defined in §3); times in units of $1/g_E$; couplings as the four-tuple $(c_E, c_M, c_H, c_B)$.
- **(label)** marks a name the project invented. It is not a standard physics or machine-learning term.
- **Preliminary** marks a number read directly from training files and not yet passed through the project's official gate script. Only gate scripts decide PASS/FAIL.
- File paths are relative to the repository root.

---

## 1. The project in one paragraph

The project trains a **JEPA world model** on a small, exactly solvable lattice gauge theory: the SU(2) gauge field with matter on a single square plaquette (4 sites, 4 links). JEPA (Joint-Embedding Predictive Architecture) is a machine-learning design in which an encoder compresses an observation into a short vector (the *latent*) and a predictor learns how that latent changes over time. The physics studied is **string breaking**: a flux string between static colour charges breaks by creating matter–antimatter pairs.

The model reads finite-shot measurement records, the kind a quantum computer produces. It is trained to predict how the system evolves under given actions (time steps at given couplings, sudden mass changes). The goal is **not quantum advantage**: everything here can be solved exactly on a laptop. The goals are:
1. a learned forecaster of late-time behaviour, compared fairly with simple baselines;
2. a *label-free error signal* for quantum hardware, i.e. a way to tell how wrong a hardware result is without knowing the true answer, validated here where the truth *is* known;
3. a hardware dataset taken on IBM quantum computers with a compact 12-qubit circuit design, the "Krylov-chain carrier" *(label)*, that has a controllable circuit depth and a built-in error flag.

The plan runs eight weeks, 5 Oct – 29 Nov 2026. The end product is a methods-and-benchmark paper.

---

## 2. Glossary (every technical term used below)

| term | meaning |
|---|---|
| SU(2) lattice gauge theory | a model of a force field (like a simplified version of the strong force) placed on a grid. "SU(2)" is the symmetry group: two "colours" instead of the three of real QCD |
| plaquette | the smallest closed square of a lattice: 4 sites (vertices) and 4 links |
| Kogut–Susskind Hamiltonian | the standard way to write the energy operator of a lattice gauge theory with continuous time |
| link, $j_\ell$ | the gauge field lives on links; $j_\ell\in\{0,\tfrac12\}$ is the "electric flux" on link $\ell$ (truncated at $j_{\max}=\tfrac12$) |
| staggered fermions | a way to put matter particles on a lattice; even and odd sites carry particles and antiparticles |
| Gauss's law, gauge invariance | a constraint linking the flux at each site to the matter charge there; only states satisfying it are physical ("gauge-invariant") |
| string, string breaking | a line of flux between charges; it "breaks" when the energy stored in it is used to create a matter pair that screens the charges |
| sector $N$ | the subspace with total matter number $N$; the dynamics studied live in the $N=4$ sector (38 states) |
| S3, S1, MM, $B\bar B$, Loop, $\Omega_0$ | named basis states (§3): S3 = the stretched string over three links, S1 = short string on one link, MM = two mesons, $B\bar B$ = baryon–antibaryon, Loop = closed flux loop, $\Omega_0$ = bare vacuum |
| $\mu^*=3/8$ resonance | the mass at which the stretched-string energy equals the energies of broken configurations, so the string breaks fastest |
| Lanczos / Krylov | an algorithm that builds, from a start state, a small orthonormal basis (the Krylov basis) in which the Hamiltonian is tridiagonal (nonzero only on the diagonal and next to it) with coefficients $\alpha_k$ (diagonal) and $\beta_k$ (off-diagonal) |
| Trotter / Strang splitting | approximating $e^{-iHt}$ by a product of simpler exponentials; Strang is the symmetric second-order version |
| CZ gate | the two-qubit entangling gate on IBM hardware; CZ count is the main measure of circuit cost and noise |
| shots | the number of times a quantum circuit is run and measured; estimates have statistical error $\propto 1/\sqrt{\text{shots}}$ |
| twin (digital twin) | a classical noisy simulation of the device (Qiskit Aer density-matrix simulator with a noise model), used to rehearse and compare |
| JEPA | Joint-Embedding Predictive Architecture: predict the *representation* of the future observation, not the raw observation |
| encoder, latent, predictor | encoder: network mapping an observation to a latent vector; predictor: network advancing the latent under actions |
| collapse | a failure where the encoder maps everything to (nearly) the same latent, which makes prediction trivially easy and useless |
| SIGReg | "Sketched Isotropic Gaussian Regularizer" from LeJEPA (arXiv:2511.08544): a loss pushing the latent distribution toward a standard Gaussian, preventing collapse |
| EMA target encoder | an alternative anti-collapse device (I-JEPA style): the target latent comes from a slowly updated copy of the encoder ("exponential moving average") with no gradient through it ("stop-gradient") |
| grounding heads | small linear maps from the latent to known physical quantities (energy, $C_{\text{string}}$, $P_{\text{meson}}$, $P_{\text{baryonic}}$, flag rate), trained alongside, so that the latent stays physically meaningful |
| semigroup consistency | the requirement that predicting two steps at once equals predicting one step twice, as true time evolution does |
| effective rank | $\exp$ of the entropy of the normalised singular values of the latent batch: roughly "how many latent directions are really used" (max 16 for a 16-dimensional latent) |
| $R^2$ | coefficient of determination, $1-\sum(y-\hat y)^2/\sum(y-\bar y)^2$; 1 = perfect prediction |
| ridge regression | linear regression with a small penalty on coefficient size |
| MAE | mean absolute error |
| Spearman correlation | rank correlation (does the signal order points the same way as the true error?) |
| AUROC | area under the receiver-operating curve: how well a score separates two groups (1 = perfect, 0.5 = chance) |
| gate | a scripted pass/fail check with preregistered thresholds; gate scripts are the only arbiters |
| preregistration | fixing hypotheses, thresholds and analysis commands *before* seeing the final data, signed by a git tag |
| Perlmutter | the NERSC supercomputer (A100 GPUs) used for heavy jobs |
| Slurm | the job scheduler on Perlmutter |
| node-hour | accounting unit: one full node for one hour; one A100 on the shared queue = ¼ node-hour per hour |
| Graphify | a tool that builds a navigable graph of the codebase (files, functions, calls); used for navigation only, never as evidence of correctness |

---

## 3. The physics object (frozen)

### 3.1 Model
Hard-core SU(2) Kogut–Susskind plaquette:
- link flux $j_\ell\in\{0,\tfrac12\}$ on four links $(l_a,l_1,l_2,l_3)$;
- two-colour staggered fermions on four vertices;
- open boundaries.

In units of $g_E=g^2/2a$:

$$\frac{H}{g_E}=c_E\sum_\ell j_\ell(j_\ell+1)+c_M\sum_n(-1)^{n_x+n_y}N_n+c_H\sum_\ell\big(\eta_\ell\,\psi_{\text{tail}}^\dagger U_\ell\,\psi_{\text{head}}+\text{h.c.}\big)+c_B\,\mathrm{Tr}\big(U_\square+U_\square^\dagger\big),$$

with:
- plaquette loop $U_\square=U_aU_3U_2^\dagger U_1^\dagger$;
- staggered phases $\eta=(+1,+1,+1,-1)$ on $(l_a,l_1,l_2,l_3)$, so $\prod_\square\eta=-1$;
- Jordan–Wigner ordering $(v_0^-,v_0^+,\dots,v_3^+)$ (the rule that maps fermions onto qubits).

The four terms are the electric energy $\mathcal{E}$, the mass term $\mathcal{M}$, the hopping (kinetic) term $\mathcal{T}$ and the magnetic/plaquette term $\mathcal{B}$. On-family couplings are $c_E=1$, $c_M=\mu=m/g_E$, $c_H=1/(2g_E)$, $c_B=-1/(4g_E^2)$. All conventions are frozen in `src/su2qc_jepa/physics/conventions.py` (`decisions/000`).

### 3.2 Coupling points
- **P-A** ($g_E=2$, $\mu=3/8$): $(c_E,c_M,c_H,c_B)=(1,\,0.375,\,0.25,\,-0.0625)$. This is the hardware window.
- **P-S** (strong coupling): $(1,\,0.375,\,0.02,\,-0.02)$, the regime of an earlier study by Sufian.
- **On-family scan:** $g_E\in\{1.0,1.15,1.3,1.45,1.6,1.75,2.0\}$.

### 3.3 Verified fingerprints (all MEASURED or PROVEN by tests)
- **82 gauge-invariant states**, split by matter number $N=0,2,4,6,8$ as 2/20/38/20/2. Electric degeneracies 16/16/18/16/16. At $j_{\max}=1$: 152 states, 3/36/74/36/3.
- **Two routes agree.** Route A builds vertex singlets and block tensors; route B uses the full 160,000-dimensional space with explicit Gauss-law projection. They agree to $4\times10^{-16}$. The Gauss-law commutator $\|[G^a_n,H]\|=0$ exactly, and $H$ keeps the physical subspace invariant to $2\times10^{-16}$.
- **Named states and bare energies** relative to $\Omega_0$:

  | state | content | bare energy |
  |---|---|---|
  | S3 | flux on $(l_1,l_2,l_3)$ | $2\mu+9/4$ |
  | S1 | flux on $l_a$ | $2\mu+3/4$ |
  | MM | two mesons | $4\mu+3/2$ |
  | $B\bar B$ | baryon–antibaryon | $4\mu$ |
  | Loop | flux on all four links | $3$ |
  | $\Omega_0$ | bare vacuum | $0$ |

  The degeneracies relevant to string breaking coincide at $\mu^*=3/8$.
- **Hamiltonian structure.** Hopping: 4 links × 36 disjoint real 2×2 blocks (288 nonzeros). Plaquette: 41 disjoint pairs (82 nonzeros).
- **Channels in the $N=4$ sector** (matter content only): pair 8, meson 2, baryonic 26, vacuum-matter 2. Sub-projectors: S3, S1, hopped (6), $B\bar B$ (4), antivac (1).
- **Dynamics from S3** at $g_E=1$, $\mu=3/8$: $P_{\text{baryonic}}(t=1,2,3)=0.432,\,0.732,\,0.821$; $P_{\text{meson}}<0.04$; $P_{S1}<0.02$; $C_{\text{string}}(3)=0.238$. This reproduces the project's earlier physics notes to three digits.
- **Dynamics from S3 at P-A**, at the hardware times $t=0.375/0.75/1.5/3.0$:
  - $P_{S3}=0.969/0.884/0.622/0.183$;
  - $P_{\text{meson}}=0.004/0.014/0.034/0.046$;
  - $P_{\text{baryonic}}=0.022/0.082/0.270/0.579$;
  - $C_{\text{string}}=0.744/0.727/0.662/0.448$.
- **Mass dependence** (why the data use two coupling families):
  - On-family ($g_E=2$): the breaking fraction at $t=3$ falls only from 0.628 to 0.531 over $\mu=0.15\to0.65$. There is no resonance peak.
  - Strong coupling ($c_H=0.02$): breaking fraction at $t=16.7/33.3/50$:

    | $\mu$ | $t=16.7$ | $t=33.3$ | $t=50$ |
    |---|---|---|---|
    | 0.375 | 0.227 | 0.555 | 0.740 |
    | 0.30 | 0.143 | 0.071 | 0.056 |
    | 0.45 | 0.141 | 0.067 | 0.060 |
    | 0.15 | 0.007 | 0.016 | 0.016 |

    The resonance at $\mu^*=3/8$ is sharp here.
- **Truncation error** ($j_{\max}=1$ vs $\tfrac12$, P-A window): $|\Delta P_{S3}|\le0.053$, $|\Delta P_{\text{meson}}|\le0.060$, $|\Delta P_{\text{baryonic}}|\le0.014$, $|\Delta C_{\text{string}}|\le0.034$. This is an error-budget line, not something the hardware can resolve.
- **Effective Krylov dimension** from S3 at P-A: $\beta_{27}\approx10^{-6}$, i.e. about 27–28 of the 38 sector states are reached.

### 3.4 Cross-check against the project's independent verified code (M1, `evidence/J0_data/crosscheck_su2qc.json`, PASS)
This package's physics core ("route C") was compared with the earlier verified `su2qc` code (routes 1 and 2) at P-A and P-S, against a tolerance of $10^{-10}$. Maximum absolute deviations:

| quantity | P-A route 1 | P-A route 2 | P-S route 1 | P-S route 2 |
|---|---|---|---|---|
| 82 diagonal energies | 0 | $4.4\times10^{-16}$ | 0 | $4.4\times10^{-16}$ |
| full spectrum | $6.2\times10^{-15}$ | $6.2\times10^{-15}$ | $8.2\times10^{-15}$ | $5.3\times10^{-15}$ |
| $N=4$ block (after a sign gauge) | $5.6\times10^{-17}$ | $4.4\times10^{-16}$ | $1.2\times10^{-16}$ | $4.4\times10^{-16}$ |
| full $82\times82$ matrix (after a sign gauge) | $5.6\times10^{-17}$ | $4.4\times10^{-16}$ | $1.2\times10^{-16}$ | $4.4\times10^{-16}$ |
| sector populations from S3, 12 times | $1.1\times10^{-15}$ | $2.7\times10^{-15}$ | $3.9\times10^{-14}$ | $2.7\times10^{-14}$ |
| observables from S3 | $2.1\times10^{-15}$ | $3.0\times10^{-15}$ | $7.3\times10^{-14}$ | $5.9\times10^{-14}$ |
| Lanczos $\alpha_k$, $k<12$ | $1.3\times10^{-15}$ | $1.3\times10^{-15}$ | $5.8\times10^{-15}$ | $2.7\times10^{-15}$ |
| Lanczos $\beta_k$, $k<12$ | $6.7\times10^{-16}$ | $1.1\times10^{-15}$ | $1.7\times10^{-15}$ | $6.9\times10^{-15}$ |

The largest deviation is $7.3\times10^{-14}$, so the two codes describe the same Hamiltonian, including at the off-family point P-S. The "sign gauge" is needed because the two codes choose opposite phases for 8 (route 1) or 24 (route 2) basis states. A diagonal $\pm1$ matrix is fixed on a spanning tree of the coupling graph, and every remaining matrix entry, including every closed loop, is then checked.

**Hand check:** $\alpha_0=\langle S3|H|S3\rangle=3\cdot\tfrac34+\mu(1-1+0-2)=1.5$ at $\mu=3/8$. The computed value is 1.5.

Lanczos coefficients at P-A:
- $\alpha_{0..11}=(1.5,1.684,1.492,0.399,0.434,1.144,2.394,2.452,1.876,1.889,0.946,0.828)$;
- $\beta_{0..11}=(0.472,0.846,1.341,1.502,1.439,1.482,1.534,1.141,0.408,1.156,0.546,1.117)$.

---

## 4. The Krylov-chain hardware carrier (KC) *(label)*

**Construction.**
1. Run Lanczos from $|S3\rangle$ under $H$ restricted to the 38-state $N=4$ sector. This gives orthonormal vectors $|k\rangle$ and a tridiagonal $H_K=\sum_k\alpha_k|k\rangle\langle k|+\sum_k\beta_k(|k\rangle\langle k{+}1|+\text{h.c.})$.
2. Encode $|k\rangle$ "one-hot" on $K=12$ qubits in a line: qubit $k$ is in $|1\rangle$, all others in $|0\rangle$.
3. Then $|k\rangle\langle k|\to n_k=(1-Z_k)/2$ and $|k\rangle\langle k{+}1|+\text{h.c.}\to(X_kX_{k+1}+Y_kY_{k+1})/2$. So the gauge-theory evolution becomes a nearest-neighbour **XY spin chain** with site fields.

**Two circuit arms on the same qubits:**
- **KC-Trotter** *(label)*: $e^{-iH_Kt}$ by Strang splitting (order: fields/2, even bonds/2, odd bonds, even bonds/2, fields/2). Each bond is one `XXPlusYY` gate = 2 CZ. It costs $2(K-1)=22$ CZ per step and has a genuine **depth ladder**.
- **KC-prep** *(label)*: prepares the exact time-$t$ state directly with $K-1=11$ rotations (22 CZ, fixed). It has no depth ladder and serves as the control arm.

**Excitation flag.** Both arms conserve the number of excited qubits. Any measurement shot with $\neq1$ excited qubit is a *detected error* and is discarded and counted. This is an encoding flag, not a gauge-violation flag.

**Measurement settings.** Z (populations, plus the flag) and X (real coherences $\langle X_kX_{k'}\rangle=2\,\mathrm{Re}\,\rho_{kk'}$). Every physical observable has a real symmetric matrix $O_K=Q_K^{\mathsf T}OQ_K$ in the Krylov basis, so $\langle O\rangle=\sum_{kk'}(O_K)_{kk'}\mathrm{Re}\,\rho_{kk'}$.

**Measured costs at P-A** ($K=12$, $\Delta t=0.375$; synthetic Heron-like noise: CZ error $3\times10^{-3}$, readout 1–2%, $T_1=250\,\mu$s, $T_2=150\,\mu$s):

| steps $r$ | $t$ ($1/g_E$) | CZ | two-qubit depth | Strang infidelity | emulated flag rate | emulated post-selected population error |
|---|---|---|---|---|---|---|
| 1 | 0.375 | 34 | 6 | $2\times10^{-5}$ | 0.23 | 0.006 |
| 2 | 0.75 | 56 | 10 | $8\times10^{-5}$ | 0.28 | 0.011 |
| 4 | 1.5 | 100 | 18 | $3\times10^{-4}$ | 0.38 | 0.020 |
| 8 | 3.0 | 188 | 34 | $1.2\times10^{-3}$ | 0.55 | 0.016 |

- **Krylov truncation:** $K=12$ reproduces observables over $t\le3/g_E$ to $1.1\times10^{-4}$ (J0 row D4 measured $1.05\times10^{-4}$).
- **Circuit correctness:** the circuits equal the in-sector unitary to $10^{-15}$, and KC-prep is exact to $10^{-15}$.
- **Strong coupling:** Trotterising is hopeless there (hundreds of steps), so the hardware arm is KC-prep only, at $t\in\{10,15,20\}/g_E$.
- **Routing:** a dry run against IBM's simulated `FakeTorino` device chose a 12-qubit line with zero routing overhead (CZ counts preserved).
- **What it is not:** the Krylov basis is computed classically, so this is a testbed with known truth and controllable depth. It is not a computation beyond classical reach.

---

## 5. The world model (JEPA)

**Observation vector** (`data/records.py`, dimension 24, frozen):
- 18 physical observables: $\langle N_v\rangle$ (4 vertex occupations), $\langle j_\ell(j_\ell{+}1)\rangle$ (4 link Casimirs), $P_{\text{pair}}$, $P_{\text{meson}}$, $P_{\text{baryonic}}$, $P_{\text{vacmatter}}$, $P_{S3}$, $P_{S1}$, $P_{\text{hopped}}$, $P_{B\bar B}$, $P_{\text{antivac}}$, $C_{\text{string}}$;
- the flag rate;
- a source one-hot (exact / twin / hardware);
- a carrier one-hot (diagonal / chain).

All three sources go through the same estimator. All 18 observables are *diagonal* in the configuration basis: they can be read from computational-basis measurements.

**Actions:** $a_t=(\Delta t,\,c_M,\,c_H,\,c_B)$. A mass quench changes $c_M$ mid-trajectory.

**Training rule:** the context is the *noisy* record ($S\in\{256,512,1024,4096\}$ shots). The target is the latent of the *clean* (exact) record.

**Architecture** (`src/su2qc_jepa/models/jepa.py`):
- encoder: MLP $24\to128\to128\to16$ with LayerNorm and GELU;
- predictor: a GRU over action tokens, initialised from the latent, with a skip connection;
- grounding heads: one linear map to (energy, $C_{\text{string}}$, $P_{\text{meson}}$, $P_{\text{baryonic}}$, flag).

**Parameter count** (counted in code, 5 Oct): **90,309 trainable** (encoder 22,288; predictor 67,936; grounding 85). With latent 32: 97,349. The EMA copy adds 22,288 non-trained parameters. (The plan's "~0.2 M parameters" was an overestimate.)

**Loss** = $w_{\text{pred}}\cdot$ prediction MSE at horizons $k\in\{1,2,4,8\}$ + $w_{\text{sigreg}}\cdot$ SIGReg (Epps–Pulley statistic on 64 random 1-D projections) + $w_{\text{ground}}\cdot$ grounding MSE (context and clean latents) + $w_{\text{semigroup}}\cdot$ semigroup consistency. Defaults: $w_{\text{pred}}=1$, $w_{\text{sigreg}}=0.5$ (script default; the class default is 0.05), $w_{\text{ground}}=1$, $w_{\text{semigroup}}=0.1$. Training: AdamW, lr $2\times10^{-3}$, batch 64, cosine schedule, gradient clipping 1.0.

**Readout for forecasting:** a ridge probe from clean latents to observables, fit on the training split.

**Baselines** (same inputs: noisy records up to the context step plus all actions): ridge regression; an autoregressive one-step MLP rolled out in observation space; a direct supervised MLP. Each also comes in a masked-coupling variant.

**Tasks:**
1. **Forecasting** (gate J2): from the noisy record at context step $c=4$, predict $P_{\text{baryonic}}$, $P_{\text{meson}}$, $C_{\text{string}}$ at $+4$ and $+8$ steps on held-out couplings.
2. **Masked-coupling identification** *(label)*: the same, with $(c_M,c_H,c_B)$ hidden, so the model must infer the couplings from the early record.
3. **Label-free error signal** (gate J3):
   - `jepa_twin` = latent distance between a hardware record and the twin's record;
   - `jepa_self` = distance between the measured deep record and the prediction from the shallowest record;
   - `jepa_t0` = prediction from the exact initial record;
   - baselines: `raw_twin` (observation-space distance) and `flag_rate`.
4. **Depth extrapolation on hardware:** forecast the $t=3/g_E$ observables from the $r=1,2$ hardware records and compare with the direct $r=8$ hardware estimate.
5. **$\mu^*$ from held-out data:** fit the resonance in the strong-coupling family.

**Anti-collapse options added on 5 Oct** (commit `0a76800`): `JEPAConfig.ema_target` (EMA target encoder with stop-gradient; SIGReg then acts on the context latent only); a horizon curriculum (`curriculum_epochs`: first train on horizons 1–2, then all); a `--w-ground` flag; and spawned training seeds (§12.4).

---

## 6. Data

| dataset | family | carrier | trajectories | steps × $\Delta t$ | built on | wall time | checksum (sha256, first 12) | splits: train / val / held-out mass / held-out family |
|---|---|---|---|---|---|---|---|---|
| `main` | on-family + strong | diagonal | 20,000 | 8–12 × {0.125, 0.25, 0.5} (on-family) / {2, 4, 8} (strong) | laptop | 158 s | `73fff8e5a7b7` | 11,539 / 2,392 / 6,069 / onfam 2,935, strong 3,134 |
| `chain_onfam` | on-family, S3 starts, no quench | chain, $K=12$ | 5,000 | 8–12 × 0.375 | laptop | 1,668 s | `bdcd6e895a06` | 2,859 / 741 / 1,400 / 1,400 |
| `chain_strong` | strong, S3 starts | chain, $K=24$ | 3,000 | 8 × {2, 4, 8} | Perlmutter (`jobs/001`) | 789 s | `935692f343d8` | 1,897 / 276 / 827 / 827 |

**Grids:**
- On-family: $g_E\in\{1.0,1.15,1.3,1.45,1.6,1.75,2.0\}$; held out **1.3, 1.75**; validation 1.45. $\mu\in\{0.15,0.25,0.375,0.5,0.65\}$.
- Strong coupling: $\mu\in\{0.15,0.2,0.25,0.3,0.33,0.375,0.42,0.45,0.5,0.575,0.65\}$; held out **0.3, 0.42, 0.5**; validation 0.45.
- Starts: S3 ×3, S1, random $N=4$ superposition. Quench fraction 0.2. Master seed 20261005.

Splits are made by rule (by coupling label), never by row, and are checked to have zero leakage. "Held-out family" sets are subsets of "held-out mass", which is why the counts don't add up to the totals.

**Reproducibility finding (5 Oct, new):** `data/main` rebuilt on Perlmutter from the same manifest and seed has checksum **`76f4c9055591`**, not the laptop's `73fff8e5a7b7`. Every split size is identical, and two independent Perlmutter jobs (002, 003) agree with each other. So the data differ in their bytes, most likely in the last floating-point bits from different numerical libraries (an untested assumption). The size of the difference can't be measured yet, because the worker doesn't send back the data arrays. All Perlmutter training used the Perlmutter copy; the ceiling analysis (§10.3) used the laptop copy.

---

## 7. The digital twin
- Qiskit Aer density-matrix simulation of the 12-qubit chain circuits: 268 MB per state; 6–30 s per circuit on 2 CPU cores.
- Noise: a synthetic Heron-like model for development. For every hardware day, a model built from that day's calibration (`NoiseModel.from_backend`). The twin is "calibrated, not trusted": J3 measures how far it is from the device.
- Seeds come from `SeedSequence(master).spawn`, one per circuit. Twin repeats are checked to be distinct (J0 row D5).
- A full hardware day of twin runs is about 480 circuits, so full campaigns run on Perlmutter. "Arm B" on the twin is a degraded noise model (2× CZ error, 2× readout error).
- **Known limitation (report 008):** there is no GPU Aer on Perlmutter (`qiskit-aer` 0.17.2 overrides `qiskit-aer-gpu` 0.15.1), so twin runs there are CPU-only.

---

## 8. The hardware campaign (planned; nothing submitted yet)
- **Access:** IBM Quantum Open Plan, 10 QPU-minutes per 28-day window; Heron r2 devices (`ibm_torino` class). Two windows (late Oct, Nov) give about 20 minutes without paying.
- **Full design per calibration day:**
  - on-family $g_E\in\{1.3,1.75,2.0\}$, $\mu=3/8$, KC-Trotter $r\in\{1,2,4,8\}$: 12 points;
  - KC-prep at the same times: 12 points;
  - strong-coupling KC-prep at $\mu\in\{0.3,0.375,0.42,0.5\}$, $t\in\{10,15,20\}$: 12 points;
  - each point in Z and X settings, plus a mitigation arm B (dynamical decoupling + gate twirling).

  Total 144 circuits × 4,000 shots ≈ 5 QPU-min per day. Minimum design: 72 circuits, ≈ 2.5 min.
- **Pilot** (M4b): 12 circuits, ~1 min, measures the real shot rate, flag rates and line quality. Expected: flag rates 0.2–0.6; post-selected populations within 0.03 of ideal at $r=1$; 40–90 QPU-seconds.
- **Discipline, enforced in code** (`hardware/ibm.py`):
  1. a dry-run manifest with circuit hashes;
  2. a **human** sets `approved: true` and the manifest hash in `configs/hardware_budget.yaml`;
  3. `hw_submit.py submit --confirm` re-checks everything and submits **one** job;
  4. `collect` writes immutable raw counts.

  Claude never edits the approval fields. A QPU ledger tracks spent seconds; so far **0 s spent, no job ever submitted**.
- **Cross-backend day:** a second Open-plan QPU replaces IonQ. IonQ or any paid provider only with explicit approval (≈ \$8–20k on Braket otherwise).

---

## 9. Gates, preregistration and hypotheses

### 9.1 Gate thresholds (current `configs/gates.yaml`, commit `2b10e5b`)
| gate | when | rows |
|---|---|---|
| **J0 data** | 11 Oct (done 3 Oct) | fingerprints (82; 2/20/38/20/2; 16/16/18/16/16); two routes $\le10^{-12}$; Gauss commutator $\le10^{-12}$; estimator bias $\le4$ standard errors (diagonal and chain carriers); Krylov $K=12$ reproduces the P-A window to $10^{-3}$; twin repeats distinct (5); split leakage 0; checksum recorded |
| **J1 training** | 18 Oct | 5 seeds; no NaN; effective rank $\ge8/16$; grounding $R^2$: **energy $\ge0.887$** (changed from 0.99 on 5 Oct, `decisions/005`), $C_{\text{string}}\ge0.99$, $P_{\text{meson}}\ge0.95$, $P_{\text{baryonic}}\ge0.98$; semigroup residual $<10^{-3}$ |
| **J2 forecast** | 30 Oct | per family: JEPA MAE $\le0.05$ at $+4$ and $+8$ steps; not worse than ridge and autoregressive within 1.1× on $\ge2$ of 3 targets; masked-coupling task reported. Context step 4, 512 context shots, targets $P_{\text{baryonic}}$, $P_{\text{meson}}$, $C_{\text{string}}$ |
| **J3 hardware** | 13 Nov | $\ge24$ points; Spearman(`jepa_twin`, exact error) $\ge0.7$ at 512 shots; non-inferior to `raw_twin` within 0.05; AUROC $\ge0.8$ (arm B vs A); 3 calibration days; all baselines reported |
| **J4 quantum encoder** (optional) | week 7 | trains at 12 qubits; matched-shot comparison with the classical encoder |

### 9.2 Preregistered hypotheses (H1–H5)
- **H1 (no collapse):** the J1 rows above. Expected: met after the ablation ladder.
- **H2 (forecasting):** MAE $\le0.05$ at $+8$ on both held-out families; not worse than ridge/autoregressive within 1.1×. Expected: parity, not superiority; a possible advantage on the masked-coupling task.
- **H3 (label-free error signal):** at 512 shots, `jepa_twin` is non-inferior to `raw_twin` in rank correlation with the exact error, and separates mitigation arms with AUROC $\ge0.8$. Expected: non-inferior at low shots, a tie at 4,000.
- **H4 (depth extrapolation on hardware):** the forecast of $t=3/g_E$ from $r\le2$ hardware records beats the direct $r=8$ hardware estimate on $\ge2$ of 3 targets at every $g_E$. Expected: yes, by 2–5×.
- **H5 (resonance from hardware):** the $\mu^*$ estimate from the strong-coupling KC-prep points lies within 0.05 of 3/8.

**Preregistration** (session M2b, 16 Oct): `configs/gates.yaml` frozen, `docs/PREREGISTRATION.md` completed (hypotheses, exact analysis commands, exclusion rules — e.g. hardware points with flag rate > 0.8 are excluded and listed), dataset checksums, model configuration hash, git tag `prereg-2026-10-16`. **Not done yet.**

### 9.3 Claims the paper may and may not make
- **May (if the gates pass):**
  - a 12-qubit, 22-CZ-per-step hardware carrier with a depth ladder and an encoding flag;
  - a JEPA forecaster compared with baselines;
  - a label-free hardware error signal validated where the truth is known;
  - a hardware observation of the strong-coupling resonance via a compressed carrier;
  - an open benchmark dataset.
- **May never:**
  - quantum advantage;
  - new SU(2) physics, continuum limit or string tension;
  - "2+1D" (reserved for lattices of at least 2×3);
  - hardware evidence of gauge leakage;
  - scalability of the carrier;
  - "AI invented".

### 9.4 Error budget (lines, each to be measured)
| line | size (P-A window) | where measured |
|---|---|---|
| truncation $j_{\max}=\tfrac12$ | $\le0.06$ ($P_{\text{meson}}$), $\le0.014$ ($P_{\text{baryonic}}$) | plan App. B.3 |
| Krylov $K=12$ | $\le1.1\times10^{-4}$ | J0 row D4 |
| Trotter (Strang, $\Delta t=0.375$) | infidelity $\le1.2\times10^{-3}$ at $r=8$ | `trotter_error` |
| shot noise (4,000 shots, Z+X) | ~0.01–0.02 on chain estimates | J0 row D3 |
| device (post-selected) | to be measured (pilot) | W4 |
| twin mismatch | `raw_twin` | J3 |
| model forecast | J2 | W4 |

---

## 10. What has been done, session by session (with every number)

### 10.1 Before the repository existed (1–2 Oct, planner sessions; reports 000–005)
- **`reports/000` — audit of the 1 Oct plan and the starter package.** The audit found 15 problems, 5 of them severe:
  - the old hardware design had no depth ladder;
  - it had no label-free baselines;
  - its forecasting baselines were guessed (ridge regression already reached 0.02–0.04 MAE on the old task);
  - its resonance claim was untestable at $g_E=2$;
  - it misjudged the IBM budget.

  The fixes are the v2 plan: the Krylov-chain carrier, two coupling families, label-free baselines, and an IBM budget of about 8–13 minutes. The audit also implemented the full physics core, the carrier, estimators, the dataset generator, the JEPA, the baselines, the twin, the hardware guard, gates J0–J3 and CI. At smoke scale, J0 passed in full mode and the whole pipeline ran end to end in about 1 minute. The v0 JEPA was not yet healthy (effective rank 4–6/16; grounding $R^2$ 0.81–0.99).
- **`reports/001` — numbered artifacts and the Graphify code graph.**
  - Every plan, prompt, report, decision and figure is a numbered, append-only file created by `scripts/new_artifact.py` and checked by `scripts/check_artifacts.py`.
  - The code graph (graphifyy 0.9.74, no LLM) is rebuilt each session, and CI checks that the committed copy is up to date.
  - 26 tests passed.
- **`reports/002`–`004` — compute.** The RTX 3070 desktop was dropped. The project now runs on the laptop for light work and Perlmutter for heavy work, through a GitHub job queue. All laptop computation goes through `scripts/run.py`, which:
  - **classifies** each command: GPU work or more than 20 estimated laptop-minutes goes to Perlmutter;
  - **admits** it only if 16 GB of memory stay free and 2 logical CPUs stay idle;
  - **caps** it at nice 19, 2–4 threads, 4–16 GB, with `oom_score_adj=1000` so the kernel kills it before anything else;
  - **heals** it (retry with more memory, or send it to Perlmutter).

  The Perlmutter worker is a `scrontab` tick every 15 min that runs Slurm jobs and pushes results to a `results` branch, resubmitting on TIMEOUT, OOM or node failure. Measured laptop costs (2 cores): tests 34 s / 0.9 GB; J0 10 s / 0.2 GB; 20,000-trajectory dataset 87 s / 0.2 GB; one twin circuit 51 s / 0.5 GB. Bugs found and fixed along the way:
  - a `data/` ignore pattern also hid the package folder `src/su2qc_jepa/data/`;
  - a cgroup memory limit that wasn't enforced;
  - a job that could outlive its runner;
  - a ledger mislabel.
- **`reports/005`:** the worker install now merges into Digonto's existing scrontab and keeps the two other repositories' entries byte for byte (`scripts/worker/scrontab_merge.sh`).

### 10.2 Environment and M0 (2 Oct; reports 006–008)
- **`reports/006` — laptop environments.** The `coding` conda environment, broken by a CUDA-13 PyTorch install, was repaired:
  - `cuda-bindings` 13.4.3 → 12.9.9;
  - 16 CUDA-13 packages, torch/triton and graphify removed;
  - `pip check` clean;
  - 14 GB → 8.3 GB.

  The separate `su2qc-jepa` environment was created: Python 3.12.14, torch 2.14.1+cpu, qiskit 2.5.2, qiskit-aer 0.17.2, graphifyy 0.9.74; 47 tests passed. The laptop GPU (GTX 1060, compute capability 6.1) can't be used by current PyTorch.
- **`reports/007` — M0 PASS.** Public repository created, bootstrap commit `88dc52d`, CI run 37069894565 green (lint, artifact conventions, tests, graph freshness, physics fingerprints), 47/47 tests, code graph 842 nodes / 1,615 edges / 64 communities.
- **`reports/008` — Perlmutter worker installed.** Account `m4135_g`; environment `/global/common/software/m4135/su2qc-jepa-env`. Smoke test `jobs/000`: Slurm id 59236367 on an NVIDIA A100-SXM4-40GB, `torch_device_used: cuda`, COMPLETED, 0.003 node-hours. Problems recorded: `fetch.py` can overwrite tracked files; no GPU Aer on Perlmutter.

### 10.3 M1 — physics cross-check, datasets, gate J0 (3–4 Oct; `reports/009`) — **J0 PASS 9/9**
- The cross-check against `su2qc` passed (§3.4).
- The three datasets were built (§6). `chain_strong` was too slow for the laptop (0.82 s per trajectory, ≈ 41 min) and ran on Perlmutter (`jobs/001`, Slurm 59281851, 0.223 h, 0.056 node-hours).
- Gate J0 on `data/main` (`evidence/J0_data/20261003T201012Z.json`):

| row | measured | threshold |
|---|---|---|
| D1 state counts | 82; 2/20/38/20/2; 16/16/18/16/16 | same |
| D2 two-route agreement | $4.4\times10^{-16}$ | $10^{-12}$ |
| D2 Gauss-law commutator | 0 | $10^{-12}$ |
| D3 estimator bias, diagonal carrier (1,024 shots, 200 trials, max over 18 observables) | 2.36 standard errors | 4.0 |
| D3 estimator bias, chain carrier (Z+X) | 1.44 standard errors | 4.0 |
| D4 Krylov $K=12$, P-A window $t\le3/g_E$ | $1.05\times10^{-4}$ | $10^{-3}$ |
| D5 twin repeats independent | 5/5 distinct | 5 |
| D6 split leakage | 0 | 0 |
| D6 checksum recorded | `73fff8e5a7b7` | present |

Problems noted in M1:
- the runner's time estimate ignores the carrier, so chain datasets ran about 56× (`chain_onfam`, 0.5 min estimated vs 28 min) and 137× (`chain_strong`, 0.3 vs ≈ 41 min) longer than estimated;
- the plan says bias $\le2.5$ standard errors while the config says 4.0 (both measured values meet 2.5);
- a false "worker stopped" warning (an idle worker only heartbeats every 12 h).

### 10.4 M2a — model health (5 Oct; `reports/010`, `decisions/005`, and results fetched at 21:30 UTC)

**Code changes** (commit `0a76800`): the EMA target encoder, the horizon curriculum, `--w-ground`, and a **seed fix**. Training seeds had been the integers 0–4, and the shuffle seed $s+e$ overlapped between runs (seed 0 epoch 1 = seed 1 epoch 0). The project forbids adjacent seeds, because that bug once voided error bars. Seeds now come from `SeedSequence(20261005)`: [462709266, 3658436304, 2224198422, 672449321, 2231613345].

**Laptop check** (10 epochs, 1 seed, `runs/v1_check`): no NaN; 17.5 s per epoch on 2 threads; total 765 s including baselines. At epoch 10:

| quantity | value | J1 threshold |
|---|---|---|
| effective rank | 3.93/16 | $\ge8$ |
| $R^2$ energy | 0.895 | $\ge0.887$ |
| $R^2$ $C_{\text{string}}$ | 0.997 | $\ge0.99$ |
| $R^2$ $P_{\text{meson}}$ | 0.964 | $\ge0.95$ |
| $R^2$ $P_{\text{baryonic}}$ | 0.996 | $\ge0.98$ |
| semigroup residual | $2.5\times10^{-4}$ | $<10^{-3}$ |

Forecast MAE at +8 steps, on-family, $P_{\text{baryonic}}$: JEPA 0.072, ridge 0.144, supervised MLP 0.048 (1 seed, 10 epochs; not a J2 result).

**The energy ceiling** (`scripts/j1_ceiling.py`, `evidence/J1_training/ceiling_main.json`; validation split, 26,348 rows; training split 126,824 rows). The question was: how well can *any* regressor predict each grounding target from one clean observation?

| target | ridge | 5-NN | boosted trees | MLP | best, with couplings added |
|---|---|---|---|---|---|
| energy | 0.887 | 0.851 | 0.890 | **0.914** | 0.994 |
| $C_{\text{string}}$ | 1.000 | 0.997 | 1.000 | 1.000 | 1.000 |
| $P_{\text{meson}}$ | 1.000 | 0.989 | 0.996 | 1.000 | 1.000 |
| $P_{\text{baryonic}}$ | 1.000 | 0.997 | 1.000 | 1.000 | 1.000 |

Why energy is capped: $E=\langle\psi|H|\psi\rangle$ contains the hopping and plaquette expectation values, which are off-diagonal and not among the 18 observables. It also depends on the couplings, which reach the model only through the actions. The other three targets are themselves inputs. The clean observations have effective rank 11.2 (standardised; 9.1 raw), with 14 nonzero variance directions of 18, so a latent rank $\ge8$ is reachable in principle.

**Decision `decisions/005`** (Digonto, option C, 5 Oct): the J1 energy threshold is $0.887=0.97\times0.9145$. The model may lose at most 3% of the energy variance that one record actually contains. The rejected alternatives were:
- A: keep 0.99 (always fails);
- B: let the energy head see the couplings (ceiling 0.994, so a margin of only 0.004, a design change made just to pass, and every run redone);
- D: drop the row (the other three rows are nearly automatic).

**Perlmutter runs.** All at commit `0a76800`, 5 seeds, 200 epochs, `data/main` rebuilt on Perlmutter:

| job | run | change vs base | state at 21:30 UTC | Slurm time / node-hours |
|---|---|---|---|---|
| `jobs/002` | `v1_base` | none ($w_{\text{sigreg}}=0.5$), plus masked runs | **FAILED after all training finished** | 2.164 h / 0.541 |
| `jobs/003` | `v1_wsigreg2` | $w_{\text{sigreg}}=2$ | **FAILED after all training finished** | 1.035 h / 0.259 |
| `jobs/004` | `v1_wsigreg5` | $w_{\text{sigreg}}=5$ | submitted | – |
| `jobs/005` | `v1_latent32` | latent 32 | submitted | – |
| `jobs/006` | `v1_ema` | EMA target $\tau=0.996$ | submitted | – |
| `jobs/007` | `v1_wground3` | $w_{\text{ground}}=3$ | submitted | – |
| `jobs/008` | `v1_curriculum` | 50 epochs on horizons 1–2 first | submitted | – |

Perlmutter budget used: 0.859 of 50 node-hours. Training speed on the A100: about 3.8 s per epoch (≈ 760 s per 200-epoch run), against 17.5 s on 2 laptop threads.

**Why 002 and 003 failed (a code defect, found 5 Oct):** after training finished and the models and `history.json` files were saved, the script computes the forecasting baselines. `baseline_autoregressive` in `src/su2qc_jepa/models/train.py` builds its network on the CPU while the data are on the GPU, so it crashes with "Expected all tensors to be on the same device". It never showed on the laptop, which has no GPU. Consequences:
- the **training results needed for J1 exist**;
- `forecast_eval.json` (the J2 input) was not written;
- jobs 004–008 run the same code and will most likely fail at the same final step. That is a prediction, not yet observed.

**Preliminary J1 numbers** (final epoch 200, validation split, read from the fetched `history.json` files; **not a gate result**, since the gate script has not been run):

| run (seeds) | effective rank (min…max) | $R^2$ energy (min) | $R^2$ $C_{\text{string}}$ (min) | $R^2$ $P_{\text{meson}}$ (min) | $R^2$ $P_{\text{baryonic}}$ (min) | semigroup residual (max) | isotropy |
|---|---|---|---|---|---|---|---|
| `v1_base` (5) | 5.16 … 6.15 | 0.8994 | 0.9982 | 0.9779 | 0.9971 | $3.29\times10^{-3}$ | 0.002–0.013 |
| `v1_base` masked (5) | 4.50 … 5.42 | 0.9005 | 0.9976 | 0.9752 | 0.9968 | $2.49\times10^{-4}$ | 0.002–0.004 |
| `v1_wsigreg2` (5) | 8.26 … 9.10 | 0.8999 | 0.9976 | 0.9720 | 0.9965 | $5.34\times10^{-3}$ | 0.025–0.069 |
| J1 threshold | $\ge8$ | $\ge0.887$ | $\ge0.99$ | $\ge0.95$ | $\ge0.98$ | $<10^{-3}$ | – |

What this shows, preliminary:
1. All four grounding rows pass in every run. Energy $R^2\approx0.90$ is close to the measured ceiling of 0.914.
2. **Raising the SIGReg weight from 0.5 to 2 fixes the rank** (5.2–6.2 → 8.3–9.1). It also raises the prediction loss from 0.004 to 0.011.
3. **A new problem: the semigroup row fails in the unmasked runs** ($1.9$–$3.3\times10^{-3}$ for base, $3.5$–$5.3\times10^{-3}$ for SIGReg 2), although the 10-epoch check had $2.5\times10^{-4}$ and the masked runs have about $2\times10^{-4}$. So the residual grows with longer training when the couplings are visible. No rung so far passes every row. The remaining rungs (004–008) will show whether any does.

---

## 11. Infrastructure and repository conventions (how the work is done)
- **Sessions:** each Claude Code session is driven by a numbered prompt and ends with tests, the milestone gate, a code-graph refresh, a numbered report, an artifact check, a `STATE.json` update and scoped commits (`physics:`, `data:`, `model:`, `gate:`, `docs:`, `chore:`). History is never rewritten.
- **Frozen items** (changing them needs a decision record): physics conventions; `configs/gates.yaml` after the preregistration tag; the observation layout; dataset checksums; artifact and graph conventions.
- **Decision records:** `decisions/000` frozen conventions; `001` numbered artifacts and code graph; `002`→`003`→`004` compute policy (laptop + Perlmutter only, runner and queue); `005` J1 energy threshold.
- **Folders:** `plans/`, `prompts/`, `reports/`, `decisions/`, `figures/`, `jobs/` (numbered); `src/su2qc_jepa/{physics,data,models,twin,hardware,gates,repo}`; `scripts/`; `configs/`; `tests/` (54 fast tests; on 5 Oct 53 passed and the 54th, the code-graph freshness check, passed after the graph refresh); `evidence/` (machine records); `graphify-out/` (code graph, 931+ nodes).
- **Hardware rules:** dry-run manifest → human approval in the budget file → one confirmed job → immutable raw counts; QPU ledger; IBM token only on the laptop.
- **Writing rules:** plain English, every jargon word defined, LaTeX math, no "quantum advantage", no "AI invented", no "first 2+1D".

---

## 12. Open problems and risks (as of 5 Oct, 21:40 UTC)
1. **The baseline code crashes on GPU** (`baseline_autoregressive`, device mismatch). It blocks `forecast_eval.json` (the J2 input) for every Perlmutter run. Fix: build the network on the data's device, then re-queue under new job numbers.
2. **The semigroup residual fails J1** in all unmasked 200-epoch runs so far. Candidate directions (not tested): a higher semigroup loss weight; the plan's ladder rungs still to come; checking whether the relative residual's denominator shrinks as SIGReg spreads the latent.
3. **The laptop and Perlmutter rebuilds of `data/main` differ** in checksum (`73fff8e5a7b7` vs `76f4c9055591`), with identical splits. The size of the difference is unmeasured. The preregistration must name which checksum is the reference.
4. **The energy row now depends on a measured ceiling** (0.9145) that a better regressor could raise. `decisions/005` says to re-measure if the data or the observation layout change.
5. The runner's time estimate ignores the carrier (chain datasets ran 56–137× longer than estimated); the worker "stopped" warning fires falsely between 8 and 12 h of idleness; `fetch.py` can overwrite tracked files such as `data/main/manifest.json`.
6. There is no GPU Aer on Perlmutter, so twin campaigns are CPU-only there.
7. **Schedule:** J1 is due 18 Oct and the preregistration tag 16 Oct. J1 is still NOT RUN.
8. **Never yet tested:** any real hardware job, the IBM pilot, the calibrated twin, J2, J3.

---

## 13. Timeline and milestone status

| milestone | weeks | content | status |
|---|---|---|---|
| M-env | 2 Oct | laptop environments | DONE (`reports/006`) |
| M0 | W1 | repository, CI, code graph, Perlmutter worker | PASS (`reports/007`, `008`) |
| M1 | W1 (5–11 Oct) | physics cross-check, datasets, J0 | PASS (`reports/009`), J0 9/9 |
| M2a | W2 (12–18 Oct) | JEPA v1, ablation ladder, J1, diagnostics figure, model card | IN PROGRESS: ladder running; J1 NOT RUN; preliminary numbers in §10.4 |
| M2b | 16 Oct | preregistration, tag `prereg-2026-10-16` | NOT RUN |
| M3 | W3 (19–25 Oct) | forecasting, $\mu^*$ estimator, figures F1/F2; calibrated twin, twin campaign, J3 rehearsal, hardware dry run | NOT RUN |
| M4 | W4 (26 Oct – 1 Nov) | J2; ablation table; hardware pilot (12 circuits, one job) | NOT RUN |
| M5 | W5 (2–8 Nov) | hardware days 1 and 2 (twin of the day, dry run, approval, two jobs per day) | NOT RUN |
| M6 | W6 (9–15 Nov) | hardware day 3, J3, error budget, $\mu^*$ from hardware | NOT RUN |
| M7 | W7 (16–22 Nov) | one stretch item: 2×3 ladder (simulator), quantum encoder J4, or IonQ only with credits | NOT RUN |
| M8 | W8 (23–29 Nov) | paper assembly, release, clean replication; preprint target 27 Nov | NOT RUN |

---

## 14. Next actions
1. Fix the GPU device bug in `baseline_autoregressive` (and check the other baselines). Add a test that would have caught it. Re-queue the forecasting evaluation.
2. When jobs 004–008 finish, fetch them (taking care not to overwrite `data/main/manifest.json`). Run the official J1 gate per rung with `python scripts/run.py -- python scripts/run_gate.py J1 --runs runs/<rung>/seed0 … seed4`, then make the diagnostics figure (`scripts/plot_j1_diagnostics.py`) and write `docs/MODEL_CARD.md` (`prompts/010`).
3. Diagnose the semigroup residual if no rung passes it.
4. Before 16 Oct: decide which `data/main` checksum is the reference; then do M2b (preregistration).

---

## 15. Where to find things
- Plan: `plans/001_gauge-jepa-p-v2.md`.
- Prompts: `prompts/000`–`010`.
- Reports: `reports/000`–`011` (this file).
- Decisions: `decisions/000`–`005`.
- Thresholds: `configs/gates.yaml`.
- Gate ledger: `evidence/GATE_LEDGER.md`.
- J0 evidence: `evidence/J0_data/`. J1 ceiling: `evidence/J1_training/ceiling_main.json`.
- Job files: `jobs/000`–`008`; job results on the git branch `results`.
- Physics summary: `docs/PHYSICS.md`. Claims ledger: `docs/CLAIMS.md`. Preregistration draft: `docs/PREREGISTRATION.md`.
- State: `STATE.json`.
