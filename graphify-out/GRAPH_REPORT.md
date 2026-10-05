# Graph Report - su2qc-jepa  (2026-10-05)

## Corpus Check
- 117 files · ~81,706 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 3, .cff 1)

## Summary
- 970 nodes · 1832 edges · 83 communities (53 shown, 30 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 123 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3fd0a658`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- train.py
- PlaquetteModel
- artifacts.py
- localrun.py
- pathlib
- ibm.py
- Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)
- Worker
- FullSpaceOperators
- ledger.py
- j0_data.py
- test_physics.py
- chain.py
- decisions/INDEX.md
- estimate_chain
- Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier
- train_jepa.py
- jobs.py
- test_committed_graph_is_fresh
- crosscheck_su2qc.py
- test_jobs.py
- Krylov
- Numbered artifacts and the Graphify code graph
- Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code)
- prompts/INDEX.md
- ObservableSet
- CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`
- .seeds
- scripts/run.py
- test_crosscheck.py
- Compute update 3: laptop and Perlmutter only, environment repair prompt, self-healing runners
- M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED
- 10. Week by week — what Claude Code does, what is tested, what we expect
- Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`)
- Package build: plan audit, Gauge-JEPA-P v2 and the starter package
- Conventions update: numbered artifacts and the Graphify code graph
- Perlmutter worker install keeps the user's other scrontab entries
- test_worker_slurm_mode_resubmits_after_timeout
- residual_eval.py
- noise.py
- {{title}}
- Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`)
- M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)
- su2qc-jepa — Gauge-JEPA-P v2 starter package
- Compute update: laptop for light work, Perlmutter for heavy jobs
- Compute update 2: safe laptop and a pull-based job queue for Perlmutter
- M0: repository created, CI green, code graph committed
- _Cache
- Heavy jobs: the job queue and the Perlmutter worker
- M0 — Bootstrap (first Claude Code invocation, ~45 min)
- M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card
- Results and what they mean
- {{title}}
- {{title}}
- test_scrontab_merge.py
- M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)
- M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)
- M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version.
- plans/INDEX.md
- reports/INDEX.md
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
3. `Worker` - 21 edges
4. `generate_dataset()` - 20 edges
5. `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier` - 20 edges
6. `ObservableSet` - 19 edges
7. `test_training_and_baselines_run_on_device()` - 17 edges
8. `Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)` - 17 edges
9. `ChainSpec` - 16 edges
10. `GaugeJEPA` - 15 edges

## Surprising Connections (you probably didn't know these)
- `Self-healing` --references--> `retry_resources()`  [INFERRED]
  docs/PERLMUTTER.md → src/su2qc_jepa/jobs.py
- `Actions taken` --references--> `retry_resources()`  [INFERRED]
  reports/004_compute-update-3-laptop-and-perlmutter-only-environment-repa.md → src/su2qc_jepa/jobs.py
- `12. Error budget (lines, each measured)` --references--> `trotter_error()`  [INFERRED]
  plans/001_gauge-jepa-p-v2.md → src/su2qc_jepa/physics/chain.py
- `9.4 Error budget (lines, each to be measured)` --references--> `trotter_error()`  [INFERRED]
  reports/011_project-overview-gauge-jepa-p-v2-plan-physics-status-and-eve.md → src/su2qc_jepa/physics/chain.py
- `Code graph` --references--> `PlaquetteModel`  [INFERRED]
  reports/001_conventions-update-numbered-artifacts-and-the-graphify-code.md → src/su2qc_jepa/physics/plaquette.py

## Import Cycles
- None detected.

## Communities (83 total, 30 thin omitted)

### Community 0 - "train.py"
Cohesion: 0.06
Nodes (36): Actions taken, Code graph, Laptop check, 10 epochs, 1 seed (`runs/v1_check/seed0/history.json`, local; validation split), M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914), Next action, Options for Digonto (a decision record in `decisions/` is needed for any of B–D, before the 16 Oct preregistration), Problems and assumptions, Results and what they mean (+28 more)

### Community 1 - "PlaquetteModel"
Cohesion: 0.05
Nodes (10): GIBasisState, LinkSpace, PlaquetteModel, _cg_cached(), clebsch_gordan(), _fact(), m_values(), spin_matrices() (+2 more)

### Community 2 - "artifacts.py"
Cohesion: 0.10
Nodes (23): Artifact, check_artifacts(), list_artifacts(), new_artifact(), next_number(), read_front_matter(), render_index(), _resolve() (+15 more)

