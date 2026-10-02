# CLAUDE.md — rules for every Claude Code session in `su2qc-jepa`

Before anything else, read `~/.claude/CLAUDE.md` (user-level instructions; §2 step 1 says how the two files combine). You are running the Gauge-JEPA-P v2 plan (`plans/001_gauge-jepa-p-v2.md`; the active plan is always the one marked `active` in `plans/INDEX.md`). Read this file first in every session; it is short on purpose. The plan says *what*; this file says *how* — and what you must never do.

## 1. Priorities, in order
1. **Physics correctness** beats speed, throughput and completeness. A number that is not reproduced by the deterministic gate scripts does not exist.
2. **Evidence beats prose.** Every claim in a report points at a file under `evidence/`, `runs/` or `figures/` that a reviewer can open.
3. **Honesty about status.** Use only PASS / FAIL / PARTIAL / NOT RUN / VOID for gates. Never upgrade a status in prose. Emulated numbers are labelled EMULATED; nothing is "hardware" until it has an IBM job id.

## 2. Session protocol (every session, no exceptions)

**Start**
1. Read your user-level instructions in `~/.claude/CLAUDE.md` (Digonto's personal rules for every project — e.g. how to report, math formatting). If the file does not exist, say so in the report and continue. Where it conflicts with this file, this file wins for work inside this repository and the conflict is noted in the report; where it adds a rule this file does not cover (style, reporting, tooling preferences), follow it.
2. Read this file, the session's prompt (`prompts/NNN_*.md`), `STATE.json`, and the newest report in `reports/INDEX.md`.
3. `python scripts/env_check.py` (writes `evidence/ENV.json`).
4. `bash scripts/graph_update.sh --check` — rebuilds the code graph and says FRESH or STALE against the committed one (stale at start means the last session forgot to commit it; note it in your report). Read the first screen of `graphify-out/GRAPH_REPORT.md` (hubs, communities) before opening source files.
5. `python scripts/run.py -- python -m pytest -q` before touching physics.

**During**
- Codebase questions go to the graph first: `graphify query "<question>"`, `graphify explain "<symbol>"`, `graphify path "<A>" "<B>"`. Grep or open whole files only when the graph does not answer.
- Before changing a function or class: `graphify affected "<symbol>"`; run the tests that cover what it lists, and name them in your report.
- Every new plan, prompt, report, decision record or figure is created with `python scripts/new_artifact.py <series> "<title>" --milestone Mx` — never by choosing a file name yourself. If you write a prompt for a later session (a repair, an escalation, a follow-up), it goes into `prompts/` the same way, with `--supersedes prompts/NNN` when it replaces one. Revisions are new numbers; old artifacts are never edited except for the `status`/`superseded_by` change the tool makes.
- Figures: `python scripts/new_artifact.py figures "<caption>" --ext .png` prints the path to save to.

**End**
1. `python scripts/run.py -- python -m pytest -q`; the milestone's gate (`python scripts/run.py -- python scripts/run_gate.py ...`), if any.
2. `bash scripts/graph_update.sh` — rebuilds `graphify-out/graph.json` and `GRAPH_REPORT.md`, writes `evidence/graph/stats.json`. (The Graphify section at the end of this file says `graphify update .`; use the wrapper instead — it pins `PYTHONHASHSEED=0` so rebuilds are reproducible, drops dated snapshots and records the stats.)
3. The session report: `python scripts/new_artifact.py reports "<milestone>: <one-line result>" --milestone Mx`, filled in the template's order — what was asked, actions taken, results and what they mean, code graph (nodes/edges/communities before → after, `affected` checks run), problems and assumptions, next action. Set its `status: done`.
4. `python scripts/check_artifacts.py` must print `OK`.
5. Update `STATE.json` (milestone status, report id, gate status).
6. Commit in scoped commits with conventional prefixes (`physics:`, `data:`, `model:`, `twin:`, `hw:`, `gate:`, `docs:`, `chore:`), the graph refresh last as `chore(graph): refresh code graph`. Show `git log --oneline -6`. Never rewrite history.

**Stop conditions** (write the reason in the report, then end): a physics fingerprint test fails; two routes disagree above 1e-12; a gate threshold would have to change to pass; the hardware budget file does not approve the manifest you hold; 8 hours of wall time.

## 3. Frozen things (changing any of these needs a new `decisions/` record and a new version tag)
- `src/su2qc_jepa/physics/conventions.py` (geometry, phases, Jordan–Wigner order, coupling points, fingerprints) — `decisions/000`.
- `configs/gates.yaml` after the preregistration tag `prereg-2026-10-16`.
- The observation layout (`data/records.py: ObservationSpec`).
- Dataset checksums recorded in `evidence/J0_data/`.
- The artifact and graph conventions — `decisions/001`; the pinned `graphifyy` version.

## 4. Hardware rules (non-negotiable)
- Nothing is submitted to a QPU without, in this order: a dry-run manifest (`scripts/hw_dry_run.py`), a human editing `configs/hardware_budget.yaml` (`approved: true`, the manifest hash, caps), and `scripts/hw_submit.py submit --confirm`. The code enforces this (`hardware/ibm.py: check_budget`); do not work around it.
- You never edit `approved`, `approved_by`, `approved_utc` or `manifest_hash` in the budget file. Propose values in your report.
- One job per approval. After `collect`, raw counts are immutable (`evidence/hardware/jobs/<id>.raw.json`); analysis writes new files.
- Record for every job: job id, backend, qubit line, calibration snapshot, options (DD, twirling), shots, measured QPU seconds, circuit hashes. `evidence/hardware/QPU_LEDGER.json` is the running total; the IBM Open Plan allows 600 s per 28-day window.
- IonQ or any paid provider: never, unless the session prompt explicitly contains "paid provider approved by Digonto".

## 5. Compute rules (`decisions/004`, `configs/compute.yaml`, `docs/PERLMUTTER.md`)
Two machines only: the **laptop** (64 GB RAM, 6 cores / 12 threads; its GTX 1060 is not used — current PyTorch has no kernels for it) and **NERSC Perlmutter** (A100s). The laptop is shared with other Claude sessions; protecting them comes first.
- **Every computation goes through `python scripts/run.py -- <command>`** — tests, gates, datasets, training, twin runs, analysis scripts. Never call `python scripts/<x>.py` for computing work directly, never start background jobs, never run two su2qc computations at once (the runner's lock enforces it across sessions). Exceptions: `git`, `graphify`, `scripts/new_artifact.py`, `scripts/check_artifacts.py`, `scripts/jobs/*`, `scripts/env_check.py` and reading files.
- **What the runner does:**
  - *Classifies* the command. A GPU, or an estimated laptop time above 20 min, means **always Perlmutter**: it writes the numbered job `jobs/NNN_*.yaml` (with a step that rebuilds the dataset there from the same seed) and, with `--push`, commits and pushes it.
  - *Admits* light work only if there is room now. At least 16 GB of memory must stay available for others, and the load plus the job's threads must leave 2 logical CPUs free. Otherwise it waits up to 20 min, then sends the job to Perlmutter.
  - *Runs it capped:* nice 19, idle I/O, 2–4 threads, a memory ceiling of 4 GB by default and 16 GB at most, a time limit, and `oom_score_adj = 1000`, so the kernel kills this job before any other session's.
  - *Heals:* after a memory kill it retries once with twice the memory if there is room, otherwise it sends the job to Perlmutter. A timeout sends it to Perlmutter. A program error is never retried: read the log tail and fix the bug.
  - The exit code says what happened: 0 done here, 10 queued, 1 failed, 2 not run. The ledger is `.local_runs/ledger.jsonl`, and each attempt's log is in `.local_runs/logs/`.
- **Queued jobs:** commit and push the code before queueing; `run.py --push` (or `scripts/jobs/enqueue.py --push`) pushes the job file. The Perlmutter worker (`scrontab`, every 15 min) runs it with Slurm at that exact commit, resubmits automatically after TIMEOUT (twice the time), OUT_OF_MEMORY (twice the GPUs/memory), NODE_FAIL / PREEMPTED / LOST (up to 3 attempts), and pushes status, log tail and outputs to the `results` branch. Follow with `python scripts/jobs/status.py` (also shows the worker heartbeat); when COMPLETED, `python scripts/jobs/fetch.py NNN`. Compare the fetched dataset checksum with the laptop's and report it. A job FAILED by a program error is fixed in code and queued again as a new number.
- **Never** push to `results`, merge it into `main`, edit a job file after it is pushed, connect to Perlmutter yourself, or handle NERSC or IBM credentials. If `status.py` warns that the worker looks stopped, say so in the report and continue with laptop work.
- The IBM token stays on the laptop: twin jobs read a noise model built on the laptop and committed as a file (`--noise-model`), never `--backend`.
- Device: code calls `su2qc_jepa.compute.pick_device()` (CPU on the laptop, CUDA on Perlmutter); `SU2QC_DEVICE` overrides.
- Seeds: every stochastic step derives its seed from `numpy.random.SeedSequence` with a recorded master seed; twin seeds through `TwinRunner.seeds`. Adjacent integer seeds are forbidden (that bug voided the v0.5.0 error bars).

## 6. Writing rules (reports, prompts, docs, paper)
- Plain English; define every jargon word on first use (software and physics); never invent physics-sounding terms. If a label is yours (e.g. "Krylov chain", "KC-prep", "masked-coupling task"), say so once.
- Report order: what was asked, the concrete actions taken, what the result means, then problems and assumptions.
- Math in LaTeX; times in units of $1/g_E$; couplings as the four-tuple $(c_E,c_M,c_H,c_B)$.
- Never write "quantum advantage", "AI invented", or "first 2+1D"; "2+1D" is reserved for geometries with an interior vertex (≥ 2×3).
- A code graph is navigation, not review: never cite Graphify output as evidence that code is correct.

## 7. What the package already guarantees (do not re-derive, do re-run)
- Physics core: 82 states, sectors 2/20/38/20/2, electric degeneracies 16/16/18/16/16, named energies, resonance at $\mu^*=3/8$, two routes agree to 1e-16, Gauss law exact, the $g_E=1$ dynamics table of the physics notes reproduced.
- Chain carrier: Strang circuits equal the sector unitary to 1e-15; CZ counts 34/56/100/188 for $r=1,2,4,8$ at $K=12$; KC-prep exact with 11 rotations.
- Estimators unbiased (J0 row D3); twin seeds independent (D5); splits by rule (D6); artifact conventions enforced (`tests/test_repo_conventions.py`).

## 8. Where things are
| Path | What | Numbered? |
|---|---|---|
| `plans/` | plans (current one has `status: active`) | yes |
| `prompts/` | one prompt per Claude Code session, incl. repair/follow-up prompts | yes |
| `reports/` | one report per session, plus analysis/review reports | yes |
| `decisions/` | decision records (conventions, thresholds, tool versions) | yes |
| `figures/` | every figure cited by a report or the paper | yes |
| `templates/` | templates used by `new_artifact.py` | no |
| `docs/` | living documents: PHYSICS, CLAIMS, PREREGISTRATION, PAPER_OUTLINE | no |
| `src/su2qc_jepa/` | `physics, data, models, twin, hardware, gates, repo` | no |
| `scripts/`, `configs/`, `tests/` | CLIs, thresholds/budget, tests | no |
| `jobs/` | job requests for the Perlmutter worker (YAML); results come back on the `results` branch | yes |
| `.local_runs/` | the laptop runner's ledger and logs (git-ignored) | no |
| `evidence/` | machine records: gate JSON, ledger, hardware jobs, fetched job status/logs, graph stats (UTC-stamped) | no |
| `graphify-out/` | code graph: `graph.json`, `GRAPH_REPORT.md` committed; the rest ignored | no |
| `data/`, `runs/` | datasets and models (local, not committed) | no |

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
