# Graph Report - su2qc-jepa  (2026-10-05)

## Corpus Check
- 116 files · ~74,600 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 3, .cff 1)

## Summary
- 937 nodes · 1781 edges · 90 communities (50 shown, 40 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 108 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2b10e5b4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- train.py
- Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier
- artifacts.py
- ibm.py
- ledger.py
- Worker
- FullSpaceOperators
- retry_resources
- twin/run.py
- chain.py
- PlaquetteModel
- test_jobs.py
- named_states
- ChainSpec
- test_crosscheck.py
- run_j0
- crosscheck_su2qc.py
- worker.py
- localrun.py
- test_localrun.py
- m_values
- Krylov
- su2.py
- test_committed_graph_is_fresh
- prompts/INDEX.md
- M1: su2qc cross-check PASS, three datasets built, gate J0 PASS
- ObservableSet
- CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`
- Compute: laptop for light work, Perlmutter for heavy jobs
- scripts/run.py
- M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED
- Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`)
- Package build: plan audit, Gauge-JEPA-P v2 and the starter package
- Conventions update: numbered artifacts and the Graphify code graph
- Perlmutter worker install keeps the user's other scrontab entries
- _Cache
- {{title}}
- Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`)
- M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)
- su2qc-jepa — Gauge-JEPA-P v2 starter package
- Compute update: laptop for light work, Perlmutter for heavy jobs
- Compute update 2: safe laptop and a pull-based job queue for Perlmutter
- M0: repository created, CI green, code graph committed
- LinkSpace
- Compute: a safe laptop and a pull-based job queue for Perlmutter
- J1 energy grounding threshold set relative to the measured information ceiling
- M0 — Bootstrap (first Claude Code invocation, ~45 min)
- M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card
- Results and what they mean
- residual_eval.py
- {{title}}
- {{title}}
- test_scrontab_merge.py
- .status
- decisions/INDEX.md
- Numbered artifacts and the Graphify code graph
- M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)
- M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)
- M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version.
- ._apply_term
- reports/INDEX.md
- noise.py
- HeronLike
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
1. `PlaquetteModel` - 42 edges
2. `run_j0()` - 24 edges
3. `Worker` - 21 edges
4. `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier` - 20 edges
5. `generate_dataset()` - 19 edges
6. `ObservableSet` - 19 edges
7. `ChainSpec` - 16 edges
8. `GaugeJEPA` - 15 edges
9. `lanczos()` - 15 edges
10. `GateResult` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Problems and assumptions` --references--> `estimate_minutes()`  [INFERRED]
  reports/009_m1-su2qc-cross-check-pass-three-datasets-built-gate-j0-pass.md → src/su2qc_jepa/localrun.py
- `12. Error budget (lines, each measured)` --references--> `trotter_error()`  [INFERRED]
  plans/001_gauge-jepa-p-v2.md → src/su2qc_jepa/physics/chain.py
- `Code graph` --references--> `PlaquetteModel`  [INFERRED]
  reports/001_conventions-update-numbered-artifacts-and-the-graphify-code.md → src/su2qc_jepa/physics/plaquette.py
- `Actions taken` --references--> `check_artifacts()`  [INFERRED]
  reports/003_compute-update-2-safe-laptop-and-a-pull-based-job-queue-for.md → src/su2qc_jepa/repo/artifacts.py
- `Bugs found and fixed while doing this` --references--> `check_artifacts()`  [INFERRED]
  reports/004_compute-update-3-laptop-and-perlmutter-only-environment-repa.md → src/su2qc_jepa/repo/artifacts.py

## Import Cycles
- None detected.

## Communities (90 total, 40 thin omitted)

### Community 0 - "train.py"
Cohesion: 0.06
Nodes (36): Actions taken, Code graph, Laptop check, 10 epochs, 1 seed (`runs/v1_check/seed0/history.json`, local; validation split), M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914), Next action, Options for Digonto (a decision record in `decisions/` is needed for any of B–D, before the 16 Oct preregistration), Problems and assumptions, Results and what they mean (+28 more)

