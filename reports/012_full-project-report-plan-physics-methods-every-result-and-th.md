---
id: reports/012
title: 'Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)'
series: reports
created_utc: '2026-10-06T05:49:57Z'
author: claude-code
milestone: M2
status: done
supersedes: null
superseded_by: null
---

# Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)

**Milestone:** M2 · **Prompt:** none numbered (direct request from Digonto via the coordinating session; the prompt in force for M2 is `prompts/002`, follow-up `prompts/010`) · **Commit range:** read at `80d7fdf` (HEAD, 2026-10-05 23:34 -0600) · **Written:** 2026-10-06, about 06:00 UTC · **Active plan:** `plans/001` · **Supersedes in spirit (not formally):** `reports/011` (the overview of 5 Oct); this report keeps 011 as its backbone and updates and extends it.

**Repository:** https://github.com/digonto10602/su2qc-jepa (public) · **Researcher:** Digonto

## What was asked
Digonto asked, through the coordinating session, for one self-contained Markdown report that (a) explains the whole project (plan, physics, methods, infrastructure, history, every result) and (b) carries, as parseable tables, the data behind every plot, so that another AI assistant to which the file is uploaded can both explain the project and re-make every plot without access to the repository.

## Actions taken (for this report)
1. Read `~/.claude/CLAUDE.md`, `CLAUDE.md`, `plans/001`, `prompts/000`–`010`, `reports/009`–`011`, `decisions/000`–`005`, `docs/*`, `configs/gates.yaml`, `STATE.json`, `evidence/GATE_LEDGER.md`, all `evidence/J0_data` and `evidence/J1_training` JSON files, `evidence/jobs/*/status.json`, the job files, the logs of jobs 002, 004, 007, 009, 010, and the model code (`models/jepa.py`, `models/train.py`).
2. Ran `python scripts/jobs/status.py` (read-only) to read the job states and the node-hour budget.
3. Wrote three helper scripts (Appendix A) and ran each through `python scripts/run.py --no-queue --threads 1 -- python <script>` (all exit 0, peak memory below 0.1 GB): `plot_tables.py` (tables from the 7 groups of run histories), `physics_curves.py` (recomputes the plan's physics curves with the repository's own physics core and compares them with the numbers quoted in the plan), `evidence_tables.py` (tables from evidence JSON files).
4. Created this file with `python scripts/new_artifact.py reports ... --milestone M2 --author claude-code`; set `status: done`.
5. **Not done, on purpose:** no commit, no push, no edit of any other file, no change of `configs/gates.yaml`, `STATE.json`, `data/`, `runs/`, `jobs/`; no job queued or fetched; no test suite or gate run.

**Provenance rule for this report.** Every number comes from a file I read (the path is given) or from a computation I ran (the helper script is in Appendix A). Where a number is quoted from an earlier report or the plan and I did not re-derive it, the text says "quoted from". Where a value could not be found it says "not recorded".

---

## 0. Reading guide and glossary

### 0.1 How to read this document
This document is for a person, or for another AI assistant asked to explain the project. §1–§6 explain the project; §7 is the chronological history; §8 the current results; **§9 is the plot-data section** (the most important part for re-making figures); §10 the decisions and risks; §11 what happens next; the appendices hold the helper scripts, a file map and the commit list.

Conventions:
- **Status words for gates** (only these): PASS, FAIL, PARTIAL, NOT RUN, VOID. **Claim words:** MEASURED, PROVEN (by tests), PROPOSED, UNVERIFIED, EMULATED.
- **EMULATED** = from a simulation of a noisy device, not from a real device. **No job has ever been run on real quantum hardware in this project (0 QPU seconds spent, no IBM job id exists); every noisy number is EMULATED.**
- **Units:** energies in units of $g_E$ (the electric energy quantum, §2.1); times in units of $1/g_E$; couplings as the four-tuple $(c_E,c_M,c_H,c_B)$. Quantities such as $R^2$, ranks and residuals are dimensionless.
- **(label)** marks a name the project invented; it is not a standard physics or machine-learning term.
- File paths are relative to the repository root. Short hashes such as `0a76800` are git commits.
- Where this report quotes a number from a JSON file with 5 significant digits, the JSON holds the full double-precision value.

### 0.2 Glossary (every technical term used)
| term | meaning |
|---|---|
| SU(2) lattice gauge theory | a model of a force field (a simplified version of the strong force) on a grid. "SU(2)" is the symmetry group: two "colours" instead of the three of real QCD |
| plaquette | the smallest closed square of a lattice: 4 sites (vertices) and 4 links |
| Kogut–Susskind Hamiltonian | the standard energy operator of a lattice gauge theory with continuous time |
| link, $j_\ell$ | the gauge field lives on links; $j_\ell\in\{0,\tfrac12\}$ is the electric flux on link $\ell$ (truncated at $j_{\max}=\tfrac12$) |
| truncation | keeping only $j\le j_{\max}$; $j_{\max}=1$ is the larger reference space used to estimate the truncation error |
| staggered fermions | a way to put matter particles on a lattice; even and odd sites carry particles and antiparticles |
| Gauss's law, gauge invariance | a constraint linking the flux at each site to the matter charge there; only states obeying it are physical ("gauge-invariant") |
| string, string breaking | a line of flux between charges; it "breaks" when its energy is used to create a matter pair that screens the charges |
| sector $N$ | the subspace with total matter number $N$; the dynamics studied live in the $N=4$ sector (38 states) |
| S3, S1, MM, $B\bar B$, Loop, $\Omega_0$ | named basis states (§2.4): S3 stretched string over three links, S1 short string on one link, MM two mesons, $B\bar B$ baryon–antibaryon, Loop closed flux loop, $\Omega_0$ bare vacuum |
| $\mu^*=3/8$ resonance | the mass at which the stretched-string energy equals the energies of broken configurations, so the string breaks fastest |
| breaking fraction | $P_{\text{meson}}+P_{\text{baryonic}}$, the weight of broken-string channels (definition fixed by the check in §9, P11; the plan does not state it in words) |
| Lanczos / Krylov | Lanczos builds, from a start state, an orthonormal basis (Krylov basis) in which $H$ is tridiagonal, with diagonal $\alpha_k$ and off-diagonal $\beta_k$ |
| Trotter / Strang splitting | approximating $e^{-iHt}$ by a product of simpler exponentials; Strang is the symmetric second-order version |
| CZ gate | the two-qubit entangling gate on IBM hardware; the CZ count is the main cost and noise measure |
| shots | number of repetitions of a quantum circuit; statistical error $\propto1/\sqrt{\text{shots}}$ |
| QPU | quantum processing unit, the real quantum chip |
| twin (digital twin) | a classical noisy simulation of the device (Qiskit Aer density-matrix simulator with a noise model) |
| JEPA | Joint-Embedding Predictive Architecture: predict the *representation* of the future observation, not the observation itself |
| encoder, latent, predictor | encoder: network mapping an observation to a short vector (the latent); predictor: network that advances the latent under actions |
| collapse | failure in which the encoder maps everything to nearly the same latent; prediction becomes trivially easy and useless |
| SIGReg | "Sketched Isotropic Gaussian Regularizer" (LeJEPA, arXiv:2511.08544): a loss that pushes the latent distribution toward a standard Gaussian, preventing collapse |
| Epps–Pulley statistic | a distance between the empirical characteristic function of a sample and that of a Gaussian; SIGReg applies it to random 1-D projections |
| EMA target encoder | alternative anti-collapse device (I-JEPA style): the target latent comes from a slowly updated copy of the encoder (exponential moving average, EMA) with no gradient through it ("stop-gradient") |
| grounding heads | small linear maps from the latent to known physical quantities (energy, $C_{\text{string}}$, $P_{\text{meson}}$, $P_{\text{baryonic}}$, flag rate), trained alongside so the latent stays physically meaningful |
| semigroup consistency | predicting two steps at once should equal predicting one step twice, as true time evolution does |
| semigroup residual | the diagnostic $\overline{(P_{2}-P_{1}\!\circ\!P_{1})^2}/\overline{P_{2}^2}$ (relative squared mismatch) on the validation split (`models/train.py: diagnostics`) |
| effective rank | $\exp$ of the entropy of the normalised singular values of the centred latent batch: roughly "how many latent directions are really used"; maximum 16 for a 16-dimensional latent (32 for latent 32) |
| isotropy | smallest divided by largest per-direction latent variance (1 = perfectly round latent cloud) |
| $R^2$ | coefficient of determination $1-\sum(y-\hat y)^2/\sum(y-\bar y)^2$; 1 is perfect |
| ridge regression | linear regression with a small penalty on coefficient size |
| k-NN, gradient-boosted trees, MLP | nearest-neighbour regression; an ensemble of small decision trees; a multi-layer perceptron (a plain neural network) |
| MAE | mean absolute error |
| Spearman correlation | rank correlation (do two quantities order the points the same way?) |
| AUROC | area under the receiver-operating curve; how well a score separates two groups (1 perfect, 0.5 chance) |
| seed | the integer that starts a random-number stream; "spawned" seeds come from `numpy.random.SeedSequence`, which makes the streams independent |
| epoch | one pass of the training algorithm over the whole training set |
| gate | a scripted pass/fail check with preregistered thresholds; gate scripts are the only arbiters |
| preregistration | fixing hypotheses, thresholds and analysis commands before seeing the final data, signed by a git tag |
| ledger | `evidence/GATE_LEDGER.md` (gate results), `.local_runs/ledger.jsonl` (laptop runner attempts), `evidence/hardware/QPU_LEDGER.json` (QPU seconds; no job yet) |
| fingerprint (dataset) | compact summary of a dataset (sum per trajectory of each array and 2000 sampled raw values, plus array checksums) used to compare two builds (`data/trajectories.py: dataset_fingerprint`) |
| checksum | a hash (sha256) of the data arrays; two builds are bit-identical if and only if the checksums agree |
| CUDA, GPU, A100 | NVIDIA's GPU programming platform; graphics processor; the NVIDIA A100 accelerator on Perlmutter |
| device mismatch | a PyTorch error when a computation mixes tensors on the CPU and on the GPU |
| Perlmutter, NERSC | the US supercomputer (and its centre) used for heavy jobs |
| Slurm, scrontab | Perlmutter's batch scheduler; NERSC's replacement for cron (timed job starts) |
| node-hour | accounting unit: one full node for one hour; one A100 on the shared queue costs ¼ node-hour per hour |
| job (here) | a numbered request `jobs/NNN_*.yaml` that the Perlmutter worker runs with Slurm |
| Graphify | a tool that builds a navigable graph of the codebase (files, functions, calls); used for navigation only, never as evidence of correctness |
| conda environment | an isolated Python installation (here `su2qc-jepa` on the laptop) |

---

## 1. Project goal, scope, allowed and forbidden claims

**One paragraph.** The project trains a **JEPA world model** on a small, exactly solvable lattice gauge theory: SU(2) gauge field with matter on one square plaquette (4 sites, 4 links). The physics studied is **string breaking**. The model reads finite-shot measurement records of the kind a quantum computer produces, and is trained to predict how the system evolves under given actions (time steps at given couplings, sudden mass changes). The goal is **not** a computational advantage: everything is solved exactly on a laptop. The three goals are:
1. a learned forecaster of late-time behaviour, compared fairly with simple baselines (hypothesis H2);
2. a *label-free error signal* for quantum hardware, i.e. a way to tell how wrong a hardware result is without knowing the true answer, validated here where the truth *is* known (H3);
3. a hardware dataset taken on IBM quantum computers with a compact 12-qubit circuit design, the **Krylov-chain carrier (label)**, which has a controllable circuit depth and a built-in error flag (H4, H5).

The plan runs eight weeks, 5 Oct – 29 Nov 2026 (`plans/001`). The end product is a methods-and-benchmark paper (preprint target 27 Nov).

**The paper may say (only if the corresponding gates pass):**
- a 12-qubit, 22-CZ-per-step hardware carrier with a depth ladder and an encoding flag;
- a JEPA forecaster compared with baselines;
- a label-free hardware error signal validated where the truth is known;
- a hardware observation of the strong-coupling resonance through a compressed carrier;
- an open benchmark dataset with checksums and a preregistered evaluation.

**The paper may never say:** quantum advantage; new SU(2) physics, a continuum limit or a string tension; "2+1D" (reserved for lattices with an interior vertex, at least 2×3; this plaquette is the smallest 2D unit); hardware evidence of gauge leakage (the chain carrier cannot leak in the gauge sense; its flag is an *encoding* flag); scalability of the carrier; "AI invented"; "first 2+1D".

**Status of the claims (docs/CLAIMS.md, updated reading):** C1–C5 (state counts, two routes, $g_E=1$ dynamics, Krylov window, chain cost) PROVEN or MEASURED; C7 (JEPA meets H1) is **UNVERIFIED and currently contradicted for the semigroup row** (§8.3); C8–C11 UNVERIFIED; C12 (all noisy numbers) EMULATED.

---

## 2. Physics

### 2.1 Model and Hamiltonian
Hard-core SU(2) Kogut–Susskind plaquette:
- link flux $j_\ell\in\{0,\tfrac12\}$ on four links $(l_a,l_1,l_2,l_3)$;
- two-colour staggered fermions on four vertices $v_0..v_3$ at coordinates $(0,0),(1,0),(1,1),(0,1)$;
- open boundaries.

In units of $g_E=g^2/2a$:

$$\frac{H}{g_E}=c_E\sum_\ell j_\ell(j_\ell+1)+c_M\sum_n(-1)^{n_x+n_y}N_n+c_H\sum_\ell\big(\eta_\ell\,\psi_{\text{tail}}^\dagger U_\ell\,\psi_{\text{head}}+\text{h.c.}\big)+c_B\,\mathrm{Tr}\big(U_\square+U_\square^\dagger\big),$$

with plaquette loop $U_\square=U_aU_3U_2^\dagger U_1^\dagger$, staggered phases $\eta=(+1,+1,+1,-1)$ on $(l_a,l_1,l_2,l_3)$ (so $\prod_\square\eta=-1$), and Jordan–Wigner ordering $(v_0^-,v_0^+,\dots,v_3^+)$ (the rule that maps fermions onto qubits). The four terms are the electric energy $\mathcal E$, the mass term $\mathcal M$, the hopping (kinetic) term $\mathcal T$ and the magnetic (plaquette) term $\mathcal B$; in code $H/g_E=c_E\mathcal E+c_M\mathcal M+2c_H\mathcal T+c_B\mathcal B$ (quoted from `reports/009`, `reports/010`).

On-family couplings: $c_E=1$, $c_M=\mu=m/g_E$, $c_H=1/(2g_E)$, $c_B=-1/(4g_E^2)$. All conventions are frozen in `src/su2qc_jepa/physics/conventions.py` (`decisions/000`: the staggered-phase product and the *negative* magnetic coefficient are one joint convention).

### 2.2 Coupling points
| point | $(c_E,c_M,c_H,c_B)$ | note |
|---|---|---|
| **P-A** ($g_E=2$, $\mu=3/8$) | $(1,\,0.375,\,0.25,\,-0.0625)$ | the hardware window |
| **P-S** (strong coupling) | $(1,\,0.375,\,0.02,\,-0.02)$ | the regime of an earlier study by Sufian |
| $g_E=1$ | $(1,\,0.375,\,0.5,\,-0.25)$ (on-family formula) | used for the notes' dynamics table |
| on-family scan | $g_E\in\{1.0,1.15,1.3,1.45,1.6,1.75,2.0\}$ | with $\mu\in\{0.15,0.25,0.375,0.5,0.65\}$ |

### 2.3 Verified fingerprints (PROVEN by tests or MEASURED)
- **82 gauge-invariant states**, split by matter number $N=0,2,4,6,8$ as 2/20/38/20/2. Numbers of links excited: degeneracies 16/16/18/16/16. At $j_{\max}=1$: 152 states, 3/36/74/36/3. (Domain-wall counting: $82=32+48+2$; generating function $2+20x^2+38x^4+20x^6+2x^8$; `docs/PHYSICS.md`.)
- **Two routes agree.** Route A builds vertex singlets and block tensors; route B uses the full 160,000-dimensional space with explicit Gauss-law projection. They agree to $4.4\times10^{-16}$ (J0 row D2, `evidence/J0_data/20261003T201012Z.json`). The Gauss-law commutator $\|[G^a_n,H]\|=0$ exactly, and $H$ keeps the physical subspace invariant to $2\times10^{-16}$ (plan §3).
- **Hamiltonian structure.** Hopping: 4 links × 36 disjoint real $2\times2$ blocks (288 nonzeros). Plaquette: 41 disjoint pairs (82 nonzeros).
- **Channels in the $N=4$ sector** (matter content only): pair 8, meson 2, baryonic 26, vacuum-matter 2. Sub-projectors: S3 (1 state), S1 (1), hopped (6), $B\bar B$ (4), antivac (1).
- **Effective Krylov dimension** from S3 at P-A: $\beta_{27}\approx10^{-6}$, so about 27–28 of the 38 sector states are reached (test `test_krylov_dimension_window_PA` asserts $\beta_{27}<10^{-3}$).

### 2.4 Named states and bare energies
| state | content | links at $j=\tfrac12$ | $N(v_0..v_3)$ | bare energy above $\Omega_0$ |
|---|---|---|---|---|
| S3 | stretched string | $l_1,l_2,l_3$ | (1,1,0,2) | $2\mu+9/4$ |
| S1 | short string | $l_a$ | (1,1,0,2) | $2\mu+3/4$ |
| MM | two mesons | $(l_1,l_3)$ or $(l_a,l_2)$ | (1,1,1,1) | $4\mu+3/2$ |
| $B\bar B$ | baryon–antibaryon | none | one even $N=2$, one odd $N=0$ | $4\mu$ |
| Loop | closed flux loop | all four | (0,2,0,2) | $3$ |
| $\Omega_0$ | bare vacuum | none | (0,2,0,2) | $0$ |
| antivac | (test asserts $8\mu$) | – | – | $8\mu$ |

Three degeneracies (S3 with MM, S1 with $B\bar B$, S3 with Loop) coincide at $\mu^*=3/8$.
Hand check: $\alpha_0=\langle S3|H|S3\rangle=3\cdot\tfrac34+\mu(1-1+0-2)=1.5$ at $\mu=3/8$; the computed value is 1.5 (`crosscheck_su2qc.json`).

### 2.5 Dynamics tables (MEASURED; recomputed in this report by `physics_curves.py`, Appendix A, and equal to the plan's quoted numbers)
- **$g_E=1$, $\mu=3/8$ from S3:** $P_{\text{baryonic}}(t=1,2,3)=0.43185,\,0.73219,\,0.82096$; $P_{\text{meson}}(1,2,3)=0.037,\,0.028,\,0.034$; $P_{S1}(1,2,3)=0.0099,\,0.0073,\,0.0104$; $C_{\text{string}}(3)=0.23824$. The plan quotes $0.432/0.732/0.821$, $P_{\text{meson}}<0.04$, $P_{S1}<0.02$ (as maxima over the curve; I computed only $t=1,2,3$), $C_{\text{string}}(3)=0.238$. This reproduces the project's earlier physics notes to three digits (test `test_dynamics_reproduce_preliminary_expectation`). ($C_{\text{string}}$ is the string correlator observable of the 18; its exact definition is in `physics/observables.py`, not re-derived here.)
- **P-A from S3 at the hardware times** (full tables in §9, P11a):

| $t$ ($1/g_E$) | 0.375 | 0.75 | 1.5 | 3.0 |
|---|---|---|---|---|
| $P_{S3}$ | 0.96928 | 0.88382 | 0.62184 | 0.18293 |
| $P_{\text{meson}}$ | 0.0041726 | 0.014368 | 0.034185 | 0.046364 |
| $P_{\text{baryonic}}$ | 0.021598 | 0.082077 | 0.26955 | 0.57906 |
| $C_{\text{string}}$ | 0.74412 | 0.72675 | 0.66173 | 0.44802 |

- **Mass dependence (why the data use two coupling families).**
  - On-family ($g_E=2$): breaking fraction at $t=3$ for $\mu=0.15,0.25,0.375,0.5,0.65$ is $0.62791,\,0.63513,\,0.62542,\,0.59589,\,0.53109$ (P11c). The plan says it "falls monotonically 0.628 to 0.531"; the end points agree but the sequence is **not monotone** (0.635 at $\mu=0.25$ exceeds 0.628 at $\mu=0.15$). There is no resonance peak.
  - Strong coupling ($c_H=0.02$): sharp resonance at $\mu^*=3/8$ (P11d); at $t=33.3$ the breaking fraction is 0.554 at $\mu=0.375$ against 0.0715 at 0.30 and 0.0676 at 0.45.
- **Truncation error** ($j_{\max}=1$ versus $\tfrac12$, P-A window; quoted from plan §3, App. B, not re-derived): $|\Delta P_{S3}|\le0.053$, $|\Delta P_{\text{meson}}|\le0.060$, $|\Delta P_{\text{baryonic}}|\le0.014$, $|\Delta C_{\text{string}}|\le0.034$. An error-budget line.

### 2.6 Cross-check against the project's independent verified code (M1; `evidence/J0_data/crosscheck_su2qc.json`, status PASS, tolerance $10^{-10}$, commit `0bb5d6d`)
This package's physics core ("route C") was compared with the earlier verified `su2qc` code (its routes 1 and 2, source from SU2ZX git head `0bfa96d`) at P-A and P-S. Maximum absolute deviations (all values read from the JSON):

| quantity | P-A route 1 | P-A route 2 | P-S route 1 | P-S route 2 |
|---|---|---|---|---|
| 82 diagonal energies | 0 | $4.4\times10^{-16}$ | 0 | $4.4\times10^{-16}$ |
| full spectrum | $6.2\times10^{-15}$ | $6.2\times10^{-15}$ | $8.2\times10^{-15}$ | $5.3\times10^{-15}$ |
| $N=4$ block (after sign gauge) | $5.6\times10^{-17}$ | $4.4\times10^{-16}$ | $1.2\times10^{-16}$ | $4.4\times10^{-16}$ |
| full $82\times82$ matrix (after sign gauge) | $5.6\times10^{-17}$ | $4.4\times10^{-16}$ | $1.2\times10^{-16}$ | $4.4\times10^{-16}$ |
| basis states with opposite sign convention | 8 | 24 | 8 | 24 |
| sector populations from S3, 12 times | $1.1\times10^{-15}$ | $2.7\times10^{-15}$ | $3.9\times10^{-14}$ | $2.7\times10^{-14}$ |
| observables from S3 | $2.1\times10^{-15}$ | $3.0\times10^{-15}$ | $7.3\times10^{-14}$ | $5.9\times10^{-14}$ |
| Lanczos $\alpha_k$, $k<12$ | $1.3\times10^{-15}$ | $1.3\times10^{-15}$ | $5.8\times10^{-15}$ | $2.7\times10^{-15}$ |
| Lanczos $\beta_k$, $k<12$ | $6.7\times10^{-16}$ | $1.1\times10^{-15}$ | $1.7\times10^{-15}$ | $6.9\times10^{-15}$ |
| native `su2qc` build, P-A only | $5.6\times10^{-17}$ | $4.4\times10^{-16}$ | – | – |
| term-extraction residual on a 5th, independent build | $1.1\times10^{-16}$ | $8.9\times10^{-16}$ | same | same |

The largest deviation anywhere is $7.3\times10^{-14}$ (P-S route 1, observables). The two codes therefore describe the same Hamiltonian, including at the off-family point P-S. A "sign gauge" is needed because the two codes choose opposite phases for 8 (route 1) or 24 (route 2) basis states; a diagonal $\pm1$ matrix is fixed on a spanning tree of the coupling graph and every remaining entry, including every closed loop, is then checked (so a wrong plaquette sign or Jordan–Wigner string would show). The link map route C to `su2qc` is $[0,3,2,1]$. The units differ: `su2qc` has $H=\tfrac{g^2}{2}\mathcal E+m\mathcal M+\mathcal T-\tfrac1{2g^2}\mathcal B$; route C uses $g_E=g^2/2$, $m=\mu g_E$ (`reports/009`).

**Lanczos coefficients from S3** (P-A and P-S, all 12 each) are in §9, table P11e. At P-A: $\alpha_{0..11}=(1.5,1.684,1.492,0.399,0.434,1.144,2.394,2.452,1.876,1.889,0.946,0.828)$, $\beta_{0..11}=(0.472,0.846,1.341,1.502,1.439,1.482,1.534,1.141,0.408,1.156,0.546,1.117)$.

---

## 3. The Krylov-chain (KC) hardware carrier *(label)*

**Construction.**
1. Run Lanczos from $|S3\rangle$ under $H$ restricted to the 38-state $N=4$ sector. This gives orthonormal vectors $|k\rangle$ and a tridiagonal $H_K=\sum_k\alpha_k|k\rangle\langle k|+\sum_k\beta_k(|k\rangle\langle k{+}1|+\text{h.c.})$.
2. Encode $|k\rangle$ "one-hot" on $K=12$ qubits in a line: qubit $k$ in $|1\rangle$, all others in $|0\rangle$ (single-excitation states).
3. Then $|k\rangle\langle k|\to n_k=(1-Z_k)/2$ and $|k\rangle\langle k{+}1|+\text{h.c.}\to(X_kX_{k+1}+Y_kY_{k+1})/2$. The gauge-theory evolution becomes a nearest-neighbour **XY spin chain** with site fields.

