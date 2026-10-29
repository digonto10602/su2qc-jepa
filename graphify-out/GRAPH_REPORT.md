# Graph Report - su2qc-jepa  (2026-10-28)

## Corpus Check
- 142 files · ~165,649 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 3, .cff 1)

## Summary
- 1358 nodes · 2459 edges · 114 communities (78 shown, 36 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 227 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0067ef89`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- pathlib
- Worker
- Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier
- test_jobs.py
- artifacts.py
- 9. Plot data (the data behind every figure; each table can be parsed as Markdown)
- localrun.py
- test_pipeline.py
- PlaquetteModel
- trajectories.py
- load_line_noise_model
- jepa.py
- Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)
- generate_dataset
- train.py
- j0_data.py
- Preregistration — Gauge-JEPA-P v2 (signed by tag `prereg-2026-10-16`)
- ibm.py
- named_states
- chain.py
- run_j0
- LinkSpace
- test_crosscheck.py
- .__init__
- JEPAConfig
- build_chain_circuit
- Hand-over report: full project state, results, data and how to continue (28 Oct 2026)
- su2.py
- Compute: laptop for light work, Perlmutter for heavy jobs
- FullSpaceOperators
- test_committed_graph_is_fresh
- 6. Results in full
- M3 exploratory: strategies for J1 training success (research and comparison)
- Krylov
- MatterSpace
- ObservationSpec
- Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)
- M2a closed: J1 FAIL after 14 configurations (semigroup row on a fresh seed); working model $w_{\text{sigreg}}=3$, $w_{\text{semigroup}}=10$
- Desktop GPU worker online; `v1_final` trained; preregistered J2 FAIL (on-family passes, strong coupling fails)
- CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`
- prompts/INDEX.md
- 11. What happens next
- 4. Infrastructure and how to operate it
- 7. Plot data (the data to re-make every figure, for example on claude.ai)
- compare_point
- ObservableSet
- Model card — Gauge-JEPA-P v1 (working configuration after M2a)
- M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914)
- J3 gate scores the low-shot rows at the preregistered 512 shots
- Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`)
- Package build: plan audit, Gauge-JEPA-P v2 and the starter package
- Conventions update: numbered artifacts and the Graphify code graph
- Compute update 2: safe laptop and a pull-based job queue for Perlmutter
- Perlmutter worker install keeps the user's other scrontab entries
- train_jepa
- 7.6 J1 data for all 14 configurations and v1_final
- {{title}}
- M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)
- su2qc-jepa — Gauge-JEPA-P v2 starter package
- Compute update: laptop for light work, Perlmutter for heavy jobs
- M0: repository created, CI green, code graph committed
- 4. The world model (JEPA)
- 8. Current results in full
- _Cache
- Compute: a safe laptop and a pull-based job queue for Perlmutter
- J1 energy grounding threshold set relative to the measured information ceiling
- Preregistration deviation: dataset-equivalence tolerance corrected to rounding scale
- Heavy jobs on the desktop GPU (RTX 3070) — setup and daily use
- TwinRunner
- M0 — Bootstrap (first Claude Code invocation, ~45 min)
- M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card
- Results and what they mean
- 5. Data, twin, hardware plan, gates, hypotheses, error budget
- 7. Chronological history (every session so far, with the numbers)
- {{title}}
- {{title}}
- test_scrontab_merge.py
- decisions/INDEX.md
- Twin with Quantinuum noise from Nexus device specifications
- Preregistration deviation: J3 model `v2_final` reads only the physical observables
- layout.py
- M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)
- M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)
- M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version.
- reports/INDEX.md
- 2. Project goal, claims, preregistration
- 10. Decisions log and problems/risks
- Appendix A — helper scripts (verbatim; run with `python scripts/run.py --no-queue --threads 1 -- python <script> <out.md>` from the repository root)
- Appendix D. Helper scripts (verbatim; in `.local_runs/probe/`, git-ignored; run each with `python scripts/run.py --no-queue --threads 1 -- python .local_runs/probe/<name>.py`, then read the runner log)
- Couplings
- 005_hardware-days.md
- graph_update.sh
- test_job_dies_with_the_runner
- PAPER_OUTLINE.md
- PHYSICS.md
- jobs/INDEX.md
- bootstrap_repo.sh
- replicate.sh
- safe_run.sh
- smoke.sh
- install_desktop.sh
- install_perlmutter.sh
- scrontab_merge.sh
- setup_env_desktop.sh
- setup_env_perlmutter.sh
- plan.md
- su2qc-jepa

## God Nodes (most connected - your core abstractions)
1. `PlaquetteModel` - 44 edges
2. `generate_dataset()` - 29 edges
3. `Worker` - 24 edges
4. `run_j0()` - 24 edges
5. `test_training_and_baselines_run_on_device()` - 22 edges
6. `JEPAConfig` - 21 edges
7. `GaugeJEPA` - 20 edges
8. `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier` - 20 edges
9. `ObservableSet` - 19 edges
10. `Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)` - 19 edges

## Surprising Connections (you probably didn't know these)
- `Decision` --references--> `ObservationSpec`  [INFERRED]
  decisions/010_preregistration-deviation-j3-model-v2-final-reads-only-the-p.md → src/su2qc_jepa/data/records.py
- `10.1 Decisions (`decisions/INDEX.md`)` --references--> `retry_resources()`  [INFERRED]
  reports/012_full-project-report-plan-physics-methods-every-result-and-th.md → src/su2qc_jepa/jobs.py
- `10.4 M2a — model health (5 Oct; `reports/010`, `decisions/005`, and results fetched at 21:30 UTC)` --references--> `baseline_autoregressive()`  [INFERRED]
  reports/011_project-overview-gauge-jepa-p-v2-plan-physics-status-and-eve.md → src/su2qc_jepa/models/train.py
- `12. Open problems and risks (as of 5 Oct, 21:40 UTC)` --references--> `baseline_autoregressive()`  [INFERRED]
  reports/011_project-overview-gauge-jepa-p-v2-plan-physics-status-and-eve.md → src/su2qc_jepa/models/train.py
- `14. Next actions` --references--> `baseline_autoregressive()`  [INFERRED]
  reports/011_project-overview-gauge-jepa-p-v2-plan-physics-status-and-eve.md → src/su2qc_jepa/models/train.py

## Import Cycles
- None detected.

## Communities (114 total, 36 thin omitted)

### Community 1 - "Worker"
Cohesion: 0.07
Nodes (25): Alternatives considered, Compute: laptop and Perlmutter only, admission-controlled laptop runner, self-healing jobs, Consequences (what must be re-run or re-checked), Decision, Why, Costs and limits, Heavy jobs: the job queue and the Perlmutter worker, One-time setup (Digonto, about 30 minutes, after the repository exists on GitHub) (+17 more)

### Community 2 - "Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier"
Cohesion: 0.04
Nodes (42): Alternatives considered, Consequences, Decision, Numbered artifacts and the Graphify code graph, Why, Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code), Model, Observables (+34 more)

### Community 3 - "test_jobs.py"
Cohesion: 0.06
Nodes (29): Alternatives considered, Compute: add the desktop RTX 3070 as a second job-queue worker, Consequences (what must be re-run or re-checked), Decision, Why, Actions taken, Code graph, M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED (+21 more)

### Community 4 - "artifacts.py"
Cohesion: 0.10
Nodes (25): Bugs found and fixed while doing this, Results and what they mean, Artifact, check_artifacts(), list_artifacts(), new_artifact(), next_number(), read_front_matter() (+17 more)

### Community 5 - "9. Plot data (the data behind every figure; each table can be parsed as Markdown)"
Cohesion: 0.05
Nodes (40): 9.0 How to use this section, 9.1 Catalogue of plots, 9.2 P11 sub-plots (physics curves and carrier costs), 9. Plot data (the data behind every figure; each table can be parsed as Markdown), Dataset reproducibility (evidence/J0_data/fingerprint_compare_*.json; per-trajectory-sum tolerance 1e-12), Further machine-readable tables (P10, P11e, P11f, J1 records, jobs, dataset reproducibility), J1 gate records (evidence/J1_training/*.json), Job table (jobs/*.yaml and evidence/jobs/NNN/status.json; states read on 2026-10-06 by scripts/jobs/status.py) (+32 more)

### Community 6 - "localrun.py"
Cohesion: 0.09
Nodes (31): Actions taken, Code graph, M1: su2qc cross-check PASS, three datasets built, gate J0 PASS, Next action, Part A — route C agrees with both su2qc routes (`evidence/J0_data/crosscheck_su2qc.json`, commit `0bb5d6d`, status PASS), Part B — datasets (`evidence/J0_data/datasets.json`, commit `358d0bd`), Part C — gate J0 PASS (`evidence/J0_data/20261003T201012Z.json`, 15 s on the laptop), Problems and assumptions (+23 more)

### Community 7 - "test_pipeline.py"
Cohesion: 0.11
Nodes (14): run_j1(), run_j2(), auroc(), run_j3(), spearman(), _fmt(), GateResult, GateRow (+6 more)

### Community 8 - "PlaquetteModel"
Cohesion: 0.10
Nodes (4): GIBasisState, PlaquetteModel, model(), test_jmax1_counts()

### Community 10 - "load_line_noise_model"
Cohesion: 0.07
Nodes (16): Consequences, edge_errors_from_backend(), _decode_complex(), degraded_noise_model(), HeronLike, line_noise_dict(), load_line_noise_model(), load_twin_noise() (+8 more)

### Community 11 - "jepa.py"
Cohesion: 0.11
Nodes (7): Code graph, 3. Comparison table (deliverable B), GaugeJEPA, MarkovPredictor, mix_actions(), sigreg_loss(), vicreg_terms()

### Community 12 - "Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)"
Cohesion: 0.07
Nodes (29): 0. How to read this document, 10.1 Before the repository existed (1–2 Oct, planner sessions; reports 000–005), 10.2 Environment and M0 (2 Oct; reports 006–008), 10.3 M1 — physics cross-check, datasets, gate J0 (3–4 Oct; `reports/009`) — **J0 PASS 9/9**, 10.4 M2a — model health (5 Oct; `reports/010`, `decisions/005`, and results fetched at 21:30 UTC), 10. What has been done, session by session (with every number), 11. Infrastructure and repository conventions (how the work is done), 12. Open problems and risks (as of 5 Oct, 21:40 UTC) (+21 more)

### Community 13 - "generate_dataset"
Cohesion: 0.16
Nodes (17): Code graph, load(), _checksum(), dataset_fingerprint(), DatasetConfig, FamilyConfig, generate_dataset(), load_dataset() (+9 more)

### Community 14 - "train.py"
Cohesion: 0.16
Nodes (13): 7.5 The 5 Oct evening and 6 Oct session (this report adds these), Actions taken, effective_rank(), baseline_autoregressive(), baseline_ridge(), baseline_supervised_mlp(), diagnostics(), fit_probe() (+5 more)

### Community 15 - "j0_data.py"
Cohesion: 0.16
Nodes (9): estimate(), subsample(), _bits_from_key(), estimate_chain(), estimate_diagonal(), Record, sample_exact_chain(), sample_exact_diagonal() (+1 more)

### Community 16 - "Preregistration — Gauge-JEPA-P v2 (signed by tag `prereg-2026-10-16`)"
Cohesion: 0.10
Nodes (19): 0. What was already known when this was written (disclosure), 1. Hypotheses (thresholds are those of `configs/gates.yaml`, frozen below), 2. Frozen inputs, 3. Analysis plan (exact commands; every computation through `scripts/run.py`), 4. Exclusion and handling rules, 5. Known open items (not part of the frozen record), 6. Signatures, 7. Deviations after signing (+11 more)

### Community 17 - "ibm.py"
Cohesion: 0.14
Nodes (12): W4 (26 Oct – 1 Nov) — J2, pilot job; end of the one-month version, BudgetError, calibration_snapshot(), check_budget(), collect(), dry_run(), DryRunSummary, estimate_qpu_seconds() (+4 more)

### Community 18 - "named_states"
Cohesion: 0.12
Nodes (16): 2.1 Model and Hamiltonian, 2.2 Coupling points, 2.3 Verified fingerprints (PROVEN by tests or MEASURED), 2.4 Named states and bare energies, 2.5 Dynamics tables (MEASURED; recomputed in this report by `physics_curves.py`, Appendix A, and equal to the plan's quoted numbers), 2.6 Cross-check against the project's independent verified code (M1; `evidence/J0_data/crosscheck_su2qc.json`, status PASS, tolerance $10^{-10}$, commit `0bb5d6d`), 2. Physics, krylov() (+8 more)

### Community 19 - "chain.py"
Cohesion: 0.16
Nodes (11): _bond_rotation(), build_chain_prep_circuit(), chain_sector_unitary(), _layer(), _phase_weights(), prep_cascade_params(), sample_x_basis(), sample_z_basis() (+3 more)

### Community 20 - "run_j0"
Cohesion: 0.16
Nodes (12): 12. Error budget (lines, each measured), 5.6 Error budget (lines, each to be measured; plan §12), run_j0(), chain_amplitudes(), ChainSpec, trotter_error(), lanczos(), heron_like_noise_model() (+4 more)

### Community 21 - "LinkSpace"
Cohesion: 0.15
Nodes (3): LinkSpace, m_values(), spin_matrices()

### Community 23 - ".__init__"
Cohesion: 0.14
Nodes (8): 1. Code changes (builder; `graphify affected "GaugeJEPA"`, `"ActionPredictor"`, `"run_j1"` first and run the tests it lists), 3. Screening stage (paired design: one master seed for every arm, so seeds are matched), 4. Confirmation stage (fresh master seeds, full protocol), 5. Replication (one more fresh master seed), 6. Session report, Tasks, ActionPredictor, MLP

### Community 24 - "JEPAConfig"
Cohesion: 0.29
Nodes (11): 2. Unit tests (builder; `tests/test_jepa_options.py`, fast, fixed seeds, small `generate_dataset` as in `tests/test_pipeline.py::test_jepa_ema_target_and_curriculum`), JEPAConfig, _batch(), _loss(), test_cli_flags_reach_config_and_skip_baselines(), test_default_config_is_unchanged(), test_markov_predictor_composes_exactly(), test_old_checkpoint_loads() (+3 more)

### Community 25 - "build_chain_circuit"
Cohesion: 0.14
Nodes (7): Claims ledger — every substantive statement, its status and its evidence, build_chain_circuit(), z_layer(), cz_count(), twin_variance_check(), test_chain_circuit_matches_sector_unitary(), test_two_routes_agree_and_gauss_law()

### Community 26 - "Hand-over report: full project state, results, data and how to continue (28 Oct 2026)"
Cohesion: 0.14
Nodes (14): 10. Problems log and open problems, 1. Glossary (every technical word used), 3. Physics and methods (short; depth in `reports/012` §2–§4), 5. Chronology (compact; commit hashes from `git log`), 8. Current in-flight state (28 Oct 2026, 23:22 UTC; `python scripts/jobs/status.py`, `git show origin/results:...`), 9. How to continue (step by step, exact commands), Actions taken (to write this report), Appendix A. Decisions (`decisions/INDEX.md`; one line each) (+6 more)

### Community 27 - "su2.py"
Cohesion: 0.19
Nodes (3): _cg_cached(), clebsch_gordan(), _fact()

### Community 28 - "Compute: laptop for light work, Perlmutter for heavy jobs"
Cohesion: 0.17
Nodes (11): 5. Compute rules (`decisions/004`, `decisions/006`, `configs/compute.yaml`, `docs/PERLMUTTER.md`, `docs/DESKTOP.md`), Alternatives considered, Compute: laptop for light work, Perlmutter for heavy jobs, Consequences, Decision, Why, Actions taken, 6.1 Compute (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`) (+3 more)

