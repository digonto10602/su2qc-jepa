# Graph Report - su2qc-jepa  (2026-10-28)

## Corpus Check
- 134 files · ~134,544 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 3, .cff 1)

## Summary
- 1215 nodes · 2225 edges · 91 communities (54 shown, 37 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 174 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `44230474`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_j0
- chain.py
- localrun.py
- test_jobs.py
- ibm.py
- Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier
- Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)
- 9. Plot data (the data behind every figure; each table can be parsed as Markdown)
- artifacts.py
- trajectories.py
- Worker
- ledger.py
- retry_resources
- Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)
- PlaquetteModel
- Preregistration — Gauge-JEPA-P v2 (signed by tag `prereg-2026-10-16`)
- test_pipeline.py
- test_training_and_baselines_run_on_device
- argparse
- test_committed_graph_is_fresh
- train.py
- LinkSpace
- train_jepa.py
- jepa.py
- generate_dataset
- GaugeJEPA
- FullSpaceOperators
- MatterSpace
- su2.py
- Desktop GPU worker online; `v1_final` trained; preregistered J2 FAIL (on-family passes, strong coupling fails)
- CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`
- prompts/INDEX.md
- reports/INDEX.md
- M1: su2qc cross-check PASS, three datasets built, gate J0 PASS
- Model card — Gauge-JEPA-P v1 (working configuration after M2a)
- M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914)
- ._apply_term
- J3 gate scores the low-shot rows at the preregistered 512 shots
- Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`)
- Package build: plan audit, Gauge-JEPA-P v2 and the starter package
- Conventions update: numbered artifacts and the Graphify code graph
- Compute update 2: safe laptop and a pull-based job queue for Perlmutter
- Perlmutter worker install keeps the user's other scrontab entries
- {{title}}
- pick_device
- M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)
- su2qc-jepa — Gauge-JEPA-P v2 starter package
- Compute update: laptop for light work, Perlmutter for heavy jobs
- M0: repository created, CI green, code graph committed
- Compute: a safe laptop and a pull-based job queue for Perlmutter
- J1 energy grounding threshold set relative to the measured information ceiling
- Preregistration deviation: dataset-equivalence tolerance corrected to rounding scale
- Heavy jobs on the desktop GPU (RTX 3070) — setup and daily use
- M0 — Bootstrap (first Claude Code invocation, ~45 min)
- M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card
- Results and what they mean
- residual_eval.py
- {{title}}
- {{title}}
- decisions/INDEX.md
- Compute: laptop for light work, Perlmutter for heavy jobs
- M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)
- M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)
- M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version.
- ObservationSpec
- cross_carrier_check.py
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
- install_desktop.sh
- install_perlmutter.sh
- scrontab_merge.sh
- setup_env_desktop.sh
- setup_env_perlmutter.sh
- plan.md
- su2qc-jepa

## God Nodes (most connected - your core abstractions)
1. `PlaquetteModel` - 43 edges
2. `generate_dataset()` - 26 edges
3. `Worker` - 24 edges
4. `run_j0()` - 24 edges
5. `test_training_and_baselines_run_on_device()` - 22 edges
6. `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier` - 20 edges
7. `ObservableSet` - 19 edges
8. `Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)` - 19 edges
9. `ChainSpec` - 17 edges
10. `Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)` - 17 edges

## Surprising Connections (you probably didn't know these)
- `10.4 M2a — model health (5 Oct; `reports/010`, `decisions/005`, and results fetched at 21:30 UTC)` --references--> `baseline_autoregressive()`  [INFERRED]
  reports/011_project-overview-gauge-jepa-p-v2-plan-physics-status-and-eve.md → src/su2qc_jepa/models/train.py
- `12. Error budget (lines, each measured)` --references--> `trotter_error()`  [INFERRED]
  plans/001_gauge-jepa-p-v2.md → src/su2qc_jepa/physics/chain.py
