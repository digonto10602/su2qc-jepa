# Graph Report - su2qc-jepa  (2026-10-15)

## Corpus Check
- 123 files · ~123,183 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 3, .cff 1)

## Summary
- 1118 nodes · 2027 edges · 102 communities (65 shown, 37 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 150 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6ef16d59`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- train.py
- pathlib
- trajectories.py
- ChainSpec
- artifacts.py
- 9. Plot data (the data behind every figure; each table can be parsed as Markdown)
- localrun.py
- PlaquetteModel
- Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)
- ledger.py
- Worker
- retry_resources
- test_jobs.py
- Preregistration — Gauge-JEPA-P v2 (signed by tag `prereg-2026-10-16`)
- ibm.py
- run_j0
- train_jepa.py
- LinkSpace
- test_crosscheck.py
- Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier
- test_committed_graph_is_fresh
- su2.py
- FullSpaceOperators
- named_states
- MatterSpace
- M2a closed: J1 FAIL after 14 configurations (semigroup row on a fresh seed); working model $w_{\text{sigreg}}=3$, $w_{\text{semigroup}}=10$
- sample_exact_chain
- worker.py
- Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code)
- prompts/INDEX.md
- 11. What happens next
- compare_point
- ObservableSet
- CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`
- Compute: laptop for light work, Perlmutter for heavy jobs
- Model card — Gauge-JEPA-P v1 (working configuration after M2a)
- M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED
- ObservationSpec
- 10. Week by week — what Claude Code does, what is tested, what we expect
- Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`)
- Package build: plan audit, Gauge-JEPA-P v2 and the starter package
- Conventions update: numbered artifacts and the Graphify code graph
- Compute update 2: safe laptop and a pull-based job queue for Perlmutter
- Perlmutter worker install keeps the user's other scrontab entries
- Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)
- {{title}}
- layout.py
- M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)
- su2qc-jepa — Gauge-JEPA-P v2 starter package
- Compute update: laptop for light work, Perlmutter for heavy jobs
- test_krylov_dimension_window_PA
- 8. Current results in full
- _Cache
- Compute: a safe laptop and a pull-based job queue for Perlmutter
- J1 energy grounding threshold set relative to the measured information ceiling
- TwinRunner
- M0 — Bootstrap (first Claude Code invocation, ~45 min)
- M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card
- Results and what they mean
- M0: repository created, CI green, code graph committed
- 4. The world model (JEPA)
- 5. Data, twin, hardware plan, gates, hypotheses, error budget
- 7. Chronological history (every session so far, with the numbers)
- {{title}}
- {{title}}
- test_scrontab_merge.py
- .status
- decisions/INDEX.md
- Numbered artifacts and the Graphify code graph
- M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)
- M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)
- M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version.
- reports/INDEX.md
- sector_restrict
- plans/INDEX.md
- 10. Decisions log and problems/risks
- Appendix A — helper scripts (verbatim; run with `python scripts/run.py --no-queue --threads 1 -- python <script> <out.md>` from the repository root)
- Couplings
- 005_hardware-days.md
- 0. Reading guide and glossary
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
1. `PlaquetteModel` - 43 edges
2. `run_j0()` - 24 edges
3. `generate_dataset()` - 23 edges
4. `Worker` - 21 edges
5. `test_training_and_baselines_run_on_device()` - 21 edges
6. `Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier` - 20 edges
7. `ObservableSet` - 19 edges
8. `Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)` - 19 edges
9. `Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)` - 17 edges
10. `9. Plot data (the data behind every figure; each table can be parsed as Markdown)` - 17 edges

## Surprising Connections (you probably didn't know these)
- `6.1 Compute (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`)` --references--> `pick_device()`  [INFERRED]
  reports/012_full-project-report-plan-physics-methods-every-result-and-th.md → src/su2qc_jepa/compute.py
- `10.1 Decisions (`decisions/INDEX.md`)` --references--> `retry_resources()`  [INFERRED]
  reports/012_full-project-report-plan-physics-methods-every-result-and-th.md → src/su2qc_jepa/jobs.py
- `10.4 M2a — model health (5 Oct; `reports/010`, `decisions/005`, and results fetched at 21:30 UTC)` --references--> `baseline_autoregressive()`  [INFERRED]
  reports/011_project-overview-gauge-jepa-p-v2-plan-physics-status-and-eve.md → src/su2qc_jepa/models/train.py
- `12. Open problems and risks (as of 5 Oct, 21:40 UTC)` --references--> `baseline_autoregressive()`  [INFERRED]
  reports/011_project-overview-gauge-jepa-p-v2-plan-physics-status-and-eve.md → src/su2qc_jepa/models/train.py
- `14. Next actions` --references--> `baseline_autoregressive()`  [INFERRED]
  reports/011_project-overview-gauge-jepa-p-v2-plan-physics-status-and-eve.md → src/su2qc_jepa/models/train.py

## Import Cycles
- None detected.

## Communities (102 total, 37 thin omitted)

### Community 0 - "train.py"
Cohesion: 0.05
Nodes (44): Actions taken, Code graph, Laptop check, 10 epochs, 1 seed (`runs/v1_check/seed0/history.json`, local; validation split), M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914), Next action, Options for Digonto (a decision record in `decisions/` is needed for any of B–D, before the 16 Oct preregistration), Problems and assumptions, Results and what they mean (+36 more)

