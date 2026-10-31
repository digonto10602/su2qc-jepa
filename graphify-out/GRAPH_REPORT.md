# Graph Report - su2qc-jepa  (2026-10-31)

## Corpus Check
- 143 files · ~200,843 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 3, .cff 1)

## Summary
- 1456 nodes · 2565 edges · 127 communities (90 shown, 37 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 235 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ea83ce00`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- noise.py
- test_jobs.py
- Worker
- localrun.py
- 9. Plot data (the data behind every figure; each table can be parsed as Markdown)
- test_physics.py
- PlaquetteModel
- ledger.py
- generate_dataset
- 7. Plot data (the data to re-make every figure, for example on claude.ai)
- j0_data.py
- Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)
- retry_resources
- artifacts.py
- chain.py
- 10. Week by week — what Claude Code does, what is tested, what we expect
- dataset_fingerprint
- Preregistration — Gauge-JEPA-P v2 (signed by tag `prereg-2026-10-16`)
- jepa.py
- train.py
- argparse
- JEPAConfig
- Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier
- LinkSpace
- GaugeJEPA
- 6. Results in full
- records.py
- test_committed_graph_is_fresh
- Hand-over report: full project state, results, data and how to continue (28 Oct 2026)
- su2.py
- FullSpaceOperators
- test_localrun.py
- Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)
- 6. Results in full
- M3 exploratory: strategies for J1 training success (research and comparison)
- Final hand-over report: complete project state, results, data and how to continue on the desktop (31 Oct 2026)
- crosscheck_su2qc.py
- Krylov
- MatterSpace
- ObservationSpec
- M2a closed: J1 FAIL after 14 configurations (semigroup row on a fresh seed); working model $w_{\text{sigreg}}=3$, $w_{\text{semigroup}}=10$
- train_jepa.py
- CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`
- graph.py
- decisions/INDEX.md
- Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code)
- prompts/INDEX.md
- 11. What happens next
- 4. Infrastructure and how to operate it
- 7. Plot data (the data to re-make every figure, for example on claude.ai)
- 4. Infrastructure and how to operate it
- 9. How to continue (prioritised, exact commands)
- pick_device
- Model card — Gauge-JEPA-P v1 (working configuration after M2a)
- test_crosscheck.py
- M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914)
- Numbered artifacts and the Graphify code graph
- J3 gate scores the low-shot rows at the preregistered 512 shots
- scripts/run.py
- Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`)
- Package build: plan audit, Gauge-JEPA-P v2 and the starter package
- Conventions update: numbered artifacts and the Graphify code graph
- Compute update 2: safe laptop and a pull-based job queue for Perlmutter
- Perlmutter worker install keeps the user's other scrontab entries
- 7.6 J1 data for all 14 configurations and v1_final
- residual_eval.py
- {{title}}
- M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)
- su2qc-jepa — Gauge-JEPA-P v2 starter package
- Compute update: laptop for light work, Perlmutter for heavy jobs
- M0: repository created, CI green, code graph committed
- 4. The world model (JEPA)
- 5. Data, twin, hardware plan, gates, hypotheses, error budget
- 8. Current results in full
- .seeds
- Compute: a safe laptop and a pull-based job queue for Perlmutter
- J1 energy grounding threshold set relative to the measured information ceiling
- Preregistration deviation: dataset-equivalence tolerance corrected to rounding scale
- Preregistration deviation: J3 model `v2_final` reads only the physical observables
- Heavy jobs on the desktop GPU (RTX 3070) — setup and daily use
- M0 — Bootstrap (first Claude Code invocation, ~45 min)
- M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card
- Tasks
- Results and what they mean
- 2. Physics
- 2. Project goal, claims, preregistration
- Appendix D. Helper scripts (verbatim; in `.local_runs/probe/`, git-ignored; run each with `python scripts/run.py --no-queue --threads 1 -- python .local_runs/probe/<name>.py`, then read the runner log)
- {{title}}
- {{title}}
- M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)
- M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)
- M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version.
- reports/INDEX.md
- 2. Project goal, claims, preregistration
- 4A. Moving development to the desktop (new; read before doing anything on the desktop)
- plans/INDEX.md
- Appendix A — helper scripts (verbatim; run with `python scripts/run.py --no-queue --threads 1 -- python <script> <out.md>` from the repository root)
- Appendix D. Helper scripts (verbatim; in `.local_runs/probe/`, git-ignored; run each with `python scripts/run.py --no-queue --threads 1 -- python .local_runs/probe/<name>.py`, then read the runner log)
- Couplings
- 005_hardware-days.md
- graph_update.sh
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
1. `PlaquetteModel` - 45 edges
2. `generate_dataset()` - 29 edges
3. `Worker` - 24 edges
4. `run_j0()` - 24 edges
5. `JEPAConfig` - 23 edges
6. `test_training_and_baselines_run_on_device()` - 22 edges
7. `GaugeJEPA` - 20 edges
8. `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier` - 20 edges
9. `Final hand-over report: complete project state, results, data and how to continue on the desktop (31 Oct 2026)` - 20 edges
10. `ObservableSet` - 19 edges

## Surprising Connections (you probably didn't know these)
- `6.1 Compute (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`)` --references--> `pick_device()`  [INFERRED]
  reports/012_full-project-report-plan-physics-methods-every-result-and-th.md → src/su2qc_jepa/compute.py
- `Decision` --references--> `ObservationSpec`  [INFERRED]
  decisions/010_preregistration-deviation-j3-model-v2-final-reads-only-the-p.md → src/su2qc_jepa/data/records.py
- `6.13 The exploratory J1 programme (EXPLORATORY / post-hoc; `prompts/011`, `reports/017`; jobs 034–040; commits `98255dd` (code), `77bb9a0` (screening results), `8c05689` (confirmation and S3b))` --references--> `JEPAConfig`  [INFERRED]
  reports/018_final-hand-over-report-complete-project-state-results-data-a.md → src/su2qc_jepa/models/jepa.py
- `Appendix B. File map` --references--> `JEPAConfig`  [INFERRED]
  reports/018_final-hand-over-report-complete-project-state-results-data-a.md → src/su2qc_jepa/models/jepa.py
- `10.4 M2a — model health (5 Oct; `reports/010`, `decisions/005`, and results fetched at 21:30 UTC)` --references--> `baseline_autoregressive()`  [INFERRED]
  reports/011_project-overview-gauge-jepa-p-v2-plan-physics-status-and-eve.md → src/su2qc_jepa/models/train.py

## Import Cycles
- None detected.

## Communities (127 total, 37 thin omitted)

### Community 0 - "noise.py"
Cohesion: 0.06
Nodes (20): Consequences, calibration_snapshot(), best_line(), e(), edge_errors_from_backend(), heavy_hex_edges(), _decode_complex(), degraded_noise_model() (+12 more)

### Community 1 - "test_jobs.py"
Cohesion: 0.06
Nodes (28): Alternatives considered, Compute: add the desktop RTX 3070 as a second job-queue worker, Consequences (what must be re-run or re-checked), Decision, Why, Actions taken, Code graph, M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED (+20 more)

### Community 2 - "Worker"
Cohesion: 0.12
Nodes (17): Actions taken, Code graph, Cost, Dataset used by `v1_final` (`evidence/J0_data/fingerprint_compare_main_laptop_vs_desktop_v1_final.json`), Desktop GPU worker online; `v1_final` trained; preregistered J2 FAIL (on-family passes, strong coupling fails), J1 on `v1_final`, information only (`evidence/J1_training/20261021T203007Z.json`), J2: preregistered forecasting gate, **FAIL** (`evidence/J2_forecast/20261021T201507Z.json`), Next action (+9 more)

### Community 3 - "localrun.py"
Cohesion: 0.09
Nodes (32): Actions taken, Code graph, M1: su2qc cross-check PASS, three datasets built, gate J0 PASS, Next action, Part A — route C agrees with both su2qc routes (`evidence/J0_data/crosscheck_su2qc.json`, commit `0bb5d6d`, status PASS), Part B — datasets (`evidence/J0_data/datasets.json`, commit `358d0bd`), Part C — gate J0 PASS (`evidence/J0_data/20261003T201012Z.json`, 15 s on the laptop), Problems and assumptions (+24 more)

### Community 4 - "9. Plot data (the data behind every figure; each table can be parsed as Markdown)"
Cohesion: 0.05
Nodes (37): 9.0 How to use this section, 9.1 Catalogue of plots, 9.2 P11 sub-plots (physics curves and carrier costs), 9. Plot data (the data behind every figure; each table can be parsed as Markdown), Dataset reproducibility (evidence/J0_data/fingerprint_compare_*.json; per-trajectory-sum tolerance 1e-12), Further machine-readable tables (P10, P11e, P11f, J1 records, jobs, dataset reproducibility), J1 gate records (evidence/J1_training/*.json), Job table (jobs/*.yaml and evidence/jobs/NNN/status.json; states read on 2026-10-06 by scripts/jobs/status.py) (+29 more)

### Community 5 - "test_physics.py"
Cohesion: 0.08
Nodes (15): Claims ledger — every substantive statement, its status and its evidence, 2.5 Dynamics tables (MEASURED; recomputed in this report by `physics_curves.py`, Appendix A, and equal to the plan's quoted numbers), cz_count(), sector_restrict(), channel_masks(), named_states(), ObservableSet, test_chain_circuit_matches_sector_unitary() (+7 more)

### Community 6 - "PlaquetteModel"
Cohesion: 0.10
Nodes (4): GIBasisState, PlaquetteModel, model(), test_jmax1_counts()

### Community 7 - "ledger.py"
Cohesion: 0.11
Nodes (14): run_j1(), run_j2(), auroc(), run_j3(), spearman(), _fmt(), GateResult, GateRow (+6 more)

### Community 8 - "generate_dataset"
Cohesion: 0.18
Nodes (18): Actions taken, DatasetConfig, FamilyConfig, generate_dataset(), load_dataset(), train_jepa(), TrainConfig, dataset_dir() (+10 more)

### Community 9 - "7. Plot data (the data to re-make every figure, for example on claude.ai)"
Cohesion: 0.06
Nodes (31): 7.0 How to use this section, 7.1 T1 Spearman(score, exact_error) and AUROC(arm B vs arm A), five twins (the four device twins plus the noiseless control), model v1_final seed0 (evidence/twin/<twin>/residual_eval.json), 7.1c T1c compact: Spearman jepa_twin vs raw_twin and AUROC, per twin and shot level (v1_final), 7.2 T2 mean flag rate and mean exact error by arm and depth (4000 shots), 7.3 T3 noiseless null check by shot level (evidence/twin/ideal0/null_check.json), 7.4 T4 cross-carrier summary, v1_final vs v2_final (median / p90 / median over noise_diag median), 7.5 J2 MAE (evidence/runs/v1_final/forecast_eval.json = input of evidence/J2_forecast/20261021T201507Z.json; mean of 5 seeds; n_test {'onfam': 2935, 'strong': 3134} ; context_step 4 ; master_seed 27182818 ), 7.6 J1 data for all 14 configurations and v1_final (+23 more)

### Community 10 - "j0_data.py"
Cohesion: 0.14
Nodes (13): Results and what they mean, run_j0(), build_chain_circuit(), z_layer(), ChainSpec, lanczos(), heron_like_noise_model(), chain_point_records() (+5 more)

### Community 11 - "Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)"
Cohesion: 0.07
Nodes (29): 0. How to read this document, 10.1 Before the repository existed (1–2 Oct, planner sessions; reports 000–005), 10.2 Environment and M0 (2 Oct; reports 006–008), 10.3 M1 — physics cross-check, datasets, gate J0 (3–4 Oct; `reports/009`) — **J0 PASS 9/9**, 10.4 M2a — model health (5 Oct; `reports/010`, `decisions/005`, and results fetched at 21:30 UTC), 10. What has been done, session by session (with every number), 11. Infrastructure and repository conventions (how the work is done), 12. Open problems and risks (as of 5 Oct, 21:40 UTC) (+21 more)

### Community 12 - "retry_resources"
Cohesion: 0.08
Nodes (25): Alternatives considered, Compute: laptop and Perlmutter only, admission-controlled laptop runner, self-healing jobs, Consequences (what must be re-run or re-checked), Decision, Why, Costs and limits, Heavy jobs: the job queue and the Perlmutter worker, One-time setup (Digonto, about 30 minutes, after the repository exists on GitHub) (+17 more)

### Community 13 - "artifacts.py"
Cohesion: 0.16
Nodes (17): Artifact, check_artifacts(), list_artifacts(), new_artifact(), next_number(), read_front_matter(), render_index(), _resolve() (+9 more)

### Community 15 - "chain.py"
Cohesion: 0.14
Nodes (12): _bond_rotation(), build_chain_prep_circuit(), chain_amplitudes(), chain_sector_unitary(), _layer(), _phase_weights(), prep_cascade_params(), sample_x_basis() (+4 more)

### Community 17 - "10. Week by week — what Claude Code does, what is tested, what we expect"
Cohesion: 0.10
Nodes (17): 10. Week by week — what Claude Code does, what is tested, what we expect, W1 (5–11 Oct) — bootstrap, physics cross-check, data → J0, W2 (12–18 Oct) — JEPA v1, collapse diagnostics, preregistration → J1, W3 (19–25 Oct) — forecasting, twin rehearsal, hardware dry runs, W4 (26 Oct – 1 Nov) — J2, pilot job; end of the one-month version, W5 (2–8 Nov) — hardware days 1 and 2, W6 (9–15 Nov) — day 3, J3, advantage-free analysis, W7 (16–22 Nov) — one stretch item, chosen on 15 Nov (+9 more)

### Community 18 - "dataset_fingerprint"
Cohesion: 0.11
Nodes (16): 7.1 Before the repository existed (1–2 Oct; planner sessions; reports 000–005), 7.2 Environment and M0 (2 Oct; reports 006–008), 7.3 M1 — physics cross-check, datasets, gate J0 (3–4 Oct; `reports/009`) — J0 PASS (9 of 9 rows), 7.4 M2a — model health (5 Oct; `reports/010`, `decisions/005`), 7.5 The 5 Oct evening and 6 Oct session (this report adds these), 7.6 Parameter count, 7. Chronological history (every session so far, with the numbers), Actions taken (+8 more)

### Community 19 - "Preregistration — Gauge-JEPA-P v2 (signed by tag `prereg-2026-10-16`)"
Cohesion: 0.10
Nodes (19): 0. What was already known when this was written (disclosure), 1. Hypotheses (thresholds are those of `configs/gates.yaml`, frozen below), 2. Frozen inputs, 3. Analysis plan (exact commands; every computation through `scripts/run.py`), 4. Exclusion and handling rules, 5. Known open items (not part of the frozen record), 6. Signatures, 7. Deviations after signing (+11 more)

### Community 20 - "jepa.py"
Cohesion: 0.12
Nodes (4): 3. Comparison table (deliverable B), ActionPredictor, MarkovPredictor, MLP

### Community 21 - "train.py"
Cohesion: 0.20
Nodes (10): effective_rank(), baseline_ridge(), baseline_supervised_mlp(), diagnostics(), fit_probe(), _flat_inputs(), forecast_jepa(), _ground_targets() (+2 more)

### Community 23 - "JEPAConfig"
Cohesion: 0.22
Nodes (13): 2. Unit tests (builder; `tests/test_jepa_options.py`, fast, fixed seeds, small `generate_dataset` as in `tests/test_pipeline.py::test_jepa_ema_target_and_curriculum`), 5. Preregistration and reporting consequences (constraint 2), JEPAConfig, vicreg_terms(), _batch(), _loss(), test_cli_flags_reach_config_and_skip_baselines(), test_default_config_is_unchanged() (+5 more)

### Community 24 - "Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier"
Cohesion: 0.12
Nodes (17): 0. The idea in one paragraph, 11. Preregistered hypotheses and expected results, 12. Error budget (lines, each measured), 13. Publishability, 14. Assumptions, risks, open points, 16. Compute: the laptop and Perlmutter only (amended 2 Oct 2026; `decisions/004`, superseding `decisions/003` and `decisions/002`), 2. Why v2 is better — side by side, 3. Physics object (frozen) and measured fingerprints (+9 more)

### Community 25 - "LinkSpace"
Cohesion: 0.15
Nodes (3): LinkSpace, m_values(), spin_matrices()

### Community 26 - "GaugeJEPA"
Cohesion: 0.22
Nodes (4): Code graph, GaugeJEPA, mix_actions(), sigreg_loss()

### Community 28 - "6. Results in full"
Cohesion: 0.13
Nodes (15): 6.10 Device parameter tables, 6.12 `v2_final` (decisions/010; `jobs/033`, desktop, 1.256 h, finished 2026-10-29 00:45 UTC, code commit `35bcf61`; evidence committed in `0067ef8`), 6.13 The exploratory J1 programme (EXPLORATORY / post-hoc; `prompts/011`, `reports/017`; jobs 034–040; commits `98255dd` (code), `77bb9a0` (screening results), `8c05689` (confirmation and S3b)), 6.14 Overall reading (what the results mean today), 6.1 J0, the data and physics gate: PASS, 9 of 9 rows (`evidence/J0_data/20261003T201012Z.json`), 6.2 Energy ceiling (J1 input; `evidence/J1_training/ceiling_main.json`, `data/main` `73fff8e5a7b7`, validation split 26,348 rows), 6.3 J1, the training-health gate: FAIL after 14 configurations plus a fresh-seed confirmation, 6.4 Dataset reproducibility (laptop vs workers) (+7 more)

### Community 29 - "records.py"
Cohesion: 0.25
Nodes (7): _bits_from_key(), estimate_chain(), estimate_diagonal(), Record, sample_exact_chain(), sample_exact_diagonal(), test_estimators_unbiased()

### Community 30 - "test_committed_graph_is_fresh"
Cohesion: 0.15
Nodes (10): Actions taken, Code graph, Laptop environments: coding repaired, su2qc-jepa created, Next action, Problems and assumptions, What was asked, 6.1 Compute (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`), 6.2 Repository and conventions (+2 more)

### Community 31 - "Hand-over report: full project state, results, data and how to continue (28 Oct 2026)"
Cohesion: 0.14
Nodes (14): 10. Problems log and open problems, 1. Glossary (every technical word used), 3. Physics and methods (short; depth in `reports/012` §2–§4), 5. Chronology (compact; commit hashes from `git log`), 8. Current in-flight state (28 Oct 2026, 23:22 UTC; `python scripts/jobs/status.py`, `git show origin/results:...`), 9. How to continue (step by step, exact commands), Actions taken (to write this report), Appendix A. Decisions (`decisions/INDEX.md`; one line each) (+6 more)

### Community 32 - "su2.py"
Cohesion: 0.19
Nodes (3): _cg_cached(), clebsch_gordan(), _fact()

### Community 34 - "test_localrun.py"
Cohesion: 0.23
Nodes (5): test_job_dies_with_the_runner(), _env(), _run(), test_add_to_empty_table_and_remove_last_entry(), test_add_update_remove_keeps_other_entries()

### Community 35 - "Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)"
Cohesion: 0.17
Nodes (11): 0.1 How to read this document, 0.2 Glossary (every technical term used), 0. Reading guide and glossary, 12. Code graph, problems and assumptions of this report, next action, 1. Project goal, scope, allowed and forbidden claims, 3. The Krylov-chain (KC) hardware carrier *(label)*, Actions taken (for this report), Appendix B — file map (where things are) (+3 more)

### Community 36 - "6. Results in full"
Cohesion: 0.17
Nodes (12): 6.10 Device parameter tables, 6.11 Overall reading (what the results mean today), 6.1 J0, the data and physics gate: PASS, 9 of 9 rows (`evidence/J0_data/20261003T201012Z.json`), 6.2 Energy ceiling (J1 input; `evidence/J1_training/ceiling_main.json`, `data/main` `73fff8e5a7b7`, validation split 26,348 rows), 6.3 J1, the training-health gate: FAIL after 14 configurations plus a fresh-seed confirmation, 6.4 Dataset reproducibility (laptop vs workers), 6.5 J2, the preregistered forecasting gate: FAIL (`evidence/J2_forecast/20261021T201507Z.json`, model `v1_final`), 6.6 Noiseless twin `ideal0`: all known-answer checks PASS (job 023; `evidence/twin/ideal0/null_check.json`, `63a42ff`) (+4 more)

### Community 37 - "M3 exploratory: strategies for J1 training success (research and comparison)"
Cohesion: 0.17
Nodes (11): 1. Diagnosis: what the 15 training runs say (all numbers from `reports/016` §6.3 and §7.6, `runs/<run>/seed*/history.json`), 2. Survey of strategies (what each does, with the source), 4. The shortlist (deliverable C, detailed in `prompts/011`), Actions taken, Appendix B. Sources opened, Code graph, M3 exploratory: strategies for J1 training success (research and comparison), Next action (+3 more)

### Community 38 - "Final hand-over report: complete project state, results, data and how to continue on the desktop (31 Oct 2026)"
Cohesion: 0.17
Nodes (12): 1. Glossary (every technical word used), 3. Physics and methods (short; depth in `reports/012` §2–§4), 5. Chronology (compact; commit hashes from `git log`), 8. Current state (31 Oct 2026; `python scripts/jobs/status.py`, `git status`, `git fetch`), Actions taken (to write this report), Appendix A. Decisions (`decisions/INDEX.md`; one line each), Appendix B. File map, Appendix C. Commit list (`git log --oneline | head -100`, newest first; 154 commits in all; hash, day-month, time, subject) (+4 more)

### Community 39 - "crosscheck_su2qc.py"
Cohesion: 0.26
Nodes (6): compare_point(), extract_terms(), import_su2qc(), main(), sign_gauge(), su2qc_label_to_c()

### Community 40 - "Krylov"
Cohesion: 0.26
Nodes (3): evolve(), Krylov, krylov_error()

### Community 42 - "ObservationSpec"
Cohesion: 0.20
Nodes (6): Context, Definition of done, M3 exploratory: J1 training improvement experiments, Out of scope / stop conditions, ObservationSpec, test_observation_spec_roundtrip()

### Community 43 - "M2a closed: J1 FAIL after 14 configurations (semigroup row on a fresh seed); working model $w_{\text{sigreg}}=3$, $w_{\text{semigroup}}=10$"
Cohesion: 0.18
Nodes (10): Cost, Dataset reproducibility (`evidence/J0_data/fingerprint_compare_*.json`), Forecasting, preliminary (`runs/v1_confirm/forecast_eval.json`; not a J2 result), J1 (validation split, final epoch; every row is in `evidence/GATE_LEDGER.md`), M2a closed: J1 FAIL after 14 configurations (semigroup row on a fresh seed); working model $w_{\text{sigreg}}=3$, $w_{\text{semigroup}}=10$, Next action, Problems and assumptions, Results and what they mean (+2 more)

### Community 45 - "CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`"
Cohesion: 0.20
Nodes (9): 1. Priorities, in order, 2. Session protocol (every session, no exceptions), 3. Frozen things (changing any of these needs a new `decisions/` record and a new version tag), 4. Hardware rules (non-negotiable), 6. Writing rules (reports, prompts, docs, paper), 7. What the package already guarantees (do not re-derive, do re-run), 8. Where things are, CLAUDE.md — rules for every Claude Code session in `su2qc-jepa` (+1 more)

### Community 46 - "graph.py"
Cohesion: 0.29
Nodes (6): _edges(), graph_stats(), load_graph(), same_structure(), structure_signature(), test_graph_helpers()

### Community 47 - "decisions/INDEX.md"
Cohesion: 0.20
Nodes (6): Frozen conventions and coupling points, Alternatives considered, Decision, Twin with Quantinuum noise from Nexus device specifications, Why, Decisions — index

### Community 48 - "Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code)"
Cohesion: 0.20
Nodes (10): Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code), Model, Observables, Predicted results, Problems and assumptions, Publishability, Schedule (5 Oct – 29 Nov 2026), Testing ladder (budgets are Claude's estimates) (+2 more)

### Community 49 - "prompts/INDEX.md"
Cohesion: 0.20
Nodes (5): Expected, M6 — Hardware day 3, gate J3, error budget (W6, 2 sessions), M7 — One stretch item (W7), chosen on 15 Nov by Digonto, M8 — Paper assembly, release, replication (W8, 2 sessions), Prompts — index

### Community 50 - "11. What happens next"
Cohesion: 0.20
Nodes (10): 11.1 The rest of M2 (M2a continuation, `prompts/010`), 11.2 M2b — preregistration (16 Oct; `prompts/002` items 6–8), 11.3 M3 (W3, 19–25 Oct; `prompts/003`): forecasting, calibrated twin, dry run, 11.4 M4 (W4, 26 Oct – 1 Nov; `prompts/004`): J2 and the pilot (end of the one-month version), 11.5 M5 (W5, 2–8 Nov; `prompts/005`): hardware days 1 and 2, 11.6 M6 (W6, 9–15 Nov; `prompts/006`): day 3, J3, error budget, 11.7 M7 (W7, 16–22 Nov; `prompts/007`): one stretch item, chosen 15 Nov by Digonto, 11.8 M8 (W8, 23–29 Nov; `prompts/008`): paper, release, replication (+2 more)

### Community 51 - "4. Infrastructure and how to operate it"
Cohesion: 0.20
Nodes (10): 4.1 Rules of the house (read `CLAUDE.md` and `~/.claude/CLAUDE.md` first), 4.2 Three machines, 4.3 The runner (`scripts/run.py`, `decisions/004`, `configs/compute.yaml`), 4.4 The job queue, 4.5 Repository layout (details in Appendix B), 4.6 Code graph (Graphify), 4.7 CI and environment pins, 4.8 Credentials and hardware rules (`CLAUDE.md` §4) (+2 more)

### Community 52 - "7. Plot data (the data to re-make every figure, for example on claude.ai)"
Cohesion: 0.20
Nodes (10): 7.0 How to use this section, 7.1 T1 Spearman(score, exact_error) and AUROC(score separates arm B from arm A), per twin, shot level and score, 7.2 T2 mean flag rate and mean exact error by arm and depth (4000 shots), 7.3 T3 noiseless null check by shot level (evidence/twin/ideal0/null_check.json), 7.4 T4 cross-carrier summary (v1_final seed0; evidence/twin/cross_carrier/cross_carrier.json; median / p90 / median over noise_diag), 7.5 J2 MAE (evidence/runs/v1_final/forecast_eval.json = input of evidence/J2_forecast/20261021T201507Z.json; mean of 5 seeds; n_test {'onfam': 2935, 'strong': 3134} ; context_step 4 ; master_seed 27182818 ), 7.7 T5 Quantinuum device parameters (evidence/hardware/quantinuum_devices_20261028T220635Z.json), 7. Plot data (the data to re-make every figure, for example on claude.ai) (+2 more)

### Community 53 - "4. Infrastructure and how to operate it"
Cohesion: 0.20
Nodes (10): 4.1 Rules of the house (read `CLAUDE.md` and `~/.claude/CLAUDE.md` first), 4.2 Three machines (state on 31 Oct 2026; from now on the desktop is also the development machine, see 4A), 4.3 The runner (`scripts/run.py`, `decisions/004`, `configs/compute.yaml`), 4.4 The job queue, 4.5 Repository layout (details in Appendix B), 4.6 Code graph (Graphify), 4.7 CI and environment pins, 4.8 Credentials and hardware rules (`CLAUDE.md` §4) (+2 more)

### Community 54 - "9. How to continue (prioritised, exact commands)"
Cohesion: 0.20
Nodes (10): 9. How to continue (prioritised, exact commands), Decisions only Digonto can take (ask first), Risks and open questions, Step A. Set up the desktop and verify (section 4A), Step B. J1 in information mode for `v2_final` (cheap, light, do this first), Step C. The S2 + S3b combination (decision A), Step D. Re-run the four twin campaigns with `v2_final` (or the adopted model) — the first fair test of H3, Step E. Finish M3 (`prompts/003`) (+2 more)

### Community 55 - "pick_device"
Cohesion: 0.22
Nodes (8): Alternatives considered, Compute: laptop for light work, Perlmutter for heavy jobs, Consequences, Decision, Why, Actions taken, 4A.3 Coexisting with the worker, pick_device()

### Community 56 - "Model card — Gauge-JEPA-P v1 (working configuration after M2a)"
Cohesion: 0.22
Nodes (8): 1. What the model is, 2. Working configuration, 3. Training cost, 4. J1 results (validation split, final epoch; `evidence/GATE_LEDGER.md`, `figures/000`, `figures/001`), 5. Forecasting, preliminary (`runs/v1_confirm/forecast_eval.json`, mean of 5 seeds; NOT a J2 result, since J2 is run in M4a), 6. Data and reproducibility, 7. Known limitations, Model card — Gauge-JEPA-P v1 (working configuration after M2a)

### Community 58 - "M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914)"
Cohesion: 0.22
Nodes (8): Laptop check, 10 epochs, 1 seed (`runs/v1_check/seed0/history.json`, local; validation split), M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914), Next action, Options for Digonto (a decision record in `decisions/` is needed for any of B–D, before the 16 Oct preregistration), Problems and assumptions, Results and what they mean, The energy row cannot pass with this encoder (`evidence/J1_training/ceiling_main.json`, validation split, 26,348 rows; training split 126,824 rows; `data/main` `73fff8e5a7b7`), What was asked

### Community 59 - "Numbered artifacts and the Graphify code graph"
Cohesion: 0.25
Nodes (7): Alternatives considered, Consequences, Decision, Numbered artifacts and the Graphify code graph, Why, 15. Repository conventions — numbered artifacts and the code graph (added 2 Oct 2026; `decisions/001`), series()

### Community 60 - "J3 gate scores the low-shot rows at the preregistered 512 shots"
Cohesion: 0.25
Nodes (6): Alternatives considered, Consequences, Decision, J3 gate scores the low-shot rows at the preregistered 512 shots, Why, test_j3_uses_the_preregistered_low_shot_level()

### Community 61 - "scripts/run.py"
Cohesion: 0.32
Nodes (3): dataset_step(), guess_outputs(), queue()

### Community 62 - "Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`)"
Cohesion: 0.25
Nodes (8): Absolute safety rules (you have no permission prompts), Context, Definition of done, Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`), Phase A — inventory and backup (no changes), Phase B — repair `coding` (only after rule 4 allows it), Phase C — create `su2qc-jepa` (safe to do at any time; it touches no existing environment), Phase D — report

### Community 64 - "Package build: plan audit, Gauge-JEPA-P v2 and the starter package"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Package build: plan audit, Gauge-JEPA-P v2 and the starter package, Problems and assumptions, Results and what they mean, What was asked

### Community 65 - "Conventions update: numbered artifacts and the Graphify code graph"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Conventions update: numbered artifacts and the Graphify code graph, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 66 - "Compute update 2: safe laptop and a pull-based job queue for Perlmutter"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Compute update 2: safe laptop and a pull-based job queue for Perlmutter, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 67 - "Perlmutter worker install keeps the user's other scrontab entries"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Perlmutter worker install keeps the user's other scrontab entries, Problems and assumptions, Results and what they mean, What was asked

### Community 68 - "7.6 J1 data for all 14 configurations and v1_final"
Cohesion: 0.25
Nodes (8): 7.6 J1 data for all 14 configurations and v1_final, args.json of v1_final and v1_confirm, P8x final epoch (200), per seed, all configurations (runs/<run>/seed0..4/history.json, unmasked), P8y per-configuration summary of the final epoch (what the J1 gate compares: min over seeds, max for semigroup), P-curve: effective rank (seed mean; band min..max in P1 of reports/012 for configs 1-6) at selected epochs (all configurations), P-curve: grounding R2 of energy (seed mean) at selected epochs, P-curve: semigroup residual (seed mean; log axis) at selected epochs (all configurations), P-curve: training loss terms (unweighted, seed mean) at epoch 200, all configurations

### Community 70 - "residual_eval.py"
Cohesion: 0.32
Nodes (3): estimate(), krylov(), subsample()

### Community 71 - "{{title}}"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Problems and assumptions, Results and what they mean, {{title}}, What was asked

### Community 72 - "M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)"
Cohesion: 0.29
Nodes (6): Expected, M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h), Part A — cross-check against the project's verified `su2qc` code, Part B — datasets, Part C — gate, Tests to add

### Community 73 - "su2qc-jepa — Gauge-JEPA-P v2 starter package"
Cohesion: 0.29
Nodes (6): First two sessions on the laptop, Five-minute tour, Install on the laptop (done by prompts/009), Layout, su2qc-jepa — Gauge-JEPA-P v2 starter package, What is verified today (`python scripts/run.py -- python -m pytest -q`: 47 fast tests; `-m slow` adds 1 more)

### Community 74 - "Compute update: laptop for light work, Perlmutter for heavy jobs"
Cohesion: 0.29
Nodes (6): Code graph, Compute update: laptop for light work, Perlmutter for heavy jobs, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 75 - "M0: repository created, CI green, code graph committed"
Cohesion: 0.29
Nodes (6): Actions taken, Code graph, M0: repository created, CI green, code graph committed, Next action, Problems and assumptions, What was asked

### Community 76 - "4. The world model (JEPA)"
Cohesion: 0.29
Nodes (7): 4.1 Observation, actions, training rule, 4.2 Architecture (`src/su2qc_jepa/models/jepa.py`), 4.3 Losses, 4.4 Baselines, tasks, 4. The world model (JEPA), Appendix A. Probe script (`.local_runs/probe/planner_probe.py`, git-ignored; run with `python scripts/run.py --no-queue --threads 1 -- python .local_runs/probe/planner_probe.py`), eff_rank()

### Community 77 - "5. Data, twin, hardware plan, gates, hypotheses, error budget"
Cohesion: 0.29
Nodes (7): 5.1 Data (`evidence/J0_data/datasets.json`, commit `358d0bd`; checksums are sha256 of the data arrays, first 12 hex digits shown), 5.2 The digital twin, 5.3 Hardware plan and rules (nothing submitted), 5.4 Gates (current thresholds, `configs/gates.yaml`), 5.5 Preregistered hypotheses H1–H5 (plan §11, `docs/PREREGISTRATION.md` draft), 5.6 Error budget (lines, each to be measured; plan §12), 5. Data, twin, hardware plan, gates, hypotheses, error budget

### Community 78 - "8. Current results in full"
Cohesion: 0.29
Nodes (7): 8.1 J0 (data gate): PASS, 9 of 9 rows (`evidence/J0_data/20261003T201012Z.json`, `evidence/GATE_LEDGER.md`), 8.2 Energy ceiling (J1 input; `evidence/J1_training/ceiling_main.json`, commit `63065dd`, 2026-10-05T17:31Z; `data/main` `73fff8e5a7b7`; training split 126,824 rows, validation split 26,348 rows; regressor seeds 462709266, 3658436304), 8.3 J1 (training gate) for the six gated rungs (official gate runs; `evidence/GATE_LEDGER.md` rows; records in `evidence/J1_training/`), 8.4 Dataset reproducibility (laptop versus Perlmutter; `evidence/J0_data/fingerprint_compare_*.json`, commit `3010090`, 2026-10-05T23:47Z), 8.5 GPU-fix verification and the job table, 8.6 Forecast results so far, 8. Current results in full

### Community 80 - "Compute: a safe laptop and a pull-based job queue for Perlmutter"
Cohesion: 0.33
Nodes (5): Alternatives considered, Compute: a safe laptop and a pull-based job queue for Perlmutter, Consequences, Decision, Why

### Community 81 - "J1 energy grounding threshold set relative to the measured information ceiling"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences (what must be re-run or re-checked), Decision, J1 energy grounding threshold set relative to the measured information ceiling, Why

### Community 82 - "Preregistration deviation: dataset-equivalence tolerance corrected to rounding scale"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences, Decision, Preregistration deviation: dataset-equivalence tolerance corrected to rounding scale, Why

### Community 83 - "Preregistration deviation: J3 model `v2_final` reads only the physical observables"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences, Decision, Preregistration deviation: J3 model `v2_final` reads only the physical observables, Why

### Community 84 - "Heavy jobs on the desktop GPU (RTX 3070) — setup and daily use"
Cohesion: 0.33
Nodes (5): Daily use, From the laptop, Heavy jobs on the desktop GPU (RTX 3070) — setup and daily use, One-time setup (on the desktop, Linux, about 20 minutes), Troubleshooting (on the desktop)

### Community 85 - "M0 — Bootstrap (first Claude Code invocation, ~45 min)"
Cohesion: 0.33
Nodes (5): Context, Definition of done, M0 — Bootstrap (first Claude Code invocation, ~45 min), Out of scope, Tasks

### Community 86 - "M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card"
Cohesion: 0.33
Nodes (5): Context, Definition of done, M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card, Out of scope / stop conditions, Tasks

### Community 87 - "Tasks"
Cohesion: 0.33
Nodes (6): 1. Code changes (builder; `graphify affected "GaugeJEPA"`, `"ActionPredictor"`, `"run_j1"` first and run the tests it lists), 3. Screening stage (paired design: one master seed for every arm, so seeds are matched), 4. Confirmation stage (fresh master seeds, full protocol), 5. Replication (one more fresh master seed), 6. Session report, Tasks

### Community 88 - "Results and what they mean"
Cohesion: 0.33
Nodes (6): `coding`: imports before and after (`import-before.json` → `import-after.json`), Disk, `pip check`, Results and what they mean, `su2qc-jepa` environment, The GTX 1060 (compute capability 6.1, driver 580.178.04, CUDA 13.0 driver API)

### Community 89 - "2. Physics"
Cohesion: 0.33
Nodes (6): 2.1 Model and Hamiltonian, 2.2 Coupling points, 2.3 Verified fingerprints (PROVEN by tests or MEASURED), 2.4 Named states and bare energies, 2.6 Cross-check against the project's independent verified code (M1; `evidence/J0_data/crosscheck_su2qc.json`, status PASS, tolerance $10^{-10}$, commit `0bb5d6d`), 2. Physics

### Community 90 - "2. Project goal, claims, preregistration"
Cohesion: 0.33
Nodes (6): 2.1 Goal (plain English), 2.2 Claims allowed and forbidden (`reports/012` §1, `CLAUDE.md` §6, `docs/CLAIMS.md`), 2.3 Hypotheses and their status (`docs/PREREGISTRATION.md` §1; thresholds in `configs/gates.yaml`), 2.3b Claims ledger now (`docs/CLAIMS.md`), 2.4 Preregistration and its deviations, 2. Project goal, claims, preregistration

### Community 91 - "Appendix D. Helper scripts (verbatim; in `.local_runs/probe/`, git-ignored; run each with `python scripts/run.py --no-queue --threads 1 -- python .local_runs/probe/<name>.py`, then read the runner log)"
Cohesion: 0.33
Nodes (6): Appendix D. Helper scripts (verbatim; in `.local_runs/probe/`, git-ignored; run each with `python scripts/run.py --no-queue --threads 1 -- python .local_runs/probe/<name>.py`, then read the runner log), D.final_tables.py, D.j1_tables.py, D.j2_dev_tables.py, D.screen_table.py, D.twin_tables.py

### Community 93 - "{{title}}"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences (what must be re-run or re-checked), Decision, {{title}}, Why

### Community 94 - "{{title}}"
Cohesion: 0.33
Nodes (5): Context, Definition of done, Out of scope / stop conditions, Tasks, {{title}}

### Community 95 - "M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)"
Cohesion: 0.40
Nodes (4): Expected, M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions), Session M2a — make the model healthy, Session M2b — preregistration (16 Oct)

### Community 96 - "M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)"
Cohesion: 0.40
Nodes (4): Expected, M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions), Session M3a — forecasting, Session M3b — twin and dry run

### Community 97 - "M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version."
Cohesion: 0.40
Nodes (4): Expected, M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version., Session M4a — J2 (30 Oct), Session M4b — pilot (one job)

### Community 99 - "2. Project goal, claims, preregistration"
Cohesion: 0.40
Nodes (5): 2.1 Goal (plain English), 2.2 Claims allowed and forbidden (`reports/012` §1, `CLAUDE.md` §6, `docs/CLAIMS.md`), 2.3 Hypotheses (`docs/PREREGISTRATION.md` §1; thresholds in `configs/gates.yaml`), 2.4 Preregistration and its deviations, 2. Project goal, claims, preregistration

### Community 100 - "4A. Moving development to the desktop (new; read before doing anything on the desktop)"
Cohesion: 0.40
Nodes (5): 4A.1 What already exists on the desktop (from `docs/DESKTOP.md`, `scripts/worker/*.sh`; verify, do not assume), 4A.2 Steps (one-time), 4A.4 Which rules of `CLAUDE.md` assume the laptop (proposals; nothing was changed), 4A.5 First actions for the first desktop session (checklist), 4A. Moving development to the desktop (new; read before doing anything on the desktop)

### Community 102 - "Appendix A — helper scripts (verbatim; run with `python scripts/run.py --no-queue --threads 1 -- python <script> <out.md>` from the repository root)"
Cohesion: 0.50
Nodes (4): A.1 plot_tables.py (plots P1 to P9, P12), A.2 physics_curves.py (plot P11a to P11d), A.3 evidence_tables.py (P10, P11e, P11f, job and reproducibility tables), Appendix A — helper scripts (verbatim; run with `python scripts/run.py --no-queue --threads 1 -- python <script> <out.md>` from the repository root)

### Community 103 - "Appendix D. Helper scripts (verbatim; in `.local_runs/probe/`, git-ignored; run each with `python scripts/run.py --no-queue --threads 1 -- python .local_runs/probe/<name>.py`, then read the runner log)"
Cohesion: 0.50
Nodes (4): Appendix D. Helper scripts (verbatim; in `.local_runs/probe/`, git-ignored; run each with `python scripts/run.py --no-queue --threads 1 -- python .local_runs/probe/<name>.py`, then read the runner log), D.j1_tables.py, D.j2_dev_tables.py, D.twin_tables.py

## Knowledge Gaps
- **479 isolated node(s):** `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script`, `PYTHONHASHSEED`, `replicate.sh script` (+474 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 783 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PlaquetteModel` connect `PlaquetteModel` to `Conventions update: numbered artifacts and the Graphify code graph`, `test_physics.py`, `crosscheck_su2qc.py`, `generate_dataset`, `j0_data.py`, `trajectories.py`, `dataset_fingerprint`, `4. Infrastructure and how to operate it`, `4. Infrastructure and how to operate it`, `LinkSpace`, `test_committed_graph_is_fresh`?**
  _High betweenness centrality (0.136) - this node is a cross-community bridge._
- **Why does `Final hand-over report: complete project state, results, data and how to continue on the desktop (31 Oct 2026)` connect `Final hand-over report: complete project state, results, data and how to continue on the desktop (31 Oct 2026)` to `reports/INDEX.md`, `Worker`, `4A. Moving development to the desktop (new; read before doing anything on the desktop)`, `7. Plot data (the data to re-make every figure, for example on claude.ai)`, `4. Infrastructure and how to operate it`, `9. How to continue (prioritised, exact commands)`, `2. Project goal, claims, preregistration`, `Appendix D. Helper scripts (verbatim; in `.local_runs/probe/`, git-ignored; run each with `python scripts/run.py --no-queue --threads 1 -- python .local_runs/probe/<name>.py`, then read the runner log)`, `6. Results in full`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Why does `Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)` connect `Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)` to `9. Plot data (the data behind every figure; each table can be parsed as Markdown)`, `Appendix A — helper scripts (verbatim; run with `python scripts/run.py --no-queue --threads 1 -- python <script> <out.md>` from the repository root)`, `retry_resources`, `5. Data, twin, hardware plan, gates, hypotheses, error budget`, `4. The world model (JEPA)`, `8. Current results in full`, `11. What happens next`, `dataset_fingerprint`, `2. Physics`, `test_committed_graph_is_fresh`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `PlaquetteModel` (e.g. with `Code graph` and `6.2 Repository and conventions`) actually correct?**
  _`PlaquetteModel` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `generate_dataset()` (e.g. with `2. Unit tests (builder; `tests/test_jepa_options.py`, fast, fixed seeds, small `generate_dataset` as in `tests/test_pipeline.py::test_jepa_ema_target_and_curriculum`)` and `Code graph`) actually correct?**
  _`generate_dataset()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script` to the rest of the system?**
  _479 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `noise.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06376811594202898 - nodes in this community are weakly interconnected._