---
id: plans/000
title: Gauge-JEPA-P v1 — JEPA for SU(2) QML, 1–2 months
series: plans
created_utc: '2026-10-01T16:13:12Z'
author: planner
milestone: null
status: superseded
supersedes: null
superseded_by: plans/001
---

# Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code)

> **Superseded by `plans/001`** (Gauge-JEPA-P v2, Krylov-chain carrier). Kept verbatim for provenance; the audit of this plan is `plans/001` §1.

## The idea in one paragraph

Gauge-JEPA-P ("P" for plaquette; the name is Claude's) takes the project's verified SU(2)-with-matter plaquette system (82 gauge-invariant states at $j_{\max}=1/2$, 152 at $j_{\max}=1$; 2×3 ladder 1,727; static-charge models 112 and 2,417) and trains a JEPA world model on it. Each time step or quench is an *action*; each finite-shot measurement is an *observation*. An encoder maps the observation to a 16-dimensional latent, a predictor advances the latent under actions, and the loss asks the predicted latent to match the latent of the clean future observation (never the observation itself). The model is then used as a physics instrument: (1) forecast late-time string-breaking channel yields from early-time, few-shot records at couplings it never saw; (2) use the distance between the latent predicted from the Aer noise twin and the latent of real IBM/IonQ records as a label-free hardware error signal (digital-twin residual); (3) run a preregistered matched-shot test of a gauge-respecting quantum encoder against the classical one. Everything is exactly solvable at this size, so the paper claims a method and a hardware instrument, not quantum advantage.

## What it builds on (from this project)

- Verified Hamiltonian by two routes to $10^{-12}$; sectors 2/20/38/20/2; electric degeneracies 16/16/18/16/16 (v0.5.0 review; physics setup notes).
- Named states S3, S1, MM, BB̄, Loop; channel projectors $P_{\text{pair}}(8)$, $P_{\text{meson}}(2)$, $P_{\text{baryonic}}(26)$, $P_{\text{vacmatter}}(2)$ in the $N=4$ sector of 38.
- Resonance $2m = \tfrac34 g_E \Rightarrow \mu^*=3/8$, $m^* = 3g^2/(16a)$; coupling points P-A ($g^2=4$, $m=0.75$, $g_E=2$) and P-S (Sufian, 1 : 0.02 : 0.02).
- L12 encoding (3 qubits/vertex, 6 physical + 2 leakage codes, S3 codeword 3793): one Z-basis measurement gives every density, Casimir, projector and leakage flag.
- Arm GI (2,156 two-qubit gates per Strang step, 8.6× over budget): twin data only, never hardware. Arm KR (Krylov playback, $K\le 28$, 2–5 qubits, 13–27 CZ in Sufian's regime): the only hardware-runnable circuits.
- Calibrated Aer noise twin with SeedSequence seeding (v0.6.2); the project's deterministic-gate session discipline, now run through Claude Code sessions instead of the Hermes agent; the Nine-Month Plan's Gauge-JEPA architecture (two encoders, SIGReg, grounding heads, cross-prediction, honest advantage test).
- Not carried over: the 1+1D LSH chain as first data source (deferred); any hardware run of GI circuits.

## Model

$$\frac{H}{g_E} = \sum_\ell j_\ell(j_\ell+1) + \mu\sum_n (-1)^{n_x+n_y} N_n + \frac{1}{2g_E}\sum_\ell(\eta_\ell\psi_n^\dagger U_\ell\psi_{n'} + \text{h.c.}) - \frac{1}{4g_E^2}\mathrm{Tr}(U_\square + U_\square^\dagger)$$

- Actions: $dt \in \{0.125, 0.25, 0.5\}/g_E$; 9 masses $\mu\in[0.15,0.65]$; 3 hopping/electric ratios (0.25 = P-A, 0.02 = P-S, 0.5); mass quenches. Trajectories: S3, S1 or random gauge-invariant start, 8–16 actions.
- Observation: $o_t = (\hat N_{v_0..v_3},\ \widehat{j(j+1)}_{\ell},\ \hat P_{\text{pair}},\hat P_{\text{meson}},\hat P_{\text{baryonic}},\hat P_{\text{vacmatter}},\hat P_{S3},\hat P_{S1},\hat P_{B\bar B},\ \hat\ell_{\text{leak}};\ S)$ from $S$ shots. Built identically from exact states, twin L12 records and hardware Krylov records — this is the design choice that lets one encoder serve all three sources and makes the twin residual meaningful.
- Classical encoder: MLP or set transformer → $s_t\in\mathbb R^{16}$. Quantum encoder: gauge-respecting trainable circuit $W_\theta$, latent $s^Q_t = (\langle\psi_t|W_\theta^\dagger O_j W_\theta|\psi_t\rangle)_{j=1..8}$, CUDA-Q statevector only (one optional hardware inference run in week 7).
- Predictor: small transformer over $(s_t, a_t,\dots,a_{t+k-1})$, horizons $k=1..8$.
- Loss: prediction + SIGReg anti-collapse + grounding heads (energy, Casimir, channel weights, leakage) + semigroup consistency $P(2\Delta t)\approx P(\Delta t)\circ P(\Delta t)$ + cross-prediction between encoders. Noisy few-shot context, clean target.

## Testing ladder (budgets are Claude's estimates)

| Layer | Tool | Runs | Budget | Gate |
|---|---|---|---|---|
| 0 Exact | NumPy/SciPy routes A/B | $10^5$ plaquette, $10^4$ ladder trajectories; truth labels | ~20 CPU-h on the laptop | J0 |
| 1 Statevector GPU | CUDA-Q cu13-0.15.1; Qiskit Aer GPU | L12 (12 q), Krylov (2–5 q), ladder 20-q encoding; shots 256–4,096 | ~10 GPU-h, laptop GPU or one Perlmutter node | J0 |
| 2 Noise twin | Aer + backend noise model, fixed seeds | GI $r=1,2,3$ and KR, two arms, five seeds (~3,000 runs) | ~25 A100 GPU-h on Perlmutter | J0, J2 |
| 3 Training | PyTorch; CUDA-Q parameter-shift (PennyLane lightning.gpu adjoint fallback) | main runs, 5 seeds, ablations, baselines, quantum encoder | ~100 + ~40 A100 GPU-h on Perlmutter; request 200 GPU node-hours (4 A100 per node) for shared-queue charging and reruns; laptop for development | J1, J2, J4 |
| 4 Hardware | IBM Quantum (Qiskit Runtime Sampler, Heron-class QPU); IonQ (qiskit-ionq provider or IonQ cloud API, Aria/Forte-class QPU) | KR circuits only, $K\le16$, 3 couplings × 6 times × 2 arms × 3 calibration days; one IonQ day | IBM ~10 min QPU (minimum design) to ~30 min (full); IonQ ~100 tasks × 1,000 shots, ≈ USD 1–3k at list per-shot prices depending on plan (approximate) | J3 |

Gates: J0 data (observables to $10^{-12}$, unbiased shot estimator, distinct twin seeds, split manifest by coupling/time/seed/day). J1 training health (effective rank ≥ 8/16, grounding $R^2\ge0.99$, semigroup residual < $10^{-3}$). J2 forecasting (from $t\le1/g_E$ at 512 shots, $P_{\text{baryonic}}, P_{\text{meson}}, C_{\text{string}}$ at $t=2,3/g_E$ within 0.05 at held-out masses; beats ridge/autoregressive on ≥2 of 3). J3 hardware twin (residual Spearman ≥ 0.7 vs exact error; AUROC ≥ 0.8 on arms/days). J4 quantum encoder (trains at 12 q; preregistered matched-shot test vs classical encoder and vs classical simulation of the circuit, reported either way).

Why only Krylov circuits on hardware: GI costs 2,156 two-qubit gates per step; KR ran on IBM Kingston at 13–27 CZ. Price: no leakage flags on hardware; the twin residual is the replacement gauge-error signal.

Who runs what: Claude Code drives every layer — a `CLAUDE.md` in the SU2ZX repo carries frozen conventions, gate thresholds and evidence-bundle rules; one session per milestone, ending in its gate script and a committed bundle; Perlmutter jobs via `sbatch` from a login-node session (or SSH from the laptop); hardware jobs dry-run first, user approval, then submission with job IDs, calibration snapshots and hashes.

One-month version: layers 0–3, gates J0–J2, twin-only residual, no device time → simulator-and-twin methods note.

## Observables

Primary: $\langle N_n\rangle$ (4), $\langle j(j+1)\rangle$ per link (4), $C_{\text{string}}$; channel projectors and sub-projectors ($P_{S3}, P_{S1}, P_{\text{hopped}}, P_{B\bar B}, P_{\text{antivac}}$); string survival $=P_{\text{pair}}$; intact string $=P_{S3}+P_{S1}$; breaking fraction $=P_{\text{meson}}+P_{\text{baryonic}}$; leakage-flag rate (L12/twin only); energy (extra settings; hardware only at $t=0$ as control). Derived by the model: breaking time $t_b$ (first $t$ with $P_{S3}+P_{S1}<1/2$), ratio $R_{B/M}=P_{B\bar B}/P_{\text{meson}}$ (~11 on one plaquette, preliminary), $\mu^*_{\text{model}}$ from held-out data, and the twin residual
$$r_t = \big\|E_\theta(o^{\text{hw}}_t) - P_\phi(E_\theta(o^{\text{twin}}_0), a_{0:t-1})\big\|_2.$$
Diagnostics: effective rank, isotropy, grounding $R^2$, rollout drift vs horizon, gradient variance vs depth.

## Predicted results

- R1 no collapse: effective rank 10–14/16; grounding $R^2>0.99$ (energy, Casimir), $>0.98$ (channels).
- R2 forecasting at P-A within 0.05; ridge baseline ~0.08–0.12; margin shrinks at $g_E=1$ (broad resonance).
- R3 $\mu^*_{\text{model}}$ within 0.05 of 3/8 at $g_E=2$; estimator-dependent at $g_E=1$ (reported as a finding).
- R4 depth extrapolation on the twin: forecasting $t=3/g_E$ from noisy $r=1$ beats direct noisy $r=3$ (~6,500 two-qubit gates). Simulator result, labelled as such.
- R5 twin residual: Spearman 0.7–0.85 vs exact error on IBM; AUROC 0.8–0.9 for mitigation arms; calibration-day separation may be null.
- R6 quantum encoder trains; advantage test null (12-q shallow gauge-respecting circuit is classically simulable).
- R7 ladder transfer with 10% fine-tune data: densities/Casimirs within 0.05; $R_{B/M}$ is the hard case; compare the model forecast with the exact N5 answer.
- R8 cross-device: residual sign transfers to IonQ, scale needs one-day rescaling.

Not shown: quantum advantage, new SU(2) physics, continuum limit, 2+1D beyond 2×3, hardware gauge-leakage evidence.

## Publishability

Methods-and-benchmark paper with hardware data. Preprint (hep-lat, cross-list quant-ph, cs.LG) end of week 8 (27 Nov 2026 if start is 5 Oct). Venues: Phys. Rev. D (best fit with hardware + error budget), Quantum, Machine Learning: Science and Technology (if the quantum encoder is central), PRX Quantum (stretch; needs residual to beat a mitigation-selection rule), Lattice 2027 proceedings. Decision typically 2–4 months → journal publication ≈ 4–7 months after the project ends. Without J3 it is an ML-venue simulation study. Settle scope with the advisor re Sufian's report (same model, resonance, hardware circuits) before the preprint; cite his Krylov route as the hardware carrier.

## Schedule (5 Oct – 29 Nov 2026)

One researcher driving Claude Code sessions; simulations on the laptop and NERSC Perlmutter; QPU runs on IBM-Q and IonQ.

1. W1 (5–11 Oct): observation builder, trajectory generator, split manifest, samplers → J0 (11 Oct).
2. W2 (12–18 Oct): classical Gauge-JEPA v0, collapse diagnostics, preregistration signed 16 Oct → J1 (18 Oct).
3. W3 (19–25 Oct): held-out-mass forecasting, baselines, twin data generation starts.
4. W4 (26 Oct–1 Nov): depth-extrapolation on twin, ablations, IBM dry run + 2,048-shot pilot → J2 (30 Oct). End of one-month version.
5. W5 (2–8 Nov): IBM calibration days 1–2, first residuals; quantum-encoder training starts.
6. W6 (9–15 Nov): IBM day 3; residual vs exact error, AUROC; advantage test; ladder fine-tuning → J3 (13 Nov), J4 (15 Nov).
7. W7 (16–22 Nov): ladder transfer + N5; IonQ day + rescaling; optional quantum-encoder hardware inference.
8. W8 (23–29 Nov): paper, claim table, error budget, code/data/model release, replication; preprint 27 Nov.

Drop order if weeks 5–6 slip: ladder, IonQ, quantum-encoder hardware run.

## Problems and assumptions

- Exactly solvable → instrument/method claim only. Krylov carrier cannot leak; leakage head trained on twin only. $g_E=1$ resonance broad. Close two physics-setup open points first: P-A coefficients (1:0.5:0.25 vs 1:0.25:0.0625) and the real L12 map (3793). Device drift may be too small for day separation. Quantum encoder can at best tie. Collapse/co-adaptation guarded by SIGReg, grounding, rank gate, moving-average ablation.
- Assumed: start 5 Oct 2026; one researcher driving Claude Code sessions; IBM Quantum access for 10–30 min Heron-class time in November; an IonQ account with credit for ~100 tasks; ~200 NERSC Perlmutter GPU node-hours; the laptop covers development and all 12-qubit exact/statevector work; all cost/time figures are estimates; quantum encoder simulator-only; 1+1D LSH data deferred.
