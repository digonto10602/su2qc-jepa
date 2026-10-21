# Graph Report - su2qc-jepa  (2026-10-21)

## Corpus Check
- 129 files · ~129,366 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 3, .cff 1)

## Summary
- 1170 nodes · 2110 edges · 108 communities (69 shown, 39 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 159 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4a44a69d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier
- Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)
- 9. Plot data (the data behind every figure; each table can be parsed as Markdown)
- artifacts.py
- run_j0
- Worker
- trajectories.py
- ibm.py
- Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)
- FullSpaceOperators
- chain.py
- Preregistration — Gauge-JEPA-P v2 (signed by tag `prereg-2026-10-16`)
- PlaquetteModel
- lanczos
- test_jobs.py
- LinkSpace
- localrun.py
- test_crosscheck.py
- test_localrun.py
- train.py
- ChainSpec
- test_physics.py
- jepa.py
- compare_point
- generate_dataset
- su2.py
- test_training_and_baselines_run_on_device
- GaugeJEPA
- _queue_setup
- test_committed_graph_is_fresh
- M2a closed: J1 FAIL after 14 configurations (semigroup row on a fresh seed); working model $w_{\text{sigreg}}=3$, $w_{\text{semigroup}}=10$
- Desktop GPU worker online; `v1_final` trained; preregistered J2 FAIL (on-family passes, strong coupling fails)
- CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`
- test_worker_recovers_interrupted_local_jobs
- prompts/INDEX.md
- M1: su2qc cross-check PASS, three datasets built, gate J0 PASS
- ObservableSet
- retry_resources
- Model card — Gauge-JEPA-P v1 (working configuration after M2a)
- M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED
- M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914)
- test_jepa_trains_one_epoch
- Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`)
- Package build: plan audit, Gauge-JEPA-P v2 and the starter package
- Conventions update: numbered artifacts and the Graphify code graph
- Compute update 2: safe laptop and a pull-based job queue for Perlmutter
- Compute update 3: laptop and Perlmutter only, environment repair prompt, self-healing runners
- Perlmutter worker install keeps the user's other scrontab entries
- test_dynamics_reproduce_preliminary_expectation
- _Cache
- named_states
- {{title}}
- pick_device
- os
- M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)
- su2qc-jepa — Gauge-JEPA-P v2 starter package
- Compute update: laptop for light work, Perlmutter for heavy jobs
- M0: repository created, CI green, code graph committed
- compute.py
- Compute: a safe laptop and a pull-based job queue for Perlmutter
- J1 energy grounding threshold set relative to the measured information ceiling
- Preregistration deviation: dataset-equivalence tolerance corrected to rounding scale
- Heavy jobs on the desktop GPU (RTX 3070) — setup and daily use
- Heavy jobs: the job queue and the Perlmutter worker
- M0 — Bootstrap (first Claude Code invocation, ~45 min)
- M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card
- Results and what they mean
- 7. Chronological history (every session so far, with the numbers)
- residual_eval.py
- {{title}}
- {{title}}
- decisions/INDEX.md
- Numbered artifacts and the Graphify code graph
- Compute: laptop for light work, Perlmutter for heavy jobs
- M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)
- M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)
- M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version.
- reports/INDEX.md
- ._apply_term
- 10. Decisions log and problems/risks
- noise.py
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
1. `PlaquetteModel` - 43 edges
2. `Worker` - 24 edges
3. `generate_dataset()` - 24 edges
4. `run_j0()` - 24 edges
5. `test_training_and_baselines_run_on_device()` - 22 edges
6. `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier` - 20 edges
7. `ObservableSet` - 19 edges
8. `Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)` - 19 edges
9. `Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)` - 17 edges
10. `9. Plot data (the data behind every figure; each table can be parsed as Markdown)` - 17 edges

## Surprising Connections (you probably didn't know these)
- `Self-healing` --references--> `retry_resources()`  [INFERRED]
  docs/PERLMUTTER.md → src/su2qc_jepa/jobs.py