### Community 2 - "Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier"
Cohesion: 0.05
Nodes (37): Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code), Model, Observables, Predicted results, Problems and assumptions, Publishability, Schedule (5 Oct – 29 Nov 2026), Testing ladder (budgets are Claude's estimates) (+29 more)

### Community 3 - "artifacts.py"
Cohesion: 0.11
Nodes (23): Artifact, check_artifacts(), list_artifacts(), new_artifact(), next_number(), read_front_matter(), render_index(), _resolve() (+15 more)

### Community 5 - "ibm.py"
Cohesion: 0.10
Nodes (13): BudgetError, calibration_snapshot(), check_budget(), collect(), dry_run(), DryRunSummary, estimate_qpu_seconds(), _hash_circuits() (+5 more)

### Community 6 - "ledger.py"
Cohesion: 0.15
Nodes (12): run_j1(), run_j2(), auroc(), run_j3(), spearman(), _fmt(), GateResult, GateRow (+4 more)

### Community 7 - "Worker"
Cohesion: 0.20
Nodes (5): hms_to_hours(), main(), now(), sh(), Worker

### Community 9 - "retry_resources"
Cohesion: 0.09
Nodes (21): Alternatives considered, Compute: laptop and Perlmutter only, admission-controlled laptop runner, self-healing jobs, Consequences (what must be re-run or re-checked), Decision, Why, Costs and limits, Heavy jobs: the job queue and the Perlmutter worker, One-time setup (Digonto, about 30 minutes, after the repository exists on GitHub) (+13 more)

### Community 10 - "twin/run.py"
Cohesion: 0.13
Nodes (10): _bits_from_key(), estimate_chain(), estimate_diagonal(), ObservationSpec, Record, sample_exact_chain(), sample_exact_diagonal(), chain_point_records() (+2 more)

### Community 11 - "chain.py"
Cohesion: 0.16
Nodes (11): _bond_rotation(), build_chain_prep_circuit(), chain_sector_unitary(), _layer(), _phase_weights(), prep_cascade_params(), sample_x_basis(), sample_z_basis() (+3 more)

### Community 13 - "test_jobs.py"
Cohesion: 0.15
Nodes (11): Actions taken, parse_steps(), validate_job(), _git(), good_job(), test_allowlist_refuses(), test_valid_job_passes(), test_validation_catches_bad_fields() (+3 more)

### Community 14 - "named_states"
Cohesion: 0.15
Nodes (11): Claims ledger — every substantive statement, its status and its evidence, krylov(), sector_restrict(), channel_masks(), named_states(), test_channel_split(), test_dynamics_reproduce_preliminary_expectation(), test_krylov_dimension_window_PA() (+3 more)

### Community 15 - "ChainSpec"
Cohesion: 0.16
Nodes (9): Results and what they mean, build_chain_circuit(), z_layer(), chain_amplitudes(), ChainSpec, cz_count(), trotter_error(), test_chain_circuit_matches_sector_unitary() (+1 more)

### Community 17 - "run_j0"
Cohesion: 0.17
Nodes (7): 1. Audit of the 1 Oct plan — issues found and what changed, run_j0(), lanczos(), heron_like_noise_model(), twin_variance_check(), TwinRunner, test_twin_runner_seed_independence()

### Community 18 - "crosscheck_su2qc.py"
Cohesion: 0.17
Nodes (7): compare_point(), extract_terms(), import_su2qc(), main(), sign_gauge(), su2qc_label_to_c(), Couplings

### Community 20 - "localrun.py"
Cohesion: 0.20
Nodes (9): _arg(), estimate_minutes(), ledger_append(), _limit_env(), load_policy(), _manifest_ntrain(), _preexec(), run_capped() (+1 more)

### Community 21 - "test_localrun.py"
Cohesion: 0.27
Nodes (12): admit(), classify(), heal_decision(), is_heavy(), is_resource_failure(), Policy, Probe, Request (+4 more)

### Community 23 - "Krylov"
Cohesion: 0.26
Nodes (3): evolve(), Krylov, krylov_error()

### Community 24 - "su2.py"
Cohesion: 0.24
Nodes (3): _cg_cached(), clebsch_gordan(), _fact()

### Community 26 - "test_committed_graph_is_fresh"
Cohesion: 0.20
Nodes (7): Actions taken, Code graph, Laptop environments: coding repaired, su2qc-jepa created, Next action, Problems and assumptions, What was asked, test_committed_graph_is_fresh()

### Community 27 - "prompts/INDEX.md"
Cohesion: 0.20
Nodes (5): Expected, M6 — Hardware day 3, gate J3, error budget (W6, 2 sessions), M7 — One stretch item (W7), chosen on 15 Nov by Digonto, M8 — Paper assembly, release, replication (W8, 2 sessions), Prompts — index

### Community 28 - "M1: su2qc cross-check PASS, three datasets built, gate J0 PASS"
Cohesion: 0.20
Nodes (10): Actions taken, Code graph, M1: su2qc cross-check PASS, three datasets built, gate J0 PASS, Next action, Part A — route C agrees with both su2qc routes (`evidence/J0_data/crosscheck_su2qc.json`, commit `0bb5d6d`, status PASS), Part B — datasets (`evidence/J0_data/datasets.json`, commit `358d0bd`), Part C — gate J0 PASS (`evidence/J0_data/20261003T201012Z.json`, 15 s on the laptop), Problems and assumptions (+2 more)

### Community 30 - "CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`"
Cohesion: 0.22
Nodes (8): 1. Priorities, in order, 3. Frozen things (changing any of these needs a new `decisions/` record and a new version tag), 4. Hardware rules (non-negotiable), 6. Writing rules (reports, prompts, docs, paper), 7. What the package already guarantees (do not re-derive, do re-run), 8. Where things are, CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`, graphify

### Community 31 - "Compute: laptop for light work, Perlmutter for heavy jobs"
Cohesion: 0.22
Nodes (8): 5. Compute rules (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`), Alternatives considered, Compute: laptop for light work, Perlmutter for heavy jobs, Consequences, Decision, Why, Actions taken, pick_device()

