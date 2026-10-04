# Graph Report - su2qc-jepa  (2026-10-03)

## Corpus Check
- 111 files · ~68,858 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 3, .cff 1)

## Summary
- 893 nodes · 1697 edges · 64 communities (38 shown, 26 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 89 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0cff86f0`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- FullSpaceOperators
- localrun.py
- train.py
- chain.py
- prompts/INDEX.md
- reports/INDEX.md
- artifacts.py
- ibm.py
- graph.py
- Worker
- PlaquetteModel
- ledger.py
- trajectories.py
- j0_data.py
- plaquette.py
- ObservableSet
- Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier
- test_crosscheck.py
- Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code)
- Compute: laptop for light work, Perlmutter for heavy jobs
- decisions/INDEX.md
- crosscheck_su2qc.py
- CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`
- test_dataset_generation_and_splits
- test_jobs.py
- TwinRunner
- Numbered artifacts and the Graphify code graph
- 10. Week by week — what Claude Code does, what is tested, what we expect
- jobs.py
- Compute update 3: laptop and Perlmutter only, environment repair prompt, self-healing runners
- test_worker_slurm_mode_resubmits_after_timeout
- noise.py
- {{title}}
- Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`)
- su2qc-jepa — Gauge-JEPA-P v2 starter package
- Compute update: laptop for light work, Perlmutter for heavy jobs
- _Cache
- Heavy jobs: the job queue and the Perlmutter worker
- M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED
- residual_eval.py
- {{title}}
- {{title}}
- Compute: laptop and Perlmutter only, admission-controlled laptop runner, self-healing jobs
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
4. `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier` - 20 edges
5. `ObservableSet` - 19 edges
6. `generate_dataset()` - 18 edges
7. `ChainSpec` - 16 edges
8. `lanczos()` - 15 edges
9. `GateResult` - 14 edges
10. `Krylov` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Consequences (what must be re-run or re-checked)` --references--> `retry_resources()`  [INFERRED]
  decisions/004_compute-laptop-and-perlmutter-only-admission-controlled-lapt.md → src/su2qc_jepa/jobs.py
- `Decision` --references--> `retry_resources()`  [INFERRED]
  decisions/004_compute-laptop-and-perlmutter-only-admission-controlled-lapt.md → src/su2qc_jepa/jobs.py
- `Self-healing` --references--> `retry_resources()`  [INFERRED]
  docs/PERLMUTTER.md → src/su2qc_jepa/jobs.py
- `Actions taken` --references--> `retry_resources()`  [INFERRED]
  reports/004_compute-update-3-laptop-and-perlmutter-only-environment-repa.md → src/su2qc_jepa/jobs.py
- `12. Error budget (lines, each measured)` --references--> `trotter_error()`  [INFERRED]
  plans/001_gauge-jepa-p-v2.md → src/su2qc_jepa/physics/chain.py

## Import Cycles
- None detected.

## Communities (64 total, 26 thin omitted)

### Community 0 - "FullSpaceOperators"
Cohesion: 0.06
Nodes (9): Couplings, FullSpaceOperators, LinkSpace, MatterSpace, _cg_cached(), clebsch_gordan(), _fact(), m_values() (+1 more)

### Community 1 - "localrun.py"
Cohesion: 0.07
Nodes (33): Problems and assumptions, Problems and assumptions, dataset_step(), guess_outputs(), queue(), parse_steps(), admit(), _arg() (+25 more)

### Community 2 - "train.py"
Cohesion: 0.07
Nodes (19): ActionPredictor, effective_rank(), GaugeJEPA, JEPAConfig, MLP, sigreg_loss(), baseline_autoregressive(), baseline_ridge() (+11 more)

### Community 3 - "chain.py"
Cohesion: 0.06
Nodes (25): Claims ledger — every substantive statement, its status and its evidence, _bond_rotation(), build_chain_circuit(), z_layer(), build_chain_prep_circuit(), chain_amplitudes(), chain_sector_unitary(), ChainSpec (+17 more)

### Community 4 - "prompts/INDEX.md"
Cohesion: 0.04
Nodes (38): Context, Definition of done, M0 — Bootstrap (first Claude Code invocation, ~45 min), Out of scope, Tasks, Expected, M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h), Part A — cross-check against the project's verified `su2qc` code (+30 more)

### Community 5 - "reports/INDEX.md"
Cohesion: 0.04
Nodes (38): Actions taken, Code graph, Next action, Package build: plan audit, Gauge-JEPA-P v2 and the starter package, Problems and assumptions, Results and what they mean, What was asked, Actions taken (+30 more)

### Community 6 - "artifacts.py"
Cohesion: 0.10
Nodes (17): Artifact, check_artifacts(), list_artifacts(), new_artifact(), next_number(), read_front_matter(), render_index(), _resolve() (+9 more)

