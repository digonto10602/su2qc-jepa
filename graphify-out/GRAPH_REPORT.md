# Graph Report - su2qc-jepa  (2026-10-21)

## Corpus Check
- 130 files · ~130,466 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 3, .cff 1)

## Summary
- 1178 nodes · 2139 edges · 96 communities (61 shown, 35 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 167 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6479fb18`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Worker
- Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier
- pathlib
- artifacts.py
- Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)
- 9. Plot data (the data behind every figure; each table can be parsed as Markdown)
- test_jobs.py
- CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`
- graph.py
- ibm.py
- PlaquetteModel
- ledger.py
- decisions/INDEX.md
- ChainSpec
- generate_dataset
- train.py
- chain.py
- ndarray
- Preregistration — Gauge-JEPA-P v2 (signed by tag `prereg-2026-10-16`)
- LinkSpace
- dynamics.py
- test_crosscheck.py
- localrun.py
- jepa.py
- heal_decision
- su2.py
- GaugeJEPA
- FullSpaceOperators
- test_physics.py
- crosscheck_su2qc.py
- M2a closed: J1 FAIL after 14 configurations (semigroup row on a fresh seed); working model $w_{\text{sigreg}}=3$, $w_{\text{semigroup}}=10$
- MatterSpace
- env_check.py
- Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)
- Desktop GPU worker online; `v1_final` trained; preregistered J2 FAIL (on-family passes, strong coupling fails)
- dataset_fingerprint
- sample_exact_diagonal
- prompts/INDEX.md
- M1: su2qc cross-check PASS, three datasets built, gate J0 PASS
- 11. What happens next
- Model card — Gauge-JEPA-P v1 (working configuration after M2a)
- M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914)
- scripts/run.py
- Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`)
- Package build: plan audit, Gauge-JEPA-P v2 and the starter package
- Conventions update: numbered artifacts and the Graphify code graph
- Compute update 2: safe laptop and a pull-based job queue for Perlmutter
- Perlmutter worker install keeps the user's other scrontab entries
- test_localrun.py
- residual_eval.py
- {{title}}
- M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)
- su2qc-jepa — Gauge-JEPA-P v2 starter package
- 2. Physics
- 8. Current results in full
- Heavy jobs on the desktop GPU (RTX 3070) — setup and daily use
- M0 — Bootstrap (first Claude Code invocation, ~45 min)
- M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card
- M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED
- 4. The world model (JEPA)
- 7. Chronological history (every session so far, with the numbers)
- {{title}}
- {{title}}
- test_scrontab_merge.py
- M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)
- M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)
- M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version.
- reports/INDEX.md
- Appendix A — helper scripts (verbatim; run with `python scripts/run.py --no-queue --threads 1 -- python <script> <out.md>` from the repository root)
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
2. `generate_dataset()` - 25 edges
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
- `12. Open problems and risks (as of 5 Oct, 21:40 UTC)` --references--> `baseline_autoregressive()`  [INFERRED]
  reports/011_project-overview-gauge-jepa-p-v2-plan-physics-status-and-eve.md → src/su2qc_jepa/models/train.py
- `14. Next actions` --references--> `baseline_autoregressive()`  [INFERRED]
  reports/011_project-overview-gauge-jepa-p-v2-plan-physics-status-and-eve.md → src/su2qc_jepa/models/train.py
- `Code graph` --references--> `PlaquetteModel`  [INFERRED]
  reports/001_conventions-update-numbered-artifacts-and-the-graphify-code.md → src/su2qc_jepa/physics/plaquette.py
- `Actions taken` --references--> `check_artifacts()`  [INFERRED]
  reports/003_compute-update-2-safe-laptop-and-a-pull-based-job-queue-for.md → src/su2qc_jepa/repo/artifacts.py

## Import Cycles
- None detected.

## Communities (96 total, 35 thin omitted)

### Community 0 - "Worker"
Cohesion: 0.06
Nodes (31): Alternatives considered, Compute: laptop and Perlmutter only, admission-controlled laptop runner, self-healing jobs, Consequences (what must be re-run or re-checked), Decision, Why, Costs and limits, Heavy jobs: the job queue and the Perlmutter worker, One-time setup (Digonto, about 30 minutes, after the repository exists on GitHub) (+23 more)

### Community 1 - "Gauge-JEPA-P v2 — a JEPA world model for SU(2) string breaking on one plaquette, with a Krylov-chain hardware carrier"
Cohesion: 0.05
Nodes (38): Decision, Gauge-JEPA-P: JEPA for SU(2) gauge-theory QML — 1–2 month plan (1 October 2026, revised same day: IBM-Q + IonQ QPUs, laptop + NERSC Perlmutter, Claude Code), Model, Observables, Predicted results, Problems and assumptions, Publishability, Schedule (5 Oct – 29 Nov 2026) (+30 more)

### Community 2 - "pathlib"
Cohesion: 0.08
Nodes (4): heron_like_noise_model(), HeronLike, noise_model_from_backend(), save_noise_summary()

### Community 3 - "artifacts.py"
Cohesion: 0.10
Nodes (17): Artifact, check_artifacts(), list_artifacts(), new_artifact(), next_number(), read_front_matter(), render_index(), _resolve() (+9 more)

### Community 4 - "Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)"
Cohesion: 0.05
Nodes (38): 12. Error budget (lines, each measured), 0. How to read this document, 10.1 Before the repository existed (1–2 Oct, planner sessions; reports 000–005), 10.2 Environment and M0 (2 Oct; reports 006–008), 10.3 M1 — physics cross-check, datasets, gate J0 (3–4 Oct; `reports/009`) — **J0 PASS 9/9**, 10.4 M2a — model health (5 Oct; `reports/010`, `decisions/005`, and results fetched at 21:30 UTC), 10. What has been done, session by session (with every number), 11. Infrastructure and repository conventions (how the work is done) (+30 more)

### Community 5 - "9. Plot data (the data behind every figure; each table can be parsed as Markdown)"
Cohesion: 0.05
Nodes (37): 9.0 How to use this section, 9.1 Catalogue of plots, 9.2 P11 sub-plots (physics curves and carrier costs), 9. Plot data (the data behind every figure; each table can be parsed as Markdown), Dataset reproducibility (evidence/J0_data/fingerprint_compare_*.json; per-trajectory-sum tolerance 1e-12), Further machine-readable tables (P10, P11e, P11f, J1 records, jobs, dataset reproducibility), J1 gate records (evidence/J1_training/*.json), Job table (jobs/*.yaml and evidence/jobs/NNN/status.json; states read on 2026-10-06 by scripts/jobs/status.py) (+29 more)

### Community 6 - "test_jobs.py"
Cohesion: 0.08
Nodes (22): Alternatives considered, Compute: add the desktop RTX 3070 as a second job-queue worker, Consequences (what must be re-run or re-checked), Decision, Why, Actions taken, parse_steps(), validate_job() (+14 more)

### Community 7 - "CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`"
Cohesion: 0.06
Nodes (27): 1. Priorities, in order, 2. Session protocol (every session, no exceptions), 3. Frozen things (changing any of these needs a new `decisions/` record and a new version tag), 4. Hardware rules (non-negotiable), 5. Compute rules (`decisions/004`, `decisions/006`, `configs/compute.yaml`, `docs/PERLMUTTER.md`, `docs/DESKTOP.md`), 6. Writing rules (reports, prompts, docs, paper), 7. What the package already guarantees (do not re-derive, do re-run), 8. Where things are (+19 more)