### Community 3 - "localrun.py"
Cohesion: 0.09
Nodes (31): Actions taken, Code graph, M1: su2qc cross-check PASS, three datasets built, gate J0 PASS, Next action, Part A — route C agrees with both su2qc routes (`evidence/J0_data/crosscheck_su2qc.json`, commit `0bb5d6d`, status PASS), Part B — datasets (`evidence/J0_data/datasets.json`, commit `358d0bd`), Part C — gate J0 PASS (`evidence/J0_data/20261003T201012Z.json`, 15 s on the laptop), Problems and assumptions (+23 more)

### Community 5 - "ibm.py"
Cohesion: 0.09
Nodes (14): W4 (26 Oct – 1 Nov) — J2, pilot job; end of the one-month version, BudgetError, calibration_snapshot(), check_budget(), collect(), dry_run(), DryRunSummary, estimate_qpu_seconds() (+6 more)

### Community 6 - "Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)"
Cohesion: 0.07
Nodes (30): 0. How to read this document, 10.1 Before the repository existed (1–2 Oct, planner sessions; reports 000–005), 10.2 Environment and M0 (2 Oct; reports 006–008), 10.3 M1 — physics cross-check, datasets, gate J0 (3–4 Oct; `reports/009`) — **J0 PASS 9/9**, 10.4 M2a — model health (5 Oct; `reports/010`, `decisions/005`, and results fetched at 21:30 UTC), 10. What has been done, session by session (with every number), 11. Infrastructure and repository conventions (how the work is done), 12. Open problems and risks (as of 5 Oct, 21:40 UTC) (+22 more)

### Community 7 - "Worker"
Cohesion: 0.18
Nodes (5): hms_to_hours(), main(), now(), sh(), Worker

### Community 9 - "FullSpaceOperators"
Cohesion: 0.14
Nodes (3): Couplings, FullSpaceOperators, MatterSpace

### Community 10 - "ledger.py"
Cohesion: 0.15
Nodes (12): run_j1(), run_j2(), auroc(), run_j3(), spearman(), _fmt(), GateResult, GateRow (+4 more)

### Community 11 - "j0_data.py"
Cohesion: 0.14
Nodes (12): run_j0(), build_chain_circuit(), z_layer(), ChainSpec, trotter_error(), lanczos(), heron_like_noise_model(), chain_point_records() (+4 more)

### Community 12 - "test_physics.py"
Cohesion: 0.12
Nodes (14): Claims ledger — every substantive statement, its status and its evidence, _initial_state(), cz_count(), sector_restrict(), channel_masks(), named_states(), test_chain_circuit_matches_sector_unitary(), test_chain_prep_cascade() (+6 more)

### Community 13 - "chain.py"
Cohesion: 0.15
Nodes (11): _bond_rotation(), build_chain_prep_circuit(), chain_amplitudes(), chain_sector_unitary(), _layer(), _phase_weights(), prep_cascade_params(), sample_x_basis() (+3 more)

### Community 14 - "decisions/INDEX.md"
Cohesion: 0.09
Nodes (16): Frozen conventions and coupling points, Alternatives considered, Compute: laptop for light work, Perlmutter for heavy jobs, Consequences, Why, Alternatives considered, Compute: a safe laptop and a pull-based job queue for Perlmutter, Consequences (+8 more)

### Community 15 - "estimate_chain"
Cohesion: 0.15
Nodes (9): _bits_from_key(), estimate_chain(), estimate_diagonal(), ObservationSpec, Record, sample_exact_chain(), sample_exact_diagonal(), test_estimators_unbiased() (+1 more)

### Community 16 - "Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier"
Cohesion: 0.12
Nodes (17): 0. The idea in one paragraph, 11. Preregistered hypotheses and expected results, 12. Error budget (lines, each measured), 13. Publishability, 14. Assumptions, risks, open points, 16. Compute: the laptop and Perlmutter only (amended 2 Oct 2026; `decisions/004`, superseding `decisions/003` and `decisions/002`), 2. Why v2 is better — side by side, 3. Physics object (frozen) and measured fingerprints (+9 more)

### Community 18 - "jobs.py"
Cohesion: 0.20
Nodes (7): Alternatives considered, Compute: laptop and Perlmutter only, admission-controlled laptop runner, self-healing jobs, Consequences (what must be re-run or re-checked), Decision, Why, _hms(), retry_resources()

### Community 19 - "test_committed_graph_is_fresh"
Cohesion: 0.18
Nodes (8): Actions taken, Code graph, Laptop environments: coding repaired, su2qc-jepa created, Next action, Problems and assumptions, What was asked, Actions taken, test_committed_graph_is_fresh()

### Community 20 - "crosscheck_su2qc.py"
Cohesion: 0.26
Nodes (6): compare_point(), extract_terms(), import_su2qc(), main(), sign_gauge(), su2qc_label_to_c()

### Community 21 - "test_jobs.py"
Cohesion: 0.23
Nodes (7): parse_steps(), validate_job(), good_job(), test_allowlist_refuses(), test_retry_rule(), test_valid_job_passes(), test_validation_catches_bad_fields()

