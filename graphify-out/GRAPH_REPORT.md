# Graph Report - su2qc-jepa  (2026-10-05)

## Corpus Check
- 118 files · ~82,330 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 3, .cff 1)

## Summary
- 976 nodes · 1853 edges · 93 communities (56 shown, 37 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 125 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ade81b09`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- artifacts.py
- Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier
- ledger.py
- Worker
- Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)
- ibm.py
- j0_data.py
- PlaquetteModel
- retry_resources
- run_j0
- chain.py
- dynamics.py
- test_physics.py
- generate_dataset
- train.py
- train_jepa.py
- LinkSpace
- test_jobs.py
- localrun.py
- jepa.py
- heal_decision
- GaugeJEPA
- FullSpaceOperators
- test_committed_graph_is_fresh
- MatterSpace
- su2.py
- M1: su2qc cross-check PASS, three datasets built, gate J0 PASS
- crosscheck_su2qc.py
- decisions/INDEX.md
- prompts/INDEX.md
- ObservableSet
- CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`
- M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED
- M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914)
- test_jepa_trains_one_epoch
- ._apply_term
- Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`)
- Package build: plan audit, Gauge-JEPA-P v2 and the starter package
- Conventions update: numbered artifacts and the Graphify code graph
- Compute update 2: safe laptop and a pull-based job queue for Perlmutter
- Perlmutter worker install keeps the user's other scrontab entries
- test_worker_slurm_mode_resubmits_after_timeout
- residual_eval.py
- scripts/run.py
- {{title}}
- .seeds
- Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`)
- os
- M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)
- su2qc-jepa — Gauge-JEPA-P v2 starter package
- Compute update: laptop for light work, Perlmutter for heavy jobs
- _Cache
- Compute: a safe laptop and a pull-based job queue for Perlmutter
- J1 energy grounding threshold set relative to the measured information ceiling
- M0 — Bootstrap (first Claude Code invocation, ~45 min)
- M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card
- Results and what they mean
- M0: repository created, CI green, code graph committed
- {{title}}
- {{title}}
- .status
- Compute: laptop for light work, Perlmutter for heavy jobs
- M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)
- M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)
- M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version.
- test_localrun.py
- reports/INDEX.md
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
- install_perlmutter.sh
- scrontab_merge.sh
- setup_env_perlmutter.sh
- plan.md
- su2qc-jepa

## God Nodes (most connected - your core abstractions)
1. `PlaquetteModel` - 42 edges
2. `run_j0()` - 24 edges
3. `generate_dataset()` - 22 edges
4. `Worker` - 21 edges
5. `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier` - 20 edges
6. `ObservableSet` - 19 edges
7. `test_training_and_baselines_run_on_device()` - 17 edges
8. `Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)` - 17 edges
9. `ChainSpec` - 16 edges
10. `GaugeJEPA` - 15 edges

## Surprising Connections (you probably didn't know these)
- `Problems and assumptions` --references--> `estimate_minutes()`  [INFERRED]
  reports/009_m1-su2qc-cross-check-pass-three-datasets-built-gate-j0-pass.md → src/su2qc_jepa/localrun.py
- `12. Error budget (lines, each measured)` --references--> `trotter_error()`  [INFERRED]
  plans/001_gauge-jepa-p-v2.md → src/su2qc_jepa/physics/chain.py
- `9.4 Error budget (lines, each to be measured)` --references--> `trotter_error()`  [INFERRED]
  reports/011_project-overview-gauge-jepa-p-v2-plan-physics-status-and-eve.md → src/su2qc_jepa/physics/chain.py
- `Code graph` --references--> `PlaquetteModel`  [INFERRED]
  reports/001_conventions-update-numbered-artifacts-and-the-graphify-code.md → src/su2qc_jepa/physics/plaquette.py
- `Actions taken` --references--> `check_artifacts()`  [INFERRED]
  reports/003_compute-update-2-safe-laptop-and-a-pull-based-job-queue-for.md → src/su2qc_jepa/repo/artifacts.py

## Import Cycles
- None detected.

## Communities (93 total, 37 thin omitted)

### Community 0 - "artifacts.py"
Cohesion: 0.06
Nodes (25): Artifact, check_artifacts(), list_artifacts(), new_artifact(), next_number(), read_front_matter(), render_index(), _resolve() (+17 more)

