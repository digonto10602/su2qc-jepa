# Graph Report - su2qc-jepa  (2026-10-02)

## Corpus Check
- 105 files · ~62,749 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 3, .cff 1)

## Summary
- 842 nodes · 1615 edges · 64 communities (37 shown, 27 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 95 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- trajectories.py
- localrun.py
- pathlib
- train.py
- artifacts.py
- prompts/INDEX.md
- ibm.py
- FullSpaceOperators
- graph.py
- Worker
- chain.py
- PlaquetteModel
- run_j0
- Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier
- main
- decisions/INDEX.md
- Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code)
- ChainSpec
- CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`
- su2.py
- retry_resources
- m_values
- test_physics.py
- TwinRunner
- ._apply_term
- named_states
- Compute: laptop for light work, Perlmutter for heavy jobs
- Package build: plan audit, Gauge-JEPA-P v2 and the starter package
- Compute update 2: safe laptop and a pull-based job queue for Perlmutter
- Compute update 3: laptop and Perlmutter only, environment repair prompt, self-healing runners
- {{title}}
- Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`)
- su2qc-jepa — Gauge-JEPA-P v2 starter package
- Conventions update: numbered artifacts and the Graphify code graph
- Compute update: laptop for light work, Perlmutter for heavy jobs
- Perlmutter worker install keeps the user's other scrontab entries
- test_chain_cz_budget_PA
- LinkSpace
- Heavy jobs: the job queue and the Perlmutter worker
- {{title}}
- {{title}}
- reports/INDEX.md
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
- test_jmax1_counts
- plan.md
- model
- su2qc-jepa

## God Nodes (most connected - your core abstractions)
1. `PlaquetteModel` - 40 edges
2. `run_j0()` - 24 edges
3. `Worker` - 21 edges
4. `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier` - 20 edges
5. `generate_dataset()` - 18 edges
6. `ObservableSet` - 18 edges
7. `main()` - 17 edges
8. `ChainSpec` - 16 edges
9. `GateResult` - 14 edges
10. `Krylov` - 14 edges

## Surprising Connections (you probably didn't know these)
- `When something is wrong` --references--> `main()`  [INFERRED]
  docs/PERLMUTTER.md → scripts/worker/worker.py
- `6. Data` --references--> `main()`  [INFERRED]
  plans/001_gauge-jepa-p-v2.md → scripts/worker/worker.py
- `Tasks` --references--> `main()`  [INFERRED]
  prompts/000_bootstrap.md → scripts/worker/worker.py
- `What is verified today (`python scripts/run.py -- python -m pytest -q`: 47 fast tests; `-m slow` adds 1 more)` --references--> `main()`  [INFERRED]
  README.md → scripts/worker/worker.py
- `Results and what they mean` --references--> `main()`  [INFERRED]
  reports/003_compute-update-2-safe-laptop-and-a-pull-based-job-queue-for.md → scripts/worker/worker.py

## Import Cycles
- None detected.

## Communities (64 total, 27 thin omitted)

### Community 0 - "trajectories.py"
Cohesion: 0.06
Nodes (23): estimate(), krylov(), subsample(), _bits_from_key(), estimate_chain(), estimate_diagonal(), ObservationSpec, Record (+15 more)

### Community 1 - "localrun.py"
Cohesion: 0.05
Nodes (33): dataset_step(), guess_outputs(), queue(), estimate_hours(), load_compute(), parse_steps(), admit(), _arg() (+25 more)

### Community 2 - "pathlib"
Cohesion: 0.06
Nodes (15): run_j1(), run_j2(), auroc(), run_j3(), spearman(), _fmt(), GateResult, GateRow (+7 more)

### Community 3 - "train.py"
Cohesion: 0.07
Nodes (19): ActionPredictor, effective_rank(), GaugeJEPA, JEPAConfig, MLP, sigreg_loss(), baseline_autoregressive(), baseline_ridge() (+11 more)

### Community 4 - "artifacts.py"
Cohesion: 0.07
Nodes (26): validate_job(), Artifact, check_artifacts(), list_artifacts(), new_artifact(), next_number(), read_front_matter(), render_index() (+18 more)

### Community 5 - "prompts/INDEX.md"
Cohesion: 0.04
Nodes (38): Context, Definition of done, M0 — Bootstrap (first Claude Code invocation, ~45 min), Out of scope, Tasks, Expected, M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h), Part A — cross-check against the project's verified `su2qc` code (+30 more)

### Community 6 - "ibm.py"
Cohesion: 0.09
Nodes (14): W4 (26 Oct – 1 Nov) — J2, pilot job; end of the one-month version, BudgetError, calibration_snapshot(), check_budget(), collect(), dry_run(), DryRunSummary, estimate_qpu_seconds() (+6 more)

