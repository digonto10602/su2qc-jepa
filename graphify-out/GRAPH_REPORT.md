# Graph Report - su2qc-jepa  (2026-10-15)

## Corpus Check
- 122 files · ~122,222 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 3, .cff 1)

## Summary
- 1108 nodes · 2014 edges · 102 communities (63 shown, 39 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 147 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5119b7af`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- artifacts.py
- trajectories.py
- chain.py
- Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier
- 9. Plot data (the data behind every figure; each table can be parsed as Markdown)
- ibm.py
- Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)
- j0_data.py
- test_pipeline.py
- Worker
- retry_resources
- FullSpaceOperators
- test_jobs.py
- test_physics.py
- PlaquetteModel
- generate_dataset
- dynamics.py
- train.py
- LinkSpace
- test_crosscheck.py
- crosscheck_su2qc.py
- localrun.py
- test_localrun.py
- su2.py
- os
- GaugeJEPA
- test_committed_graph_is_fresh
- M2a closed: J1 FAIL after 14 configurations (semigroup row on a fresh seed); working model $w_{\text{sigreg}}=3$, $w_{\text{semigroup}}=10$
- decisions/INDEX.md
- M1: su2qc cross-check PASS, three datasets built, gate J0 PASS
- Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)
- Numbered artifacts and the Graphify code graph
- scripts/run.py
- prompts/INDEX.md
- M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED
- 11. What happens next
- CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`
- Model card — Gauge-JEPA-P v1 (working configuration after M2a)
- M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914)
- test_jepa_trains_one_epoch
- .__init__
- Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`)
- Package build: plan audit, Gauge-JEPA-P v2 and the starter package
- Conventions update: numbered artifacts and the Graphify code graph
- Compute update 2: safe laptop and a pull-based job queue for Perlmutter
- Perlmutter worker install keeps the user's other scrontab entries
- {{title}}
- M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)
- su2qc-jepa — Gauge-JEPA-P v2 starter package
- Compute update: laptop for light work, Perlmutter for heavy jobs
- 2. Physics
- 7. Chronological history (every session so far, with the numbers)
- 8. Current results in full
- _Cache
- .seeds
- pick_device
- J1 energy grounding threshold set relative to the measured information ceiling
- M0 — Bootstrap (first Claude Code invocation, ~45 min)
- M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card
- Results and what they mean
- M0: repository created, CI green, code graph committed
- 4. The world model (JEPA)
- 5. Data, twin, hardware plan, gates, hypotheses, error budget
- ._apply_term
- heron_like_noise_model
- {{title}}
- {{title}}
- Compute: laptop for light work, Perlmutter for heavy jobs
- M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)
- M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)
- M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version.
- reports/INDEX.md
- Appendix A — helper scripts (verbatim; run with `python scripts/run.py --no-queue --threads 1 -- python <script> <out.md>` from the repository root)
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
- install_perlmutter.sh
- scrontab_merge.sh
- setup_env_perlmutter.sh
- test_jmax1_counts
- plan.md
- model
- su2qc-jepa

## God Nodes (most connected - your core abstractions)
1. `PlaquetteModel` - 43 edges
2. `run_j0()` - 24 edges
3. `generate_dataset()` - 23 edges
4. `Worker` - 21 edges
5. `test_training_and_baselines_run_on_device()` - 20 edges
6. `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier` - 20 edges
7. `ObservableSet` - 19 edges
8. `Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)` - 19 edges
9. `Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)` - 17 edges
10. `9. Plot data (the data behind every figure; each table can be parsed as Markdown)` - 17 edges

## Surprising Connections (you probably didn't know these)
- `Problems and assumptions` --references--> `estimate_minutes()`  [INFERRED]
  reports/009_m1-su2qc-cross-check-pass-three-datasets-built-gate-j0-pass.md → src/su2qc_jepa/localrun.py
- `9.4 Error budget (lines, each to be measured)` --references--> `trotter_error()`  [INFERRED]
  reports/011_project-overview-gauge-jepa-p-v2-plan-physics-status-and-eve.md → src/su2qc_jepa/physics/chain.py
- `Code graph` --references--> `PlaquetteModel`  [INFERRED]
  reports/001_conventions-update-numbered-artifacts-and-the-graphify-code.md → src/su2qc_jepa/physics/plaquette.py
- `Actions taken` --references--> `check_artifacts()`  [INFERRED]
  reports/003_compute-update-2-safe-laptop-and-a-pull-based-job-queue-for.md → src/su2qc_jepa/repo/artifacts.py
- `Bugs found and fixed while doing this` --references--> `check_artifacts()`  [INFERRED]
  reports/004_compute-update-3-laptop-and-perlmutter-only-environment-repa.md → src/su2qc_jepa/repo/artifacts.py

## Import Cycles
- None detected.

## Communities (102 total, 39 thin omitted)

### Community 0 - "artifacts.py"
Cohesion: 0.08
Nodes (32): 0. What was already known when this was written (disclosure), 1. Hypotheses (thresholds are those of `configs/gates.yaml`, frozen below), 2. Frozen inputs, 3. Analysis plan (exact commands; every computation through `scripts/run.py`), 4. Exclusion and handling rules, 5. Known open items (not part of the frozen record), 6. Signatures, Preregistration — Gauge-JEPA-P v2 (signed by tag `prereg-2026-10-16`) (+24 more)

### Community 2 - "chain.py"
Cohesion: 0.08
Nodes (22): 12. Error budget (lines, each measured), Results and what they mean, 5.6 Error budget (lines, each to be measured; plan §12), _bond_rotation(), build_chain_circuit(), z_layer(), build_chain_prep_circuit(), chain_amplitudes() (+14 more)

### Community 3 - "Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier"
Cohesion: 0.05
Nodes (35): Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code), Model, Observables, Predicted results, Problems and assumptions, Publishability, Schedule (5 Oct – 29 Nov 2026), Testing ladder (budgets are Claude's estimates) (+27 more)

### Community 4 - "9. Plot data (the data behind every figure; each table can be parsed as Markdown)"
Cohesion: 0.06
Nodes (35): 9.1 Catalogue of plots, 9.2 P11 sub-plots (physics curves and carrier costs), 9. Plot data (the data behind every figure; each table can be parsed as Markdown), Dataset reproducibility (evidence/J0_data/fingerprint_compare_*.json; per-trajectory-sum tolerance 1e-12), Further machine-readable tables (P10, P11e, P11f, J1 records, jobs, dataset reproducibility), J1 gate records (evidence/J1_training/*.json), Job table (jobs/*.yaml and evidence/jobs/NNN/status.json; states read on 2026-10-06 by scripts/jobs/status.py), P10 table: R2 ceilings from one clean observation (validation split, 26,348 rows; evidence/J1_training/ceiling_main.json) (+27 more)

### Community 5 - "ibm.py"
Cohesion: 0.09
Nodes (14): W4 (26 Oct – 1 Nov) — J2, pilot job; end of the one-month version, BudgetError, calibration_snapshot(), check_budget(), collect(), dry_run(), DryRunSummary, estimate_qpu_seconds() (+6 more)

### Community 6 - "Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)"
Cohesion: 0.07
Nodes (30): 0. How to read this document, 10.1 Before the repository existed (1–2 Oct, planner sessions; reports 000–005), 10.2 Environment and M0 (2 Oct; reports 006–008), 10.3 M1 — physics cross-check, datasets, gate J0 (3–4 Oct; `reports/009`) — **J0 PASS 9/9**, 10.4 M2a — model health (5 Oct; `reports/010`, `decisions/005`, and results fetched at 21:30 UTC), 10. What has been done, session by session (with every number), 11. Infrastructure and repository conventions (how the work is done), 12. Open problems and risks (as of 5 Oct, 21:40 UTC) (+22 more)

### Community 7 - "j0_data.py"
Cohesion: 0.12
Nodes (14): estimate(), subsample(), _bits_from_key(), estimate_chain(), estimate_diagonal(), ObservationSpec, Record, sample_exact_chain() (+6 more)

### Community 8 - "test_pipeline.py"
Cohesion: 0.13
Nodes (13): run_j1(), run_j2(), auroc(), run_j3(), spearman(), _fmt(), GateResult, GateRow (+5 more)

### Community 9 - "Worker"
Cohesion: 0.18
Nodes (5): hms_to_hours(), main(), now(), sh(), Worker

### Community 10 - "retry_resources"
Cohesion: 0.08
Nodes (25): Alternatives considered, Compute: laptop and Perlmutter only, admission-controlled laptop runner, self-healing jobs, Consequences (what must be re-run or re-checked), Decision, Why, Costs and limits, Heavy jobs: the job queue and the Perlmutter worker, One-time setup (Digonto, about 30 minutes, after the repository exists on GitHub) (+17 more)

### Community 12 - "test_jobs.py"
Cohesion: 0.11
Nodes (10): parse_steps(), validate_job(), _git(), good_job(), test_allowlist_refuses(), test_valid_job_passes(), test_validation_catches_bad_fields(), test_worker_end_to_end_local() (+2 more)

### Community 13 - "test_physics.py"
Cohesion: 0.14
Nodes (12): Claims ledger — every substantive statement, its status and its evidence, sector_restrict(), channel_masks(), named_states(), ObservableSet, test_chain_prep_cascade(), test_channel_split(), test_dynamics_reproduce_preliminary_expectation() (+4 more)

### Community 15 - "generate_dataset"
Cohesion: 0.21
Nodes (12): Code graph, load(), _checksum(), dataset_fingerprint(), DatasetConfig, FamilyConfig, generate_dataset(), load_dataset() (+4 more)

### Community 16 - "dynamics.py"
Cohesion: 0.18
Nodes (5): krylov(), evolve(), Krylov, krylov_error(), lanczos()

### Community 17 - "train.py"
Cohesion: 0.21
Nodes (9): effective_rank(), baseline_ridge(), baseline_supervised_mlp(), diagnostics(), fit_probe(), _flat_inputs(), forecast_jepa(), _ground_targets() (+1 more)

### Community 18 - "LinkSpace"
Cohesion: 0.15
Nodes (3): LinkSpace, m_values(), spin_matrices()

### Community 20 - "crosscheck_su2qc.py"
Cohesion: 0.17
Nodes (7): compare_point(), extract_terms(), import_su2qc(), main(), sign_gauge(), su2qc_label_to_c(), Couplings

### Community 22 - "localrun.py"
Cohesion: 0.20
Nodes (9): _arg(), estimate_minutes(), ledger_append(), _limit_env(), load_policy(), _manifest_ntrain(), _preexec(), run_capped() (+1 more)

### Community 23 - "test_localrun.py"
Cohesion: 0.27
Nodes (12): admit(), classify(), heal_decision(), is_heavy(), is_resource_failure(), Policy, Probe, Request (+4 more)

### Community 25 - "su2.py"
Cohesion: 0.19
Nodes (3): _cg_cached(), clebsch_gordan(), _fact()

### Community 26 - "os"
Cohesion: 0.21
Nodes (6): estimate_hours(), load_compute(), _env(), _run(), test_add_to_empty_table_and_remove_last_entry(), test_add_update_remove_keeps_other_entries()

### Community 28 - "test_committed_graph_is_fresh"
Cohesion: 0.18
Nodes (8): Actions taken, Code graph, Laptop environments: coding repaired, su2qc-jepa created, Next action, Problems and assumptions, What was asked, Actions taken, test_committed_graph_is_fresh()

### Community 29 - "M2a closed: J1 FAIL after 14 configurations (semigroup row on a fresh seed); working model $w_{\text{sigreg}}=3$, $w_{\text{semigroup}}=10$"
Cohesion: 0.17
Nodes (11): Actions taken, Cost, Dataset reproducibility (`evidence/J0_data/fingerprint_compare_*.json`), Forecasting, preliminary (`runs/v1_confirm/forecast_eval.json`; not a J2 result), J1 (validation split, final epoch; every row is in `evidence/GATE_LEDGER.md`), M2a closed: J1 FAIL after 14 configurations (semigroup row on a fresh seed); working model $w_{\text{sigreg}}=3$, $w_{\text{semigroup}}=10$, Next action, Problems and assumptions (+3 more)

### Community 30 - "decisions/INDEX.md"
Cohesion: 0.18
Nodes (7): Frozen conventions and coupling points, Alternatives considered, Compute: a safe laptop and a pull-based job queue for Perlmutter, Consequences, Decision, Why, Decisions — index

### Community 31 - "M1: su2qc cross-check PASS, three datasets built, gate J0 PASS"
Cohesion: 0.18
Nodes (10): Actions taken, Code graph, M1: su2qc cross-check PASS, three datasets built, gate J0 PASS, Next action, Part A — route C agrees with both su2qc routes (`evidence/J0_data/crosscheck_su2qc.json`, commit `0bb5d6d`, status PASS), Part B — datasets (`evidence/J0_data/datasets.json`, commit `358d0bd`), Part C — gate J0 PASS (`evidence/J0_data/20261003T201012Z.json`, 15 s on the laptop), Problems and assumptions (+2 more)

### Community 32 - "Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)"
Cohesion: 0.18
Nodes (11): 0.1 How to read this document, 0.2 Glossary (every technical term used), 0. Reading guide and glossary, 12. Code graph, problems and assumptions of this report, next action, 1. Project goal, scope, allowed and forbidden claims, 3. The Krylov-chain (KC) hardware carrier *(label)*, Actions taken (for this report), Appendix B — file map (where things are) (+3 more)

### Community 33 - "Numbered artifacts and the Graphify code graph"
Cohesion: 0.22
Nodes (8): 2. Session protocol (every session, no exceptions), Alternatives considered, Consequences, Decision, Numbered artifacts and the Graphify code graph, Why, 15. Repository conventions — numbered artifacts and the code graph (added 2 Oct 2026; `decisions/001`), series()

### Community 34 - "scripts/run.py"
Cohesion: 0.24
Nodes (5): 9.0 How to use this section, dataset_step(), guess_outputs(), val(), queue()

### Community 35 - "prompts/INDEX.md"
Cohesion: 0.20
Nodes (5): Expected, M6 — Hardware day 3, gate J3, error budget (W6, 2 sessions), M7 — One stretch item (W7), chosen on 15 Nov by Digonto, M8 — Paper assembly, release, replication (W8, 2 sessions), Prompts — index

### Community 36 - "M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED"
Cohesion: 0.20
Nodes (8): Actions taken, Code graph, M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED, Next action, Problems and assumptions, Results and what they mean, What was asked, test_run_py_retries_after_memory_limit()

### Community 37 - "11. What happens next"
Cohesion: 0.20
Nodes (10): 11.1 The rest of M2 (M2a continuation, `prompts/010`), 11.2 M2b — preregistration (16 Oct; `prompts/002` items 6–8), 11.3 M3 (W3, 19–25 Oct; `prompts/003`): forecasting, calibrated twin, dry run, 11.4 M4 (W4, 26 Oct – 1 Nov; `prompts/004`): J2 and the pilot (end of the one-month version), 11.5 M5 (W5, 2–8 Nov; `prompts/005`): hardware days 1 and 2, 11.6 M6 (W6, 9–15 Nov; `prompts/006`): day 3, J3, error budget, 11.7 M7 (W7, 16–22 Nov; `prompts/007`): one stretch item, chosen 15 Nov by Digonto, 11.8 M8 (W8, 23–29 Nov; `prompts/008`): paper, release, replication (+2 more)

### Community 38 - "CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`"
Cohesion: 0.22
Nodes (8): 1. Priorities, in order, 3. Frozen things (changing any of these needs a new `decisions/` record and a new version tag), 4. Hardware rules (non-negotiable), 6. Writing rules (reports, prompts, docs, paper), 7. What the package already guarantees (do not re-derive, do re-run), 8. Where things are, CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`, graphify

### Community 39 - "Model card — Gauge-JEPA-P v1 (working configuration after M2a)"
Cohesion: 0.22
Nodes (8): 1. What the model is, 2. Working configuration, 3. Training cost, 4. J1 results (validation split, final epoch; `evidence/GATE_LEDGER.md`, `figures/000`, `figures/001`), 5. Forecasting, preliminary (`runs/v1_confirm/forecast_eval.json`, mean of 5 seeds; NOT a J2 result, since J2 is run in M4a), 6. Data and reproducibility, 7. Known limitations, Model card — Gauge-JEPA-P v1 (working configuration after M2a)

### Community 40 - "M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914)"
Cohesion: 0.22
Nodes (8): Laptop check, 10 epochs, 1 seed (`runs/v1_check/seed0/history.json`, local; validation split), M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914), Next action, Options for Digonto (a decision record in `decisions/` is needed for any of B–D, before the 16 Oct preregistration), Problems and assumptions, Results and what they mean, The energy row cannot pass with this encoder (`evidence/J1_training/ceiling_main.json`, validation split, 26,348 rows; training split 126,824 rows; `data/main` `73fff8e5a7b7`), What was asked

### Community 41 - "test_jepa_trains_one_epoch"
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

### Community 48 - "Perlmutter worker install keeps the user's other scrontab entries"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Perlmutter worker install keeps the user's other scrontab entries, Problems and assumptions, Results and what they mean, What was asked

### Community 51 - "{{title}}"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Problems and assumptions, Results and what they mean, {{title}}, What was asked

### Community 52 - "M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)"
Cohesion: 0.29
Nodes (6): Expected, M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h), Part A — cross-check against the project's verified `su2qc` code, Part B — datasets, Part C — gate, Tests to add

### Community 53 - "su2qc-jepa — Gauge-JEPA-P v2 starter package"
Cohesion: 0.29
Nodes (6): First two sessions on the laptop, Five-minute tour, Install on the laptop (done by prompts/009), Layout, su2qc-jepa — Gauge-JEPA-P v2 starter package, What is verified today (`python scripts/run.py -- python -m pytest -q`: 47 fast tests; `-m slow` adds 1 more)

### Community 54 - "Compute update: laptop for light work, Perlmutter for heavy jobs"
Cohesion: 0.29
Nodes (6): Code graph, Compute update: laptop for light work, Perlmutter for heavy jobs, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 55 - "2. Physics"
Cohesion: 0.29
Nodes (7): 2.1 Model and Hamiltonian, 2.2 Coupling points, 2.3 Verified fingerprints (PROVEN by tests or MEASURED), 2.4 Named states and bare energies, 2.5 Dynamics tables (MEASURED; recomputed in this report by `physics_curves.py`, Appendix A, and equal to the plan's quoted numbers), 2.6 Cross-check against the project's independent verified code (M1; `evidence/J0_data/crosscheck_su2qc.json`, status PASS, tolerance $10^{-10}$, commit `0bb5d6d`), 2. Physics

### Community 56 - "7. Chronological history (every session so far, with the numbers)"
Cohesion: 0.29
Nodes (7): 7.1 Before the repository existed (1–2 Oct; planner sessions; reports 000–005), 7.2 Environment and M0 (2 Oct; reports 006–008), 7.3 M1 — physics cross-check, datasets, gate J0 (3–4 Oct; `reports/009`) — J0 PASS (9 of 9 rows), 7.4 M2a — model health (5 Oct; `reports/010`, `decisions/005`), 7.5 The 5 Oct evening and 6 Oct session (this report adds these), 7.6 Parameter count, 7. Chronological history (every session so far, with the numbers)

### Community 57 - "8. Current results in full"
Cohesion: 0.29
Nodes (7): 8.1 J0 (data gate): PASS, 9 of 9 rows (`evidence/J0_data/20261003T201012Z.json`, `evidence/GATE_LEDGER.md`), 8.2 Energy ceiling (J1 input; `evidence/J1_training/ceiling_main.json`, commit `63065dd`, 2026-10-05T17:31Z; `data/main` `73fff8e5a7b7`; training split 126,824 rows, validation split 26,348 rows; regressor seeds 462709266, 3658436304), 8.3 J1 (training gate) for the six gated rungs (official gate runs; `evidence/GATE_LEDGER.md` rows; records in `evidence/J1_training/`), 8.4 Dataset reproducibility (laptop versus Perlmutter; `evidence/J0_data/fingerprint_compare_*.json`, commit `3010090`, 2026-10-05T23:47Z), 8.5 GPU-fix verification and the job table, 8.6 Forecast results so far, 8. Current results in full

### Community 60 - "pick_device"
Cohesion: 0.33
Nodes (6): Decision, Actions taken, 6.1 Compute (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`), 6.2 Repository and conventions, 6. Compute and repository infrastructure, pick_device()