### Community 32 - "scripts/run.py"
Cohesion: 0.28
Nodes (3): dataset_step(), guess_outputs(), queue()

### Community 33 - "M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED"
Cohesion: 0.22
Nodes (7): Code graph, M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED, Next action, Problems and assumptions, Results and what they mean, What was asked, test_run_py_retries_after_memory_limit()

### Community 34 - "Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`)"
Cohesion: 0.25
Nodes (8): Absolute safety rules (you have no permission prompts), Context, Definition of done, Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`), Phase A — inventory and backup (no changes), Phase B — repair `coding` (only after rule 4 allows it), Phase C — create `su2qc-jepa` (safe to do at any time; it touches no existing environment), Phase D — report

### Community 35 - "Package build: plan audit, Gauge-JEPA-P v2 and the starter package"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Package build: plan audit, Gauge-JEPA-P v2 and the starter package, Problems and assumptions, Results and what they mean, What was asked

### Community 36 - "Conventions update: numbered artifacts and the Graphify code graph"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Conventions update: numbered artifacts and the Graphify code graph, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 37 - "Perlmutter worker install keeps the user's other scrontab entries"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Perlmutter worker install keeps the user's other scrontab entries, Problems and assumptions, Results and what they mean, What was asked

### Community 38 - "_Cache"
Cohesion: 0.36
Nodes (3): _Cache, _checksum(), _initial_state()

### Community 39 - "{{title}}"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Problems and assumptions, Results and what they mean, {{title}}, What was asked

### Community 40 - "Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`)"
Cohesion: 0.29
Nodes (6): Analysis plan (exact commands), Exclusion rules, Frozen inputs (fill in), Hypotheses (from PLAN §11), Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`), Signatures

### Community 41 - "M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)"
Cohesion: 0.29
Nodes (6): Expected, M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h), Part A — cross-check against the project's verified `su2qc` code, Part B — datasets, Part C — gate, Tests to add

### Community 42 - "su2qc-jepa — Gauge-JEPA-P v2 starter package"
Cohesion: 0.29
Nodes (6): First two sessions on the laptop, Five-minute tour, Install on the laptop (done by prompts/009), Layout, su2qc-jepa — Gauge-JEPA-P v2 starter package, What is verified today (`python scripts/run.py -- python -m pytest -q`: 47 fast tests; `-m slow` adds 1 more)

### Community 43 - "Compute update: laptop for light work, Perlmutter for heavy jobs"
Cohesion: 0.29
Nodes (6): Code graph, Compute update: laptop for light work, Perlmutter for heavy jobs, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 44 - "Compute update 2: safe laptop and a pull-based job queue for Perlmutter"
Cohesion: 0.29
Nodes (7): Actions taken, Code graph, Compute update 2: safe laptop and a pull-based job queue for Perlmutter, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 45 - "M0: repository created, CI green, code graph committed"
Cohesion: 0.29
Nodes (6): Actions taken, Code graph, M0: repository created, CI green, code graph committed, Next action, Problems and assumptions, What was asked

### Community 47 - "Compute: a safe laptop and a pull-based job queue for Perlmutter"
Cohesion: 0.33
Nodes (5): Alternatives considered, Compute: a safe laptop and a pull-based job queue for Perlmutter, Consequences, Decision, Why

### Community 48 - "J1 energy grounding threshold set relative to the measured information ceiling"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences (what must be re-run or re-checked), Decision, J1 energy grounding threshold set relative to the measured information ceiling, Why

### Community 49 - "M0 — Bootstrap (first Claude Code invocation, ~45 min)"
Cohesion: 0.33
Nodes (5): Context, Definition of done, M0 — Bootstrap (first Claude Code invocation, ~45 min), Out of scope, Tasks

### Community 50 - "M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card"
Cohesion: 0.33
Nodes (5): Context, Definition of done, M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card, Out of scope / stop conditions, Tasks

### Community 51 - "Results and what they mean"
Cohesion: 0.33
Nodes (6): `coding`: imports before and after (`import-before.json` → `import-after.json`), Disk, `pip check`, Results and what they mean, `su2qc-jepa` environment, The GTX 1060 (compute capability 6.1, driver 580.178.04, CUDA 13.0 driver API)

### Community 53 - "{{title}}"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences (what must be re-run or re-checked), Decision, {{title}}, Why

### Community 54 - "{{title}}"
Cohesion: 0.33
Nodes (5): Context, Definition of done, Out of scope / stop conditions, Tasks, {{title}}

### Community 55 - "test_scrontab_merge.py"
Cohesion: 0.60
Nodes (4): _env(), _run(), test_add_to_empty_table_and_remove_last_entry(), test_add_update_remove_keeps_other_entries()

### Community 56 - ".status"
Cohesion: 0.50
Nodes (4): 2. Session protocol (every session, no exceptions), Decision, 15. Repository conventions — numbered artifacts and the code graph (added 2 Oct 2026; `decisions/001`), series()

### Community 58 - "Numbered artifacts and the Graphify code graph"
Cohesion: 0.40
Nodes (4): Alternatives considered, Consequences, Numbered artifacts and the Graphify code graph, Why

### Community 59 - "M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)"
Cohesion: 0.40
Nodes (4): Expected, M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions), Session M2a — make the model healthy, Session M2b — preregistration (16 Oct)

### Community 60 - "M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)"
Cohesion: 0.40
Nodes (4): Expected, M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions), Session M3a — forecasting, Session M3b — twin and dry run

### Community 61 - "M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version."
Cohesion: 0.40
Nodes (4): Expected, M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version., Session M4a — J2 (30 Oct), Session M4b — pilot (one job)

## Knowledge Gaps
- **191 isolated node(s):** `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script`, `PYTHONHASHSEED`, `replicate.sh script` (+186 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 442 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **40 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PlaquetteModel` connect `PlaquetteModel` to `train.py`, `trajectories.py`, `Conventions update: numbered artifacts and the Graphify code graph`, `j0_data.py`, `_Cache`, `.full_space_vectors`, `named_states`, `test_jmax1_counts`, `run_j0`, `crosscheck_su2qc.py`, `model`, `m_values`, `ObservableSet`, `._apply_term`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Why does `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier` connect `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier` to `.status`, `run_j0`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `retry_resources()` connect `retry_resources` to `worker.py`, `Worker`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `PlaquetteModel` (e.g. with `Code graph` and `compare_point()`) actually correct?**
  _`PlaquetteModel` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `run_j0()` (e.g. with `ChainSpec` and `ObservableSet`) actually correct?**
  _`run_j0()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script` to the rest of the system?**
  _191 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `train.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05621621621621622 - nodes in this community are weakly interconnected._