### Community 30 - "test_committed_graph_is_fresh"
Cohesion: 0.18
Nodes (8): Actions taken, Code graph, Laptop environments: coding repaired, su2qc-jepa created, Next action, Problems and assumptions, What was asked, Actions taken, test_committed_graph_is_fresh()

### Community 31 - "6. Results in full"
Cohesion: 0.17
Nodes (12): 6.10 Device parameter tables, 6.11 Overall reading (what the results mean today), 6.1 J0, the data and physics gate: PASS, 9 of 9 rows (`evidence/J0_data/20261003T201012Z.json`), 6.2 Energy ceiling (J1 input; `evidence/J1_training/ceiling_main.json`, `data/main` `73fff8e5a7b7`, validation split 26,348 rows), 6.3 J1, the training-health gate: FAIL after 14 configurations plus a fresh-seed confirmation, 6.4 Dataset reproducibility (laptop vs workers), 6.5 J2, the preregistered forecasting gate: FAIL (`evidence/J2_forecast/20261021T201507Z.json`, model `v1_final`), 6.6 Noiseless twin `ideal0`: all known-answer checks PASS (job 023; `evidence/twin/ideal0/null_check.json`, `63a42ff`) (+4 more)

### Community 32 - "M3 exploratory: strategies for J1 training success (research and comparison)"
Cohesion: 0.17
Nodes (11): 1. Diagnosis: what the 15 training runs say (all numbers from `reports/016` §6.3 and §7.6, `runs/<run>/seed*/history.json`), 2. Survey of strategies (what each does, with the source), 4. The shortlist (deliverable C, detailed in `prompts/011`), Actions taken, Appendix B. Sources opened, Code graph, M3 exploratory: strategies for J1 training success (research and comparison), Next action (+3 more)