**Two circuit arms on the same qubits.**
- **KC-Trotter (label):** $e^{-iH_Kt}$ by Strang splitting; time order per step: fields/2 ($A$), even bonds/2 ($E$), odd bonds ($O$), even bonds/2, fields/2; consecutive half-layers merge. Each bond is one `XXPlusYY` gate = 2 CZ. CZ cost for $r$ steps:
$$\mathrm{CZ}(r)=2\Big[(r+1)\Big\lceil\tfrac{K-1}{2}\Big\rceil+r\Big\lfloor\tfrac{K-1}{2}\Big\rfloor\Big]$$
 which for $K=12$ gives $34,56,100,188$ for $r=1,2,4,8$ (I verified the arithmetic; the circuits' counts are asserted by `tests/test_physics.py`). Per step the incremental cost is $2(K-1)=22$ CZ. The noiseless reference is simulated exactly inside the sector with $K\times K$ matrices.
- **KC-prep (label):** prepares $\sum_kc_k(t)|k\rangle$ directly with $K-1=11$ `XXPlusYY` rotations plus one $R_z$ layer (22 CZ, two-qubit depth 22). No depth ladder; the control arm and the analogue of Sufian's "playback" arm.

**Excitation flag.** Both arms conserve the number of excited qubits. A Z-basis shot with $\ne1$ excited qubit is a *detected error*; it is discarded and counted (an *encoding* flag, not a gauge-violation flag).

**Measurement settings.** Z (populations $|c_k|^2$ plus the flag) and X (real coherences $\langle X_kX_{k'}\rangle=2\,\mathrm{Re}\,\rho_{kk'}$). Because $H_K$ and the start vector are real, every physical observable $O$ has a real symmetric $O_K=Q_K^{\mathsf T}OQ_K$ in the Krylov basis, so $\langle O\rangle=\sum_{kk'}(O_K)_{kk'}\mathrm{Re}\,\rho_{kk'}$. A Y setting is an optional cross-check. Renormalising coherences by the single-excitation fraction $p_1$ is a mitigation arm, reported raw and renormalised.

**Cost table at P-A** ($K=12$, $\Delta t=0.375$; synthetic Heron-like noise: CZ error $3\times10^{-3}$, readout 1–2 %, $T_1=250\,\mu$s, $T_2=150\,\mu$s). Flag rates and population errors are **EMULATED**; infidelity and CZ are computed exactly (quoted from plan §4; also in §9, P11g):

| steps $r$ | $t$ ($1/g_E$) | CZ | two-qubit depth | Strang infidelity | emulated flag rate | emulated post-selected population error |
|---|---|---|---|---|---|---|
| 1 | 0.375 | 34 | 6 | $2\times10^{-5}$ | 0.23 | 0.006 |
| 2 | 0.75 | 56 | 10 | $8\times10^{-5}$ | 0.28 | 0.011 |
| 4 | 1.5 | 100 | 18 | $3\times10^{-4}$ | 0.38 | 0.020 |
| 8 | 3.0 | 188 | 34 | $1.2\times10^{-3}$ | 0.55 | 0.016 |

- **Krylov truncation.** $K=12$ reproduces observables over $t\le3/g_E$ to $1.1\times10^{-4}$ (plan); J0 row D4 measured $1.05\times10^{-4}$. $K=11$ suffices for $10^{-3}$, $K=9$ for $10^{-2}$ (plan). $K=12$ also covers on-family $g_E\ge1.3$ to $10^{-3}$ ($g_E=1$ needs $K=13$).
- **Circuit correctness.** Circuits equal the in-sector unitary to $10^{-15}$ (Lie and Strang, $K\le6$ against `Statevector`; $K=12$ via transpiled CZ counts); KC-prep exact to $10^{-15}$. The X/Y sequential sampler has total-variation distance 0.007 to the brute-force distribution at $2\times10^5$ shots ($K=6$) (plan App. B.4).
- **Strong coupling.** At $c_H=0.02$ the chain fields are $O(1)$ while the physics is slow, so Trotterising needs hundreds of steps. The hardware arm there is KC-prep only, at $t\in\{10,15,20\}/g_E$ ($K=12$ reproduces the dynamics to $10^{-3}$; $K=11$ suffices at $t=20.8$).
- **Routing.** A dry run against IBM's simulated `FakeTorino` chose a 12-qubit line with zero routing overhead (counts 34/56/100/188 preserved).
- **What it is not.** The Krylov basis is computed classically, so this is a testbed with known truth and controllable depth. It is not a computation beyond classical reach.

---

## 4. The world model (JEPA)

### 4.1 Observation, actions, training rule
- **Observation vector** (`data/records.py: ObservationSpec`, dimension 24, frozen): 18 physical observables: $\langle N_v\rangle$ (4), $\langle j_\ell(j_\ell{+}1)\rangle$ (4), $P_{\text{pair}},P_{\text{meson}},P_{\text{baryonic}},P_{\text{vacmatter}},P_{S3},P_{S1},P_{\text{hopped}},P_{B\bar B},P_{\text{antivac}}$, $C_{\text{string}}$; plus the flag rate (1); a source one-hot (exact / twin / hardware, 3); a carrier one-hot (diagonal / chain, 2). All 18 observables are diagonal in the configuration basis, so computational-basis measurements give them. All three sources go through the same estimator.
- **Actions:** $a_t=(\Delta t,c_M,c_H,c_B)$ (4 numbers). A mass quench changes $c_M$ mid-trajectory.
- **Training rule:** the context is the *noisy* record ($S\in\{256,512,1024,4096\}$ shots); the target is the encoding of the *clean* (exact expectation values, flag zero) record.

### 4.2 Architecture (`src/su2qc_jepa/models/jepa.py`)
- **Encoder:** observation normalised by a non-affine BatchNorm, then MLP $24\to128\to128\to d$ with LayerNorm and GELU after each hidden layer ($d=16$ by default).
- **Predictor:** action embedding MLP $4\to32\to32$; the latent initialises a GRU state via $\tanh(\text{Linear}(s))$ (128 hidden units); the GRU runs over the action tokens; output Linear$\to d$ plus a skip Linear from $s$.
- **Grounding heads:** one Linear map $d\to5$ (energy, $C_{\text{string}}$, $P_{\text{meson}}$, $P_{\text{baryonic}}$, flag); used in training and as the J1 diagnostic.
- **Parameter count** (counted in code, 5 Oct; given by the coordinating session): **90,309 trainable** = encoder 22,288 + predictor 67,936 + grounding 85. Latent 32: 97,349. The EMA target copy adds 22,288 non-trained parameters. (The plan's "$\sim0.2$ M" was an overestimate.)

### 4.3 Losses
Total loss
$$\mathcal L=w_{\text{pred}}\mathcal L_{\text{pred}}+w_{\text{sigreg}}\mathcal L_{\text{sigreg}}+w_{\text{ground}}\mathcal L_{\text{ground}}+w_{\text{semigroup}}\mathcal L_{\text{semigroup}}.$$
- $\mathcal L_{\text{pred}}$: mean over horizons $k\in\{1,2,4,8\}$ of the mean-squared error between the predictor's latent after $k$ actions, started from the noisy context latent $s_t$, and the target latent at $t+k$ (the clean latent from the online encoder, or from the EMA encoder with stop-gradient if EMA is on).
- $\mathcal L_{\text{sigreg}}$: SIGReg, the Epps–Pulley statistic on 64 random unit projections, $t$-grid of 17 points in $[-3,3]$, weight $e^{-t^2/2}$, applied to the context and clean latents together (to the context latents only when EMA is on).
- $\mathcal L_{\text{ground}}$: MSE of the grounding head against the true (energy, $C_{\text{string}}$, $P_{\text{meson}}$, $P_{\text{baryonic}}$, flag), on both the clean and the context latents.
- $\mathcal L_{\text{semigroup}}$: MSE between $P(s,[a_t,a_{t+1}])$ and $P(P(s,[a_t]),[a_{t+1}])$ on random consecutive action pairs.

**Defaults:** $w_{\text{pred}}=1$, $w_{\text{sigreg}}=0.5$ (the training script's default; the class default is 0.05), $w_{\text{ground}}=1$, $w_{\text{semigroup}}=0.1$. Optimiser AdamW, learning rate $2\times10^{-3}$, weight decay $10^{-5}$, batch size 64, cosine learning-rate schedule over the epochs, gradient-norm clipping 1.0. EMA decay $\tau=0.996$ when used. The per-epoch loss entries in `history.json` are the **unweighted** terms averaged over the epoch's batches (`total` is the weighted sum); the diagnostics are computed on the validation split.

**Diagnostics logged each epoch** (validation split, `models/train.py: diagnostics`): `eff_rank` (of the clean-observation latents), `ground_r2` (list of 5: energy, $C_{\text{string}}$, $P_{\text{meson}}$, $P_{\text{baryonic}}$, flag; the flag entry is NaN because the flag target, taken from the context record, is constant zero in this diagonal-carrier dataset, so $R^2$ is undefined), `semigroup_resid` (relative squared mismatch on the noisy-context latents), `isotropy`.

**Readout for forecasting:** a ridge probe (penalty $10^{-3}$) from clean latents to observables, fit on the training split.

**Options added on 5 Oct (commit `0a76800`):** EMA target encoder (`ema_target`, SIGReg on the context only); horizon curriculum (`curriculum_epochs`, first epochs use horizons $\{1,2\}$ only); `--w-ground`; spawned training seeds (§7). Added later (commit `ade81b0`): `--w-semigroup`.

### 4.4 Baselines, tasks
**Baselines** (same inputs: noisy records up to the context step plus all actions): ridge regression; an autoregressive one-step MLP rolled out in observation space; a direct supervised MLP. Each also has a masked-coupling variant. Training epochs for the baselines: 100 (`args.json: baseline_epochs`).

**Tasks:**
1. **Forecasting** (gate J2): from the noisy record at context step $c=4$, predict $P_{\text{baryonic}}$, $P_{\text{meson}}$, $C_{\text{string}}$ at $+4$ and $+8$ steps on held-out couplings, with 512 context shots.
2. **Masked-coupling identification (label):** the same with $(c_M,c_H,c_B)$ zeroed in the actions; the model must infer the couplings from the early record.
3. **Label-free error signal** (gate J3): `jepa_twin` = latent distance between a hardware record and the twin's record; `jepa_self` = distance between the measured deep record and the prediction propagated from the shallowest record of the same series; `jepa_t0` = prediction from the exact initial record; baselines `raw_twin` (observation-space distance) and `flag_rate`. Scored against the exact error at full shots and at 512/256 shots by exact subsampling of stored counts.
4. **Depth extrapolation on hardware (H4):** forecast the $t=3/g_E$ observables from the $r=1,2$ records and compare with the direct $r=8$ estimate.
5. **$\mu^*$ from held-out data (H5):** fit the resonance maximum of the forecast breaking fraction over $\mu$ in the strong-coupling family.

---

## 5. Data, twin, hardware plan, gates, hypotheses, error budget

### 5.1 Data (`evidence/J0_data/datasets.json`, commit `358d0bd`; checksums are sha256 of the data arrays, first 12 hex digits shown)
| dataset | family | carrier | trajectories | steps × $\Delta t$ | built on | wall time | checksum | splits train / val / held-out mass / held-out family |
|---|---|---|---|---|---|---|---|---|
| `main` | on-family + strong | diagonal | 20,000 | 8–12 × {0.125, 0.25, 0.5} (on-family) / {2, 4, 8} (strong) | laptop | 157.7 s | `73fff8e5a7b7` | 11,539 / 2,392 / 6,069 / onfam 2,935, strong 3,134 |
| `chain_onfam` | on-family, S3 starts, no quench | chain, $K=12$ | 5,000 | 8–12 × 0.375 | laptop | 1,669.6 s | `bdcd6e895a06` | 2,859 / 741 / 1,400 / 1,400 |
| `chain_strong` | strong, S3 starts | chain, $K=24$ (exact emulation) | 3,000 | 8 × {2, 4, 8} | Perlmutter (`jobs/001`) | 789.9 s | `935692f343d8` (manifest only, not recomputable on the laptop) | 1,897 / 276 / 827 / 827 |

- Full checksums: `main` `73fff8e5a7b7f670b26056a000b4d50d13db79499a7467f36b15c69f66539828`; `chain_onfam` `bdcd6e895a06ca28ea107bfe374be1b44bbfabe3398780b9f903b788d352e1ac`; `chain_strong` `935692f343d89895f5e93c232ec1b7bef470a1c3d638fcbb813364914e60cd59`.
- Dimensions: observation 24, maximum trajectory length $T=12$ steps; master seed 20261005 for all three.
- **Grids.** On-family: $g_E\in\{1.0,1.15,1.3,1.45,1.6,1.75,2.0\}$, held out **1.3, 1.75**, validation 1.45; $\mu\in\{0.15,0.25,0.375,0.5,0.65\}$. Strong coupling: $\mu\in\{0.15,0.2,0.25,0.3,0.33,0.375,0.42,0.45,0.5,0.575,0.65\}$, held out **0.3, 0.42, 0.5**, validation 0.45. Starts: S3 ×3, S1, random $N=4$ superposition. Quench fraction 0.2 (`chain_*`: none).
- **Splits** are made by rule (by coupling label), never by row, and J0 row D6 checks zero leakage. "Held-out family" sets are subsets of "held-out mass", which is why the counts do not add up to the totals. The J1 gate and the plots below use the **validation** split (2,392 trajectories of `main`; 26,348 valid rows in the ceiling analysis).
- **Dataset-build command** (from the job files): `python scripts/make_dataset.py --name main --n-traj 20000 --steps 8 12 --families onfam strong --carrier diagonal --starts S3 S3 S3 S1 random --quench-fraction 0.2 --seed 20261005 --out data/main`.
- Samplers: for the diagonal carrier the exact source emulates the measurement by multinomial sampling over the configuration basis; for the chain carrier by exact sequential sampling of Z- and X-basis bitstrings (closed-form conditional sampler).
- A planned stretch dataset `ladder` (2,000 trajectories, plan §6) has **not** been built. A small `gpu_smoke` dataset (400 trajectories, same command with `--n-traj 400`; checksum laptop `585e1d0013d1`, Perlmutter `eb294d7db29f`) exists for GPU checks only.

### 5.2 The digital twin
- Qiskit Aer density-matrix simulation of the 12-qubit chain circuits: 268 MB per state; 6–30 s per circuit on 2 CPU cores. A full hardware day of twin runs is about 480 circuits, so full campaigns run on Perlmutter and pilot-size runs (up to about 100 circuits) on the laptop.
- Noise: a synthetic Heron-like model for development; for each hardware day a model built from that day's calibration (`NoiseModel.from_backend`) on the laptop, saved to a file and committed (the IBM token never leaves the laptop). The twin is "calibrated, not trusted": J3 measures how far it is from the device. "Arm B" on the twin is a degraded noise model (2× CZ error, 2× readout error).
- Seeds: `SeedSequence(master).spawn`, one per circuit; twin repeats are checked distinct (J0 row D5, measured 5/5 distinct, $\sigma(p_1)=0.0147$).
- Known limitation (`reports/008`): there is no GPU Aer on Perlmutter (`qiskit-aer` 0.17.2 overrides `qiskit-aer-gpu` 0.15.1), so twin runs there are CPU only.
- **Status: the calibrated twin and the twin campaign are NOT RUN (M3).** Synthetic-noise rehearsal numbers at smoke scale (plan App. B.6: $K=8$, 24 points; `jepa_twin` AUROC 1.0 versus `raw_twin` 0.70 with an untuned v0 model) are EMULATED and not meaningful for J3.

### 5.3 Hardware plan and rules (nothing submitted)
- **Access assumption:** IBM Quantum Open Plan, 10 QPU-minutes per 28-day rolling window (plus an optional extra 180 minutes per 12 months announced March 2026; `CLAUDE.md` §4 states 600 s per 28 days); Heron r2 devices (`ibm_torino` class). Two windows (late Oct, Nov) give about 20 minutes without paying. Pay-as-you-go is \$96 per QPU-minute (fallback for one extra day, not a plan). IonQ or any paid provider: never, unless the session prompt contains "paid provider approved by Digonto" (Braket IonQ Forte: \$0.30 per task + \$0.08 per shot; about \$8k for 100 tasks × 1,000 shots, about \$20k with mitigation; plan App. B.8, external facts checked 1 Oct 2026).
- **Per calibration day (full design, plan §8):**

| family | arm | points | settings | circuits | shots |
|---|---|---|---|---|---|
| on-family $g_E\in\{1.3,1.75,2.0\}$, $\mu=3/8$ | KC-Trotter $r\in\{1,2,4,8\}$ | 12 | Z, X | 24 | 4,000 |
| on-family | KC-prep at the same four times | 12 | Z, X | 24 | 4,000 |
| strong $\mu\in\{0.3,0.375,0.42,0.5\}$ | KC-prep $t\in\{10,15,20\}/g_E$ | 12 | Z, X | 24 | 4,000 |
| all | mitigation arm B (dynamical decoupling + gate twirling) | – | – | 72 | 4,000 |

 144 circuits × 4,000 shots = 576,000 shots; at the prior rate of 2,000 shots/s this is 4.8 min plus about 0.5 min overhead, about 5 QPU-min per day; three days about 15 min. **Minimum design** (fits 10 min plus pilot): drop KC-prep on-family and arm B on the strong family: 72 circuits, about 2.5 min per day. The 2,000 shots/s is a prior (`shots_per_second_prior` in `STATE.json`), not a measurement.
- **Pilot (M4b):** 12 circuits (on-family $g_E=2$, $r\in\{1,8\}$ × KC-Trotter/KC-prep × Z/X), 4,000 shots, arm A, one job; expected QPU time 40–90 s, flag rates 0.2–0.6, post-selected populations within 0.03 of ideal at $r=1$ (all PROPOSED).
- **Discipline, enforced in code** (`src/su2qc_jepa/hardware/ibm.py: check_budget`): (1) a dry-run manifest with circuit hashes (`scripts/hw_dry_run.py`); (2) a **human** edits `configs/hardware_budget.yaml` (`approved: true`, the manifest hash, caps); (3) `scripts/hw_submit.py submit --confirm` re-checks hashes, job cap, CZ cap and the QPU ledger, snapshots calibration, submits **one** job; (4) `collect` writes immutable raw counts (`evidence/hardware/jobs/<id>.raw.json`). Claude never edits `approved`, `approved_by`, `approved_utc` or `manifest_hash`. One job per approval. For each job record: job id, backend, qubit line, calibration snapshot, options (DD, twirling), shots, measured QPU seconds, circuit hashes. Pilot caps in `prompts/004`: max 90 QPU-s, 1 job, at most 200 CZ per circuit, 4,000 shots. A "day" is defined by the calibration snapshot hash, not the date.
- **Cross-backend day** (replaces IonQ): the on-family block on a second Open-plan Heron QPU on the same day.
- **Budget spent so far:** 0 QPU-seconds; no job ever submitted; `STATE.json: hardware.jobs = []`, `backend = null`. (The file `evidence/hardware/QPU_LEDGER.json` does not yet exist; `ls evidence` shows no `hardware` folder.)

### 5.4 Gates (current thresholds, `configs/gates.yaml`)
Gate scripts (`scripts/run_gate.py`) are the only arbiters and append to `evidence/GATE_LEDGER.md`. The file is **not yet frozen**; it is frozen at preregistration (M2b).

| gate | when (plan) | rows and thresholds |
|---|---|---|
| **J0 data** | 11 Oct (done 3 Oct, PASS) | state counts 82; 2/20/38/20/2; 16/16/18/16/16; two routes $\le10^{-12}$; Gauss commutator $\le10^{-12}$; estimator bias $\le4.0$ standard errors (200 trials, 1,024 shots; diagonal and chain carriers); Krylov $K=12$ reproduces the P-A window to $10^{-3}$; 5 distinct twin repeats; split leakage 0; checksum recorded |
| **J1 training** | 18 Oct | 5 seeds; no NaN; effective rank $\ge8.0$ (of 16); grounding $R^2\ge$ **0.887** (energy; `decisions/005`), 0.99 ($C_{\text{string}}$), 0.95 ($P_{\text{meson}}$), 0.98 ($P_{\text{baryonic}}$); semigroup residual $<10^{-3}$ |
| **J2 forecast** | 30 Oct | context step 4, 512 context shots, targets $P_{\text{baryonic}},P_{\text{meson}},C_{\text{string}}$, scored 4 and 8 steps after the context; JEPA MAE $\le0.05$ on the held-out split of each family; JEPA MAE $\le1.1\times$ the baseline MAE counts as "not worse"; must be so against ridge and autoregressive on at least 2 of 3 targets (per horizon); masked-coupling task also evaluated |
| **J3 hardware** | 13 Nov | at least 24 points; Spearman(`jepa_twin`, exact error) $\ge0.7$ at the 512-shot level; `jepa_twin` Spearman $\ge$ `raw_twin` Spearman $-0.05$; AUROC $\ge0.8$ (degraded arm/day versus nominal); 3 calibration days; must report `raw_twin`, `flag_rate`, `jepa_self`, `jepa_t0` |
| **J4 quantum encoder** | week 7, optional | trains at 12 qubits; matched-shot test preregistered |

Note on the J1 energy row: the plan, `docs/CLAIMS.md` and `prompts/010` still mention 0.99 in places; `decisions/005` and `configs/gates.yaml` (0.887) rule.

### 5.5 Preregistered hypotheses H1–H5 (plan §11, `docs/PREREGISTRATION.md` draft)
- **H1 (no collapse):** effective rank $\ge8/16$ and the grounding rows of J1 (energy 0.887, $C_{\text{string}}$ 0.99, $P_{\text{meson}}$ 0.95, $P_{\text{baryonic}}$ 0.98), semigroup residual $<10^{-3}$, 5 seeds. *Expected in the plan: met after the ablation ladder.* Current status: see §8.3 (not met on the semigroup row).
- **H2 (forecasting):** MAE $\le0.05$ at $+8$ steps on both held-out families; not worse than ridge or autoregressive within $1.1\times$ on at least 2 of 3 targets. Expected: parity, not superiority; a possible advantage on the masked-coupling task.
- **H3 (label-free error signal):** at 512 shots `jepa_twin` is non-inferior to `raw_twin` in rank correlation with the exact error (margin 0.05) and separates mitigation arms with AUROC $\ge0.8$. Expected: non-inferior at low shots, a tie at 4,000.
- **H4 (depth extrapolation on hardware):** the forecast of $t=3/g_E$ from $r\le2$ records beats the direct $r=8$ estimate on at least 2 of 3 targets at every $g_E$. Expected: by a factor 2–5.
- **H5 (resonance from hardware):** the $\mu^*$ estimate from the strong-coupling KC-prep points lies within 0.05 of $3/8$. Expected: yes (four masses bracket the resonance).

**Exclusion rules (draft):** hardware points with flag rate above 0.8 are excluded and listed; a job whose calibration snapshot differs from the twin's is a new "day"; no post-hoc change of shot levels, targets or evaluation steps.

### 5.6 Error budget (lines, each to be measured; plan §12)
| line | size (P-A window) | where measured | status |
|---|---|---|---|
| truncation $j_{\max}=\tfrac12$ | $\le0.06$ ($P_{\text{meson}}$), $\le0.014$ ($P_{\text{baryonic}}$) | plan App. B.3 (quoted) | MEASURED (plan session), not re-derived here |
| Krylov $K=12$ | $\le1.1\times10^{-4}$ | J0 row D4: $1.05\times10^{-4}$ | MEASURED |
| Trotter (Strang, $\Delta t=0.375$) | infidelity $\le1.2\times10^{-3}$ at $r=8$ | `trotter_error` | MEASURED (plan) |
| shot noise (4,000 shots, Z+X) | about 0.01–0.02 on chain estimates | J0 row D3 (bias test only) | partly MEASURED |
| device (post-selected) | to be measured | pilot, W4 | NOT RUN |
| twin mismatch | `raw_twin` | J3 | NOT RUN |
| model forecast | J2 | W4 | NOT RUN |

---

## 6. Compute and repository infrastructure

### 6.1 Compute (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`)
Two machines only. The **laptop** (Dell G7 7588, 64 GB RAM, i7-8750H with 6 cores / 12 threads, GTX 1060 Max-Q not used because current PyTorch has no kernels for its Pascal architecture, compute capability 6.1) runs Claude Code and light work, and is **shared with other Claude sessions**, whose protection comes first. **NERSC Perlmutter** (A100 GPU nodes; account `m4135_g`; environment `/global/common/software/m4135/su2qc-jepa-env`) runs everything heavy. Laptop conda environment `su2qc-jepa`: Python 3.12.14, torch 2.14.1+cpu, qiskit 2.5.2, qiskit-aer 0.17.2, graphifyy 0.9.74 (quoted from `reports/006`).

**One entry point for all computation: `python scripts/run.py -- <command>`** (`src/su2qc_jepa/localrun.py`):
1. **Classify.** A GPU requirement, or an estimated laptop time above 20 minutes, means always Perlmutter: the runner writes the numbered job `jobs/NNN_*.yaml` (with a step that rebuilds the dataset there from the same seed) and, with `--push`, commits and pushes it. (The estimate comes from unit costs measured 2 Oct on 2 cores and ignores the carrier: chain datasets ran 56× and 137× longer than estimated.)
2. **Admit.** A light job runs only if at least 16 GB of memory stay available, the load plus the job's threads leaves 2 logical CPUs free, and no other su2qc computation runs (a kernel file lock across sessions). Otherwise it waits up to 20 minutes, then is sent to Perlmutter; a command that cannot be queued is not run (exit 2).
3. **Cap.** nice 19, idle I/O priority, 2 threads by default (4 maximum), memory ceiling 4 GB by default (16 GB maximum; cgroup limit through `systemd-run`, otherwise an address-space limit), time limit, and `oom_score_adj = 1000` so the kernel kills this job before any other session's.
4. **Heal.** After a memory kill: one retry with twice the memory if there is room, else Perlmutter. A timeout goes to Perlmutter. A program error is never retried.
Exit codes: 0 done here, 10 queued, 1 failed, 2 not run. Ledger `.local_runs/ledger.jsonl`; logs `.local_runs/logs/`.

**The Perlmutter job queue (pull-based).** A worker started by `scrontab` every 15 minutes pulls `main`, submits new jobs with Slurm (`shared` queue, one A100 = ¼ node-hour per hour), polls running ones, and pushes `status.json`, a log tail and declared outputs (at most 50 MB; `.npz` never) to the separate `results` branch. It resubmits automatically after TIMEOUT (twice the time, cap 48 h), OUT_OF_MEMORY (twice the GPUs), NODE_FAIL/PREEMPTED/BOOT_FAIL/LOST (3 attempts at most). It runs only commits on `main`, only allowlisted scripts (never the IBM submission), never pushes to `main`, stops at 50 node-hours, and writes a heartbeat. The laptop reads with `scripts/jobs/status.py` and `scripts/jobs/fetch.py NNN`. The laptop never connects to Perlmutter, and no NERSC or IBM credentials are handled by agents.

**Device and seeds.** Code calls `su2qc_jepa.compute.pick_device()` (CPU on the laptop, CUDA on Perlmutter; `SU2QC_DEVICE` overrides). Every stochastic step derives its seed from `numpy.random.SeedSequence` with a recorded master seed (20261005); adjacent integer seeds are forbidden (that bug voided the v0.5.0 error bars). Training seeds (spawned from the master seed): 462709266, 3658436304, 2224198422, 672449321, 2231613345 (`runs/*/args.json`).

**Measured laptop costs (2 cores)** (`decisions/004`): tests 34 s / 0.9 GB; J0 gate 10 s / 0.2 GB; 20,000-trajectory dataset 87 s / 0.2 GB; training check 46 s / 1.2 GB; one 12-qubit twin circuit 51 s / 0.5 GB. **Perlmutter training speed** (from jobs): about 1.0 h of Slurm time (0.25 node-hours) for five 200-epoch runs of one rung; earlier estimate 3.8 s per epoch on the A100 versus 17.5 s per epoch on 2 laptop threads (`reports/011`).

**Whole-plan Perlmutter estimate:** 15–40 node-hours, capped at 50. **Used so far: 1.898 node-hours** (`python scripts/jobs/status.py` at 05:00 UTC heartbeat, 6 Oct; equals the sum of `node_hours` in `evidence/jobs/*/status.json`; jobs 008, 011, 012 not yet counted).

### 6.2 Repository and conventions
- **Artifacts** (`decisions/001`): plans, prompts, reports, decisions, figures and jobs are numbered, append-only files `NNN_<slug>.<ext>` created only by `scripts/new_artifact.py` (front matter `id,title,series,created_utc,author,milestone,status,supersedes,superseded_by`), checked by `scripts/check_artifacts.py` (names, gaps, front matter, cross-references, index freshness). Living documents (`README.md`, `CLAUDE.md`, `docs/*`, `configs/*`, `STATE.json`) are edited in place. Machine records under `evidence/` are immutable and UTC-stamped.
- **Session protocol** (`CLAUDE.md` §2): env check; code-graph freshness check; tests; work; tests and gate; graph refresh; numbered report; artifact check; `STATE.json`; scoped commits with prefixes `physics:`, `data:`, `model:`, `twin:`, `hw:`, `gate:`, `docs:`, `chore:`, the graph refresh last. History is never rewritten. Stop conditions: a physics fingerprint test fails; two routes disagree above $10^{-12}$; a gate threshold would have to change to pass; the hardware budget file does not approve the manifest; 8 hours of wall time.
- **Frozen things** (change needs a `decisions/` record and a new tag): `physics/conventions.py`; `configs/gates.yaml` after the tag `prereg-2026-10-16`; the observation layout; dataset checksums recorded in `evidence/J0_data/`; artifact and graph conventions, and the pinned `graphifyy`. (No git tags exist yet: `git tag` is empty.)
- **Code graph** (Graphify, code-only, `PYTHONHASHSEED=0`): `evidence/graph/stats.json` at commit `ade81b0`: 976 nodes, 1,853 edges, 93 communities, 117 files. Highest-degree nodes: `PlaquetteModel` (42), `trajectories.py` (38), `j0_data.py` (33), `localrun.py` (33), `train.py` (27), `chain.py` (26). History of the graph: M0 842/1,615/64; start of M2a 893/1,697/64; after M2a code 931/1,775/80. A code graph is navigation, not review; it is never evidence that code is correct. I did not change code, so no graph update was run for this report.
- **Tests:** 54 fast tests passed at the end of the M2a session (`reports/010`). Since then a test was added (`test_training_and_baselines_run_on_device`, CPU case runs everywhere, CUDA case only where a GPU exists), others in `tests/test_pipeline.py` and `tests/test_jobs.py` (commits `ade81b0`, `3010090`). The latest logged pytest runs in `.local_runs/logs/` (5 Oct, 22:54 UTC) printed 11 dots in one file and one failure of `test_committed_graph_is_fresh` in an earlier one (a stale committed graph; presumably fixed by the next graph-refresh commit, which I did not verify). A full-suite count after the last commit is **not recorded** (I was told not to run the suite).
- **CI:** GitHub Actions run 37069894565 (success) on the bootstrap commit: lint, artifact conventions, tests, graph freshness, physics fingerprints (`reports/007`). Later CI results are not recorded in the sources I read.

---

## 7. Chronological history (every session so far, with the numbers)

The repository has 51 commits, from `88dc52d` (2 Oct 2026, 15:57 -0600) to `80d7fdf` (5 Oct 2026, 23:34 -0600); the full list is in Appendix C.

### 7.1 Before the repository existed (1–2 Oct; planner sessions; reports 000–005)
- **`reports/000` (1 Oct) — audit of the 1 Oct plan and the starter package.** 15 problems, 5 of them severe: (1) the old hardware design (Krylov "playback") had no depth ladder; (2) no label-free baselines, so a Spearman test on the residual was trivially satisfiable (the raw twin residual had Spearman 0.997 with the exact error); (3) forecasting baselines were guessed (ridge already reached 0.02–0.04 MAE at held-out masses because the dynamics barely depend on the mass at P-A); (4) the resonance claim was untestable at $g_E=2$; (5) the IBM budget was misjudged (the Open Plan gives 10 QPU-minutes per 28 days). Fixes: the v2 plan (Krylov-chain carrier, two coupling families, label-free baselines, an IBM budget of about 8–13 minutes, IonQ out of the critical path, the quantum encoder moved to an optional week-7 item). The starter package implemented the physics core, carrier, estimators, dataset generator, JEPA, baselines, twin, hardware guard, gates J0–J3 and CI. At smoke scale J0 passed in full mode and the whole pipeline ran end to end in about 1 minute; the v0 JEPA was not yet healthy (effective rank 4–6 of 16; grounding $R^2$ 0.81–0.99).
- **`reports/001` (2 Oct) — numbered artifacts and the Graphify code graph** (`decisions/001`). 26 tests passed.
- **`reports/002`–`004` (2 Oct) — compute.** The RTX 3070 desktop was dropped; the project settled on laptop plus Perlmutter, with a GitHub job queue and an admission-controlled laptop runner (`decisions/002` → `003` → `004`). Bugs found on the way: a `data/` ignore pattern that also hid the package folder `src/su2qc_jepa/data/`; a cgroup memory limit that was not enforced; a job that could outlive its runner; a ledger mislabel. The runner self-healing was tested (a 0.5 GB attempt failed, the retry with 1 GB succeeded; a TIMEOUT was resubmitted with twice the time using stand-in `sbatch`/`sacct`).
- **`reports/005` (2 Oct):** the worker install merges into Digonto's existing scrontab and keeps the two other repositories' entries byte for byte.

### 7.2 Environment and M0 (2 Oct; reports 006–008)
- **`reports/006` — laptop environments.** The `coding` conda environment, broken by a CUDA-13 PyTorch install, was repaired (`cuda-bindings` 13.4.3 → 12.9.9; 16 CUDA-13 packages and torch/triton/graphify removed; `pip check` clean; 14 GB → 8.3 GB). The separate `su2qc-jepa` environment was created (Python 3.12.14, torch 2.14.1+cpu, qiskit 2.5.2, qiskit-aer 0.17.2, graphifyy 0.9.74; 47 tests passed).
- **`reports/007` — M0 PASS.** Public repository created, bootstrap commit `88dc52d`, CI run 37069894565 green, 47/47 tests, code graph 842 nodes / 1,615 edges / 64 communities.
- **`reports/008` — Perlmutter worker installed.** Smoke test `jobs/000`: Slurm id 59236367 on an NVIDIA A100-SXM4-40GB, `torch_device_used: cuda`, COMPLETED, 0.011 h, 0.003 node-hours. Problems recorded: `fetch.py` can overwrite tracked files (fixed 5 Oct, `3010090`); no GPU Aer on Perlmutter.

### 7.3 M1 — physics cross-check, datasets, gate J0 (3–4 Oct; `reports/009`) — J0 PASS (9 of 9 rows)
- Cross-check against `su2qc`: PASS, maximum deviation $7.3\times10^{-14}$ (§2.6).
- Datasets built (§5.1). `chain_strong` was too slow for the laptop (0.82 s per trajectory, about 41 min) and ran on Perlmutter (`jobs/001`, Slurm 59281851, 0.223 h, 0.056 node-hours).
- Gate J0 on `data/main` (`evidence/J0_data/20261003T201012Z.json`, 15 s): see §8.1.
- Problems noted: the runner's time estimate ignores the carrier (56× and 137× underestimates); plan says estimator bias $\le2.5$ standard errors but the config says 4.0 (both measured values, 2.36 and 1.44, meet 2.5); a false "worker stopped" warning (an idle worker only heartbeats every 12 h).

### 7.4 M2a — model health (5 Oct; `reports/010`, `decisions/005`)
1. **Code** (commit `0a76800`): EMA target encoder, horizon curriculum, `--w-ground`, spawned training seeds. The old seeds were the integers 0–4 with shuffle seed $s+e$, so seed 0 epoch 1 had the same batch order as seed 1 epoch 0; this is forbidden by `CLAUDE.md` §5 and fixed. Test `test_jepa_ema_target_and_curriculum` added.
2. **Laptop check** (`runs/v1_check`, 10 epochs, 1 seed, 2 threads): no NaN; 17.5 s per epoch; 765 s in total including baselines; peak 0.98 GB. Numbers in §9, P12.
3. **Ceiling analysis** (`scripts/j1_ceiling.py`, 625 s; `evidence/J1_training/ceiling_main.json`): no regressor predicts the energy from one clean observation better than $R^2=0.9145$ (§8.2). This triggered a stop condition ("a gate threshold would have to change to pass"); Digonto chose option C, recorded as `decisions/005` (energy threshold $0.887=0.97\times0.9145$), commit `2b10e5b`.
4. **Ladder queued** on Perlmutter (jobs 002–008, §8.5), each at the code of `0a76800` with `data/main` rebuilt on Perlmutter from the manifest.

### 7.5 The 5 Oct evening and 6 Oct session (this report adds these)
1. **Baseline crash on the GPU.** Jobs 002 and 003 finished training for every seed and then crashed in the forecasting baselines. The log tail of 002, 004 and 007 shows `RuntimeError: Expected all tensors to be on the same device, but got mat1 is on cuda:0, different from other tensors on cpu`. `baseline_autoregressive` built its network on the CPU while data were on CUDA, and `baseline_supervised_mlp` had the same problem (`3fd0a65` message). It never showed on the laptop, which has no GPU. As predicted in `reports/011`, **jobs 004, 005, 006 and 007 failed in the same way** (state FAILED in `evidence/jobs/NNN/status.json`; all training outputs, `history.json` and `model.pt`, were nevertheless pushed). Consequence: for rungs 002–007 `history.json` and `model.pt` exist for every seed but there is **no `forecast_eval.json`** (the J2 input). The J1 gate does not need it.
2. **GPU fix** (commit `3fd0a65`): networks and inputs of the baselines moved to the data's device; new test `tests/test_pipeline.py::test_training_and_baselines_run_on_device` (CPU case everywhere; CUDA case only on a GPU). **Verified on Perlmutter by `jobs/009`** (data `data/gpu_smoke`, 400 trajectories, 2 epochs, masked, all baselines, `--device cuda`, commit `5000bc9`): state COMPLETED, 0.011 h, 0.003 node-hours, Slurm 59393121, log shows `device: cuda, torch threads: 32` and `forecast_eval.json` written. The two training lines show 2 epochs only; the numbers of this 2-epoch model (e.g. effective rank 5.86, energy $R^2$ 0.767) are meaningless as results.
3. **Dataset reproducibility** (`jobs/010`, new `dataset_fingerprint` in `data/trajectories.py`, `scripts/compare_fingerprints.py`, commit `ade81b0`). The Perlmutter rebuild of `data/main` has checksum `76f4c9055591` against the laptop's `73fff8e5a7b7` (and `gpu_smoke` `eb294d7db29f` against `585e1d0013d1`). The fingerprint comparison (§8.4) shows that `ctx` (the noisy model inputs including every shot sample), `act` and `valid` are bit-identical, and that `tgt` and `energy` (exact expectation values) differ only by floating-point rounding: at most $5.7\times10^{-14}$ ($tgt$) and $1.9\times10^{-13}$ (energy) per sampled value, and at most $5.7\times10^{-12}$ and $2.5\times10^{-12}$ per trajectory sum. **Meaning:** the two datasets are numerically equivalent; the checksum differs because different linear-algebra libraries round the last bits differently. (The cause is an inference from the pattern of the differences; I did not test the libraries.)
4. **`fetch.py` fix** (commit `3010090`): fetching a job never overwrites a different local file; the job's copy goes to `evidence/jobs/NNN/outputs/`.
5. **Official J1 gate** run for each of the six rungs that had finished (commits `8a80885`, `80d7fdf`; ledger rows in §8.3): all six are FAIL. The runs were fetched with `fetch.py` and the gate run once per rung on `runs/<rung>/seed0..seed4` (masked seeds excluded).
6. **Diagnosis** (the coordinating session's analysis; the correlation figure in §9, P9, is computed by my helper script): the semigroup residual (the relative mismatch between predicting two steps at once and one step twice) grows as the latent spreads out (rank up, residual up), and the semigroup loss weight is only 0.1. The masked-coupling runs keep it at about $2\times10^{-4}$ (all 5 masked seeds: $1.8$–$2.5\times10^{-4}$). Two extra runs beyond the plan's ladder were therefore queued at code commit `36f4224` (job files `25567ea` and `8be2aa4`): `jobs/011` `v1_wsemigroup1` (`--w-semigroup 1`, a single change) and `jobs/012` `v1_wsig2_wsg1` (`--w-sigreg 2 --w-semigroup 1`). `jobs/008` (`v1_curriculum`) is also still unfinished.
7. **Process incidents** (reported honestly):
   - (a) A retry loop of the coordinator re-ran the `v1_base` J1 gate 10 extra times because it treated the gate's FAIL exit code as "laptop busy". The 10 identical duplicate ledger records were removed before commit; one record is kept (`evidence/J1_training/20261005T231912Z.json`).
   - (b) The laptop runner once converted a J1 gate run into a Perlmutter job file (`jobs/013`) because the laptop was busy; it was never committed or pushed and was deleted (job number 013 is therefore unused; the next job gets 013).
   - (c) The laptop was shared with another session at load 13–20 (of 12 logical CPUs) for hours, which delayed tests. (Earlier, in M2a, the runner also refused two end-of-session test attempts for lack of free cores.)

### 7.6 Parameter count
90,309 trainable parameters (encoder 22,288; predictor 67,936; grounding 85); latent 32: 97,349; the EMA copy adds 22,288 non-trained parameters (counted in code by the coordinating session; not re-counted here).

---

## 8. Current results in full

### 8.1 J0 (data gate): PASS, 9 of 9 rows (`evidence/J0_data/20261003T201012Z.json`, `evidence/GATE_LEDGER.md`)
| row | status | measured | threshold |
|---|---|---|---|
| D1 state counts | PASS | 82; sectors 2/20/38/20/2; electric 16/16/18/16/16 | same |
| D2 two-route agreement | PASS | $4.44\times10^{-16}$ | $10^{-12}$ |
| D2 Gauss-law commutator | PASS | 0 | $10^{-12}$ |
| D3 estimator bias, diagonal carrier (1,024 shots, 200 trials, max over 18 observables of $|$bias$|$/SE) | PASS | 2.355 SE | 4.0 SE |
| D3 estimator bias, chain carrier (Z+X, against the $K$-truncated state) | PASS | 1.439 SE | 4.0 SE |
| D4 Krylov $K=12$ reproduces the P-A window $t\le3/g_E$ | PASS | $1.054\times10^{-4}$ | $10^{-3}$ |
| D5 twin repeats independent | PASS | 5 distinct (of 5), $\sigma(p_1)=0.0147$ | 5 |
| D6 split leakage | PASS | 0 | 0 |
| D6 checksum recorded | PASS | `73fff8e5a7b7` | present |

J0 was run on the laptop copy of `data/main`. It has not been re-run on the Perlmutter copy.

### 8.2 Energy ceiling (J1 input; `evidence/J1_training/ceiling_main.json`, commit `63065dd`, 2026-10-05T17:31Z; `data/main` `73fff8e5a7b7`; training split 126,824 rows, validation split 26,348 rows; regressor seeds 462709266, 3658436304)
Validation $R^2$ of four regressors predicting each grounding target from one clean observation, alone and with the step's couplings $(c_M,c_H,c_B)$ appended:

| target | ridge | 5-NN | boosted trees | MLP | best, with couplings added |
|---|---|---|---|---|---|
| energy | 0.88684 | 0.85088 | 0.89016 | **0.91445** | 0.99412 (MLP; trees 0.9851, 5-NN 0.9696, ridge 0.9509) |
| $C_{\text{string}}$ | 1.00000 | 0.99720 | 0.99997 | 0.99990 | 1.0000 |
| $P_{\text{meson}}$ | 1.00000 | 0.98865 | 0.99598 | 0.99998 | 1.0000 |
| $P_{\text{baryonic}}$ | 1.00000 | 0.99685 | 0.99996 | 0.99995 | 1.0000 |

(Full table, including the with-couplings columns for every target, is P10 in §9.)
**Why energy is capped.** The grounding target is
$$E=\langle\psi|\,c_E\mathcal E+c_M\mathcal M+2c_H\mathcal T+c_B\mathcal B\,|\psi\rangle .$$
The encoder's input holds only configuration-basis (diagonal) quantities, so it lacks $\langle\mathcal T\rangle$ and $\langle\mathcal B\rangle$ (off-diagonal), and the couplings that weight each term differ between trajectories and reach the model only through the actions. The other three targets are themselves entries of the observation. The clean observations have effective rank 11.19 (standardised; 9.13 raw) and 14 nonzero variance directions of 18, so a latent rank of at least 8 is reachable in principle. Decision `decisions/005`: threshold $0.887=0.97\times0.9145$ (rounded down to three decimals).

### 8.3 J1 (training gate) for the six gated rungs (official gate runs; `evidence/GATE_LEDGER.md` rows; records in `evidence/J1_training/`)
All five-seed rungs: 5 seeds, no NaN (PASS), "number of seeds" PASS. Numbers are the final epoch (200) on the validation split; "min" and "max" are over the 5 seeds, exactly as the gate compares them. (All values verified against both the ledger and my own recomputation from the `history.json` files; they agree. The ledger prints rounded values such as 10.5 for 10.525.)

| rung (change vs base) | overall | rank min (≥ 8) | rank max | $R^2$ energy min (≥ 0.887) | $R^2$ $C_{\text{string}}$ min (≥ 0.99) | $R^2$ $P_{\text{meson}}$ min (≥ 0.95) | $R^2$ $P_{\text{baryonic}}$ min (≥ 0.98) | semigroup max (< $10^{-3}$) | semigroup min | per-seed ranks (seed 0..4) |
|---|---|---|---|---|---|---|---|---|---|---|
| `v1_base` (none; $w_{\text{sigreg}}=0.5$) | FAIL | 5.1562 **FAIL** | 6.1539 | 0.89943 PASS | 0.99820 PASS | 0.97786 PASS | 0.99707 PASS | 0.0032928 **FAIL** | 0.0018857 | 5.65, 6.15, 5.16, 5.89, 5.85 |
| `v1_wsigreg2` ($w_{\text{sigreg}}=2$) | FAIL | 8.2625 PASS | 9.1040 | 0.89994 PASS | 0.99763 PASS | 0.97205 PASS | 0.99654 PASS | 0.0053439 **FAIL** | 0.0034857 | 8.26, 9.10, 8.92, 8.93, 9.08 |
| `v1_wsigreg5` ($w_{\text{sigreg}}=5$) | FAIL | 10.525 PASS | 10.943 | 0.89929 PASS | 0.99687 PASS | 0.96767 PASS | 0.99573 PASS | 0.0084698 **FAIL** | 0.0062859 | 10.66, 10.84, 10.94, 10.83, 10.53 |
| `v1_latent32` (latent 32) | FAIL | 6.1165 **FAIL** (of 32) | 6.5754 | 0.90166 PASS | 0.99819 PASS | 0.97725 PASS | 0.99707 PASS | 0.0047161 **FAIL** | 0.0015498 | 6.53, 6.12, 6.58, 6.35, 6.22 |
| `v1_ema` (EMA target, $\tau=0.996$) | FAIL | 13.086 PASS | 13.475 | 0.89656 PASS | 0.99324 PASS | 0.91464 **FAIL** | 0.99347 PASS | 0.022098 **FAIL** | 0.015838 | 13.38, 13.27, 13.31, 13.09, 13.47 |
| `v1_wground3` ($w_{\text{ground}}=3$) | FAIL | 5.6294 **FAIL** | 6.1419 | 0.90001 PASS | 0.99796 PASS | 0.98338 PASS | 0.99717 PASS | 0.0069369 **FAIL** | 0.0023000 | 5.79, 6.14, 5.73, 6.13, 5.63 |

Ledger record ids: base `20261005T231912Z`; wsigreg2 `20261005T234716Z`; wsigreg5 `20261005T234719Z`; latent32 `20261006T000318Z`; ema `20261006T024735Z`; wground3 `20261006T030159Z`.

Additional diagnostics from the same final epoch (my helper `plot_tables.py`; P8 and P8b in §9): isotropy ranges 0.0019–0.013 (base), 0.025–0.069 (wsigreg2), 0.095–0.31 (wsigreg5), 0.00031–0.00084 (latent32), 0.077–0.23 (ema), 0.0023–0.0035 (wground3). The masked `v1_base` runs (not gated; information only): rank 4.5022–5.4179, $R^2$ minima 0.90054 / 0.99764 / 0.97523 / 0.99679, semigroup 0.00018148–0.00024869 (so a gate on them would pass the semigroup row but fail the rank row).

**What this means.**
1. **All energy, $C_{\text{string}}$, $P_{\text{baryonic}}$ rows PASS everywhere**; $P_{\text{meson}}$ passes everywhere except `v1_ema` (0.915). Energy $R^2\approx0.90$ is within about 0.015 of the measured ceiling 0.9145.
2. **Raising the SIGReg weight fixes the rank** (5.2–6.2 at weight 0.5; 8.3–9.1 at 2; 10.5–10.9 at 5), and the EMA target gives the highest rank (13.1–13.5). Latent 32 and grounding weight 3 do not fix it (6.1–6.6 and 5.6–6.1; for latent 32 the maximum possible rank is 32, so 6 is a much smaller fraction).
3. **No rung passes the semigroup row** (all between $3.3\times10^{-3}$ and $2.2\times10^{-2}$, against the threshold $10^{-3}$). The residual increases with the rank (§9, P9): Pearson correlation between rank and $\log_{10}$ residual over the 30 unmasked final-epoch points is 0.898 (Spearman 0.774; computed by `plot_tables.py`). This is a **correlation among runs that also differ in the loss weights**, not a proven mechanism; it is the coordinating session's PROPOSED explanation, to be tested by jobs 011 and 012.
4. In the epoch curves (P1, P6) the base rung's rank stays near 4.0 until about epoch 20 and then rises (mean 4.96 at epoch 50, 5.41 at 100, 5.74 at 200), while its semigroup residual is smallest around epoch 20 (mean $6.2\times10^{-4}$, below the threshold) and then rises to $2.6\times10^{-3}$. The 10-epoch laptop check had semigroup $2.5\times10^{-4}$ and rank 3.93.
5. **J1 verdict so far: FAIL for every rung that has finished.** The plan's fallback ("if rank stays below 8 after the ladder, report the collapse diagnosis and continue with the best model: J1 PARTIAL") is written for the rank row, whereas the row that fails for every rung here is the semigroup row; the plan has no explicit rule for a semigroup failure (flagged in §11). The verdict cannot yet be formed: rungs `v1_curriculum`, `v1_wsemigroup1`, `v1_wsig2_wsg1` are still to come (§8.5).

### 8.4 Dataset reproducibility (laptop versus Perlmutter; `evidence/J0_data/fingerprint_compare_*.json`, commit `3010090`, 2026-10-05T23:47Z)
| dataset | laptop checksum | Perlmutter checksum | arrays bit-identical | arrays differing only by rounding |
|---|---|---|---|---|
| `main` (20,000 traj) | `73fff8e5a7b7` | `76f4c9055591` | `ctx`, `act`, `valid` | `tgt`, `energy` |
| `gpu_smoke` (400 traj) | `585e1d0013d1` | `eb294d7db29f` | `ctx`, `act`, `valid` | `tgt`, `energy` |

Full per-array numbers (max difference of per-trajectory sums, count of trajectories above the $10^{-12}$ tolerance, max difference of the 2,000 sampled raw values) are in the table at the end of §9. Summary for `main`: `tgt` per-trajectory-sum maximum $5.73\times10^{-12}$ with 2,513 of 20,000 trajectories above $10^{-12}$, sampled values at most $5.66\times10^{-14}$ (none above tolerance); `energy` per-trajectory-sum maximum $2.48\times10^{-12}$ with 37 of 20,000 above tolerance, sampled values at most $1.94\times10^{-13}$. Since `ctx` is bit-identical, the noisy model inputs of laptop and Perlmutter training are the same; only the clean targets carry rounding noise of order $10^{-13}$ per value. Which checksum is the preregistration reference is still undecided (§11).

### 8.5 GPU-fix verification and the job table
GPU fix: `jobs/009` COMPLETED (§7.5 item 2). Jobs (all `where: perlmutter`; the job file's commit is the code commit for 002; for 003–008 it is the commit of the previous "job:" file, which contains the same code as `0a76800` since only job files were committed in between; for 010–012 see §7.5):

| job | purpose | job-file commit | Slurm limit | state | elapsed h | node-hours |
|---|---|---|---|---|---|---|
| 000 | worker smoke test (`env_check`) | `80efb3d` | 0:10 | COMPLETED | 0.011 | 0.003 |
| 001 | build `chain_strong` (3,000 traj) | `9affe3a` | 2:00 | COMPLETED | 0.223 | 0.056 |
| 002 | `v1_base` + masked runs (5+5 seeds, 200 epochs) | `0a76800` | 8:28 | FAILED after training (GPU baseline bug) | 2.164 | 0.541 |
| 003 | `v1_wsigreg2` | `1d9c4d0` | 4:14 | FAILED after training (same) | 1.035 | 0.259 |
| 004 | `v1_wsigreg5` | `a3ab4ca` | 4:14 | FAILED after training (same) | 1.031 | 0.258 |
| 005 | `v1_latent32` | `1c60d57` | 4:14 | FAILED after training (same) | 1.039 | 0.260 |
| 006 | `v1_ema` | `0cf933f` | 4:14 | FAILED after training (same) | 0.981 | 0.245 |
| 007 | `v1_wground3` | `aa7f8af` | 4:14 | FAILED after training (same) | 1.071 | 0.268 |
| 008 | `v1_curriculum` (50 epochs on horizons 1–2 first) | `7a18cdb` | 4:14 | SUBMITTED (not started or not finished; no status file) | – | – |
| 009 | `gpu_smoke` GPU check (2 epochs, 400 traj) | `5000bc9` | 0:30 | COMPLETED | 0.011 | 0.003 |
| 010 | rebuild fingerprints of `main` and `gpu_smoke` | `36f4224` | 0:40 | COMPLETED | 0.020 | 0.005 |
| 011 | `v1_wsemigroup1` (`--w-semigroup 1`) | `25567ea` | 4:14 | SUBMITTED | – | – |
| 012 | `v1_wsig2_wsg1` (`--w-sigreg 2 --w-semigroup 1`) | `8be2aa4` | 4:14 | SUBMITTED | – | – |

Sum of node-hours used: $0.003+0.056+0.541+0.259+0.258+0.260+0.245+0.268+0.003+0.005=1.898$ of the 50-node-hour budget (matches `status.py`: "node-hours used 1.898, in flight ['008', '011', '012']", worker heartbeat 2026-10-06T05:00:30Z). The "FAILED" states of 002–007 mean the *job* failed at its last step; the training results inside are complete and are what the J1 gates used. **Jobs 008, 011 and 012 are in progress and NOT RUN for J1;** I did not fetch or gate them. (Job 008 was submitted on 5 Oct about 17:40 UTC and is still listed SUBMITTED, so it is presumably waiting in the Slurm queue; I did not investigate.)

### 8.6 Forecast results so far
There is **no J2 result**. The only forecast numbers are from the 1-seed, 10-epoch laptop check (P12b, §9; the gate rows require 5 seeds, 200 epochs, per-family comparison): at $+8$ steps on-family, $P_{\text{baryonic}}$ MAE is 0.0722 (JEPA), 0.1437 (ridge), 0.4022 (autoregressive), 0.0483 (supervised MLP); the J2 threshold for JEPA is 0.05. Strong family $+8$, $P_{\text{baryonic}}$: JEPA 0.1291, ridge 0.1854, autoregressive 0.3705, supervised MLP 0.1528. J2 is NOT RUN. The twin, residual evaluation (J3), the pilot and every hardware day are NOT RUN.

---

## 9. Plot data (the data behind every figure; each table can be parsed as Markdown)

### 9.0 How to use this section
- All tables are Markdown pipe tables with a header row. "Long format" tables have one row per (series, x) pair; filter on the first column to get a series.
- **Runs.** Each *rung* is one training configuration with 5 independent seeds (`seed0`..`seed4`, spawned seeds listed in §6.1), 200 epochs, on `data/main` (Perlmutter copy). Rung names and what they change relative to `v1_base`: `v1_base` (none; $w_{\text{sigreg}}=0.5$, latent 16, $w_{\text{ground}}=1$, $w_{\text{semigroup}}=0.1$, shared target encoder), `v1_base_masked` (the same, trained with the masked-coupling task; folders `seed*_masked`; information only, not gated), `v1_wsigreg2` ($w_{\text{sigreg}}=2$), `v1_wsigreg5` ($w_{\text{sigreg}}=5$), `v1_latent32` (latent dimension 32), `v1_ema` (EMA target encoder, $\tau=0.996$), `v1_wground3` ($w_{\text{ground}}=3$).
- **What a "mean / min / max" is.** For each rung and epoch, the mean, minimum and maximum of the quantity over the 5 seeds of that rung (the "band" in a plot is min to max).
- **Epochs shown:** 1, 2, 5, 10, 20, 30, ..., 200 (23 epochs). Each `history.json` holds all 200 epochs; epochs are 1-based.
- **Source of all tables from P1 to P9b and P12/P12b:** `runs/<rung>/seed*/history.json` and `runs/v1_check/*` (local files, not in git), processed by `plot_tables.py` (Appendix A.1). Values printed with 5 significant digits (`%.5g`).
- **Source of P10, P11e, P11f and the evidence tables:** `evidence_tables.py` (A.3). **Source of P11a–P11d:** `physics_curves.py` (A.2), which uses the repository's physics core.
- The validation split is used throughout (diagnostics were computed on `data/main` split `val`). The `ground_r2` entries are in the order (energy, $C_{\text{string}}$, $P_{\text{meson}}$, $P_{\text{baryonic}}$, flag); flag is NaN.

### 9.1 Catalogue of plots
| plot | title | x axis | y axis | series | scale and drawing hints | table(s) |
|---|---|---|---|---|---|---|
| P1 | Effective rank vs epoch | epoch (1..200) | effective rank (dimensionless, max 16; 32 for latent32) | 7 rungs; line = mean, band = min..max over seeds | linear; horizontal reference line at 8 (J1 threshold) | P1 |
| P2 | Grounding $R^2$ of the energy vs epoch | epoch | $R^2$ (dimensionless) | 7 rungs, mean and band | linear, y from about 0.85 to 0.91; reference lines at 0.887 (J1 threshold) and 0.9145 (measured ceiling) | P2 |
| P3 | Grounding $R^2$ of $C_{\text{string}}$ vs epoch | epoch | $R^2$ | 7 rungs | linear; threshold 0.99 | P3 |
| P4 | Grounding $R^2$ of $P_{\text{meson}}$ vs epoch | epoch | $R^2$ | 7 rungs | linear; threshold 0.95 | P4 |
| P5 | Grounding $R^2$ of $P_{\text{baryonic}}$ vs epoch | epoch | $R^2$ | 7 rungs | linear; threshold 0.98 | P5 |
| P6 | Semigroup residual vs epoch | epoch | relative squared mismatch (dimensionless) | 7 rungs, mean and band | **logarithmic y axis**; threshold $10^{-3}$ | P6 |
| P7 | Training loss terms vs epoch | epoch | loss value (unweighted terms as logged; `total` is weighted) | for each rung four curves: pred, sigreg, ground, semigroup (seed means); `total` also given | log y axis advisable; one panel per loss term, 7 curves each | P7, P7b |
| P8 | Final-epoch per-seed table | – (table) | eff_rank, four $R^2$, semigroup residual, isotropy, pred loss | 7 rungs × 5 seeds | strip or dot plot per metric; P8b gives the per-rung min/max used by the gate | P8, P8b |
| P9 | Trade-off scatter: rank vs semigroup residual | effective rank at epoch 200 | semigroup residual at epoch 200 | one point per (rung, seed), 35 points, colour by rung | log y axis; vertical line at rank 8, horizontal line at $10^{-3}$; masked rung shown but excluded from the correlation | P9 |
| P10 | Energy ceiling bars | target (energy, $C_{\text{string}}$, $P_{\text{meson}}$, $P_{\text{baryonic}}$) | validation $R^2$ | grouped bars: regressor (ridge, 5-NN, trees, MLP) × inputs (observation only; observation + couplings) | linear, y from 0.84 to 1.0; line at 0.887 | P10 |
| P11 | Physics curves and carrier costs | see sub-plots | see sub-plots | see sub-plots | see sub-plots | P11a–P11g |
| P12 | v1_check (10-epoch laptop check) | epoch (1..10) | rank, $R^2$s, residual, losses | 1 seed | same hints as P1–P7; plus forecast MAE bars from P12b (not a J2 result) | P12, P12b |

The seed-aggregated band for P1–P6 is min..max (not a standard deviation).

### P1 (data): effective rank vs epoch

#### P1 table: eff_rank (mean, min, max over 5 seeds)

| rung | epoch | mean | min | max |
|---|---|---|---|---|
| v1_base | 1 | 4.0017 | 3.7271 | 4.2733 |
| v1_base | 2 | 4.1513 | 3.9563 | 4.306 |
| v1_base | 5 | 4.0514 | 3.9042 | 4.2496 |
| v1_base | 10 | 3.9974 | 3.8592 | 4.1853 |
| v1_base | 20 | 4.0364 | 3.8356 | 4.427 |
| v1_base | 30 | 4.4523 | 4.0723 | 4.9104 |
| v1_base | 40 | 4.8473 | 4.7281 | 4.9725 |
| v1_base | 50 | 4.9587 | 4.7351 | 5.0587 |
| v1_base | 60 | 5.0529 | 4.8518 | 5.1645 |
| v1_base | 70 | 5.1411 | 4.7938 | 5.3267 |
| v1_base | 80 | 5.2404 | 4.8589 | 5.5582 |
| v1_base | 90 | 5.3155 | 4.9231 | 5.6105 |
| v1_base | 100 | 5.4129 | 4.978 | 5.619 |
| v1_base | 110 | 5.5031 | 5.0066 | 5.7316 |
| v1_base | 120 | 5.5595 | 5.0528 | 5.7363 |
| v1_base | 130 | 5.6541 | 5.0462 | 5.8678 |
| v1_base | 140 | 5.674 | 5.0557 | 5.9318 |
| v1_base | 150 | 5.7325 | 5.1097 | 6.0912 |
| v1_base | 160 | 5.7347 | 5.1232 | 6.1132 |
| v1_base | 170 | 5.7508 | 5.0949 | 6.1629 |
| v1_base | 180 | 5.7452 | 5.1162 | 6.1934 |
| v1_base | 190 | 5.7738 | 5.1541 | 6.2218 |
| v1_base | 200 | 5.7408 | 5.1562 | 6.1539 |
| v1_base_masked | 1 | 3.9877 | 3.7223 | 4.2368 |
| v1_base_masked | 2 | 4.1376 | 3.9238 | 4.3145 |
| v1_base_masked | 5 | 4.0834 | 3.9678 | 4.2373 |
| v1_base_masked | 10 | 4.0259 | 3.9295 | 4.1588 |
| v1_base_masked | 20 | 3.913 | 3.7607 | 4.1437 |
| v1_base_masked | 30 | 3.8938 | 3.7451 | 4.2917 |
| v1_base_masked | 40 | 3.8735 | 3.7394 | 4.2433 |
| v1_base_masked | 50 | 3.9817 | 3.7782 | 4.5478 |
| v1_base_masked | 60 | 4.0981 | 3.8143 | 4.943 |
| v1_base_masked | 70 | 4.2269 | 3.9854 | 4.9859 |
| v1_base_masked | 80 | 4.4059 | 3.9872 | 5.0196 |
| v1_base_masked | 90 | 4.5407 | 4.1102 | 5.1338 |
| v1_base_masked | 100 | 4.6531 | 4.4149 | 5.1778 |
| v1_base_masked | 110 | 4.7226 | 4.457 | 5.2503 |
| v1_base_masked | 120 | 4.739 | 4.5202 | 5.334 |
| v1_base_masked | 130 | 4.7659 | 4.4852 | 5.3506 |
| v1_base_masked | 140 | 4.756 | 4.5034 | 5.3532 |
| v1_base_masked | 150 | 4.7941 | 4.5337 | 5.3946 |
| v1_base_masked | 160 | 4.7725 | 4.5138 | 5.3794 |
| v1_base_masked | 170 | 4.7842 | 4.496 | 5.4241 |
| v1_base_masked | 180 | 4.786 | 4.4939 | 5.4451 |
| v1_base_masked | 190 | 4.7982 | 4.529 | 5.3831 |
| v1_base_masked | 200 | 4.7707 | 4.5022 | 5.4179 |
| v1_wsigreg2 | 1 | 4.545 | 4.4303 | 4.6827 |
| v1_wsigreg2 | 2 | 4.6617 | 4.3799 | 4.9091 |
| v1_wsigreg2 | 5 | 5.7323 | 5.5431 | 5.8761 |
| v1_wsigreg2 | 10 | 6.4504 | 6.2583 | 6.7635 |
| v1_wsigreg2 | 20 | 7.2578 | 6.9811 | 7.5376 |
| v1_wsigreg2 | 30 | 7.8667 | 7.4871 | 8.1678 |
| v1_wsigreg2 | 40 | 8.1865 | 7.8184 | 8.4817 |
| v1_wsigreg2 | 50 | 8.4006 | 7.9409 | 8.8007 |
| v1_wsigreg2 | 60 | 8.528 | 8.0824 | 8.8798 |
| v1_wsigreg2 | 70 | 8.6327 | 8.1426 | 8.9838 |
| v1_wsigreg2 | 80 | 8.7023 | 8.1522 | 9.0742 |
| v1_wsigreg2 | 90 | 8.7546 | 8.1107 | 9.0973 |
| v1_wsigreg2 | 100 | 8.811 | 8.1647 | 9.1499 |
| v1_wsigreg2 | 110 | 8.8469 | 8.3169 | 9.1366 |
| v1_wsigreg2 | 120 | 8.8656 | 8.2482 | 9.1417 |
| v1_wsigreg2 | 130 | 8.8859 | 8.3179 | 9.125 |
| v1_wsigreg2 | 140 | 8.8627 | 8.2484 | 9.1187 |
| v1_wsigreg2 | 150 | 8.886 | 8.3213 | 9.1438 |
| v1_wsigreg2 | 160 | 8.8701 | 8.2909 | 9.1074 |
| v1_wsigreg2 | 170 | 8.8719 | 8.3097 | 9.1115 |
| v1_wsigreg2 | 180 | 8.8556 | 8.2648 | 9.0787 |
| v1_wsigreg2 | 190 | 8.8854 | 8.3168 | 9.1308 |
| v1_wsigreg2 | 200 | 8.8602 | 8.2625 | 9.104 |
| v1_wsigreg5 | 1 | 6.3141 | 5.8701 | 6.5792 |
| v1_wsigreg5 | 2 | 6.8505 | 6.5277 | 7.1047 |
| v1_wsigreg5 | 5 | 7.6939 | 7.2739 | 7.8662 |
| v1_wsigreg5 | 10 | 8.6303 | 8.118 | 9.2154 |
| v1_wsigreg5 | 20 | 9.494 | 8.9479 | 9.6593 |
| v1_wsigreg5 | 30 | 9.8596 | 9.642 | 10.101 |
| v1_wsigreg5 | 40 | 10.072 | 9.6769 | 10.406 |
| v1_wsigreg5 | 50 | 10.222 | 9.8411 | 10.548 |
| v1_wsigreg5 | 60 | 10.265 | 9.8297 | 10.567 |
| v1_wsigreg5 | 70 | 10.365 | 9.9152 | 10.623 |
| v1_wsigreg5 | 80 | 10.472 | 10.099 | 10.717 |
| v1_wsigreg5 | 90 | 10.532 | 10.177 | 10.714 |
| v1_wsigreg5 | 100 | 10.598 | 10.28 | 10.817 |
| v1_wsigreg5 | 110 | 10.656 | 10.525 | 10.836 |
| v1_wsigreg5 | 120 | 10.719 | 10.537 | 10.903 |
| v1_wsigreg5 | 130 | 10.744 | 10.553 | 10.881 |
| v1_wsigreg5 | 140 | 10.745 | 10.555 | 10.863 |
| v1_wsigreg5 | 150 | 10.755 | 10.558 | 10.842 |
| v1_wsigreg5 | 160 | 10.751 | 10.584 | 10.909 |
| v1_wsigreg5 | 170 | 10.767 | 10.511 | 10.902 |
| v1_wsigreg5 | 180 | 10.739 | 10.536 | 10.919 |
| v1_wsigreg5 | 190 | 10.767 | 10.59 | 10.929 |
| v1_wsigreg5 | 200 | 10.759 | 10.525 | 10.943 |
| v1_latent32 | 1 | 4.965 | 4.7781 | 5.2408 |
| v1_latent32 | 2 | 4.8674 | 4.5731 | 5.0103 |
| v1_latent32 | 5 | 4.4842 | 4.2944 | 4.6121 |
| v1_latent32 | 10 | 4.341 | 4.2455 | 4.5523 |
| v1_latent32 | 20 | 4.166 | 4.005 | 4.3526 |
| v1_latent32 | 30 | 4.481 | 4.1423 | 4.9644 |
| v1_latent32 | 40 | 5.1748 | 4.9857 | 5.3985 |
| v1_latent32 | 50 | 5.3578 | 5.0971 | 5.5745 |
| v1_latent32 | 60 | 5.5045 | 5.1919 | 5.7487 |
| v1_latent32 | 70 | 5.6589 | 5.3161 | 6.0591 |
| v1_latent32 | 80 | 5.8569 | 5.4256 | 6.3673 |
| v1_latent32 | 90 | 6.0315 | 5.5029 | 6.3654 |
| v1_latent32 | 100 | 6.1966 | 5.6596 | 6.4342 |
| v1_latent32 | 110 | 6.3217 | 5.8568 | 6.6038 |
| v1_latent32 | 120 | 6.338 | 5.935 | 6.5477 |
| v1_latent32 | 130 | 6.3916 | 6.096 | 6.6138 |
| v1_latent32 | 140 | 6.374 | 6.1513 | 6.5678 |
| v1_latent32 | 150 | 6.388 | 6.1505 | 6.6301 |
| v1_latent32 | 160 | 6.3818 | 6.1449 | 6.5876 |
| v1_latent32 | 170 | 6.3753 | 6.137 | 6.6137 |
| v1_latent32 | 180 | 6.3618 | 6.1328 | 6.5576 |
| v1_latent32 | 190 | 6.39 | 6.1491 | 6.5983 |
| v1_latent32 | 200 | 6.3587 | 6.1165 | 6.5754 |
| v1_ema | 1 | 7.1609 | 6.8903 | 7.3365 |
| v1_ema | 2 | 7.8183 | 7.5127 | 7.9728 |
| v1_ema | 5 | 8.9594 | 8.7334 | 9.2838 |
| v1_ema | 10 | 9.7822 | 9.6319 | 9.8961 |
| v1_ema | 20 | 10.875 | 10.545 | 11.173 |
| v1_ema | 30 | 11.566 | 11.281 | 11.962 |
| v1_ema | 40 | 12.041 | 11.799 | 12.305 |
| v1_ema | 50 | 12.432 | 12.237 | 12.616 |
| v1_ema | 60 | 12.734 | 12.515 | 12.988 |
| v1_ema | 70 | 12.903 | 12.782 | 13.035 |
| v1_ema | 80 | 13.089 | 12.966 | 13.243 |
| v1_ema | 90 | 13.13 | 12.948 | 13.29 |
| v1_ema | 100 | 13.164 | 12.824 | 13.261 |
| v1_ema | 110 | 13.258 | 13.056 | 13.492 |
| v1_ema | 120 | 13.323 | 13.159 | 13.426 |
| v1_ema | 130 | 13.263 | 13.055 | 13.401 |
| v1_ema | 140 | 13.265 | 13.027 | 13.376 |
| v1_ema | 150 | 13.338 | 13.016 | 13.553 |
| v1_ema | 160 | 13.27 | 12.984 | 13.428 |
| v1_ema | 170 | 13.357 | 13.188 | 13.465 |
| v1_ema | 180 | 13.287 | 12.997 | 13.453 |
| v1_ema | 190 | 13.28 | 12.896 | 13.453 |
| v1_ema | 200 | 13.305 | 13.086 | 13.475 |
| v1_wground3 | 1 | 4.4093 | 4.141 | 4.6228 |
| v1_wground3 | 2 | 4.3104 | 4.1081 | 4.4624 |
| v1_wground3 | 5 | 4.2919 | 4.1599 | 4.478 |
| v1_wground3 | 10 | 4.2877 | 4.1851 | 4.4744 |
| v1_wground3 | 20 | 4.1083 | 3.9574 | 4.1928 |
| v1_wground3 | 30 | 4.2689 | 3.9998 | 4.5799 |
| v1_wground3 | 40 | 4.8155 | 4.2866 | 5.1465 |
| v1_wground3 | 50 | 5.1499 | 4.9951 | 5.2053 |
| v1_wground3 | 60 | 5.2497 | 5.1609 | 5.3544 |
| v1_wground3 | 70 | 5.3429 | 5.1111 | 5.4751 |
| v1_wground3 | 80 | 5.4303 | 5.2278 | 5.6134 |
| v1_wground3 | 90 | 5.4939 | 5.2653 | 5.7788 |
| v1_wground3 | 100 | 5.6168 | 5.3809 | 5.9625 |
| v1_wground3 | 110 | 5.7175 | 5.4054 | 6.1562 |
| v1_wground3 | 120 | 5.7328 | 5.455 | 6.1225 |
| v1_wground3 | 130 | 5.8159 | 5.499 | 6.1713 |
| v1_wground3 | 140 | 5.8189 | 5.5695 | 6.1448 |
| v1_wground3 | 150 | 5.8543 | 5.6008 | 6.1488 |
| v1_wground3 | 160 | 5.8698 | 5.6297 | 6.1442 |
| v1_wground3 | 170 | 5.8838 | 5.6302 | 6.1659 |
| v1_wground3 | 180 | 5.8828 | 5.6419 | 6.1724 |
| v1_wground3 | 190 | 5.9162 | 5.6879 | 6.1943 |
| v1_wground3 | 200 | 5.8844 | 5.6294 | 6.1419 |

### P2 (data): grounding R2 of energy vs epoch

#### P2 table: R2 energy (mean, min, max over 5 seeds)

| rung | epoch | mean | min | max |
|---|---|---|---|---|
| v1_base | 1 | 0.87737 | 0.85951 | 0.89065 |
| v1_base | 2 | 0.87626 | 0.84226 | 0.89267 |
| v1_base | 5 | 0.88582 | 0.88038 | 0.89733 |
| v1_base | 10 | 0.88735 | 0.87628 | 0.89775 |
| v1_base | 20 | 0.89429 | 0.88608 | 0.89987 |
| v1_base | 30 | 0.89056 | 0.88525 | 0.8949 |
| v1_base | 40 | 0.89583 | 0.88986 | 0.90271 |
| v1_base | 50 | 0.89108 | 0.88196 | 0.89915 |
| v1_base | 60 | 0.89439 | 0.88693 | 0.90341 |
| v1_base | 70 | 0.89867 | 0.89608 | 0.9007 |
| v1_base | 80 | 0.89716 | 0.89574 | 0.89825 |
| v1_base | 90 | 0.89919 | 0.89745 | 0.90278 |
| v1_base | 100 | 0.89798 | 0.89472 | 0.90152 |
| v1_base | 110 | 0.89894 | 0.89659 | 0.90418 |
| v1_base | 120 | 0.9004 | 0.89513 | 0.90615 |
| v1_base | 130 | 0.90037 | 0.8963 | 0.90365 |
| v1_base | 140 | 0.89938 | 0.89545 | 0.90272 |
| v1_base | 150 | 0.8979 | 0.88639 | 0.90394 |
| v1_base | 160 | 0.90155 | 0.89429 | 0.90486 |
| v1_base | 170 | 0.90149 | 0.89943 | 0.90234 |
| v1_base | 180 | 0.8993 | 0.8905 | 0.90247 |
| v1_base | 190 | 0.89717 | 0.88082 | 0.90346 |
| v1_base | 200 | 0.90089 | 0.89943 | 0.90343 |
| v1_base_masked | 1 | 0.87718 | 0.8589 | 0.89049 |
| v1_base_masked | 2 | 0.87657 | 0.84669 | 0.89136 |
| v1_base_masked | 5 | 0.88731 | 0.88161 | 0.89791 |
| v1_base_masked | 10 | 0.8873 | 0.87526 | 0.89644 |
| v1_base_masked | 20 | 0.89321 | 0.88694 | 0.89919 |
| v1_base_masked | 30 | 0.8914 | 0.88305 | 0.89563 |
| v1_base_masked | 40 | 0.89755 | 0.89271 | 0.90237 |
| v1_base_masked | 50 | 0.894 | 0.88604 | 0.90066 |
| v1_base_masked | 60 | 0.8959 | 0.88789 | 0.9037 |
| v1_base_masked | 70 | 0.89977 | 0.8989 | 0.90236 |
| v1_base_masked | 80 | 0.89733 | 0.89396 | 0.89965 |
| v1_base_masked | 90 | 0.90028 | 0.89832 | 0.90319 |
| v1_base_masked | 100 | 0.89797 | 0.89468 | 0.9008 |
| v1_base_masked | 110 | 0.89901 | 0.89623 | 0.90532 |
| v1_base_masked | 120 | 0.89957 | 0.89474 | 0.90427 |
| v1_base_masked | 130 | 0.9003 | 0.89686 | 0.90346 |
| v1_base_masked | 140 | 0.90142 | 0.8985 | 0.90405 |
| v1_base_masked | 150 | 0.9008 | 0.89678 | 0.90592 |
| v1_base_masked | 160 | 0.90339 | 0.90209 | 0.90508 |
| v1_base_masked | 170 | 0.90179 | 0.9003 | 0.90337 |
| v1_base_masked | 180 | 0.90219 | 0.89869 | 0.9042 |
| v1_base_masked | 190 | 0.90046 | 0.89906 | 0.9025 |
| v1_base_masked | 200 | 0.90168 | 0.90054 | 0.90261 |
| v1_wsigreg2 | 1 | 0.8806 | 0.87055 | 0.88969 |
| v1_wsigreg2 | 2 | 0.87507 | 0.83405 | 0.89176 |
| v1_wsigreg2 | 5 | 0.87912 | 0.87053 | 0.88674 |
| v1_wsigreg2 | 10 | 0.89058 | 0.88623 | 0.89587 |
| v1_wsigreg2 | 20 | 0.88969 | 0.87266 | 0.89582 |
| v1_wsigreg2 | 30 | 0.89035 | 0.88361 | 0.89541 |
| v1_wsigreg2 | 40 | 0.8943 | 0.8875 | 0.89908 |
| v1_wsigreg2 | 50 | 0.88979 | 0.88122 | 0.89472 |
| v1_wsigreg2 | 60 | 0.89214 | 0.88362 | 0.89938 |
| v1_wsigreg2 | 70 | 0.89681 | 0.89423 | 0.89825 |
| v1_wsigreg2 | 80 | 0.89644 | 0.89068 | 0.89906 |
| v1_wsigreg2 | 90 | 0.89809 | 0.89649 | 0.89974 |
| v1_wsigreg2 | 100 | 0.89591 | 0.89309 | 0.89704 |
| v1_wsigreg2 | 110 | 0.8976 | 0.89258 | 0.90416 |
| v1_wsigreg2 | 120 | 0.89778 | 0.89292 | 0.90364 |
| v1_wsigreg2 | 130 | 0.89886 | 0.89481 | 0.90187 |
| v1_wsigreg2 | 140 | 0.90005 | 0.89782 | 0.90294 |
| v1_wsigreg2 | 150 | 0.89976 | 0.8963 | 0.90416 |
| v1_wsigreg2 | 160 | 0.90177 | 0.8995 | 0.9032 |
| v1_wsigreg2 | 170 | 0.90049 | 0.8985 | 0.90204 |
| v1_wsigreg2 | 180 | 0.90128 | 0.89933 | 0.90313 |
| v1_wsigreg2 | 190 | 0.89957 | 0.89728 | 0.9012 |
| v1_wsigreg2 | 200 | 0.90087 | 0.89994 | 0.90228 |
| v1_wsigreg5 | 1 | 0.877 | 0.8659 | 0.88347 |
| v1_wsigreg5 | 2 | 0.87665 | 0.85009 | 0.88426 |
| v1_wsigreg5 | 5 | 0.88 | 0.86982 | 0.88863 |
| v1_wsigreg5 | 10 | 0.88536 | 0.868 | 0.89616 |
| v1_wsigreg5 | 20 | 0.88769 | 0.8758 | 0.89674 |
| v1_wsigreg5 | 30 | 0.88994 | 0.8855 | 0.89416 |
| v1_wsigreg5 | 40 | 0.8943 | 0.88802 | 0.89943 |
| v1_wsigreg5 | 50 | 0.88799 | 0.87618 | 0.89504 |
| v1_wsigreg5 | 60 | 0.89253 | 0.88493 | 0.89982 |
| v1_wsigreg5 | 70 | 0.89583 | 0.89226 | 0.89736 |
| v1_wsigreg5 | 80 | 0.89834 | 0.89176 | 0.90191 |
| v1_wsigreg5 | 90 | 0.8968 | 0.8934 | 0.89799 |
| v1_wsigreg5 | 100 | 0.89509 | 0.89019 | 0.9006 |
| v1_wsigreg5 | 110 | 0.89833 | 0.89593 | 0.89997 |
| v1_wsigreg5 | 120 | 0.89819 | 0.89184 | 0.90203 |
| v1_wsigreg5 | 130 | 0.89902 | 0.89317 | 0.90125 |
| v1_wsigreg5 | 140 | 0.89935 | 0.89805 | 0.90149 |
| v1_wsigreg5 | 150 | 0.89912 | 0.89469 | 0.90545 |
| v1_wsigreg5 | 160 | 0.90114 | 0.89992 | 0.90299 |
| v1_wsigreg5 | 170 | 0.90009 | 0.89699 | 0.90242 |
| v1_wsigreg5 | 180 | 0.90162 | 0.89941 | 0.90458 |
| v1_wsigreg5 | 190 | 0.89875 | 0.89702 | 0.90081 |
| v1_wsigreg5 | 200 | 0.90101 | 0.89929 | 0.9019 |
| v1_latent32 | 1 | 0.87287 | 0.85592 | 0.88578 |
| v1_latent32 | 2 | 0.87114 | 0.82349 | 0.89368 |
| v1_latent32 | 5 | 0.88365 | 0.87432 | 0.89643 |
| v1_latent32 | 10 | 0.88522 | 0.87697 | 0.89826 |
| v1_latent32 | 20 | 0.89254 | 0.88839 | 0.89642 |
| v1_latent32 | 30 | 0.88908 | 0.88089 | 0.89666 |
| v1_latent32 | 40 | 0.89655 | 0.88937 | 0.90189 |
| v1_latent32 | 50 | 0.89118 | 0.88251 | 0.89914 |
| v1_latent32 | 60 | 0.89393 | 0.88409 | 0.9042 |
| v1_latent32 | 70 | 0.89882 | 0.89547 | 0.90096 |
| v1_latent32 | 80 | 0.89677 | 0.8907 | 0.90059 |
| v1_latent32 | 90 | 0.8989 | 0.89494 | 0.90135 |
| v1_latent32 | 100 | 0.89899 | 0.89624 | 0.90096 |
| v1_latent32 | 110 | 0.90011 | 0.89803 | 0.90586 |
| v1_latent32 | 120 | 0.90126 | 0.89626 | 0.90539 |
| v1_latent32 | 130 | 0.9013 | 0.89838 | 0.90373 |
| v1_latent32 | 140 | 0.9013 | 0.89906 | 0.90475 |
| v1_latent32 | 150 | 0.90215 | 0.89776 | 0.90509 |
| v1_latent32 | 160 | 0.90307 | 0.90132 | 0.90468 |
| v1_latent32 | 170 | 0.90217 | 0.90035 | 0.90461 |
| v1_latent32 | 180 | 0.90249 | 0.90061 | 0.90537 |
| v1_latent32 | 190 | 0.90147 | 0.9002 | 0.90363 |
| v1_latent32 | 200 | 0.90223 | 0.90166 | 0.90304 |
| v1_ema | 1 | 0.88086 | 0.87012 | 0.89051 |
| v1_ema | 2 | 0.8725 | 0.83835 | 0.89558 |
| v1_ema | 5 | 0.8769 | 0.87004 | 0.88375 |
| v1_ema | 10 | 0.88442 | 0.8638 | 0.89383 |
| v1_ema | 20 | 0.89183 | 0.88654 | 0.89701 |
| v1_ema | 30 | 0.89286 | 0.8894 | 0.8951 |
| v1_ema | 40 | 0.89462 | 0.88778 | 0.90111 |
| v1_ema | 50 | 0.89019 | 0.88136 | 0.89592 |
| v1_ema | 60 | 0.89333 | 0.88286 | 0.8989 |
| v1_ema | 70 | 0.89678 | 0.89536 | 0.89943 |
| v1_ema | 80 | 0.89438 | 0.88753 | 0.90165 |
| v1_ema | 90 | 0.89742 | 0.89261 | 0.89922 |
| v1_ema | 100 | 0.89637 | 0.89294 | 0.89794 |
| v1_ema | 110 | 0.89724 | 0.89359 | 0.9021 |
| v1_ema | 120 | 0.89812 | 0.89082 | 0.902 |
| v1_ema | 130 | 0.89763 | 0.89094 | 0.9005 |
| v1_ema | 140 | 0.89888 | 0.89608 | 0.90069 |
| v1_ema | 150 | 0.89848 | 0.89625 | 0.90191 |
| v1_ema | 160 | 0.90062 | 0.89833 | 0.90301 |
| v1_ema | 170 | 0.89802 | 0.89519 | 0.90078 |
| v1_ema | 180 | 0.90067 | 0.89931 | 0.90207 |
| v1_ema | 190 | 0.89928 | 0.89573 | 0.90294 |
| v1_ema | 200 | 0.89897 | 0.89656 | 0.90175 |
| v1_wground3 | 1 | 0.87034 | 0.83101 | 0.88849 |
| v1_wground3 | 2 | 0.88528 | 0.87594 | 0.89376 |
| v1_wground3 | 5 | 0.89149 | 0.88781 | 0.89776 |
| v1_wground3 | 10 | 0.8853 | 0.86655 | 0.89537 |
| v1_wground3 | 20 | 0.89387 | 0.88623 | 0.90187 |
| v1_wground3 | 30 | 0.89282 | 0.88443 | 0.89964 |
| v1_wground3 | 40 | 0.89774 | 0.892 | 0.90481 |
| v1_wground3 | 50 | 0.89165 | 0.87951 | 0.8994 |
| v1_wground3 | 60 | 0.89496 | 0.88641 | 0.90293 |
| v1_wground3 | 70 | 0.89906 | 0.89574 | 0.90149 |
| v1_wground3 | 80 | 0.89776 | 0.89372 | 0.90033 |
| v1_wground3 | 90 | 0.90009 | 0.89773 | 0.9024 |
| v1_wground3 | 100 | 0.89871 | 0.89532 | 0.90038 |
| v1_wground3 | 110 | 0.89988 | 0.89688 | 0.9042 |
| v1_wground3 | 120 | 0.90077 | 0.89524 | 0.90468 |
| v1_wground3 | 130 | 0.90081 | 0.89586 | 0.90416 |
| v1_wground3 | 140 | 0.90088 | 0.89832 | 0.90417 |
| v1_wground3 | 150 | 0.90086 | 0.89801 | 0.90429 |
| v1_wground3 | 160 | 0.90342 | 0.90236 | 0.90457 |
| v1_wground3 | 170 | 0.90159 | 0.89937 | 0.90414 |
| v1_wground3 | 180 | 0.90212 | 0.90048 | 0.90444 |
| v1_wground3 | 190 | 0.90109 | 0.89955 | 0.90353 |
| v1_wground3 | 200 | 0.9015 | 0.90001 | 0.90268 |

### P3 (data): grounding R2 of C_string vs epoch

#### P3 table: R2 C_string (mean, min, max over 5 seeds)

| rung | epoch | mean | min | max |
|---|---|---|---|---|
| v1_base | 1 | 0.96506 | 0.94061 | 0.98095 |
| v1_base | 2 | 0.96952 | 0.9562 | 0.98857 |
| v1_base | 5 | 0.98433 | 0.97782 | 0.99151 |
| v1_base | 10 | 0.98435 | 0.97041 | 0.9921 |
| v1_base | 20 | 0.99207 | 0.98482 | 0.99542 |
| v1_base | 30 | 0.99565 | 0.99303 | 0.99662 |
| v1_base | 40 | 0.99523 | 0.99232 | 0.99727 |
| v1_base | 50 | 0.99594 | 0.99286 | 0.99803 |
| v1_base | 60 | 0.99627 | 0.99357 | 0.99762 |
| v1_base | 70 | 0.99664 | 0.99457 | 0.99777 |
| v1_base | 80 | 0.99742 | 0.99626 | 0.99841 |
| v1_base | 90 | 0.99741 | 0.99652 | 0.99811 |
| v1_base | 100 | 0.99673 | 0.99476 | 0.99759 |
| v1_base | 110 | 0.99773 | 0.99716 | 0.99808 |
| v1_base | 120 | 0.99784 | 0.99761 | 0.99801 |
| v1_base | 130 | 0.9974 | 0.9945 | 0.99863 |
| v1_base | 140 | 0.99797 | 0.99677 | 0.99851 |
| v1_base | 150 | 0.99805 | 0.99735 | 0.99856 |
| v1_base | 160 | 0.99807 | 0.99722 | 0.99854 |
| v1_base | 170 | 0.99838 | 0.99819 | 0.99849 |
| v1_base | 180 | 0.99845 | 0.99837 | 0.99861 |
| v1_base | 190 | 0.99772 | 0.99639 | 0.99836 |
| v1_base | 200 | 0.99831 | 0.9982 | 0.99843 |
| v1_base_masked | 1 | 0.96441 | 0.93822 | 0.98059 |
| v1_base_masked | 2 | 0.97006 | 0.95072 | 0.99033 |
| v1_base_masked | 5 | 0.98544 | 0.97883 | 0.99234 |
| v1_base_masked | 10 | 0.9834 | 0.96636 | 0.99238 |
| v1_base_masked | 20 | 0.98958 | 0.98367 | 0.99277 |
| v1_base_masked | 30 | 0.99375 | 0.99014 | 0.99644 |
| v1_base_masked | 40 | 0.9942 | 0.99053 | 0.99615 |
| v1_base_masked | 50 | 0.99445 | 0.99353 | 0.99659 |
| v1_base_masked | 60 | 0.99555 | 0.99254 | 0.99712 |
| v1_base_masked | 70 | 0.99625 | 0.99342 | 0.99756 |
| v1_base_masked | 80 | 0.99723 | 0.99637 | 0.99779 |
| v1_base_masked | 90 | 0.99703 | 0.99613 | 0.99772 |
| v1_base_masked | 100 | 0.9965 | 0.99499 | 0.99733 |
| v1_base_masked | 110 | 0.99739 | 0.99711 | 0.99792 |
| v1_base_masked | 120 | 0.99753 | 0.99695 | 0.99787 |
| v1_base_masked | 130 | 0.99711 | 0.99469 | 0.99794 |
| v1_base_masked | 140 | 0.99759 | 0.9971 | 0.9979 |
| v1_base_masked | 150 | 0.99755 | 0.99708 | 0.99833 |
| v1_base_masked | 160 | 0.99781 | 0.99724 | 0.99819 |
| v1_base_masked | 170 | 0.99801 | 0.99768 | 0.99821 |
| v1_base_masked | 180 | 0.99792 | 0.9969 | 0.99836 |
| v1_base_masked | 190 | 0.99741 | 0.99656 | 0.99819 |
| v1_base_masked | 200 | 0.99809 | 0.99764 | 0.99836 |
| v1_wsigreg2 | 1 | 0.96324 | 0.93039 | 0.98153 |
| v1_wsigreg2 | 2 | 0.97624 | 0.96053 | 0.98472 |
| v1_wsigreg2 | 5 | 0.97108 | 0.95827 | 0.98483 |
| v1_wsigreg2 | 10 | 0.98787 | 0.98201 | 0.99297 |
| v1_wsigreg2 | 20 | 0.99214 | 0.987 | 0.99465 |
| v1_wsigreg2 | 30 | 0.99371 | 0.992 | 0.9955 |
| v1_wsigreg2 | 40 | 0.99459 | 0.99318 | 0.99628 |
| v1_wsigreg2 | 50 | 0.99586 | 0.99394 | 0.99728 |
| v1_wsigreg2 | 60 | 0.99444 | 0.98896 | 0.99665 |
| v1_wsigreg2 | 70 | 0.99555 | 0.99395 | 0.99709 |
| v1_wsigreg2 | 80 | 0.99501 | 0.99097 | 0.99682 |
| v1_wsigreg2 | 90 | 0.99664 | 0.99578 | 0.99737 |
| v1_wsigreg2 | 100 | 0.99582 | 0.9951 | 0.99627 |
| v1_wsigreg2 | 110 | 0.99646 | 0.99428 | 0.99752 |
| v1_wsigreg2 | 120 | 0.99684 | 0.99497 | 0.99795 |
| v1_wsigreg2 | 130 | 0.9972 | 0.99631 | 0.99801 |
| v1_wsigreg2 | 140 | 0.99741 | 0.99717 | 0.99766 |
| v1_wsigreg2 | 150 | 0.99744 | 0.99663 | 0.998 |
| v1_wsigreg2 | 160 | 0.99747 | 0.99719 | 0.99762 |
| v1_wsigreg2 | 170 | 0.998 | 0.99788 | 0.9981 |
| v1_wsigreg2 | 180 | 0.99777 | 0.99726 | 0.99818 |
| v1_wsigreg2 | 190 | 0.99696 | 0.99646 | 0.99807 |
| v1_wsigreg2 | 200 | 0.99777 | 0.99763 | 0.99787 |
| v1_wsigreg5 | 1 | 0.94726 | 0.93039 | 0.96169 |
| v1_wsigreg5 | 2 | 0.96599 | 0.90514 | 0.98726 |
| v1_wsigreg5 | 5 | 0.97603 | 0.9578 | 0.99266 |
| v1_wsigreg5 | 10 | 0.97974 | 0.97194 | 0.98648 |
| v1_wsigreg5 | 20 | 0.98832 | 0.98357 | 0.99314 |
| v1_wsigreg5 | 30 | 0.99046 | 0.98496 | 0.99338 |
| v1_wsigreg5 | 40 | 0.9927 | 0.99036 | 0.99492 |
| v1_wsigreg5 | 50 | 0.99323 | 0.99009 | 0.9954 |
| v1_wsigreg5 | 60 | 0.9927 | 0.99105 | 0.99432 |
| v1_wsigreg5 | 70 | 0.99215 | 0.98835 | 0.99552 |
| v1_wsigreg5 | 80 | 0.99364 | 0.99066 | 0.99551 |
| v1_wsigreg5 | 90 | 0.99538 | 0.99456 | 0.9962 |
| v1_wsigreg5 | 100 | 0.99467 | 0.99372 | 0.9959 |
| v1_wsigreg5 | 110 | 0.9949 | 0.99394 | 0.99618 |
| v1_wsigreg5 | 120 | 0.99531 | 0.99323 | 0.99654 |
| v1_wsigreg5 | 130 | 0.99614 | 0.99529 | 0.99659 |
| v1_wsigreg5 | 140 | 0.99578 | 0.99509 | 0.99695 |
| v1_wsigreg5 | 150 | 0.99677 | 0.99636 | 0.99716 |
| v1_wsigreg5 | 160 | 0.99674 | 0.99578 | 0.99741 |
| v1_wsigreg5 | 170 | 0.99707 | 0.99666 | 0.99741 |
| v1_wsigreg5 | 180 | 0.99701 | 0.99577 | 0.99768 |
| v1_wsigreg5 | 190 | 0.99634 | 0.99505 | 0.99699 |
| v1_wsigreg5 | 200 | 0.9971 | 0.99687 | 0.99758 |
| v1_latent32 | 1 | 0.97275 | 0.95252 | 0.98897 |
| v1_latent32 | 2 | 0.97759 | 0.95878 | 0.99301 |
| v1_latent32 | 5 | 0.98159 | 0.97647 | 0.98535 |
| v1_latent32 | 10 | 0.98468 | 0.97542 | 0.99489 |
| v1_latent32 | 20 | 0.99112 | 0.98599 | 0.99384 |
| v1_latent32 | 30 | 0.99401 | 0.99154 | 0.99601 |
| v1_latent32 | 40 | 0.99502 | 0.99033 | 0.99698 |
| v1_latent32 | 50 | 0.99462 | 0.99167 | 0.99656 |
| v1_latent32 | 60 | 0.9958 | 0.99405 | 0.99729 |
| v1_latent32 | 70 | 0.997 | 0.9956 | 0.99775 |
| v1_latent32 | 80 | 0.99735 | 0.99624 | 0.99821 |
| v1_latent32 | 90 | 0.99724 | 0.99687 | 0.9975 |
| v1_latent32 | 100 | 0.9968 | 0.99585 | 0.99754 |
| v1_latent32 | 110 | 0.99758 | 0.99664 | 0.99828 |
| v1_latent32 | 120 | 0.99779 | 0.99696 | 0.99839 |
| v1_latent32 | 130 | 0.99794 | 0.99659 | 0.99863 |
| v1_latent32 | 140 | 0.99799 | 0.99757 | 0.99853 |
| v1_latent32 | 150 | 0.99804 | 0.99748 | 0.99877 |
| v1_latent32 | 160 | 0.99815 | 0.99766 | 0.99844 |
| v1_latent32 | 170 | 0.99833 | 0.99788 | 0.99853 |
| v1_latent32 | 180 | 0.99819 | 0.99667 | 0.99868 |
| v1_latent32 | 190 | 0.99769 | 0.99656 | 0.99824 |
| v1_latent32 | 200 | 0.99843 | 0.99819 | 0.99865 |
| v1_ema | 1 | 0.97419 | 0.96164 | 0.98697 |
| v1_ema | 2 | 0.97652 | 0.96816 | 0.98276 |
| v1_ema | 5 | 0.98049 | 0.97004 | 0.99076 |
| v1_ema | 10 | 0.98593 | 0.97664 | 0.99354 |
| v1_ema | 20 | 0.98872 | 0.98595 | 0.99065 |
| v1_ema | 30 | 0.99029 | 0.98504 | 0.9934 |
| v1_ema | 40 | 0.991 | 0.98899 | 0.99323 |
| v1_ema | 50 | 0.99086 | 0.98741 | 0.99266 |
| v1_ema | 60 | 0.9901 | 0.98695 | 0.99345 |
| v1_ema | 70 | 0.9912 | 0.98851 | 0.99351 |
| v1_ema | 80 | 0.99229 | 0.9908 | 0.99349 |
| v1_ema | 90 | 0.9934 | 0.99199 | 0.99413 |
| v1_ema | 100 | 0.99179 | 0.98869 | 0.99404 |
| v1_ema | 110 | 0.9931 | 0.99175 | 0.99437 |
| v1_ema | 120 | 0.99226 | 0.9862 | 0.99438 |
| v1_ema | 130 | 0.99291 | 0.98949 | 0.9953 |
| v1_ema | 140 | 0.99345 | 0.98985 | 0.99517 |
| v1_ema | 150 | 0.99346 | 0.99132 | 0.9956 |
| v1_ema | 160 | 0.99336 | 0.99269 | 0.99474 |
| v1_ema | 170 | 0.99464 | 0.994 | 0.9953 |
| v1_ema | 180 | 0.99443 | 0.9935 | 0.99554 |
| v1_ema | 190 | 0.99251 | 0.99108 | 0.99439 |
| v1_ema | 200 | 0.99423 | 0.99324 | 0.99495 |
| v1_wground3 | 1 | 0.98183 | 0.97229 | 0.98774 |
| v1_wground3 | 2 | 0.97655 | 0.95334 | 0.99374 |
| v1_wground3 | 5 | 0.98501 | 0.97213 | 0.99551 |
| v1_wground3 | 10 | 0.98445 | 0.96805 | 0.99469 |
| v1_wground3 | 20 | 0.99152 | 0.98928 | 0.99407 |
| v1_wground3 | 30 | 0.9953 | 0.99222 | 0.99728 |
| v1_wground3 | 40 | 0.99541 | 0.99478 | 0.99732 |
| v1_wground3 | 50 | 0.99661 | 0.99554 | 0.9979 |
| v1_wground3 | 60 | 0.99573 | 0.99316 | 0.99788 |
| v1_wground3 | 70 | 0.99696 | 0.99578 | 0.99773 |
| v1_wground3 | 80 | 0.99752 | 0.99699 | 0.99821 |
| v1_wground3 | 90 | 0.99739 | 0.99671 | 0.99794 |
| v1_wground3 | 100 | 0.99734 | 0.99633 | 0.99816 |
| v1_wground3 | 110 | 0.99788 | 0.9976 | 0.99807 |
| v1_wground3 | 120 | 0.99812 | 0.998 | 0.99824 |
| v1_wground3 | 130 | 0.99791 | 0.99664 | 0.99856 |
| v1_wground3 | 140 | 0.99817 | 0.99802 | 0.99831 |
| v1_wground3 | 150 | 0.99823 | 0.99799 | 0.99836 |
| v1_wground3 | 160 | 0.99826 | 0.99801 | 0.99857 |
| v1_wground3 | 170 | 0.99848 | 0.99823 | 0.9986 |
| v1_wground3 | 180 | 0.99837 | 0.99769 | 0.99867 |
| v1_wground3 | 190 | 0.99796 | 0.99741 | 0.99855 |
| v1_wground3 | 200 | 0.99835 | 0.99796 | 0.99859 |

### P4 (data): grounding R2 of P_meson vs epoch

#### P4 table: R2 P_meson (mean, min, max over 5 seeds)

| rung | epoch | mean | min | max |
|---|---|---|---|---|
| v1_base | 1 | 0.80449 | 0.74928 | 0.84118 |
| v1_base | 2 | 0.86772 | 0.81737 | 0.90017 |
| v1_base | 5 | 0.93071 | 0.90295 | 0.95318 |
| v1_base | 10 | 0.95144 | 0.93077 | 0.96825 |
| v1_base | 20 | 0.9579 | 0.93217 | 0.96794 |
| v1_base | 30 | 0.96818 | 0.95936 | 0.97653 |
| v1_base | 40 | 0.96722 | 0.95558 | 0.97686 |
| v1_base | 50 | 0.96987 | 0.96558 | 0.97289 |
| v1_base | 60 | 0.97077 | 0.9596 | 0.9798 |
| v1_base | 70 | 0.97409 | 0.96495 | 0.98287 |
| v1_base | 80 | 0.97178 | 0.95883 | 0.98105 |
| v1_base | 90 | 0.97555 | 0.96765 | 0.98214 |
| v1_base | 100 | 0.98134 | 0.97845 | 0.98424 |
| v1_base | 110 | 0.97885 | 0.97296 | 0.98408 |
| v1_base | 120 | 0.97828 | 0.97337 | 0.98069 |
| v1_base | 130 | 0.98015 | 0.97877 | 0.98279 |
| v1_base | 140 | 0.98048 | 0.97305 | 0.98374 |
| v1_base | 150 | 0.97941 | 0.97396 | 0.98252 |
| v1_base | 160 | 0.98334 | 0.98116 | 0.98628 |
| v1_base | 170 | 0.98242 | 0.97748 | 0.9859 |
| v1_base | 180 | 0.98153 | 0.98075 | 0.98246 |
| v1_base | 190 | 0.98135 | 0.97839 | 0.98324 |
| v1_base | 200 | 0.98164 | 0.97786 | 0.98546 |
| v1_base_masked | 1 | 0.79797 | 0.73693 | 0.84309 |
| v1_base_masked | 2 | 0.88079 | 0.84751 | 0.91379 |
| v1_base_masked | 5 | 0.9304 | 0.89662 | 0.95132 |
| v1_base_masked | 10 | 0.95062 | 0.93388 | 0.96419 |
| v1_base_masked | 20 | 0.95645 | 0.92565 | 0.97015 |
| v1_base_masked | 30 | 0.96367 | 0.9503 | 0.97244 |
| v1_base_masked | 40 | 0.96879 | 0.96036 | 0.97697 |
| v1_base_masked | 50 | 0.96427 | 0.96033 | 0.97019 |
| v1_base_masked | 60 | 0.96519 | 0.95929 | 0.9686 |
| v1_base_masked | 70 | 0.972 | 0.96688 | 0.97608 |
| v1_base_masked | 80 | 0.96926 | 0.96237 | 0.97423 |
| v1_base_masked | 90 | 0.97287 | 0.9683 | 0.97653 |
| v1_base_masked | 100 | 0.9768 | 0.97476 | 0.98015 |
| v1_base_masked | 110 | 0.97634 | 0.96759 | 0.98017 |
| v1_base_masked | 120 | 0.97477 | 0.97135 | 0.9773 |
| v1_base_masked | 130 | 0.97409 | 0.96396 | 0.98111 |
| v1_base_masked | 140 | 0.97736 | 0.97039 | 0.98069 |
| v1_base_masked | 150 | 0.97809 | 0.97224 | 0.98074 |
| v1_base_masked | 160 | 0.98077 | 0.97706 | 0.98532 |
| v1_base_masked | 170 | 0.98053 | 0.97722 | 0.98353 |
| v1_base_masked | 180 | 0.97927 | 0.97677 | 0.98129 |
| v1_base_masked | 190 | 0.97956 | 0.97615 | 0.98187 |
| v1_base_masked | 200 | 0.97874 | 0.97523 | 0.98315 |
| v1_wsigreg2 | 1 | 0.77418 | 0.60743 | 0.8684 |
| v1_wsigreg2 | 2 | 0.8803 | 0.83918 | 0.91613 |
| v1_wsigreg2 | 5 | 0.91436 | 0.84935 | 0.94431 |
| v1_wsigreg2 | 10 | 0.94608 | 0.93373 | 0.95488 |
| v1_wsigreg2 | 20 | 0.95075 | 0.93534 | 0.95901 |
| v1_wsigreg2 | 30 | 0.94803 | 0.94281 | 0.95179 |
| v1_wsigreg2 | 40 | 0.95696 | 0.95154 | 0.96294 |
| v1_wsigreg2 | 50 | 0.95609 | 0.94896 | 0.96565 |
| v1_wsigreg2 | 60 | 0.95209 | 0.94259 | 0.96773 |
| v1_wsigreg2 | 70 | 0.95935 | 0.95116 | 0.96476 |
| v1_wsigreg2 | 80 | 0.96264 | 0.95635 | 0.96893 |
| v1_wsigreg2 | 90 | 0.96639 | 0.96172 | 0.9706 |
| v1_wsigreg2 | 100 | 0.96859 | 0.96585 | 0.97286 |
| v1_wsigreg2 | 110 | 0.97041 | 0.96464 | 0.97493 |
| v1_wsigreg2 | 120 | 0.97108 | 0.96775 | 0.97307 |
| v1_wsigreg2 | 130 | 0.97317 | 0.97062 | 0.97547 |
| v1_wsigreg2 | 140 | 0.97341 | 0.97127 | 0.97698 |
| v1_wsigreg2 | 150 | 0.97342 | 0.96894 | 0.97842 |
| v1_wsigreg2 | 160 | 0.97643 | 0.97271 | 0.97905 |
| v1_wsigreg2 | 170 | 0.97571 | 0.97096 | 0.97908 |
| v1_wsigreg2 | 180 | 0.9753 | 0.97178 | 0.9807 |
| v1_wsigreg2 | 190 | 0.97426 | 0.97285 | 0.97719 |
| v1_wsigreg2 | 200 | 0.97517 | 0.97205 | 0.97928 |
| v1_wsigreg5 | 1 | 0.65629 | 0.41364 | 0.86038 |
| v1_wsigreg5 | 2 | 0.84854 | 0.75842 | 0.9065 |
| v1_wsigreg5 | 5 | 0.88027 | 0.8428 | 0.91466 |
| v1_wsigreg5 | 10 | 0.88356 | 0.85134 | 0.92913 |
| v1_wsigreg5 | 20 | 0.91248 | 0.8805 | 0.94407 |
| v1_wsigreg5 | 30 | 0.9365 | 0.91426 | 0.94508 |
| v1_wsigreg5 | 40 | 0.94133 | 0.91798 | 0.9552 |
| v1_wsigreg5 | 50 | 0.9514 | 0.94288 | 0.96324 |
| v1_wsigreg5 | 60 | 0.94938 | 0.93521 | 0.95746 |
| v1_wsigreg5 | 70 | 0.95262 | 0.93894 | 0.95934 |
| v1_wsigreg5 | 80 | 0.95827 | 0.94891 | 0.96689 |
| v1_wsigreg5 | 90 | 0.95551 | 0.94714 | 0.96837 |
| v1_wsigreg5 | 100 | 0.96031 | 0.94402 | 0.97125 |
| v1_wsigreg5 | 110 | 0.96202 | 0.95636 | 0.96455 |
| v1_wsigreg5 | 120 | 0.96283 | 0.95724 | 0.96708 |
| v1_wsigreg5 | 130 | 0.96763 | 0.96472 | 0.96988 |
| v1_wsigreg5 | 140 | 0.96777 | 0.95789 | 0.97355 |
| v1_wsigreg5 | 150 | 0.96805 | 0.96356 | 0.971 |
| v1_wsigreg5 | 160 | 0.97022 | 0.96764 | 0.9726 |
| v1_wsigreg5 | 170 | 0.97037 | 0.96642 | 0.97354 |
| v1_wsigreg5 | 180 | 0.97063 | 0.96755 | 0.97573 |
| v1_wsigreg5 | 190 | 0.97033 | 0.96785 | 0.97199 |
| v1_wsigreg5 | 200 | 0.9718 | 0.96767 | 0.97456 |
| v1_latent32 | 1 | 0.8547 | 0.81631 | 0.88931 |
| v1_latent32 | 2 | 0.8511 | 0.66569 | 0.92517 |
| v1_latent32 | 5 | 0.93477 | 0.90092 | 0.96384 |
| v1_latent32 | 10 | 0.95867 | 0.95122 | 0.96382 |
| v1_latent32 | 20 | 0.96574 | 0.9598 | 0.97159 |
| v1_latent32 | 30 | 0.96756 | 0.96336 | 0.97159 |
| v1_latent32 | 40 | 0.97292 | 0.95973 | 0.98434 |
| v1_latent32 | 50 | 0.96266 | 0.96138 | 0.96497 |
| v1_latent32 | 60 | 0.96558 | 0.96034 | 0.97998 |
| v1_latent32 | 70 | 0.97739 | 0.96538 | 0.98198 |
| v1_latent32 | 80 | 0.97456 | 0.96543 | 0.98204 |
| v1_latent32 | 90 | 0.97381 | 0.96574 | 0.97841 |
| v1_latent32 | 100 | 0.98047 | 0.97593 | 0.98259 |
| v1_latent32 | 110 | 0.98094 | 0.97142 | 0.9863 |
| v1_latent32 | 120 | 0.97984 | 0.97458 | 0.9853 |
| v1_latent32 | 130 | 0.97924 | 0.96952 | 0.98531 |
| v1_latent32 | 140 | 0.98321 | 0.97331 | 0.98727 |
| v1_latent32 | 150 | 0.98254 | 0.97923 | 0.98676 |
| v1_latent32 | 160 | 0.98473 | 0.98324 | 0.98775 |
| v1_latent32 | 170 | 0.98458 | 0.97981 | 0.98762 |
| v1_latent32 | 180 | 0.98375 | 0.97961 | 0.98729 |
| v1_latent32 | 190 | 0.98329 | 0.98197 | 0.98594 |
| v1_latent32 | 200 | 0.98292 | 0.97725 | 0.98698 |
| v1_ema | 1 | 0.75318 | 0.52071 | 0.86912 |
| v1_ema | 2 | 0.89554 | 0.84802 | 0.93353 |
| v1_ema | 5 | 0.92764 | 0.89719 | 0.95657 |
| v1_ema | 10 | 0.91105 | 0.88353 | 0.92829 |
| v1_ema | 20 | 0.92467 | 0.90632 | 0.94053 |
| v1_ema | 30 | 0.94502 | 0.93041 | 0.95645 |
| v1_ema | 40 | 0.92456 | 0.87757 | 0.95182 |
| v1_ema | 50 | 0.93198 | 0.92236 | 0.94099 |
| v1_ema | 60 | 0.90822 | 0.85055 | 0.94919 |
| v1_ema | 70 | 0.91579 | 0.81033 | 0.9493 |
| v1_ema | 80 | 0.91127 | 0.79538 | 0.95548 |
| v1_ema | 90 | 0.91537 | 0.87122 | 0.95382 |
| v1_ema | 100 | 0.8991 | 0.82038 | 0.96481 |
| v1_ema | 110 | 0.91556 | 0.89118 | 0.95278 |
| v1_ema | 120 | 0.92939 | 0.89594 | 0.9588 |
| v1_ema | 130 | 0.86989 | 0.68538 | 0.95974 |
| v1_ema | 140 | 0.89082 | 0.80613 | 0.93191 |
| v1_ema | 150 | 0.92936 | 0.89761 | 0.95096 |
| v1_ema | 160 | 0.89857 | 0.86948 | 0.92753 |
| v1_ema | 170 | 0.92797 | 0.8906 | 0.96027 |
| v1_ema | 180 | 0.9283 | 0.89544 | 0.95453 |
| v1_ema | 190 | 0.92228 | 0.86209 | 0.96021 |
| v1_ema | 200 | 0.93085 | 0.91464 | 0.95215 |
| v1_wground3 | 1 | 0.85975 | 0.79108 | 0.9139 |
| v1_wground3 | 2 | 0.83726 | 0.77205 | 0.93745 |
| v1_wground3 | 5 | 0.93599 | 0.90441 | 0.958 |
| v1_wground3 | 10 | 0.95698 | 0.92823 | 0.9763 |
| v1_wground3 | 20 | 0.9571 | 0.92837 | 0.96826 |
| v1_wground3 | 30 | 0.96906 | 0.96056 | 0.97265 |
| v1_wground3 | 40 | 0.97311 | 0.96515 | 0.98302 |
| v1_wground3 | 50 | 0.97015 | 0.96447 | 0.97559 |
| v1_wground3 | 60 | 0.96874 | 0.9573 | 0.97909 |
| v1_wground3 | 70 | 0.97752 | 0.97014 | 0.98251 |
| v1_wground3 | 80 | 0.97968 | 0.97526 | 0.98231 |
| v1_wground3 | 90 | 0.9824 | 0.97612 | 0.9857 |
| v1_wground3 | 100 | 0.98346 | 0.98125 | 0.98487 |
| v1_wground3 | 110 | 0.98392 | 0.97798 | 0.98625 |
| v1_wground3 | 120 | 0.98294 | 0.98172 | 0.98447 |
| v1_wground3 | 130 | 0.98322 | 0.9784 | 0.98561 |
| v1_wground3 | 140 | 0.98348 | 0.9764 | 0.98879 |
| v1_wground3 | 150 | 0.98464 | 0.98141 | 0.98712 |
| v1_wground3 | 160 | 0.98632 | 0.9845 | 0.98989 |
| v1_wground3 | 170 | 0.98655 | 0.98414 | 0.98834 |
| v1_wground3 | 180 | 0.98556 | 0.98417 | 0.98847 |
| v1_wground3 | 190 | 0.9853 | 0.98282 | 0.98717 |
| v1_wground3 | 200 | 0.98587 | 0.98338 | 0.98864 |

### P5 (data): grounding R2 of P_baryonic vs epoch

#### P5 table: R2 P_baryonic (mean, min, max over 5 seeds)

| rung | epoch | mean | min | max |
|---|---|---|---|---|
| v1_base | 1 | 0.97442 | 0.96931 | 0.98253 |
| v1_base | 2 | 0.98497 | 0.97701 | 0.99098 |
| v1_base | 5 | 0.98971 | 0.98158 | 0.99489 |
| v1_base | 10 | 0.98895 | 0.98321 | 0.99403 |
| v1_base | 20 | 0.98995 | 0.98705 | 0.99331 |
| v1_base | 30 | 0.99199 | 0.98482 | 0.99555 |
| v1_base | 40 | 0.99412 | 0.99319 | 0.99585 |
| v1_base | 50 | 0.99478 | 0.99123 | 0.99601 |
| v1_base | 60 | 0.99501 | 0.99396 | 0.99623 |
| v1_base | 70 | 0.99577 | 0.99519 | 0.99683 |
| v1_base | 80 | 0.99543 | 0.99439 | 0.99708 |
| v1_base | 90 | 0.99645 | 0.99538 | 0.99713 |
| v1_base | 100 | 0.99687 | 0.99669 | 0.99731 |
| v1_base | 110 | 0.99648 | 0.9948 | 0.9971 |
| v1_base | 120 | 0.99661 | 0.99553 | 0.99759 |
| v1_base | 130 | 0.9969 | 0.99601 | 0.99766 |
| v1_base | 140 | 0.99671 | 0.9955 | 0.99743 |
| v1_base | 150 | 0.99668 | 0.99508 | 0.99723 |
| v1_base | 160 | 0.99705 | 0.99612 | 0.99772 |
| v1_base | 170 | 0.99709 | 0.99655 | 0.99758 |
| v1_base | 180 | 0.99697 | 0.99477 | 0.99796 |
| v1_base | 190 | 0.99597 | 0.99308 | 0.99696 |
| v1_base | 200 | 0.99732 | 0.99707 | 0.99759 |
| v1_base_masked | 1 | 0.97511 | 0.97027 | 0.98313 |
| v1_base_masked | 2 | 0.98559 | 0.9783 | 0.99179 |
| v1_base_masked | 5 | 0.98601 | 0.97793 | 0.99335 |
| v1_base_masked | 10 | 0.98805 | 0.98465 | 0.99152 |
| v1_base_masked | 20 | 0.99058 | 0.98694 | 0.99351 |
| v1_base_masked | 30 | 0.99194 | 0.98633 | 0.99587 |
| v1_base_masked | 40 | 0.99379 | 0.99313 | 0.99519 |
| v1_base_masked | 50 | 0.99387 | 0.99162 | 0.99526 |
| v1_base_masked | 60 | 0.99416 | 0.99269 | 0.99509 |
| v1_base_masked | 70 | 0.99475 | 0.99268 | 0.99697 |
| v1_base_masked | 80 | 0.99514 | 0.99453 | 0.99562 |
| v1_base_masked | 90 | 0.99483 | 0.99378 | 0.99632 |
| v1_base_masked | 100 | 0.99497 | 0.99218 | 0.99698 |
| v1_base_masked | 110 | 0.99581 | 0.99435 | 0.99704 |
| v1_base_masked | 120 | 0.99624 | 0.99513 | 0.99696 |
| v1_base_masked | 130 | 0.99575 | 0.99401 | 0.99692 |
| v1_base_masked | 140 | 0.99596 | 0.99398 | 0.99729 |
| v1_base_masked | 150 | 0.99674 | 0.99647 | 0.99732 |
| v1_base_masked | 160 | 0.9967 | 0.99612 | 0.99698 |
| v1_base_masked | 170 | 0.99674 | 0.99641 | 0.99729 |
| v1_base_masked | 180 | 0.99718 | 0.99683 | 0.99764 |
| v1_base_masked | 190 | 0.99641 | 0.99557 | 0.99705 |
| v1_base_masked | 200 | 0.99706 | 0.99679 | 0.99754 |
| v1_wsigreg2 | 1 | 0.97808 | 0.97182 | 0.98486 |
| v1_wsigreg2 | 2 | 0.9839 | 0.97819 | 0.98817 |
| v1_wsigreg2 | 5 | 0.98832 | 0.98232 | 0.99076 |
| v1_wsigreg2 | 10 | 0.98542 | 0.97561 | 0.99228 |
| v1_wsigreg2 | 20 | 0.99117 | 0.98595 | 0.99391 |
| v1_wsigreg2 | 30 | 0.9903 | 0.98491 | 0.99286 |
| v1_wsigreg2 | 40 | 0.99249 | 0.9907 | 0.99453 |
| v1_wsigreg2 | 50 | 0.99309 | 0.99131 | 0.99455 |
| v1_wsigreg2 | 60 | 0.9938 | 0.99082 | 0.99483 |
| v1_wsigreg2 | 70 | 0.99526 | 0.99306 | 0.99611 |
| v1_wsigreg2 | 80 | 0.99543 | 0.99463 | 0.99647 |
| v1_wsigreg2 | 90 | 0.99558 | 0.99467 | 0.99635 |
| v1_wsigreg2 | 100 | 0.99607 | 0.99556 | 0.9964 |
| v1_wsigreg2 | 110 | 0.99574 | 0.99468 | 0.9969 |
| v1_wsigreg2 | 120 | 0.99532 | 0.99477 | 0.99607 |
| v1_wsigreg2 | 130 | 0.99596 | 0.99482 | 0.99744 |
| v1_wsigreg2 | 140 | 0.99631 | 0.99468 | 0.99684 |
| v1_wsigreg2 | 150 | 0.99673 | 0.99622 | 0.997 |
| v1_wsigreg2 | 160 | 0.99671 | 0.99632 | 0.99707 |
| v1_wsigreg2 | 170 | 0.99627 | 0.99565 | 0.99736 |
| v1_wsigreg2 | 180 | 0.99703 | 0.99612 | 0.9974 |
| v1_wsigreg2 | 190 | 0.99614 | 0.99574 | 0.99674 |
| v1_wsigreg2 | 200 | 0.99685 | 0.99654 | 0.99719 |
| v1_wsigreg5 | 1 | 0.96748 | 0.95402 | 0.97205 |
| v1_wsigreg5 | 2 | 0.97498 | 0.96486 | 0.98002 |
| v1_wsigreg5 | 5 | 0.98446 | 0.98211 | 0.98711 |
| v1_wsigreg5 | 10 | 0.98017 | 0.97114 | 0.98908 |
| v1_wsigreg5 | 20 | 0.98817 | 0.98358 | 0.99189 |
| v1_wsigreg5 | 30 | 0.99112 | 0.98875 | 0.99322 |
| v1_wsigreg5 | 40 | 0.99165 | 0.98725 | 0.99316 |
| v1_wsigreg5 | 50 | 0.99291 | 0.99222 | 0.99365 |
| v1_wsigreg5 | 60 | 0.99307 | 0.99001 | 0.99534 |
| v1_wsigreg5 | 70 | 0.99416 | 0.99319 | 0.99535 |
| v1_wsigreg5 | 80 | 0.99298 | 0.99198 | 0.99425 |
| v1_wsigreg5 | 90 | 0.99423 | 0.99257 | 0.99577 |
| v1_wsigreg5 | 100 | 0.99432 | 0.99305 | 0.99566 |
| v1_wsigreg5 | 110 | 0.99448 | 0.99384 | 0.99568 |
| v1_wsigreg5 | 120 | 0.99463 | 0.993 | 0.99634 |
| v1_wsigreg5 | 130 | 0.99521 | 0.99417 | 0.99634 |
| v1_wsigreg5 | 140 | 0.99539 | 0.99477 | 0.99581 |
| v1_wsigreg5 | 150 | 0.99567 | 0.99506 | 0.99639 |
| v1_wsigreg5 | 160 | 0.99546 | 0.99466 | 0.99611 |
| v1_wsigreg5 | 170 | 0.99582 | 0.99527 | 0.99649 |
| v1_wsigreg5 | 180 | 0.99631 | 0.99588 | 0.99671 |
| v1_wsigreg5 | 190 | 0.99575 | 0.99493 | 0.99637 |
| v1_wsigreg5 | 200 | 0.99627 | 0.99573 | 0.99678 |
| v1_latent32 | 1 | 0.98021 | 0.96775 | 0.98881 |
| v1_latent32 | 2 | 0.98822 | 0.97716 | 0.9935 |
| v1_latent32 | 5 | 0.98657 | 0.97505 | 0.994 |
| v1_latent32 | 10 | 0.98559 | 0.97389 | 0.99428 |
| v1_latent32 | 20 | 0.99246 | 0.98897 | 0.99539 |
| v1_latent32 | 30 | 0.99356 | 0.99027 | 0.99577 |
| v1_latent32 | 40 | 0.99403 | 0.99349 | 0.99501 |
| v1_latent32 | 50 | 0.99468 | 0.99402 | 0.99509 |
| v1_latent32 | 60 | 0.99509 | 0.99386 | 0.99611 |
| v1_latent32 | 70 | 0.99555 | 0.99434 | 0.99626 |
| v1_latent32 | 80 | 0.99559 | 0.99471 | 0.99675 |
| v1_latent32 | 90 | 0.99547 | 0.99438 | 0.99624 |
| v1_latent32 | 100 | 0.99646 | 0.99622 | 0.99674 |
| v1_latent32 | 110 | 0.99649 | 0.99573 | 0.99772 |
| v1_latent32 | 120 | 0.99682 | 0.99632 | 0.99724 |
| v1_latent32 | 130 | 0.99677 | 0.99585 | 0.99786 |
| v1_latent32 | 140 | 0.99677 | 0.99514 | 0.99767 |
| v1_latent32 | 150 | 0.9971 | 0.99674 | 0.99733 |
| v1_latent32 | 160 | 0.99715 | 0.99664 | 0.99793 |
| v1_latent32 | 170 | 0.99715 | 0.99609 | 0.99769 |
| v1_latent32 | 180 | 0.99742 | 0.99648 | 0.99792 |
| v1_latent32 | 190 | 0.99663 | 0.99535 | 0.99729 |
| v1_latent32 | 200 | 0.99732 | 0.99707 | 0.99751 |
| v1_ema | 1 | 0.97786 | 0.96733 | 0.98783 |
| v1_ema | 2 | 0.9852 | 0.9764 | 0.9919 |
| v1_ema | 5 | 0.9874 | 0.98396 | 0.99182 |
| v1_ema | 10 | 0.98837 | 0.97993 | 0.99345 |
| v1_ema | 20 | 0.9886 | 0.97972 | 0.99308 |
| v1_ema | 30 | 0.99093 | 0.98578 | 0.99308 |
| v1_ema | 40 | 0.99088 | 0.98741 | 0.9931 |
| v1_ema | 50 | 0.991 | 0.98873 | 0.99262 |
| v1_ema | 60 | 0.99185 | 0.99033 | 0.99397 |
| v1_ema | 70 | 0.99319 | 0.9925 | 0.99403 |
| v1_ema | 80 | 0.99263 | 0.99178 | 0.99363 |
| v1_ema | 90 | 0.99266 | 0.99074 | 0.99479 |
| v1_ema | 100 | 0.99317 | 0.99243 | 0.99392 |
| v1_ema | 110 | 0.9931 | 0.99073 | 0.99439 |
| v1_ema | 120 | 0.99333 | 0.99186 | 0.99414 |
| v1_ema | 130 | 0.99363 | 0.99154 | 0.99539 |
| v1_ema | 140 | 0.99309 | 0.99172 | 0.99533 |
| v1_ema | 150 | 0.99424 | 0.9938 | 0.99461 |
| v1_ema | 160 | 0.99407 | 0.99262 | 0.99566 |
| v1_ema | 170 | 0.99383 | 0.99167 | 0.9949 |
| v1_ema | 180 | 0.99474 | 0.99346 | 0.99575 |
| v1_ema | 190 | 0.9936 | 0.99146 | 0.99485 |
| v1_ema | 200 | 0.99451 | 0.99347 | 0.99536 |
| v1_wground3 | 1 | 0.96555 | 0.92737 | 0.98608 |
| v1_wground3 | 2 | 0.98347 | 0.96454 | 0.99386 |
| v1_wground3 | 5 | 0.98665 | 0.97873 | 0.99215 |
| v1_wground3 | 10 | 0.99004 | 0.98528 | 0.99331 |
| v1_wground3 | 20 | 0.98741 | 0.97575 | 0.99491 |
| v1_wground3 | 30 | 0.99382 | 0.99161 | 0.99557 |
| v1_wground3 | 40 | 0.99531 | 0.99394 | 0.9968 |
| v1_wground3 | 50 | 0.99526 | 0.99406 | 0.99607 |
| v1_wground3 | 60 | 0.99511 | 0.99332 | 0.99655 |
| v1_wground3 | 70 | 0.9957 | 0.99478 | 0.99631 |
| v1_wground3 | 80 | 0.99574 | 0.99529 | 0.99616 |
| v1_wground3 | 90 | 0.99638 | 0.99585 | 0.99678 |
| v1_wground3 | 100 | 0.99672 | 0.99597 | 0.99736 |
| v1_wground3 | 110 | 0.99631 | 0.99441 | 0.99756 |
| v1_wground3 | 120 | 0.99673 | 0.99618 | 0.99726 |
| v1_wground3 | 130 | 0.99675 | 0.99419 | 0.99793 |
| v1_wground3 | 140 | 0.9967 | 0.99541 | 0.99773 |
| v1_wground3 | 150 | 0.9972 | 0.99648 | 0.99766 |
| v1_wground3 | 160 | 0.99696 | 0.99616 | 0.99777 |
| v1_wground3 | 170 | 0.99718 | 0.99632 | 0.99789 |
| v1_wground3 | 180 | 0.99741 | 0.99652 | 0.99822 |
| v1_wground3 | 190 | 0.99636 | 0.99536 | 0.99787 |
| v1_wground3 | 200 | 0.99758 | 0.99717 | 0.99796 |

### P6 (data): semigroup residual vs epoch (draw on a log y axis)

#### P6 table: semigroup_resid (mean, min, max over 5 seeds)

| rung | epoch | mean | min | max |
|---|---|---|---|---|
| v1_base | 1 | 0.0019933 | 0.0014529 | 0.0026045 |
| v1_base | 2 | 0.0013408 | 0.0010832 | 0.0016667 |
| v1_base | 5 | 0.0010233 | 0.00053618 | 0.0015421 |
| v1_base | 10 | 0.00093611 | 0.0005316 | 0.0013653 |
| v1_base | 20 | 0.00062066 | 0.00046889 | 0.00085259 |
| v1_base | 30 | 0.00083513 | 0.00057164 | 0.0010809 |
| v1_base | 40 | 0.0015738 | 0.0013394 | 0.0017612 |
| v1_base | 50 | 0.0018855 | 0.0011199 | 0.0025734 |
| v1_base | 60 | 0.0016208 | 0.0012594 | 0.0019069 |
| v1_base | 70 | 0.0018426 | 0.0010267 | 0.002575 |
| v1_base | 80 | 0.0017434 | 0.0014184 | 0.0019348 |
| v1_base | 90 | 0.0023342 | 0.0014398 | 0.0038581 |
| v1_base | 100 | 0.001989 | 0.0014734 | 0.0025757 |
| v1_base | 110 | 0.0021426 | 0.0014336 | 0.0032029 |
| v1_base | 120 | 0.0021349 | 0.00143 | 0.0031703 |
| v1_base | 130 | 0.0023603 | 0.0017103 | 0.0034278 |
| v1_base | 140 | 0.0024624 | 0.0017088 | 0.0033787 |
| v1_base | 150 | 0.0023037 | 0.0017423 | 0.0029386 |
| v1_base | 160 | 0.0024107 | 0.0015198 | 0.0032765 |
| v1_base | 170 | 0.002513 | 0.0019334 | 0.003363 |
| v1_base | 180 | 0.0024762 | 0.0018837 | 0.003296 |
| v1_base | 190 | 0.0025737 | 0.0019797 | 0.0033205 |
| v1_base | 200 | 0.002591 | 0.0018857 | 0.0032928 |
| v1_base_masked | 1 | 0.0019285 | 0.0015303 | 0.0023971 |
| v1_base_masked | 2 | 0.0011698 | 0.00089876 | 0.0015673 |
| v1_base_masked | 5 | 0.00084387 | 0.00052225 | 0.00099726 |
| v1_base_masked | 10 | 0.00071663 | 0.00042522 | 0.0010051 |
| v1_base_masked | 20 | 0.00048998 | 0.00029051 | 0.00085215 |
| v1_base_masked | 30 | 0.00044983 | 0.00023374 | 0.00079301 |
| v1_base_masked | 40 | 0.00035015 | 0.00026079 | 0.000403 |
| v1_base_masked | 50 | 0.00046691 | 0.00038608 | 0.00055071 |
| v1_base_masked | 60 | 0.00034982 | 0.00025206 | 0.00041951 |
| v1_base_masked | 70 | 0.00036795 | 0.00023679 | 0.00043348 |
| v1_base_masked | 80 | 0.00028571 | 0.00022608 | 0.00034003 |
| v1_base_masked | 90 | 0.00033639 | 0.00027183 | 0.00042112 |
| v1_base_masked | 100 | 0.00037319 | 0.00026614 | 0.00045244 |
| v1_base_masked | 110 | 0.0003169 | 0.00024205 | 0.00043143 |
| v1_base_masked | 120 | 0.00030473 | 0.00026495 | 0.00038085 |
| v1_base_masked | 130 | 0.00027951 | 0.00025688 | 0.00030784 |
| v1_base_masked | 140 | 0.00026592 | 0.00022621 | 0.00030567 |
| v1_base_masked | 150 | 0.00024042 | 0.00021092 | 0.00028479 |
| v1_base_masked | 160 | 0.00023535 | 0.00021673 | 0.0002689 |
| v1_base_masked | 170 | 0.00021958 | 0.00020275 | 0.00024705 |
| v1_base_masked | 180 | 0.00021184 | 0.0001776 | 0.00025241 |
| v1_base_masked | 190 | 0.00021409 | 0.0001924 | 0.0002421 |
| v1_base_masked | 200 | 0.00020667 | 0.00018148 | 0.00024869 |
| v1_wsigreg2 | 1 | 0.0029653 | 0.0019521 | 0.0053511 |
| v1_wsigreg2 | 2 | 0.0016841 | 0.0010254 | 0.0021388 |
| v1_wsigreg2 | 5 | 0.0015654 | 0.0010345 | 0.0020615 |
| v1_wsigreg2 | 10 | 0.0016931 | 0.0014364 | 0.0018146 |
| v1_wsigreg2 | 20 | 0.002299 | 0.0020228 | 0.002558 |
| v1_wsigreg2 | 30 | 0.003904 | 0.0029535 | 0.0043758 |
| v1_wsigreg2 | 40 | 0.0045804 | 0.0039269 | 0.0052519 |
| v1_wsigreg2 | 50 | 0.0046414 | 0.0040813 | 0.0053715 |
| v1_wsigreg2 | 60 | 0.0044642 | 0.0038509 | 0.0049352 |
| v1_wsigreg2 | 70 | 0.0046707 | 0.0035249 | 0.0054666 |
| v1_wsigreg2 | 80 | 0.0042152 | 0.0035759 | 0.0046813 |
| v1_wsigreg2 | 90 | 0.004668 | 0.0039209 | 0.0052117 |
| v1_wsigreg2 | 100 | 0.0044949 | 0.0032868 | 0.0052471 |
| v1_wsigreg2 | 110 | 0.0044341 | 0.0035417 | 0.0058469 |
| v1_wsigreg2 | 120 | 0.0044364 | 0.0036788 | 0.0054988 |
| v1_wsigreg2 | 130 | 0.0043981 | 0.003772 | 0.0055365 |
| v1_wsigreg2 | 140 | 0.0043561 | 0.003472 | 0.0054084 |
| v1_wsigreg2 | 150 | 0.0040301 | 0.0033786 | 0.0056829 |
| v1_wsigreg2 | 160 | 0.004281 | 0.0034445 | 0.0057711 |
| v1_wsigreg2 | 170 | 0.0042675 | 0.0035291 | 0.0055968 |
| v1_wsigreg2 | 180 | 0.0043062 | 0.0034901 | 0.0054239 |
| v1_wsigreg2 | 190 | 0.004439 | 0.0035307 | 0.0057029 |
| v1_wsigreg2 | 200 | 0.0043172 | 0.0034857 | 0.0053439 |
| v1_wsigreg5 | 1 | 0.0044149 | 0.0037256 | 0.0050423 |
| v1_wsigreg5 | 2 | 0.0031831 | 0.0024233 | 0.0036899 |
| v1_wsigreg5 | 5 | 0.0031328 | 0.0028561 | 0.0035399 |
| v1_wsigreg5 | 10 | 0.0037157 | 0.0024879 | 0.0050561 |
| v1_wsigreg5 | 20 | 0.0064448 | 0.0050065 | 0.0087621 |
| v1_wsigreg5 | 30 | 0.0068022 | 0.0057584 | 0.007449 |
| v1_wsigreg5 | 40 | 0.0067873 | 0.006117 | 0.0072198 |
| v1_wsigreg5 | 50 | 0.0071172 | 0.0061723 | 0.0079654 |
| v1_wsigreg5 | 60 | 0.0068143 | 0.0051865 | 0.0094564 |
| v1_wsigreg5 | 70 | 0.0071798 | 0.0055743 | 0.0098199 |
| v1_wsigreg5 | 80 | 0.0073735 | 0.0056974 | 0.0095541 |
| v1_wsigreg5 | 90 | 0.0073974 | 0.0059028 | 0.00958 |
| v1_wsigreg5 | 100 | 0.0072791 | 0.0058033 | 0.0099814 |
| v1_wsigreg5 | 110 | 0.0070159 | 0.0052621 | 0.0091018 |
| v1_wsigreg5 | 120 | 0.0069871 | 0.0061829 | 0.0084064 |
| v1_wsigreg5 | 130 | 0.0067884 | 0.0054326 | 0.0078512 |
| v1_wsigreg5 | 140 | 0.007003 | 0.0058555 | 0.0079152 |
| v1_wsigreg5 | 150 | 0.0070984 | 0.005623 | 0.0084641 |
| v1_wsigreg5 | 160 | 0.0073683 | 0.0061325 | 0.0084126 |
| v1_wsigreg5 | 170 | 0.007365 | 0.0060584 | 0.0081048 |
| v1_wsigreg5 | 180 | 0.0074979 | 0.0063686 | 0.0086039 |
| v1_wsigreg5 | 190 | 0.0072703 | 0.006018 | 0.0082384 |
| v1_wsigreg5 | 200 | 0.0074137 | 0.0062859 | 0.0084698 |
| v1_latent32 | 1 | 0.0017112 | 0.0012284 | 0.0024575 |
| v1_latent32 | 2 | 0.0013658 | 0.00090905 | 0.0023586 |
| v1_latent32 | 5 | 0.0010548 | 0.00053248 | 0.0018233 |
| v1_latent32 | 10 | 0.0010217 | 0.00051441 | 0.0014401 |
| v1_latent32 | 20 | 0.00075332 | 0.00042128 | 0.0010865 |
| v1_latent32 | 30 | 0.00087509 | 0.00055085 | 0.0011069 |
| v1_latent32 | 40 | 0.0015958 | 0.0013269 | 0.0023504 |
| v1_latent32 | 50 | 0.0019203 | 0.0010788 | 0.002644 |
| v1_latent32 | 60 | 0.0017784 | 0.0012194 | 0.0030265 |
| v1_latent32 | 70 | 0.0018211 | 0.001198 | 0.0023387 |
| v1_latent32 | 80 | 0.002039 | 0.0012528 | 0.0036137 |
| v1_latent32 | 90 | 0.0024828 | 0.0015362 | 0.004783 |
| v1_latent32 | 100 | 0.0022059 | 0.0014136 | 0.0036351 |
| v1_latent32 | 110 | 0.0022905 | 0.0014005 | 0.0036534 |
| v1_latent32 | 120 | 0.0022713 | 0.0014317 | 0.0035687 |
| v1_latent32 | 130 | 0.0025878 | 0.0016845 | 0.004534 |
| v1_latent32 | 140 | 0.0024563 | 0.0014559 | 0.0043952 |
| v1_latent32 | 150 | 0.0022157 | 0.0015191 | 0.0036486 |
| v1_latent32 | 160 | 0.0025051 | 0.0013836 | 0.0045311 |
| v1_latent32 | 170 | 0.0023853 | 0.0014527 | 0.0043615 |
| v1_latent32 | 180 | 0.0024843 | 0.0014174 | 0.0045985 |
| v1_latent32 | 190 | 0.0025029 | 0.0015706 | 0.0047114 |
| v1_latent32 | 200 | 0.0025595 | 0.0015498 | 0.0047161 |
| v1_ema | 1 | 0.031752 | 0.025083 | 0.036753 |
| v1_ema | 2 | 0.011242 | 0.0092822 | 0.013452 |
| v1_ema | 5 | 0.0057388 | 0.0053038 | 0.006243 |
| v1_ema | 10 | 0.012487 | 0.011838 | 0.013198 |
| v1_ema | 20 | 0.014758 | 0.012715 | 0.0188 |
| v1_ema | 30 | 0.014354 | 0.013705 | 0.015089 |
| v1_ema | 40 | 0.015197 | 0.013543 | 0.016165 |
| v1_ema | 50 | 0.01516 | 0.013767 | 0.018718 |
| v1_ema | 60 | 0.017813 | 0.015398 | 0.020605 |
| v1_ema | 70 | 0.015642 | 0.012682 | 0.018977 |
| v1_ema | 80 | 0.018045 | 0.015966 | 0.019942 |
| v1_ema | 90 | 0.017302 | 0.014597 | 0.019332 |
| v1_ema | 100 | 0.016907 | 0.015804 | 0.017945 |
| v1_ema | 110 | 0.017599 | 0.015887 | 0.020451 |
| v1_ema | 120 | 0.017802 | 0.015683 | 0.020357 |
| v1_ema | 130 | 0.01721 | 0.013867 | 0.021196 |
| v1_ema | 140 | 0.01801 | 0.014535 | 0.02267 |
| v1_ema | 150 | 0.018413 | 0.014605 | 0.02415 |
| v1_ema | 160 | 0.017449 | 0.014876 | 0.022017 |
| v1_ema | 170 | 0.017727 | 0.013843 | 0.023468 |
| v1_ema | 180 | 0.017861 | 0.014673 | 0.024563 |
| v1_ema | 190 | 0.017256 | 0.013639 | 0.022009 |
| v1_ema | 200 | 0.018383 | 0.015838 | 0.022098 |
| v1_wground3 | 1 | 0.0024653 | 0.0018363 | 0.003343 |
| v1_wground3 | 2 | 0.001292 | 0.0011167 | 0.0015297 |
| v1_wground3 | 5 | 0.0016253 | 0.00065811 | 0.002671 |
| v1_wground3 | 10 | 0.00097448 | 0.00068663 | 0.0013451 |
| v1_wground3 | 20 | 0.00087799 | 0.000587 | 0.0011963 |
| v1_wground3 | 30 | 0.001151 | 0.0006952 | 0.001753 |
| v1_wground3 | 40 | 0.0018192 | 0.001103 | 0.0028589 |
| v1_wground3 | 50 | 0.0027288 | 0.002375 | 0.0032048 |
| v1_wground3 | 60 | 0.0035612 | 0.0028346 | 0.0048107 |
| v1_wground3 | 70 | 0.0031612 | 0.0027539 | 0.0041407 |
| v1_wground3 | 80 | 0.0037026 | 0.0023411 | 0.0057429 |
| v1_wground3 | 90 | 0.003919 | 0.0021921 | 0.0063147 |
| v1_wground3 | 100 | 0.003629 | 0.0026513 | 0.0066463 |
| v1_wground3 | 110 | 0.0037839 | 0.0025034 | 0.0059065 |
| v1_wground3 | 120 | 0.0036386 | 0.0024207 | 0.0061527 |
| v1_wground3 | 130 | 0.0035591 | 0.0022992 | 0.0060229 |
| v1_wground3 | 140 | 0.0035229 | 0.0022502 | 0.0061133 |
| v1_wground3 | 150 | 0.0034268 | 0.002246 | 0.0060942 |
| v1_wground3 | 160 | 0.003611 | 0.0023155 | 0.00666 |
| v1_wground3 | 170 | 0.0036223 | 0.0022736 | 0.0069059 |
| v1_wground3 | 180 | 0.0036848 | 0.0023241 | 0.0069323 |
| v1_wground3 | 190 | 0.0038434 | 0.0023027 | 0.0075099 |
| v1_wground3 | 200 | 0.0037433 | 0.0023 | 0.0069369 |

### P7 (data): training losses vs epoch, seed mean per rung

| rung | epoch | pred | sigreg | ground | semigroup | total |
|---|---|---|---|---|---|---|
| v1_base | 1 | 0.022474 | 0.13863 | 0.076963 | 0.0040497 | 0.16916 |
| v1_base | 2 | 0.011561 | 0.099511 | 0.054046 | 0.00069875 | 0.11543 |
| v1_base | 5 | 0.0094214 | 0.069816 | 0.051406 | 0.00057442 | 0.095793 |
| v1_base | 10 | 0.0072246 | 0.062083 | 0.049386 | 0.00049081 | 0.087702 |
| v1_base | 20 | 0.0059457 | 0.055835 | 0.046981 | 0.00045292 | 0.08089 |
| v1_base | 30 | 0.0055338 | 0.048932 | 0.04569 | 0.00065838 | 0.075756 |
| v1_base | 40 | 0.006281 | 0.040941 | 0.044774 | 0.00089173 | 0.071615 |
| v1_base | 50 | 0.0059697 | 0.038768 | 0.044185 | 0.00084728 | 0.069623 |
| v1_base | 60 | 0.0057057 | 0.037851 | 0.043707 | 0.00081797 | 0.06842 |
| v1_base | 70 | 0.0055243 | 0.036795 | 0.043195 | 0.00079967 | 0.067197 |
| v1_base | 80 | 0.0052771 | 0.036055 | 0.042996 | 0.00077339 | 0.066378 |
| v1_base | 90 | 0.0051633 | 0.035558 | 0.042642 | 0.00076353 | 0.065661 |
| v1_base | 100 | 0.0051182 | 0.035043 | 0.042389 | 0.00074362 | 0.065103 |
| v1_base | 110 | 0.0048491 | 0.034524 | 0.04201 | 0.00071107 | 0.064192 |
| v1_base | 120 | 0.0048605 | 0.034031 | 0.041787 | 0.00071281 | 0.063734 |
| v1_base | 130 | 0.0047558 | 0.033475 | 0.041709 | 0.00069499 | 0.063272 |
| v1_base | 140 | 0.0045825 | 0.033326 | 0.04125 | 0.00068119 | 0.062564 |
| v1_base | 150 | 0.0045091 | 0.032728 | 0.041013 | 0.00066903 | 0.061953 |
| v1_base | 160 | 0.0044204 | 0.032333 | 0.040942 | 0.00065042 | 0.061594 |
| v1_base | 170 | 0.0043859 | 0.03217 | 0.040743 | 0.0006444 | 0.061278 |
| v1_base | 180 | 0.004277 | 0.032002 | 0.040637 | 0.00063505 | 0.060979 |
| v1_base | 190 | 0.0042632 | 0.031992 | 0.040451 | 0.00063458 | 0.060774 |
| v1_base | 200 | 0.004292 | 0.032281 | 0.040567 | 0.0006352 | 0.061063 |
| v1_base_masked | 1 | 0.022554 | 0.13912 | 0.077002 | 0.0040542 | 0.16952 |
| v1_base_masked | 2 | 0.011395 | 0.10246 | 0.054085 | 0.00064694 | 0.11677 |
| v1_base_masked | 5 | 0.010427 | 0.073018 | 0.051618 | 0.00047566 | 0.098602 |
| v1_base_masked | 10 | 0.008613 | 0.065756 | 0.049458 | 0.00036064 | 0.090985 |
| v1_base_masked | 20 | 0.0076825 | 0.059115 | 0.047012 | 0.00030117 | 0.084282 |
| v1_base_masked | 30 | 0.0072466 | 0.056082 | 0.045693 | 0.00031189 | 0.081012 |
| v1_base_masked | 40 | 0.0069614 | 0.054733 | 0.044834 | 0.00028085 | 0.07919 |
| v1_base_masked | 50 | 0.0069318 | 0.053609 | 0.044236 | 0.00027463 | 0.078 |
| v1_base_masked | 60 | 0.0069398 | 0.05244 | 0.043757 | 0.00028906 | 0.076945 |
| v1_base_masked | 70 | 0.0068013 | 0.051493 | 0.043271 | 0.00027558 | 0.075847 |
| v1_base_masked | 80 | 0.0068662 | 0.050272 | 0.043036 | 0.00027041 | 0.075065 |
| v1_base_masked | 90 | 0.0071285 | 0.048751 | 0.042666 | 0.00027887 | 0.074198 |
| v1_base_masked | 100 | 0.0072199 | 0.0477 | 0.042418 | 0.00027157 | 0.073515 |
| v1_base_masked | 110 | 0.0072235 | 0.046728 | 0.041991 | 0.00025061 | 0.072604 |
| v1_base_masked | 120 | 0.0071259 | 0.045931 | 0.041742 | 0.00025038 | 0.071858 |
| v1_base_masked | 130 | 0.0071859 | 0.045642 | 0.041641 | 0.00023297 | 0.071671 |
| v1_base_masked | 140 | 0.0069765 | 0.045265 | 0.041153 | 0.00021795 | 0.070784 |
| v1_base_masked | 150 | 0.00699 | 0.044617 | 0.040876 | 0.00020909 | 0.070196 |
| v1_base_masked | 160 | 0.0068851 | 0.044478 | 0.040811 | 0.00019502 | 0.069954 |
| v1_base_masked | 170 | 0.0067886 | 0.044318 | 0.040571 | 0.00018945 | 0.069537 |
| v1_base_masked | 180 | 0.0068035 | 0.044123 | 0.040495 | 0.00018577 | 0.069378 |
| v1_base_masked | 190 | 0.0067455 | 0.044026 | 0.040288 | 0.00018264 | 0.069065 |
| v1_base_masked | 200 | 0.0068278 | 0.044382 | 0.040423 | 0.00018166 | 0.069459 |
| v1_wsigreg2 | 1 | 0.047625 | 0.087684 | 0.084092 | 0.0058047 | 0.30767 |
| v1_wsigreg2 | 2 | 0.027277 | 0.061551 | 0.056044 | 0.0013406 | 0.20656 |
| v1_wsigreg2 | 5 | 0.024634 | 0.045931 | 0.05257 | 0.001434 | 0.16921 |
| v1_wsigreg2 | 10 | 0.023296 | 0.035981 | 0.050255 | 0.001633 | 0.14568 |
| v1_wsigreg2 | 20 | 0.017084 | 0.029887 | 0.047384 | 0.0021569 | 0.12446 |
| v1_wsigreg2 | 30 | 0.015671 | 0.026284 | 0.045875 | 0.0024458 | 0.11436 |
| v1_wsigreg2 | 40 | 0.015734 | 0.02413 | 0.045028 | 0.0026008 | 0.10928 |
| v1_wsigreg2 | 50 | 0.015107 | 0.023121 | 0.044434 | 0.0025026 | 0.10603 |
| v1_wsigreg2 | 60 | 0.015384 | 0.022302 | 0.043894 | 0.0024707 | 0.10413 |
| v1_wsigreg2 | 70 | 0.014712 | 0.021735 | 0.043459 | 0.0023735 | 0.10188 |
| v1_wsigreg2 | 80 | 0.013904 | 0.021314 | 0.043164 | 0.0022363 | 0.099919 |
| v1_wsigreg2 | 90 | 0.013722 | 0.021071 | 0.042814 | 0.002166 | 0.098895 |
| v1_wsigreg2 | 100 | 0.013427 | 0.020766 | 0.042509 | 0.0021096 | 0.097679 |
| v1_wsigreg2 | 110 | 0.012786 | 0.020574 | 0.04211 | 0.0020043 | 0.096244 |
| v1_wsigreg2 | 120 | 0.012626 | 0.020372 | 0.041889 | 0.0019695 | 0.095455 |
| v1_wsigreg2 | 130 | 0.012354 | 0.020266 | 0.04176 | 0.0018907 | 0.094835 |
| v1_wsigreg2 | 140 | 0.011856 | 0.020015 | 0.041345 | 0.0018274 | 0.093414 |
| v1_wsigreg2 | 150 | 0.011614 | 0.01986 | 0.041057 | 0.0017799 | 0.09257 |
| v1_wsigreg2 | 160 | 0.011421 | 0.019828 | 0.041007 | 0.0017374 | 0.092257 |
| v1_wsigreg2 | 170 | 0.011285 | 0.019721 | 0.040792 | 0.0017103 | 0.09169 |
| v1_wsigreg2 | 180 | 0.011029 | 0.019595 | 0.040682 | 0.0016966 | 0.09107 |
| v1_wsigreg2 | 190 | 0.010931 | 0.01975 | 0.04049 | 0.0016831 | 0.091088 |
| v1_wsigreg2 | 200 | 0.011089 | 0.01963 | 0.040595 | 0.0016877 | 0.091113 |
| v1_wsigreg5 | 1 | 0.085481 | 0.065892 | 0.10428 | 0.0090398 | 0.52013 |
| v1_wsigreg5 | 2 | 0.062143 | 0.041656 | 0.059734 | 0.002972 | 0.33045 |
| v1_wsigreg5 | 5 | 0.048728 | 0.030339 | 0.054132 | 0.0030407 | 0.25486 |
| v1_wsigreg5 | 10 | 0.044214 | 0.0252 | 0.050897 | 0.0033699 | 0.22145 |
| v1_wsigreg5 | 20 | 0.032406 | 0.020623 | 0.047883 | 0.0045627 | 0.18386 |
| v1_wsigreg5 | 30 | 0.029485 | 0.018939 | 0.046384 | 0.0046564 | 0.17103 |
| v1_wsigreg5 | 40 | 0.028614 | 0.018247 | 0.045437 | 0.0044055 | 0.16573 |
| v1_wsigreg5 | 50 | 0.026807 | 0.017644 | 0.044824 | 0.0041905 | 0.16027 |
| v1_wsigreg5 | 60 | 0.026633 | 0.017175 | 0.0444 | 0.0040457 | 0.15731 |
| v1_wsigreg5 | 70 | 0.026023 | 0.016811 | 0.043868 | 0.0039386 | 0.15434 |
| v1_wsigreg5 | 80 | 0.0248 | 0.016595 | 0.043526 | 0.0037844 | 0.15168 |
| v1_wsigreg5 | 90 | 0.024295 | 0.016327 | 0.04316 | 0.0036757 | 0.14946 |
| v1_wsigreg5 | 100 | 0.023785 | 0.016085 | 0.042821 | 0.0035708 | 0.14739 |
| v1_wsigreg5 | 110 | 0.02318 | 0.015907 | 0.042454 | 0.003504 | 0.14552 |
| v1_wsigreg5 | 120 | 0.022968 | 0.015638 | 0.042235 | 0.0034428 | 0.14374 |
| v1_wsigreg5 | 130 | 0.02251 | 0.015558 | 0.042092 | 0.0033171 | 0.14272 |
| v1_wsigreg5 | 140 | 0.021846 | 0.015433 | 0.041648 | 0.0032486 | 0.14098 |
| v1_wsigreg5 | 150 | 0.021444 | 0.015291 | 0.041347 | 0.0032199 | 0.13957 |
| v1_wsigreg5 | 160 | 0.021117 | 0.015169 | 0.04134 | 0.0031532 | 0.13862 |
| v1_wsigreg5 | 170 | 0.020891 | 0.015079 | 0.041083 | 0.0031248 | 0.13768 |
| v1_wsigreg5 | 180 | 0.020509 | 0.014942 | 0.040919 | 0.0031002 | 0.13645 |
| v1_wsigreg5 | 190 | 0.020284 | 0.014979 | 0.040771 | 0.0031025 | 0.13626 |
| v1_wsigreg5 | 200 | 0.020714 | 0.015004 | 0.040891 | 0.0031062 | 0.13693 |
| v1_latent32 | 1 | 0.01922 | 0.13042 | 0.075132 | 0.0040378 | 0.15996 |
| v1_latent32 | 2 | 0.0096584 | 0.097959 | 0.054367 | 0.00069156 | 0.11307 |
| v1_latent32 | 5 | 0.0087404 | 0.071546 | 0.05197 | 0.00060115 | 0.096543 |
| v1_latent32 | 10 | 0.0069073 | 0.065062 | 0.049945 | 0.0005146 | 0.089435 |
| v1_latent32 | 20 | 0.0055251 | 0.058359 | 0.047406 | 0.00049989 | 0.08216 |
| v1_latent32 | 30 | 0.0047435 | 0.052909 | 0.045943 | 0.00063188 | 0.077204 |
| v1_latent32 | 40 | 0.0057807 | 0.045624 | 0.045009 | 0.00088341 | 0.07369 |
| v1_latent32 | 50 | 0.0058311 | 0.041507 | 0.044277 | 0.00089047 | 0.070951 |
| v1_latent32 | 60 | 0.0057497 | 0.040038 | 0.043758 | 0.00086063 | 0.069612 |
| v1_latent32 | 70 | 0.0057747 | 0.039244 | 0.043256 | 0.0008806 | 0.068741 |
| v1_latent32 | 80 | 0.0054124 | 0.037957 | 0.043014 | 0.00084311 | 0.067489 |
| v1_latent32 | 90 | 0.0052336 | 0.036963 | 0.042656 | 0.00083776 | 0.066455 |
| v1_latent32 | 100 | 0.0052787 | 0.035983 | 0.042382 | 0.00082965 | 0.065735 |
| v1_latent32 | 110 | 0.0050534 | 0.035005 | 0.041995 | 0.00080414 | 0.064632 |
| v1_latent32 | 120 | 0.0050961 | 0.034619 | 0.041796 | 0.00080482 | 0.064282 |
| v1_latent32 | 130 | 0.0049823 | 0.034079 | 0.04168 | 0.00075902 | 0.063777 |
| v1_latent32 | 140 | 0.0047631 | 0.033484 | 0.041255 | 0.00073849 | 0.062834 |
| v1_latent32 | 150 | 0.004676 | 0.033312 | 0.040981 | 0.00071039 | 0.062384 |
| v1_latent32 | 160 | 0.0045545 | 0.033146 | 0.040947 | 0.00068642 | 0.062143 |
| v1_latent32 | 170 | 0.0045305 | 0.032942 | 0.04075 | 0.00067249 | 0.061819 |
| v1_latent32 | 180 | 0.0043912 | 0.032923 | 0.04063 | 0.00065724 | 0.061549 |
| v1_latent32 | 190 | 0.0043741 | 0.032725 | 0.040423 | 0.00065718 | 0.061225 |
| v1_latent32 | 200 | 0.00441 | 0.032837 | 0.040545 | 0.00065444 | 0.061439 |
| v1_ema | 1 | 0.051192 | 0.093621 | 0.075993 | 0.019115 | 0.17591 |
| v1_ema | 2 | 0.071979 | 0.054577 | 0.053474 | 0.0086918 | 0.15361 |
| v1_ema | 5 | 0.11983 | 0.035719 | 0.050907 | 0.0062798 | 0.18922 |
| v1_ema | 10 | 0.097409 | 0.027359 | 0.049541 | 0.010008 | 0.16163 |
| v1_ema | 20 | 0.087195 | 0.022439 | 0.047402 | 0.012432 | 0.14706 |
| v1_ema | 30 | 0.082578 | 0.020262 | 0.045722 | 0.012183 | 0.13965 |
| v1_ema | 40 | 0.082357 | 0.019 | 0.044869 | 0.012052 | 0.13793 |
| v1_ema | 50 | 0.081632 | 0.018368 | 0.044406 | 0.012123 | 0.13643 |
| v1_ema | 60 | 0.082025 | 0.017843 | 0.043962 | 0.012258 | 0.13613 |
| v1_ema | 70 | 0.081233 | 0.01745 | 0.043586 | 0.012218 | 0.13477 |
| v1_ema | 80 | 0.079679 | 0.017205 | 0.043323 | 0.012109 | 0.13281 |
| v1_ema | 90 | 0.07755 | 0.016984 | 0.043076 | 0.011807 | 0.1303 |
| v1_ema | 100 | 0.07834 | 0.016881 | 0.042882 | 0.011819 | 0.13085 |
| v1_ema | 110 | 0.07616 | 0.01663 | 0.042495 | 0.011525 | 0.12812 |
| v1_ema | 120 | 0.07429 | 0.016427 | 0.042404 | 0.01137 | 0.12604 |
| v1_ema | 130 | 0.07379 | 0.016283 | 0.042288 | 0.011167 | 0.12534 |
| v1_ema | 140 | 0.072241 | 0.01626 | 0.041972 | 0.011023 | 0.12344 |
| v1_ema | 150 | 0.07026 | 0.015969 | 0.041714 | 0.010805 | 0.12104 |
| v1_ema | 160 | 0.069296 | 0.015964 | 0.041773 | 0.010671 | 0.12012 |
| v1_ema | 170 | 0.068861 | 0.016078 | 0.041648 | 0.01066 | 0.11961 |
| v1_ema | 180 | 0.067456 | 0.015849 | 0.0415 | 0.010529 | 0.11793 |
| v1_ema | 190 | 0.067054 | 0.015917 | 0.041367 | 0.010523 | 0.11743 |
| v1_ema | 200 | 0.068052 | 0.016078 | 0.04149 | 0.010561 | 0.11864 |
| v1_wground3 | 1 | 0.029532 | 0.1545 | 0.074741 | 0.0053061 | 0.33154 |
| v1_wground3 | 2 | 0.012055 | 0.11929 | 0.053727 | 0.0007767 | 0.23296 |
| v1_wground3 | 5 | 0.010879 | 0.082131 | 0.051186 | 0.00066945 | 0.20557 |
| v1_wground3 | 10 | 0.0088949 | 0.069942 | 0.049111 | 0.00056299 | 0.19125 |
| v1_wground3 | 20 | 0.0062875 | 0.059631 | 0.046785 | 0.00056784 | 0.17651 |
| v1_wground3 | 30 | 0.0050562 | 0.053926 | 0.045463 | 0.00068758 | 0.16848 |
| v1_wground3 | 40 | 0.005904 | 0.04679 | 0.04454 | 0.00085262 | 0.163 |
| v1_wground3 | 50 | 0.0064296 | 0.041387 | 0.043988 | 0.00093217 | 0.15918 |
| v1_wground3 | 60 | 0.006121 | 0.039156 | 0.043535 | 0.00088976 | 0.15639 |
| v1_wground3 | 70 | 0.0060356 | 0.03819 | 0.043048 | 0.00087455 | 0.15436 |
| v1_wground3 | 80 | 0.0057931 | 0.037887 | 0.042789 | 0.0008295 | 0.15319 |
| v1_wground3 | 90 | 0.0056097 | 0.036702 | 0.042415 | 0.00081938 | 0.15129 |
| v1_wground3 | 100 | 0.0055337 | 0.036244 | 0.042194 | 0.00078787 | 0.15032 |
| v1_wground3 | 110 | 0.0053529 | 0.035233 | 0.041807 | 0.00077723 | 0.14847 |
| v1_wground3 | 120 | 0.005283 | 0.034732 | 0.041569 | 0.00076962 | 0.14743 |
| v1_wground3 | 130 | 0.0052059 | 0.034394 | 0.041514 | 0.00075162 | 0.14702 |
| v1_wground3 | 140 | 0.0050809 | 0.034193 | 0.041074 | 0.00072761 | 0.14547 |
| v1_wground3 | 150 | 0.0049831 | 0.033825 | 0.040837 | 0.00071712 | 0.14448 |
| v1_wground3 | 160 | 0.0048892 | 0.033519 | 0.040802 | 0.00069976 | 0.14413 |
| v1_wground3 | 170 | 0.0048791 | 0.033396 | 0.040617 | 0.00069426 | 0.1435 |
| v1_wground3 | 180 | 0.0047518 | 0.033198 | 0.040523 | 0.00068673 | 0.14299 |
| v1_wground3 | 190 | 0.0047332 | 0.033312 | 0.040311 | 0.00068659 | 0.14239 |
| v1_wground3 | 200 | 0.0047809 | 0.033251 | 0.040451 | 0.00068714 | 0.14283 |

### P8 (data): final-epoch (200) per-seed table

| rung | seed | eff_rank | R2_energy | R2_C_string | R2_P_meson | R2_P_baryonic | semigroup_resid | isotropy | pred_loss |
|---|---|---|---|---|---|---|---|---|---|
| v1_base | 0 | 5.6538 | 0.90055 | 0.99841 | 0.98184 | 0.99759 | 0.0018857 | 0.0030296 | 0.0045908 |
| v1_base | 1 | 6.1539 | 0.89943 | 0.9982 | 0.97786 | 0.99741 | 0.0021573 | 0.013128 | 0.0042442 |
| v1_base | 2 | 5.1562 | 0.89954 | 0.99843 | 0.98546 | 0.99733 | 0.0032023 | 0.0018968 | 0.0039533 |
| v1_base | 3 | 5.8895 | 0.90343 | 0.99824 | 0.98143 | 0.99722 | 0.0024169 | 0.0080982 | 0.0042795 |
| v1_base | 4 | 5.8507 | 0.9015 | 0.99825 | 0.98159 | 0.99707 | 0.0032928 | 0.0063634 | 0.0043925 |
| v1_base_masked | 0 | 4.7505 | 0.9013 | 0.99836 | 0.97942 | 0.99754 | 0.00020118 | 0.0019576 | 0.0069607 |
| v1_base_masked | 1 | 4.6548 | 0.90054 | 0.99764 | 0.97523 | 0.99679 | 0.00024869 | 0.0035364 | 0.0071327 |
| v1_base_masked | 2 | 4.5022 | 0.90149 | 0.99797 | 0.98315 | 0.99713 | 0.00018148 | 0.0023078 | 0.0066253 |
| v1_base_masked | 3 | 5.4179 | 0.90247 | 0.99824 | 0.9775 | 0.99685 | 0.00021635 | 0.004325 | 0.006914 |
| v1_base_masked | 4 | 4.5283 | 0.90261 | 0.99825 | 0.97838 | 0.99697 | 0.00018566 | 0.0021643 | 0.0065061 |
| v1_wsigreg2 | 0 | 8.2625 | 0.90128 | 0.99771 | 0.97928 | 0.99706 | 0.0039475 | 0.026515 | 0.011113 |
| v1_wsigreg2 | 1 | 9.104 | 0.89999 | 0.99787 | 0.97285 | 0.99719 | 0.0051619 | 0.02452 | 0.01114 |
| v1_wsigreg2 | 2 | 8.9244 | 0.89994 | 0.99763 | 0.9765 | 0.99662 | 0.003647 | 0.047643 | 0.011253 |
| v1_wsigreg2 | 3 | 8.9336 | 0.90088 | 0.99778 | 0.97519 | 0.99685 | 0.0053439 | 0.068916 | 0.011042 |
| v1_wsigreg2 | 4 | 9.0766 | 0.90228 | 0.99785 | 0.97205 | 0.99654 | 0.0034857 | 0.029621 | 0.010897 |
| v1_wsigreg5 | 0 | 10.664 | 0.9017 | 0.99758 | 0.97456 | 0.99678 | 0.0062859 | 0.17709 | 0.021374 |
| v1_wsigreg5 | 1 | 10.836 | 0.9007 | 0.99687 | 0.96767 | 0.99661 | 0.0083137 | 0.13562 | 0.020745 |
| v1_wsigreg5 | 2 | 10.943 | 0.89929 | 0.99691 | 0.97443 | 0.99605 | 0.0072521 | 0.25555 | 0.020579 |
| v1_wsigreg5 | 3 | 10.828 | 0.90147 | 0.99709 | 0.97123 | 0.99616 | 0.0067471 | 0.31023 | 0.020748 |
| v1_wsigreg5 | 4 | 10.525 | 0.9019 | 0.99706 | 0.97109 | 0.99573 | 0.0084698 | 0.094874 | 0.020122 |
| v1_latent32 | 0 | 6.5275 | 0.90201 | 0.99865 | 0.98514 | 0.99751 | 0.0047161 | 0.00038727 | 0.0045495 |
| v1_latent32 | 1 | 6.1165 | 0.90166 | 0.99819 | 0.97725 | 0.99718 | 0.0027028 | 0.00082769 | 0.0043562 |
| v1_latent32 | 2 | 6.5754 | 0.90223 | 0.99831 | 0.98698 | 0.99738 | 0.0015498 | 0.00055248 | 0.0044224 |
| v1_latent32 | 3 | 6.3543 | 0.90304 | 0.99852 | 0.97963 | 0.99747 | 0.0020761 | 0.00031021 | 0.0044773 |
| v1_latent32 | 4 | 6.2198 | 0.90219 | 0.99848 | 0.98562 | 0.99707 | 0.0017529 | 0.00084261 | 0.0042445 |
| v1_ema | 0 | 13.382 | 0.90175 | 0.99324 | 0.92188 | 0.99536 | 0.016267 | 0.076712 | 0.071916 |
| v1_ema | 1 | 13.266 | 0.89656 | 0.99495 | 0.93294 | 0.99347 | 0.015838 | 0.097372 | 0.069123 |
| v1_ema | 2 | 13.314 | 0.89818 | 0.99396 | 0.91464 | 0.99458 | 0.021326 | 0.11124 | 0.066807 |
| v1_ema | 3 | 13.086 | 0.89985 | 0.99444 | 0.93262 | 0.99477 | 0.022098 | 0.1666 | 0.064924 |
| v1_ema | 4 | 13.475 | 0.89849 | 0.99454 | 0.95215 | 0.99437 | 0.016387 | 0.22544 | 0.06749 |
| v1_wground3 | 0 | 5.7862 | 0.90268 | 0.99859 | 0.98666 | 0.99796 | 0.0069369 | 0.0022643 | 0.0048044 |
| v1_wground3 | 1 | 6.1419 | 0.90001 | 0.99796 | 0.98338 | 0.99765 | 0.0037939 | 0.0035023 | 0.0050111 |
| v1_wground3 | 2 | 5.7342 | 0.90064 | 0.99823 | 0.98864 | 0.99754 | 0.0027285 | 0.0022924 | 0.0046309 |
| v1_wground3 | 3 | 6.1304 | 0.90256 | 0.99844 | 0.98451 | 0.99758 | 0.0029573 | 0.0027246 | 0.0050436 |
| v1_wground3 | 4 | 5.6294 | 0.9016 | 0.99852 | 0.98616 | 0.99717 | 0.0023 | 0.0032934 | 0.0044146 |

### P8b: per-rung summary of the final epoch (min / max over 5 seeds; this is what the J1 gate compares)

| rung | rank min | rank max | R2 energy min | R2 C_string min | R2 P_meson min | R2 P_baryonic min | semigroup max | semigroup min | isotropy min | isotropy max |
|---|---|---|---|---|---|---|---|---|---|---|
| v1_base | 5.1562 | 6.1539 | 0.89943 | 0.9982 | 0.97786 | 0.99707 | 0.0032928 | 0.0018857 | 0.0018968 | 0.013128 |
| v1_base_masked | 4.5022 | 5.4179 | 0.90054 | 0.99764 | 0.97523 | 0.99679 | 0.00024869 | 0.00018148 | 0.0019576 | 0.004325 |
| v1_wsigreg2 | 8.2625 | 9.104 | 0.89994 | 0.99763 | 0.97205 | 0.99654 | 0.0053439 | 0.0034857 | 0.02452 | 0.068916 |
| v1_wsigreg5 | 10.525 | 10.943 | 0.89929 | 0.99687 | 0.96767 | 0.99573 | 0.0084698 | 0.0062859 | 0.094874 | 0.31023 |
| v1_latent32 | 6.1165 | 6.5754 | 0.90166 | 0.99819 | 0.97725 | 0.99707 | 0.0047161 | 0.0015498 | 0.00031021 | 0.00084261 |
| v1_ema | 13.086 | 13.475 | 0.89656 | 0.99324 | 0.91464 | 0.99347 | 0.022098 | 0.015838 | 0.076712 | 0.22544 |
| v1_wground3 | 5.6294 | 6.1419 | 0.90001 | 0.99796 | 0.98338 | 0.99717 | 0.0069369 | 0.0023 | 0.0022643 | 0.0035023 |

### P9 (data): scatter, rank vs semigroup residual (final epoch, every seed)

| rung | seed | eff_rank (x) | semigroup_resid (y, log axis) |
|---|---|---|---|
| v1_base | 0 | 5.6538 | 0.0018857 |
| v1_base | 1 | 6.1539 | 0.0021573 |
| v1_base | 2 | 5.1562 | 0.0032023 |
| v1_base | 3 | 5.8895 | 0.0024169 |
| v1_base | 4 | 5.8507 | 0.0032928 |
| v1_base_masked | 0 | 4.7505 | 0.00020118 |
| v1_base_masked | 1 | 4.6548 | 0.00024869 |
| v1_base_masked | 2 | 4.5022 | 0.00018148 |
| v1_base_masked | 3 | 5.4179 | 0.00021635 |
| v1_base_masked | 4 | 4.5283 | 0.00018566 |
| v1_wsigreg2 | 0 | 8.2625 | 0.0039475 |
| v1_wsigreg2 | 1 | 9.104 | 0.0051619 |
| v1_wsigreg2 | 2 | 8.9244 | 0.003647 |
| v1_wsigreg2 | 3 | 8.9336 | 0.0053439 |
| v1_wsigreg2 | 4 | 9.0766 | 0.0034857 |
| v1_wsigreg5 | 0 | 10.664 | 0.0062859 |
| v1_wsigreg5 | 1 | 10.836 | 0.0083137 |
| v1_wsigreg5 | 2 | 10.943 | 0.0072521 |
| v1_wsigreg5 | 3 | 10.828 | 0.0067471 |
| v1_wsigreg5 | 4 | 10.525 | 0.0084698 |
| v1_latent32 | 0 | 6.5275 | 0.0047161 |
| v1_latent32 | 1 | 6.1165 | 0.0027028 |
| v1_latent32 | 2 | 6.5754 | 0.0015498 |
| v1_latent32 | 3 | 6.3543 | 0.0020761 |
| v1_latent32 | 4 | 6.2198 | 0.0017529 |
| v1_ema | 0 | 13.382 | 0.016267 |
| v1_ema | 1 | 13.266 | 0.015838 |
| v1_ema | 2 | 13.314 | 0.021326 |
| v1_ema | 3 | 13.086 | 0.022098 |
| v1_ema | 4 | 13.475 | 0.016387 |
| v1_wground3 | 0 | 5.7862 | 0.0069369 |
| v1_wground3 | 1 | 6.1419 | 0.0037939 |
| v1_wground3 | 2 | 5.7342 | 0.0027285 |
| v1_wground3 | 3 | 6.1304 | 0.0029573 |
| v1_wground3 | 4 | 5.6294 | 0.0023 |

Correlation over the 30 unmasked final-epoch points (computed by this script): Pearson r(rank, log10 semigroup_resid) = 0.898; Spearman rho = 0.774.

### P7b: final-epoch seed-mean losses and weights (context for the semigroup diagnosis)

| rung | pred | sigreg | ground | semigroup (loss term, unweighted as logged) | semigroup_resid (validation diagnostic) |
|---|---|---|---|---|---|
| v1_base | 0.004292 | 0.032281 | 0.040567 | 0.0006352 | 0.002591 |
| v1_base_masked | 0.0068278 | 0.044382 | 0.040423 | 0.00018166 | 0.00020667 |
| v1_wsigreg2 | 0.011089 | 0.01963 | 0.040595 | 0.0016877 | 0.0043172 |
| v1_wsigreg5 | 0.020714 | 0.015004 | 0.040891 | 0.0031062 | 0.0074137 |
| v1_latent32 | 0.00441 | 0.032837 | 0.040545 | 0.00065444 | 0.0025595 |
| v1_ema | 0.068052 | 0.016078 | 0.04149 | 0.010561 | 0.018383 |
| v1_wground3 | 0.0047809 | 0.033251 | 0.040451 | 0.00068714 | 0.0037433 |

### P12 (data): v1_check, 1 seed, 10 epochs, laptop (runs/v1_check/seed0/history.json)

| epoch | total | pred | sigreg | ground | semigroup | eff_rank | R2_energy | R2_C_string | R2_P_meson | R2_P_baryonic | semigroup_resid | isotropy |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.17098 | 0.021249 | 0.13561 | 0.081485 | 0.0043781 | 3.7043 | 0.88986 | 0.93904 | 0.78614 | 0.96016 | 0.0014192 | 0.018612 |
| 2 | 0.11481 | 0.010784 | 0.099955 | 0.053986 | 0.00062724 | 3.9221 | 0.87837 | 0.96567 | 0.90041 | 0.97054 | 0.0015851 | 0.029835 |
| 3 | 0.10468 | 0.011261 | 0.080558 | 0.053069 | 0.00069076 | 3.9074 | 0.86767 | 0.97882 | 0.89344 | 0.98564 | 0.0017195 | 0.042141 |
| 4 | 0.096824 | 0.010459 | 0.072345 | 0.050138 | 0.00054444 | 4.0289 | 0.88734 | 0.98941 | 0.93434 | 0.98783 | 0.0005004 | 0.039093 |
| 5 | 0.093102 | 0.0093974 | 0.068349 | 0.049487 | 0.00043479 | 3.9854 | 0.89151 | 0.98815 | 0.95231 | 0.99454 | 0.0006864 | 0.033197 |
| 6 | 0.092471 | 0.0089411 | 0.067269 | 0.04986 | 0.00035959 | 3.9435 | 0.88575 | 0.99466 | 0.96165 | 0.99006 | 0.00041171 | 0.031451 |
| 7 | 0.089256 | 0.0081711 | 0.065865 | 0.048122 | 0.00030128 | 3.9338 | 0.89866 | 0.98961 | 0.94091 | 0.99536 | 0.00037558 | 0.026313 |
| 8 | 0.087271 | 0.0078339 | 0.065204 | 0.046811 | 0.00024567 | 3.9962 | 0.88346 | 0.99679 | 0.95635 | 0.99463 | 0.00028883 | 0.023029 |
| 9 | 0.086114 | 0.0074501 | 0.064804 | 0.046242 | 0.00021003 | 3.9513 | 0.89347 | 0.99733 | 0.95769 | 0.99575 | 0.00041583 | 0.022802 |
| 10 | 0.084537 | 0.0073115 | 0.063282 | 0.045566 | 0.00019338 | 3.9285 | 0.89546 | 0.99664 | 0.9639 | 0.99574 | 0.00024557 | 0.021849 |

### P12b (data): v1_check forecast MAE (runs/v1_check/forecast_eval.json; 1 seed, 10 epochs; NOT a J2 result)

Context step 4, eval steps [4, 8], dataset main (checksum 73fff8e5a7b7), n_test {'onfam': 2935, 'strong': 3134}.

| family | method | horizon | P_baryonic | P_meson | C_string |
|---|---|---|---|---|---|
| onfam | jepa | +4 | 0.052674 | 0.017718 | 0.033895 |
| onfam | jepa | +8 | 0.072241 | 0.026415 | 0.042866 |
| onfam | ridge | +4 | 0.059832 | 0.019022 | 0.030469 |
| onfam | ridge | +8 | 0.14368 | 0.030069 | 0.136 |
| onfam | autoregressive | +4 | 0.029684 | 0.010979 | 0.01427 |
| onfam | autoregressive | +8 | 0.40221 | 0.18864 | 1.1368 |
| onfam | supervised_mlp | +4 | 0.022456 | 0.0098695 | 0.011954 |
| onfam | supervised_mlp | +8 | 0.048277 | 0.019746 | 0.024095 |
| strong | jepa | +4 | 0.0795 | 0.013247 | 0.032178 |
| strong | jepa | +8 | 0.12905 | 0.016545 | 0.05477 |
| strong | ridge | +4 | 0.085261 | 0.01392 | 0.03773 |
| strong | ridge | +8 | 0.18543 | 0.023942 | 0.24823 |
| strong | autoregressive | +4 | 0.12849 | 0.014637 | 0.053901 |
| strong | autoregressive | +8 | 0.3705 | 0.077423 | 0.23706 |
| strong | supervised_mlp | +4 | 0.10847 | 0.013318 | 0.045559 |
| strong | supervised_mlp | +8 | 0.15278 | 0.018361 | 0.068042 |

### 9.2 P11 sub-plots (physics curves and carrier costs)
| sub-plot | title | x | y | series | tables |
|---|---|---|---|---|---|
| P11a | P-A dynamics from S3 | $t$ in units of $1/g_E$ (0..3) | probability or correlator (dimensionless) | $P_{S3}$, $P_{S1}$, $P_{\text{meson}}$, $P_{\text{baryonic}}$, breaking fraction, $C_{\text{string}}$; markers at the hardware times $0.375,0.75,1.5,3.0$ | P11a, P11a2 |
| P11b | $g_E=1$, $\mu=3/8$ dynamics table | $t$ (1, 2, 3) | $P_{\text{baryonic}}$, $P_{\text{meson}}$, $P_{S1}$, $C_{\text{string}}$ | four series | P11b |
| P11c | On-family breaking fraction at $t=3$ versus mass | $\mu$ | breaking fraction | $g_E=2$ | P11c |
| P11d | Strong-coupling resonance | $\mu$ | breaking fraction | three curves, $t=16.7,33.3,50$ ($c_H=0.02$, $c_B=-0.02$) | P11d |
| P11e | Lanczos coefficients | index $k$ (0..11) | $\alpha_k$ and $\beta_k$ | P-A, P-S | P11e |
| P11f | $P_{S3}(t)$ at the 12 cross-check times | $t$ | $P_{S3}$ | P-A (0.25..3.0), P-S (2..24) | P11f |
| P11g | Carrier cost versus depth | steps $r$ (1, 2, 4, 8) or $t$ | CZ count, two-qubit depth, infidelity, flag rate | KC-Trotter; KC-prep fixed at 22 CZ | P11g |

Check of my recomputation against the plan: P11a, P11b, P11c end points (0.62791 and 0.53109 versus the plan's 0.628 and 0.531), and the breaking fractions of P11d for $\mu=0.375,0.30,0.45,0.15$ (0.227/0.554/0.740, 0.143/0.0715/0.0556, 0.141/0.0676/0.0596, 0.0068/0.0162/0.0162) all agree with plan Appendix B to the digits the plan quotes. The definition "breaking fraction $=P_{\text{meson}}+P_{\text{baryonic}}$" was fixed by this agreement. The plan's other numbers for $\mu=0.2$, 0.25, 0.33, 0.42, 0.5, 0.575, 0.65 are not quoted in the plan, so those rows are new.

#### P11g table: carrier cost at P-A ($K=12$, $\Delta t=0.375$; source plan §4; CZ counts also checked against the formula in §3; flag rate and population error are EMULATED)
| r | t | CZ_KC-Trotter | two_qubit_depth | strang_infidelity | emulated_flag_rate | emulated_postselected_population_error | CZ_KC-prep |
|---|---|---|---|---|---|---|---|
| 1 | 0.375 | 34 | 6 | 2e-5 | 0.23 | 0.006 | 22 |
| 2 | 0.75 | 56 | 10 | 8e-5 | 0.28 | 0.011 | 22 |
| 4 | 1.5 | 100 | 18 | 3e-4 | 0.38 | 0.020 | 22 |
| 8 | 3.0 | 188 | 34 | 1.2e-3 | 0.55 | 0.016 | 22 |

#### P11a table: dynamics from S3 at P-A (g_E=2, mu=3/8), hardware times

| t (1/g_E) | P_S3 | P_meson | P_baryonic | C_string |
|---|---|---|---|---|
| 0.375 | 0.96928 | 0.0041726 | 0.021598 | 0.74412 |
| 0.75 | 0.88382 | 0.014368 | 0.082077 | 0.72675 |
| 1.5 | 0.62184 | 0.034185 | 0.26955 | 0.66173 |
| 3.0 | 0.18293 | 0.046364 | 0.57906 | 0.44802 |

#### P11a2 table: P-A dynamics from S3, fine time grid (t = 0 .. 3 in steps of 0.125)

| t (1/g_E) | P_S3 | P_S1 | P_meson | P_baryonic | breaking (P_meson+P_baryonic) | C_string |
|---|---|---|---|---|---|---|
| 0.000 | 1 | 7.9788e-34 | 1.7613e-31 | 8.4117e-31 | 1.0173e-30 | 0.75 |
| 0.125 | 0.99653 | 6.05e-05 | 0.00048546 | 0.0024367 | 0.0029222 | 0.74934 |
| 0.250 | 0.9862 | 0.00023568 | 0.0019084 | 0.0096911 | 0.0116 | 0.74738 |
| 0.375 | 0.96928 | 0.00050736 | 0.0041726 | 0.021598 | 0.02577 | 0.74412 |
| 0.500 | 0.94619 | 0.00084771 | 0.0071296 | 0.037887 | 0.045017 | 0.73957 |
| 0.625 | 0.91747 | 0.0012226 | 0.010595 | 0.058195 | 0.06879 | 0.73377 |
| 0.750 | 0.88382 | 0.0015956 | 0.014368 | 0.082077 | 0.096445 | 0.72675 |
| 0.875 | 0.84596 | 0.0019321 | 0.018249 | 0.10902 | 0.12727 | 0.71855 |
| 1.000 | 0.80471 | 0.0022027 | 0.022058 | 0.13847 | 0.16053 | 0.70922 |
| 1.125 | 0.76089 | 0.0023863 | 0.025645 | 0.16983 | 0.19548 | 0.69882 |
| 1.250 | 0.7153 | 0.0024711 | 0.028901 | 0.20252 | 0.23142 | 0.6874 |
| 1.375 | 0.66871 | 0.0024551 | 0.031757 | 0.23594 | 0.2677 | 0.67502 |
| 1.500 | 0.62184 | 0.0023451 | 0.034185 | 0.26955 | 0.30374 | 0.66173 |
| 1.625 | 0.57532 | 0.0021547 | 0.036194 | 0.30285 | 0.33904 | 0.64759 |
| 1.750 | 0.5297 | 0.0019025 | 0.03782 | 0.3354 | 0.37322 | 0.63263 |
| 1.875 | 0.48545 | 0.0016099 | 0.039122 | 0.36683 | 0.40595 | 0.61689 |
| 2.000 | 0.44294 | 0.0012993 | 0.040171 | 0.39687 | 0.43704 | 0.6004 |
| 2.125 | 0.40243 | 0.00099326 | 0.041043 | 0.42532 | 0.46637 | 0.58322 |
| 2.250 | 0.36412 | 0.00071367 | 0.041811 | 0.45207 | 0.49388 | 0.56537 |
| 2.375 | 0.32813 | 0.00048136 | 0.042538 | 0.47708 | 0.51962 | 0.5469 |
| 2.500 | 0.2945 | 0.00031585 | 0.043268 | 0.50039 | 0.54365 | 0.52789 |
| 2.625 | 0.26323 | 0.00023463 | 0.044027 | 0.52208 | 0.56611 | 0.5084 |
| 2.750 | 0.23427 | 0.00025211 | 0.044815 | 0.54231 | 0.58712 | 0.48853 |
| 2.875 | 0.20753 | 0.0003781 | 0.045609 | 0.56123 | 0.60684 | 0.46836 |
| 3.000 | 0.18293 | 0.00061602 | 0.046364 | 0.57906 | 0.62542 | 0.44802 |

#### P11b table: g_E = 1, mu = 3/8 (the physics notes' table), from S3

| t (1/g_E) | P_baryonic | P_meson | P_S1 | C_string |
|---|---|---|---|---|
| 1.0 | 0.43185 | 0.03706 | 0.0099413 | 0.58093 |
| 2.0 | 0.73219 | 0.027806 | 0.0072587 | 0.34532 |
| 3.0 | 0.82096 | 0.033611 | 0.010362 | 0.23824 |

#### P11c table: on-family (g_E = 2) breaking fraction at t = 3 vs mu

| mu | P_meson | P_baryonic | breaking fraction |
|---|---|---|---|
| 0.15 | 0.045712 | 0.5822 | 0.62791 |
| 0.25 | 0.044314 | 0.59082 | 0.63513 |
| 0.375 | 0.046364 | 0.57906 | 0.62542 |
| 0.5 | 0.051881 | 0.54401 | 0.59589 |
| 0.65 | 0.059821 | 0.47127 | 0.53109 |

#### P11d table: strong coupling (c_H = 0.02, c_B = -0.02) breaking fraction vs mu at t = 16.7, 33.3, 50

| mu | t=16.7 | t=33.3 | t=50 |
|---|---|---|---|
| 0.15 | 0.0067669 | 0.016244 | 0.016229 |
| 0.2 | 0.0023847 | 0.0087824 | 0.015666 |
| 0.25 | 0.04774 | 0.041834 | 0.011251 |
| 0.3 | 0.14284 | 0.07152 | 0.055614 |
| 0.33 | 0.19466 | 0.352 | 0.26399 |
| 0.375 | 0.22734 | 0.55435 | 0.73967 |
| 0.42 | 0.19309 | 0.33634 | 0.24066 |
| 0.45 | 0.14091 | 0.06759 | 0.059628 |
| 0.5 | 0.046528 | 0.042054 | 0.011914 |
| 0.575 | 0.0014826 | 0.0048785 | 0.0089347 |
| 0.65 | 0.012792 | 0.0020107 | 0.0094453 |

#### Further machine-readable tables (P10, P11e, P11f, J1 records, jobs, dataset reproducibility)

#### P10 table: R2 ceilings from one clean observation (validation split, 26,348 rows; evidence/J1_training/ceiling_main.json)

| inputs | target | ridge | knn5 | gbt | mlp |
|---|---|---|---|---|---|
| obs | energy | 0.88684 | 0.85088 | 0.89016 | 0.91445 |
| obs | C_string | 1 | 0.9972 | 0.99997 | 0.9999 |
| obs | P_meson | 1 | 0.98865 | 0.99598 | 0.99998 |
| obs | P_baryonic | 1 | 0.99685 | 0.99996 | 0.99995 |
| obs+couplings | energy | 0.95086 | 0.96959 | 0.9851 | 0.99412 |
| obs+couplings | C_string | 1 | 0.99537 | 0.99997 | 0.99986 |
| obs+couplings | P_meson | 1 | 0.98556 | 0.99595 | 0.99997 |
| obs+couplings | P_baryonic | 1 | 0.99466 | 0.99996 | 0.99995 |

Best R2 from the observation: energy 0.91445, C_string 1, P_meson 1, P_baryonic 1. Best with couplings: energy 0.99412, C_string 1, P_meson 1, P_baryonic 1. Clean-observation effective rank: raw 9.1297, standardised 11.195.

Variance fractions of the standardised clean observations (18 directions, descending): 0.37187, 0.19507, 0.10574, 0.062974, 0.060508, 0.058639, 0.047336, 0.042337, 0.027393, 0.0083999, 0.0070831, 0.0058836, 0.0037457, 0.0030283, 5.094e-29, 2.3817e-31, 2.7241e-32, 6.3511e-33

#### P11e table: Lanczos coefficients from S3 (evidence/J0_data/crosscheck_su2qc.json, route C)

| k | alpha_k P-A | beta_k P-A | alpha_k P-S | beta_k P-S |
|---|---|---|---|---|
| 0 | 1.5 | 0.47186 | 1.5 | 0.042426 |
| 1 | 1.6842 | 0.84564 | 1.3333 | 0.85234 |
| 2 | 1.4924 | 1.3415 | 1.3151 | 1.2022 |
| 3 | 0.39859 | 1.5023 | 1.823 | 0.28653 |
| 4 | 0.4345 | 1.4385 | -1.085 | 0.97686 |
| 5 | 1.1436 | 1.4819 | 1.1523 | 0.68766 |
| 6 | 2.3935 | 1.5336 | 1.5666 | 1.3769 |
| 7 | 2.4523 | 1.1415 | 1.4898 | 0.49531 |
| 8 | 1.8761 | 0.40824 | 4.2058 | 0.73028 |
| 9 | 1.8891 | 1.1556 | 1.6927 | 0.056829 |
| 10 | 0.94602 | 0.54566 | 1.4571 | 0.26958 |
| 11 | 0.8275 | 1.1166 | 0.13017 | 0.50907 |

#### P11f table: P_S3(t) from S3 at the 12 cross-check times (route C)

| i | t P-A | P_S3 P-A | t P-S | P_S3 P-S |
|---|---|---|---|---|
| 1 | 0.25 | 0.9862 | 2.0 | 0.99416 |
| 2 | 0.5 | 0.94619 | 4.0 | 0.98098 |
| 3 | 0.75 | 0.88382 | 6.0 | 0.95678 |
| 4 | 1.0 | 0.80471 | 8.0 | 0.9261 |
| 5 | 1.25 | 0.7153 | 10.0 | 0.88628 |
| 6 | 1.5 | 0.62184 | 12.0 | 0.84156 |
| 7 | 1.75 | 0.5297 | 14.0 | 0.79042 |
| 8 | 2.0 | 0.44294 | 16.0 | 0.73636 |
| 9 | 2.25 | 0.36412 | 18.0 | 0.679 |
| 10 | 2.5 | 0.2945 | 20.0 | 0.62081 |
| 11 | 2.75 | 0.23427 | 22.0 | 0.56228 |
| 12 | 3.0 | 0.18293 | 24.0 | 0.50479 |

#### J1 gate records (evidence/J1_training/*.json)

| record | rung | status | rank min (thr 8) | R2 energy min (0.887) | R2 C_string min (0.99) | R2 P_meson min (0.95) | R2 P_baryonic min (0.98) | semigroup max (<0.001) | per-seed ranks (gate note) |
|---|---|---|---|---|---|---|---|---|---|
| 20261005T231912Z | v1_base | FAIL | 5.1562 FAIL | 0.89943 PASS | 0.9982 PASS | 0.97786 PASS | 0.99707 PASS | 0.0032928 FAIL | [5.65, 6.15, 5.16, 5.89, 5.85] |
| 20261005T234716Z | v1_wsigreg2 | FAIL | 8.2625 PASS | 0.89994 PASS | 0.99763 PASS | 0.97205 PASS | 0.99654 PASS | 0.0053439 FAIL | [8.26, 9.1, 8.92, 8.93, 9.08] |
| 20261005T234719Z | v1_wsigreg5 | FAIL | 10.525 PASS | 0.89929 PASS | 0.99687 PASS | 0.96767 PASS | 0.99573 PASS | 0.0084698 FAIL | [10.66, 10.84, 10.94, 10.83, 10.53] |
| 20261006T000318Z | v1_latent32 | FAIL | 6.1165 FAIL | 0.90166 PASS | 0.99819 PASS | 0.97725 PASS | 0.99707 PASS | 0.0047161 FAIL | [6.53, 6.12, 6.58, 6.35, 6.22] |
| 20261006T024735Z | v1_ema | FAIL | 13.086 PASS | 0.89656 PASS | 0.99324 PASS | 0.91464 FAIL | 0.99347 PASS | 0.022098 FAIL | [13.38, 13.27, 13.31, 13.09, 13.47] |
| 20261006T030159Z | v1_wground3 | FAIL | 5.6294 FAIL | 0.90001 PASS | 0.99796 PASS | 0.98338 PASS | 0.99717 PASS | 0.0069369 FAIL | [5.79, 6.14, 5.73, 6.13, 5.63] |

#### Job table (jobs/*.yaml and evidence/jobs/NNN/status.json; states read on 2026-10-06 by scripts/jobs/status.py)

| job | title (slug) | kind | job-file commit | Slurm limit | state | elapsed h | node-h | Slurm id |
|---|---|---|---|---|---|---|---|---|
| 000 | worker smoke test | check | 80efb3d | 00:10:00 | COMPLETED | 0.011 | 0.003 | 59236367 |
| 001 | chain_strong | dataset | 9affe3a | 02:00:00 | COMPLETED | 0.223 | 0.056 | 59281851 |
| 002 | v1_base | train | 0a76800 | 08:28:00 | FAILED | 2.164 | 0.541 | 59381539 |
| 003 | v1_wsigreg2 | train | 1d9c4d0 | 04:14:00 | FAILED | 1.035 | 0.259 | 59381540 |
| 004 | v1_wsigreg5 | train | a3ab4ca | 04:14:00 | FAILED | 1.031 | 0.258 | 59382099 |
| 005 | v1_latent32 | train | 1c60d57 | 04:14:00 | FAILED | 1.039 | 0.26 | 59382104 |
| 006 | v1_ema | train | 0cf933f | 04:14:00 | FAILED | 0.981 | 0.245 | 59382743 |
| 007 | v1_wground3 | train | aa7f8af | 04:14:00 | FAILED | 1.071 | 0.268 | 59382746 |
| 008 | v1_curriculum | train | 7a18cdb | 04:14:00 | (no status file; SUBMITTED per status.py) | - | - | - |
| 009 | gpu_smoke | train | 5000bc9 | 00:30:00 | COMPLETED | 0.011 | 0.003 | 59393121 |
| 010 | fingerprints of main and gpu_smoke rebuilt on Perlmutter | dataset | 36f4224 | 00:40:00 | COMPLETED | 0.02 | 0.005 | 59396170 |
| 011 | v1_wsemigroup1 | train | 25567ea | 04:14:00 | (no status file; SUBMITTED per status.py) | - | - | - |
| 012 | v1_wsig2_wsg1 | train | 8be2aa4 | 04:14:00 | (no status file; SUBMITTED per status.py) | - | - | - |

Sum of node_hours over the status files: 1.898

#### Dataset reproducibility (evidence/J0_data/fingerprint_compare_*.json; per-trajectory-sum tolerance 1e-12)

| dataset | array | checksum equal | max abs diff of per-trajectory sums | trajectories above tol | max abs diff of sampled raw values (2000 samples) | samples above tol |
|---|---|---|---|---|---|---|
| main (20,000 traj) | act | True | 0 | 0 / 20000 | 0 | 0 / 2000 |
| main (20,000 traj) | ctx | True | 0 | 0 / 20000 | 0 | 0 / 2000 |
| main (20,000 traj) | energy | False | 2.4798e-12 | 37 / 20000 | 1.9407e-13 | 0 / 2000 |
| main (20,000 traj) | tgt | False | 5.727e-12 | 2513 / 20000 | 5.6621e-14 | 0 / 2000 |
| main (20,000 traj) | valid | True | 0 | 0 / 20000 | 0 | 0 / 2000 |
| gpu_smoke (400 traj) | act | True | 0 | 0 / 400 | 0 | 0 / 2000 |
| gpu_smoke (400 traj) | ctx | True | 0 | 0 / 400 | 0 | 0 / 2000 |
| gpu_smoke (400 traj) | energy | False | 1.6342e-12 | 1 / 400 | 2.025e-13 | 0 / 2000 |
| gpu_smoke (400 traj) | tgt | False | 2.7285e-12 | 49 / 400 | 5.0182e-14 | 0 / 2000 |
| gpu_smoke (400 traj) | valid | True | 0 | 0 / 400 | 0 | 0 / 2000 |

---

## 10. Decisions log and problems/risks

### 10.1 Decisions (`decisions/INDEX.md`)
| id | status | what was decided | why | consequences |
|---|---|---|---|---|
| `000` (planner, 1 Oct) | active | Frozen conventions: link order $(l_a,l_1,l_2,l_3)$; loop $U_\square=U_aU_3U_2^\dagger U_1^\dagger$; staggered phases with $\prod\eta=-1$ jointly with a *negative* magnetic coefficient ($c_B=-1/(4g_E^2)$ on-family, $-0.02$ at P-S); Jordan–Wigner order; P-A $=(1,3/8,0.25,-0.0625)$; P-S $=(1,3/8,0.02,-0.02)$ | The physics notes (9 Sept) state that $\prod\eta$ and the magnetic sign are one joint convention; the v0.6.1 ruling fixes P-A; reproducing the notes' $g_E=1$ table to 3 digits pins the convention | A change needs a new decision, a new fingerprint test and a J0 re-run. The L12 map (3793) is not used in v2 |
| `001` (planner, 2 Oct) | active | Numbered append-only artifacts created by `new_artifact.py`; the Graphify code graph (pinned `graphifyy==0.9.74`, code-only) committed and CI-checked | unambiguous order and citable ids; a graph rebuilt from the real tree each session closes the gap that let the twin-seed defect through review in the SU2ZX campaign (v0.6.3) | graph hooks off by default; `.claude/settings.json` not committed; LLM labels off |
| `002` (2 Oct) | superseded by 003 | Laptop for light work, Perlmutter by SSH for heavy jobs | no desktop GPU available | replaced because SSH needs a fresh NERSC key every 24 h |
| `003` (2 Oct) | superseded by 004 | Fixed-cap laptop runner, pull-based GitHub job queue, optional desktop worker | other sessions share the laptop; no NERSC credentials near an agent | replaced because it ignored current load and did not recover from crashes |
| `004` (2 Oct) | active | Laptop and Perlmutter only; admission-controlled laptop runner (`scripts/run.py`); self-healing worker (resubmission rules) | protects other sessions in both directions; GTX 1060 unusable with current PyTorch and broke the `coding` environment once | `localrun.py`, `jobs.retry_resources`, worker heartbeat; checks on the real laptop and Perlmutter later done in reports 006–008 |
| `005` (Digonto, 5 Oct; option C of `reports/010`) | active | J1 row "grounding $R^2$ energy" threshold $0.99\to0.887=0.97\times0.9145$, tied to `data/main` `73fff8e5a7b7` and the observation layout | measured ceiling: no regressor of one observation exceeds 0.9145 (four families agree 0.851–0.915; with couplings 0.994), so 0.99 is unreachable by construction; options A (keep 0.99), B (give the head the couplings; margin only 0.004; redo all runs) and D (drop the row) rejected | `configs/gates.yaml` edited (commit `2b10e5b`); plan §9/§11 and `prompts/010` still say 0.99 (plans are not edited); PREREGISTRATION H1 updated; re-measure the ceiling if the data or observation layout change; weakness: a better regressor could raise the ceiling slightly |

### 10.2 Problems and risks
**Open**
1. **The semigroup row of J1 fails for every finished rung** ($3.3\times10^{-3}$ to $2.2\times10^{-2}$ against $<10^{-3}$) and the residual grows with the rank (§8.3). Candidate fixes under test: a larger semigroup loss weight (jobs 011, 012). If these also fail, a method change goes to the planner (CLAUDE.md global rules).
2. **The rank row fails for four of six rungs**; the rungs that pass it (wsigreg2, wsigreg5, ema) have larger residuals; `v1_ema` additionally fails $P_{\text{meson}}$ (0.915). There may be no ladder rung that passes every row at once.
3. **No forecast results for any 200-epoch run.** Jobs 002–007 crashed before writing `forecast_eval.json`; jobs 008 (old code, will likely crash the same way: PROPOSED) and 011/012 (fixed code). The J2 input must be produced by a rerun of the chosen configuration at a commit with the fix.
4. **Which `data/main` checksum is the preregistration reference** (laptop `73fff8e5a7b7` or Perlmutter `76f4c9055591`) is undecided; numerically they are equivalent to about $10^{-13}$ (§8.4).
5. **The energy row rests on a measured ceiling** (0.9145) that a better regressor could raise (`decisions/005`).
6. Time-estimate defect of the runner (ignores the carrier); worker "stopped" warning false between 8 and 12 h idle; no GPU Aer on Perlmutter; `shots_per_second` is a prior (2,000/s), not a measurement.
7. **Schedule risk:** preregistration tag 16 Oct (10 days), J1 due 18 Oct, J2 30 Oct. Nothing about the twin, J2, J3, pilot or hardware has been run.
8. **Never yet tested:** any real hardware job, the IBM pilot, the calibrated twin, J2, J3, the 2×3 ladder, the quantum encoder.
9. **Hardware budget file not yet set up for the pilot:** `configs/hardware_budget.yaml` has `approved: false`, `backend: ibm_torino`, `max_qpu_seconds: 120`; `scripts/hw_list_backends.py` (task of `prompts/003`) is not written yet.
10. A decision for Digonto: pushing the preregistration tag (`git push --tags`) is a push; global rules say to ask before pushing.

**Resolved**
- GPU device bug in the baselines (commit `3fd0a65`; verified by `jobs/009`).
- Laptop/Perlmutter dataset difference diagnosed as rounding (`jobs/010`, §8.4).
- `fetch.py` overwriting tracked files (`3010090`).
- Adjacent training seeds (`0a76800`, spawned seeds).
- J1 energy row unreachable (`decisions/005`).
- `coding` environment broken by CUDA-13 packages (`reports/006`).
- False worker-stopped alarms understood (`reports/009`, `010`).
- Duplicate J1 ledger records removed (incident a); stray job file `jobs/013` deleted before commit (incident b).

### 10.3 Disagreements between sources that I noticed
1. **Plan audit table (§1, item 3) says the breaking fraction is "0.82 at $\mu^*=3/8$ versus below 0.15 at $\mu=0.30$ or $0.45$"; plan Appendix B.3 gives 0.227/0.555/0.740 at $t=16.7/33.3/50$.** My recomputation reproduces B.3 (P11d). The 0.82 may refer to a later time; I did not compute $t>50$.
2. **Plan B.3 says the on-family breaking fraction "falls monotonically 0.628 to 0.531"; the recomputed sequence is 0.62791, 0.63513, 0.62542, 0.59589, 0.53109** (not monotone; end points agree).
3. **Estimator bias threshold:** plan says $\le2.5$ SE (§10 W1); `configs/gates.yaml` says 4.0 (and plan §9 says 4). Measured 2.36 and 1.44 meet both.
4. **J1 energy threshold:** plan §9/§11 and `prompts/010` mention 0.99; `configs/gates.yaml` and `decisions/005` say 0.887 (the latter rule).
5. **`STATE.json` is out of date for M2:** it says jobs 004–008 running, node-hours used 0.859, "J1 NOT RUN", preliminary J1 for base and wsigreg2 only; the newer facts are 6 official J1 FAILs, 1.898 node-hours, jobs 004–007 FAILED (after training). This report uses the newer facts; I did not edit `STATE.json`.
6. **Pilot budget:** `prompts/004` says caps of 90 QPU-s; `configs/hardware_budget.yaml` has `max_qpu_seconds: 120`; the budget file's notes describe the pilot as "3 couplings × 2 depths × 2 settings × 1 arm = 12 circuits" whereas `prompts/003`/`004` describe $g_E=2$ only with KC-Trotter and KC-prep, $r\in\{1,8\}$, Z and X (also 12 circuits).
7. **Commit of the ladder jobs:** `reports/010`/`011` say every job is at commit `0a76800`; the job files of 003–008 carry the commit of the preceding "job:" commit (code identical to `0a76800`; only job files were committed in between, `git log`).
8. **`docs/CLAIMS.md` C6** says the mass-dependence evidence would be re-emitted as `evidence/J0_data/mass_dependence.json` in M1; that file does not exist (the numbers are only in the plan and now in §9 P11c/P11d).
9. **Training-time estimates:** plan §16 said 2–4 h on an A100 for the main run; measured about 1.0 h per rung of five unmasked seeds, 2.16 h for the base run with masked seeds.
10. The ledger prints the wsigreg5 rank minimum as 10.5; the exact value is 10.525 (the gate note's per-seed list says 10.53). Not a disagreement, a rounding.

---

## 11. What happens next

### 11.1 The rest of M2 (M2a continuation, `prompts/010`)
1. Wait for jobs 008 (`v1_curriculum`), 011 (`v1_wsemigroup1`), 012 (`v1_wsig2_wsg1`); check with `python scripts/jobs/status.py`; fetch each when COMPLETED or FAILED-after-training with `python scripts/jobs/fetch.py NNN` (the fixed fetch no longer overwrites `data/main/manifest.json`; compare any fetched checksum with the laptop's). Job 008 predates the GPU fix and will probably crash after training like 002–007 (PROPOSED); its training outputs will still be pushed.
2. J1 once per new rung: `python scripts/run.py -- python scripts/run_gate.py J1 --runs runs/<rung>/seed0 ... runs/<rung>/seed4` (never `seed*`, which also matches the masked folders).
3. **Choose the configuration.** `prompts/010` rule: the first rung in ladder order that passes every J1 row; if none passes, the best rung by rank, J1 PARTIAL, with a diagnosis (which loss term dominates, latent spectrum). The plan's PARTIAL fallback is written for the rank row; the semigroup row has no written fallback, so if jobs 011/012 also fail, the verdict needs Digonto's or the planner's ruling (PROPOSED). Expected result per `prompts/002`: rank 10–14, energy/$C_{\text{string}}$ $R^2$ above the thresholds, semigroup below $10^{-3}$ (not achieved so far).
4. **Diagnostics figure:** `python scripts/new_artifact.py figures "J1 effective rank and grounding R2 vs epoch" --ext .png`, then `python scripts/run.py -- python scripts/plot_j1_diagnostics.py --out <path> --rungs v1_base v1_wsigreg2 v1_wsigreg5 v1_latent32 v1_ema v1_wground3 v1_curriculum` (plus the two new rungs); a JSON sidecar is committed with it. The tables of §9 are the data of that figure.
5. **Model card** `docs/MODEL_CARD.md`: architecture, parameter count (90,309), training time per rung from the job status files (about 1.0 h and 0.25 node-hours per rung; §8.5), the chosen configuration and why, the energy ceiling.
6. **Re-queue the forecast evaluation** for the chosen configuration at a commit containing `3fd0a65` (for example the `v1_final` command of `prompts/003` step 1), to obtain `runs/<name>/forecast_eval.json` (cost estimate from the measured rungs: about 1 h and 0.25–0.55 node-hours; PROPOSED).
7. Update `STATE.json` (M2 entry), write the session report (`new_artifact.py reports "M2: ..." --milestone M2`), run the graph refresh and commit.

### 11.2 M2b — preregistration (16 Oct; `prompts/002` items 6–8)
- Freeze `configs/gates.yaml` (no change afterwards without a decision record).
- Complete `docs/PREREGISTRATION.md`: the frozen-inputs table (sha256 of `gates.yaml`; checksums of `data/main`, `data/chain_onfam`, `data/chain_strong`; the model configuration JSON; hardware design; backends) and the exact analysis commands; list `decisions/005` and `ceiling_main.json` among the frozen inputs.
- **Decide the reference `data/main` checksum.** Facts: `73fff8e5a7b7` (laptop) underlies J0, the ceiling and `decisions/005`; `76f4c9055591` (Perlmutter) underlies all training; the data are equal to about $10^{-13}$ in the clean targets and bit-identical in the noisy inputs. A PROPOSED wording: name both, state the fingerprint evidence, and make the gate checks insensitive to rounding.
- Tag: `git tag -a prereg-2026-10-16 -m "preregistration"`; pushing the tag needs Digonto's go-ahead.
- Run J1 on the chosen configuration; commit evidence.

### 11.3 M3 (W3, 19–25 Oct; `prompts/003`): forecasting, calibrated twin, dry run
- **M3a:** train the final model (`v1_final`, 5 seeds, 200 epochs, `--masked`) and obtain `forecast_eval.json`; write `scripts/resonance_eval.py` (strong family: forecast the breaking fraction at $t=20,30,50/g_E$ from the context at $t=8/g_E$ for each held-out $\mu$, fit a Lorentzian or parabola over $\mu$ to forecast and exact curves, report both maxima and their difference; evidence `evidence/J2_forecast/resonance.json`); figures F1 (held-out $g_E$ forecasts versus exact, all baselines) and F2 (resonance curve); a cross-carrier latent-distance check between `chain_onfam` and `main` records (should be comparable to the shot-noise scale).
- **M3b:** save the IBM account (the token is never pasted into a file under git); `scripts/hw_list_backends.py` (to be written); choose a backend; calibrated twin (`--noise-model` file built on the laptop); twin campaign `run_twin.py --K 12 --seeds 5` for both families (strong family KC-prep points $t=10,15,20$); `residual_eval.py` with shot levels 0, 512, 256; a **rehearsal** of J3 on the twin (labelled "twin rehearsal", not a J3 pass); hardware dry run on the live backend (pilot design 12 circuits), no submission.
- **Expected (plan):** rehearsal Spearman of `jepa_twin` $\ge$ `raw_twin` $-0.05$ at 512 shots; AUROC(arm B) $\ge0.9$ on the twin; dry-run estimate 8–12 circuits, 30–60 QPU-seconds, a 12-qubit line with summed CZ error below 0.05.

### 11.4 M4 (W4, 26 Oct – 1 Nov; `prompts/004`): J2 and the pilot (end of the one-month version)
- **M4a (30 Oct):** `run_gate.py J2 --eval runs/v1_final/forecast_eval.json`. Thresholds: JEPA MAE $\le0.05$ at $+4$ and $+8$ steps on each held-out family; JEPA $\le1.1\times$ ridge and autoregressive on at least 2 of 3 targets; masked-coupling task reported. Ablation table (`evidence/J2_forecast/ablations.json`): no SIGReg / no grounding / no semigroup / EMA target / latent 8 and 32, forecasting MAE per family, 3 seeds each. Figure F3 (baseline comparison); draft of "Results: forecasting" in `docs/PAPER_OUTLINE.md`. **Expectation (plan H2): parity, not superiority.** The only data so far (1 seed, 10 epochs, §9 P12b) has JEPA at 0.072 for $P_{\text{baryonic}}$ at $+8$ on-family, i.e. above 0.05, so a clear J2 pass is **not** to be assumed; if JEPA is worse than ridge the plan makes the forecasting claim parity or inferiority reported as such, and J3 the primary outcome.
- **M4b (pilot):** dry run on the day's calibration; Digonto sets `approved: true`, the manifest hash and caps (`max_qpu_seconds` 90, `max_jobs` 1, `max_cz_per_circuit` 200, shots 4,000); `hw_submit.py submit --dry-run-dir evidence/hardware/pilot --confirm`; `collect`; update the `shots_per_second` prior; `scripts/pilot_analysis.py` (to be written); figure F4; stop/go: go if post-selected $r=1$ populations are within 0.03 of the ideal circuit and the flag rate at $r=8$ is below 0.7. Expected: QPU time 40–90 s, flag rates 0.2–0.6.

### 11.5 M5 (W5, 2–8 Nov; `prompts/005`): hardware days 1 and 2
Per day (defined by the calibration snapshot hash): twin of the day (5 seeds, both families, both arms) queued to Perlmutter; dry run of the day's design (full or minimum depending on the remaining budget in `evidence/hardware/QPU_LEDGER.json`); **two jobs**, arm A (plain) and arm B (`--dd --twirl`), each needing its own human approval; collect; `scripts/hw_analysis.py` (to be written) converts raw counts to the `records.json` schema; `residual_eval.py --source hardware --reference ...`; day figures (depth ladder; strong-family resonance; the H4 panel). Day 2 extra: the on-family block on a second Open-plan QPU. **Expected:** depth-ladder error growing from about 0.03 ($r=1$) to 0.1–0.3 ($r=8$); KC-prep within 0.05 of ideal; resonance contrast at $t=20/g_E$ about 0.25 versus below 0.1; H4 forecast error $\le0.05$ against direct 0.1–0.3. Budget at most 5 QPU-min per day. All PROPOSED until measured.

### 11.6 M6 (W6, 9–15 Nov; `prompts/006`): day 3, J3, error budget
Day 3 as M5; residual evaluation over all days (shot levels 0/512/256); **J3 on 13 Nov** (thresholds in §5.4: at least 24 points, Spearman $\ge0.7$ at 512 shots, non-inferiority margin 0.05, AUROC $\ge0.8$, three days, all baselines reported); day-separation AUROC (reported even if null); $\mu^*$ from hardware (H5: within 0.05 of 0.375) in `evidence/J3_hardware/resonance_hw.json`; error-budget table `docs/ERROR_BUDGET.md`; draft "Results: hardware". Expected: J3 PASS or a clean PARTIAL (non-inferiority met, Spearman missed at 512 shots). If non-inferiority fails, the instrument claim is dropped and the dataset and carrier remain the contribution.

### 11.7 M7 (W7, 16–22 Nov; `prompts/007`): one stretch item, chosen 15 Nov by Digonto
(a) 2×3 ladder, simulator only (6 vertices, 7 links, 1,727 states to verify, stretched-string analogue, Krylov dimension and chain cost, 2,000-trajectory dataset, transfer test with 10 % fine-tuning); (b) quantum encoder J4 (12-qubit excitation-conserving circuit, latent of 8 expectation values, parameter-shift training, preregistered matched-shot test); (c) IonQ Forte via Braket only if the session prompt contains "paid provider approved by Digonto" (25 tasks × 2,500 shots, about \$5k). Drop order if W5–W6 slip: W7 entirely.

### 11.8 M8 (W8, 23–29 Nov; `prompts/008`): paper, release, replication
Assemble `paper/` (LaTeX; every number with an evidence path in a comment; claims table; error-budget table); release manifest `evidence/RELEASE_MANIFEST.json`; models as release assets; `scripts/replicate.sh` from a clean clone re-runs J0 (quick), J1 (from released histories), J2, J3 and the physics tests and must print the ledger's PASS/FAIL; `CITATION.cff` version bump; tag `v1.0.0-preprint`; preprint 27 Nov (hep-lat, cross-list quant-ph and cs.LG); checklist: advisor sign-off on scope against Sufian's report, no forbidden phrases, figures with evidence paths.

### 11.9 Hardware budget plan
Nothing has been spent: 0 of 600 QPU-seconds per 28-day window. Planned use: pilot 40–90 s (one job, cap 90–120 s, see disagreement 6); then per day about 150–300 s (full design about 5 min, minimum about 2.5 min), two windows (late Oct, Nov) for about 20 min in all; total design 8–13 QPU-minutes. Perlmutter: 1.898 of 50 node-hours used; whole plan estimate 15–40; each rung of five seeds costs about 0.25 node-hours, so the remaining ladder runs, the final run and the twin campaigns (about 480 circuits per hardware day, CPU only) fit inside the cap.

---

## 12. Code graph, problems and assumptions of this report, next action

**Code graph.** Nodes / edges / communities: 976 / 1,853 / 93 at `ade81b0` (`evidence/graph/stats.json`); before this report and after it the same, since I changed no code and ran no `graphify update`. No `graphify affected` check was needed. I used `graphify query` once to locate the definitions of the diagnostics (`models/train.py: diagnostics`, `models/jepa.py: effective_rank`).

**Problems and assumptions of this report.**
1. Values quoted from the plan or earlier reports that I did not re-derive are marked "quoted from"; the cross-check, the J0 gate, the ceiling, the J1 gate records, the job states, the fingerprint comparison, all histories and the physics curves I did read or recompute.
2. The coordinating session's facts (parameter counts, the diagnosis, the process incidents, the verification of job 009) were given to me; the parts I could check in files (job logs, status files, ledger, git log) agree with them. The deleted `jobs/013` and the duplicate ledger records no longer exist, so incidents (a) and (b) are reported on the coordinator's word.
3. Run histories and `model.pt` files are local (not in git); the tables in §9 are therefore the only copy outside the laptop.
4. "Breaking fraction" is defined here as $P_{\text{meson}}+P_{\text{baryonic}}$ by agreement with the plan's numbers, not by a definition I found in the plan.
5. I did not run the tests, the gates, or any job. The test count after the last commit and the CI state after the first one are not recorded.
6. The job states are those of `scripts/jobs/status.py` at about 05:50 UTC on 6 Oct; jobs 008, 011, 012 may have changed since.

**Next action.** `python scripts/jobs/status.py`, then continue with §11.1.

---

## Appendix A — helper scripts (verbatim; run with `python scripts/run.py --no-queue --threads 1 -- python <script> <out.md>` from the repository root)


### A.1 plot_tables.py (plots P1 to P9, P12)

```python
"""Build the plot-data tables of reports/012 from runs/<rung>/seed*/history.json.
Read-only. Run from the repository root through scripts/run.py. Writes Markdown to
the path given as argv[1] (default: plot_tables.md next to this script)."""
import json, math, sys, pathlib
import numpy as np

ROOT = pathlib.Path(".")
RUNS = ROOT / "runs"
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "plot_tables.md")
RUNGS = [  # (label, directory, seed-folder suffix)
    ("v1_base", "v1_base", ""),
    ("v1_base_masked", "v1_base", "_masked"),
    ("v1_wsigreg2", "v1_wsigreg2", ""),
    ("v1_wsigreg5", "v1_wsigreg5", ""),
    ("v1_latent32", "v1_latent32", ""),
    ("v1_ema", "v1_ema", ""),
    ("v1_wground3", "v1_wground3", ""),
]
EPOCHS = [1, 2, 5] + list(range(10, 201, 10))
R2NAMES = ["energy", "C_string", "P_meson", "P_baryonic"]


def load(dirname, suffix):
    hs = []
    for s in range(5):
        p = RUNS / dirname / f"seed{s}{suffix}" / "history.json"
        h = json.load(open(p))
        assert [r["epoch"] for r in h] == list(range(1, len(h) + 1)), p
        hs.append(h)
    return hs


DATA = {lab: load(d, suf) for lab, d, suf in RUNGS}


def val(rec, key):
    if key.startswith("r2_"):
        return rec["ground_r2"][R2NAMES.index(key[3:])]
    return rec[key]


def g(x):  # 5 significant digits
    return "nan" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.5g}"


lines = []
w = lines.append


def band_table(title, key):
    w(f"#### {title}\n")
    w("| rung | epoch | mean | min | max |")
    w("|---|---|---|---|---|")
    for lab, _, _ in RUNGS:
        for e in EPOCHS:
            v = np.array([val(h[e - 1], key) for h in DATA[lab]], float)
            w(f"| {lab} | {e} | {g(v.mean())} | {g(v.min())} | {g(v.max())} |")
    w("")


w("### P1 (data): effective rank vs epoch\n")
band_table("P1 table: eff_rank (mean, min, max over 5 seeds)", "eff_rank")
for i, (k, n) in enumerate(zip(R2NAMES, ["P2", "P3", "P4", "P5"])):
    w(f"### {n} (data): grounding R2 of {k} vs epoch\n")
    band_table(f"{n} table: R2 {k} (mean, min, max over 5 seeds)", "r2_" + k)
w("### P6 (data): semigroup residual vs epoch (draw on a log y axis)\n")
band_table("P6 table: semigroup_resid (mean, min, max over 5 seeds)", "semigroup_resid")

w("### P7 (data): training losses vs epoch, seed mean per rung\n")
w("| rung | epoch | pred | sigreg | ground | semigroup | total |")
w("|---|---|---|---|---|---|---|")
for lab, _, _ in RUNGS:
    for e in EPOCHS:
        m = [np.mean([h[e - 1][k] for h in DATA[lab]]) for k in ["pred", "sigreg", "ground", "semigroup", "total"]]
        w(f"| {lab} | {e} | " + " | ".join(g(x) for x in m) + " |")
w("")

w("### P8 (data): final-epoch (200) per-seed table\n")
w("| rung | seed | eff_rank | R2_energy | R2_C_string | R2_P_meson | R2_P_baryonic | semigroup_resid | isotropy | pred_loss |")
w("|---|---|---|---|---|---|---|---|---|---|")
pts = []
for lab, _, _ in RUNGS:
    for s, h in enumerate(DATA[lab]):
        r = h[-1]
        assert r["epoch"] == 200
        w(f"| {lab} | {s} | {g(r['eff_rank'])} | " + " | ".join(g(x) for x in r["ground_r2"][:4])
          + f" | {g(r['semigroup_resid'])} | {g(r['isotropy'])} | {g(r['pred'])} |")
        pts.append((lab, s, r["eff_rank"], r["semigroup_resid"]))
w("")

w("### P8b: per-rung summary of the final epoch (min / max over 5 seeds; this is what the J1 gate compares)\n")
w("| rung | rank min | rank max | R2 energy min | R2 C_string min | R2 P_meson min | R2 P_baryonic min | semigroup max | semigroup min | isotropy min | isotropy max |")
w("|---|---|---|---|---|---|---|---|---|---|---|")
for lab, _, _ in RUNGS:
    F = [h[-1] for h in DATA[lab]]
    rk = [f["eff_rank"] for f in F]
    r2 = [[f["ground_r2"][i] for f in F] for i in range(4)]
    sg = [f["semigroup_resid"] for f in F]
    iso = [f["isotropy"] for f in F]
    w(f"| {lab} | {g(min(rk))} | {g(max(rk))} | " + " | ".join(g(min(x)) for x in r2)
      + f" | {g(max(sg))} | {g(min(sg))} | {g(min(iso))} | {g(max(iso))} |")
w("")

w("### P9 (data): scatter, rank vs semigroup residual (final epoch, every seed)\n")
w("| rung | seed | eff_rank (x) | semigroup_resid (y, log axis) |")
w("|---|---|---|---|")
for lab, s, rk, sg in pts:
    w(f"| {lab} | {s} | {g(rk)} | {g(sg)} |")
w("")
un = [(rk, sg) for lab, s, rk, sg in pts if lab != "v1_base_masked"]
x = np.array([a for a, b in un]); y = np.log10([b for a, b in un])
pear = np.corrcoef(x, y)[0, 1]
rx = np.argsort(np.argsort(x)); ry = np.argsort(np.argsort(y))
spear = np.corrcoef(rx, ry)[0, 1]
w(f"Correlation over the {len(un)} unmasked final-epoch points (computed by this script): Pearson r(rank, log10 semigroup_resid) = {pear:.3f}; Spearman rho = {spear:.3f}.\n")

# loss-weight check: seed-mean of the semigroup *loss* term vs the *residual* at the end
w("### P7b: final-epoch seed-mean losses and weights (context for the semigroup diagnosis)\n")
w("| rung | pred | sigreg | ground | semigroup (loss term, unweighted as logged) | semigroup_resid (validation diagnostic) |")
w("|---|---|---|---|---|---|")
for lab, _, _ in RUNGS:
    F = [h[-1] for h in DATA[lab]]
    w(f"| {lab} | " + " | ".join(g(np.mean([f[k] for f in F])) for k in ["pred", "sigreg", "ground", "semigroup"])
      + f" | {g(np.mean([f['semigroup_resid'] for f in F]))} |")
w("")

# P12: v1_check
h = json.load(open(RUNS / "v1_check" / "seed0" / "history.json"))
w("### P12 (data): v1_check, 1 seed, 10 epochs, laptop (runs/v1_check/seed0/history.json)\n")
w("| epoch | total | pred | sigreg | ground | semigroup | eff_rank | R2_energy | R2_C_string | R2_P_meson | R2_P_baryonic | semigroup_resid | isotropy |")
w("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in h:
    w(f"| {r['epoch']} | {g(r['total'])} | {g(r['pred'])} | {g(r['sigreg'])} | {g(r['ground'])} | {g(r['semigroup'])} | {g(r['eff_rank'])} | "
      + " | ".join(g(x) for x in r["ground_r2"][:4]) + f" | {g(r['semigroup_resid'])} | {g(r['isotropy'])} |")
w("")
fe = json.load(open(RUNS / "v1_check" / "forecast_eval.json"))
w("### P12b (data): v1_check forecast MAE (runs/v1_check/forecast_eval.json; 1 seed, 10 epochs; NOT a J2 result)\n")
w(f"Context step {fe['context_step']}, eval steps {fe['eval_steps']}, dataset {fe['dataset']} (checksum {fe['checksum'][:12]}), n_test {fe['n_test']}.\n")
w("| family | method | horizon | P_baryonic | P_meson | C_string |")
w("|---|---|---|---|---|---|")
for fam in fe["mae"]:
    for meth in fe["mae"][fam]:
        for hz in ["+4", "+8"]:
            d = fe["mae"][fam][meth][hz]
            w(f"| {fam} | {meth} | {hz} | {g(d['P_baryonic'])} | {g(d['P_meson'])} | {g(d['C_string'])} |")
w("")
OUT.write_text("\n".join(lines))
print("wrote", OUT, len(lines), "lines")
```

### A.2 physics_curves.py (plot P11a to P11d)

```python
"""Recompute the physics curves of plan Appendix B (plot P11) with the repository's own physics core.
Read-only; run from the repository root through scripts/run.py. Writes Markdown to argv[1].
breaking fraction := P_meson + P_baryonic (definition tested against the plan's quoted numbers)."""
import sys, pathlib
import numpy as np
from su2qc_jepa.physics import conventions as C
from su2qc_jepa.physics.dynamics import evolve, sector_restrict
from su2qc_jepa.physics.observables import ObservableSet, named_states
from su2qc_jepa.physics.plaquette import PlaquetteModel

OUT = pathlib.Path(sys.argv[1])
model = PlaquetteModel(0.5)
obs = ObservableSet.primary(model)
n = named_states(model)
N4 = model.sector(4)
i0 = list(N4).index(n["S3"])
L = []
w = L.append


def run(coup, times):
    H4 = sector_restrict(model.hamiltonian(coup), N4)
    psi0 = np.zeros(len(N4)); psi0[i0] = 1
    psi_t = evolve(H4, psi0, np.asarray(times, float))
    full = np.zeros((len(times), model.dim), dtype=complex)
    full[:, N4] = psi_t
    ex = obs.expectation(full)
    return {k: ex[:, obs.index(k)] for k in ["P_S3", "P_S1", "P_meson", "P_baryonic", "C_string"]}


def g(x): return f"{x:.5g}"


w("#### P11a table: dynamics from S3 at P-A (g_E=2, mu=3/8), hardware times\n")
w("| t (1/g_E) | P_S3 | P_meson | P_baryonic | C_string |"); w("|---|---|---|---|---|")
tt = [0.375, 0.75, 1.5, 3.0]
r = run(C.POINT_PA, tt)
for i, t in enumerate(tt):
    w(f"| {t} | {g(r['P_S3'][i])} | {g(r['P_meson'][i])} | {g(r['P_baryonic'][i])} | {g(r['C_string'][i])} |")
w("")
w("#### P11a2 table: P-A dynamics from S3, fine time grid (t = 0 .. 3 in steps of 0.125)\n")
w("| t (1/g_E) | P_S3 | P_S1 | P_meson | P_baryonic | breaking (P_meson+P_baryonic) | C_string |"); w("|---|---|---|---|---|---|---|")
tt = list(np.arange(0, 3.0001, 0.125))
r = run(C.POINT_PA, tt)
for i, t in enumerate(tt):
    w(f"| {t:.3f} | {g(r['P_S3'][i])} | {g(r['P_S1'][i])} | {g(r['P_meson'][i])} | {g(r['P_baryonic'][i])} | {g(r['P_meson'][i]+r['P_baryonic'][i])} | {g(r['C_string'][i])} |")
w("")
w("#### P11b table: g_E = 1, mu = 3/8 (the physics notes' table), from S3\n")
w("| t (1/g_E) | P_baryonic | P_meson | P_S1 | C_string |"); w("|---|---|---|---|---|")
tt = [1.0, 2.0, 3.0]
r = run(C.POINT_G1, tt)
for i, t in enumerate(tt):
    w(f"| {t} | {g(r['P_baryonic'][i])} | {g(r['P_meson'][i])} | {g(r['P_S1'][i])} | {g(r['C_string'][i])} |")
w("")
w("#### P11c table: on-family (g_E = 2) breaking fraction at t = 3 vs mu\n")
w("| mu | P_meson | P_baryonic | breaking fraction |"); w("|---|---|---|---|")
for mu in [0.15, 0.25, 0.375, 0.5, 0.65]:
    r = run(C.Couplings.on_family(gE=2.0, mu=mu), [3.0])
    w(f"| {mu} | {g(r['P_meson'][0])} | {g(r['P_baryonic'][0])} | {g(r['P_meson'][0]+r['P_baryonic'][0])} |")
w("")
w("#### P11d table: strong coupling (c_H = 0.02, c_B = -0.02) breaking fraction vs mu at t = 16.7, 33.3, 50\n")
w("| mu | t=16.7 | t=33.3 | t=50 |"); w("|---|---|---|---|")
for mu in [0.15, 0.2, 0.25, 0.3, 0.33, 0.375, 0.42, 0.45, 0.5, 0.575, 0.65]:
    coup = C.Couplings(cE=1.0, cM=mu, cH=0.02, cB=-0.02)
    r = run(coup, [16.7, 33.3, 50.0])
    b = r["P_meson"] + r["P_baryonic"]
    w(f"| {mu} | {g(b[0])} | {g(b[1])} | {g(b[2])} |")
w("")
OUT.write_text("\n".join(L)); print("wrote", OUT)
```

### A.3 evidence_tables.py (P10, P11e, P11f, job and reproducibility tables)

```python
"""Tables of reports/012 built from evidence/ JSON files (read-only). Run from the repo root via scripts/run.py.
Writes Markdown to argv[1]."""
import json, sys, pathlib, glob, yaml
OUT = pathlib.Path(sys.argv[1]); L = []; w = L.append
g = lambda x: f"{x:.5g}" if isinstance(x, float) else str(x)

# --- P10: energy ceiling
c = json.load(open("evidence/J1_training/ceiling_main.json"))
w("#### P10 table: R2 ceilings from one clean observation (validation split, 26,348 rows; evidence/J1_training/ceiling_main.json)\n")
w("| inputs | target | ridge | knn5 | gbt | mlp |"); w("|---|---|---|---|---|---|")
for inp in ["obs", "obs+couplings"]:
    for tg in ["energy", "C_string", "P_meson", "P_baryonic"]:
        r = c["r2"][inp][tg]
        w(f"| {inp} | {tg} | {g(r['ridge'])} | {g(r['knn5'])} | {g(r['gbt'])} | {g(r['mlp'])} |")
w("")
w("Best R2 from the observation: " + ", ".join(f"{k} {g(v)}" for k, v in c["best_r2_from_obs"].items())
  + ". Best with couplings: " + ", ".join(f"{k} {g(v)}" for k, v in c["best_r2_from_obs_and_couplings"].items())
  + f". Clean-observation effective rank: raw {g(c['clean_obs_effective_rank']['raw'])}, standardised {g(c['clean_obs_effective_rank']['standardised'])}.\n")
w("Variance fractions of the standardised clean observations (18 directions, descending): " + ", ".join(g(v) for v in c["clean_obs_effective_rank"]["variance_fractions_standardised"]) + "\n")

# --- cross-check: Lanczos and P_S3 curves
x = json.load(open("evidence/J0_data/crosscheck_su2qc.json"))
w("#### P11e table: Lanczos coefficients from S3 (evidence/J0_data/crosscheck_su2qc.json, route C)\n")
w("| k | alpha_k P-A | beta_k P-A | alpha_k P-S | beta_k P-S |"); w("|---|---|---|---|---|")
for k in range(12):
    a = x["points"]["P-A"]["route_C"]; s = x["points"]["P-S"]["route_C"]
    w(f"| {k} | {g(a['alpha'][k])} | {g(a['beta'][k])} | {g(s['alpha'][k])} | {g(s['beta'][k])} |")
w("")
w("#### P11f table: P_S3(t) from S3 at the 12 cross-check times (route C)\n")
w("| i | t P-A | P_S3 P-A | t P-S | P_S3 P-S |"); w("|---|---|---|---|---|")
for i in range(12):
    a = x["points"]["P-A"]; s = x["points"]["P-S"]
    w(f"| {i+1} | {a['times'][i]} | {g(a['route_C']['P_S3'][i])} | {s['times'][i]} | {g(s['route_C']['P_S3'][i])} |")
w("")

# --- J1 gate records
w("#### J1 gate records (evidence/J1_training/*.json)\n")
names = {"20261005T231912Z": "v1_base", "20261005T234716Z": "v1_wsigreg2", "20261005T234719Z": "v1_wsigreg5",
         "20261006T000318Z": "v1_latent32", "20261006T024735Z": "v1_ema", "20261006T030159Z": "v1_wground3"}
w("| record | rung | status | rank min (thr 8) | R2 energy min (0.887) | R2 C_string min (0.99) | R2 P_meson min (0.95) | R2 P_baryonic min (0.98) | semigroup max (<0.001) | per-seed ranks (gate note) |")
w("|---|---|---|---|---|---|---|---|---|---|")
for k, n in names.items():
    d = json.load(open(f"evidence/J1_training/{k}.json"))
    R = {r["name"]: r for r in d["rows"]}
    st = lambda nm: f"{g(R[nm]['measured'])} {R[nm]['status']}"
    w(f"| {k} | {n} | {d['status']} | {st('effective rank (min over seeds)')} | {st('grounding R2 energy (min over seeds)')} | {st('grounding R2 C_string (min over seeds)')} | {st('grounding R2 P_meson (min over seeds)')} | {st('grounding R2 P_baryonic (min over seeds)')} | {st('semigroup residual (max over seeds)')} | {R['effective rank (min over seeds)']['note'].replace('per seed: ','')} |")
w("")

# --- jobs
w("#### Job table (jobs/*.yaml and evidence/jobs/NNN/status.json; states read on 2026-10-06 by scripts/jobs/status.py)\n")
w("| job | title (slug) | kind | job-file commit | Slurm limit | state | elapsed h | node-h | Slurm id |"); w("|---|---|---|---|---|---|---|---|---|")
for f in sorted(glob.glob("jobs/0*.yaml")):
    y = yaml.safe_load(open(f)); n = y["id"].split("/")[1]
    sp = pathlib.Path(f"evidence/jobs/{n}/status.json")
    s = json.load(open(sp)) if sp.exists() else {}
    w(f"| {n} | {y['title'].split(':')[0]} | {y['kind']} | {y['commit'][:7]} | {y['resources']['time']} | {s.get('state','(no status file; SUBMITTED per status.py)')} | {s.get('elapsed_hours','-')} | {s.get('node_hours','-')} | {s.get('slurm_id','-')} |")
tot = sum(json.load(open(p)).get("node_hours", 0) for p in glob.glob("evidence/jobs/*/status.json"))
w(f"\nSum of node_hours over the status files: {tot:.3f}\n")

# --- fingerprints
w("#### Dataset reproducibility (evidence/J0_data/fingerprint_compare_*.json; per-trajectory-sum tolerance 1e-12)\n")
w("| dataset | array | checksum equal | max abs diff of per-trajectory sums | trajectories above tol | max abs diff of sampled raw values (2000 samples) | samples above tol |")
w("|---|---|---|---|---|---|---|")
for nm, f in [("main (20,000 traj)", "evidence/J0_data/fingerprint_compare_main_laptop_vs_perlmutter.json"), ("gpu_smoke (400 traj)", "evidence/J0_data/fingerprint_compare_gpu_smoke_laptop_vs_perlmutter.json")]:
    d = json.load(open(f))
    for a, v in d["arrays"].items():
        w(f"| {nm} | {a} | {v['checksum_equal']} | {g(v['max_abs_diff_row_sum'])} | {v['rows_differing']} / {v['n_rows']} | {g(v['max_abs_diff_sample'])} | {v['samples_differing']} / {v['n_samples']} |")
w("")
OUT.write_text("\n".join(L)); print("wrote", OUT)
```

## Appendix B — file map (where things are)
| path | what |
|---|---|
| `plans/001_gauge-jepa-p-v2.md` | the active plan (`plans/000` superseded) |
| `prompts/000`–`010` | session prompts: 000 bootstrap, 001 physics and data (M1), 002 model and preregistration (M2), 003 forecast/twin/dry run (M3), 004 J2 and pilot (M4), 005 hardware days (M5), 006 day 3 and J3 (M6), 007 stretch (M7), 008 release (M8), 009 laptop environment repair, 010 M2a continuation |
| `reports/000`–`012` | one report per session; 011 is the 5 Oct overview, 012 this file |
| `decisions/000`–`005` | decision records (§10.1) |
| `configs/gates.yaml`, `configs/hardware_budget.yaml`, `configs/compute.yaml` | thresholds; human-edited approval file; compute settings |
| `STATE.json` | machine-readable project state (its M2 entry is behind; §10.3) |
| `docs/PHYSICS.md`, `CLAIMS.md`, `PREREGISTRATION.md` (draft), `PAPER_OUTLINE.md`, `PERLMUTTER.md` | living documents |
| `src/su2qc_jepa/physics/` | `conventions.py` (frozen), `plaquette.py` (routes A/B), `su2.py`, `observables.py`, `dynamics.py` (Lanczos, Krylov), `chain.py` (carrier circuits and samplers) |
| `src/su2qc_jepa/data/` | `records.py` (observation layout, estimators), `trajectories.py` (dataset generator, fingerprint) |
| `src/su2qc_jepa/models/` | `jepa.py` (model, SIGReg, effective rank), `train.py` (training, diagnostics, probes, baselines) |
| `src/su2qc_jepa/gates/` | `j0_data.py`, `j1_training.py`, `j2_forecast.py`, `j3_hardware.py`, `ledger.py` |
| `src/su2qc_jepa/twin/`, `hardware/ibm.py` | noise-model twin; budget-checked IBM submission |
| `src/su2qc_jepa/localrun.py`, `jobs.py`, `compute.py` | laptop runner, job format, device choice |
| `scripts/` | `run.py`, `make_dataset.py`, `train_jepa.py`, `run_gate.py`, `crosscheck_su2qc.py`, `record_datasets.py`, `j1_ceiling.py`, `plot_j1_diagnostics.py`, `compare_fingerprints.py`, `residual_eval.py`, `run_twin.py`, `hw_dry_run.py`, `hw_submit.py`, `new_artifact.py`, `check_artifacts.py`, `graph_update.sh`, `env_check.py`, `jobs/{enqueue,status,fetch}.py`, `worker/` |
| not yet written (named in the prompts) | `resonance_eval.py`, `hw_list_backends.py`, `hw_analysis.py`, `pilot_analysis.py`, `depth_extrapolation.py`, `docs/MODEL_CARD.md`, `docs/ERROR_BUDGET.md`, `paper/` |
| `tests/` | `test_physics.py`, `test_pipeline.py`, `test_crosscheck.py`, `test_jobs.py`, `test_localrun.py`, `test_compute.py`, `test_repo_conventions.py`, `test_scrontab_merge.py` |
| `evidence/GATE_LEDGER.md` | all gate results |
| `evidence/J0_data/` | `20261003T201012Z.json` (J0), `crosscheck_su2qc.json`, `datasets.json`, `fingerprint_compare_main_laptop_vs_perlmutter.json`, `fingerprint_compare_gpu_smoke_laptop_vs_perlmutter.json` |
| `evidence/J1_training/` | six J1 gate records, `ceiling_main.json` |
| `evidence/jobs/NNN/` | `status.json`, `log.txt`, `outputs/` per fetched job (000–007, 009, 010) |
| `evidence/graph/stats.json`, `evidence/ENV.json` | code-graph statistics; environment record |
| `jobs/000`–`012` | job requests for the Perlmutter worker; results on the git branch `results` |
| `runs/<rung>/seed*/{history.json,model.pt}`, `runs/<rung>/args.json` | training outputs (local, not in git): `v1_base` (+ `seed*_masked`), `v1_wsigreg2`, `v1_wsigreg5`, `v1_latent32`, `v1_ema`, `v1_wground3`, `v1_check`, `gpu_smoke`, `cli_check` |
| `data/main`, `data/chain_onfam`, `data/chain_strong`, `data/gpu_smoke` | datasets (local, not in git) |
| `graphify-out/` | code graph (`graph.json`, `GRAPH_REPORT.md` committed) |
| `.local_runs/` | laptop runner ledger and logs (git-ignored) |

## Appendix C — commit list (`git log --oneline`, newest first, 51 commits)
```
80d7fdf gate: J1 FAIL for v1_latent32, v1_ema, v1_wground3
8a80885 gate: J1 FAIL for v1_base, v1_wsigreg2, v1_wsigreg5 (semigroup residual; rank only for base)
a1da245 data: laptop vs Perlmutter builds of data/main and gpu_smoke agree to ~1e-13 (jobs/010)
3010090 chore: fetch.py keeps a differing local file and stores the job's copy under evidence/jobs/NNN/outputs/
ad4af2e job: 012_v1-wsig2-wsg1-estimated-510-min-20-min-on-the-laptop-perlmut (train on perlmutter)
8be2aa4 job: 011_v1-wsemigroup1-estimated-510-min-20-min-on-the-laptop-perlmu (train on perlmutter)
25567ea job: 010_fingerprints-of-main-and-gpu-smoke-rebuilt-on-perlmutter (dataset on perlmutter)
36f4224 chore(graph): refresh code graph
ade81b0 data: dataset fingerprint (per-trajectory sums + fixed samples) to compare laptop and Perlmutter builds; --w-semigroup flag
872ed09 job: 009_gpu-smoke-needs-a-gpu-the-laptop-gpu-is-not-used-perlmutter (train on perlmutter)
5000bc9 chore(graph): refresh code graph
3fd0a65 model: baselines run on the data's device (fixes jobs/002, 003 crash on the GPU)
9e9c496 chore(graph): refresh code graph
5a934f7 docs: project overview report (reports/011); STATE: jobs 002/003 failed after training (GPU device bug in baselines), Perlmutter data/main checksum differs
12ad4df chore(graph): refresh code graph
2b10e5b gate: J1 energy grounding threshold 0.99 -> 0.887 (decisions/005)
339d900 chore(graph): refresh code graph
ee58679 docs: M2a session report (reports/010), follow-up prompt (prompts/010), STATE M2 in progress
070238d model: J1 diagnostics figure script (rank, grounding R2, semigroup vs epoch per rung)
f1cc1f3 gate: J1 grounding ceilings from one clean observation (energy R2 <= 0.914)
63065dd job: 008_v1-curriculum-estimated-510-min-20-min-on-the-laptop-perlmut (train on perlmutter)
7a18cdb job: 007_v1-wground3-estimated-510-min-20-min-on-the-laptop-perlmutte (train on perlmutter)
aa7f8af job: 006_v1-ema-estimated-510-min-20-min-on-the-laptop-perlmutter (train on perlmutter)
0cf933f job: 005_v1-latent32-estimated-510-min-20-min-on-the-laptop-perlmutte (train on perlmutter)
1c60d57 job: 004_v1-wsigreg5-estimated-510-min-20-min-on-the-laptop-perlmutte (train on perlmutter)
a3ab4ca job: 003_v1-wsigreg2-estimated-510-min-20-min-on-the-laptop-perlmutte (train on perlmutter)
1d9c4d0 job: 002_v1-base-estimated-1017-min-20-min-on-the-laptop-perlmutter (train on perlmutter)
0a76800 model: EMA target encoder, horizon curriculum, grounding-weight flag, SeedSequence training seeds
5b9277e data: dataset checksums for main, chain_onfam and chain_strong (recorded at 358d0bd)
4930515 chore(graph): refresh code graph
0cff86f docs: M1 session report (reports/009), STATE M1 PASS
358d0bd data: fetch jobs/001 (chain_strong built on Perlmutter, COMPLETED, 0.056 node-h)
d385a54 gate: J0 PASS on data/main (9/9 rows); dataset checksums for main and chain_onfam
0fccca4 data: record_datasets hashes the data arrays only (the generator's rule) and accepts manifest-only Perlmutter datasets
2915f11 job: 001_chain-strong-estimated-45-min-20-min-on-the-laptop-perlmutte (dataset on perlmutter)
9affe3a data: record_datasets.py writes checksums and split sizes to evidence/J0_data/datasets.json
41a3bb0 physics: su2qc cross-check evidence, PASS at P-A and P-S (max dev 7.4e-14)
0bb5d6d physics: cross-check route C against su2qc routes 1 and 2 (prompts/001 Part A)
be8c177 chore(graph): refresh code graph
2b4bad4 chore(test): worker tests start from an empty job queue
4496f98 chore(graph): refresh code graph
4b7a028 docs: Perlmutter worker smoke test COMPLETED on A100 (jobs/000, reports/008)
273f5cb job: 000_worker-smoke-test (check on perlmutter)
80efb3d chore(compute): Perlmutter worker installed; account m4135_g
8e82e6d chore(graph): refresh code graph
2b0ea41 chore(test): keep host shell functions and BASH_ENV out of the stand-in Slurm job
74fbcc7 chore(graph): refresh code graph
73a1ae5 chore(worker): installers accept the GPU account (m1234_g) and keep the env under the bare project
208952c chore(graph): refresh code graph
0b98ca3 docs: M0 session report
88dc52d chore: bootstrap su2qc-jepa starter package (Gauge-JEPA-P v2, plans/001)
```
