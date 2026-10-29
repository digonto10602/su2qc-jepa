---
id: reports/017
title: 'M3 exploratory: strategies for J1 training success (research and comparison)'
series: reports
created_utc: '2026-10-29T00:12:47Z'
author: planner
milestone: M3
status: done
supersedes: null
superseded_by: null
---

# M3 exploratory: strategies for J1 training success (research and comparison)

**Milestone:** M3 · **Prompt:** none of its own (planner research requested by Digonto in the coordinator session of 28/29 Oct 2026); the experiment prompt it feeds is `prompts/011` · **Commit:** `9ede5c9` (`main`, clean) · **Related:** `reports/016` (hand-over; §6.3 and §7.6 hold every J1 number used here), `reports/013` (M2a close), `reports/012` §9 (J1 epoch curves), `decisions/005` (energy threshold), `decisions/010` (`v2_final`, physics-only encoder), `docs/PREREGISTRATION.md` §7.

**Status words:** PASS / FAIL / PARTIAL / NOT RUN / VOID only. **Everything proposed here is EXPLORATORY and post-hoc.** The preregistered J1 and J2 verdicts (both FAIL) stand whatever these experiments show (constraint 2 of the request). No threshold in `configs/gates.yaml` and no way of measuring a row is changed or proposed to change (constraint 1).

## What was asked
Digonto: "make a plan of all the strategies that could be applied for making the training successful, compare those methods, then apply a few best options for this project and see if that changes anything." This report is the research and comparison; `prompts/011` is the executable experiment plan (3–5 options, screening then fresh-seed confirmation, about 5.5 desktop hours, cap 8 h). Nothing was trained, queued, committed or changed in `src/` for this report.

"Training successful" means the J1 gate rows of `configs/gates.yaml` on all 5 seeds at the **final epoch** (the gate reads `history.json[-1]`, `src/su2qc_jepa/gates/j1_training.py`): effective rank $\ge 8$ of 16; grounding $R^2$: energy $\ge 0.887$, $C_{\text{string}}\ge 0.99$, $P_{\text{meson}}\ge0.95$, $P_{\text{baryonic}}\ge0.98$; semigroup residual $<10^{-3}$; no NaN. Secondary target: the J2 forecast error must not get worse (strong-coupling $P_{\text{baryonic}}$ MAE is 0.105 / 0.123 at +4 / +8 against the 0.05 bound, `evidence/J2_forecast/20261021T201507Z.json`).

## Actions taken
1. Read the two instruction files, `STATE.json`, `reports/016` (§2, §6, §7.6, §8–§10), `reports/013`, `decisions/005`, `decisions/010`, `docs/PREREGISTRATION.md`, `configs/gates.yaml`, `jobs/019`, `jobs/033`, `configs/compute.yaml`.
2. Code graph first (`graphify query "J1 training gate effective rank semigroup residual"`, `graphify explain GaugeJEPA`, `graphify explain TrainConfig`, `graphify explain run_gate.py`), then the raw files the graph pointed at: `src/su2qc_jepa/models/jepa.py`, `src/su2qc_jepa/models/train.py`, `scripts/train_jepa.py`, `src/su2qc_jepa/gates/j1_training.py`, `src/su2qc_jepa/gates/ledger.py`, `scripts/run_gate.py`, `scripts/prereg_hashes.py`, `tests/test_pipeline.py` (test names and two tests).
3. Literature (sources in §4; every method below is cited to a paper I opened): LeJEPA/SIGReg, VICReg, Barlow-Twins-style decorrelation, BYOL/I-JEPA EMA targets, dimensional collapse (Jing et al.), RankMe (the effective-rank metric the gate uses), SWA and EMA-of-weights, uncertainty weighting, GradNorm, multi-horizon latent consistency and Koopman-style latent dynamics (Lusch et al.; Koopman Dreamer; TD-MPC).
4. One read-only probe on the laptop through the runner (`python scripts/run.py --no-queue --threads 1 -- python .local_runs/probe/planner_probe.py`, exit 0, 10 s, peak 0.6 GB; log `.local_runs/logs/20261029T000708Z-3c15ba_planner_probe_a1.log`; script in Appendix A). It measured (a) the effective rank of the clean observations themselves, (b) the epoch-to-epoch noise of the J1 numbers in the last 20 epochs of `v1_final`, (c) the Monte-Carlo noise of the SIGReg estimate with 64 vs 1024 projections.
5. Checked the job queue read-only (`python scripts/jobs/status.py`): `jobs/033` (`v2_final`) RUNNING on the desktop since 2026-10-28 23:30 UTC; `jobs/032` finished (0.124 h); Perlmutter worker still stopped.
6. Wrote this report and `prompts/011` with `scripts/new_artifact.py`; `scripts/check_artifacts.py` OK.

