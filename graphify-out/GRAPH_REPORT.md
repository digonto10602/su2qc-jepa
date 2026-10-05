# Graph Report - su2qc-jepa  (2026-10-05)

## Corpus Check
- 115 files · ~73,733 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 3, .cff 1)

## Summary
- 931 nodes · 1775 edges · 80 communities (44 shown, 36 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 108 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ee586790`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- train.py
- localrun.py
- chain.py
- pathlib
- CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`
- artifacts.py
- ibm.py
- Worker
- PlaquetteModel
- retry_resources
- trajectories.py
- test_crosscheck.py
- Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier
- LinkSpace
- test_pipeline.py
- dynamics.py
- su2.py
- train_jepa.py
- FullSpaceOperators
- crosscheck_su2qc.py
- MatterSpace
- test_committed_graph_is_fresh
- M1: su2qc cross-check PASS, three datasets built, gate J0 PASS
- estimate_chain
- Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code)
- prompts/INDEX.md
- ObservableSet
- scripts/run.py
- 10. Week by week — what Claude Code does, what is tested, what we expect
- M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED
- ._apply_term
- Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`)
- Package build: plan audit, Gauge-JEPA-P v2 and the starter package
- Conventions update: numbered artifacts and the Graphify code graph
- Compute update 2: safe laptop and a pull-based job queue for Perlmutter
- Perlmutter worker install keeps the user's other scrontab entries
- residual_eval.py
- _Cache
- {{title}}
- Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`)
- M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)
- su2qc-jepa — Gauge-JEPA-P v2 starter package
- TwinRunner
- M0 — Bootstrap (first Claude Code invocation, ~45 min)
- M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card
- Results and what they mean
- M0: repository created, CI green, code graph committed
- {{title}}
- {{title}}
- M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)
- M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)
- M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version.
- plans/INDEX.md
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
- `Code graph` --references--> `PlaquetteModel`  [INFERRED]
  reports/001_conventions-update-numbered-artifacts-and-the-graphify-code.md → src/su2qc_jepa/physics/plaquette.py
- `Actions taken` --references--> `check_artifacts()`  [INFERRED]
  reports/003_compute-update-2-safe-laptop-and-a-pull-based-job-queue-for.md → src/su2qc_jepa/repo/artifacts.py
- `Bugs found and fixed while doing this` --references--> `check_artifacts()`  [INFERRED]
  reports/004_compute-update-3-laptop-and-perlmutter-only-environment-repa.md → src/su2qc_jepa/repo/artifacts.py
- `W4 (26 Oct – 1 Nov) — J2, pilot job; end of the one-month version` --references--> `estimate_qpu_seconds()`  [INFERRED]
  plans/001_gauge-jepa-p-v2.md → src/su2qc_jepa/hardware/ibm.py

## Import Cycles
- None detected.

## Communities (80 total, 36 thin omitted)

### Community 0 - "train.py"
Cohesion: 0.06
Nodes (28): Actions taken, Code graph, Laptop check, 10 epochs, 1 seed (`runs/v1_check/seed0/history.json`, local; validation split), M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914), Next action, Options for Digonto (a decision record in `decisions/` is needed for any of B–D, before the 16 Oct preregistration), Problems and assumptions, Results and what they mean (+20 more)

### Community 1 - "localrun.py"
Cohesion: 0.06
Nodes (37): Actions taken, parse_steps(), validate_job(), admit(), _arg(), classify(), estimate_minutes(), heal_decision() (+29 more)

### Community 2 - "chain.py"
Cohesion: 0.06
Nodes (29): Claims ledger — every substantive statement, its status and its evidence, 12. Error budget (lines, each measured), _bond_rotation(), build_chain_circuit(), z_layer(), build_chain_prep_circuit(), chain_amplitudes(), chain_sector_unitary() (+21 more)

### Community 3 - "pathlib"
Cohesion: 0.07
Nodes (23): run_j0(), run_j1(), run_j2(), auroc(), run_j3(), spearman(), _fmt(), GateResult (+15 more)