- `9.4 Error budget (lines, each to be measured)` --references--> `trotter_error()`  [INFERRED]
  reports/011_project-overview-gauge-jepa-p-v2-plan-physics-status-and-eve.md → src/su2qc_jepa/physics/chain.py
- `5.6 Error budget (lines, each to be measured; plan §12)` --references--> `trotter_error()`  [INFERRED]
  reports/012_full-project-report-plan-physics-methods-every-result-and-th.md → src/su2qc_jepa/physics/chain.py
- `Code graph` --references--> `PlaquetteModel`  [INFERRED]
  reports/001_conventions-update-numbered-artifacts-and-the-graphify-code.md → src/su2qc_jepa/physics/plaquette.py

## Import Cycles
- None detected.

## Communities (91 total, 37 thin omitted)

### Community 0 - "run_j0"
Cohesion: 0.05
Nodes (30): 2.1 Model and Hamiltonian, 2.2 Coupling points, 2.3 Verified fingerprints (PROVEN by tests or MEASURED), 2.4 Named states and bare energies, 2.5 Dynamics tables (MEASURED; recomputed in this report by `physics_curves.py`, Appendix A, and equal to the plan's quoted numbers), 2.6 Cross-check against the project's independent verified code (M1; `evidence/J0_data/crosscheck_su2qc.json`, status PASS, tolerance $10^{-10}$, commit `0bb5d6d`), 2. Physics, compare_point() (+22 more)

### Community 1 - "chain.py"
Cohesion: 0.06
Nodes (29): Claims ledger — every substantive statement, its status and its evidence, 1. Audit of the 1 Oct plan — issues found and what changed, _bond_rotation(), build_chain_circuit(), z_layer(), build_chain_prep_circuit(), chain_amplitudes(), chain_sector_unitary() (+21 more)

### Community 2 - "localrun.py"
Cohesion: 0.07
Nodes (30): Problems and assumptions, Problems and assumptions, parse_steps(), admit(), _arg(), classify(), estimate_minutes(), heal_decision() (+22 more)

### Community 3 - "test_jobs.py"
Cohesion: 0.05
Nodes (23): Alternatives considered, Compute: add the desktop RTX 3070 as a second job-queue worker, Consequences (what must be re-run or re-checked), Decision, Why, Actions taken, validate_job(), record() (+15 more)

### Community 4 - "ibm.py"
Cohesion: 0.06
Nodes (24): W4 (26 Oct – 1 Nov) — J2, pilot job; end of the one-month version, BudgetError, calibration_snapshot(), check_budget(), collect(), dry_run(), DryRunSummary, estimate_qpu_seconds() (+16 more)

### Community 5 - "Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier"
Cohesion: 0.04
Nodes (43): Alternatives considered, Consequences, Decision, Numbered artifacts and the Graphify code graph, Why, Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code), Model, Observables (+35 more)

### Community 6 - "Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)"
Cohesion: 0.04
Nodes (45): 0.1 How to read this document, 0.2 Glossary (every technical term used), 0. Reading guide and glossary, 11.1 The rest of M2 (M2a continuation, `prompts/010`), 11.2 M2b — preregistration (16 Oct; `prompts/002` items 6–8), 11.3 M3 (W3, 19–25 Oct; `prompts/003`): forecasting, calibrated twin, dry run, 11.4 M4 (W4, 26 Oct – 1 Nov; `prompts/004`): J2 and the pilot (end of the one-month version), 11.5 M5 (W5, 2–8 Nov; `prompts/005`): hardware days 1 and 2 (+37 more)