### Community 61 - "J1 energy grounding threshold set relative to the measured information ceiling"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences (what must be re-run or re-checked), Decision, J1 energy grounding threshold set relative to the measured information ceiling, Why

### Community 62 - "M0 — Bootstrap (first Claude Code invocation, ~45 min)"
Cohesion: 0.33
Nodes (5): Context, Definition of done, M0 — Bootstrap (first Claude Code invocation, ~45 min), Out of scope, Tasks

### Community 63 - "M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card"
Cohesion: 0.33
Nodes (5): Context, Definition of done, M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card, Out of scope / stop conditions, Tasks

### Community 64 - "Results and what they mean"
Cohesion: 0.33
Nodes (6): `coding`: imports before and after (`import-before.json` → `import-after.json`), Disk, `pip check`, Results and what they mean, `su2qc-jepa` environment, The GTX 1060 (compute capability 6.1, driver 580.178.04, CUDA 13.0 driver API)

### Community 65 - "M0: repository created, CI green, code graph committed"
Cohesion: 0.33
Nodes (5): Code graph, M0: repository created, CI green, code graph committed, Next action, Problems and assumptions, What was asked

### Community 66 - "4. The world model (JEPA)"
Cohesion: 0.33
Nodes (6): 4.1 Observation, actions, training rule, 4.2 Architecture (`src/su2qc_jepa/models/jepa.py`), 4.3 Losses, 4.4 Baselines, tasks, 4. The world model (JEPA), eff_rank()