- `Actions taken` --references--> `retry_resources()`  [INFERRED]
  reports/004_compute-update-3-laptop-and-perlmutter-only-environment-repa.md → src/su2qc_jepa/jobs.py
- `10.1 Decisions (`decisions/INDEX.md`)` --references--> `retry_resources()`  [INFERRED]
  reports/012_full-project-report-plan-physics-methods-every-result-and-th.md → src/su2qc_jepa/jobs.py
- `10.4 M2a — model health (5 Oct; `reports/010`, `decisions/005`, and results fetched at 21:30 UTC)` --references--> `baseline_autoregressive()`  [INFERRED]
  reports/011_project-overview-gauge-jepa-p-v2-plan-physics-status-and-eve.md → src/su2qc_jepa/models/train.py
- `12. Open problems and risks (as of 5 Oct, 21:40 UTC)` --references--> `baseline_autoregressive()`  [INFERRED]
  reports/011_project-overview-gauge-jepa-p-v2-plan-physics-status-and-eve.md → src/su2qc_jepa/models/train.py

## Import Cycles
- None detected.

## Communities (108 total, 39 thin omitted)

### Community 0 - "Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier"
Cohesion: 0.04
Nodes (41): Decision, Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code), Model, Observables, Predicted results, Problems and assumptions, Publishability, Schedule (5 Oct – 29 Nov 2026) (+33 more)

### Community 2 - "Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)"
Cohesion: 0.04
Nodes (45): 0.1 How to read this document, 0.2 Glossary (every technical term used), 0. Reading guide and glossary, 11.1 The rest of M2 (M2a continuation, `prompts/010`), 11.2 M2b — preregistration (16 Oct; `prompts/002` items 6–8), 11.3 M3 (W3, 19–25 Oct; `prompts/003`): forecasting, calibrated twin, dry run, 11.4 M4 (W4, 26 Oct – 1 Nov; `prompts/004`): J2 and the pilot (end of the one-month version), 11.5 M5 (W5, 2–8 Nov; `prompts/005`): hardware days 1 and 2 (+37 more)