### Community 7 - "FullSpaceOperators"
Cohesion: 0.14
Nodes (3): Couplings, FullSpaceOperators, MatterSpace

### Community 8 - "graph.py"
Cohesion: 0.09
Nodes (19): Actions taken, Code graph, `coding`: imports before and after (`import-before.json` → `import-after.json`), Disk, Laptop environments: coding repaired, su2qc-jepa created, Next action, `pip check`, Problems and assumptions (+11 more)

### Community 9 - "Worker"
Cohesion: 0.21
Nodes (4): hms_to_hours(), now(), sh(), Worker

### Community 10 - "chain.py"
Cohesion: 0.14
Nodes (12): _bond_rotation(), build_chain_prep_circuit(), chain_amplitudes(), chain_sector_unitary(), _layer(), _phase_weights(), prep_cascade_params(), sample_x_basis() (+4 more)

### Community 12 - "run_j0"
Cohesion: 0.19
Nodes (6): run_j0(), evolve(), Krylov, krylov_error(), lanczos(), test_krylov_dimension_window_PA()

### Community 13 - "Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier"
Cohesion: 0.12
Nodes (16): 0. The idea in one paragraph, 11. Preregistered hypotheses and expected results, 12. Error budget (lines, each measured), 13. Publishability, 14. Assumptions, risks, open points, 2. Why v2 is better — side by side, 3. Physics object (frozen) and measured fingerprints, 4. The Krylov-chain carrier (KC) (+8 more)

### Community 14 - "main"
Cohesion: 0.16
Nodes (15): Alternatives considered, Compute: a safe laptop and a pull-based job queue for Perlmutter, Consequences, Decision, Why, 10. Week by week — what Claude Code does, what is tested, what we expect, 16. Compute: the laptop and Perlmutter only (amended 2 Oct 2026; `decisions/004`, superseding `decisions/003` and `decisions/002`), W1 (5–11 Oct) — bootstrap, physics cross-check, data → J0 (+7 more)

### Community 15 - "decisions/INDEX.md"
Cohesion: 0.14
Nodes (9): 2. Session protocol (every session, no exceptions), Frozen conventions and coupling points, Alternatives considered, Consequences, Decision, Numbered artifacts and the Graphify code graph, Why, Decisions — index (+1 more)

