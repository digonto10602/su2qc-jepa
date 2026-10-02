---
id: plans/001
title: Gauge-JEPA-P v2 — JEPA world model with a Krylov-chain hardware carrier
series: plans
created_utc: '2026-10-01T17:45:00Z'
author: planner
milestone: null
status: active
supersedes: plans/000
superseded_by: null
---

# Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier

**Revised plan, 1 October 2026 (supersedes the 1 Oct "Gauge-JEPA-P" plan). Eight weeks, 5 Oct – 29 Nov 2026. One researcher driving Claude Code sessions. Starter package: `su2qc-jepa` (this repository).**

*Amended 2 Oct 2026 (same plan number; no physics or gate changes): compute: laptop (resource-aware, self-healing runner) + Perlmutter job queue only (§16, `decisions/004`); repository conventions added — every plan, prompt, report, decision record and figure is a numbered, append-only file in its own folder, and Claude Code tracks the codebase with the Graphify code graph. See §15 and `decisions/001`. This plan was `docs/PLAN.md` on 1 Oct; the plan it supersedes is kept as `plans/000`.*

Labels that are the author's own and not standard physics terms are marked *(label)* the first time they appear.

---

## 0. The idea in one paragraph

Take the project's verified SU(2)-with-matter plaquette (82 gauge-invariant states at $j_{\max}=\tfrac12$; the string-breaking dynamics from the stretched string S3 lives in the 38-state $N=4$ sector) and train a *JEPA world model* on it: an encoder maps a finite-shot measurement record to a 16-dimensional latent, a predictor advances the latent under actions (time steps at given couplings, mass quenches), and the loss asks the predicted latent to match the latent of the clean future record. Everything is exactly solvable, so the paper claims a method and a hardware instrument, not quantum advantage. What is new relative to the 1 Oct plan: the hardware carrier is a **Krylov chain** *(label)* — the 12 Lanczos vectors that span the dynamics are encoded one-hot on 12 qubits of a line, so the gauge theory's propagator becomes a nearest-neighbour XY chain that costs **22 CZ per Trotter step**, has a genuine **depth ladder** (34 → 188 CZ for $t = 0.375 \ldots 3/g_E$) and a built-in **excitation flag** (any shot with $\ne 1$ excited qubit is a detected error). This turns the plan's two hardware claims — label-free error signal and "forecast late times from shallow hardware records" — into things the device can actually test, inside the IBM Open Plan's 10 QPU-minutes per 28 days, with light work on the laptop and the few heavy jobs on Perlmutter.

---

## 1. Audit of the 1 Oct plan — issues found and what changed

Severity: **H** = would have blocked a publishable result, **M** = would have cost weeks or credibility, **L** = cosmetic. Every item was checked against the project's physics-setup notes (9 Sept), the v0.5.0 review, the Sufian overlap note, and numbers measured in this session with the starter package (Appendix B).

| # | Sev. | Issue in the 1 Oct plan | Evidence | Fix in v2 |
|---|---|---|---|---|
| 1 | **H** | The hardware layer used only "Krylov playback" (state preparation of a classically known 2–5-qubit state). Every time point costs the same ~13–27 CZ, so there is **no depth ladder**: result R4 ("forecast $t=3/g_E$ from noisy $r=1$ beats direct noisy $r=3$") could only ever be a simulator result, and the "hardware error signal" would be a state-prep fidelity benchmark. | Sufian overlap note §2; plan's own R4 caption "simulator result" | **Krylov-chain carrier**: one-hot Lanczos basis on $K=12$ qubits, Strang-Trotterised XY chain, $2(K-1)=22$ CZ per step, depths $r=1,2,4,8$ (34/56/100/188 CZ, two-qubit depth 6/10/18/34). R4 becomes a hardware result. A second arm, **KC-prep** *(label)*, prepares the exact state with $K-1 = 11$ XY rotations (22 CZ) and plays the role of the old playback baseline — on the same qubits, with the same flag. |
| 2 | **H** | No label-free **baselines for the residual**. With everything exactly solvable, the raw observation-space distance to the twin (or to the ideal circuit) correlates ~perfectly with the exact error, so "Spearman ≥ 0.7" is trivially satisfiable and says nothing about JEPA. | Smoke run (App. B.6): raw twin residual Spearman 0.997 with the exact error when the ideal-circuit output is used | J3 now preregisters three JEPA residuals (`jepa_twin`, `jepa_self`, `jepa_t0`) against two label-free baselines (`raw_twin`, `flag_rate`); the pass criterion is **non-inferiority at low shot counts** (512) plus arm/day separation (AUROC), where the encoder's denoising can matter. |
| 3 | **H** | Forecasting baselines were guessed ("ridge ~0.08–0.12"). Measured: with the mass given as an action input and the 1 Oct coupling grid, ridge regression already reaches 0.02–0.04 MAE at held-out masses — because at the P-A point the dynamics **barely depend on the mass** (App. B.3: breaking fraction at $t=3/g_E$ moves only from 0.63 to 0.53 across $\mu\in[0.15,0.65]$). | App. B.3, B.5 | Two coupling **families** replace the 9-mass scan: (i) *on-family* points $(c_H,c_B)=(1/2g_E,-1/4g_E^2)$ with $g_E$ scanned and **held out by $g_E$** (dynamics depend strongly on $g_E$); (ii) *strong-coupling* points $c_H=|c_B|=0.02$ (the P-S regime) with $\mu$ scanned around the resonance and **held out by $\mu$** — there the resonance is sharp (breaking fraction 0.82 at $\mu^*=3/8$ vs < 0.15 at $\mu=0.30$ or $0.45$). A **masked-coupling task** (couplings hidden; the model must infer them from early records) is added. |
| 4 | **H** | R3 ("$\mu^*_{\text{model}}$ within 0.05 of 3/8 at $g_E=2$") is not testable at $g_E=2$: no resonance peak is visible in the window $t\le 3/g_E$ (monotone in $\mu$). | App. B.3 | R3 moves to the strong-coupling family, where the resonance is the dominant feature. |
| 5 | **H** | IBM budget was "10–30 min of Heron time" without checking the plan. The **Open Plan gives 10 min per 28-day rolling window** (plus an opt-in of 180 min/year announced March 2026); Heron r3 (`ibm_boston`, 2.15×10⁻³ two-qubit error) is Premium/Flex only. | IBM plans page; Quantum Insider 13 Jan 2026 | Campaign designed to **~8–13 QPU-minutes total** across two 28-day windows (pilot + day 1 in October's window, days 2–3 in November's). Budget file + ledger + dry-run discipline in the package. Pay-as-you-go ($96/min) is the fallback for one extra day, not a plan. |
| 6 | **M** | IonQ priced at "USD 1–3k". On Amazon Braket only **Forte** is listed ($0.30/task + $0.08/shot; 2,500-shot minimum with error mitigation); Aria was withdrawn. 100 tasks × 1,000 shots ≈ $8k; with mitigation ≈ $20k. | Braket pricing page | IonQ is **out of the critical path**; cross-device becomes cross-backend (two Open-plan Heron QPUs). IonQ only if the group already holds credits. |
| 7 | **M** | Quantum encoder (J4) with a predicted null consumed weeks 5–7 and ~40 GPU-h. | Plan's own R6 | Moved to an optional appendix experiment in week 7 (simulator only); its time goes to the hardware campaign and the ladder stretch. |
| 8 | **M** | "~200 Perlmutter GPU node-hours" assumed an allocation that may not exist, and every stated job fits a desktop: exact dynamics are 82×82, the twin is a 12-qubit density matrix (0.3 GB), the JEPA is ~0.2 M parameters. | App. B.7 timings | Laptop (CPU, capped, admitted only when there is room) for light work; Perlmutter, through a GitHub job queue, for everything above 20 laptop-minutes or needing a GPU — about 15–40 node-hours in all, capped at 50 (§16). |
| 9 | **M** | Observation vector "built identically from exact states, twin L12 records and hardware Krylov records" was not identical: Krylov records cannot yield leakage flags, and L12 records cannot yield Krylov populations. | Plan §Model | One observation layout for all sources: 18 physical observables + flag rate + source one-hot + carrier one-hot; carrier-specific estimators (`records.py`) produce the same physical observables; flags are a per-carrier channel (gauge leakage for L12, excitation flag for the chain). |
| 10 | **M** | Twin σ's from v0.5.0 were void (adjacent seeds). The plan said "distinct twin seeds" but had no test. | v0.6.2 ruling; SU2QC contracts | `TwinRunner.seeds` derives seeds from `SeedSequence(...).spawn`; the **twin variance check** is a J0 row and a unit test. |
| 11 | **M** | The 1 Oct plan had the L12 encoding (2,156 two-qubit gates per Strang step) as "twin data only"; it adds nothing to the hardware story and costs twin time. | v0.5.0 review | L12 twin data become optional (week 7) — useful only for the leakage-flag head. |
| 12 | **L** | "9 masses in [0.15, 0.65]" at 0.0625 spacing does not contain 0.3 or 0.5, the held-out values named in the plan. | Arithmetic | Grids fixed (App. A); held-out values are grid points. |
| 13 | **L** | The P-A coefficient discrepancy (1:0.5:0.25 vs 1:0.25:0.0625) and the L12 map (3793) were listed as "close first" but with no owner. | Physics notes §10.2 | P-A is frozen here as $g_E=2$: $(1, 3/8, 0.25, -0.0625)$ — the v0.6.1 ruling. The starter package reproduces the project's $g_E=1$ preliminary expectation exactly (App. B.2), which fixes the conventions independently of the L12 map; L12 is not used on hardware in v2. |
| 14 | **L** | Timeline put the paper in a single week after the last hardware day. | — | Figures and sections are written at each gate (`docs/PAPER_OUTLINE.md` filled by the gate sessions); week 8 is assembly, error budget and replication. |
| 15 | **M** | No rule for where prompts, reports and figures go or how they are named, and no way for a session to see the codebase it is changing. In the SU2ZX campaign the generated code documentation covered a different package than the one under gate, which let the twin-seed defect through review (v0.6.3). | v0.6.3 prompt, R13–R15 | Numbered, append-only artifacts in `plans/`, `prompts/`, `reports/`, `decisions/`, `figures/` created only by `scripts/new_artifact.py` and checked in CI; the Graphify code graph rebuilt from the actual tree every session and checked fresh in CI (§15, `decisions/001`). |