### Community 2 - "trajectories.py"
Cohesion: 0.11
Nodes (4): estimate_diagonal(), Record, sample_exact_diagonal(), chain_point_records()

### Community 3 - "ChainSpec"
Cohesion: 0.06
Nodes (24): Claims ledger — every substantive statement, its status and its evidence, 12. Error budget (lines, each measured), Results and what they mean, 5.6 Error budget (lines, each to be measured; plan §12), _bond_rotation(), build_chain_circuit(), z_layer(), build_chain_prep_circuit() (+16 more)

### Community 4 - "artifacts.py"
Cohesion: 0.10
Nodes (25): Bugs found and fixed while doing this, Results and what they mean, Artifact, check_artifacts(), list_artifacts(), new_artifact(), next_number(), read_front_matter() (+17 more)

### Community 5 - "9. Plot data (the data behind every figure; each table can be parsed as Markdown)"
Cohesion: 0.05
Nodes (40): 9.0 How to use this section, 9.1 Catalogue of plots, 9.2 P11 sub-plots (physics curves and carrier costs), 9. Plot data (the data behind every figure; each table can be parsed as Markdown), Dataset reproducibility (evidence/J0_data/fingerprint_compare_*.json; per-trajectory-sum tolerance 1e-12), Further machine-readable tables (P10, P11e, P11f, J1 records, jobs, dataset reproducibility), J1 gate records (evidence/J1_training/*.json), Job table (jobs/*.yaml and evidence/jobs/NNN/status.json; states read on 2026-10-06 by scripts/jobs/status.py) (+32 more)

### Community 6 - "localrun.py"
Cohesion: 0.09
Nodes (31): Actions taken, Code graph, M1: su2qc cross-check PASS, three datasets built, gate J0 PASS, Next action, Part A — route C agrees with both su2qc routes (`evidence/J0_data/crosscheck_su2qc.json`, commit `0bb5d6d`, status PASS), Part B — datasets (`evidence/J0_data/datasets.json`, commit `358d0bd`), Part C — gate J0 PASS (`evidence/J0_data/20261003T201012Z.json`, 15 s on the laptop), Problems and assumptions (+23 more)

### Community 7 - "PlaquetteModel"
Cohesion: 0.10
Nodes (4): GIBasisState, PlaquetteModel, model(), test_jmax1_counts()

### Community 8 - "Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)"
Cohesion: 0.07
Nodes (29): 0. How to read this document, 10.1 Before the repository existed (1–2 Oct, planner sessions; reports 000–005), 10.2 Environment and M0 (2 Oct; reports 006–008), 10.3 M1 — physics cross-check, datasets, gate J0 (3–4 Oct; `reports/009`) — **J0 PASS 9/9**, 10.4 M2a — model health (5 Oct; `reports/010`, `decisions/005`, and results fetched at 21:30 UTC), 10. What has been done, session by session (with every number), 11. Infrastructure and repository conventions (how the work is done), 12. Open problems and risks (as of 5 Oct, 21:40 UTC) (+21 more)

### Community 9 - "ledger.py"
Cohesion: 0.15
Nodes (12): run_j1(), run_j2(), auroc(), run_j3(), spearman(), _fmt(), GateResult, GateRow (+4 more)

### Community 10 - "Worker"
Cohesion: 0.22
Nodes (3): now(), sh(), Worker

### Community 11 - "retry_resources"
Cohesion: 0.10
Nodes (19): Alternatives considered, Compute: laptop and Perlmutter only, admission-controlled laptop runner, self-healing jobs, Consequences (what must be re-run or re-checked), Decision, Why, Costs and limits, Heavy jobs: the job queue and the Perlmutter worker, One-time setup (Digonto, about 30 minutes, after the repository exists on GitHub) (+11 more)

### Community 12 - "test_jobs.py"
Cohesion: 0.12
Nodes (13): Actions taken, parse_steps(), validate_job(), best_line(), e(), _git(), good_job(), test_allowlist_refuses() (+5 more)

### Community 13 - "Preregistration — Gauge-JEPA-P v2 (signed by tag `prereg-2026-10-16`)"
Cohesion: 0.10
Nodes (18): 0. What was already known when this was written (disclosure), 1. Hypotheses (thresholds are those of `configs/gates.yaml`, frozen below), 2. Frozen inputs, 3. Analysis plan (exact commands; every computation through `scripts/run.py`), 4. Exclusion and handling rules, 5. Known open items (not part of the frozen record), 6. Signatures, Preregistration — Gauge-JEPA-P v2 (signed by tag `prereg-2026-10-16`) (+10 more)

### Community 14 - "ibm.py"
Cohesion: 0.18
Nodes (10): W4 (26 Oct – 1 Nov) — J2, pilot job; end of the one-month version, BudgetError, calibration_snapshot(), check_budget(), collect(), dry_run(), DryRunSummary, estimate_qpu_seconds() (+2 more)

### Community 15 - "run_j0"
Cohesion: 0.18
Nodes (7): estimate_chain(), run_j0(), evolve(), Krylov, krylov_error(), lanczos(), test_estimators_unbiased()

### Community 17 - "LinkSpace"
Cohesion: 0.15
Nodes (3): LinkSpace, m_values(), spin_matrices()

### Community 19 - "Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier"
Cohesion: 0.12
Nodes (16): 0. The idea in one paragraph, 11. Preregistered hypotheses and expected results, 13. Publishability, 14. Assumptions, risks, open points, 16. Compute: the laptop and Perlmutter only (amended 2 Oct 2026; `decisions/004`, superseding `decisions/003` and `decisions/002`), 2. Why v2 is better — side by side, 3. Physics object (frozen) and measured fingerprints, 4. The Krylov-chain carrier (KC) (+8 more)

### Community 20 - "test_committed_graph_is_fresh"
Cohesion: 0.15
Nodes (11): Actions taken, Code graph, Laptop environments: coding repaired, su2qc-jepa created, Next action, Problems and assumptions, What was asked, Actions taken, 6.1 Compute (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`) (+3 more)

### Community 21 - "su2.py"
Cohesion: 0.19
Nodes (3): _cg_cached(), clebsch_gordan(), _fact()

### Community 23 - "named_states"
Cohesion: 0.21
Nodes (7): 2.5 Dynamics tables (MEASURED; recomputed in this report by `physics_curves.py`, Appendix A, and equal to the plan's quoted numbers), channel_masks(), named_states(), test_channel_split(), test_dynamics_reproduce_preliminary_expectation(), test_named_state_energies_and_resonance(), setup()

### Community 25 - "M2a closed: J1 FAIL after 14 configurations (semigroup row on a fresh seed); working model $w_{\text{sigreg}}=3$, $w_{\text{semigroup}}=10$"
Cohesion: 0.18
Nodes (10): Cost, Dataset reproducibility (`evidence/J0_data/fingerprint_compare_*.json`), Forecasting, preliminary (`runs/v1_confirm/forecast_eval.json`; not a J2 result), J1 (validation split, final epoch; every row is in `evidence/GATE_LEDGER.md`), M2a closed: J1 FAIL after 14 configurations (semigroup row on a fresh seed); working model $w_{\text{sigreg}}=3$, $w_{\text{semigroup}}=10$, Next action, Problems and assumptions, Results and what they mean (+2 more)

### Community 26 - "sample_exact_chain"
Cohesion: 0.22
Nodes (6): sample_exact_chain(), _phase_weights(), sample_x_basis(), sample_z_basis(), x_basis_probabilities(), test_samplers()

### Community 28 - "Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code)"
Cohesion: 0.20
Nodes (10): Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code), Model, Observables, Predicted results, Problems and assumptions, Publishability, Schedule (5 Oct – 29 Nov 2026), Testing ladder (budgets are Claude's estimates) (+2 more)

### Community 29 - "prompts/INDEX.md"
Cohesion: 0.20
Nodes (5): Expected, M6 — Hardware day 3, gate J3, error budget (W6, 2 sessions), M7 — One stretch item (W7), chosen on 15 Nov by Digonto, M8 — Paper assembly, release, replication (W8, 2 sessions), Prompts — index

### Community 30 - "11. What happens next"
Cohesion: 0.20
Nodes (10): 11.1 The rest of M2 (M2a continuation, `prompts/010`), 11.2 M2b — preregistration (16 Oct; `prompts/002` items 6–8), 11.3 M3 (W3, 19–25 Oct; `prompts/003`): forecasting, calibrated twin, dry run, 11.4 M4 (W4, 26 Oct – 1 Nov; `prompts/004`): J2 and the pilot (end of the one-month version), 11.5 M5 (W5, 2–8 Nov; `prompts/005`): hardware days 1 and 2, 11.6 M6 (W6, 9–15 Nov; `prompts/006`): day 3, J3, error budget, 11.7 M7 (W7, 16–22 Nov; `prompts/007`): one stretch item, chosen 15 Nov by Digonto, 11.8 M8 (W8, 23–29 Nov; `prompts/008`): paper, release, replication (+2 more)

### Community 31 - "compare_point"
Cohesion: 0.22
Nodes (6): compare_point(), extract_terms(), import_su2qc(), main(), sign_gauge(), su2qc_label_to_c()

### Community 33 - "CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`"
Cohesion: 0.22
Nodes (8): 1. Priorities, in order, 3. Frozen things (changing any of these needs a new `decisions/` record and a new version tag), 4. Hardware rules (non-negotiable), 6. Writing rules (reports, prompts, docs, paper), 7. What the package already guarantees (do not re-derive, do re-run), 8. Where things are, CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`, graphify

### Community 34 - "Compute: laptop for light work, Perlmutter for heavy jobs"
Cohesion: 0.22
Nodes (8): 5. Compute rules (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`), Alternatives considered, Compute: laptop for light work, Perlmutter for heavy jobs, Consequences, Decision, Why, Actions taken, pick_device()

### Community 35 - "Model card — Gauge-JEPA-P v1 (working configuration after M2a)"
Cohesion: 0.22
Nodes (8): 1. What the model is, 2. Working configuration, 3. Training cost, 4. J1 results (validation split, final epoch; `evidence/GATE_LEDGER.md`, `figures/000`, `figures/001`), 5. Forecasting, preliminary (`runs/v1_confirm/forecast_eval.json`, mean of 5 seeds; NOT a J2 result, since J2 is run in M4a), 6. Data and reproducibility, 7. Known limitations, Model card — Gauge-JEPA-P v1 (working configuration after M2a)

### Community 36 - "M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED"
Cohesion: 0.22
Nodes (7): Code graph, M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED, Next action, Problems and assumptions, Results and what they mean, What was asked, test_run_py_retries_after_memory_limit()

### Community 37 - "ObservationSpec"
Cohesion: 0.25
Nodes (3): _bits_from_key(), ObservationSpec, test_observation_spec_roundtrip()

### Community 38 - "10. Week by week — what Claude Code does, what is tested, what we expect"
Cohesion: 0.25
Nodes (8): 10. Week by week — what Claude Code does, what is tested, what we expect, W1 (5–11 Oct) — bootstrap, physics cross-check, data → J0, W2 (12–18 Oct) — JEPA v1, collapse diagnostics, preregistration → J1, W3 (19–25 Oct) — forecasting, twin rehearsal, hardware dry runs, W5 (2–8 Nov) — hardware days 1 and 2, W6 (9–15 Nov) — day 3, J3, advantage-free analysis, W7 (16–22 Nov) — one stretch item, chosen on 15 Nov, W8 (23–29 Nov) — paper, release, replication

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

### Community 44 - "Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)"
Cohesion: 0.25
Nodes (8): 12. Code graph, problems and assumptions of this report, next action, 1. Project goal, scope, allowed and forbidden claims, 3. The Krylov-chain (KC) hardware carrier *(label)*, Actions taken (for this report), Appendix B — file map (where things are), Appendix C — commit list (`git log --oneline`, newest first, 51 commits), Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026), What was asked

### Community 46 - "{{title}}"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Problems and assumptions, Results and what they mean, {{title}}, What was asked

### Community 48 - "M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)"
Cohesion: 0.29
Nodes (6): Expected, M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h), Part A — cross-check against the project's verified `su2qc` code, Part B — datasets, Part C — gate, Tests to add

### Community 49 - "su2qc-jepa — Gauge-JEPA-P v2 starter package"
Cohesion: 0.29
Nodes (6): First two sessions on the laptop, Five-minute tour, Install on the laptop (done by prompts/009), Layout, su2qc-jepa — Gauge-JEPA-P v2 starter package, What is verified today (`python scripts/run.py -- python -m pytest -q`: 47 fast tests; `-m slow` adds 1 more)

### Community 50 - "Compute update: laptop for light work, Perlmutter for heavy jobs"
Cohesion: 0.29
Nodes (6): Code graph, Compute update: laptop for light work, Perlmutter for heavy jobs, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 51 - "test_krylov_dimension_window_PA"
Cohesion: 0.29
Nodes (7): 2.1 Model and Hamiltonian, 2.2 Coupling points, 2.3 Verified fingerprints (PROVEN by tests or MEASURED), 2.4 Named states and bare energies, 2.6 Cross-check against the project's independent verified code (M1; `evidence/J0_data/crosscheck_su2qc.json`, status PASS, tolerance $10^{-10}$, commit `0bb5d6d`), 2. Physics, test_krylov_dimension_window_PA()

### Community 52 - "8. Current results in full"
Cohesion: 0.29
Nodes (7): 8.1 J0 (data gate): PASS, 9 of 9 rows (`evidence/J0_data/20261003T201012Z.json`, `evidence/GATE_LEDGER.md`), 8.2 Energy ceiling (J1 input; `evidence/J1_training/ceiling_main.json`, commit `63065dd`, 2026-10-05T17:31Z; `data/main` `73fff8e5a7b7`; training split 126,824 rows, validation split 26,348 rows; regressor seeds 462709266, 3658436304), 8.3 J1 (training gate) for the six gated rungs (official gate runs; `evidence/GATE_LEDGER.md` rows; records in `evidence/J1_training/`), 8.4 Dataset reproducibility (laptop versus Perlmutter; `evidence/J0_data/fingerprint_compare_*.json`, commit `3010090`, 2026-10-05T23:47Z), 8.5 GPU-fix verification and the job table, 8.6 Forecast results so far, 8. Current results in full

### Community 54 - "Compute: a safe laptop and a pull-based job queue for Perlmutter"
Cohesion: 0.33
Nodes (5): Alternatives considered, Compute: a safe laptop and a pull-based job queue for Perlmutter, Consequences, Decision, Why

### Community 55 - "J1 energy grounding threshold set relative to the measured information ceiling"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences (what must be re-run or re-checked), Decision, J1 energy grounding threshold set relative to the measured information ceiling, Why

### Community 57 - "M0 — Bootstrap (first Claude Code invocation, ~45 min)"
Cohesion: 0.33
Nodes (5): Context, Definition of done, M0 — Bootstrap (first Claude Code invocation, ~45 min), Out of scope, Tasks

### Community 58 - "M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card"
Cohesion: 0.33
Nodes (5): Context, Definition of done, M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card, Out of scope / stop conditions, Tasks

### Community 59 - "Results and what they mean"
Cohesion: 0.33
Nodes (6): `coding`: imports before and after (`import-before.json` → `import-after.json`), Disk, `pip check`, Results and what they mean, `su2qc-jepa` environment, The GTX 1060 (compute capability 6.1, driver 580.178.04, CUDA 13.0 driver API)

### Community 60 - "M0: repository created, CI green, code graph committed"
Cohesion: 0.33
Nodes (5): Code graph, M0: repository created, CI green, code graph committed, Next action, Problems and assumptions, What was asked

### Community 61 - "4. The world model (JEPA)"
Cohesion: 0.33
Nodes (6): 4.1 Observation, actions, training rule, 4.2 Architecture (`src/su2qc_jepa/models/jepa.py`), 4.3 Losses, 4.4 Baselines, tasks, 4. The world model (JEPA), eff_rank()

### Community 62 - "5. Data, twin, hardware plan, gates, hypotheses, error budget"
Cohesion: 0.33
Nodes (6): 5.1 Data (`evidence/J0_data/datasets.json`, commit `358d0bd`; checksums are sha256 of the data arrays, first 12 hex digits shown), 5.2 The digital twin, 5.3 Hardware plan and rules (nothing submitted), 5.4 Gates (current thresholds, `configs/gates.yaml`), 5.5 Preregistered hypotheses H1–H5 (plan §11, `docs/PREREGISTRATION.md` draft), 5. Data, twin, hardware plan, gates, hypotheses, error budget

### Community 63 - "7. Chronological history (every session so far, with the numbers)"
Cohesion: 0.33
Nodes (6): 7.1 Before the repository existed (1–2 Oct; planner sessions; reports 000–005), 7.2 Environment and M0 (2 Oct; reports 006–008), 7.3 M1 — physics cross-check, datasets, gate J0 (3–4 Oct; `reports/009`) — J0 PASS (9 of 9 rows), 7.4 M2a — model health (5 Oct; `reports/010`, `decisions/005`), 7.6 Parameter count, 7. Chronological history (every session so far, with the numbers)

### Community 64 - "{{title}}"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences (what must be re-run or re-checked), Decision, {{title}}, Why

### Community 65 - "{{title}}"
Cohesion: 0.33
Nodes (5): Context, Definition of done, Out of scope / stop conditions, Tasks, {{title}}

### Community 66 - "test_scrontab_merge.py"
Cohesion: 0.60
Nodes (4): _env(), _run(), test_add_to_empty_table_and_remove_last_entry(), test_add_update_remove_keeps_other_entries()

### Community 67 - ".status"
Cohesion: 0.50
Nodes (4): 2. Session protocol (every session, no exceptions), Decision, 15. Repository conventions — numbered artifacts and the code graph (added 2 Oct 2026; `decisions/001`), series()

### Community 69 - "Numbered artifacts and the Graphify code graph"
Cohesion: 0.40
Nodes (4): Alternatives considered, Consequences, Numbered artifacts and the Graphify code graph, Why

### Community 70 - "M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)"
Cohesion: 0.40
Nodes (4): Expected, M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions), Session M2a — make the model healthy, Session M2b — preregistration (16 Oct)

### Community 71 - "M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)"
Cohesion: 0.40
Nodes (4): Expected, M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions), Session M3a — forecasting, Session M3b — twin and dry run

### Community 72 - "M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version."
Cohesion: 0.40
Nodes (4): Expected, M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version., Session M4a — J2 (30 Oct), Session M4b — pilot (one job)

### Community 74 - "sector_restrict"
Cohesion: 0.40
Nodes (4): estimate(), krylov(), subsample(), sector_restrict()

### Community 76 - "10. Decisions log and problems/risks"
Cohesion: 0.50
Nodes (4): 10.1 Decisions (`decisions/INDEX.md`), 10.2 Problems and risks, 10.3 Disagreements between sources that I noticed, 10. Decisions log and problems/risks

### Community 77 - "Appendix A — helper scripts (verbatim; run with `python scripts/run.py --no-queue --threads 1 -- python <script> <out.md>` from the repository root)"
Cohesion: 0.50
Nodes (4): A.1 plot_tables.py (plots P1 to P9, P12), A.2 physics_curves.py (plot P11a to P11d), A.3 evidence_tables.py (P10, P11e, P11f, job and reproducibility tables), Appendix A — helper scripts (verbatim; run with `python scripts/run.py --no-queue --threads 1 -- python <script> <out.md>` from the repository root)

### Community 80 - "0. Reading guide and glossary"
Cohesion: 0.67
Nodes (3): 0.1 How to read this document, 0.2 Glossary (every technical term used), 0. Reading guide and glossary

## Knowledge Gaps
- **306 isolated node(s):** `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script`, `PYTHONHASHSEED`, `replicate.sh script` (+301 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 564 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)` connect `Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)` to `9. Plot data (the data behind every figure; each table can be parsed as Markdown)`, `reports/INDEX.md`, `10. Decisions log and problems/risks`, `Appendix A — helper scripts (verbatim; run with `python scripts/run.py --no-queue --threads 1 -- python <script> <out.md>` from the repository root)`, `0. Reading guide and glossary`, `test_krylov_dimension_window_PA`, `test_committed_graph_is_fresh`, `8. Current results in full`, `5. Data, twin, hardware plan, gates, hypotheses, error budget`, `4. The world model (JEPA)`, `11. What happens next`, `7. Chronological history (every session so far, with the numbers)`?**
  _High betweenness centrality (0.097) - this node is a cross-community bridge._
- **Why does `PlaquetteModel` connect `PlaquetteModel` to `train.py`, `ObservableSet`, `trajectories.py`, `Conventions update: numbered artifacts and the Graphify code graph`, `run_j0`, `LinkSpace`, `test_committed_graph_is_fresh`, `_Cache`, `named_states`, `compare_point`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._
- **Why does `trotter_error()` connect `ChainSpec` to `Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)`, `trajectories.py`, `run_j0`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `PlaquetteModel` (e.g. with `Code graph` and `6.2 Repository and conventions`) actually correct?**
  _`PlaquetteModel` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `run_j0()` (e.g. with `ChainSpec` and `ObservableSet`) actually correct?**
  _`run_j0()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `generate_dataset()` (e.g. with `Code graph` and `ObservableSet`) actually correct?**
  _`generate_dataset()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script` to the rest of the system?**
  _306 weakly-connected nodes found - possible documentation gaps or missing edges._