## Results and what they mean

### 1. Diagnosis: what the 15 training runs say (all numbers from `reports/016` §6.3 and §7.6, `runs/<run>/seed*/history.json`)

**1.1 Which rows fail.** Over 14 configurations plus `v1_final`, energy, $C_{\text{string}}$ and $P_{\text{baryonic}}$ $R^2$ pass in every run; $P_{\text{meson}}$ fails only with the EMA target. The two rows that decide J1 are the effective rank (min over seeds) and the semigroup residual (max over seeds), and they pull against each other:

| lever | rank (min over seeds) | semigroup (max over seeds) | source |
|---|---|---|---|
| $w_{\text{sigreg}}$ 0.5 → 2 → 5 (with $w_{\text{sg}}=0.1$) | 5.16 → 8.26 → 10.53 | 3.3e-3 → 5.3e-3 → 8.5e-3 | rungs 1–3 |
| $w_{\text{sg}}$ 1 → 3 → 5 → 10 (with $w_{\text{sigreg}}=2$) | 8.56 → 8.07 → 7.80 → 7.42 | 5.6e-3 → 1.2e-3 → 1.0e-3 → 9.2e-4 | rungs 9–12 |
| $w_{\text{sigreg}}=3,w_{\text{sg}}=10$, three master seeds | 8.26 / 8.45 / **7.97** | 7.8e-4 / **1.48e-3** / 8.6e-4 | rungs 13, 14, F |

The working point $(3,10)$ sits on the knife edge: the three master seeds give one pass, one semigroup fail and one rank fail. Pearson $r=0.90$ between rank and $\log_{10}$ residual across rungs 1–6 (`reports/013`) is a correlation across runs that also differ in weights, not a mechanism. **A plan that only moves the two weights again has been tried eight times and should not be repeated.**

**1.2 The semigroup residual is a held-out-coupling problem, not an optimisation problem (new reading).** The training semigroup term is an absolute mean-squared error; the gate's residual is the same quantity on the *validation* split divided by the mean squared latent, $\text{resid}=\langle(P_{2}-P_{1}\circ P_{1})^2\rangle/\langle P_2^2\rangle$ (`models/train.py: diagnostics`). For `v1_final` seed 0 at epoch 200 the training term is $6.3\times10^{-5}$ while the validation residual is $3.9\times10^{-4}$ (`evidence/runs/v1_final/seed0/history.json`). The latent's per-dimension standard deviations are 0.34–1.46 (probe), so $\langle P_2^2\rangle\approx1$ and the validation mean-squared inconsistency is about **6 times** the training one. The validation split holds out couplings ($g_E=1.45$, $\mu=0.45$), never rows. Together with the earlier finding that the residual drops to about $2\times10^{-4}$ when the couplings are masked (`reports/016` §6.3 item 3), the picture is: the predictor composes consistently for the couplings it was trained on and less consistently for couplings in between. Strategies that regularise *how the predictor uses the action inputs*, or that make composition exact by construction, address this; strategies that only push harder on the training-set semigroup term (higher $w_{\text{sg}}$) do not, and the ladder shows they cost rank.