### Community 1 - "Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier"
Cohesion: 0.05
Nodes (36): Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code), Model, Observables, Predicted results, Problems and assumptions, Publishability, Schedule (5 Oct – 29 Nov 2026), Testing ladder (budgets are Claude's estimates) (+28 more)

### Community 2 - "ledger.py"
Cohesion: 0.10
Nodes (16): run_j1(), run_j2(), auroc(), run_j3(), spearman(), _fmt(), GateResult, GateRow (+8 more)

### Community 3 - "Worker"
Cohesion: 0.17
Nodes (5): hms_to_hours(), main(), now(), sh(), Worker

### Community 4 - "Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)"
Cohesion: 0.07
Nodes (30): 0. How to read this document, 10.1 Before the repository existed (1–2 Oct, planner sessions; reports 000–005), 10.2 Environment and M0 (2 Oct; reports 006–008), 10.3 M1 — physics cross-check, datasets, gate J0 (3–4 Oct; `reports/009`) — **J0 PASS 9/9**, 10.4 M2a — model health (5 Oct; `reports/010`, `decisions/005`, and results fetched at 21:30 UTC), 10. What has been done, session by session (with every number), 11. Infrastructure and repository conventions (how the work is done), 12. Open problems and risks (as of 5 Oct, 21:40 UTC) (+22 more)

### Community 5 - "ibm.py"
Cohesion: 0.10
Nodes (14): W4 (26 Oct – 1 Nov) — J2, pilot job; end of the one-month version, BudgetError, calibration_snapshot(), check_budget(), collect(), dry_run(), DryRunSummary, estimate_qpu_seconds() (+6 more)

### Community 6 - "j0_data.py"
Cohesion: 0.14
Nodes (10): _bits_from_key(), estimate_chain(), estimate_diagonal(), ObservationSpec, Record, sample_exact_chain(), sample_exact_diagonal(), chain_point_records() (+2 more)

### Community 8 - "retry_resources"
Cohesion: 0.09
Nodes (21): Alternatives considered, Compute: laptop and Perlmutter only, admission-controlled laptop runner, self-healing jobs, Consequences (what must be re-run or re-checked), Decision, Why, Costs and limits, Heavy jobs: the job queue and the Perlmutter worker, One-time setup (Digonto, about 30 minutes, after the repository exists on GitHub) (+13 more)

### Community 9 - "run_j0"
Cohesion: 0.13
Nodes (11): run_j0(), build_chain_circuit(), z_layer(), ChainSpec, cz_count(), trotter_error(), twin_variance_check(), TwinRunner (+3 more)

### Community 10 - "chain.py"
Cohesion: 0.15
Nodes (11): _bond_rotation(), build_chain_prep_circuit(), chain_amplitudes(), chain_sector_unitary(), _layer(), _phase_weights(), prep_cascade_params(), sample_x_basis() (+3 more)

### Community 11 - "dynamics.py"
Cohesion: 0.16
Nodes (8): compare_point(), evolve(), Krylov, krylov_error(), lanczos(), sector_restrict(), test_krylov_dimension_window_PA(), setup()

### Community 13 - "test_physics.py"
Cohesion: 0.12
Nodes (10): Claims ledger — every substantive statement, its status and its evidence, channel_masks(), named_states(), model(), test_chain_prep_cascade(), test_channel_split(), test_dynamics_reproduce_preliminary_expectation(), test_jmax1_counts() (+2 more)

### Community 14 - "generate_dataset"
Cohesion: 0.22
Nodes (11): load(), _checksum(), dataset_fingerprint(), DatasetConfig, FamilyConfig, generate_dataset(), load_dataset(), test_chain_dataset_uses_chain_carrier() (+3 more)

### Community 15 - "train.py"
Cohesion: 0.21
Nodes (9): effective_rank(), baseline_ridge(), baseline_supervised_mlp(), diagnostics(), fit_probe(), _flat_inputs(), forecast_jepa(), _ground_targets() (+1 more)

### Community 18 - "LinkSpace"
Cohesion: 0.14
Nodes (3): LinkSpace, m_values(), spin_matrices()

### Community 19 - "test_jobs.py"
Cohesion: 0.19
Nodes (6): parse_steps(), validate_job(), good_job(), test_allowlist_refuses(), test_valid_job_passes(), test_validation_catches_bad_fields()

### Community 20 - "localrun.py"
Cohesion: 0.20
Nodes (9): _arg(), estimate_minutes(), ledger_append(), _limit_env(), load_policy(), _manifest_ntrain(), _preexec(), run_capped() (+1 more)

### Community 22 - "heal_decision"
Cohesion: 0.31
Nodes (12): admit(), classify(), heal_decision(), is_heavy(), is_resource_failure(), Policy, Probe, Request (+4 more)

### Community 25 - "test_committed_graph_is_fresh"
Cohesion: 0.18
Nodes (8): Actions taken, Code graph, Laptop environments: coding repaired, su2qc-jepa created, Next action, Problems and assumptions, What was asked, Actions taken, test_committed_graph_is_fresh()

### Community 27 - "su2.py"
Cohesion: 0.24
Nodes (3): _cg_cached(), clebsch_gordan(), _fact()

### Community 28 - "M1: su2qc cross-check PASS, three datasets built, gate J0 PASS"
Cohesion: 0.18
Nodes (10): Actions taken, Code graph, M1: su2qc cross-check PASS, three datasets built, gate J0 PASS, Next action, Part A — route C agrees with both su2qc routes (`evidence/J0_data/crosscheck_su2qc.json`, commit `0bb5d6d`, status PASS), Part B — datasets (`evidence/J0_data/datasets.json`, commit `358d0bd`), Part C — gate J0 PASS (`evidence/J0_data/20261003T201012Z.json`, 15 s on the laptop), Problems and assumptions (+2 more)

### Community 29 - "crosscheck_su2qc.py"
Cohesion: 0.25
Nodes (5): extract_terms(), import_su2qc(), main(), sign_gauge(), su2qc_label_to_c()

### Community 30 - "decisions/INDEX.md"
Cohesion: 0.20
Nodes (6): Frozen conventions and coupling points, Alternatives considered, Consequences, Numbered artifacts and the Graphify code graph, Why, Decisions — index

### Community 32 - "prompts/INDEX.md"
Cohesion: 0.20
Nodes (5): Expected, M6 — Hardware day 3, gate J3, error budget (W6, 2 sessions), M7 — One stretch item (W7), chosen on 15 Nov by Digonto, M8 — Paper assembly, release, replication (W8, 2 sessions), Prompts — index

### Community 34 - "CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`"
Cohesion: 0.22
Nodes (8): 1. Priorities, in order, 3. Frozen things (changing any of these needs a new `decisions/` record and a new version tag), 4. Hardware rules (non-negotiable), 6. Writing rules (reports, prompts, docs, paper), 7. What the package already guarantees (do not re-derive, do re-run), 8. Where things are, CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`, graphify

### Community 35 - "M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED"
Cohesion: 0.22
Nodes (7): Code graph, M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED, Next action, Problems and assumptions, Results and what they mean, What was asked, test_run_py_retries_after_memory_limit()

### Community 36 - "M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914)"
Cohesion: 0.22
Nodes (8): Laptop check, 10 epochs, 1 seed (`runs/v1_check/seed0/history.json`, local; validation split), M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914), Next action, Options for Digonto (a decision record in `decisions/` is needed for any of B–D, before the 16 Oct preregistration), Problems and assumptions, Results and what they mean, The energy row cannot pass with this encoder (`evidence/J1_training/ceiling_main.json`, validation split, 26,348 rows; training split 126,824 rows; `data/main` `73fff8e5a7b7`), What was asked

### Community 37 - "test_jepa_trains_one_epoch"
Cohesion: 0.56
Nodes (8): Actions taken, Code graph, JEPAConfig, prepare_tensors(), train_jepa(), TrainConfig, test_jepa_ema_target_and_curriculum(), test_jepa_trains_one_epoch()

### Community 40 - "Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`)"
Cohesion: 0.25
Nodes (8): Absolute safety rules (you have no permission prompts), Context, Definition of done, Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`), Phase A — inventory and backup (no changes), Phase B — repair `coding` (only after rule 4 allows it), Phase C — create `su2qc-jepa` (safe to do at any time; it touches no existing environment), Phase D — report

### Community 41 - "Package build: plan audit, Gauge-JEPA-P v2 and the starter package"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Package build: plan audit, Gauge-JEPA-P v2 and the starter package, Problems and assumptions, Results and what they mean, What was asked

### Community 42 - "Conventions update: numbered artifacts and the Graphify code graph"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Conventions update: numbered artifacts and the Graphify code graph, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 43 - "Compute update 2: safe laptop and a pull-based job queue for Perlmutter"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Compute update 2: safe laptop and a pull-based job queue for Perlmutter, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 44 - "Perlmutter worker install keeps the user's other scrontab entries"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Perlmutter worker install keeps the user's other scrontab entries, Problems and assumptions, Results and what they mean, What was asked

### Community 45 - "test_worker_slurm_mode_resubmits_after_timeout"
Cohesion: 0.29
Nodes (5): Actions taken, _git(), test_worker_end_to_end_local(), ignore(), test_worker_slurm_mode_resubmits_after_timeout()

### Community 46 - "residual_eval.py"
Cohesion: 0.32
Nodes (3): estimate(), krylov(), subsample()

### Community 47 - "scripts/run.py"
Cohesion: 0.32
Nodes (3): dataset_step(), guess_outputs(), queue()

### Community 48 - "{{title}}"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Problems and assumptions, Results and what they mean, {{title}}, What was asked

### Community 49 - ".seeds"
Cohesion: 0.29
Nodes (5): 5. Compute rules (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`), Decision, 1. Audit of the 1 Oct plan — issues found and what changed, Actions taken, pick_device()