### Community 33 - "Krylov"
Cohesion: 0.26
Nodes (3): evolve(), Krylov, krylov_error()

### Community 35 - "ObservationSpec"
Cohesion: 0.20
Nodes (6): Context, Definition of done, M3 exploratory: J1 training improvement experiments, Out of scope / stop conditions, ObservationSpec, test_observation_spec_roundtrip()

### Community 36 - "Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)"
Cohesion: 0.18
Nodes (11): 0.1 How to read this document, 0.2 Glossary (every technical term used), 0. Reading guide and glossary, 12. Code graph, problems and assumptions of this report, next action, 1. Project goal, scope, allowed and forbidden claims, 3. The Krylov-chain (KC) hardware carrier *(label)*, Actions taken (for this report), Appendix B — file map (where things are) (+3 more)

### Community 37 - "M2a closed: J1 FAIL after 14 configurations (semigroup row on a fresh seed); working model $w_{\text{sigreg}}=3$, $w_{\text{semigroup}}=10$"
Cohesion: 0.18
Nodes (10): Cost, Dataset reproducibility (`evidence/J0_data/fingerprint_compare_*.json`), Forecasting, preliminary (`runs/v1_confirm/forecast_eval.json`; not a J2 result), J1 (validation split, final epoch; every row is in `evidence/GATE_LEDGER.md`), M2a closed: J1 FAIL after 14 configurations (semigroup row on a fresh seed); working model $w_{\text{sigreg}}=3$, $w_{\text{semigroup}}=10$, Next action, Problems and assumptions, Results and what they mean (+2 more)