### Community 22 - "Krylov"
Cohesion: 0.26
Nodes (3): evolve(), Krylov, krylov_error()

### Community 23 - "Numbered artifacts and the Graphify code graph"
Cohesion: 0.22
Nodes (8): 2. Session protocol (every session, no exceptions), Alternatives considered, Consequences, Decision, Numbered artifacts and the Graphify code graph, Why, 15. Repository conventions — numbered artifacts and the code graph (added 2 Oct 2026; `decisions/001`), series()

### Community 24 - "Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code)"
Cohesion: 0.20
Nodes (10): Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code), Model, Observables, Predicted results, Problems and assumptions, Publishability, Schedule (5 Oct – 29 Nov 2026), Testing ladder (budgets are Claude's estimates) (+2 more)

### Community 25 - "prompts/INDEX.md"
Cohesion: 0.20
Nodes (5): Expected, M6 — Hardware day 3, gate J3, error budget (W6, 2 sessions), M7 — One stretch item (W7), chosen on 15 Nov by Digonto, M8 — Paper assembly, release, replication (W8, 2 sessions), Prompts — index

### Community 27 - "CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`"
Cohesion: 0.22
Nodes (8): 1. Priorities, in order, 3. Frozen things (changing any of these needs a new `decisions/` record and a new version tag), 4. Hardware rules (non-negotiable), 6. Writing rules (reports, prompts, docs, paper), 7. What the package already guarantees (do not re-derive, do re-run), 8. Where things are, CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`, graphify

### Community 28 - ".seeds"
Cohesion: 0.22
Nodes (5): 5. Compute rules (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`), Decision, 1. Audit of the 1 Oct plan — issues found and what changed, Actions taken, pick_device()

### Community 29 - "scripts/run.py"
Cohesion: 0.28
Nodes (3): dataset_step(), guess_outputs(), queue()

### Community 31 - "Compute update 3: laptop and Perlmutter only, environment repair prompt, self-healing runners"
Cohesion: 0.22
Nodes (8): Actions taken, Bugs found and fixed while doing this, Code graph, Compute update 3: laptop and Perlmutter only, environment repair prompt, self-healing runners, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 32 - "M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED"
Cohesion: 0.22
Nodes (7): Code graph, M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED, Next action, Problems and assumptions, Results and what they mean, What was asked, test_run_py_retries_after_memory_limit()

### Community 34 - "10. Week by week — what Claude Code does, what is tested, what we expect"
Cohesion: 0.25
Nodes (8): 10. Week by week — what Claude Code does, what is tested, what we expect, W1 (5–11 Oct) — bootstrap, physics cross-check, data → J0, W2 (12–18 Oct) — JEPA v1, collapse diagnostics, preregistration → J1, W3 (19–25 Oct) — forecasting, twin rehearsal, hardware dry runs, W5 (2–8 Nov) — hardware days 1 and 2, W6 (9–15 Nov) — day 3, J3, advantage-free analysis, W7 (16–22 Nov) — one stretch item, chosen on 15 Nov, W8 (23–29 Nov) — paper, release, replication