### Community 16 - "Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code)"
Cohesion: 0.14
Nodes (11): Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code), Model, Observables, Predicted results, Problems and assumptions, Publishability, Schedule (5 Oct – 29 Nov 2026), Testing ladder (budgets are Claude's estimates) (+3 more)

### Community 17 - "ChainSpec"
Cohesion: 0.22
Nodes (6): build_chain_circuit(), z_layer(), ChainSpec, chain_point_records(), twin_variance_check(), test_chain_circuit_matches_sector_unitary()

### Community 18 - "CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`"
Cohesion: 0.18
Nodes (10): 1. Priorities, in order, 3. Frozen things (changing any of these needs a new `decisions/` record and a new version tag), 4. Hardware rules (non-negotiable), 5. Compute rules (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`), 6. Writing rules (reports, prompts, docs, paper), 7. What the package already guarantees (do not re-derive, do re-run), 8. Where things are, CLAUDE.md — rules for every Claude Code session in `su2qc-jepa` (+2 more)

### Community 19 - "su2.py"
Cohesion: 0.24
Nodes (3): _cg_cached(), clebsch_gordan(), _fact()

### Community 20 - "retry_resources"
Cohesion: 0.22
Nodes (8): Alternatives considered, Compute: laptop and Perlmutter only, admission-controlled laptop runner, self-healing jobs, Consequences (what must be re-run or re-checked), Decision, Why, _hms(), retry_resources(), test_retry_rule()

### Community 22 - "test_physics.py"
Cohesion: 0.25
Nodes (3): Claims ledger — every substantive statement, its status and its evidence, test_dynamics_reproduce_preliminary_expectation(), test_two_routes_agree_and_gauss_law()

### Community 23 - "TwinRunner"
Cohesion: 0.28
Nodes (4): 1. Audit of the 1 Oct plan — issues found and what changed, heron_like_noise_model(), TwinRunner, test_twin_runner_seed_independence()

### Community 25 - "named_states"
Cohesion: 0.28
Nodes (5): channel_masks(), named_states(), test_channel_split(), test_named_state_energies_and_resonance(), setup()

### Community 26 - "Compute: laptop for light work, Perlmutter for heavy jobs"
Cohesion: 0.25
Nodes (7): Alternatives considered, Compute: laptop for light work, Perlmutter for heavy jobs, Consequences, Decision, Why, Actions taken, pick_device()

### Community 27 - "Package build: plan audit, Gauge-JEPA-P v2 and the starter package"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Package build: plan audit, Gauge-JEPA-P v2 and the starter package, Problems and assumptions, Results and what they mean, What was asked

### Community 28 - "Compute update 2: safe laptop and a pull-based job queue for Perlmutter"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Compute update 2: safe laptop and a pull-based job queue for Perlmutter, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 29 - "Compute update 3: laptop and Perlmutter only, environment repair prompt, self-healing runners"
Cohesion: 0.25
Nodes (8): Actions taken, Bugs found and fixed while doing this, Code graph, Compute update 3: laptop and Perlmutter only, environment repair prompt, self-healing runners, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 30 - "{{title}}"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Problems and assumptions, Results and what they mean, {{title}}, What was asked

### Community 31 - "Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`)"
Cohesion: 0.29
Nodes (6): Analysis plan (exact commands), Exclusion rules, Frozen inputs (fill in), Hypotheses (from PLAN §11), Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`), Signatures

### Community 32 - "su2qc-jepa — Gauge-JEPA-P v2 starter package"
Cohesion: 0.29
Nodes (6): First two sessions on the laptop, Five-minute tour, Install on the laptop (done by prompts/009), Layout, su2qc-jepa — Gauge-JEPA-P v2 starter package, What is verified today (`python scripts/run.py -- python -m pytest -q`: 47 fast tests; `-m slow` adds 1 more)

### Community 33 - "Conventions update: numbered artifacts and the Graphify code graph"
Cohesion: 0.29
Nodes (7): Actions taken, Code graph, Conventions update: numbered artifacts and the Graphify code graph, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 34 - "Compute update: laptop for light work, Perlmutter for heavy jobs"
Cohesion: 0.29
Nodes (6): Code graph, Compute update: laptop for light work, Perlmutter for heavy jobs, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 35 - "Perlmutter worker install keeps the user's other scrontab entries"
Cohesion: 0.29
Nodes (7): Actions taken, Code graph, Next action, Perlmutter worker install keeps the user's other scrontab entries, Problems and assumptions, Results and what they mean, What was asked

### Community 36 - "test_chain_cz_budget_PA"
Cohesion: 0.33
Nodes (3): cz_count(), trotter_error(), test_chain_cz_budget_PA()

### Community 38 - "Heavy jobs: the job queue and the Perlmutter worker"
Cohesion: 0.33
Nodes (5): Costs and limits, Heavy jobs: the job queue and the Perlmutter worker, One-time setup (Digonto, about 30 minutes, after the repository exists on GitHub), Self-healing, When something is wrong

### Community 39 - "{{title}}"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences (what must be re-run or re-checked), Decision, {{title}}, Why

### Community 40 - "{{title}}"
Cohesion: 0.33
Nodes (5): Context, Definition of done, Out of scope / stop conditions, Tasks, {{title}}

## Knowledge Gaps
- **151 isolated node(s):** `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script`, `PYTHONHASHSEED`, `replicate.sh script` (+146 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 377 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **27 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `main` to `su2qc-jepa — Gauge-JEPA-P v2 starter package`, `localrun.py`, `prompts/INDEX.md`, `Heavy jobs: the job queue and the Perlmutter worker`, `Worker`, `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier`, `CLAUDE.md — rules for every Claude Code session in `su2qc-jepa``, `retry_resources`, `Compute update 2: safe laptop and a pull-based job queue for Perlmutter`?**
  _High betweenness centrality (0.199) - this node is a cross-community bridge._
- **Why does `PlaquetteModel` connect `PlaquetteModel` to `trajectories.py`, `Conventions update: numbered artifacts and the Graphify code graph`, `.full_space_vectors`, `run_j0`, `m_values`, `test_jmax1_counts`, `._apply_term`, `named_states`, `model`?**
  _High betweenness centrality (0.104) - this node is a cross-community bridge._
- **Why does `Tasks` connect `prompts/INDEX.md` to `main`?**
  _High betweenness centrality (0.100) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `PlaquetteModel` (e.g. with `Code graph` and `_Cache`) actually correct?**
  _`PlaquetteModel` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `run_j0()` (e.g. with `ChainSpec` and `ObservableSet`) actually correct?**
  _`run_j0()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script` to the rest of the system?**
  _151 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `trajectories.py` be split into smaller, more focused modules?**
  _Cohesion score 0.057512797350195724 - nodes in this community are weakly interconnected._