### Community 8 - "graph.py"
Cohesion: 0.07
Nodes (25): Actions taken, Code graph, `coding`: imports before and after (`import-before.json` → `import-after.json`), Disk, Laptop environments: coding repaired, su2qc-jepa created, Next action, `pip check`, Problems and assumptions (+17 more)

### Community 9 - "ibm.py"
Cohesion: 0.09
Nodes (14): W4 (26 Oct – 1 Nov) — J2, pilot job; end of the one-month version, BudgetError, calibration_snapshot(), check_budget(), collect(), dry_run(), DryRunSummary, estimate_qpu_seconds() (+6 more)

### Community 10 - "PlaquetteModel"
Cohesion: 0.14
Nodes (14): compare_point(), estimate_diagonal(), _initial_state(), run_j0(), sector_restrict(), channel_masks(), named_states(), ObservableSet (+6 more)

### Community 11 - "ledger.py"
Cohesion: 0.14
Nodes (12): run_j1(), run_j2(), auroc(), run_j3(), spearman(), _fmt(), GateResult, GateRow (+4 more)

### Community 12 - "decisions/INDEX.md"
Cohesion: 0.07
Nodes (21): Frozen conventions and coupling points, Alternatives considered, Consequences, Numbered artifacts and the Graphify code graph, Why, Alternatives considered, Compute: a safe laptop and a pull-based job queue for Perlmutter, Consequences (+13 more)