### Community 67 - "5. Data, twin, hardware plan, gates, hypotheses, error budget"
Cohesion: 0.33
Nodes (6): 5.1 Data (`evidence/J0_data/datasets.json`, commit `358d0bd`; checksums are sha256 of the data arrays, first 12 hex digits shown), 5.2 The digital twin, 5.3 Hardware plan and rules (nothing submitted), 5.4 Gates (current thresholds, `configs/gates.yaml`), 5.5 Preregistered hypotheses H1–H5 (plan §11, `docs/PREREGISTRATION.md` draft), 5. Data, twin, hardware plan, gates, hypotheses, error budget

### Community 69 - "heron_like_noise_model"
Cohesion: 0.33
Nodes (3): heron_like_noise_model(), HeronLike, save_noise_summary()

### Community 70 - "{{title}}"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences (what must be re-run or re-checked), Decision, {{title}}, Why

### Community 71 - "{{title}}"
Cohesion: 0.33
Nodes (5): Context, Definition of done, Out of scope / stop conditions, Tasks, {{title}}

### Community 72 - "Compute: laptop for light work, Perlmutter for heavy jobs"
Cohesion: 0.40
Nodes (4): Alternatives considered, Compute: laptop for light work, Perlmutter for heavy jobs, Consequences, Why

