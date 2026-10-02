# su2qc-jepa — Gauge-JEPA-P v2 starter package

A JEPA world model (joint-embedding predictive architecture: an encoder maps measurement records to a latent, a predictor advances the latent under actions, and the loss compares predicted and target *latents*, never raw records) for the real-time string-breaking dynamics of the hard-core SU(2) lattice gauge theory with two-colour staggered fermions on one plaquette — with a **Krylov-chain hardware carrier** that runs on 12 qubits of an IBM Heron processor at 22 CZ per Trotter step.

The plan is `plans/001_gauge-jepa-p-v2.md` (read it first). The rules for Claude Code sessions are `CLAUDE.md`. The session prompts are `prompts/`.

**Two repository conventions (decisions/001).** (1) Every plan, prompt, report, decision record and figure is a numbered, append-only file — `prompts/004_j2-and-pilot.md`, `reports/002_...md` — created only with `python scripts/new_artifact.py <series> "<title>"`, which also keeps each folder's `INDEX.md`; prompts written later by the planner or by Claude Code go into `prompts/` the same way. (2) Claude Code tracks the codebase with [Graphify](https://github.com/Graphify-Labs/graphify) (`pip install graphifyy`, command `graphify`): a code graph built locally from the source with no LLM or API key, committed as `graphify-out/graph.json` + `GRAPH_REPORT.md`, checked at the start of every session, rebuilt at the end, and verified fresh in CI.

## First two sessions on the laptop

```
# 1. environments (once): repairs the `coding` env and creates `su2qc-jepa`
claude --dangerously-skip-permissions     # inside this directory
> Read prompts/009_laptop-environment-repair-and-setup.md and execute it.

# 2. bootstrap: GitHub repository, CI, code graph
mamba activate su2qc-jepa && claude
> Read CLAUDE.md and prompts/000_bootstrap.md, then execute the bootstrap session.
```

The bootstrap session runs the environment check and the tests, then `scripts/bootstrap_repo.sh`, which installs Graphify if needed, registers it with Claude Code (`graphify claude install`), builds and commits the first code graph, creates the public repository **github.com/digonto10602/su2qc-jepa** with the GitHub CLI (`gh auth login` must have been done once) and pushes. It ends with the first numbered session report.

## Install on the laptop (done by prompts/009)

```
mamba env create -f environment.yml && mamba activate su2qc-jepa
pip install torch --index-url https://download.pytorch.org/whl/cpu      # CPU build first; the GTX 1060 is not supported
pip install -e ".[ml,ibm,dev]"
python scripts/env_check.py                                              # "torch_device_used": "cpu"
python scripts/run.py -- python -m pytest -q
```

**Two machines, one rule.** Every computation runs through `python scripts/run.py -- <command>`. Light work runs on the laptop only when there is room (16 GB of memory always kept free for other sessions, 2 CPUs kept free, one su2qc job at a time), with hard caps and `oom_score_adj = 1000`, so under memory pressure the kernel kills this project's job, never another session's. A job that hits its memory limit is retried once with more memory; otherwise it goes to Perlmutter. Heavy or GPU work always goes to NERSC Perlmutter: `run.py` writes a numbered `jobs/NNN_*.yaml`, a `scrontab` worker on Perlmutter pulls it from GitHub, runs it with Slurm (resubmitting automatically after timeouts, memory kills and node failures), and pushes results to the `results` branch. One-time Perlmutter setup: `docs/PERLMUTTER.md`.

## Five-minute tour

```
python scripts/run.py --no-queue -- bash scripts/smoke.sh   # dataset -> JEPA -> gates J0/J1/J2 -> twin -> residual -> J3 (CPU, ~1-5 min)
python scripts/run.py -- python scripts/make_dataset.py --name main --n-traj 20000 --out data/main   # light: laptop
python scripts/run.py --push -- python scripts/train_jepa.py --data data/main --name main --epochs 200 --seeds 5 --masked   # heavy: queued
python scripts/jobs/status.py && python scripts/jobs/fetch.py 000
python scripts/run.py -- python scripts/run_gate.py J2 --eval runs/main/forecast_eval.json
python scripts/run.py -- python scripts/run_twin.py --name day0 --K 12 --seeds 5   # ~2.4 h: queued
python scripts/run.py -- python scripts/residual_eval.py --model runs/main/seed0/model.pt --records evidence/twin/day0/records.json --out evidence/twin/day0/residual_eval.json
python scripts/hw_dry_run.py --fake            # rehearse the hardware path on FakeTorino (no account needed)
graphify query "how is the observation vector assembled"   # ask the code graph
graphify affected "estimate_chain"                          # what breaks if this changes
python scripts/new_artifact.py reports "My first report"     # next numbered report, INDEX.md updated
python scripts/check_artifacts.py                           # numbering conventions
```