### Community 13 - "ChainSpec"
Cohesion: 0.14
Nodes (13): estimate_chain(), Record, build_chain_circuit(), z_layer(), ChainSpec, cz_count(), chain_point_records(), twin_variance_check() (+5 more)

### Community 14 - "generate_dataset"
Cohesion: 0.22
Nodes (17): Actions taken, Code graph, DatasetConfig, FamilyConfig, generate_dataset(), load_dataset(), JEPAConfig, prepare_tensors() (+9 more)

### Community 15 - "train.py"
Cohesion: 0.16
Nodes (13): 7.5 The 5 Oct evening and 6 Oct session (this report adds these), Actions taken, effective_rank(), baseline_autoregressive(), baseline_ridge(), baseline_supervised_mlp(), diagnostics(), fit_probe() (+5 more)

### Community 16 - "chain.py"
Cohesion: 0.14
Nodes (12): sample_exact_chain(), _bond_rotation(), build_chain_prep_circuit(), chain_amplitudes(), chain_sector_unitary(), _layer(), _phase_weights(), prep_cascade_params() (+4 more)

### Community 18 - "Preregistration — Gauge-JEPA-P v2 (signed by tag `prereg-2026-10-16`)"
Cohesion: 0.10
Nodes (19): 0. What was already known when this was written (disclosure), 1. Hypotheses (thresholds are those of `configs/gates.yaml`, frozen below), 2. Frozen inputs, 3. Analysis plan (exact commands; every computation through `scripts/run.py`), 4. Exclusion and handling rules, 5. Known open items (not part of the frozen record), 6. Signatures, 7. Deviations after signing (+11 more)

### Community 20 - "LinkSpace"
Cohesion: 0.13
Nodes (3): LinkSpace, m_values(), spin_matrices()

### Community 21 - "dynamics.py"
Cohesion: 0.18
Nodes (6): Results and what they mean, evolve(), Krylov, krylov_error(), lanczos(), test_estimators_unbiased()

### Community 23 - "localrun.py"
Cohesion: 0.19
Nodes (9): Problems and assumptions, _arg(), estimate_minutes(), ledger_append(), _limit_env(), _manifest_ntrain(), _preexec(), run_capped() (+1 more)

### Community 25 - "heal_decision"
Cohesion: 0.27
Nodes (13): admit(), classify(), heal_decision(), is_heavy(), is_resource_failure(), load_policy(), Policy, Probe (+5 more)

### Community 26 - "su2.py"
Cohesion: 0.19
Nodes (3): _cg_cached(), clebsch_gordan(), _fact()

### Community 29 - "test_physics.py"
Cohesion: 0.17
Nodes (5): Claims ledger — every substantive statement, its status and its evidence, model(), test_chain_prep_cascade(), test_jmax1_counts(), test_two_routes_agree_and_gauss_law()