### Community 3 - "9. Plot data (the data behind every figure; each table can be parsed as Markdown)"
Cohesion: 0.05
Nodes (40): 9.0 How to use this section, 9.1 Catalogue of plots, 9.2 P11 sub-plots (physics curves and carrier costs), 9. Plot data (the data behind every figure; each table can be parsed as Markdown), Dataset reproducibility (evidence/J0_data/fingerprint_compare_*.json; per-trajectory-sum tolerance 1e-12), Further machine-readable tables (P10, P11e, P11f, J1 records, jobs, dataset reproducibility), J1 gate records (evidence/J1_training/*.json), Job table (jobs/*.yaml and evidence/jobs/NNN/status.json; states read on 2026-10-06 by scripts/jobs/status.py) (+32 more)

### Community 4 - "artifacts.py"
Cohesion: 0.11
Nodes (23): Artifact, check_artifacts(), list_artifacts(), new_artifact(), next_number(), read_front_matter(), render_index(), _resolve() (+15 more)

### Community 5 - "run_j0"
Cohesion: 0.10
Nodes (16): run_j0(), run_j1(), run_j2(), auroc(), run_j3(), spearman(), _fmt(), GateResult (+8 more)

### Community 6 - "Worker"
Cohesion: 0.17
Nodes (6): Code graph, hms_to_hours(), main(), now(), sh(), Worker

### Community 7 - "trajectories.py"
Cohesion: 0.13
Nodes (10): _bits_from_key(), estimate_chain(), estimate_diagonal(), ObservationSpec, Record, sample_exact_chain(), sample_exact_diagonal(), chain_point_records() (+2 more)

### Community 8 - "ibm.py"
Cohesion: 0.10
Nodes (14): W4 (26 Oct – 1 Nov) — J2, pilot job; end of the one-month version, BudgetError, calibration_snapshot(), check_budget(), collect(), dry_run(), DryRunSummary, estimate_qpu_seconds() (+6 more)

### Community 9 - "Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)"
Cohesion: 0.07
Nodes (29): 0. How to read this document, 10.1 Before the repository existed (1–2 Oct, planner sessions; reports 000–005), 10.2 Environment and M0 (2 Oct; reports 006–008), 10.3 M1 — physics cross-check, datasets, gate J0 (3–4 Oct; `reports/009`) — **J0 PASS 9/9**, 10.4 M2a — model health (5 Oct; `reports/010`, `decisions/005`, and results fetched at 21:30 UTC), 10. What has been done, session by session (with every number), 11. Infrastructure and repository conventions (how the work is done), 12. Open problems and risks (as of 5 Oct, 21:40 UTC) (+21 more)

### Community 11 - "chain.py"
Cohesion: 0.14
Nodes (12): _bond_rotation(), build_chain_prep_circuit(), chain_amplitudes(), chain_sector_unitary(), _layer(), _phase_weights(), prep_cascade_params(), sample_x_basis() (+4 more)

### Community 13 - "Preregistration — Gauge-JEPA-P v2 (signed by tag `prereg-2026-10-16`)"
Cohesion: 0.10
Nodes (19): 0. What was already known when this was written (disclosure), 1. Hypotheses (thresholds are those of `configs/gates.yaml`, frozen below), 2. Frozen inputs, 3. Analysis plan (exact commands; every computation through `scripts/run.py`), 4. Exclusion and handling rules, 5. Known open items (not part of the frozen record), 6. Signatures, 7. Deviations after signing (+11 more)

### Community 15 - "lanczos"
Cohesion: 0.16
Nodes (9): Results and what they mean, 2.3 Verified fingerprints (PROVEN by tests or MEASURED), krylov(), evolve(), Krylov, krylov_error(), lanczos(), sector_restrict() (+1 more)

### Community 16 - "test_jobs.py"
Cohesion: 0.15
Nodes (8): _hms(), parse_steps(), validate_job(), good_job(), test_allowlist_refuses(), test_job_destinations(), test_valid_job_passes(), test_validation_catches_bad_fields()

### Community 17 - "LinkSpace"
Cohesion: 0.13
Nodes (3): LinkSpace, m_values(), spin_matrices()

### Community 18 - "localrun.py"
Cohesion: 0.17
Nodes (12): Problems and assumptions, _arg(), estimate_minutes(), is_resource_failure(), ledger_append(), _limit_env(), load_policy(), _manifest_ntrain() (+4 more)

### Community 20 - "test_localrun.py"
Cohesion: 0.23
Nodes (11): admit(), classify(), heal_decision(), is_heavy(), Policy, Probe, Request, test_admission_on_the_64gb_laptop() (+3 more)

### Community 21 - "train.py"
Cohesion: 0.23
Nodes (8): effective_rank(), baseline_ridge(), diagnostics(), fit_probe(), _flat_inputs(), forecast_jepa(), _ground_targets(), r2_score()

### Community 22 - "ChainSpec"
Cohesion: 0.17
Nodes (7): build_chain_circuit(), z_layer(), ChainSpec, trotter_error(), twin_variance_check(), test_chain_cz_budget_PA(), test_twin_runner_seed_independence()

### Community 23 - "test_physics.py"
Cohesion: 0.14
Nodes (7): Claims ledger — every substantive statement, its status and its evidence, cz_count(), model(), test_chain_circuit_matches_sector_unitary(), test_channel_split(), test_jmax1_counts(), test_two_routes_agree_and_gauss_law()

### Community 25 - "compare_point"
Cohesion: 0.15
Nodes (7): compare_point(), extract_terms(), import_su2qc(), main(), sign_gauge(), su2qc_label_to_c(), Couplings

### Community 26 - "generate_dataset"
Cohesion: 0.30
Nodes (9): DatasetConfig, FamilyConfig, generate_dataset(), load_dataset(), test_chain_dataset_uses_chain_carrier(), test_dataset_fingerprint_is_exact_and_locates_differences(), test_dataset_generation_and_splits(), test_fingerprint_equivalence_verdict() (+1 more)

### Community 27 - "su2.py"
Cohesion: 0.19
Nodes (3): _cg_cached(), clebsch_gordan(), _fact()

### Community 28 - "test_training_and_baselines_run_on_device"
Cohesion: 0.24
Nodes (8): 7.5 The 5 Oct evening and 6 Oct session (this report adds these), Actions taken, Code graph, load(), dataset_fingerprint(), baseline_autoregressive(), baseline_supervised_mlp(), test_training_and_baselines_run_on_device()

### Community 30 - "_queue_setup"
Cohesion: 0.20
Nodes (7): Actions taken, _git(), _queue_setup(), ignore(), test_run_py_queues_heavy_work_for_the_chosen_worker(), test_worker_end_to_end_local(), test_worker_slurm_mode_resubmits_after_timeout()

### Community 31 - "test_committed_graph_is_fresh"
Cohesion: 0.20
Nodes (7): Actions taken, Code graph, Laptop environments: coding repaired, su2qc-jepa created, Next action, Problems and assumptions, What was asked, test_committed_graph_is_fresh()

### Community 32 - "M2a closed: J1 FAIL after 14 configurations (semigroup row on a fresh seed); working model $w_{\text{sigreg}}=3$, $w_{\text{semigroup}}=10$"
Cohesion: 0.18
Nodes (10): Cost, Dataset reproducibility (`evidence/J0_data/fingerprint_compare_*.json`), Forecasting, preliminary (`runs/v1_confirm/forecast_eval.json`; not a J2 result), J1 (validation split, final epoch; every row is in `evidence/GATE_LEDGER.md`), M2a closed: J1 FAIL after 14 configurations (semigroup row on a fresh seed); working model $w_{\text{sigreg}}=3$, $w_{\text{semigroup}}=10$, Next action, Problems and assumptions, Results and what they mean (+2 more)

### Community 33 - "Desktop GPU worker online; `v1_final` trained; preregistered J2 FAIL (on-family passes, strong coupling fails)"
Cohesion: 0.18
Nodes (10): Actions taken, Cost, Dataset used by `v1_final` (`evidence/J0_data/fingerprint_compare_main_laptop_vs_desktop_v1_final.json`), Desktop GPU worker online; `v1_final` trained; preregistered J2 FAIL (on-family passes, strong coupling fails), J1 on `v1_final`, information only (`evidence/J1_training/20261021T203007Z.json`), J2: preregistered forecasting gate, **FAIL** (`evidence/J2_forecast/20261021T201507Z.json`), Next action, Problems and assumptions (+2 more)

### Community 34 - "CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`"
Cohesion: 0.20
Nodes (9): 1. Priorities, in order, 2. Session protocol (every session, no exceptions), 3. Frozen things (changing any of these needs a new `decisions/` record and a new version tag), 4. Hardware rules (non-negotiable), 6. Writing rules (reports, prompts, docs, paper), 7. What the package already guarantees (do not re-derive, do re-run), 8. Where things are, CLAUDE.md — rules for every Claude Code session in `su2qc-jepa` (+1 more)

### Community 35 - "test_worker_recovers_interrupted_local_jobs"
Cohesion: 0.22
Nodes (8): Alternatives considered, Compute: add the desktop RTX 3070 as a second job-queue worker, Consequences (what must be re-run or re-checked), Decision, Why, test_worker_recovers_interrupted_local_jobs(), _tick(), _tiny_job()

### Community 36 - "prompts/INDEX.md"
Cohesion: 0.20
Nodes (5): Expected, M6 — Hardware day 3, gate J3, error budget (W6, 2 sessions), M7 — One stretch item (W7), chosen on 15 Nov by Digonto, M8 — Paper assembly, release, replication (W8, 2 sessions), Prompts — index

### Community 37 - "M1: su2qc cross-check PASS, three datasets built, gate J0 PASS"
Cohesion: 0.20
Nodes (9): Actions taken, Code graph, M1: su2qc cross-check PASS, three datasets built, gate J0 PASS, Next action, Part A — route C agrees with both su2qc routes (`evidence/J0_data/crosscheck_su2qc.json`, commit `0bb5d6d`, status PASS), Part B — datasets (`evidence/J0_data/datasets.json`, commit `358d0bd`), Part C — gate J0 PASS (`evidence/J0_data/20261003T201012Z.json`, 15 s on the laptop), Results and what they mean (+1 more)

### Community 39 - "retry_resources"
Cohesion: 0.25
Nodes (7): Alternatives considered, Compute: laptop and Perlmutter only, admission-controlled laptop runner, self-healing jobs, Consequences (what must be re-run or re-checked), Decision, Why, retry_resources(), test_retry_rule()

### Community 40 - "Model card — Gauge-JEPA-P v1 (working configuration after M2a)"
Cohesion: 0.22
Nodes (8): 1. What the model is, 2. Working configuration, 3. Training cost, 4. J1 results (validation split, final epoch; `evidence/GATE_LEDGER.md`, `figures/000`, `figures/001`), 5. Forecasting, preliminary (`runs/v1_confirm/forecast_eval.json`, mean of 5 seeds; NOT a J2 result, since J2 is run in M4a), 6. Data and reproducibility, 7. Known limitations, Model card — Gauge-JEPA-P v1 (working configuration after M2a)

### Community 41 - "M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED"
Cohesion: 0.22
Nodes (7): Code graph, M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED, Next action, Problems and assumptions, Results and what they mean, What was asked, test_run_py_retries_after_memory_limit()

### Community 42 - "M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914)"
Cohesion: 0.22
Nodes (8): Laptop check, 10 epochs, 1 seed (`runs/v1_check/seed0/history.json`, local; validation split), M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914), Next action, Options for Digonto (a decision record in `decisions/` is needed for any of B–D, before the 16 Oct preregistration), Problems and assumptions, Results and what they mean, The energy row cannot pass with this encoder (`evidence/J1_training/ceiling_main.json`, validation split, 26,348 rows; training split 126,824 rows; `data/main` `73fff8e5a7b7`), What was asked

### Community 43 - "test_jepa_trains_one_epoch"
Cohesion: 0.56
Nodes (8): Actions taken, Code graph, JEPAConfig, prepare_tensors(), train_jepa(), TrainConfig, test_jepa_ema_target_and_curriculum(), test_jepa_trains_one_epoch()

### Community 44 - "Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`)"
Cohesion: 0.25
Nodes (8): Absolute safety rules (you have no permission prompts), Context, Definition of done, Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`), Phase A — inventory and backup (no changes), Phase B — repair `coding` (only after rule 4 allows it), Phase C — create `su2qc-jepa` (safe to do at any time; it touches no existing environment), Phase D — report

### Community 45 - "Package build: plan audit, Gauge-JEPA-P v2 and the starter package"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Package build: plan audit, Gauge-JEPA-P v2 and the starter package, Problems and assumptions, Results and what they mean, What was asked

### Community 46 - "Conventions update: numbered artifacts and the Graphify code graph"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Conventions update: numbered artifacts and the Graphify code graph, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 47 - "Compute update 2: safe laptop and a pull-based job queue for Perlmutter"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Compute update 2: safe laptop and a pull-based job queue for Perlmutter, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 48 - "Compute update 3: laptop and Perlmutter only, environment repair prompt, self-healing runners"
Cohesion: 0.25
Nodes (8): Actions taken, Bugs found and fixed while doing this, Code graph, Compute update 3: laptop and Perlmutter only, environment repair prompt, self-healing runners, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 49 - "Perlmutter worker install keeps the user's other scrontab entries"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Perlmutter worker install keeps the user's other scrontab entries, Problems and assumptions, Results and what they mean, What was asked

### Community 50 - "test_dynamics_reproduce_preliminary_expectation"
Cohesion: 0.25
Nodes (7): 2.1 Model and Hamiltonian, 2.2 Coupling points, 2.4 Named states and bare energies, 2.5 Dynamics tables (MEASURED; recomputed in this report by `physics_curves.py`, Appendix A, and equal to the plan's quoted numbers), 2.6 Cross-check against the project's independent verified code (M1; `evidence/J0_data/crosscheck_su2qc.json`, status PASS, tolerance $10^{-10}$, commit `0bb5d6d`), 2. Physics, test_dynamics_reproduce_preliminary_expectation()

### Community 52 - "_Cache"
Cohesion: 0.36
Nodes (3): _Cache, _checksum(), _initial_state()

### Community 53 - "named_states"
Cohesion: 0.32
Nodes (4): channel_masks(), named_states(), test_named_state_energies_and_resonance(), setup()

### Community 54 - "{{title}}"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Problems and assumptions, Results and what they mean, {{title}}, What was asked

### Community 55 - "pick_device"
Cohesion: 0.29
Nodes (7): 5. Compute rules (`decisions/004`, `decisions/006`, `configs/compute.yaml`, `docs/PERLMUTTER.md`, `docs/DESKTOP.md`), Decision, Actions taken, 6.1 Compute (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`), 6.2 Repository and conventions, 6. Compute and repository infrastructure, pick_device()

### Community 56 - "os"
Cohesion: 0.48
Nodes (4): _env(), _run(), test_add_to_empty_table_and_remove_last_entry(), test_add_update_remove_keeps_other_entries()

### Community 57 - "M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)"
Cohesion: 0.29
Nodes (6): Expected, M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h), Part A — cross-check against the project's verified `su2qc` code, Part B — datasets, Part C — gate, Tests to add

### Community 58 - "su2qc-jepa — Gauge-JEPA-P v2 starter package"
Cohesion: 0.29
Nodes (6): First two sessions on the laptop, Five-minute tour, Install on the laptop (done by prompts/009), Layout, su2qc-jepa — Gauge-JEPA-P v2 starter package, What is verified today (`python scripts/run.py -- python -m pytest -q`: 47 fast tests; `-m slow` adds 1 more)

### Community 59 - "Compute update: laptop for light work, Perlmutter for heavy jobs"
Cohesion: 0.29
Nodes (6): Code graph, Compute update: laptop for light work, Perlmutter for heavy jobs, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 60 - "M0: repository created, CI green, code graph committed"
Cohesion: 0.29
Nodes (6): Actions taken, Code graph, M0: repository created, CI green, code graph committed, Next action, Problems and assumptions, What was asked

### Community 62 - "Compute: a safe laptop and a pull-based job queue for Perlmutter"
Cohesion: 0.33
Nodes (5): Alternatives considered, Compute: a safe laptop and a pull-based job queue for Perlmutter, Consequences, Decision, Why

### Community 63 - "J1 energy grounding threshold set relative to the measured information ceiling"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences (what must be re-run or re-checked), Decision, J1 energy grounding threshold set relative to the measured information ceiling, Why

### Community 64 - "Preregistration deviation: dataset-equivalence tolerance corrected to rounding scale"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences, Decision, Preregistration deviation: dataset-equivalence tolerance corrected to rounding scale, Why

### Community 65 - "Heavy jobs on the desktop GPU (RTX 3070) — setup and daily use"
Cohesion: 0.33
Nodes (5): Daily use, From the laptop, Heavy jobs on the desktop GPU (RTX 3070) — setup and daily use, One-time setup (on the desktop, Linux, about 20 minutes), Troubleshooting (on the desktop)

### Community 66 - "Heavy jobs: the job queue and the Perlmutter worker"
Cohesion: 0.33
Nodes (5): Costs and limits, Heavy jobs: the job queue and the Perlmutter worker, One-time setup (Digonto, about 30 minutes, after the repository exists on GitHub), Self-healing, When something is wrong

### Community 67 - "M0 — Bootstrap (first Claude Code invocation, ~45 min)"
Cohesion: 0.33
Nodes (5): Context, Definition of done, M0 — Bootstrap (first Claude Code invocation, ~45 min), Out of scope, Tasks

### Community 68 - "M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card"
Cohesion: 0.33
Nodes (5): Context, Definition of done, M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card, Out of scope / stop conditions, Tasks

### Community 69 - "Results and what they mean"
Cohesion: 0.33
Nodes (6): `coding`: imports before and after (`import-before.json` → `import-after.json`), Disk, `pip check`, Results and what they mean, `su2qc-jepa` environment, The GTX 1060 (compute capability 6.1, driver 580.178.04, CUDA 13.0 driver API)

### Community 70 - "7. Chronological history (every session so far, with the numbers)"
Cohesion: 0.33
Nodes (6): 7.1 Before the repository existed (1–2 Oct; planner sessions; reports 000–005), 7.2 Environment and M0 (2 Oct; reports 006–008), 7.3 M1 — physics cross-check, datasets, gate J0 (3–4 Oct; `reports/009`) — J0 PASS (9 of 9 rows), 7.4 M2a — model health (5 Oct; `reports/010`, `decisions/005`), 7.6 Parameter count, 7. Chronological history (every session so far, with the numbers)

### Community 72 - "{{title}}"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences (what must be re-run or re-checked), Decision, {{title}}, Why

### Community 73 - "{{title}}"
Cohesion: 0.33
Nodes (5): Context, Definition of done, Out of scope / stop conditions, Tasks, {{title}}

### Community 75 - "Numbered artifacts and the Graphify code graph"
Cohesion: 0.40
Nodes (4): Alternatives considered, Consequences, Numbered artifacts and the Graphify code graph, Why

### Community 76 - "Compute: laptop for light work, Perlmutter for heavy jobs"
Cohesion: 0.40
Nodes (4): Alternatives considered, Compute: laptop for light work, Perlmutter for heavy jobs, Consequences, Why

### Community 77 - "M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)"
Cohesion: 0.40
Nodes (4): Expected, M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions), Session M2a — make the model healthy, Session M2b — preregistration (16 Oct)

### Community 78 - "M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)"
Cohesion: 0.40
Nodes (4): Expected, M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions), Session M3a — forecasting, Session M3b — twin and dry run

### Community 79 - "M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version."
Cohesion: 0.40
Nodes (4): Expected, M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version., Session M4a — J2 (30 Oct), Session M4b — pilot (one job)

### Community 83 - "10. Decisions log and problems/risks"
Cohesion: 0.50
Nodes (4): 10.1 Decisions (`decisions/INDEX.md`), 10.2 Problems and risks, 10.3 Disagreements between sources that I noticed, 10. Decisions log and problems/risks

## Knowledge Gaps
- **327 isolated node(s):** `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script`, `PYTHONHASHSEED`, `replicate.sh script` (+322 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 596 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **39 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PlaquetteModel` connect `PlaquetteModel` to `run_j0`, `ObservableSet`, `trajectories.py`, `test_pipeline.py`, `Conventions update: numbered artifacts and the Graphify code graph`, `LinkSpace`, `._apply_term`, `_Cache`, `named_states`, `.full_space_vectors`, `pick_device`, `test_physics.py`, `compare_point`, `generate_dataset`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Why does `Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)` connect `Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)` to `9. Plot data (the data behind every figure; each table can be parsed as Markdown)`, `7. Chronological history (every session so far, with the numbers)`, `reports/INDEX.md`, `test_dynamics_reproduce_preliminary_expectation`, `10. Decisions log and problems/risks`, `pick_device`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `PlaquetteModel` (e.g. with `Code graph` and `6.2 Repository and conventions`) actually correct?**
  _`PlaquetteModel` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `generate_dataset()` (e.g. with `Code graph` and `ObservableSet`) actually correct?**
  _`generate_dataset()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script` to the rest of the system?**
  _327 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier` be split into smaller, more focused modules?**
  _Cohesion score 0.04343971631205674 - nodes in this community are weakly interconnected._
- **Should `pathlib` be split into smaller, more focused modules?**
  _Cohesion score 0.0797979797979798 - nodes in this community are weakly interconnected._