## What is verified today (`python scripts/run.py -- python -m pytest -q`: 47 fast tests; `-m slow` adds 1 more)

* 82 gauge-invariant states, sectors 2/20/38/20/2, electric degeneracies 16/16/18/16/16, 152 states at $j_{\max}=1$ (slow test).
* Two independent Hamiltonian constructions agree to $4\times10^{-16}$; Gauss-law generators commute with $H$ exactly.
* Named-state energies and the resonance $\mu^*=3/8$; the project's $g_E=1$ dynamics table ($P_{\text{baryonic}}=0.43/0.73/0.82$ at $t=1/2/3$) reproduced.
* Krylov chain: $K=12$ reproduces the P-A window $t\le3/g_E$ to $10^{-4}$; Strang circuits equal the exact in-sector unitary; CZ counts 34/56/100/188 for 1/2/4/8 steps; KC-prep exact with 11 rotations.
* Estimators for both carriers are unbiased; twin seeds are independent; splits leak nothing.
* Compute: the job format and script allowlist; a worker tick end to end against a local git remote (results only on the `results` branch, never on `main`); automatic resubmission after a Slurm TIMEOUT with twice the time; the laptop runner's classification, admission and healing rules, a real capped run that hits its memory ceiling and succeeds on the retry, a job that dies with its runner instead of living on as an orphan; and the scrontab installer keeping your other scrontab entries.

## Layout

```
plans/        numbered plans (000 = superseded 1 Oct plan, 001 = active v2 plan) + INDEX.md
prompts/      numbered Claude Code session prompts (000 bootstrap ... 008 release; later ones appended) + INDEX.md
reports/      numbered session and analysis reports + INDEX.md
decisions/    numbered decision records (000 conventions, 001 artifacts + code graph, 004 compute: laptop + Perlmutter) + INDEX.md
figures/      numbered figures + INDEX.md
templates/    templates used by scripts/new_artifact.py
docs/         living documents: PHYSICS, CLAIMS, PREREGISTRATION, PAPER_OUTLINE
src/su2qc_jepa/physics    conventions, plaquette (routes A and B), observables, dynamics (Lanczos), chain (carrier)
src/su2qc_jepa/data       records (estimators), trajectories (datasets, splits)
src/su2qc_jepa/models     jepa (encoder/predictor/SIGReg/grounding), train (loop, probe, baselines)
src/su2qc_jepa/twin       noise models, seeded runner, qubit-line chooser
src/su2qc_jepa/hardware   IBM dry run / budget guard / submit / collect
src/su2qc_jepa/gates      J0-J3 gate scripts and the ledger
src/su2qc_jepa/repo       numbered-artifact tool and code-graph helpers
scripts/                  CLIs used by the session prompts
configs/                  gates.yaml (thresholds), hardware_budget.yaml (human-approved), compute.yaml (laptop/Perlmutter routing)
jobs/                     numbered job requests for the Perlmutter worker (results come back on the `results` branch)
scripts/run.py            the only way to compute: resource-aware, capped, self-healing on the laptop; heavy work -> Perlmutter
scripts/jobs, scripts/worker   enqueue / status / fetch; the Perlmutter worker (scrontab) and its installers
evidence/                 machine records: gate outputs, GATE_LEDGER.md, hardware jobs, graph stats
graphify-out/             code graph (graph.json + GRAPH_REPORT.md committed)
```

License: MIT. Author: Digonto (NMSU / SU2QC). The physics conventions follow the SU2QC physics-setup notes of 9 Sept 2026.