### Community 30 - "crosscheck_su2qc.py"
Cohesion: 0.23
Nodes (5): extract_terms(), import_su2qc(), main(), sign_gauge(), su2qc_label_to_c()

### Community 31 - "M2a closed: J1 FAIL after 14 configurations (semigroup row on a fresh seed); working model $w_{\text{sigreg}}=3$, $w_{\text{semigroup}}=10$"
Cohesion: 0.17
Nodes (11): Code graph, Cost, Dataset reproducibility (`evidence/J0_data/fingerprint_compare_*.json`), Forecasting, preliminary (`runs/v1_confirm/forecast_eval.json`; not a J2 result), J1 (validation split, final epoch; every row is in `evidence/GATE_LEDGER.md`), M2a closed: J1 FAIL after 14 configurations (semigroup row on a fresh seed); working model $w_{\text{sigreg}}=3$, $w_{\text{semigroup}}=10$, Next action, Problems and assumptions (+3 more)

### Community 34 - "Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)"
Cohesion: 0.18
Nodes (11): 0.1 How to read this document, 0.2 Glossary (every technical term used), 0. Reading guide and glossary, 12. Code graph, problems and assumptions of this report, next action, 1. Project goal, scope, allowed and forbidden claims, 3. The Krylov-chain (KC) hardware carrier *(label)*, Actions taken (for this report), Appendix B — file map (where things are) (+3 more)

### Community 35 - "Desktop GPU worker online; `v1_final` trained; preregistered J2 FAIL (on-family passes, strong coupling fails)"
Cohesion: 0.18
Nodes (10): Actions taken, Cost, Dataset used by `v1_final` (`evidence/J0_data/fingerprint_compare_main_laptop_vs_desktop_v1_final.json`), Desktop GPU worker online; `v1_final` trained; preregistered J2 FAIL (on-family passes, strong coupling fails), J1 on `v1_final`, information only (`evidence/J1_training/20261021T203007Z.json`), J2: preregistered forecasting gate, **FAIL** (`evidence/J2_forecast/20261021T201507Z.json`), Next action, Problems and assumptions (+2 more)

### Community 36 - "dataset_fingerprint"
Cohesion: 0.25
Nodes (5): load(), _Cache, _checksum(), dataset_fingerprint(), verdict()

### Community 37 - "sample_exact_diagonal"
Cohesion: 0.20
Nodes (4): _bits_from_key(), ObservationSpec, sample_exact_diagonal(), test_observation_spec_roundtrip()

### Community 38 - "prompts/INDEX.md"
Cohesion: 0.20
Nodes (5): Expected, M6 — Hardware day 3, gate J3, error budget (W6, 2 sessions), M7 — One stretch item (W7), chosen on 15 Nov by Digonto, M8 — Paper assembly, release, replication (W8, 2 sessions), Prompts — index

### Community 39 - "M1: su2qc cross-check PASS, three datasets built, gate J0 PASS"
Cohesion: 0.20
Nodes (9): Actions taken, Code graph, M1: su2qc cross-check PASS, three datasets built, gate J0 PASS, Next action, Part A — route C agrees with both su2qc routes (`evidence/J0_data/crosscheck_su2qc.json`, commit `0bb5d6d`, status PASS), Part B — datasets (`evidence/J0_data/datasets.json`, commit `358d0bd`), Part C — gate J0 PASS (`evidence/J0_data/20261003T201012Z.json`, 15 s on the laptop), Results and what they mean (+1 more)

### Community 40 - "11. What happens next"
Cohesion: 0.20
Nodes (10): 11.1 The rest of M2 (M2a continuation, `prompts/010`), 11.2 M2b — preregistration (16 Oct; `prompts/002` items 6–8), 11.3 M3 (W3, 19–25 Oct; `prompts/003`): forecasting, calibrated twin, dry run, 11.4 M4 (W4, 26 Oct – 1 Nov; `prompts/004`): J2 and the pilot (end of the one-month version), 11.5 M5 (W5, 2–8 Nov; `prompts/005`): hardware days 1 and 2, 11.6 M6 (W6, 9–15 Nov; `prompts/006`): day 3, J3, error budget, 11.7 M7 (W7, 16–22 Nov; `prompts/007`): one stretch item, chosen 15 Nov by Digonto, 11.8 M8 (W8, 23–29 Nov; `prompts/008`): paper, release, replication (+2 more)