### Community 38 - "Desktop GPU worker online; `v1_final` trained; preregistered J2 FAIL (on-family passes, strong coupling fails)"
Cohesion: 0.18
Nodes (10): Actions taken, Cost, Dataset used by `v1_final` (`evidence/J0_data/fingerprint_compare_main_laptop_vs_desktop_v1_final.json`), Desktop GPU worker online; `v1_final` trained; preregistered J2 FAIL (on-family passes, strong coupling fails), J1 on `v1_final`, information only (`evidence/J1_training/20261021T203007Z.json`), J2: preregistered forecasting gate, **FAIL** (`evidence/J2_forecast/20261021T201507Z.json`), Next action, Problems and assumptions (+2 more)

### Community 39 - "CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`"
Cohesion: 0.20
Nodes (9): 1. Priorities, in order, 2. Session protocol (every session, no exceptions), 3. Frozen things (changing any of these needs a new `decisions/` record and a new version tag), 4. Hardware rules (non-negotiable), 6. Writing rules (reports, prompts, docs, paper), 7. What the package already guarantees (do not re-derive, do re-run), 8. Where things are, CLAUDE.md — rules for every Claude Code session in `su2qc-jepa` (+1 more)

### Community 40 - "prompts/INDEX.md"
Cohesion: 0.20
Nodes (5): Expected, M6 — Hardware day 3, gate J3, error budget (W6, 2 sessions), M7 — One stretch item (W7), chosen on 15 Nov by Digonto, M8 — Paper assembly, release, replication (W8, 2 sessions), Prompts — index