**1.3 A rank of 8 is compression, not over-stretching (probe).** The clean 18 observables on the validation split (26,348 rows) have RankMe effective rank **11.2** after column standardisation (9.13 raw); 14 principal components carry 99.9 % of the variance and 4 singular values are exactly zero (the observables obey 4 exact linear identities, e.g. channel probabilities summing to one). So an encoder that keeps the information of its input has room for rank 11–14 before any nonlinear "unfolding"; the trained latents (rank 8.0–8.9) are *below* the data's own rank, and two latent dimensions are nearly dead (std 0.34 and 0.42). Raising the rank to a safe margin above 8 is therefore a reasonable aim, and the per-dimension anisotropy is the specific thing to fix.

**1.4 Final-epoch noise is small; seed-to-seed spread is what decides (probe).** Over the last 20 epochs of `v1_final` the rank moves by sd 0.02–0.03 per seed and the residual by 5–10 % (seed 4: rank 8.005 ± 0.027, final 7.967). Across seeds the spread is 7.97–8.90 in rank and $3.9\times10^{-4}$ to $8.6\times10^{-4}$ in residual (5x in `v1_confirm`). So weight averaging over the tail (SWA) can only recover of order 0.03 in rank and 10 % in residual; it does not address the seed spread. The cosine schedule already brings the learning rate to zero, so the final point is settled.

**1.5 The SIGReg sketch is noisy at 64 projections (probe).** On a fixed batch of 1,200 `v1_final` latents, 20 draws of the random directions give a relative standard deviation of the SIGReg loss of **10.0 % at 64 projections, 4.8 % at 256, 2.2 % at 1024**; the loss value itself (0.018) is 40x the floor of an exactly Gaussian batch (0.00044), so the regulariser is far from saturated and is balanced against the prediction loss. LeJEPA's own ablation (arXiv:2511.08544, Table 1a and §6.1) recommends $\ge512$ slices and notes that more slices "slightly improve performance". Our implementation uses 64 (`JEPAConfig.sigreg_projections`), a 17-point grid on $[-3,3]$ (LeJEPA: 17 points, $[-5,5]$, with the domain having "negligible impact"), and fresh directions every step (as LeJEPA recommends, Figure 7).

### 2. Survey of strategies (what each does, with the source)

Jargon, once: **collapse** = all latents identical (complete) or confined to a few directions (dimensional); **effective rank** = $\exp$ of the Shannon entropy of the normalised singular values of the centred latent matrix (RankMe, arXiv:2210.02885 eq. 1–2; identical to `models/jepa.py: effective_rank`); **stop-gradient / EMA target** = the prediction target comes from a slowly updated copy of the encoder that receives no gradient; **predictor** = the network that maps a latent and actions to a future latent; **semigroup property** = predicting two steps at once equals predicting one step twice, $P(s,[a_1,a_2])=P(P(s,a_1),a_2)$.