### Community 7 - "ibm.py"
Cohesion: 0.07
Nodes (16): W4 (26 Oct – 1 Nov) — J2, pilot job; end of the one-month version, estimate_hours(), load_compute(), BudgetError, calibration_snapshot(), check_budget(), collect(), dry_run() (+8 more)

### Community 8 - "graph.py"
Cohesion: 0.07
Nodes (26): Actions taken, Code graph, `coding`: imports before and after (`import-before.json` → `import-after.json`), Disk, Laptop environments: coding repaired, su2qc-jepa created, Next action, `pip check`, Problems and assumptions (+18 more)

### Community 9 - "Worker"
Cohesion: 0.18
Nodes (5): hms_to_hours(), main(), now(), sh(), Worker

### Community 11 - "ledger.py"
Cohesion: 0.15
Nodes (12): run_j1(), run_j2(), auroc(), run_j3(), spearman(), _fmt(), GateResult, GateRow (+4 more)

### Community 13 - "trajectories.py"
Cohesion: 0.17
Nodes (10): _bits_from_key(), estimate_chain(), estimate_diagonal(), ObservationSpec, Record, sample_exact_chain(), sample_exact_diagonal(), _checksum() (+2 more)

### Community 14 - "j0_data.py"
Cohesion: 0.17
Nodes (8): krylov(), run_j0(), evolve(), Krylov, krylov_error(), lanczos(), sector_restrict(), test_krylov_dimension_window_PA()

### Community 16 - "ObservableSet"
Cohesion: 0.15
Nodes (7): compare_point(), channel_masks(), named_states(), ObservableSet, test_dynamics_reproduce_preliminary_expectation(), test_named_state_energies_and_resonance(), setup()

### Community 17 - "Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier"
Cohesion: 0.12
Nodes (17): 0. The idea in one paragraph, 11. Preregistered hypotheses and expected results, 12. Error budget (lines, each measured), 13. Publishability, 14. Assumptions, risks, open points, 16. Compute: the laptop and Perlmutter only (amended 2 Oct 2026; `decisions/004`, superseding `decisions/003` and `decisions/002`), 2. Why v2 is better — side by side, 3. Physics object (frozen) and measured fingerprints (+9 more)