### Community 4 - "CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`"
Cohesion: 0.05
Nodes (37): 1. Priorities, in order, 2. Session protocol (every session, no exceptions), 3. Frozen things (changing any of these needs a new `decisions/` record and a new version tag), 4. Hardware rules (non-negotiable), 5. Compute rules (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`), 6. Writing rules (reports, prompts, docs, paper), 7. What the package already guarantees (do not re-derive, do re-run), 8. Where things are (+29 more)

### Community 5 - "artifacts.py"
Cohesion: 0.11
Nodes (23): Artifact, check_artifacts(), list_artifacts(), new_artifact(), next_number(), read_front_matter(), render_index(), _resolve() (+15 more)

### Community 6 - "ibm.py"
Cohesion: 0.09
Nodes (13): BudgetError, calibration_snapshot(), check_budget(), collect(), dry_run(), DryRunSummary, estimate_qpu_seconds(), _hash_circuits() (+5 more)

### Community 7 - "Worker"
Cohesion: 0.18
Nodes (5): hms_to_hours(), main(), now(), sh(), Worker

### Community 9 - "retry_resources"
Cohesion: 0.09
Nodes (21): Alternatives considered, Compute: laptop and Perlmutter only, admission-controlled laptop runner, self-healing jobs, Consequences (what must be re-run or re-checked), Decision, Why, Costs and limits, Heavy jobs: the job queue and the Perlmutter worker, One-time setup (Digonto, about 30 minutes, after the repository exists on GitHub) (+13 more)

### Community 10 - "trajectories.py"
Cohesion: 0.19
Nodes (6): estimate_diagonal(), Record, sample_exact_chain(), sample_exact_diagonal(), chain_point_records(), test_estimators_unbiased()

### Community 12 - "Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier"
Cohesion: 0.12
Nodes (16): 0. The idea in one paragraph, 11. Preregistered hypotheses and expected results, 13. Publishability, 14. Assumptions, risks, open points, 16. Compute: the laptop and Perlmutter only (amended 2 Oct 2026; `decisions/004`, superseding `decisions/003` and `decisions/002`), 2. Why v2 is better — side by side, 3. Physics object (frozen) and measured fingerprints, 4. The Krylov-chain carrier (KC) (+8 more)

### Community 13 - "LinkSpace"
Cohesion: 0.16
Nodes (3): LinkSpace, m_values(), spin_matrices()

### Community 14 - "test_pipeline.py"
Cohesion: 0.35
Nodes (8): DatasetConfig, FamilyConfig, generate_dataset(), load_dataset(), test_chain_dataset_uses_chain_carrier(), test_dataset_generation_and_splits(), test_jepa_ema_target_and_curriculum(), test_jepa_trains_one_epoch()

### Community 15 - "dynamics.py"
Cohesion: 0.22
Nodes (3): evolve(), Krylov, lanczos()

### Community 17 - "su2.py"
Cohesion: 0.19
Nodes (3): _cg_cached(), clebsch_gordan(), _fact()

### Community 20 - "crosscheck_su2qc.py"
Cohesion: 0.26
Nodes (6): compare_point(), extract_terms(), import_su2qc(), main(), sign_gauge(), su2qc_label_to_c()

### Community 24 - "test_committed_graph_is_fresh"
Cohesion: 0.20
Nodes (8): Actions taken, Code graph, Laptop environments: coding repaired, su2qc-jepa created, Next action, Problems and assumptions, What was asked, Actions taken, test_committed_graph_is_fresh()

### Community 25 - "M1: su2qc cross-check PASS, three datasets built, gate J0 PASS"
Cohesion: 0.18
Nodes (10): Actions taken, Code graph, M1: su2qc cross-check PASS, three datasets built, gate J0 PASS, Next action, Part A — route C agrees with both su2qc routes (`evidence/J0_data/crosscheck_su2qc.json`, commit `0bb5d6d`, status PASS), Part B — datasets (`evidence/J0_data/datasets.json`, commit `358d0bd`), Part C — gate J0 PASS (`evidence/J0_data/20261003T201012Z.json`, 15 s on the laptop), Problems and assumptions (+2 more)

### Community 26 - "estimate_chain"
Cohesion: 0.22
Nodes (4): _bits_from_key(), estimate_chain(), ObservationSpec, test_observation_spec_roundtrip()

### Community 27 - "Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code)"
Cohesion: 0.20
Nodes (10): Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code), Model, Observables, Predicted results, Problems and assumptions, Publishability, Schedule (5 Oct – 29 Nov 2026), Testing ladder (budgets are Claude's estimates) (+2 more)

### Community 28 - "prompts/INDEX.md"
Cohesion: 0.20
Nodes (5): Expected, M6 — Hardware day 3, gate J3, error budget (W6, 2 sessions), M7 — One stretch item (W7), chosen on 15 Nov by Digonto, M8 — Paper assembly, release, replication (W8, 2 sessions), Prompts — index

### Community 31 - "scripts/run.py"
Cohesion: 0.28
Nodes (3): dataset_step(), guess_outputs(), queue()

### Community 32 - "10. Week by week — what Claude Code does, what is tested, what we expect"
Cohesion: 0.22
Nodes (9): 10. Week by week — what Claude Code does, what is tested, what we expect, W1 (5–11 Oct) — bootstrap, physics cross-check, data → J0, W2 (12–18 Oct) — JEPA v1, collapse diagnostics, preregistration → J1, W3 (19–25 Oct) — forecasting, twin rehearsal, hardware dry runs, W4 (26 Oct – 1 Nov) — J2, pilot job; end of the one-month version, W5 (2–8 Nov) — hardware days 1 and 2, W6 (9–15 Nov) — day 3, J3, advantage-free analysis, W7 (16–22 Nov) — one stretch item, chosen on 15 Nov (+1 more)

### Community 33 - "M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED"
Cohesion: 0.22
Nodes (7): Code graph, M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED, Next action, Problems and assumptions, Results and what they mean, What was asked, test_run_py_retries_after_memory_limit()

### Community 36 - "Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`)"
Cohesion: 0.25
Nodes (8): Absolute safety rules (you have no permission prompts), Context, Definition of done, Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`), Phase A — inventory and backup (no changes), Phase B — repair `coding` (only after rule 4 allows it), Phase C — create `su2qc-jepa` (safe to do at any time; it touches no existing environment), Phase D — report

### Community 37 - "Package build: plan audit, Gauge-JEPA-P v2 and the starter package"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Package build: plan audit, Gauge-JEPA-P v2 and the starter package, Problems and assumptions, Results and what they mean, What was asked

### Community 38 - "Conventions update: numbered artifacts and the Graphify code graph"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Conventions update: numbered artifacts and the Graphify code graph, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 39 - "Compute update 2: safe laptop and a pull-based job queue for Perlmutter"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Compute update 2: safe laptop and a pull-based job queue for Perlmutter, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 40 - "Perlmutter worker install keeps the user's other scrontab entries"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Perlmutter worker install keeps the user's other scrontab entries, Problems and assumptions, Results and what they mean, What was asked

### Community 41 - "residual_eval.py"
Cohesion: 0.32
Nodes (3): estimate(), krylov(), subsample()

### Community 42 - "_Cache"
Cohesion: 0.36
Nodes (3): _Cache, _checksum(), _initial_state()

### Community 43 - "{{title}}"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Problems and assumptions, Results and what they mean, {{title}}, What was asked

### Community 44 - "Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`)"
Cohesion: 0.29
Nodes (6): Analysis plan (exact commands), Exclusion rules, Frozen inputs (fill in), Hypotheses (from PLAN §11), Preregistration — Gauge-JEPA-P v2 (to be signed by tag `prereg-2026-10-16`), Signatures