**What was kept from the 1 Oct plan.** The physics object and conventions; the JEPA architecture (encoder, action-conditioned predictor, SIGReg anti-collapse, grounding heads, semigroup consistency); the "noisy context, clean target" training rule; the gate-and-evidence discipline; the claim boundaries (method + instrument, no quantum advantage, no new SU(2) physics); the 8-week shape with a one-month simulator-only version.

---

## 2. Why v2 is better — side by side

| | 1 Oct plan | v2 (this plan) | Why it matters |
|---|---|---|---|
| Hardware circuits | Krylov playback, 2–5 qubits, 13–27 CZ, no depth structure, no flags | Krylov chain, 12 qubits, 22 CZ/step, depths 34–188 CZ, excitation flag; KC-prep arm (22 CZ) on the same qubits | R4 and the error-signal claim become hardware results; flags give a label-free baseline the 1 Oct plan admitted it had lost |
| Hardware object | "2×2 plaquette" via playback | the same 2×2 plaquette — nothing larger is attempted on hardware | matches what the device can do; the 2×3 ladder is a simulator stretch only |
| QPU budget | 10–30 min assumed | ≈ 8–13 min designed, 1.5-min pilot measures the real rate | fits the Open Plan; nothing depends on paid time |
| Couplings | 9 masses × 3 ratios, held out by mass | two families, held out by $g_E$ (on-family) and by $\mu$ (strong coupling) | the held-out tasks are actually hard (measured), the resonance is where it is visible |
| Baselines | ridge, autoregressive (for forecasting only) | ridge, autoregressive, supervised MLP; masked-coupling variant; label-free residual baselines | the paper survives a null result honestly |
| Compute | laptop + 200 Perlmutter node-hours | one runner on the laptop that admits light work only when there is room, caps it and heals it; heavy or GPU work always queued through GitHub to a self-healing Perlmutter worker, ≲ 50 node-hours | other sessions on the laptop are protected, crashes recover by themselves, a quarter of the earlier allocation |
| Quantum encoder | weeks 5–7 | optional appendix, week 7 | time goes to hardware |
| IonQ | required (R8) | optional with credits; cross-backend instead | no $8–20k dependency |
| Starter code | none | verified physics core (route A/B agree to 4×10⁻¹⁶, Gauss law exactly), estimators, JEPA, twin, hardware guard, gates, CI | week 1 starts from passing tests, not from scratch |
| Artifacts and codebase tracking | not specified | numbered, append-only plans/prompts/reports/decisions/figures; Graphify code graph rebuilt every session, freshness checked in CI | a reviewer can trace every result to the prompt that produced it, and no session works on code it has not mapped |

The one thing v2 does **not** do better: the KC chain pays more CZ per time point than Sufian's 3-qubit playback (34 vs 13–27 at the shallowest depth). That is the price of a depth ladder and flags, and it is still 100× below the L12 route.

---

## 3. Physics object (frozen) and measured fingerprints

Model: hard-core SU(2) Kogut–Susskind plaquette, $j_\ell\in\{0,\tfrac12\}$ on four links, two-colour staggered fermions on four vertices, open boundaries (geometry, loop orientation $U_\square=U_aU_3U_2^\dagger U_1^\dagger$, staggered phases with $\prod_\square\eta=-1$, Jordan–Wigner order as in `src/su2qc_jepa/physics/conventions.py`). In units of the electric quantum $g_E=g^2/2a$:

$$\frac{H}{g_E}=\sum_\ell j_\ell(j_\ell+1)+\mu\sum_n(-1)^{n_x+n_y}N_n+c_H\sum_\ell\big(\eta_\ell\,\psi_n^\dagger U_\ell\psi_{n'}+\text{h.c.}\big)+c_B\,\mathrm{Tr}\big(U_\square+U_\square^\dagger\big),$$

with on-family coefficients $c_H=1/(2g_E)$, $c_B=-1/(4g_E^2)$ and $\mu=m/g_E$. Times are quoted in units of $1/g_E$ throughout.

Coupling points: **P-A** $g_E=2,\ \mu=3/8$ → $(1,\ 0.375,\ 0.25,\ -0.0625)$; **P-S** (Sufian regime) $(1,\ 0.375,\ 0.02,\ -0.02)$; the on-family scan $g_E\in\{1.0,1.15,1.3,1.45,1.6,1.75,2.0\}$.

Measured in this session with the starter package (all reproduce the project's verified numbers):

* 82 states; sectors $N=0,2,4,6,8$: 2/20/38/20/2; electric degeneracies 16/16/18/16/16; $j_{\max}=1$: 152 states, 3/36/74/36/3.
* Route A (vertex singlets + block tensors) and route B (full 160,000-dimensional space, sparse) agree to $4\times10^{-16}$; $\|[G^a_n,H]\|=0$ exactly; $H$ leaves the physical subspace invariant to $2\times10^{-16}$.
* Named-state energies: $E_{S3}-E_{\Omega_0}=2\mu+9/4$, $E_{S1}-E_{\Omega_0}=2\mu+3/4$, $E_{MM}-E_{\Omega_0}=4\mu+3/2$, $E_{\text{Loop}}-E_{\Omega_0}=3$ — the three degeneracies coincide at $\mu^*=3/8$.
* Hopping term: 4 links × 36 disjoint real 2×2 blocks (288 non-zeros); plaquette term: 41 disjoint pairs (82 non-zeros).
* Dynamics at $g_E=1,\ \mu=3/8$ from S3: $P_{\text{baryonic}}(t=1,2,3)=0.432,\ 0.732,\ 0.821$; $P_{\text{meson}}<0.04$; $P_{S1}<0.02$; $C_{\text{string}}(3)=0.238$ — the project's preliminary expectation (physics notes §8.1) to three digits.
* Channel split in $N=4$: 8 (pair) + 2 (meson) + 26 (baryonic) + 2 (vacuum matter); $P_{B\bar B}$ has 4 states, $P_{\text{hopped}}$ 6.
* Effective Krylov dimension from S3 at P-A: $\beta_{27}\approx10^{-6}$ (the project's "28 of 38" preliminary); the full sector is reached only through couplings below $10^{-4}$.

Truncation ($j_{\max}=1$ vs $\tfrac12$) over the hardware window at P-A, $\mu=3/8$: $|\Delta P_{S3}|\le0.053$, $|\Delta P_{\text{meson}}|\le0.060$, $|\Delta P_{\text{baryonic}}|\le0.014$, $|\Delta C_{\text{string}}|\le0.034$. This is a line of the error budget, not something the hardware can resolve.

---

## 4. The Krylov-chain carrier (KC)

**Construction.** Lanczos from $|S3\rangle$ under $H$ restricted to the $N=4$ sector gives orthonormal vectors $|k\rangle$ and a tridiagonal $H_K=\sum_k\alpha_k|k\rangle\langle k|+\sum_k\beta_k(|k\rangle\langle k{+}1|+\text{h.c.})$. Encode $|k\rangle$ as the single-excitation state of $K$ qubits on a line (qubit $k$ in $|1\rangle$, others $|0\rangle$). In that sector $|k\rangle\langle k|\to n_k=(1-Z_k)/2$ and $|k\rangle\langle k{+}1|+\text{h.c.}\to(X_kX_{k+1}+Y_kY_{k+1})/2$, so $H_K$ is an XY chain with site fields.

**Two arms on the same qubits.**

* **KC-Trotter** *(label)*: $e^{-iH_Kt}$ by a Strang product formula, time order $E/2,\ A/2,\ O,\ A/2,\ E/2$ per step ($A$ = fields, free $R_z$'s; $E,O$ = even/odd bonds, one `XXPlusYY` gate = 2 CZ each); consecutive even half-layers merge. Cost $2[(r{+}1)\lceil(K{-}1)/2\rceil + r\lfloor(K{-}1)/2\rfloor]$ CZ for $r$ steps. The ideal circuit is simulated **exactly inside the sector** with $K\times K$ matrices (no $2^K$ simulation), which is the noiseless reference for every hardware point.
* **KC-prep** *(label)*: prepare $\sum_k c_k(t)|k\rangle$ directly by a cascade of $K-1$ `XXPlusYY` rotations plus one $R_z$ layer (22 CZ, two-qubit depth 22 at $K=12$). Same qubits, same flag, no depth ladder — the analogue of the Sufian playback arm.

**Flags.** Both arms conserve the excitation number; a Z-basis shot with $\ne1$ excited qubit is discarded and counted (the *excitation flag* — an encoding-violation flag, not a gauge-violation flag; the paper says so).

**Measurement settings.** Z (populations $|c_k|^2$ + flag) and X (real coherences: $\langle X_kX_{k'}\rangle=2\,\mathrm{Re}\,\rho_{kk'}$ inside the sector). Because $H_K$ is real and the start vector is real, every physical observable $O$ has a **real symmetric** $O_K=Q_K^{\mathsf T}OQ_K$, so only real parts are needed: $\langle O\rangle=\sum_{kk'}(O_K)_{kk'}\mathrm{Re}\,\rho_{kk'}$. Y is an optional third setting for cross-checking. The sector renormalisation $\mathrm{Re}\,\rho_{kk'}\to\mathrm{Re}\,\rho_{kk'}/p_1$ (divide coherences by the single-excitation fraction) is a mitigation arm, reported raw and renormalised.

**Measured costs at P-A ($g_E=2$, $\mu=3/8$), $K=12$, $\Delta t=0.375$:**

| steps $r$ | $t$ ($1/g_E$) | CZ (KC-Trotter) | two-qubit depth | Strang infidelity (vs $e^{-iH_Kt}$) | synthetic-twin flag rate | post-selected population error |
|---|---|---|---|---|---|---|
| 1 | 0.375 | 34 | 6 | $2\times10^{-5}$ | 0.23 | 0.006 |
| 2 | 0.75 | 56 | 10 | $8\times10^{-5}$ | 0.28 | 0.011 |
| 4 | 1.5 | 100 | 18 | $3\times10^{-4}$ | 0.38 | 0.020 |
| 8 | 3.0 | 188 | 34 | $1.2\times10^{-3}$ | 0.55 | 0.016 |

(The synthetic twin uses CZ error $3\times10^{-3}$, readout 1–2 %, $T_1=250\,\mu$s, $T_2=150\,\mu$s — Heron r2-like; the calibrated twin replaces it from the pilot day.) Krylov truncation at $K=12$: observable error $\le1.1\times10^{-4}$ over $t\le3/g_E$ (needs $K=11$ for $10^{-3}$, $K=9$ for $10^{-2}$). The same $K=12$ covers the on-family points $g_E\ge1.3$ to $10^{-3}$ over $t\le3/g_E$ ($g_E=1$ needs $K=13$).

**Strong-coupling family on hardware.** At $c_H=0.02$ the chain fields are $O(1)$ while the physics is slow (resonant transfer at rate ~0.02), so Trotterising the chain is hopeless (hundreds of steps). There the hardware arm is **KC-prep only**, at $t\in\{10,15,20\}/g_E$ where $K=12$ reproduces the dynamics to $10^{-3}$ ($K=11$ suffices at $t=20.8$). The mass dependence is large there (breaking fraction at $t=16.7/g_E$: 0.23 at $\mu=3/8$, 0.05 at $\mu=0.25$, 0.007 at $\mu=0.15$), so this is where the model's $\mu^*$ estimate and the held-out-mass forecasts are tested on hardware.

**What the carrier is and is not.** The Lanczos basis is computed classically from the exact solution; the device re-enacts a classically compressed propagator. It is a *hardware testbed with known truth and controllable depth*, which is exactly what validating a label-free error instrument needs. It is not a quantum simulation beyond classical reach, and the paper will say so in the first paragraph of the hardware section. It generalises (K grows with system size and time window) but that is not claimed here.

---

## 5. The world model

**Observation layout** (`data/records.py`, dimension 24): 18 physical observables — $\langle N_v\rangle$ (4), $\langle j_\ell(j_\ell{+}1)\rangle$ (4), $P_{\text{pair}},P_{\text{meson}},P_{\text{baryonic}},P_{\text{vacmatter}},P_{S3},P_{S1},P_{\text{hopped}},P_{B\bar B},P_{\text{antivac}}$, $C_{\text{string}}$ — plus the flag rate, a source one-hot (exact / twin / hardware) and a carrier one-hot (diagonal / chain). Exact states, twin records and hardware records all pass through the same estimator; the exact source *emulates* the carrier's measurement (multinomial over the configuration basis for the diagonal carrier; exact sequential sampling of Z- and X-basis bitstrings for the chain carrier — a closed-form conditional sampler, App. B.4).

**Actions** $a_t=(\Delta t,\ c_M,\ c_H,\ c_B)$; a mass quench changes $c_M$ mid-trajectory. **Clean target**: exact expectation values with zero flag. **Noisy context**: $S\in\{256,512,1024,4096\}$ shots.

**Architecture** (`models/jepa.py`): encoder MLP ($24\to128\to128\to16$, LayerNorm, GELU); predictor = GRU over action tokens initialised from the latent with a skip connection; grounding heads = one linear map to (energy, $C_{\text{string}}$, $P_{\text{meson}}$, $P_{\text{baryonic}}$, flag). Loss = prediction MSE at horizons $k\in\{1,2,4,8\}$ + SIGReg (Epps–Pulley statistic on 64 random 1-D projections, LeJEPA) + grounding MSE on context and target latents + semigroup consistency $P(s,[a,a])\approx P(P(s,[a]),[a])$. Readout for forecasting = ridge probe from clean latents, fit on the training split.

**Baselines** (same inputs: noisy observations up to the context step + all actions): ridge regression; autoregressive one-step MLP rolled out in observation space; direct supervised MLP. Each also in the masked-coupling variant.

**Tasks.**
1. *Forecasting* (J2): from the noisy record at context step $c=4$ ($t=1/g_E$ at $\Delta t=0.25$), predict $P_{\text{baryonic}},P_{\text{meson}},C_{\text{string}}$ at $+4$ and $+8$ steps on the held-out split of each family.
2. *Masked-coupling identification* *(label)*: the same with $(c_M,c_H,c_B)$ zeroed in the actions — the model must infer the coupling from the early record.
3. *Label-free error signal* (J3): on twin and hardware records, `jepa_twin` = latent distance to the reference twin record; `jepa_self` = distance between the measured deep record and the prediction propagated from the shallowest record of the same series; `jepa_t0` = the 1 Oct definition (prediction from the exact initial record). Baselines `raw_twin`, `flag_rate`. Scored against the exact error, at full shots and at 512/256 shots by exact subsampling of the stored counts.
4. *Depth extrapolation on hardware* (R4): compare the forecast of $t=3/g_E$ observables from the $r=1,2$ hardware records with the direct $r=8$ hardware estimate.
5. *$\mu^*$ from held-out data* (R3, strong-coupling family): fit the resonance maximum of the forecast breaking fraction over $\mu$.

**Smoke-scale status (starter package, CPU, minutes):** training is stable (no NaN), the probe/forecast/baseline path works, but the v0 model is *not yet good*: effective rank 4–6 of 16, grounding $R^2$ 0.81–0.99, forecasting at or behind ridge. Week 2 exists to fix this (§10). The gate thresholds are the targets, not the current state.

---

## 6. Data

| Dataset | Family | Carrier | Trajectories | Steps × $\Delta t$ | Purpose |
|---|---|---|---|---|---|
| `main` | on-family + strong | diagonal | 20,000 (10k + 10k) | 8–12 × {0.125, 0.25, 0.5} (on-family) / {2, 4, 8} (strong) | training, J1, J2 |
| `chain_onfam` | on-family, S3 starts, no quench | chain ($K=12$) | 5,000 | 8–12 × 0.375 | cross-carrier training, residual rehearsal |
| `chain_strong` | strong, S3 starts | chain ($K=24$ exact emulation) | 3,000 | 8 × {2,4,8} | cross-carrier training |
| `ladder` (stretch) | on-family | diagonal | 2,000 | — | transfer test |

Grids: on-family $g_E\in\{1.0,1.15,1.3,1.45,1.6,1.75,2.0\}$ (held out **1.3, 1.75**; validation 1.45) × $\mu\in\{0.15,0.25,0.375,0.5,0.65\}$; strong-coupling $\mu\in\{0.15,0.2,0.25,0.3,0.33,0.375,0.42,0.45,0.5,0.575,0.65\}$ (held out **0.3, 0.42, 0.5**; validation 0.45). Starts: S3 ×3, S1, random $N=4$ superposition. Quench fraction 0.2. Splits by rule only (checked by J0 row D6). Generation cost: ~0.1 s per trajectory on one core → 20,000 in ~35 min.

---

## 7. The twin

Aer density-matrix simulation of the 12-qubit chain circuits (268 MB state; 6–30 s per circuit on two CPU cores; much faster with `qiskit-aer-gpu` on a Perlmutter A100). Noise: synthetic Heron-like model for development; `NoiseModel.from_backend` of the day's calibration for every hardware day (the twin is *calibrated, not trusted* — J3 measures its distance from the device). Seeds: `SeedSequence(master).spawn`, one per circuit; the variance check is a J0 row. Twin campaign per hardware day: 2 families × (24 + 24 circuits) × 2 arms × 5 seeds ≈ 480 circuits ≈ 1–4 laptop hours, so full campaigns run on Perlmutter and pilot-size runs (≤ ~100 circuits) on the laptop; the calibrated noise model is built on the laptop (where the IBM token lives) and shipped with the job as a file. "Arm B" on the twin is a degraded noise model (2× CZ error, 2× readout) standing in for a worse day until real day-to-day calibration data exist.

---

## 8. The hardware campaign

**Access assumption:** IBM Quantum Open Plan (10 QPU-min per 28-day window; opt in to the extra 180 min/year if offered), Heron r2 devices (`ibm_torino`-class). The dry run against `FakeTorino` already selects a 12-qubit line from calibration data (CZ + readout error score) and transpiles with zero routing overhead (CZ counts 34/56/100/188 preserved).

**Per calibration day (full design):**

| Family | Arm | Points | Settings | Circuits | Shots |
|---|---|---|---|---|---|
| on-family: $g_E\in\{1.3,1.75,2.0\}$, $\mu=3/8$ | KC-Trotter $r\in\{1,2,4,8\}$ | 12 | Z, X | 24 | 4,000 |
| on-family | KC-prep at the same four times | 12 | Z, X | 24 | 4,000 |
| strong: $\mu\in\{0.3,0.375,0.42,0.5\}$ | KC-prep at $t\in\{10,15,20\}$ | 12 | Z, X | 24 | 4,000 |
| all of the above | mitigation arm B (DD + gate twirling) | — | — | 72 | 4,000 |

144 circuits × 4,000 shots = 576k shots ≈ 4.8 min at the prior rate of 2,000 shots/s plus ~0.5 min overhead → **~5 min/day**; three days ≈ 15 min. **Minimum design** (fits 10 min + pilot): drop KC-prep on the on-family and arm B on the strong family → 72 circuits ≈ 2.5 min/day. The **pilot** (12 circuits, ~1 min) measures the real shots-per-second, flag rates and line quality; the budget file is then re-approved with measured numbers. Two Open-plan windows (late Oct, Nov) give 20 min without paying.

**Discipline** (`hardware/ibm.py`, enforced in code): dry run → manifest with circuit hashes and an estimate → the human sets `approved: true` and the manifest hash in `configs/hardware_budget.yaml` → `submit --confirm` re-checks hashes, job cap, CZ cap and the QPU ledger, snapshots calibration, submits **one** Sampler job, records the job id → `collect` writes immutable raw counts and the measured usage. Claude Code never edits the approval fields.

**Cross-backend day** (replaces IonQ): the on-family block on a second Open-plan Heron QPU, same day, to test transfer of the residual's sign and scale.

---

## 9. Gates and preregistration

Thresholds live in `configs/gates.yaml`; gate scripts (`scripts/run_gate.py`) are the only arbiters and append to `evidence/GATE_LEDGER.md`. Preregistration = the frozen `gates.yaml` + `docs/PREREGISTRATION.md` + dataset checksums, signed (committed with a tag) on **16 Oct**. Status vocabulary: PASS / FAIL / PARTIAL / NOT RUN / VOID.

| Gate | When | Rows (summary) | On failure |
|---|---|---|---|
| **J0 data** | 11 Oct | fingerprints (82, sectors, degeneracies); two routes $\le10^{-12}$; Gauss commutator $\le10^{-12}$; estimator bias $\le4$ SE for both carriers; $K=12$ reproduces P-A window to $10^{-3}$; twin repeats distinct; split leakage 0; checksum recorded | physics is frozen — a J0 failure is a code defect; fix before anything else |
| **J1 training** | 18 Oct | 5 seeds; no NaN; effective rank $\ge8/16$; grounding $R^2\ge0.99$ (energy, $C_{\text{string}}$), $\ge0.95$ ($P_{\text{meson}}$), $\ge0.98$ ($P_{\text{baryonic}}$); semigroup residual $<10^{-3}$ | ablation ladder: EMA target, latent 32, SIGReg weight sweep, grounding weight, longer training; if rank stays $<8$ after the ladder, report the collapse diagnosis and continue with the best model (J1 PARTIAL) |
| **J2 forecast** | 30 Oct | per family: JEPA MAE $\le0.05$ at $+4,+8$; not worse than ridge and autoregressive (within 1.1×) on $\ge2/3$ targets; masked-coupling task reported | if JEPA is worse than ridge: the forecasting claim becomes parity/inferiority **reported as such**; the paper's primary outcome is J3 |
| **J3 hardware** | 13 Nov | $\ge24$ points; Spearman(`jepa_twin`, exact error) $\ge0.7$ at 512 shots; non-inferior to `raw_twin` within 0.05; AUROC $\ge0.8$ for arm B vs A; 3 calibration days; all baselines reported | if non-inferiority fails: the instrument claim is dropped, the hardware dataset and the carrier remain the contribution |
| **J4 quantum encoder** (optional) | week 7 | trains at 12 qubits; matched-shot test vs classical encoder and vs classical simulation of the circuit | reported either way |

---

## 10. Week by week — what Claude Code does, what is tested, what we expect

Each week is one or two Claude Code sessions, each driven by a numbered prompt (`prompts/000` … `prompts/008`; repair or follow-up prompts get the next free number). Every session follows `CLAUDE.md` §2: it starts with `scripts/env_check.py` and a code-graph freshness check (`scripts/graph_update.sh --check`, then the first screen of `graphify-out/GRAPH_REPORT.md`), answers codebase questions through `graphify query/explain/affected` before broad searching, and ends with its gate (if any), a committed evidence bundle (`evidence/<gate>/<utc>.json` + ledger row), a graph rebuild, a numbered session report (`reports/NNN_*.md`, with graph statistics before and after), `scripts/check_artifacts.py` OK and an updated `STATE.json`. Session reports take the next free number in `reports/` (000–002 record the package build and its two amendments).

### W1 (5–11 Oct) — bootstrap, physics cross-check, data → J0
*Sessions M0, M1.*
- **M0 (first invocation, `prompts/000`):** `env_check`; `pytest`; `scripts/check_artifacts.py`; `scripts/bootstrap_repo.sh` installs Graphify, registers it with Claude Code, builds and commits the first code graph, creates `github.com/digonto10602/su2qc-jepa` (public) and pushes; CI green (lint, artifact check, tests, graph freshness). Definition of done: repository URL, all fast tests passing, `evidence/ENV.json`, committed `graphify-out/graph.json`, the M0 session report with `status: done`.
- **M1:** cross-check the starter physics core ("route C" here) against the project's verified `su2qc` code (SU2ZX, routes A/B): named-state energies, full 82-state spectra at P-A and P-S, the $g_E=1$ dynamics table, the Krylov coefficients from S3. Any disagreement above $10^{-10}$ stops the session (physics is the top priority). Then generate `main`, `chain_onfam`, `chain_strong`; run J0.
- **Tests:** `tests/test_physics.py` (fingerprints, two routes, Gauss law, dynamics expectation, Krylov window, chain circuits, samplers), `tests/test_pipeline.py`; J0 rows D1–D6.
- **Expected:** J0 PASS by 11 Oct. Numbers: 82/2-20-38-20-2/16-16-18-16-16; two-route difference $\sim10^{-16}$; estimator bias $\le2.5$ SE; $K=12$ error $1.1\times10^{-4}$.
- **If it fails:** a convention mismatch with `su2qc` (most likely the plaquette sign or a Jordan–Wigner string) → fix in `conventions.py` with an ADR; the fingerprints cannot tell those apart, the spectra and dynamics can.

### W2 (12–18 Oct) — JEPA v1, collapse diagnostics, preregistration → J1
*Sessions M2a (model), M2b (preregistration).*
- **M2a:** a 10-epoch, 1-seed check on the laptop, then train on `main` on Perlmutter (5 seeds, 200 epochs; `run.py` queues it automatically); run the ablation ladder in order until J1 rows pass: (1) SIGReg weight ∈ {0.5, 2, 5}; (2) latent 32; (3) EMA target encoder with stop-gradient (I-JEPA style) as an alternative to SIGReg; (4) grounding weight 3; (5) horizon curriculum (1,2 first, then 4,8). Record effective rank, isotropy, grounding $R^2$, semigroup residual per run (`history.json`).
- **M2b (16 Oct):** freeze `configs/gates.yaml`, write `docs/PREREGISTRATION.md` (hypotheses H1–H5 below, analysis plan, exclusion rules), tag `prereg-2026-10-16`.
- **Expected:** J1 PASS with rank 10–14/16, $R^2>0.99$ on energy and $C_{\text{string}}$. Risk: the smoke run gave rank 4–6 and $R^2(P_{\text{meson}})=0.70$–$0.74$; $P_{\text{meson}}$ is small ($<0.1$ on-family) and its $R^2$ threshold (0.95) may need the strong-coupling data to be met — the threshold stays, the reason is reported.

### W3 (19–25 Oct) — forecasting, twin rehearsal, hardware dry runs
*Sessions M3a (forecast), M3b (twin + dry run).*
- **M3a:** `train_jepa.py --masked` on `main`; `forecast_eval.json`; per-family tables; $\mu^*$ estimator on the strong family (fit of the forecast breaking fraction over $\mu$); figures F1 (forecast vs truth at held-out $g_E$), F2 (resonance curve, forecast vs exact).
- **M3b:** calibrated twin: `NoiseModel.from_backend` of a live Open-plan backend (needs the saved IBM account); twin campaign `run_twin.py --K 12` (both arms, 5 seeds); `residual_eval.py`; J3 **rehearsal** on the twin (not a gate pass — the twin is not the device). Hardware dry run against the live backend (no submission): manifest, qubit line, estimate.
- **Expected:** rehearsal Spearman of `jepa_twin` ≥ `raw_twin` − 0.05 at 512 shots; AUROC(arm B) ≥ 0.9 on the twin (the smoke run already gave 1.0 vs 0.70 for raw). Dry-run estimate ≈ 60 QPU-s for 24 circuits.

### W4 (26 Oct – 1 Nov) — J2, pilot job; end of the one-month version
*Sessions M4a (J2), M4b (pilot).*
- **M4a (30 Oct):** J2 on `forecast_eval.json` (5 seeds averaged). Ablation table (no SIGReg / no grounding / no semigroup / EMA). Figure F3 (baseline comparison).
- **M4b:** pilot: 12 circuits (on-family $g_E=2$, $r\in\{1,8\}$ × KC-Trotter/KC-prep × Z/X), 4,000 shots, arm A, **one job**; human approves the budget file; `hw_submit.py submit --confirm`; `collect`; measured QPU seconds → update `estimate_qpu_seconds` prior; flag rates vs twin; line quality. Stop/go review of bit order, mapping and flag rates against the twin.
- **Expected:** pilot flag rates 0.2–0.6 (readout-dominated at $r=1$); post-selected populations within 0.03 of the ideal circuit at $r=1$; QPU time 40–90 s. **One-month deliverable** = J0–J2 + twin rehearsal + pilot: a simulator-and-twin methods note with one hardware pilot figure.

### W5 (2–8 Nov) — hardware days 1 and 2
*Sessions M5a, M5b (one per day).*
- Each day: calibration snapshot → `NoiseModel.from_backend` twin of the day (5 seeds) → dry run with the day's best line → approval → one job per arm (two jobs; arm B = DD + twirling) → collect → `residual_eval.py --source hardware` → day figure; a second Open-plan QPU on day 2 if the window allows (cross-backend block).
- **Expected:** on-family depth ladder shows post-selected observable error growing from ~0.03 ($r=1$) to 0.1–0.3 ($r=8$); KC-prep points within 0.05 of the ideal circuit; strong-coupling resonance visible on hardware: $P_{\text{meson}}+P_{\text{baryonic}}$ at $t=20/g_E$ clearly larger at $\mu=3/8$ than at $\mu=0.30$ or $0.50$ (exact: 0.555 vs 0.071 vs 0.042 at $t=33$; at $t=20$ the contrast is 0.23–0.3 vs < 0.1).
- **R4 on hardware:** forecast of $t=3/g_E$ from the $r=1,2$ records vs the direct $r=8$ record; expected forecast error ≤ 0.05 against direct 0.1–0.3.

### W6 (9–15 Nov) — day 3, J3, advantage-free analysis
*Sessions M6a (day 3), M6b (J3 + analysis).*
- Day 3 as above; then `residual_eval.py` over all days; J3 (13 Nov); day-separation AUROC (may be null if drift is small — reported); the $\mu^*$ hardware estimate from the strong family; error-budget table assembled (truncation, Krylov, Trotter, shot, device, twin mismatch — each a measured line).
- **Expected:** J3 PASS or a clean PARTIAL (non-inferiority met, Spearman threshold missed at 512 shots). Either is publishable with the dataset.

### W7 (16–22 Nov) — one stretch item, chosen on 15 Nov
*Session M7.* In priority order, pick **one**: (a) 2×3 ladder: generalise the route-A engine to 6 vertices / 7 links (3-link vertices have intertwiner multiplicity 2), compute $K(t)$ from the ladder's S3 analogue and the chain cost; simulator-only transfer test of the world model (R7); (b) quantum encoder J4 on CUDA-Q/Aer statevector, matched-shot test; (c) IonQ Forte via Braket **only if** the group already holds credits (≥ 25 tasks × 2,500 shots ≈ $5k). Drop order if W5–W6 slip: W7 entirely.

### W8 (23–29 Nov) — paper, release, replication
*Sessions M8a (paper), M8b (release).* Assemble `paper/` from the gate-session sections; claim table (§11); error budget; code/data/model release with checksums; clean-environment replication of J0–J3 from the released artefacts (`scripts/replicate.sh`, which also re-checks the artifact conventions and the code graph); preprint 27 Nov (hep-lat, cross-list quant-ph, cs.LG).

---

## 11. Preregistered hypotheses and expected results

* **H1 (no collapse).** With SIGReg + grounding, effective rank ≥ 8/16 and grounding $R^2$ ≥ 0.99 on energy and $C_{\text{string}}$. *Expected: met after the W2 ladder; the v0 smoke model does not meet it.*
* **H2 (forecasting).** JEPA + probe reaches MAE ≤ 0.05 at $+8$ steps on both held-out families and is not worse than ridge/autoregressive within 1.1×. *Expected: parity, not superiority, on the plain task; a possible advantage on the masked-coupling task where a latent system identification is needed. The paper reports the comparison either way.*
* **H3 (label-free error signal).** At 512 shots, `jepa_twin` is non-inferior to `raw_twin` in rank correlation with the exact error and separates mitigation arms with AUROC ≥ 0.8. *Expected: non-inferiority at low shots (denoising), tie at 4,000 shots; day separation possibly null.*
* **H4 (depth extrapolation on hardware).** Forecast of $t=3/g_E$ from the $r\le2$ hardware records has lower error than the direct $r=8$ hardware estimate for ≥ 2 of 3 targets at all three $g_E$. *Expected: yes, by a factor 2–5.*
* **H5 (resonance from hardware).** The $\mu^*$ estimate from the strong-coupling hardware points (KC-prep) lies within 0.05 of 3/8. *Expected: yes; the four-mass design brackets the resonance.*

**Claims table (what the paper may say if the gates pass / may never say):**

| Supported if gates pass | Not supported by this work |
|---|---|
| A 12-qubit, 22-CZ-per-step hardware carrier for the string-breaking dynamics of the SU(2) plaquette with matter, with a depth ladder and an encoding flag | Quantum advantage of any kind; the plaquette is exactly solvable |
| A JEPA world model trained on exact/twin/hardware records that forecasts late-time channel weights at held-out couplings within a stated error, compared with baselines | New SU(2) physics, a continuum limit, string tension, 2+1D (the plaquette is the smallest 2D unit; "2+1D" is reserved for ≥ 2×3) |
| A label-free hardware error signal validated where the truth is known, with its label-free baselines | Hardware evidence of gauge leakage (the chain cannot leak gauge-wise; the flag is an encoding flag) |
| A hardware observation of the strong-coupling resonance on the plaquette via a compressed carrier | Scalability of the carrier beyond small $K$ |
| An open benchmark dataset (exact, twin, hardware) with checksums and a preregistered evaluation | |

---

## 12. Error budget (lines, each measured)

| Line | Source | Size (P-A window) | Where measured |
|---|---|---|---|
| Truncation $j_{\max}=\tfrac12$ | $j_{\max}=1$ reference (152 states) | ≤ 0.06 on $P_{\text{meson}}$, ≤ 0.014 on $P_{\text{baryonic}}$ | App. B.3 |
| Krylov truncation $K=12$ | exact vs $K$-dim propagation | ≤ $1.1\times10^{-4}$ | J0 row D4 |
| Trotter (Strang, $\Delta t=0.375$) | ideal circuit vs $e^{-iH_Kt}$ | infidelity ≤ $1.2\times10^{-3}$ at $r=8$ | `trotter_error` |
| Shot noise (4,000 shots, Z+X) | exact sampler | ~0.01–0.02 on chain estimates | J0 row D3 |
| Device (post-selected) | hardware vs ideal circuit | pilot | W4 |
| Twin mismatch | hardware vs calibrated twin | `raw_twin` | J3 |
| Model (forecast) | probe/forecast vs exact | J2 | W4 |

---

## 13. Publishability

A methods-and-benchmark paper with hardware data: "A learned world model and a Krylov-chain hardware carrier for SU(2) string breaking on a plaquette". Venues in order of fit: *Quantum* or *Machine Learning: Science and Technology* (method + benchmark + hardware instrument; either outcome of H2/H3 is publishable there), *Phys. Rev. D* (if the hardware resonance observation and the error budget are the centre), *PRX Quantum* (stretch; would need H3 to beat, not tie, the raw residual). Lattice 2027 proceedings in any case. Scope must be settled with the advisor against Sufian's report before the preprint: same model, same resonance, his Krylov route is the KC-prep arm's ancestor and is cited as such; the chain carrier, the flags, the world model and the preregistered evaluation are new.

Without J3 (no device time): the one-month version is an ML-venue simulation study with the twin rehearsal and the carrier's cost table.

---

## 14. Assumptions, risks, open points

**Assumed.** Start 5 Oct 2026; IBM Open Plan access with a saved account (10 min/28 days; opt-in extra minutes if offered); the laptop (CPU) for development and all light work, NERSC Perlmutter (Digonto's allocation, one A100 in the shared queue) for the 5-seed training runs, the ablation ladder and full twin campaigns — if Perlmutter is unavailable, those run on the laptop at 1 seed (training) or overnight (twin) and the reports say so; no IonQ unless credits exist; the project's `su2qc` code is available for the W1 cross-check (if not, the starter core's agreement with the project's published numbers — fingerprints, energies, the $g_E=1$ dynamics table — is the cross-check).

**Risks and the branch taken.** (1) JEPA does not beat ridge → report parity; the instrument and the carrier carry the paper. (2) Rank stays low → EMA target ablation; report. (3) Open-plan queue latency makes a "calibration day" span two days → the day is defined by the calibration snapshot hash, not the date. (4) Flag rates above 0.6 at $r=8$ → drop $r=8$, add $r=6$. (5) The X-setting estimates are noisier than Z (variance ∝ $K^2$ terms) → 4,000 shots on X, 2,000 on Z if the budget binds. (6) Day-to-day drift too small to separate days → report null; arm separation is the primary AUROC.

**Open points to close in W1.** Sign convention of the magnetic term at P-S (frozen here as negative, same as on-family); whether the project's `su2qc` route B kernel and this package's route B agree on the Gauss-law generator convention (they should: $E_L=-(S^a)^{\mathsf T}$, $E_R=+S^a$); the actual Open-plan device list on 5 Oct.

---

## 15. Repository conventions — numbered artifacts and the code graph (added 2 Oct 2026; `decisions/001`)

**Numbered artifacts.** Everything a person reads that the project *produces* is a numbered, append-only file in its series folder, named `NNN_<slug>.<ext>`:

| Folder | What goes there | Who creates it |
|---|---|---|
| `plans/` | plans; the active one has `status: active` (`000` = 1 Oct plan, superseded; `001` = this plan) | planner |
| `prompts/` | every prompt for a Claude Code session — the nine milestone prompts `000`–`008` and any repair, escalation or follow-up prompt written later | planner (Claude in Cowork) or Claude Code |
| `reports/` | one report per session, plus analysis and review reports (`000`, `001` = package build) | Claude Code, planner |
| `decisions/` | decision records: conventions, thresholds, tool versions (`000` conventions, `001` this section) | either |
| `figures/` | every figure a report or the paper cites | Claude Code |

Numbers are allocated only by `python scripts/new_artifact.py <series> "<title>" --milestone Mx [--supersedes <series>/NNN]`, which writes YAML front matter (`id`, `title`, `series`, `created_utc`, `author`, `milestone`, `status`, `supersedes`, `superseded_by`) from `templates/` and regenerates the folder's `INDEX.md`. A revision is a new number; the replaced file only has its `status` set to `superseded`. Numbers are never deleted or reused (`status: withdrawn` instead). `scripts/check_artifacts.py` checks names, uniqueness, absence of gaps, front matter, cross-references and index freshness; it runs in the test suite and in CI. Living documents (`README.md`, `CLAUDE.md`, `docs/*.md`, `configs/*`, `STATE.json`) are edited in place and versioned by git; machine records (`evidence/**`) keep their UTC stamps and job ids because they are immutable and referenced by hash.

**Code graph.** Claude Code tracks the codebase with Graphify (PyPI `graphifyy`, pinned at 0.9.74; command `graphify`). In code-only mode it parses the repository locally with tree-sitter (a parser library) into a graph of files, classes, functions, imports, calls and Markdown headings — so the prompts, reports and plans are in the graph too — and clusters it into communities; no LLM and no API key are involved. Measured on the starter package (2 Oct 2026): rebuild in about 2 s; two rebuilds byte-identical with `PYTHONHASHSEED=0`; paths stored relative to the repository. Per session: freshness check and `GRAPH_REPORT.md` at the start; `graphify query / explain / path` for codebase questions; `graphify affected "<symbol>"` before changing a function, with the tests of everything it lists; `bash scripts/graph_update.sh` at the end, committed as `chore(graph):`; node/edge/community counts before and after in the session report. Committed: `graphify-out/graph.json` and `GRAPH_REPORT.md`; ignored: cache, HTML view, manifest, labels, dated snapshots. CI rebuilds the graph and fails if the committed one is structurally stale (nodes and edges compared; commit stamp and community numbering ignored). Off by default: Graphify's git hooks (they leave the tree dirty after every commit and create dated snapshot folders) and LLM community labelling. The graph is navigation, not review: it is never cited as evidence that code is correct. In M1 the same tool maps the SU2ZX `su2qc` code (kept outside this repository) to locate the Hamiltonian builders and the twin seeding code for the cross-check.

## 16. Compute: the laptop and Perlmutter only (amended 2 Oct 2026; `decisions/004`, superseding `decisions/003` and `decisions/002`)

The project runs on exactly two machines. The **laptop** (Dell G7 7588: 64 GB RAM, 6-core / 12-thread i7-8750H, GTX 1060 Max-Q) runs Claude Code and light work. **NERSC Perlmutter** (A100 GPU nodes) runs everything heavy. The laptop's GPU is not used: current PyTorch CUDA builds contain no kernels for its Pascal architecture, and installing them broke the `coding` environment once (repaired by `prompts/009`). The laptop is shared with other Claude sessions, and protecting them is the first rule.

**One entry point: `scripts/run.py`.** Every computation (tests, gates, datasets, training, twin, analysis) runs as `python scripts/run.py -- <command>`. The runner (`su2qc_jepa.localrun`):

1. **Classifies.** A command that needs a GPU, or whose estimated laptop time exceeds 20 min, is *always* sent to Perlmutter. The estimate comes from unit costs measured on 2 Oct 2026: 2,000 trajectories in 11.7 s; one epoch over 1,137 trajectories in 2.5 s; one 12-qubit twin circuit in 6–30 s; all on 2 cores. Measured peaks: tests 0.9 GB, training check 1.2 GB, dataset 0.2 GB, twin circuit 0.5 GB.
2. **Admits** light work only if the laptop has room *now*. Available memory minus the request must stay ≥ 16 GB for other programs, the 1-minute load plus the job's threads must leave 2 logical CPUs free, and only one su2qc computation may run at a time across sessions (a lock file). Otherwise it waits up to 20 min, then sends the job to Perlmutter.
3. **Runs capped:** nice 19, idle I/O priority, 2–4 threads for every math library, a memory ceiling (a cgroup limit via `systemd-run --user`, otherwise an address-space limit), a time limit, and `oom_score_adj = 1000`. Under memory pressure the kernel kills this job, never another session.
4. **Heals.** A memory kill is retried once with twice the memory (≤ 16 GB) if there is room; otherwise, and after a timeout, the job is sent to Perlmutter. A program error is not retried; it is a bug. Each attempt is logged to `.local_runs/ledger.jsonl` with the probe, the limits and the outcome.

| Job | Laptop estimate | Where |
|---|---|---|
| tests, J0, physics, code graph, dry runs, IBM submission, analysis, reports | seconds–minutes | laptop |
| dataset, 20,000 trajectories | ≈ 1.5 min | laptop |
| training check (1 seed, ≤ 30 epochs) | ≤ 15 min | laptop |
| main training (5 seeds × 200 epochs, plus masked runs) | ≈ 18 h | Perlmutter (≈ 2–4 h on an A100) |
| ablation ladder (≈ 5 rungs × 5 seeds) | days | Perlmutter |
| twin, pilot size (≤ 40 circuits) | ≤ 12 min | laptop |
| twin, full hardware day (≈ 480 circuits) | ≈ 2.4 h | Perlmutter |

**How work reaches Perlmutter (the pull-based job queue: Claude updates GitHub, Perlmutter runs what it finds).**

- **The job file.** `run.py` (or `scripts/jobs/enqueue.py`) writes the next numbered job request `jobs/NNN_<slug>.yaml` on `main`. It records the exact commit, the steps (each `python scripts/<allowlisted>.py ...`, with a step that rebuilds the dataset from its manifest and seed), the outputs to send back, the wall-clock limit and the GPUs, and it is pushed.
- **The worker.** On Perlmutter, `scrontab` (NERSC's replacement for cron, `-q cron -C cron`) starts a worker tick every 15 minutes. The tick pulls `main`, submits new jobs with Slurm (`shared` queue, one A100 = ¼ node-hour per hour), polls running ones, and pushes `status.json`, a log tail and the declared outputs (≤ 50 MB) to the separate `results` branch.
- **Self-healing on Perlmutter.**
  - TIMEOUT → resubmitted with twice the time (cap 48 h).
  - OUT_OF_MEMORY → twice the GPUs, and so twice the memory (cap 2).
  - NODE_FAIL, PREEMPTED, BOOT_FAIL, LOST (no Slurm record for 3 h) → same resources.
  - At most 3 attempts; program errors are never retried.
  - A corrupted clone is re-cloned, a crashed tick is retried by the next one, and in-flight jobs are recovered from `results` if local state is lost.
  - A heartbeat file lets the laptop see that the worker is alive.
- **Safety.** The worker uses a deploy key limited to this repository, never pushes to `main`, runs only commits on `main` and only allowlisted scripts (never the IBM submission), and stops at 50 node-hours.
- **On the laptop.** `scripts/jobs/status.py` shows states and the heartbeat, and `scripts/jobs/fetch.py NNN` copies outputs in. No SSH, no daily NERSC login, and the IBM token never leaves the laptop: calibrated noise models are committed as files.

Whole-plan Perlmutter estimate: 15–40 node-hours (cap 50). One-time setup: `docs/PERLMUTTER.md`. Tested on 2 Oct 2026:

- **Laptop runner:** a job over its memory limit was retried once with more memory and completed; a job over its time limit was stopped and reported; when the runner itself was killed, its job was killed with it (no orphan).
- **Queue and worker:** with a local stand-in for GitHub and stand-ins for `sbatch`/`sacct`, a job ran at the pushed commit, its results were fetched without a merge, and the allowlist refused the hardware-submission script.
- **Automatic resubmission:** a TIMEOUT was resubmitted with twice the time and then completed, with both attempts in its history.
- **Concurrent pushes** to `results` were serialised.

---

## Appendix A — Grids and configurations

* `configs/gates.yaml` — thresholds (preregistered 16 Oct).
* `configs/hardware_budget.yaml` — approval file (human-edited).
* `src/su2qc_jepa/data/trajectories.py` — families `ONFAM` and `STRONG` with the grids of §6.
* Chain carrier: $K=12$, $\Delta t=0.375$, depths {1,2,4,8}; KC-prep times {10,15,20}$/g_E$ at strong coupling.

## Appendix B — Numbers measured in this session (starter package, 1 Oct 2026)

**B.1 Fingerprints.** See §3. Route A build 2.2 s; Hamiltonian 3 s; route B (160,000-dim) 0.3 s; $j_{\max}=1$ Hamiltonian 63 s.

**B.2 Dynamics from S3 (exact, $N=4$ sector).**

$g_E=1$, $\mu=3/8$: $P_{\text{baryonic}}=0.432/0.732/0.821$ at $t=1/2/3$; $C_{\text{string}}(3)=0.238$ (project's preliminary expectation reproduced).

P-A ($g_E=2$), at the hardware times $t=0.375/0.75/1.5/3.0$: $P_{S3}=0.969/0.884/0.622/0.183$, $P_{\text{meson}}=0.004/0.014/0.034/0.046$, $P_{\text{baryonic}}=0.022/0.082/0.270/0.579$, $C_{\text{string}}=0.744/0.727/0.662/0.448$ ($\mu=3/8$; within 0.03 of these at $\mu=0.3$ and $0.5$).

**B.3 Mass dependence.** On-family ($g_E=2$): breaking fraction at $t=3$ falls monotonically 0.628 → 0.531 for $\mu=0.15\to0.65$; no resonance peak. Strong coupling ($c_H=0.02$): breaking fraction at $t=16.7/33.3/50$: $\mu=0.375$: 0.227/0.555/0.740; $\mu=0.30$: 0.143/0.071/0.056; $\mu=0.45$: 0.141/0.067/0.060; $\mu=0.15$: 0.007/0.016/0.016. Krylov dimension for $10^{-3}$ over the window: on-family 11–14; strong coupling 16–24 (full window $t\le100$), 11 for $t\le21$.

**B.4 Chain carrier.** Circuit = sector unitary to $10^{-15}$ (Lie and Strang, $K$ up to 6 checked against `Statevector`, $K=12$ via transpiled CZ counts); CZ counts match the formula; X/Y sequential sampler total-variation distance to the brute-force distribution 0.007 at $2\times10^5$ shots ($K=6$); KC-prep exact to $10^{-15}$ with $K-1$ rotations.

**B.5 Smoke-scale learning (CPU, 300–600 trajectories, 15–40 epochs).** Old single-family design: ridge 0.02–0.04 MAE at held-out masses, JEPA v0 0.07. Family design (held-out $g_E$ / held-out $\mu$ near resonance), 164 training trajectories: all methods 0.09–0.16 on $P_{\text{baryonic}}$ at $+8$ — the task is now genuinely hard at that scale; the full runs use 60× more data.

**B.6 Twin and residual rehearsal (synthetic noise, $K=8$, 24 points).** Twin repeats with spawned seeds are distinct (5/5); `jepa_twin` AUROC for the degraded arm 1.0 vs `raw_twin` 0.70 with the untuned v0 model; Spearman values at smoke scale are not meaningful.

**B.7 Timings.** Dataset 0.1 s/trajectory; JEPA epoch (384 trajectories, CPU) ~1 s; twin circuit (12 qubits, density matrix, 4,000 shots) 6–30 s on 2 CPU cores; whole smoke pipeline 60 s.

**B.8 External facts checked (1 Oct 2026).** IBM Open Plan: 10 min per 28-day rolling window; March 2026 opt-in of 180 extra minutes over 12 months (15 min/month for users above 20 min in the past year); Heron r2 opened to Open-plan users; Heron r3 `ibm_boston` (100 qubits, 2.15×10⁻³ two-qubit error) and Nighthawk `ibm_miami` (120 qubits) are Premium/Flex. Pay-as-you-go $96/QPU-min; Flex $72/min with a 400-min floor. Amazon Braket: IonQ Forte $0.30/task + $0.08/shot (Aria withdrawn; 2,500-shot minimum with error mitigation); IQM Garnet/Emerald $0.00145–0.0016/shot. Qiskit 2.5.2, Aer 0.17.2, qiskit-ibm-runtime 0.50.0 used here; CUDA-Q 0.15.x current.
