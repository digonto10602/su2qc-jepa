# Graph Report - su2qc-jepa  (2026-10-02)

## Corpus Check
- 106 files · ~63,804 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 3, .cff 1)

## Summary
- 850 nodes · 1627 edges · 60 communities (37 shown, 23 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 98 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `73a1ae53`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- PlaquetteModel
- Worker
- train.py
- chain.py
- prompts/INDEX.md
- artifacts.py
- localrun.py
- test_physics.py
- ibm.py
- j0_data.py
- FullSpaceOperators
- pathlib
- train_jepa.py
- Krylov
- main
- Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code)
- Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier
- ObservableSet
- decisions/INDEX.md
- test_committed_graph_is_fresh
- 5. Compute rules (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`)
- graph.py
- noise.py
- CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`
- Numbered artifacts and the Graphify code graph
- Package build: plan audit, Gauge-JEPA-P v2 and the starter package
- Conventions update: numbered artifacts and the Graphify code graph
- Perlmutter worker install keeps the user's other scrontab entries
- {{title}}
- Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`)
- su2qc-jepa — Gauge-JEPA-P v2 starter package
- Compute update: laptop for light work, Perlmutter for heavy jobs
- Compute update 2: safe laptop and a pull-based job queue for Perlmutter
- M0: repository created, CI green, code graph committed
- Results and what they mean
- {{title}}
- {{title}}
- reports/INDEX.md
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
- `Tasks` --references--> `main()`  [INFERRED]
  prompts/000_bootstrap.md → scripts/worker/worker.py
- `What is verified today (`python scripts/run.py -- python -m pytest -q`: 47 fast tests; `-m slow` adds 1 more)` --references--> `main()`  [INFERRED]
  README.md → scripts/worker/worker.py
- `Results and what they mean` --references--> `main()`  [INFERRED]
  reports/003_compute-update-2-safe-laptop-and-a-pull-based-job-queue-for.md → scripts/worker/worker.py

## Import Cycles
- None detected.

## Communities (60 total, 23 thin omitted)

### Community 0 - "PlaquetteModel"
Cohesion: 0.05
Nodes (9): _Cache, GIBasisState, LinkSpace, PlaquetteModel, _cg_cached(), clebsch_gordan(), _fact(), m_values() (+1 more)

### Community 1 - "Worker"
Cohesion: 0.06
Nodes (28): Alternatives considered, Compute: laptop and Perlmutter only, admission-controlled laptop runner, self-healing jobs, Consequences (what must be re-run or re-checked), Decision, Why, Actions taken, Code graph, Compute update 3: laptop and Perlmutter only, environment repair prompt, self-healing runners (+20 more)

### Community 2 - "train.py"
Cohesion: 0.07
Nodes (23): FamilyConfig, load_dataset(), ActionPredictor, effective_rank(), GaugeJEPA, JEPAConfig, MLP, sigreg_loss() (+15 more)

### Community 3 - "chain.py"
Cohesion: 0.07
Nodes (24): 12. Error budget (lines, each measured), 1. Audit of the 1 Oct plan — issues found and what changed, _bond_rotation(), build_chain_circuit(), z_layer(), build_chain_prep_circuit(), chain_amplitudes(), chain_sector_unitary() (+16 more)

### Community 4 - "prompts/INDEX.md"
Cohesion: 0.04
Nodes (38): Context, Definition of done, M0 — Bootstrap (first Claude Code invocation, ~45 min), Out of scope, Tasks, Expected, M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h), Part A — cross-check against the project's verified `su2qc` code (+30 more)

### Community 5 - "artifacts.py"
Cohesion: 0.08
Nodes (19): Bugs found and fixed while doing this, Results and what they mean, Artifact, check_artifacts(), list_artifacts(), new_artifact(), next_number(), read_front_matter() (+11 more)

### Community 6 - "localrun.py"
Cohesion: 0.10
Nodes (25): dataset_step(), guess_outputs(), queue(), admit(), _arg(), classify(), estimate_minutes(), heal_decision() (+17 more)

### Community 7 - "test_physics.py"
Cohesion: 0.07
Nodes (8): Claims ledger — every substantive statement, its status and its evidence, channel_masks(), model(), test_chain_prep_cascade(), test_channel_split(), test_jmax1_counts(), test_named_state_energies_and_resonance(), test_two_routes_agree_and_gauss_law()

### Community 8 - "ibm.py"
Cohesion: 0.10
Nodes (14): W4 (26 Oct – 1 Nov) — J2, pilot job; end of the one-month version, BudgetError, calibration_snapshot(), check_budget(), collect(), dry_run(), DryRunSummary, estimate_qpu_seconds() (+6 more)

### Community 9 - "j0_data.py"
Cohesion: 0.13
Nodes (13): _bits_from_key(), estimate_chain(), estimate_diagonal(), ObservationSpec, Record, sample_exact_chain(), sample_exact_diagonal(), _checksum() (+5 more)

### Community 10 - "FullSpaceOperators"
Cohesion: 0.14
Nodes (3): Couplings, FullSpaceOperators, MatterSpace

### Community 12 - "pathlib"
Cohesion: 0.16
Nodes (12): run_j1(), run_j2(), auroc(), run_j3(), spearman(), _fmt(), GateResult, GateRow (+4 more)

### Community 13 - "train_jepa.py"
Cohesion: 0.13
Nodes (6): estimate_hours(), load_compute(), _env(), _run(), test_add_to_empty_table_and_remove_last_entry(), test_add_update_remove_keeps_other_entries()

### Community 14 - "Krylov"
Cohesion: 0.16
Nodes (7): estimate(), krylov(), subsample(), evolve(), Krylov, krylov_error(), lanczos()

### Community 15 - "main"
Cohesion: 0.14
Nodes (16): Costs and limits, Heavy jobs: the job queue and the Perlmutter worker, One-time setup (Digonto, about 30 minutes, after the repository exists on GitHub), Self-healing, When something is wrong, 10. Week by week — what Claude Code does, what is tested, what we expect, 16. Compute: the laptop and Perlmutter only (amended 2 Oct 2026; `decisions/004`, superseding `decisions/003` and `decisions/002`), 6. Data (+8 more)

### Community 17 - "Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code)"
Cohesion: 0.14
Nodes (11): Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code), Model, Observables, Predicted results, Problems and assumptions, Publishability, Schedule (5 Oct – 29 Nov 2026), Testing ladder (budgets are Claude's estimates) (+3 more)

### Community 18 - "Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier"
Cohesion: 0.14
Nodes (14): 0. The idea in one paragraph, 11. Preregistered hypotheses and expected results, 13. Publishability, 14. Assumptions, risks, open points, 2. Why v2 is better — side by side, 3. Physics object (frozen) and measured fingerprints, 4. The Krylov-chain carrier (KC), 5. The world model (+6 more)

### Community 19 - "ObservableSet"
Cohesion: 0.27
Nodes (7): _initial_state(), sector_restrict(), named_states(), ObservableSet, test_dynamics_reproduce_preliminary_expectation(), test_krylov_dimension_window_PA(), setup()

### Community 20 - "decisions/INDEX.md"
Cohesion: 0.18
Nodes (7): Frozen conventions and coupling points, Alternatives considered, Compute: a safe laptop and a pull-based job queue for Perlmutter, Consequences, Decision, Why, Decisions — index

### Community 21 - "test_committed_graph_is_fresh"
Cohesion: 0.20
Nodes (7): Actions taken, Code graph, Laptop environments: coding repaired, su2qc-jepa created, Next action, Problems and assumptions, What was asked, test_committed_graph_is_fresh()

### Community 22 - "5. Compute rules (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`)"
Cohesion: 0.20
Nodes (9): 5. Compute rules (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`), Alternatives considered, Compute: laptop for light work, Perlmutter for heavy jobs, Consequences, Decision, Why, Actions taken, git() (+1 more)

### Community 23 - "graph.py"
Cohesion: 0.29
Nodes (6): _edges(), graph_stats(), load_graph(), same_structure(), structure_signature(), test_graph_helpers()

### Community 24 - "noise.py"
Cohesion: 0.24
Nodes (4): heron_like_noise_model(), HeronLike, noise_model_from_backend(), save_noise_summary()

### Community 25 - "CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`"
Cohesion: 0.22
Nodes (8): 1. Priorities, in order, 3. Frozen things (changing any of these needs a new `decisions/` record and a new version tag), 4. Hardware rules (non-negotiable), 6. Writing rules (reports, prompts, docs, paper), 7. What the package already guarantees (do not re-derive, do re-run), 8. Where things are, CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`, graphify

### Community 26 - "Numbered artifacts and the Graphify code graph"
Cohesion: 0.22
Nodes (7): 2. Session protocol (every session, no exceptions), Alternatives considered, Consequences, Decision, Numbered artifacts and the Graphify code graph, Why, 15. Repository conventions — numbered artifacts and the code graph (added 2 Oct 2026; `decisions/001`)

### Community 27 - "Package build: plan audit, Gauge-JEPA-P v2 and the starter package"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Package build: plan audit, Gauge-JEPA-P v2 and the starter package, Problems and assumptions, Results and what they mean, What was asked

### Community 28 - "Conventions update: numbered artifacts and the Graphify code graph"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Conventions update: numbered artifacts and the Graphify code graph, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 29 - "Perlmutter worker install keeps the user's other scrontab entries"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Perlmutter worker install keeps the user's other scrontab entries, Problems and assumptions, Results and what they mean, What was asked

### Community 30 - "{{title}}"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Problems and assumptions, Results and what they mean, {{title}}, What was asked

### Community 31 - "Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`)"
Cohesion: 0.29
Nodes (6): Analysis plan (exact commands), Exclusion rules, Frozen inputs (fill in), Hypotheses (from PLAN §11), Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`), Signatures

### Community 32 - "su2qc-jepa — Gauge-JEPA-P v2 starter package"
Cohesion: 0.29
Nodes (6): First two sessions on the laptop, Five-minute tour, Install on the laptop (done by prompts/009), Layout, su2qc-jepa — Gauge-JEPA-P v2 starter package, What is verified today (`python scripts/run.py -- python -m pytest -q`: 47 fast tests; `-m slow` adds 1 more)

### Community 33 - "Compute update: laptop for light work, Perlmutter for heavy jobs"
Cohesion: 0.29
Nodes (6): Code graph, Compute update: laptop for light work, Perlmutter for heavy jobs, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 34 - "Compute update 2: safe laptop and a pull-based job queue for Perlmutter"
Cohesion: 0.29
Nodes (7): Actions taken, Code graph, Compute update 2: safe laptop and a pull-based job queue for Perlmutter, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 35 - "M0: repository created, CI green, code graph committed"
Cohesion: 0.29
Nodes (7): Actions taken, Code graph, M0: repository created, CI green, code graph committed, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 36 - "Results and what they mean"
Cohesion: 0.33
Nodes (6): `coding`: imports before and after (`import-before.json` → `import-after.json`), Disk, `pip check`, Results and what they mean, `su2qc-jepa` environment, The GTX 1060 (compute capability 6.1, driver 580.178.04, CUDA 13.0 driver API)

### Community 37 - "{{title}}"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences (what must be re-run or re-checked), Decision, {{title}}, Why

### Community 38 - "{{title}}"
Cohesion: 0.33
Nodes (5): Context, Definition of done, Out of scope / stop conditions, Tasks, {{title}}

## Knowledge Gaps
- **155 isolated node(s):** `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script`, `PYTHONHASHSEED`, `replicate.sh script` (+150 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 381 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `main` to `su2qc-jepa — Gauge-JEPA-P v2 starter package`, `Worker`, `Compute update 2: safe laptop and a pull-based job queue for Perlmutter`, `M0: repository created, CI green, code graph committed`, `prompts/INDEX.md`, `decisions/INDEX.md`, `5. Compute rules (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`)`?**
  _High betweenness centrality (0.206) - this node is a cross-community bridge._
- **Why does `Tasks` connect `prompts/INDEX.md` to `main`?**
  _High betweenness centrality (0.099) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `PlaquetteModel` (e.g. with `Code graph` and `_Cache`) actually correct?**
  _`PlaquetteModel` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `run_j0()` (e.g. with `ChainSpec` and `ObservableSet`) actually correct?**
  _`run_j0()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script` to the rest of the system?**
  _155 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `PlaquetteModel` be split into smaller, more focused modules?**
  _Cohesion score 0.05201266395296246 - nodes in this community are weakly interconnected._
- **Should `Worker` be split into smaller, more focused modules?**
  _Cohesion score 0.06060606060606061 - nodes in this community are weakly interconnected._