### Community 41 - "Model card — Gauge-JEPA-P v1 (working configuration after M2a)"
Cohesion: 0.22
Nodes (8): 1. What the model is, 2. Working configuration, 3. Training cost, 4. J1 results (validation split, final epoch; `evidence/GATE_LEDGER.md`, `figures/000`, `figures/001`), 5. Forecasting, preliminary (`runs/v1_confirm/forecast_eval.json`, mean of 5 seeds; NOT a J2 result, since J2 is run in M4a), 6. Data and reproducibility, 7. Known limitations, Model card — Gauge-JEPA-P v1 (working configuration after M2a)

### Community 42 - "M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914)"
Cohesion: 0.22
Nodes (8): Laptop check, 10 epochs, 1 seed (`runs/v1_check/seed0/history.json`, local; validation split), M2a: ladder queued on Perlmutter; energy grounding row of J1 is unreachable (ceiling $R^2$ 0.914), Next action, Options for Digonto (a decision record in `decisions/` is needed for any of B–D, before the 16 Oct preregistration), Problems and assumptions, Results and what they mean, The energy row cannot pass with this encoder (`evidence/J1_training/ceiling_main.json`, validation split, 26,348 rows; training split 126,824 rows; `data/main` `73fff8e5a7b7`), What was asked

### Community 43 - "scripts/run.py"
Cohesion: 0.32
Nodes (3): dataset_step(), guess_outputs(), queue()

### Community 45 - "Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`)"
Cohesion: 0.25
Nodes (8): Absolute safety rules (you have no permission prompts), Context, Definition of done, Laptop environments: repair `coding`, create `su2qc-jepa` (run once, before `prompts/000`), Phase A — inventory and backup (no changes), Phase B — repair `coding` (only after rule 4 allows it), Phase C — create `su2qc-jepa` (safe to do at any time; it touches no existing environment), Phase D — report

### Community 46 - "Package build: plan audit, Gauge-JEPA-P v2 and the starter package"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Package build: plan audit, Gauge-JEPA-P v2 and the starter package, Problems and assumptions, Results and what they mean, What was asked

### Community 47 - "Conventions update: numbered artifacts and the Graphify code graph"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Conventions update: numbered artifacts and the Graphify code graph, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 48 - "Compute update 2: safe laptop and a pull-based job queue for Perlmutter"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Compute update 2: safe laptop and a pull-based job queue for Perlmutter, Next action, Problems and assumptions, Results and what they mean, What was asked

### Community 49 - "Perlmutter worker install keeps the user's other scrontab entries"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Perlmutter worker install keeps the user's other scrontab entries, Problems and assumptions, Results and what they mean, What was asked

### Community 50 - "test_localrun.py"
Cohesion: 0.25
Nodes (3): Problems and assumptions, test_job_dies_with_the_runner(), test_run_py_retries_after_memory_limit()

### Community 52 - "residual_eval.py"
Cohesion: 0.32
Nodes (3): estimate(), krylov(), subsample()

### Community 54 - "{{title}}"
Cohesion: 0.25
Nodes (7): Actions taken, Code graph, Next action, Problems and assumptions, Results and what they mean, {{title}}, What was asked

### Community 55 - "M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h)"
Cohesion: 0.29
Nodes (6): Expected, M1 — Physics cross-check and datasets → gate J0 (W1, 2 sessions of ≤ 6 h), Part A — cross-check against the project's verified `su2qc` code, Part B — datasets, Part C — gate, Tests to add