| # | strategy | mechanism | source |
|---|---|---|---|
| S1 | SIGReg weight (LeJEPA) | push 1-D projections of the latent batch to $\mathcal N(0,1)$ via the Epps–Pulley characteristic-function statistic; rules out collapse without stop-gradient; single trade-off $\lambda$ | Balestriero & LeCun, arXiv:2511.08544 §4–5, Alg. 1 |
| S2 | SIGReg sketch size (projections 64 → 1024), fresh directions per step | reduces the variance of the regulariser's gradient; $O(N\cdot M\cdot K)$ cost | same, §4.3, §6.1 Table 1a, Fig. 7 |
| S3 | VICReg variance + covariance terms | per-dimension hinge $v(Z)=\frac1d\sum_j\max(0,\gamma-\sqrt{\mathrm{Var}(z_j)+\epsilon})$ keeps every dimension alive; $c(Z)=\frac1d\sum_{i\ne j}C_{ij}^2$ decorrelates them; directly raises the singular-value entropy | Bardes, Ponce, LeCun, arXiv:2105.04906 eq. 1, 4, 6 ($\lambda=\mu=25,\nu=1,\gamma=1,\epsilon=10^{-4}$ in their setting) |
| S4 | Whitening / Barlow Twins-style cross-correlation to identity | same goal as S3 by a different normalisation (full whitening of the batch) | Zbontar et al., arXiv:2103.03230; Ermolov et al., arXiv:2007.06346 (abstracts) |
| S5 | EMA target encoder with stop-gradient | stable targets, prevents collapse; the standard BYOL / I-JEPA recipe | Grill et al., arXiv:2006.07733 (update $\xi\leftarrow\tau\xi+(1-\tau)\theta$); Assran et al., arXiv:2301.08243 |
| S6 | Latent dimension | more dimensions = more room but also more directions to be consistent in | tried here: latent 32 lowered rank to 6.1 (rung 4) |
| S7 | Predictor capacity / regularisation (hidden size, weight decay or dropout on the action pathway) | a smoother action-conditioning generalises better to held-out couplings (§1.2) | general; LeJEPA removes the predictor entirely in the image setting (§6.1) |
| S8 | **Markov (iterated one-step) predictor** | define $P(s,[a_1..a_k])$ as $k$ applications of one latent transition $s\leftarrow f(s,a)$; composition is then exact by construction and the semigroup residual is zero up to float rounding; the question "is the latent a sufficient state?" moves to the multi-step prediction error | deterministic latent-dynamics cores of Dreamer-style and TD-MPC world models (Hafner et al., arXiv:1912.01603; Hansen et al., arXiv:2203.04955 §3, latent-consistency loss); Koopman-style linear latent dynamics (Lusch, Kutz, Brunton, Nat. Commun. 9, 4950 (2018), DOI 10.1038/s41467-018-07210-0; Koopman Dreamer, arXiv:2607.19719) |
| S9 | **Semigroup consistency on sampled actions** (my label) | the semigroup identity needs no target, so it can be enforced on actions the data never contain: convex mixtures $\alpha a_i+(1-\alpha)a_j$ of training actions (couplings between training values); a consistency regulariser on virtual inputs, aimed at the held-out-coupling gap of §1.2 | consistency-regularisation idea as in Hansen et al. arXiv:2203.04955 §3 and the multi-horizon consistency "knob" studied in arXiv:2607.21645; the mixing rule is mine |
| S10 | Multi-horizon consistency pairs (1+1, 2+2, 4+4) | more composition constraints | arXiv:2607.21645 (helps passive video, "does not" on action-conditioned control tasks); covered by S8 |
| S11 | Horizon curriculum | easy horizons first | tried here (rung 7): no effect on rank or residual |
| S12 | Learning-rate warm-up, longer training | avoids early instabilities; more epochs | LeJEPA uses linear warm-up + cosine (Experiment Details 1); here curves plateau by epoch 150 (rank +0.02 from 150 to 200) |
| S13 | Weight averaging (SWA / EMA of weights) | average the last part of the trajectory: flatter minimum, less noise; BatchNorm statistics must be recomputed | Izmailov et al., arXiv:1803.05407 §3.2 (running average $w_{\text{SWA}}\leftarrow(w_{\text{SWA}}n+w)/(n+1)$); Morales-Brotons et al., arXiv:2411.18704 |
| S14 | Loss balancing: uncertainty weighting | learn $\sum_i\frac{1}{2\sigma_i^2}L_i+\log\sigma_i$ | Kendall, Gal, Cipolla, arXiv:1705.07115 eq. 7 |
| S15 | Loss balancing: GradNorm | equalise gradient norms with restoring force $\alpha$ | Chen et al., arXiv:1711.02257 eq. 1–2 |
| S16 | Gradient clipping, weight decay, batch size | optimisation hygiene | already: clip 1.0, AdamW wd $10^{-5}$, batch 64 |
| S17 | Data augmentation (fresh shot noise per epoch) | more diverse noisy contexts | the 18 observables cannot be re-sampled exactly from themselves (they are marginals of the 82-state distribution) and the dataset is frozen; only Gaussian approximations are possible |
| S18 | Checkpoint selection by validation | pick the best epoch | **not allowed**: the gate reads the final epoch of `history.json`; writing a chosen epoch as "final" would falsify the record |
| S19 | Seed ensembling / averaging | average predictions over seeds | **not allowed by the gate definition**: J1 is min/max over 5 independently trained seeds; latents of different seeds live in different bases |
| S20 | Coupling-conditioned predictor (FiLM) for strong coupling | multiplicative conditioning on $(c_M,c_H,c_B)$ | Perez et al., arXiv:1709.07871; aimed at J2, not J1 |