### Community 8 - "9. Plot data (the data behind every figure; each table can be parsed as Markdown)"
Cohesion: 0.05
Nodes (40): 9.0 How to use this section, 9.1 Catalogue of plots, 9.2 P11 sub-plots (physics curves and carrier costs), 9. Plot data (the data behind every figure; each table can be parsed as Markdown), Dataset reproducibility (evidence/J0_data/fingerprint_compare_*.json; per-trajectory-sum tolerance 1e-12), Further machine-readable tables (P10, P11e, P11f, J1 records, jobs, dataset reproducibility), J1 gate records (evidence/J1_training/*.json), Job table (jobs/*.yaml and evidence/jobs/NNN/status.json; states read on 2026-10-06 by scripts/jobs/status.py) (+32 more)

### Community 9 - "artifacts.py"
Cohesion: 0.11
Nodes (23): Artifact, check_artifacts(), list_artifacts(), new_artifact(), next_number(), read_front_matter(), render_index(), _resolve() (+15 more)

### Community 10 - "trajectories.py"
Cohesion: 0.14
Nodes (7): _bits_from_key(), estimate_chain(), estimate_diagonal(), Record, sample_exact_chain(), sample_exact_diagonal(), test_estimators_unbiased()

### Community 11 - "Worker"
Cohesion: 0.17
Nodes (6): Code graph, hms_to_hours(), main(), now(), sh(), Worker

### Community 12 - "ledger.py"
Cohesion: 0.12
Nodes (14): run_j1(), run_j2(), auroc(), run_j3(), spearman(), _fmt(), GateResult, GateRow (+6 more)

### Community 13 - "retry_resources"
Cohesion: 0.07
Nodes (25): Alternatives considered, Compute: laptop and Perlmutter only, admission-controlled laptop runner, self-healing jobs, Consequences (what must be re-run or re-checked), Decision, Why, Costs and limits, Heavy jobs: the job queue and the Perlmutter worker, One-time setup (Digonto, about 30 minutes, after the repository exists on GitHub) (+17 more)

### Community 14 - "Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)"
Cohesion: 0.07
Nodes (27): 0. How to read this document, 10.1 Before the repository existed (1–2 Oct, planner sessions; reports 000–005), 10.2 Environment and M0 (2 Oct; reports 006–008), 10.3 M1 — physics cross-check, datasets, gate J0 (3–4 Oct; `reports/009`) — **J0 PASS 9/9**, 10.4 M2a — model health (5 Oct; `reports/010`, `decisions/005`, and results fetched at 21:30 UTC), 10. What has been done, session by session (with every number), 11. Infrastructure and repository conventions (how the work is done), 13. Timeline and milestone status (+19 more)

### Community 16 - "Preregistration — Gauge-JEPA-P v2 (signed by tag `prereg-2026-10-16`)"
Cohesion: 0.10
Nodes (19): 0. What was already known when this was written (disclosure), 1. Hypotheses (thresholds are those of `configs/gates.yaml`, frozen below), 2. Frozen inputs, 3. Analysis plan (exact commands; every computation through `scripts/run.py`), 4. Exclusion and handling rules, 5. Known open items (not part of the frozen record), 6. Signatures, 7. Deviations after signing (+11 more)

### Community 17 - "test_pipeline.py"
Cohesion: 0.24
Nodes (14): Actions taken, Code graph, FamilyConfig, load_dataset(), JEPAConfig, train_jepa(), TrainConfig, test_chain_dataset_uses_chain_carrier() (+6 more)

### Community 18 - "test_training_and_baselines_run_on_device"
Cohesion: 0.11
Nodes (17): 12. Open problems and risks (as of 5 Oct, 21:40 UTC), 14. Next actions, 7.1 Before the repository existed (1–2 Oct; planner sessions; reports 000–005), 7.2 Environment and M0 (2 Oct; reports 006–008), 7.3 M1 — physics cross-check, datasets, gate J0 (3–4 Oct; `reports/009`) — J0 PASS (9 of 9 rows), 7.4 M2a — model health (5 Oct; `reports/010`, `decisions/005`), 7.5 The 5 Oct evening and 6 Oct session (this report adds these), 7.6 Parameter count (+9 more)

### Community 20 - "test_committed_graph_is_fresh"
Cohesion: 0.12
Nodes (14): Actions taken, Code graph, `coding`: imports before and after (`import-before.json` → `import-after.json`), Disk, Laptop environments: coding repaired, su2qc-jepa created, Next action, `pip check`, Problems and assumptions (+6 more)

### Community 21 - "train.py"
Cohesion: 0.23
Nodes (9): effective_rank(), baseline_ridge(), diagnostics(), fit_probe(), _flat_inputs(), forecast_jepa(), _ground_targets(), prepare_tensors() (+1 more)

### Community 22 - "LinkSpace"
Cohesion: 0.14
Nodes (3): LinkSpace, m_values(), spin_matrices()

### Community 25 - "generate_dataset"
Cohesion: 0.23
Nodes (9): Code graph, load(), _checksum(), dataset_fingerprint(), DatasetConfig, generate_dataset(), test_dataset_fingerprint_is_exact_and_locates_differences(), test_fingerprint_equivalence_verdict() (+1 more)

### Community 29 - "su2.py"
Cohesion: 0.24
Nodes (3): _cg_cached(), clebsch_gordan(), _fact()

### Community 30 - "Desktop GPU worker online; `v1_final` trained; preregistered J2 FAIL (on-family passes, strong coupling fails)"
Cohesion: 0.18
Nodes (10): Actions taken, Cost, Dataset used by `v1_final` (`evidence/J0_data/fingerprint_compare_main_laptop_vs_desktop_v1_final.json`), Desktop GPU worker online; `v1_final` trained; preregistered J2 FAIL (on-family passes, strong coupling fails), J1 on `v1_final`, information only (`evidence/J1_training/20261021T203007Z.json`), J2: preregistered forecasting gate, **FAIL** (`evidence/J2_forecast/20261021T201507Z.json`), Next action, Problems and assumptions (+2 more)

### Community 31 - "CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`"
Cohesion: 0.20
Nodes (9): 1. Priorities, in order, 2. Session protocol (every session, no exceptions), 3. Frozen things (changing any of these needs a new `decisions/` record and a new version tag), 4. Hardware rules (non-negotiable), 6. Writing rules (reports, prompts, docs, paper), 7. What the package already guarantees (do not re-derive, do re-run), 8. Where things are, CLAUDE.md — rules for every Claude Code session in `su2qc-jepa` (+1 more)

### Community 32 - "prompts/INDEX.md"
Cohesion: 0.20
Nodes (5): Expected, M6 — Hardware day 3, gate J3, error budget (W6, 2 sessions), M7 — One stretch item (W7), chosen on 15 Nov by Digonto, M8 — Paper assembly, release, replication (W8, 2 sessions), Prompts — index

### Community 33 - "reports/INDEX.md"
Cohesion: 0.20
Nodes (6): Code graph, M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED, Next action, Results and what they mean, What was asked, Reports — index

### Community 34 - "M1: su2qc cross-check PASS, three datasets built, gate J0 PASS"
Cohesion: 0.20
Nodes (9): Actions taken, Code graph, M1: su2qc cross-check PASS, three datasets built, gate J0 PASS, Next action, Part A — route C agrees with both su2qc routes (`evidence/J0_data/crosscheck_su2qc.json`, commit `0bb5d6d`, status PASS), Part B — datasets (`evidence/J0_data/datasets.json`, commit `358d0bd`), Part C — gate J0 PASS (`evidence/J0_data/20261003T201012Z.json`, 15 s on the laptop), Results and what they mean (+1 more)

### Community 35 - "Model card — Gauge-JEPA-P v1 (working configuration after M2a)"
Cohesion: 0.22
Nodes (8): 1. What the model is, 2. Working configuration, 3. Training cost, 4. J1 results (validation split, final epoch; `evidence/GATE_LEDGER.md`, `figures/000`, `figures/001`), 5. Forecasting, preliminary (`runs/v1_confirm/forecast_eval.json`, mean of 5 seeds; NOT a J2 result, since J2 is run in M4a), 6. Data and reproducibility, 7. Known limitations, Model card — Gauge-JEPA-P v1 (working configuration after M2a)

### Community 36 - "M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914)"
Cohesion: 0.22
Nodes (8): Laptop check, 10 epochs, 1 seed (`runs/v1_check/seed0/history.json`, local; validation split), M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914), Next action, Options for Digonto (a decision record in `decisions/` is needed for any of B–D, before the 16 Oct preregistration), Problems and assumptions, Results and what they mean, The energy row cannot pass with this encoder (`evidence/J1_training/ceiling_main.json`, validation split, 26,348 rows; training split 126,824 rows; `data/main` `73fff8e5a7b7`), What was asked

### Community 38 - "J3 gate scores the low-shot rows at the preregistered 512 shots"
Cohesion: 0.25
Nodes (6): Alternatives considered, Consequences, Decision, J3 gate scores the low-shot rows at the preregistered 512 shots, Why, test_j3_uses_the_preregistered_low_shot_level()

### Community 39 - "Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`)"
Cohesion: 0.25
Nodes (8): Absolute safety rules (you have no permission prompts), Context, Definition of done, Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`), Phase A — inventory and backup (no changes), Phase B — repair `coding` (only after rule 4 allows it), Phase C — create `su2qc-jepa` (safe to do at any time; it touches no existing environment), Phase D — report

### Community 40 - "Package build: plan audit, Gauge-JEPA-P v2 and the starter package"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Package build: plan audit, Gauge-JEPA-P v2 and the starter package, Problems and assumptions, Results and what they mean, What was asked

### Community 41 - "Conventions update: numbered artifacts and the Graphify code graph"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Conventions update: numbered artifacts and the Graphify code graph, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 42 - "Compute update 2: safe laptop and a pull-based job queue for Perlmutter"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Compute update 2: safe laptop and a pull-based job queue for Perlmutter, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 43 - "Perlmutter worker install keeps the user's other scrontab entries"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Perlmutter worker install keeps the user's other scrontab entries, Problems and assumptions, Results and what they mean, What was asked

### Community 45 - "{{title}}"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Problems and assumptions, Results and what they mean, {{title}}, What was asked

### Community 46 - "pick_device"
Cohesion: 0.29
Nodes (7): 5. Compute rules (`decisions/004`, `decisions/006`, `configs/compute.yaml`, `docs/PERLMUTTER.md`, `docs/DESKTOP.md`), Decision, Actions taken, 6.1 Compute (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`), 6.2 Repository and conventions, 6. Compute and repository infrastructure, pick_device()

### Community 47 - "M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)"
Cohesion: 0.29
Nodes (6): Expected, M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h), Part A — cross-check against the project's verified `su2qc` code, Part B — datasets, Part C — gate, Tests to add

### Community 48 - "su2qc-jepa — Gauge-JEPA-P v2 starter package"
Cohesion: 0.29
Nodes (6): First two sessions on the laptop, Five-minute tour, Install on the laptop (done by prompts/009), Layout, su2qc-jepa — Gauge-JEPA-P v2 starter package, What is verified today (`python scripts/run.py -- python -m pytest -q`: 47 fast tests; `-m slow` adds 1 more)

### Community 49 - "Compute update: laptop for light work, Perlmutter for heavy jobs"
Cohesion: 0.29
Nodes (6): Code graph, Compute update: laptop for light work, Perlmutter for heavy jobs, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 50 - "M0: repository created, CI green, code graph committed"
Cohesion: 0.29
Nodes (6): Code graph, M0: repository created, CI green, code graph committed, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 51 - "Compute: a safe laptop and a pull-based job queue for Perlmutter"
Cohesion: 0.33
Nodes (5): Alternatives considered, Compute: a safe laptop and a pull-based job queue for Perlmutter, Consequences, Decision, Why

### Community 52 - "J1 energy grounding threshold set relative to the measured information ceiling"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences (what must be re-run or re-checked), Decision, J1 energy grounding threshold set relative to the measured information ceiling, Why

### Community 53 - "Preregistration deviation: dataset-equivalence tolerance corrected to rounding scale"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences, Decision, Preregistration deviation: dataset-equivalence tolerance corrected to rounding scale, Why

### Community 54 - "Heavy jobs on the desktop GPU (RTX 3070) — setup and daily use"
Cohesion: 0.33
Nodes (5): Daily use, From the laptop, Heavy jobs on the desktop GPU (RTX 3070) — setup and daily use, One-time setup (on the desktop, Linux, about 20 minutes), Troubleshooting (on the desktop)

### Community 55 - "M0 — Bootstrap (first Claude Code invocation, ~45 min)"
Cohesion: 0.33
Nodes (5): Context, Definition of done, M0 — Bootstrap (first Claude Code invocation, ~45 min), Out of scope, Tasks

### Community 56 - "M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card"
Cohesion: 0.33
Nodes (5): Context, Definition of done, M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card, Out of scope / stop conditions, Tasks

### Community 57 - "Results and what they mean"
Cohesion: 0.33
Nodes (6): Cost, Dataset reproducibility (`evidence/J0_data/fingerprint_compare_*.json`), Forecasting, preliminary (`runs/v1_confirm/forecast_eval.json`; not a J2 result), J1 (validation split, final epoch; every row is in `evidence/GATE_LEDGER.md`), Results and what they mean, Working model

### Community 59 - "{{title}}"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences (what must be re-run or re-checked), Decision, {{title}}, Why

### Community 60 - "{{title}}"
Cohesion: 0.33
Nodes (5): Context, Definition of done, Out of scope / stop conditions, Tasks, {{title}}

### Community 62 - "Compute: laptop for light work, Perlmutter for heavy jobs"
Cohesion: 0.40
Nodes (4): Alternatives considered, Compute: laptop for light work, Perlmutter for heavy jobs, Consequences, Why

### Community 63 - "M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)"
Cohesion: 0.40
Nodes (4): Expected, M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions), Session M2a — make the model healthy, Session M2b — preregistration (16 Oct)

### Community 64 - "M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)"
Cohesion: 0.40
Nodes (4): Expected, M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions), Session M3a — forecasting, Session M3b — twin and dry run

### Community 65 - "M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version."
Cohesion: 0.40
Nodes (4): Expected, M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version., Session M4a — J2 (30 Oct), Session M4b — pilot (one job)

## Knowledge Gaps
- **330 isolated node(s):** `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script`, `PYTHONHASHSEED`, `replicate.sh script` (+325 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 617 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PlaquetteModel` connect `PlaquetteModel` to `run_j0`, `chain.py`, `._apply_term`, `Conventions update: numbered artifacts and the Graphify code graph`, `trajectories.py`, `pick_device`, `LinkSpace`, `generate_dataset`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Why does `Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)` connect `Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)` to `run_j0`, `reports/INDEX.md`, `9. Plot data (the data behind every figure; each table can be parsed as Markdown)`, `retry_resources`, `pick_device`, `test_training_and_baselines_run_on_device`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Why does `test_training_and_baselines_run_on_device()` connect `test_training_and_baselines_run_on_device` to `test_jobs.py`, `pick_device`, `Preregistration — Gauge-JEPA-P v2 (signed by tag `prereg-2026-10-16`)`, `test_pipeline.py`, `train.py`, `generate_dataset`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `PlaquetteModel` (e.g. with `Code graph` and `6.2 Repository and conventions`) actually correct?**
  _`PlaquetteModel` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `generate_dataset()` (e.g. with `Code graph` and `ObservableSet`) actually correct?**
  _`generate_dataset()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script` to the rest of the system?**
  _330 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `run_j0` be split into smaller, more focused modules?**
  _Cohesion score 0.05096153846153846 - nodes in this community are weakly interconnected._