### Community 56 - "su2qc-jepa — Gauge-JEPA-P v2 starter package"
Cohesion: 0.29
Nodes (6): First two sessions on the laptop, Five-minute tour, Install on the laptop (done by prompts/009), Layout, su2qc-jepa — Gauge-JEPA-P v2 starter package, What is verified today (`python scripts/run.py -- python -m pytest -q`: 47 fast tests; `-m slow` adds 1 more)

### Community 57 - "2. Physics"
Cohesion: 0.29
Nodes (7): 2.1 Model and Hamiltonian, 2.2 Coupling points, 2.3 Verified fingerprints (PROVEN by tests or MEASURED), 2.4 Named states and bare energies, 2.5 Dynamics tables (MEASURED; recomputed in this report by `physics_curves.py`, Appendix A, and equal to the plan's quoted numbers), 2.6 Cross-check against the project's independent verified code (M1; `evidence/J0_data/crosscheck_su2qc.json`, status PASS, tolerance $10^{-10}$, commit `0bb5d6d`), 2. Physics

### Community 58 - "8. Current results in full"
Cohesion: 0.29
Nodes (7): 8.1 J0 (data gate): PASS, 9 of 9 rows (`evidence/J0_data/20261003T201012Z.json`, `evidence/GATE_LEDGER.md`), 8.2 Energy ceiling (J1 input; `evidence/J1_training/ceiling_main.json`, commit `63065dd`, 2026-10-05T17:31Z; `data/main` `73fff8e5a7b7`; training split 126,824 rows, validation split 26,348 rows; regressor seeds 462709266, 3658436304), 8.3 J1 (training gate) for the six gated rungs (official gate runs; `evidence/GATE_LEDGER.md` rows; records in `evidence/J1_training/`), 8.4 Dataset reproducibility (laptop versus Perlmutter; `evidence/J0_data/fingerprint_compare_*.json`, commit `3010090`, 2026-10-05T23:47Z), 8.5 GPU-fix verification and the job table, 8.6 Forecast results so far, 8. Current results in full

### Community 59 - "Heavy jobs on the desktop GPU (RTX 3070) — setup and daily use"
Cohesion: 0.33
Nodes (5): Daily use, From the laptop, Heavy jobs on the desktop GPU (RTX 3070) — setup and daily use, One-time setup (on the desktop, Linux, about 20 minutes), Troubleshooting (on the desktop)

### Community 60 - "M0 — Bootstrap (first Claude Code invocation, ~45 min)"
Cohesion: 0.33
Nodes (5): Context, Definition of done, M0 — Bootstrap (first Claude Code invocation, ~45 min), Out of scope, Tasks

### Community 61 - "M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card"
Cohesion: 0.33
Nodes (5): Context, Definition of done, M2a continuation: fetch the ablation ladder, J1, diagnostics figure, model card, Out of scope / stop conditions, Tasks

### Community 62 - "M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED"
Cohesion: 0.33
Nodes (5): Code graph, M0 follow-up: Perlmutter worker installed, A100 smoke test COMPLETED, Next action, Results and what they mean, What was asked

### Community 63 - "4. The world model (JEPA)"
Cohesion: 0.33
Nodes (6): 4.1 Observation, actions, training rule, 4.2 Architecture (`src/su2qc_jepa/models/jepa.py`), 4.3 Losses, 4.4 Baselines, tasks, 4. The world model (JEPA), eff_rank()

### Community 64 - "7. Chronological history (every session so far, with the numbers)"
Cohesion: 0.33
Nodes (6): 7.1 Before the repository existed (1–2 Oct; planner sessions; reports 000–005), 7.2 Environment and M0 (2 Oct; reports 006–008), 7.3 M1 — physics cross-check, datasets, gate J0 (3–4 Oct; `reports/009`) — J0 PASS (9 of 9 rows), 7.4 M2a — model health (5 Oct; `reports/010`, `decisions/005`), 7.6 Parameter count, 7. Chronological history (every session so far, with the numbers)

### Community 65 - "{{title}}"
Cohesion: 0.33
Nodes (5): Alternatives considered, Consequences (what must be re-run or re-checked), Decision, {{title}}, Why

### Community 66 - "{{title}}"
Cohesion: 0.33
Nodes (5): Context, Definition of done, Out of scope / stop conditions, Tasks, {{title}}

### Community 67 - "test_scrontab_merge.py"
Cohesion: 0.60
Nodes (4): _env(), _run(), test_add_to_empty_table_and_remove_last_entry(), test_add_update_remove_keeps_other_entries()

### Community 68 - "M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions)"
Cohesion: 0.40
Nodes (4): Expected, M2 — JEPA v1, collapse diagnostics, preregistration → gate J1 (W2, 2 sessions), Session M2a — make the model healthy, Session M2b — preregistration (16 Oct)

### Community 69 - "M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions)"
Cohesion: 0.40
Nodes (4): Expected, M3 — Forecasting evaluation, calibrated twin, hardware dry runs (W3, 2 sessions), Session M3a — forecasting, Session M3b — twin and dry run

### Community 70 - "M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version."
Cohesion: 0.40
Nodes (4): Expected, M4 — Gate J2 and the hardware pilot (W4, 2 sessions). End of the one-month version., Session M4a — J2 (30 Oct), Session M4b — pilot (one job)

### Community 72 - "Appendix A — helper scripts (verbatim; run with `python scripts/run.py --no-queue --threads 1 -- python <script> <out.md>` from the repository root)"
Cohesion: 0.50
Nodes (4): A.1 plot_tables.py (plots P1 to P9, P12), A.2 physics_curves.py (plot P11a to P11d), A.3 evidence_tables.py (P10, P11e, P11f, job and reproducibility tables), Appendix A — helper scripts (verbatim; run with `python scripts/run.py --no-queue --threads 1 -- python <script> <out.md>` from the repository root)

## Knowledge Gaps
- **327 isolated node(s):** `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script`, `PYTHONHASHSEED`, `replicate.sh script` (+322 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 601 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **35 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PlaquetteModel` connect `PlaquetteModel` to `dataset_fingerprint`, `CLAUDE.md — rules for every Claude Code session in `su2qc-jepa``, `generate_dataset`, `Conventions update: numbered artifacts and the Graphify code graph`, `ndarray`, `j0_data.py`, `LinkSpace`, `test_physics.py`, `crosscheck_su2qc.py`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Why does `Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)` connect `Full project report: plan, physics, methods, every result and the data behind every plot (6 Oct 2026)` to `Worker`, `7. Chronological history (every session so far, with the numbers)`, `Project overview: Gauge-JEPA-P v2 — plan, physics, status and every number to date (5 Oct 2026)`, `9. Plot data (the data behind every figure; each table can be parsed as Markdown)`, `reports/INDEX.md`, `11. What happens next`, `CLAUDE.md — rules for every Claude Code session in `su2qc-jepa``, `Appendix A — helper scripts (verbatim; run with `python scripts/run.py --no-queue --threads 1 -- python <script> <out.md>` from the repository root)`, `2. Physics`, `8. Current results in full`, `4. The world model (JEPA)`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Why does `test_training_and_baselines_run_on_device()` connect `train.py` to `test_jobs.py`, `CLAUDE.md — rules for every Claude Code session in `su2qc-jepa``, `generate_dataset`, `Preregistration — Gauge-JEPA-P v2 (signed by tag `prereg-2026-10-16`)`, `j0_data.py`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `PlaquetteModel` (e.g. with `Code graph` and `6.2 Repository and conventions`) actually correct?**
  _`PlaquetteModel` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `generate_dataset()` (e.g. with `Code graph` and `ObservableSet`) actually correct?**
  _`generate_dataset()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `su2qc-jepa`, `bootstrap_repo.sh script`, `graph_update.sh script` to the rest of the system?**
  _327 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Worker` be split into smaller, more focused modules?**
  _Cohesion score 0.06340326340326341 - nodes in this community are weakly interconnected._