What the project already tried (14 configurations, `reports/016` §6.3): S1 at 0.5, 2, 3, 5; S5 ($\tau=0.996$: rank 13.1 but residual $2.2\times10^{-2}$ and $P_{\text{meson}}$ 0.915 FAIL); S6 (latent 32: rank 6.1); $w_{\text{ground}}=3$ (no effect); S11 (no effect); $w_{\text{sg}}$ at 0.1, 1, 3, 5, 10. **Do not retry:** S5, S6, S11, $w_{\text{ground}}$, and any pure $(w_{\text{sigreg}},w_{\text{sg}})$ re-tuning.

### 3. Comparison table (deliverable B)

Cost basis: the desktop trains one seed for 200 epochs in 404 s (`jobs/019` log, "epoch 200 ... (404s)"), so a screening arm of 3 seeds x 100 epochs is about 10 min of training plus about 5 min dataset rebuild $\approx$ 0.25 h; a full confirmation (5 seeds x 200 epochs, masked twins, baselines) is 1.16 h (`jobs/019`, `elapsed_hours`). "Prereg" = preregistration implication if the result were adopted as the J3 model: every strategy below changes the frozen model configuration, so each needs a `decisions/` record (deviation D4), Digonto's approval, and must happen before any hardware data exist; J1 and J2 verdicts are unchanged in every case.

| strategy | mechanism (one line) | J1 row(s) it should help | evidence from this project | expected effect | desktop h | risk (incl. J2) | prereg | code size |
|---|---|---|---|---|---|---|---|---|
| **S8 Markov predictor** | iterate one latent transition; composition exact | semigroup (to float rounding) | §1.2: the inconsistency sits in the GRU's hidden memory on held-out couplings; a Markov map has no such memory | residual $\sim10^{-12}$ on every seed; rank unchanged or slightly up (predictor no longer rewards low rank for consistency) | 0.25 screen + 1.2 confirm | makes the row structural (must be disclosed; the test moves to multi-step prediction loss and J2); J2 at +8 may worsen if the GRU memory was useful | D4 record | ~40 lines (`MarkovPredictor`, `JEPAConfig.predictor`, CLI flag) |
| **S9 semigroup on mixed actions** | consistency on convex mixtures of training actions | semigroup (held-out couplings) | §1.2: 6x train→validation gap; masked-coupling residual $2\times10^{-4}$ | residual on held-out couplings down by a factor 2–5 (my estimate from the gap; to be measured) | 0.25 + 1.2 | mixtures leave the physical one-parameter family (harmless for a consistency constraint, but spends capacity); small compute overhead | D4 | ~15 lines in `GaugeJEPA.loss` + flag |
| **S3 VICReg var+cov** | per-dim std hinge + decorrelation | rank | §1.3: two latent dims at std 0.34/0.42; rank 8.0–8.9 vs data rank 11.2 | rank +0.5 to +2 at equal SIGReg weight (to be measured) | 0.25 + 1.2 | every rank increase so far raised the residual; needs S8 or S9 alongside; $P_{\text{meson}}$ $R^2$ fell when rank was forced by EMA | D4 | ~20 lines + 2 flags |
| **S2 SIGReg 1024 projections** | 4.5x less sketch noise (measured) | rank (less noisy regulariser); possibly residual via less noisy gradients | §1.5; LeJEPA recommends $\ge512$ | small: rank +0.1 to +0.3, tighter seed spread | 0.25 | +5 % run time; may do nothing | D4 | CLI flag only (field exists) |
| S7 predictor regularisation (wd $10^{-2}$ on action pathway / hidden 64) | smoother action conditioning | semigroup | §1.2 | unknown sign | 0.25 | may raise prediction loss | D4 | ~10 lines |
| S13 SWA over last 25 % epochs | average tail weights | rank, residual (noise only) | §1.4: tail noise sd 0.03 / 10 % | $\le+0.03$ rank, $\le10$ % residual | 0.3 | BatchNorm stats recomputation; negligible gain | D4 | ~25 lines |
| S12 warm-up / 400 epochs | optimisation hygiene | — | curves flat after 150 | $\le+0.05$ rank | 0.25 / 2.3 | none / cost | D4 | 5 lines / none |
| S14/S15 adaptive loss weights | learned balance | both | the hand grid already spans the trade-off | unpredictable; the tiny semigroup term ($6\times10^{-5}$) would be up-weighted enormously under uncertainty weighting | 0.5 | instability; final state depends on trajectory; frozen weights lose meaning | D4 | ~40 lines |
| S4 whitening | full decorrelation | rank | — | similar to S3 | 0.25 | same as S3; matrix inverse sqrt on 16x16 is cheap | D4 | ~20 lines |
| S5 EMA target | — | rank | **tried: residual 2e-2, $P_{\text{meson}}$ FAIL** | — | — | — | — | do not retry |
| S6 latent 32 / 12 | — | rank | **tried (32): rank 6.1**; 12 would change the meaning of "8 of 16" | — | — | — | would also need a gate re-interpretation: not allowed | — |
| S11 curriculum | — | — | **tried: no effect** | — | — | — | — | do not retry |
| S17 fresh-noise augmentation | — | — | observables not re-sampleable; dataset frozen | — | — | — | — | ruled out |
| S18 checkpoint selection, S19 seed averaging | — | — | — | — | — | not permitted by the gate definition | — | ruled out |
| S20 FiLM coupling conditioning | — | none (J2 only) | strong-coupling MAE 0.105 | unknown | 0.25 | out of the J1 scope; measure J2 in every arm instead | D4 | ~20 lines |