### Community 45 - "M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)"
Cohesion: 0.29
Nodes (6): Expected, M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h), Part A — cross-check against the project's verified `su2qc` code, Part B — datasets, Part C — gate, Tests to add

### Community 46 - "su2qc-jepa — Gauge-JEPA-P v2 starter package"
Cohesion: 0.29
Nodes (6): First two sessions on the laptop, Five-minute tour, Install on the laptop (done by prompts/009), Layout, su2qc-jepa — Gauge-JEPA-P v2 starter package, What is verified today (`python scripts/run.py -- python -m pytest -q`: 47 fast tests; `-m slow` adds 1 more)

### Community 48 - "M0 — Bootstrap (first Claude Code invocation, ~45 min)"
Cohesion: 0.33
Nodes (5): Context, Definition of done, M0 — Bootstrap (first Claude Code invocation, ~45 min), Out of scope, Tasks

### Community 49 - "M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card"
Cohesion: 0.33
Nodes (5): Context, Definition of done, M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card, Out of scope / stop conditions, Tasks

### Community 50 - "Results and what they mean"
Cohesion: 0.33
Nodes (6): `coding`: imports before and after (`import-before.json` → `import-after.json`), Disk, `pip check`, Results and what they mean, `su2qc-jepa` environment, The GTX 1060 (compute capability 6.1, driver 580.178.04, CUDA 13.0 driver API)

### Community 51 - "M0: repository created, CI green, code graph committed"
Cohesion: 0.33
Nodes (6): Code graph, M0: repository created, CI green, code graph committed, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 52 - "{{title}}"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences (what must be re-run or re-checked), Decision, {{title}}, Why

### Community 53 - "{{title}}"
Cohesion: 0.33
Nodes (5): Context, Definition of done, Out of scope / stop conditions, Tasks, {{title}}

### Community 54 - "M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)"
Cohesion: 0.40
Nodes (4): Expected, M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions), Session M2a — make the model healthy, Session M2b — preregistration (16 Oct)

### Community 55 - "M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)"
Cohesion: 0.40
Nodes (4): Expected, M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions), Session M3a — forecasting, Session M3b — twin and dry run

### Community 56 - "M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version."
Cohesion: 0.40
Nodes (4): Expected, M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version., Session M4a — J2 (30 Oct), Session M4b — pilot (one job)

## Knowledge Gaps
- **187 isolated node(s):** `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script`, `PYTHONHASHSEED`, `replicate.sh script` (+182 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 438 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **36 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PlaquetteModel` connect `PlaquetteModel` to `chain.py`, `pathlib`, `._apply_term`, `Conventions update: numbered artifacts and the Graphify code graph`, `trajectories.py`, `_Cache`, `LinkSpace`, `test_pipeline.py`, `plaquette.py`, `crosscheck_su2qc.py`, `ObservableSet`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Why does `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier` connect `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier` to `10. Week by week — what Claude Code does, what is tested, what we expect`, `chain.py`, `CLAUDE.md — rules for every Claude Code session in `su2qc-jepa``, `TwinRunner`, `plans/INDEX.md`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `retry_resources()` connect `retry_resources` to `localrun.py`, `Worker`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `PlaquetteModel` (e.g. with `Code graph` and `compare_point()`) actually correct?**
  _`PlaquetteModel` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `run_j0()` (e.g. with `ChainSpec` and `ObservableSet`) actually correct?**
  _`run_j0()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script` to the rest of the system?**
  _187 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `train.py` be split into smaller, more focused modules?**
  _Cohesion score 0.059395801331285206 - nodes in this community are weakly interconnected._