### Community 41 - "11. What happens next"
Cohesion: 0.20
Nodes (10): 11.1 The rest of M2 (M2a continuation, `prompts/010`), 11.2 M2b — preregistration (16 Oct; `prompts/002` items 6–8), 11.3 M3 (W3, 19–25 Oct; `prompts/003`): forecasting, calibrated twin, dry run, 11.4 M4 (W4, 26 Oct – 1 Nov; `prompts/004`): J2 and the pilot (end of the one-month version), 11.5 M5 (W5, 2–8 Nov; `prompts/005`): hardware days 1 and 2, 11.6 M6 (W6, 9–15 Nov; `prompts/006`): day 3, J3, error budget, 11.7 M7 (W7, 16–22 Nov; `prompts/007`): one stretch item, chosen 15 Nov by Digonto, 11.8 M8 (W8, 23–29 Nov; `prompts/008`): paper, release, replication (+2 more)

### Community 42 - "4. Infrastructure and how to operate it"
Cohesion: 0.20
Nodes (10): 4.1 Rules of the house (read `CLAUDE.md` and `~/.claude/CLAUDE.md` first), 4.2 Three machines, 4.3 The runner (`scripts/run.py`, `decisions/004`, `configs/compute.yaml`), 4.4 The job queue, 4.5 Repository layout (details in Appendix B), 4.6 Code graph (Graphify), 4.7 CI and environment pins, 4.8 Credentials and hardware rules (`CLAUDE.md` §4) (+2 more)

### Community 43 - "7. Plot data (the data to re-make every figure, for example on claude.ai)"
Cohesion: 0.20
Nodes (10): 7.0 How to use this section, 7.1 T1 Spearman(score, exact_error) and AUROC(score separates arm B from arm A), per twin, shot level and score, 7.2 T2 mean flag rate and mean exact error by arm and depth (4000 shots), 7.3 T3 noiseless null check by shot level (evidence/twin/ideal0/null_check.json), 7.4 T4 cross-carrier summary (v1_final seed0; evidence/twin/cross_carrier/cross_carrier.json; median / p90 / median over noise_diag), 7.5 J2 MAE (evidence/runs/v1_final/forecast_eval.json = input of evidence/J2_forecast/20261021T201507Z.json; mean of 5 seeds; n_test {'onfam': 2935, 'strong': 3134} ; context_step 4 ; master_seed 27182818 ), 7.7 T5 Quantinuum device parameters (evidence/hardware/quantinuum_devices_20261028T220635Z.json), 7. Plot data (the data to re-make every figure, for example on claude.ai) (+2 more)

### Community 44 - "compare_point"
Cohesion: 0.22
Nodes (6): compare_point(), extract_terms(), import_su2qc(), main(), sign_gauge(), su2qc_label_to_c()