### Community 19 - "Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code)"
Cohesion: 0.14
Nodes (11): Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code), Model, Observables, Predicted results, Problems and assumptions, Publishability, Schedule (5 Oct – 29 Nov 2026), Testing ladder (budgets are Claude's estimates) (+3 more)

### Community 20 - "Compute: laptop for light work, Perlmutter for heavy jobs"
Cohesion: 0.17
Nodes (9): 5. Compute rules (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`), Alternatives considered, Compute: laptop for light work, Perlmutter for heavy jobs, Consequences, Decision, Why, 1. Audit of the 1 Oct plan — issues found and what changed, Actions taken (+1 more)

### Community 21 - "decisions/INDEX.md"
Cohesion: 0.17
Nodes (7): Frozen conventions and coupling points, Alternatives considered, Compute: a safe laptop and a pull-based job queue for Perlmutter, Consequences, Decision, Why, Decisions — index

### Community 22 - "crosscheck_su2qc.py"
Cohesion: 0.25
Nodes (5): extract_terms(), import_su2qc(), main(), sign_gauge(), su2qc_label_to_c()

### Community 23 - "CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`"
Cohesion: 0.22
Nodes (8): 1. Priorities, in order, 3. Frozen things (changing any of these needs a new `decisions/` record and a new version tag), 4. Hardware rules (non-negotiable), 6. Writing rules (reports, prompts, docs, paper), 7. What the package already guarantees (do not re-derive, do re-run), 8. Where things are, CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`, graphify

### Community 24 - "test_dataset_generation_and_splits"
Cohesion: 0.36
Nodes (5): DatasetConfig, FamilyConfig, load_dataset(), test_chain_dataset_uses_chain_carrier(), test_dataset_generation_and_splits()

### Community 25 - "test_jobs.py"
Cohesion: 0.31
Nodes (5): validate_job(), good_job(), test_allowlist_refuses(), test_valid_job_passes(), test_validation_catches_bad_fields()

### Community 26 - "TwinRunner"
Cohesion: 0.28
Nodes (4): heron_like_noise_model(), twin_variance_check(), TwinRunner, test_twin_runner_seed_independence()

### Community 27 - "Numbered artifacts and the Graphify code graph"
Cohesion: 0.25
Nodes (7): 2. Session protocol (every session, no exceptions), Alternatives considered, Consequences, Decision, Numbered artifacts and the Graphify code graph, Why, 15. Repository conventions — numbered artifacts and the code graph (added 2 Oct 2026; `decisions/001`)

### Community 28 - "10. Week by week — what Claude Code does, what is tested, what we expect"
Cohesion: 0.25
Nodes (8): 10. Week by week — what Claude Code does, what is tested, what we expect, W1 (5–11 Oct) — bootstrap, physics cross-check, data → J0, W2 (12–18 Oct) — JEPA v1, collapse diagnostics, preregistration → J1, W3 (19–25 Oct) — forecasting, twin rehearsal, hardware dry runs, W5 (2–8 Nov) — hardware days 1 and 2, W6 (9–15 Nov) — day 3, J3, advantage-free analysis, W7 (16–22 Nov) — one stretch item, chosen on 15 Nov, W8 (23–29 Nov) — paper, release, replication

### Community 29 - "jobs.py"
Cohesion: 0.29
Nodes (3): _hms(), retry_resources(), test_retry_rule()

### Community 30 - "Compute update 3: laptop and Perlmutter only, environment repair prompt, self-healing runners"
Cohesion: 0.25
Nodes (8): Actions taken, Bugs found and fixed while doing this, Code graph, Compute update 3: laptop and Perlmutter only, environment repair prompt, self-healing runners, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 31 - "test_worker_slurm_mode_resubmits_after_timeout"
Cohesion: 0.29
Nodes (5): Actions taken, _git(), test_worker_end_to_end_local(), ignore(), test_worker_slurm_mode_resubmits_after_timeout()

### Community 32 - "noise.py"
Cohesion: 0.29
Nodes (3): HeronLike, noise_model_from_backend(), save_noise_summary()

### Community 33 - "{{title}}"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Problems and assumptions, Results and what they mean, {{title}}, What was asked

### Community 34 - "Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`)"
Cohesion: 0.29
Nodes (6): Analysis plan (exact commands), Exclusion rules, Frozen inputs (fill in), Hypotheses (from PLAN §11), Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`), Signatures

### Community 35 - "su2qc-jepa — Gauge-JEPA-P v2 starter package"
Cohesion: 0.29
Nodes (6): First two sessions on the laptop, Five-minute tour, Install on the laptop (done by prompts/009), Layout, su2qc-jepa — Gauge-JEPA-P v2 starter package, What is verified today (`python scripts/run.py -- python -m pytest -q`: 47 fast tests; `-m slow` adds 1 more)

### Community 36 - "Compute update: laptop for light work, Perlmutter for heavy jobs"
Cohesion: 0.29
Nodes (6): Code graph, Compute update: laptop for light work, Perlmutter for heavy jobs, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 38 - "Heavy jobs: the job queue and the Perlmutter worker"
Cohesion: 0.33
Nodes (5): Costs and limits, Heavy jobs: the job queue and the Perlmutter worker, One-time setup (Digonto, about 30 minutes, after the repository exists on GitHub), Self-healing, When something is wrong

### Community 39 - "M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED"
Cohesion: 0.33
Nodes (5): Code graph, M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED, Next action, Results and what they mean, What was asked

### Community 41 - "{{title}}"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences (what must be re-run or re-checked), Decision, {{title}}, Why

### Community 42 - "{{title}}"
Cohesion: 0.33
Nodes (5): Context, Definition of done, Out of scope / stop conditions, Tasks, {{title}}

### Community 43 - "Compute: laptop and Perlmutter only, admission-controlled laptop runner, self-healing jobs"
Cohesion: 0.40
Nodes (5): Alternatives considered, Compute: laptop and Perlmutter only, admission-controlled laptop runner, self-healing jobs, Consequences (what must be re-run or re-checked), Decision, Why

## Knowledge Gaps
- **177 isolated node(s):** `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script`, `PYTHONHASHSEED`, `replicate.sh script` (+172 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 414 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **26 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PlaquetteModel` connect `PlaquetteModel` to `FullSpaceOperators`, `chain.py`, `_Cache`, `reports/INDEX.md`, `trajectories.py`, `j0_data.py`, `plaquette.py`, `ObservableSet`, `.full_space_vectors`, `crosscheck_su2qc.py`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Why does `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier` connect `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier` to `Numbered artifacts and the Graphify code graph`, `Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code)`, `10. Week by week — what Claude Code does, what is tested, what we expect`, `Compute: laptop for light work, Perlmutter for heavy jobs`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Why does `retry_resources()` connect `jobs.py` to `Worker`, `Compute: laptop and Perlmutter only, admission-controlled laptop runner, self-healing jobs`, `Heavy jobs: the job queue and the Perlmutter worker`, `Compute update 3: laptop and Perlmutter only, environment repair prompt, self-healing runners`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `PlaquetteModel` (e.g. with `Code graph` and `compare_point()`) actually correct?**
  _`PlaquetteModel` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `run_j0()` (e.g. with `ChainSpec` and `ObservableSet`) actually correct?**
  _`run_j0()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script` to the rest of the system?**
  _177 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `FullSpaceOperators` be split into smaller, more focused modules?**
  _Cohesion score 0.05928614640048397 - nodes in this community are weakly interconnected._