### Community 73 - "M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)"
Cohesion: 0.40
Nodes (4): Expected, M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions), Session M2a — make the model healthy, Session M2b — preregistration (16 Oct)

### Community 74 - "M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)"
Cohesion: 0.40
Nodes (4): Expected, M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions), Session M3a — forecasting, Session M3b — twin and dry run

### Community 75 - "M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version."
Cohesion: 0.40
Nodes (4): Expected, M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version., Session M4a — J2 (30 Oct), Session M4b — pilot (one job)

### Community 77 - "Appendix A — helper scripts (verbatim; run with `python scripts/run.py --no-queue --threads 1 -- python <script> <out.md>` from the repository root)"
Cohesion: 0.50
Nodes (4): A.1 plot_tables.py (plots P1 to P9, P12), A.2 physics_curves.py (plot P11a to P11d), A.3 evidence_tables.py (P10, P11e, P11f, job and reproducibility tables), Appendix A — helper scripts (verbatim; run with `python scripts/run.py --no-queue --threads 1 -- python <script> <out.md>` from the repository root)

## Knowledge Gaps
- **301 isolated node(s):** `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script`, `PYTHONHASHSEED`, `replicate.sh script` (+296 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 559 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **39 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)` connect `Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)` to `4. The world model (JEPA)`, `5. Data, twin, hardware plan, gates, hypotheses, error budget`, `9. Plot data (the data behind every figure; each table can be parsed as Markdown)`, `11. What happens next`, `retry_resources`, `reports/INDEX.md`, `Appendix A — helper scripts (verbatim; run with `python scripts/run.py --no-queue --threads 1 -- python <script> <out.md>` from the repository root)`, `2. Physics`, `7. Chronological history (every session so far, with the numbers)`, `8. Current results in full`, `pick_device`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Why does `PlaquetteModel` connect `PlaquetteModel` to `trajectories.py`, `._apply_term`, `j0_data.py`, `test_physics.py`, `Conventions update: numbered artifacts and the Graphify code graph`, `generate_dataset`, `._reorder_matter`, `LinkSpace`, `crosscheck_su2qc.py`, `_Cache`, `test_jmax1_counts`, `pick_device`, `model`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Why does `trotter_error()` connect `chain.py` to `dynamics.py`, `Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `PlaquetteModel` (e.g. with `Code graph` and `6.2 Repository and conventions`) actually correct?**
  _`PlaquetteModel` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `run_j0()` (e.g. with `ChainSpec` and `ObservableSet`) actually correct?**
  _`run_j0()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `generate_dataset()` (e.g. with `Code graph` and `ObservableSet`) actually correct?**
  _`generate_dataset()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script` to the rest of the system?**
  _301 weakly-connected nodes found - possible documentation gaps or missing edges._