### Community 46 - "Model card — Gauge-JEPA-P v1 (working configuration after M2a)"
Cohesion: 0.22
Nodes (8): 1. What the model is, 2. Working configuration, 3. Training cost, 4. J1 results (validation split, final epoch; `evidence/GATE_LEDGER.md`, `figures/000`, `figures/001`), 5. Forecasting, preliminary (`runs/v1_confirm/forecast_eval.json`, mean of 5 seeds; NOT a J2 result, since J2 is run in M4a), 6. Data and reproducibility, 7. Known limitations, Model card — Gauge-JEPA-P v1 (working configuration after M2a)

### Community 47 - "M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914)"
Cohesion: 0.22
Nodes (8): Laptop check, 10 epochs, 1 seed (`runs/v1_check/seed0/history.json`, local; validation split), M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914), Next action, Options for Digonto (a decision record in `decisions/` is needed for any of B–D, before the 16 Oct preregistration), Problems and assumptions, Results and what they mean, The energy row cannot pass with this encoder (`evidence/J1_training/ceiling_main.json`, validation split, 26,348 rows; training split 126,824 rows; `data/main` `73fff8e5a7b7`), What was asked

### Community 48 - "J3 gate scores the low-shot rows at the preregistered 512 shots"
Cohesion: 0.25
Nodes (6): Alternatives considered, Consequences, Decision, J3 gate scores the low-shot rows at the preregistered 512 shots, Why, test_j3_uses_the_preregistered_low_shot_level()