### Community 50 - "Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`)"
Cohesion: 0.29
Nodes (6): Analysis plan (exact commands), Exclusion rules, Frozen inputs (fill in), Hypotheses (from PLAN §11), Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`), Signatures

### Community 52 - "os"
Cohesion: 0.48
Nodes (4): _env(), _run(), test_add_to_empty_table_and_remove_last_entry(), test_add_update_remove_keeps_other_entries()

### Community 53 - "M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)"
Cohesion: 0.29
Nodes (6): Expected, M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h), Part A — cross-check against the project's verified `su2qc` code, Part B — datasets, Part C — gate, Tests to add

### Community 54 - "su2qc-jepa — Gauge-JEPA-P v2 starter package"
Cohesion: 0.29
Nodes (6): First two sessions on the laptop, Five-minute tour, Install on the laptop (done by prompts/009), Layout, su2qc-jepa — Gauge-JEPA-P v2 starter package, What is verified today (`python scripts/run.py -- python -m pytest -q`: 47 fast tests; `-m slow` adds 1 more)

### Community 55 - "Compute update: laptop for light work, Perlmutter for heavy jobs"
Cohesion: 0.29
Nodes (6): Code graph, Compute update: laptop for light work, Perlmutter for heavy jobs, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 57 - "Compute: a safe laptop and a pull-based job queue for Perlmutter"
Cohesion: 0.33
Nodes (5): Alternatives considered, Compute: a safe laptop and a pull-based job queue for Perlmutter, Consequences, Decision, Why

### Community 58 - "J1 energy grounding threshold set relative to the measured information ceiling"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences (what must be re-run or re-checked), Decision, J1 energy grounding threshold set relative to the measured information ceiling, Why

### Community 59 - "M0 — Bootstrap (first Claude Code invocation, ~45 min)"
Cohesion: 0.33
Nodes (5): Context, Definition of done, M0 — Bootstrap (first Claude Code invocation, ~45 min), Out of scope, Tasks

### Community 60 - "M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card"
Cohesion: 0.33
Nodes (5): Context, Definition of done, M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card, Out of scope / stop conditions, Tasks

### Community 61 - "Results and what they mean"
Cohesion: 0.33
Nodes (6): `coding`: imports before and after (`import-before.json` → `import-after.json`), Disk, `pip check`, Results and what they mean, `su2qc-jepa` environment, The GTX 1060 (compute capability 6.1, driver 580.178.04, CUDA 13.0 driver API)

### Community 62 - "M0: repository created, CI green, code graph committed"
Cohesion: 0.33
Nodes (6): Code graph, M0: repository created, CI green, code graph committed, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 63 - "{{title}}"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences (what must be re-run or re-checked), Decision, {{title}}, Why

### Community 64 - "{{title}}"
Cohesion: 0.33
Nodes (5): Context, Definition of done, Out of scope / stop conditions, Tasks, {{title}}

### Community 65 - ".status"
Cohesion: 0.50
Nodes (4): 2. Session protocol (every session, no exceptions), Decision, 15. Repository conventions — numbered artifacts and the code graph (added 2 Oct 2026; `decisions/001`), series()

### Community 66 - "Compute: laptop for light work, Perlmutter for heavy jobs"
Cohesion: 0.40
Nodes (4): Alternatives considered, Compute: laptop for light work, Perlmutter for heavy jobs, Consequences, Why

### Community 67 - "M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)"
Cohesion: 0.40
Nodes (4): Expected, M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions), Session M2a — make the model healthy, Session M2b — preregistration (16 Oct)

### Community 68 - "M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)"
Cohesion: 0.40
Nodes (4): Expected, M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions), Session M3a — forecasting, Session M3b — twin and dry run

### Community 69 - "M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version."
Cohesion: 0.40
Nodes (4): Expected, M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version., Session M4a — J2 (30 Oct), Session M4b — pilot (one job)

## Knowledge Gaps
- **212 isolated node(s):** `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script`, `PYTHONHASHSEED`, `replicate.sh script` (+207 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 467 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PlaquetteModel` connect `PlaquetteModel` to `ObservableSet`, `j0_data.py`, `._apply_term`, `run_j0`, `Conventions update: numbered artifacts and the Graphify code graph`, `dynamics.py`, `test_physics.py`, `generate_dataset`, `trajectories.py`, `LinkSpace`, `_Cache`, `crosscheck_su2qc.py`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Why does `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier` connect `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier` to `.status`, `.seeds`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `retry_resources()` connect `retry_resources` to `test_jobs.py`, `Worker`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `PlaquetteModel` (e.g. with `Code graph` and `compare_point()`) actually correct?**
  _`PlaquetteModel` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `run_j0()` (e.g. with `ChainSpec` and `ObservableSet`) actually correct?**
  _`run_j0()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script` to the rest of the system?**
  _212 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `artifacts.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0632996632996633 - nodes in this community are weakly interconnected._