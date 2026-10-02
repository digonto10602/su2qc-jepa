# Graph Report - su2qc-jepa  (2026-10-02)

## Corpus Check
- 107 files · ~64,866 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 3, .cff 1)

## Summary
- 858 nodes · 1638 edges · 68 communities (44 shown, 24 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 101 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4b7a0282`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- train.py
- FullSpaceOperators
- prompts/INDEX.md
- PlaquetteModel
- retry_resources
- trajectories.py
- test_physics.py
- ibm.py
- artifacts.py
- Worker
- plaquette.py
- chain.py
- localrun.py
- ledger.py
- ChainSpec
- test_jobs.py
- Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier
- Krylov
- Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code)
- CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`
- test_localrun.py
- test_committed_graph_is_fresh
- train_jepa.py
- main
- graph.py
- scripts/run.py
- Package build: plan audit, Gauge-JEPA-P v2 and the starter package
- Compute update 2: safe laptop and a pull-based job queue for Perlmutter
- test_worker_slurm_mode_resubmits_after_timeout
- M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED
- noise.py
- {{title}}
- 5. Compute rules (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`)
- Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`)
- su2qc-jepa — Gauge-JEPA-P v2 starter package
- Conventions update: numbered artifacts and the Graphify code graph
- Perlmutter worker install keeps the user's other scrontab entries
- j3_hardware.py
- run_capped
- Heavy jobs: the job queue and the Perlmutter worker
- reports/INDEX.md
- Results and what they mean
- M0: repository created, CI green, code graph committed
- {{title}}
- {{title}}
- Compute: a safe laptop and a pull-based job queue for Perlmutter
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
1. `PlaquetteModel` - 40 edges
2. `run_j0()` - 24 edges
3. `Worker` - 21 edges
4. `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier` - 20 edges
5. `main()` - 18 edges
6. `generate_dataset()` - 18 edges
7. `ObservableSet` - 18 edges
8. `ChainSpec` - 16 edges
9. `GateResult` - 14 edges
10. `Krylov` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Decision` --references--> `main()`  [INFERRED]
  decisions/003_compute-a-safe-laptop-and-a-pull-based-job-queue-for-perlmut.md → scripts/worker/worker.py
- `Why` --references--> `main()`  [INFERRED]
  decisions/003_compute-a-safe-laptop-and-a-pull-based-job-queue-for-perlmut.md → scripts/worker/worker.py
- `When something is wrong` --references--> `main()`  [INFERRED]
  docs/PERLMUTTER.md → scripts/worker/worker.py
- `Tasks` --references--> `main()`  [INFERRED]
  prompts/000_bootstrap.md → scripts/worker/worker.py
- `What is verified today (`python scripts/run.py -- python -m pytest -q`: 47 fast tests; `-m slow` adds 1 more)` --references--> `main()`  [INFERRED]
  README.md → scripts/worker/worker.py

## Import Cycles
- None detected.

## Communities (68 total, 24 thin omitted)

### Community 0 - "train.py"
Cohesion: 0.07
Nodes (24): DatasetConfig, FamilyConfig, load_dataset(), ActionPredictor, effective_rank(), GaugeJEPA, JEPAConfig, MLP (+16 more)

### Community 1 - "FullSpaceOperators"
Cohesion: 0.06
Nodes (9): Couplings, FullSpaceOperators, LinkSpace, MatterSpace, _cg_cached(), clebsch_gordan(), _fact(), m_values() (+1 more)

### Community 2 - "prompts/INDEX.md"
Cohesion: 0.04
Nodes (38): Context, Definition of done, M0 — Bootstrap (first Claude Code invocation, ~45 min), Out of scope, Tasks, Expected, M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h), Part A — cross-check against the project's verified `su2qc` code (+30 more)

### Community 3 - "PlaquetteModel"
Cohesion: 0.08
Nodes (5): _Cache, GIBasisState, PlaquetteModel, model(), test_jmax1_counts()

### Community 4 - "retry_resources"
Cohesion: 0.05
Nodes (35): Frozen conventions and coupling points, Alternatives considered, Consequences, Numbered artifacts and the Graphify code graph, Why, Alternatives considered, Compute: laptop for light work, Perlmutter for heavy jobs, Consequences (+27 more)

### Community 5 - "trajectories.py"
Cohesion: 0.12
Nodes (17): _bits_from_key(), estimate_chain(), estimate_diagonal(), ObservationSpec, Record, sample_exact_chain(), sample_exact_diagonal(), _checksum() (+9 more)

### Community 6 - "test_physics.py"
Cohesion: 0.10
Nodes (12): Claims ledger — every substantive statement, its status and its evidence, sector_restrict(), channel_masks(), named_states(), ObservableSet, test_chain_prep_cascade(), test_channel_split(), test_dynamics_reproduce_preliminary_expectation() (+4 more)

### Community 7 - "ibm.py"
Cohesion: 0.10
Nodes (14): W4 (26 Oct – 1 Nov) — J2, pilot job; end of the one-month version, BudgetError, calibration_snapshot(), check_budget(), collect(), dry_run(), DryRunSummary, estimate_qpu_seconds() (+6 more)

### Community 8 - "artifacts.py"
Cohesion: 0.16
Nodes (17): Artifact, check_artifacts(), list_artifacts(), new_artifact(), next_number(), read_front_matter(), render_index(), _resolve() (+9 more)

### Community 9 - "Worker"
Cohesion: 0.18
Nodes (4): hms_to_hours(), now(), sh(), Worker

### Community 10 - "plaquette.py"
Cohesion: 0.13
Nodes (3): estimate(), krylov(), subsample()

### Community 11 - "chain.py"
Cohesion: 0.15
Nodes (11): _bond_rotation(), build_chain_prep_circuit(), chain_amplitudes(), chain_sector_unitary(), _layer(), _phase_weights(), prep_cascade_params(), sample_x_basis() (+3 more)

### Community 12 - "localrun.py"
Cohesion: 0.21
Nodes (16): admit(), _arg(), classify(), estimate_minutes(), heal_decision(), is_heavy(), is_resource_failure(), load_policy() (+8 more)

### Community 14 - "ledger.py"
Cohesion: 0.21
Nodes (8): run_j1(), run_j2(), _fmt(), GateResult, GateRow, load_thresholds(), write_gate(), test_gate_ledger()

### Community 15 - "ChainSpec"
Cohesion: 0.18
Nodes (9): Results and what they mean, build_chain_circuit(), z_layer(), ChainSpec, chain_point_records(), twin_variance_check(), TwinRunner, test_chain_circuit_matches_sector_unitary() (+1 more)

### Community 16 - "test_jobs.py"
Cohesion: 0.19
Nodes (6): parse_steps(), validate_job(), good_job(), test_allowlist_refuses(), test_valid_job_passes(), test_validation_catches_bad_fields()

### Community 17 - "Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier"
Cohesion: 0.13
Nodes (15): 0. The idea in one paragraph, 11. Preregistered hypotheses and expected results, 12. Error budget (lines, each measured), 13. Publishability, 14. Assumptions, risks, open points, 2. Why v2 is better — side by side, 3. Physics object (frozen) and measured fingerprints, 4. The Krylov-chain carrier (KC) (+7 more)

### Community 18 - "Krylov"
Cohesion: 0.18
Nodes (4): cz_count(), trotter_error(), Krylov, test_chain_cz_budget_PA()

### Community 19 - "Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code)"
Cohesion: 0.14
Nodes (11): Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code), Model, Observables, Predicted results, Problems and assumptions, Publishability, Schedule (5 Oct – 29 Nov 2026), Testing ladder (budgets are Claude's estimates) (+3 more)

### Community 20 - "CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`"
Cohesion: 0.15
Nodes (11): 1. Priorities, in order, 2. Session protocol (every session, no exceptions), 3. Frozen things (changing any of these needs a new `decisions/` record and a new version tag), 4. Hardware rules (non-negotiable), 6. Writing rules (reports, prompts, docs, paper), 7. What the package already guarantees (do not re-derive, do re-run), 8. Where things are, CLAUDE.md — rules for every Claude Code session in `su2qc-jepa` (+3 more)

### Community 21 - "test_localrun.py"
Cohesion: 0.22
Nodes (5): test_job_dies_with_the_runner(), _env(), _run(), test_add_to_empty_table_and_remove_last_entry(), test_add_update_remove_keeps_other_entries()

### Community 22 - "test_committed_graph_is_fresh"
Cohesion: 0.18
Nodes (8): Actions taken, Code graph, Laptop environments: coding repaired, su2qc-jepa created, Next action, Problems and assumptions, What was asked, Actions taken, test_committed_graph_is_fresh()

### Community 24 - "main"
Cohesion: 0.22
Nodes (11): 10. Week by week — what Claude Code does, what is tested, what we expect, 16. Compute: the laptop and Perlmutter only (amended 2 Oct 2026; `decisions/004`, superseding `decisions/003` and `decisions/002`), 6. Data, W1 (5–11 Oct) — bootstrap, physics cross-check, data → J0, W2 (12–18 Oct) — JEPA v1, collapse diagnostics, preregistration → J1, W3 (19–25 Oct) — forecasting, twin rehearsal, hardware dry runs, W5 (2–8 Nov) — hardware days 1 and 2, W6 (9–15 Nov) — day 3, J3, advantage-free analysis (+3 more)

### Community 26 - "graph.py"
Cohesion: 0.29
Nodes (6): _edges(), graph_stats(), load_graph(), same_structure(), structure_signature(), test_graph_helpers()

### Community 27 - "scripts/run.py"
Cohesion: 0.28
Nodes (3): dataset_step(), guess_outputs(), queue()

### Community 28 - "Package build: plan audit, Gauge-JEPA-P v2 and the starter package"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Package build: plan audit, Gauge-JEPA-P v2 and the starter package, Problems and assumptions, Results and what they mean, What was asked

### Community 29 - "Compute update 2: safe laptop and a pull-based job queue for Perlmutter"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Compute update 2: safe laptop and a pull-based job queue for Perlmutter, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 30 - "test_worker_slurm_mode_resubmits_after_timeout"
Cohesion: 0.29
Nodes (5): Actions taken, _git(), test_worker_end_to_end_local(), ignore(), test_worker_slurm_mode_resubmits_after_timeout()

### Community 31 - "M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED"
Cohesion: 0.25
Nodes (7): Code graph, M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED, Next action, Problems and assumptions, Results and what they mean, What was asked, test_run_py_retries_after_memory_limit()

### Community 32 - "noise.py"
Cohesion: 0.29
Nodes (3): HeronLike, noise_model_from_backend(), save_noise_summary()

### Community 33 - "{{title}}"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Problems and assumptions, Results and what they mean, {{title}}, What was asked

### Community 34 - "5. Compute rules (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`)"
Cohesion: 0.29
Nodes (3): 5. Compute rules (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`), 1. Audit of the 1 Oct plan — issues found and what changed, git()

### Community 35 - "Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`)"
Cohesion: 0.29
Nodes (6): Analysis plan (exact commands), Exclusion rules, Frozen inputs (fill in), Hypotheses (from PLAN §11), Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`), Signatures

### Community 37 - "su2qc-jepa — Gauge-JEPA-P v2 starter package"
Cohesion: 0.29
Nodes (6): First two sessions on the laptop, Five-minute tour, Install on the laptop (done by prompts/009), Layout, su2qc-jepa — Gauge-JEPA-P v2 starter package, What is verified today (`python scripts/run.py -- python -m pytest -q`: 47 fast tests; `-m slow` adds 1 more)

### Community 38 - "Conventions update: numbered artifacts and the Graphify code graph"
Cohesion: 0.29
Nodes (7): Actions taken, Code graph, Conventions update: numbered artifacts and the Graphify code graph, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 39 - "Perlmutter worker install keeps the user's other scrontab entries"
Cohesion: 0.29
Nodes (7): Actions taken, Code graph, Next action, Perlmutter worker install keeps the user's other scrontab entries, Problems and assumptions, Results and what they mean, What was asked

### Community 40 - "j3_hardware.py"
Cohesion: 0.43
Nodes (4): auroc(), run_j3(), spearman(), test_spearman_auroc()

### Community 41 - "run_capped"
Cohesion: 0.29
Nodes (5): ledger_append(), _limit_env(), _preexec(), run_capped(), _systemd_scope_ok()

### Community 42 - "Heavy jobs: the job queue and the Perlmutter worker"
Cohesion: 0.33
Nodes (5): Costs and limits, Heavy jobs: the job queue and the Perlmutter worker, One-time setup (Digonto, about 30 minutes, after the repository exists on GitHub), Self-healing, When something is wrong

### Community 44 - "Results and what they mean"
Cohesion: 0.33
Nodes (6): `coding`: imports before and after (`import-before.json` → `import-after.json`), Disk, `pip check`, Results and what they mean, `su2qc-jepa` environment, The GTX 1060 (compute capability 6.1, driver 580.178.04, CUDA 13.0 driver API)

### Community 45 - "M0: repository created, CI green, code graph committed"
Cohesion: 0.33
Nodes (5): Code graph, M0: repository created, CI green, code graph committed, Next action, Problems and assumptions, What was asked

### Community 46 - "{{title}}"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences (what must be re-run or re-checked), Decision, {{title}}, Why

### Community 47 - "{{title}}"
Cohesion: 0.33
Nodes (5): Context, Definition of done, Out of scope / stop conditions, Tasks, {{title}}

### Community 48 - "Compute: a safe laptop and a pull-based job queue for Perlmutter"
Cohesion: 0.40
Nodes (5): Alternatives considered, Compute: a safe laptop and a pull-based job queue for Perlmutter, Consequences, Decision, Why

## Knowledge Gaps
- **159 isolated node(s):** `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script`, `PYTHONHASHSEED`, `replicate.sh script` (+154 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 385 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `main` to `5. Compute rules (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`)`, `prompts/INDEX.md`, `retry_resources`, `su2qc-jepa — Gauge-JEPA-P v2 starter package`, `Worker`, `Heavy jobs: the job queue and the Perlmutter worker`, `ChainSpec`, `Compute: a safe laptop and a pull-based job queue for Perlmutter`, `Compute update 2: safe laptop and a pull-based job queue for Perlmutter`?**
  _High betweenness centrality (0.203) - this node is a cross-community bridge._
- **Why does `Tasks` connect `prompts/INDEX.md` to `main`?**
  _High betweenness centrality (0.098) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `PlaquetteModel` (e.g. with `Code graph` and `_Cache`) actually correct?**
  _`PlaquetteModel` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `run_j0()` (e.g. with `ChainSpec` and `ObservableSet`) actually correct?**
  _`run_j0()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script` to the rest of the system?**
  _159 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `train.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07017543859649122 - nodes in this community are weakly interconnected._
- **Should `FullSpaceOperators` be split into smaller, more focused modules?**
  _Cohesion score 0.06289308176100629 - nodes in this community are weakly interconnected._