### Community 49 - "Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`)"
Cohesion: 0.25
Nodes (8): Absolute safety rules (you have no permission prompts), Context, Definition of done, Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`), Phase A — inventory and backup (no changes), Phase B — repair `coding` (only after rule 4 allows it), Phase C — create `su2qc-jepa` (safe to do at any time; it touches no existing environment), Phase D — report

### Community 50 - "Package build: plan audit, Gauge-JEPA-P v2 and the starter package"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Package build: plan audit, Gauge-JEPA-P v2 and the starter package, Problems and assumptions, Results and what they mean, What was asked

### Community 51 - "Conventions update: numbered artifacts and the Graphify code graph"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Conventions update: numbered artifacts and the Graphify code graph, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 52 - "Compute update 2: safe laptop and a pull-based job queue for Perlmutter"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Compute update 2: safe laptop and a pull-based job queue for Perlmutter, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 53 - "Perlmutter worker install keeps the user's other scrontab entries"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Perlmutter worker install keeps the user's other scrontab entries, Problems and assumptions, Results and what they mean, What was asked

### Community 54 - "train_jepa"
Cohesion: 0.50
Nodes (7): Actions taken, 5. Preregistration and reporting consequences (constraint 2), prepare_tensors(), train_jepa(), TrainConfig, test_jepa_ema_target_and_curriculum(), test_jepa_trains_one_epoch()

### Community 55 - "7.6 J1 data for all 14 configurations and v1_final"
Cohesion: 0.25
Nodes (8): 7.6 J1 data for all 14 configurations and v1_final, args.json of v1_final and v1_confirm, P8x final epoch (200), per seed, all configurations (runs/<run>/seed0..4/history.json, unmasked), P8y per-configuration summary of the final epoch (what the J1 gate compares: min over seeds, max for semigroup), P-curve: effective rank (seed mean; band min..max in P1 of reports/012 for configs 1-6) at selected epochs (all configurations), P-curve: grounding R2 of energy (seed mean) at selected epochs, P-curve: semigroup residual (seed mean; log axis) at selected epochs (all configurations), P-curve: training loss terms (unweighted, seed mean) at epoch 200, all configurations

### Community 57 - "{{title}}"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Problems and assumptions, Results and what they mean, {{title}}, What was asked

### Community 58 - "M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)"
Cohesion: 0.29
Nodes (6): Expected, M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h), Part A — cross-check against the project's verified `su2qc` code, Part B — datasets, Part C — gate, Tests to add

### Community 59 - "su2qc-jepa — Gauge-JEPA-P v2 starter package"
Cohesion: 0.29
Nodes (6): First two sessions on the laptop, Five-minute tour, Install on the laptop (done by prompts/009), Layout, su2qc-jepa — Gauge-JEPA-P v2 starter package, What is verified today (`python scripts/run.py -- python -m pytest -q`: 47 fast tests; `-m slow` adds 1 more)

### Community 60 - "Compute update: laptop for light work, Perlmutter for heavy jobs"
Cohesion: 0.29
Nodes (6): Code graph, Compute update: laptop for light work, Perlmutter for heavy jobs, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 61 - "M0: repository created, CI green, code graph committed"
Cohesion: 0.29
Nodes (6): Code graph, M0: repository created, CI green, code graph committed, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 62 - "4. The world model (JEPA)"
Cohesion: 0.29
Nodes (7): 4.1 Observation, actions, training rule, 4.2 Architecture (`src/su2qc_jepa/models/jepa.py`), 4.3 Losses, 4.4 Baselines, tasks, 4. The world model (JEPA), Appendix A. Probe script (`.local_runs/probe/planner_probe.py`, git-ignored; run with `python scripts/run.py --no-queue --threads 1 -- python .local_runs/probe/planner_probe.py`), eff_rank()

### Community 63 - "8. Current results in full"
Cohesion: 0.29
Nodes (7): 8.1 J0 (data gate): PASS, 9 of 9 rows (`evidence/J0_data/20261003T201012Z.json`, `evidence/GATE_LEDGER.md`), 8.2 Energy ceiling (J1 input; `evidence/J1_training/ceiling_main.json`, commit `63065dd`, 2026-10-05T17:31Z; `data/main` `73fff8e5a7b7`; training split 126,824 rows, validation split 26,348 rows; regressor seeds 462709266, 3658436304), 8.3 J1 (training gate) for the six gated rungs (official gate runs; `evidence/GATE_LEDGER.md` rows; records in `evidence/J1_training/`), 8.4 Dataset reproducibility (laptop versus Perlmutter; `evidence/J0_data/fingerprint_compare_*.json`, commit `3010090`, 2026-10-05T23:47Z), 8.5 GPU-fix verification and the job table, 8.6 Forecast results so far, 8. Current results in full

### Community 65 - "Compute: a safe laptop and a pull-based job queue for Perlmutter"
Cohesion: 0.33
Nodes (5): Alternatives considered, Compute: a safe laptop and a pull-based job queue for Perlmutter, Consequences, Decision, Why

### Community 66 - "J1 energy grounding threshold set relative to the measured information ceiling"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences (what must be re-run or re-checked), Decision, J1 energy grounding threshold set relative to the measured information ceiling, Why

### Community 67 - "Preregistration deviation: dataset-equivalence tolerance corrected to rounding scale"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences, Decision, Preregistration deviation: dataset-equivalence tolerance corrected to rounding scale, Why

### Community 68 - "Heavy jobs on the desktop GPU (RTX 3070) — setup and daily use"
Cohesion: 0.33
Nodes (5): Daily use, From the laptop, Heavy jobs on the desktop GPU (RTX 3070) — setup and daily use, One-time setup (on the desktop, Linux, about 20 minutes), Troubleshooting (on the desktop)

### Community 70 - "M0 — Bootstrap (first Claude Code invocation, ~45 min)"
Cohesion: 0.33
Nodes (5): Context, Definition of done, M0 — Bootstrap (first Claude Code invocation, ~45 min), Out of scope, Tasks

### Community 71 - "M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card"
Cohesion: 0.33
Nodes (5): Context, Definition of done, M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card, Out of scope / stop conditions, Tasks

### Community 72 - "Results and what they mean"
Cohesion: 0.33
Nodes (6): `coding`: imports before and after (`import-before.json` → `import-after.json`), Disk, `pip check`, Results and what they mean, `su2qc-jepa` environment, The GTX 1060 (compute capability 6.1, driver 580.178.04, CUDA 13.0 driver API)

### Community 73 - "5. Data, twin, hardware plan, gates, hypotheses, error budget"
Cohesion: 0.33
Nodes (6): 5.1 Data (`evidence/J0_data/datasets.json`, commit `358d0bd`; checksums are sha256 of the data arrays, first 12 hex digits shown), 5.2 The digital twin, 5.3 Hardware plan and rules (nothing submitted), 5.4 Gates (current thresholds, `configs/gates.yaml`), 5.5 Preregistered hypotheses H1–H5 (plan §11, `docs/PREREGISTRATION.md` draft), 5. Data, twin, hardware plan, gates, hypotheses, error budget

### Community 74 - "7. Chronological history (every session so far, with the numbers)"
Cohesion: 0.33
Nodes (6): 7.1 Before the repository existed (1–2 Oct; planner sessions; reports 000–005), 7.2 Environment and M0 (2 Oct; reports 006–008), 7.3 M1 — physics cross-check, datasets, gate J0 (3–4 Oct; `reports/009`) — J0 PASS (9 of 9 rows), 7.4 M2a — model health (5 Oct; `reports/010`, `decisions/005`), 7.6 Parameter count, 7. Chronological history (every session so far, with the numbers)

### Community 75 - "{{title}}"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences (what must be re-run or re-checked), Decision, {{title}}, Why

### Community 76 - "{{title}}"
Cohesion: 0.33
Nodes (5): Context, Definition of done, Out of scope / stop conditions, Tasks, {{title}}

### Community 77 - "test_scrontab_merge.py"
Cohesion: 0.60
Nodes (4): _env(), _run(), test_add_to_empty_table_and_remove_last_entry(), test_add_update_remove_keeps_other_entries()

### Community 79 - "Twin with Quantinuum noise from Nexus device specifications"
Cohesion: 0.40
Nodes (4): Alternatives considered, Decision, Twin with Quantinuum noise from Nexus device specifications, Why

### Community 80 - "Preregistration deviation: J3 model `v2_final` reads only the physical observables"
Cohesion: 0.40
Nodes (5): Alternatives considered, Consequences, Decision, Preregistration deviation: J3 model `v2_final` reads only the physical observables, Why

### Community 82 - "M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)"
Cohesion: 0.40
Nodes (4): Expected, M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions), Session M2a — make the model healthy, Session M2b — preregistration (16 Oct)

### Community 83 - "M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)"
Cohesion: 0.40
Nodes (4): Expected, M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions), Session M3a — forecasting, Session M3b — twin and dry run

### Community 84 - "M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version."
Cohesion: 0.40
Nodes (4): Expected, M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version., Session M4a — J2 (30 Oct), Session M4b — pilot (one job)

### Community 86 - "2. Project goal, claims, preregistration"
Cohesion: 0.40
Nodes (5): 2.1 Goal (plain English), 2.2 Claims allowed and forbidden (`reports/012` §1, `CLAUDE.md` §6, `docs/CLAIMS.md`), 2.3 Hypotheses (`docs/PREREGISTRATION.md` §1; thresholds in `configs/gates.yaml`), 2.4 Preregistration and its deviations, 2. Project goal, claims, preregistration

### Community 87 - "10. Decisions log and problems/risks"
Cohesion: 0.50
Nodes (4): 10.1 Decisions (`decisions/INDEX.md`), 10.2 Problems and risks, 10.3 Disagreements between sources that I noticed, 10. Decisions log and problems/risks

### Community 88 - "Appendix A — helper scripts (verbatim; run with `python scripts/run.py --no-queue --threads 1 -- python <script> <out.md>` from the repository root)"
Cohesion: 0.50
Nodes (4): A.1 plot_tables.py (plots P1 to P9, P12), A.2 physics_curves.py (plot P11a to P11d), A.3 evidence_tables.py (P10, P11e, P11f, job and reproducibility tables), Appendix A — helper scripts (verbatim; run with `python scripts/run.py --no-queue --threads 1 -- python <script> <out.md>` from the repository root)

### Community 89 - "Appendix D. Helper scripts (verbatim; in `.local_runs/probe/`, git-ignored; run each with `python scripts/run.py --no-queue --threads 1 -- python .local_runs/probe/<name>.py`, then read the runner log)"
Cohesion: 0.50
Nodes (4): Appendix D. Helper scripts (verbatim; in `.local_runs/probe/`, git-ignored; run each with `python scripts/run.py --no-queue --threads 1 -- python .local_runs/probe/<name>.py`, then read the runner log), D.j1_tables.py, D.j2_dev_tables.py, D.twin_tables.py

## Knowledge Gaps
- **401 isolated node(s):** `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script`, `PYTHONHASHSEED`, `replicate.sh script` (+396 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 705 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **36 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PlaquetteModel` connect `PlaquetteModel` to `_Cache`, `trajectories.py`, `4. Infrastructure and how to operate it`, `compare_point`, `generate_dataset`, `ObservableSet`, `j0_data.py`, `named_states`, `Conventions update: numbered artifacts and the Graphify code graph`, `run_j0`, `LinkSpace`, `Compute: laptop for light work, Perlmutter for heavy jobs`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Why does `Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)` connect `Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)` to `9. Plot data (the data behind every figure; each table can be parsed as Markdown)`, `11. What happens next`, `5. Data, twin, hardware plan, gates, hypotheses, error budget`, `7. Chronological history (every session so far, with the numbers)`, `named_states`, `reports/INDEX.md`, `10. Decisions log and problems/risks`, `Appendix A — helper scripts (verbatim; run with `python scripts/run.py --no-queue --threads 1 -- python <script> <out.md>` from the repository root)`, `Compute: laptop for light work, Perlmutter for heavy jobs`, `4. The world model (JEPA)`, `8. Current results in full`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Why does `ObservationSpec` connect `ObservationSpec` to `trajectories.py`, `generate_dataset`, `j0_data.py`, `Preregistration deviation: J3 model `v2_final` reads only the physical observables`, `train_jepa`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `PlaquetteModel` (e.g. with `Code graph` and `6.2 Repository and conventions`) actually correct?**
  _`PlaquetteModel` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `generate_dataset()` (e.g. with `2. Unit tests (builder; `tests/test_jepa_options.py`, fast, fixed seeds, small `generate_dataset` as in `tests/test_pipeline.py::test_jepa_ema_target_and_curriculum`)` and `Code graph`) actually correct?**
  _`generate_dataset()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script` to the rest of the system?**
  _401 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `pathlib` be split into smaller, more focused modules?**
  _Cohesion score 0.04756468797564688 - nodes in this community are weakly interconnected._