### 4. The shortlist (deliverable C, detailed in `prompts/011`)
1. **S8 Markov predictor** (`--predictor markov`). Removes the semigroup failure mode at the root; the price is that the row becomes structural, so the plan requires the multi-step prediction loss and the J2 MAE to be reported next to it, and the GRU results stay side by side.
2. **S9 semigroup consistency on mixed actions** (`--semigroup-mix 1`). Keeps the GRU and the row's meaning; targets exactly the held-out-coupling gap of §1.2.
3. **S3 VICReg variance–covariance terms added to SIGReg** (`--w-var 1 --w-cov 0.1`). Targets the two dead latent dimensions and the anisotropy that the rank row measures. Weight arithmetic (from the probe's per-dimension std): $v\approx\frac1{16}\sum_j\max(0,1-\sigma_j)\approx0.13$, $c\approx\frac1{16}\sum_{i\ne j}C_{ij}^2\approx1.3$ for typical correlations 0.3; weights 1 and 0.1 make each term of the same order as the weighted SIGReg term ($3\times0.018=0.054$) and the prediction term (0.014), so they act without dominating.
4. **S2 SIGReg with 1024 projections** (`--sigreg-projections 1024`). Zero model change, measured 4.5x lower sketch noise, LeJEPA's own recommendation.
5. **Combination** of the best semigroup fix (1 or 2) with the best rank fix (3 or 4), because §1.1 shows the rows trade off and no single lever has passed on fresh seeds.

The plan is paired screening (all arms on one master seed, 3 seeds x 100 epochs, physics-only encoder as in `v2_final`), then confirmation of up to two arms on a fresh master seed (5 seeds x 200 epochs, masked twins, baselines), then one replication on another fresh master seed. Decision rules are written in `prompts/011` before any result exists.

### 5. Preregistration and reporting consequences (constraint 2)
- Every arm is EXPLORATORY; its J1 run uses `run_gate.py J1 --evidence-dir evidence/exploratory/...` (a new flag, default unchanged) so that no exploratory block lands in `evidence/GATE_LEDGER.md`.
- If a confirmed and replicated configuration is to replace `v2_final` as the J3 model, that is deviation D4: a `decisions/` record, Digonto's explicit approval, before any hardware data. J1 and J2 verdicts remain FAIL; the new model's J1 and J2 numbers are "for information".
- Side effect to know: `scripts/prereg_hashes.py` hashes the canonical JSON of `JEPAConfig`/`TrainConfig` stored in a checkpoint. Adding fields (even with defaults) changes the hash of *new* checkpoints of an otherwise unchanged configuration; the frozen hash `cd4faece…` remains verifiable from the committed `evidence/runs/v1_final/seed0/model.pt`. This already happened once with `encoder_inputs` (`decisions/010`). The paper's disclosure list (`reports/016` §2.4) gains one line.
- Nothing here touches `ObservationSpec`, `conventions.py`, dataset checksums or `configs/gates.yaml` (constraint 6).

## Code graph
| | before | after |
|---|---|---|
| nodes / edges / communities | 1,243 / 2,279 / 101 (`evidence/graph/stats.json`, built at `72a15b4`) | unchanged (no code changed) |
| new or changed hubs | – | – |
| `graphify affected` checks run | none needed (no code change); the builder must run `graphify affected "GaugeJEPA"`, `"ActionPredictor"`, `"run_j1"` before editing (listed in `prompts/011`) | |

## Problems and assumptions
1. The "6x train→validation semigroup gap" assumes $\langle P_2^2\rangle\approx1$ (per-dimension latent std 0.34–1.46 measured on clean validation latents, so the mean square is close to 1). The training value is averaged over the epoch while the model moves, but at epoch 200 the cosine schedule has brought the learning rate to zero, so this is a small effect (three last epochs: $6.5, 6.3, 6.3\times10^{-5}$).
2. The mechanism statements in §1.2 (held-out-coupling inconsistency) and §1.3 are my readings of the numbers, not proven; the screening arms are designed to test them (S9 tests §1.2 directly; S3 tests §1.3).
3. The 100-epoch screening protocol assumes the final 100-epoch point ranks arms the same way as 200 epochs. Support: `v1_final` mean rank 8.46 at epoch 100 vs 8.55 at 200; residual $6.6\times10^{-4}$ vs $6.0\times10^{-4}$ (`reports/016` §7.6 curves). The prompt includes a screening-protocol baseline so comparisons are like for like.
4. Cost estimates come from one desktop job (`jobs/019`); the per-arm 0.25 h includes a dataset rebuild of about 5 min, which I did not measure separately.
5. `v2_final` (`jobs/033`) was still RUNNING when this was written; its numbers are the reference for the confirmation stage and must be fetched first (`reports/016` §9 step 2).
6. The Markov predictor makes the semigroup row pass by construction. I consider that legitimate (it is what "compose like time evolution" asks for) but it changes what the row can tell us; Digonto should decide whether such a pass is reportable as "information" alongside the GRU results, before the arm is queued.
7. Literature access: the arXiv abstract pages do not contain equations; I used the PDF text of LeJEPA and the ar5iv full texts of VICReg, SWA, uncertainty weighting, GradNorm, RankMe and Jing et al.; for Barlow Twins, W-MSE, BYOL, I-JEPA, Dreamer, TD-MPC and the two 2026 preprints I relied on abstracts and the sections quoted above.

## Next action
Digonto decides on item 6 above; then the coordinator runs `prompts/011` starting with its task 1 (the builder's code changes and unit tests), and queues job S0 (screening baseline) first.

## Appendix A. Probe script (`.local_runs/probe/planner_probe.py`, git-ignored; run with `python scripts/run.py --no-queue --threads 1 -- python .local_runs/probe/planner_probe.py`)
Computes, on `data/main` validation split: `effective_rank` of the standardised clean 18 observables and their PCA spectrum; a `tanh` random 16-d lift of them; the last-20-epoch mean/sd/min/max of `eff_rank` and `semigroup_resid` for `evidence/runs/v1_final/seed0..4/history.json`; the per-dimension std of `v1_final/seed0` clean validation latents; and the mean/sd over 20 random-direction draws of `sigreg_loss` on 1,200 of those latents at 64/256/1024 projections, plus the same on an exactly Gaussian batch. Output (verbatim, from the runner log):

```
validation rows 26348 n_obs 18
eff_rank(clean 18 obs, standardised): 11.2
eff_rank(clean 18 obs, raw): 9.13
PCA explained-variance fractions: [0.3755, 0.1951, 0.1085, 0.0617, 0.056, 0.0528, 0.0483, 0.0445, 0.0291, 0.0089, 0.007, 0.0058, 0.0038, 0.0031, 0.0, 0.0, 0.0, 0.0]
components for 99% / 99.9% / 99.99% variance: 12 14 14
eff_rank(tanh random 16-d lift of clean obs): 10.997
seed0: rank 8.639 sd 0.017 [8.605,8.674] final 8.671 ; semigroup 3.88e-04 sd 1.64e-05 [3.57e-04,4.35e-04] final 3.92e-04
seed1: rank 8.606 sd 0.030 [8.540,8.648] final 8.646 ; semigroup 6.62e-04 sd 4.83e-05 [5.63e-04,7.81e-04] final 6.41e-04
seed2: rank 8.876 sd 0.018 [8.851,8.920] final 8.896 ; semigroup 7.01e-04 sd 8.02e-05 [5.35e-04,8.58e-04] final 6.79e-04
seed3: rank 8.569 sd 0.019 [8.535,8.611] final 8.555 ; semigroup 4.29e-04 sd 1.52e-05 [4.05e-04,4.57e-04] final 4.27e-04
seed4: rank 8.005 sd 0.027 [7.954,8.057] final 7.967 ; semigroup 8.98e-04 sd 4.91e-05 [8.11e-04,9.65e-04] final 8.62e-04
latent per-dim std (v1_final seed0, clean val): [1.295, 1.137, 0.623, 0.917, 1.034, 1.113, 1.214, 0.345, 1.159, 1.024, 0.420, 0.841, 0.891, 0.806, 1.463, 1.250]
eff_rank latent: 8.671
sigreg n_proj=64: mean 0.01826 sd 0.00183 rel sd 0.100
sigreg n_proj=256: mean 0.01811 sd 0.00087 rel sd 0.048
sigreg n_proj=1024: mean 0.01806 sd 0.00039 rel sd 0.022
gaussian floor n_proj=64: mean 0.00044 sd 0.00004
gaussian floor n_proj=1024: mean 0.00043 sd 0.00001
```

## Appendix B. Sources opened
- Balestriero, LeCun, *LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics*, arXiv:2511.08544 (PDF text: §4.2 Epps–Pulley, Alg. 1, Thm. 6, §5.1, §6.1 Table 1a–c, Fig. 7, Experiment Details 1).
- Bardes, Ponce, LeCun, *VICReg*, arXiv:2105.04906 (eq. 1, 4, 5, 6; hyperparameters §4).
- Garrido et al., *RankMe*, arXiv:2210.02885 (eq. 1–2; 25,600 embeddings recommended; rank–performance relation).
- Jing et al., *Understanding Dimensional Collapse in Contrastive SSL*, arXiv:2110.09348 (§3–6).
- Izmailov et al., *Averaging Weights Leads to Wider Optima*, arXiv:1803.05407 (§3.1–3.2, 3.4).
- Morales-Brotons et al., *Exponential Moving Average of Weights in Deep Learning*, arXiv:2411.18704 (abstract).
- Kendall, Gal, Cipolla, arXiv:1705.07115 (eq. 2, 7; log-variance reparametrisation).
- Chen et al., *GradNorm*, arXiv:1711.02257 (eq. 1–2, Alg. 1).
- Grill et al., *BYOL*, arXiv:2006.07733; Assran et al., *I-JEPA*, arXiv:2301.08243 (abstracts and method summaries).
- Zbontar et al., *Barlow Twins*, arXiv:2103.03230; Ermolov et al., *W-MSE*, arXiv:2007.06346 (abstracts).
- Hafner et al., *Dreamer*, arXiv:1912.01603; Hansen, Wang, Su, *TD-MPC*, arXiv:2203.04955 (latent-consistency loss, §3); Li et al., *Koopman Dreamer*, arXiv:2607.19719; *Multi-Horizon Consistency as Geometry*, arXiv:2607.21645 (abstract-level).
- Lusch, Kutz, Brunton, *Deep learning for universal linear embeddings of nonlinear dynamics*, Nat. Commun. 9, 4950 (2018), DOI 10.1038/s41467-018-07210-0.
- Perez et al., *FiLM*, arXiv:1709.07871 (abstract).