### Community 35 - "Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`)"
Cohesion: 0.25
Nodes (8): Absolute safety rules (you have no permission prompts), Context, Definition of done, Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`), Phase A — inventory and backup (no changes), Phase B — repair `coding` (only after rule 4 allows it), Phase C — create `su2qc-jepa` (safe to do at any time; it touches no existing environment), Phase D — report

### Community 36 - "Package build: plan audit, Gauge-JEPA-P v2 and the starter package"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Package build: plan audit, Gauge-JEPA-P v2 and the starter package, Problems and assumptions, Results and what they mean, What was asked

### Community 37 - "Conventions update: numbered artifacts and the Graphify code graph"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Conventions update: numbered artifacts and the Graphify code graph, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 38 - "Perlmutter worker install keeps the user's other scrontab entries"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Perlmutter worker install keeps the user's other scrontab entries, Problems and assumptions, Results and what they mean, What was asked

### Community 39 - "test_worker_slurm_mode_resubmits_after_timeout"
Cohesion: 0.29
Nodes (5): Actions taken, _git(), test_worker_end_to_end_local(), ignore(), test_worker_slurm_mode_resubmits_after_timeout()

### Community 40 - "residual_eval.py"
Cohesion: 0.32
Nodes (3): estimate(), krylov(), subsample()

### Community 41 - "noise.py"
Cohesion: 0.29
Nodes (3): HeronLike, noise_model_from_backend(), save_noise_summary()

### Community 42 - "{{title}}"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Problems and assumptions, Results and what they mean, {{title}}, What was asked

### Community 43 - "Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`)"
Cohesion: 0.29
Nodes (6): Analysis plan (exact commands), Exclusion rules, Frozen inputs (fill in), Hypotheses (from PLAN §11), Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`), Signatures

### Community 44 - "M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)"
Cohesion: 0.29
Nodes (6): Expected, M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h), Part A — cross-check against the project's verified `su2qc` code, Part B — datasets, Part C — gate, Tests to add

### Community 46 - "su2qc-jepa — Gauge-JEPA-P v2 starter package"
Cohesion: 0.29
Nodes (6): First two sessions on the laptop, Five-minute tour, Install on the laptop (done by prompts/009), Layout, su2qc-jepa — Gauge-JEPA-P v2 starter package, What is verified today (`python scripts/run.py -- python -m pytest -q`: 47 fast tests; `-m slow` adds 1 more)

### Community 47 - "Compute update: laptop for light work, Perlmutter for heavy jobs"
Cohesion: 0.29
Nodes (6): Code graph, Compute update: laptop for light work, Perlmutter for heavy jobs, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 48 - "Compute update 2: safe laptop and a pull-based job queue for Perlmutter"
Cohesion: 0.29
Nodes (7): Actions taken, Code graph, Compute update 2: safe laptop and a pull-based job queue for Perlmutter, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 49 - "M0: repository created, CI green, code graph committed"
Cohesion: 0.29
Nodes (6): Code graph, M0: repository created, CI green, code graph committed, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 51 - "Heavy jobs: the job queue and the Perlmutter worker"
Cohesion: 0.33
Nodes (5): Costs and limits, Heavy jobs: the job queue and the Perlmutter worker, One-time setup (Digonto, about 30 minutes, after the repository exists on GitHub), Self-healing, When something is wrong

### Community 52 - "M0 — Bootstrap (first Claude Code invocation, ~45 min)"
Cohesion: 0.33
Nodes (5): Context, Definition of done, M0 — Bootstrap (first Claude Code invocation, ~45 min), Out of scope, Tasks

### Community 53 - "M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card"
Cohesion: 0.33
Nodes (5): Context, Definition of done, M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card, Out of scope / stop conditions, Tasks

### Community 54 - "Results and what they mean"
Cohesion: 0.33
Nodes (6): `coding`: imports before and after (`import-before.json` → `import-after.json`), Disk, `pip check`, Results and what they mean, `su2qc-jepa` environment, The GTX 1060 (compute capability 6.1, driver 580.178.04, CUDA 13.0 driver API)

### Community 55 - "{{title}}"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences (what must be re-run or re-checked), Decision, {{title}}, Why

### Community 56 - "{{title}}"
Cohesion: 0.33
Nodes (5): Context, Definition of done, Out of scope / stop conditions, Tasks, {{title}}

### Community 57 - "test_scrontab_merge.py"
Cohesion: 0.60
Nodes (4): _env(), _run(), test_add_to_empty_table_and_remove_last_entry(), test_add_update_remove_keeps_other_entries()

### Community 58 - "M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)"
Cohesion: 0.40
Nodes (4): Expected, M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions), Session M2a — make the model healthy, Session M2b — preregistration (16 Oct)

### Community 59 - "M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)"
Cohesion: 0.40
Nodes (4): Expected, M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions), Session M3a — forecasting, Session M3b — twin and dry run

### Community 60 - "M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version."
Cohesion: 0.40
Nodes (4): Expected, M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version., Session M4a — J2 (30 Oct), Session M4b — pilot (one job)

## Knowledge Gaps
- **212 isolated node(s):** `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script`, `PYTHONHASHSEED`, `replicate.sh script` (+207 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 465 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **30 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PlaquetteModel` connect `PlaquetteModel` to `train.py`, `Conventions update: numbered artifacts and the Graphify code graph`, `trajectories.py`, `j0_data.py`, `test_physics.py`, `_Cache`, `crosscheck_su2qc.py`, `ObservableSet`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Why does `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier` connect `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier` to `10. Week by week — what Claude Code does, what is tested, what we expect`, `.seeds`, `plans/INDEX.md`, `Numbered artifacts and the Graphify code graph`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `retry_resources()` connect `jobs.py` to `Heavy jobs: the job queue and the Perlmutter worker`, `Worker`, `test_jobs.py`, `Compute update 3: laptop and Perlmutter only, environment repair prompt, self-healing runners`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `PlaquetteModel` (e.g. with `Code graph` and `compare_point()`) actually correct?**
  _`PlaquetteModel` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `run_j0()` (e.g. with `ChainSpec` and `ObservableSet`) actually correct?**
  _`run_j0()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script` to the rest of the system?**
  _212 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `train.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05894736842105263 - nodes in this community are weakly interconnected._