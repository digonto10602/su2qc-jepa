---
id: reports/016
title: 'Hand-over report: full project state, results, data and how to continue (28 Oct 2026)'
series: reports
created_utc: '2026-10-28T23:22:20Z'
author: claude-code
milestone: M3
status: done
supersedes: null
superseded_by: null
---

# Hand-over report: full project state, results, data and how to continue (28 Oct 2026)

**Milestone:** M3 (in progress) · **Prompt:** none of its own (a hand-over requested by Digonto in a coordinator session; the work in force is `prompts/003`, with `prompts/010` for M2a) · **Written:** 2026-10-28 23:22 UTC (repository `main` at commit `db8ab2c`) · **Earlier full reports:** `reports/012` (plan, physics, methods, J1 plot data up to 6 Oct), `reports/013` (M2a close), `reports/014` (preregistration), `reports/015` (desktop worker, `v1_final`, J2) · **Status vocabulary:** PASS / FAIL / PARTIAL / NOT RUN / VOID only. **No hardware job has ever run.** Every noisy number in this report is **EMULATED** (simulated on a computer); nothing here is a measurement on a quantum machine.

## What was asked
Digonto asked for a hand-over report: if they shut down now and a fresh agent starts a new session, that agent should read **only this report** and know what the project is, what was assumed, what was done, what was found (all results, with the data to re-make every plot, for example on claude.ai), the repository, the in-flight state and exactly how to continue. This is a documentation task. No code, configuration, data, job or `STATE.json` was changed, and nothing was committed, pushed or queued.

## Actions taken (to write this report)
1. Read the two instruction files (`~/.claude/CLAUDE.md`, `CLAUDE.md`), `reports/012`–`015`, `decisions/005`–`010`, `docs/PREREGISTRATION.md`, `docs/CLAIMS.md`, `docs/DESKTOP.md`, `configs/gates.yaml`, `configs/compute.yaml`, `STATE.json`, `evidence/GATE_LEDGER.md`, the plan's schedule, the job files 019–033, and the evidence files named below.
2. Looked up the job queue (`python scripts/jobs/status.py`), the `results` branch (`git fetch`, `git show origin/results:NNN/...`) and CI (`gh run list`), all read-only.
3. Ran two helper scripts through the runner (`python scripts/run.py --no-queue --threads 1 -- python .local_runs/probe/<script>.py`, both exit 0, about 2 s each): `j1_tables.py` (J1 data for all 14 configurations plus `v1_final`) and `twin_tables.py` (twin, null-check, cross-carrier and device tables). Their output is pasted into section 7; the scripts are in Appendix D.
4. Created this file with `python scripts/new_artifact.py reports ...` and set `status: done`.

## How to read this report (reading guide)
- **Order:** section 1 (words and glossary) → 2 (goal, claims, preregistration) → 3 (physics and methods, short) → 4 (how to operate the machines and the repository) → 5 (chronology) → 6 (all results) → 7 (data to redraw every plot) → 8 (state right now) → 9 (how to continue, exact commands) → 10 (problems) → appendices.
- **If you only have five minutes:** read the "Executive summary" below, then section 8 and section 9.
- **Source rule:** every number names the file it came from. "Not recorded" means I looked and did not find it.
- **Where this report and `STATE.json` disagree, this report is newer.** `STATE.json` still says M3 report `reports/015`, does not list jobs 023–033, the Quantinuum twins, `decisions/008`–`010` or the cross-carrier finding. It was not edited (instruction: change no file).

## Executive summary (state on 28 Oct 2026, 23:22 UTC)
- **Project.** A small learned model (a "JEPA world model", defined in section 1) is trained on simulated measurement records of an exactly solvable SU(2) lattice gauge theory (one plaquette, 4 sites, 4 links; "string breaking"). The aim is a methods-and-benchmark paper, **not** a computational advantage.
- **Gates (pass/fail checks fixed in advance).** J0 (data and physics) **PASS**. J1 (training health) **FAIL** after 14 configurations and a fresh-seed confirmation. J2 (forecasting), preregistered, on `v1_final`: **FAIL** (on-family passes the error bound, strong coupling fails it). J3 (hardware error signal): **NOT RUN** on hardware; simulated "twin" rehearsals with `v1_final` (IBM Kingston, IBM Marrakesh, Quantinuum H2-2; Helios-1 pending) all **FAIL** the Spearman rows (they are rehearsals, not J3 results).
- **Newest finding.** `v1_final`'s encoder treats every twin or hardware record as far outside its training distribution, because three input columns (the flag rate and the source and carrier labels) were constant during training and are blown up by the input normalisation to about 316 times their value (`evidence/twin/cross_carrier/cross_carrier.json`). The twin rehearsals with `v1_final` are therefore dominated by an artifact. Digonto approved (28 Oct, `decisions/010`) replacing the J3 model by `v2_final` (encoder reads only the 18 physical observables).
- **In flight.** `jobs/032` (Quantinuum Helios-1 twin) RUNNING on the desktop; `jobs/033` (train `v2_final`, 5 seeds, 200 epochs) QUEUED behind it. Results of `jobs/031` are on the `results` branch but **not yet fetched into `main`**.
- **Hardware.** No QPU job, ever; the IBM account is gone (21 Oct); Quantinuum is simulation only. Whether to get new hardware access or write a simulation-and-twin paper is **undecided** ("decide later").
- **Next.** Fetch 031 and 032; when 033 finishes, fetch and commit `v2_final`; redo the cross-carrier check and the four twin campaigns with `v2_final`; then the remaining M3 items (resonance estimator, figures F1/F2) and the hardware decision (section 9).

---

## 1. Glossary (every technical word used)

**Physics**
- **SU(2) gauge theory / lattice gauge theory.** A model of forces between particles in which the force field lives on the links of a small grid (the lattice). SU(2) is the symmetry group; "gauge" means a redundancy of description that physical states must respect (Gauss law, below). This project uses the smallest 2D unit, one square (a **plaquette**): 4 sites (vertices) and 4 links.
- **String breaking.** A stretched flux tube ("string") between two charges ends up replaced by two shorter tubes plus new particle pairs when it is stretched enough. The observable is the fraction of probability in "broken" states.
- **Gauss law.** The rule that fixes the electric flux at each vertex by the charge there. States obeying it are "gauge invariant"; there are exactly 82 for this plaquette.
- **$g_E$, $\mu$, $(c_E,c_M,c_H,c_B)$.** $g_E=g^2/2a$ is the energy unit; $\mu=m/g_E$ the dimensionless mass; the four coefficients weight the electric, mass, hopping and plaquette terms of the Hamiltonian $H$ (the energy operator). All times are in units of $1/g_E$.
- **Sector / $N$.** The Hamiltonian conserves the matter number $N=0,2,4,6,8$; the sectors have 2/20/38/20/2 states. The string starts in the $N=4$ sector.
- **S3, S1, MM, $B\bar B$, Loop.** Names of basis states: stretched string (3 flux links), short string (1 link), two mesons, baryon–antibaryon, closed flux loop. $P_{\text{meson}}$ and $P_{\text{baryonic}}$ are the probabilities in the meson and baryonic channels; $C_{\text{string}}$ is a string correlator (definition in `physics/observables.py`).
- **Resonance $\mu^*=3/8$.** The mass at which three pairs of states become degenerate; at strong coupling the breaking fraction peaks sharply there.
- **Fingerprint (two meanings in this repo).** (a) *Physics fingerprint*: a number the code must reproduce exactly (82 states, energies, etc.), asserted by tests. (b) *Dataset fingerprint*: sums and sampled values stored with a dataset so that a rebuild on another machine can be compared without moving the arrays (`scripts/compare_fingerprints.py`).

**Measurement and circuits**
- **Shots.** Repeats of one quantum measurement; the estimate of a probability has noise of order $1/\sqrt{\text{shots}}$ (about 0.016 at 4,096 shots; 0.044 at 512).
- **Carrier.** The way the physics is put on a measurement device. **Diagonal carrier:** records of configuration-basis probabilities (the training data). **Krylov-chain carrier (KC; my label for it):** the 38-state sector is compressed into a 12-qubit nearest-neighbour spin chain (Lanczos/Krylov construction) so that a real device could run it; "KC-Trotter" steps the chain in time, "KC-prep" prepares the state at time $t$ directly.
- **Trotter / Strang splitting.** Approximating $e^{-iHt}$ by a product of short steps; $r$ is the number of steps ("depth").
- **CZ.** A two-qubit gate on IBM machines. Cost for the chain: 34/56/100/188 CZ for $r=1,2,4,8$ at $K=12$.
- **Flag (rate).** A shot of the chain carrier in which the number of excited qubits is not 1 is a detected error; the fraction is the flag rate. It is an *encoding* flag, not a gauge-violation flag.
- **Post-selection.** Throwing away flagged shots before estimating.
- **QPU.** Quantum processing unit (the quantum chip). **Open Plan:** IBM's free tier (600 QPU-seconds per 28 days; no longer available to us).
- **rzz.** The native two-qubit "ZZ rotation" gate of Quantinuum's ion-trap machines (all-to-all connectivity).
- **Kraus operators.** The matrices that describe a noise process as a list of possible errors. A bug in saving them broke loading of IBM noise models (section 10).
- **SPAM.** State-preparation and measurement error. **Depolarising noise:** with some probability the qubit state is replaced by random noise. **Memory error:** error while a qubit idles (modelled as phase flips). **Average infidelity:** average loss of overlap with the ideal gate.
- **Calibration snapshot.** The stored table of a device's measured error rates on one date.
- **Nexus / qnexus.** Quantinuum's cloud portal and its Python client; Digonto has read access to device specifications. **Heron, Kingston, Marrakesh:** IBM chip family and two device names. **H2-2, Helios-1:** two Quantinuum machines.

**Machine learning**
- **JEPA (joint-embedding predictive architecture).** A model that predicts the *latent* (compressed) representation of a future measurement instead of the measurement itself. Parts: **encoder** (observation → 16-number latent), **predictor** (latent + actions → future latent), **grounding heads** (latent → known physical numbers, used as a check).
- **SIGReg.** A loss term pushing latents to look Gaussian; it fights collapse (all latents identical).
- **Effective rank.** A measure of how many latent directions are used (definition in `models/train.py: diagnostics`; not re-derived here). Gate: $\ge 8$ of 16.
- **Grounding $R^2$.** How well a linear readout of the latent predicts energy, $C_{\text{string}}$, $P_{\text{meson}}$, $P_{\text{baryonic}}$ ($R^2=1$ is perfect).
- **Semigroup residual.** Relative squared mismatch between predicting two steps at once and predicting one step twice. Gate: $<10^{-3}$.
- **Normalisation (BatchNorm).** A layer that subtracts the training mean and divides by the training standard deviation of each input column. If a column was constant in training (variance $5.6\times10^{-45}$), any other value is multiplied by about $316$; this is the cause of the cross-carrier finding.
- **Seed / SeedSequence.** The starting number of a random generator; all seeds are derived from one recorded master seed (adjacent integer seeds are forbidden).
- **Masked-coupling task.** The same forecast with the couplings hidden from the model (it must infer them). Ridge: linear regression with a penalty. Autoregressive baseline: a one-step network rolled out repeatedly. Supervised MLP: a network trained directly to output the target.
- **MAE.** Mean absolute error. **Spearman correlation:** correlation of ranks (1 = same ordering). **AUROC:** probability that a randomly chosen "arm B" point gets a higher score than a randomly chosen "arm A" point (0.5 = chance, 1 = perfect separation).

**Project process**
- **Gate / ledger.** A scripted pass/fail check with thresholds in `configs/gates.yaml`; each run appends to `evidence/GATE_LEDGER.md`.
- **Preregistration.** Fixing hypotheses, thresholds and analysis before the data that test them exist (git tag `prereg-2026-10-16`).
- **Decision record.** A numbered file in `decisions/` that explains any change to a frozen thing.
- **Twin.** A classical simulation of the 12-qubit chain circuits with a device's noise (Qiskit Aer, density-matrix method), used as the stand-in for hardware. **Arm A / arm B:** A is the nominal noise; B a degraded copy (IBM files: CZ and readout errors scaled 2x in the noise model, which `decisions/009` says is about 1.8x in CZ average infidelity; Quantinuum: all errors x2) standing in for a worse device or day. **Twin campaign:** the grid 3 masses x 2 arms x 5 depths x 5 seeds = 150 circuits at 4,000 shots; the J3 scores are also computed at 512 and 256 shots by exact subsampling of stored counts.
- **Rehearsal.** Running the J3 gate on twin data instead of hardware data; recorded as `J3_twin_rehearsal`, never as J3.
- **Known-answer / null check.** A test whose correct outcome is known: here a noiseless twin must show flag rate 0 and no separation between arms A and B.
- **Cross-carrier check.** Measures how far apart the encoder puts records of the *same* state that differ only in carrier or label (section 6.9).
- **Queue worker / job queue.** A machine that polls `jobs/NNN_*.yaml` files on GitHub, runs them and publishes results on the `results` branch. **Cron:** the Linux scheduler that triggers the desktop worker every 15 minutes. **Deploy key:** an SSH key that can write to this one repository only. **Slurm / scrontab:** Perlmutter's job scheduler and its cron. **Node-hour:** one compute node for one hour (Perlmutter budget unit).
- **Graphify.** A tool that builds a code graph of the repository (`graphify-out/`); it is navigation, never evidence of correctness.
- **EMULATED.** A label for any number that came from simulation.

---

## 2. Project goal, claims, preregistration

### 2.1 Goal (plain English)
Train a JEPA world model on finite-shot measurement records of an SU(2) plaquette and test (i) whether it forecasts late-time string-breaking observables as well as simple baselines (hypothesis H2); (ii) whether its latent distance gives a **label-free error signal** for a quantum device, that is, a way to tell how wrong a device record is without knowing the true answer, validated where the truth is known (H3); (iii) whether a compact 12-qubit carrier with controllable depth supports depth extrapolation (H4) and a hardware observation of the resonance (H5). The plan (`plans/001`) runs 5 Oct – 29 Nov 2026 and ends in a methods-and-benchmark paper (preprint target 27 Nov). The goal is **not** a computational advantage: everything is exactly solvable on a laptop.

### 2.2 Claims allowed and forbidden (`reports/012` §1, `CLAUDE.md` §6, `docs/CLAIMS.md`)
- **Allowed only if the matching gate passes:** a 12-qubit, 22-CZ-per-step carrier with a depth ladder and encoding flag; a JEPA forecaster compared with baselines; a label-free error signal validated where truth is known; a hardware observation of the strong-coupling resonance through a compressed carrier; an open benchmark dataset with checksums and a preregistered evaluation.
- **Never:** "quantum advantage"; "AI invented"; "first 2+1D"; "2+1D" for this plaquette (reserved for geometries with an interior vertex, at least 2x3); new SU(2) physics, a continuum limit or a string tension; hardware evidence of gauge leakage; scalability of the carrier.
- **Claims ledger now (`docs/CLAIMS.md`):** C1–C5 PROVEN or MEASURED; C7 (JEPA meets H1) MEASURED not met; C8 (H2) MEASURED not met; C9–C11 (H3–H5) UNVERIFIED; C12 (all noisy numbers) EMULATED.

### 2.3 Hypotheses (`docs/PREREGISTRATION.md` §1; thresholds in `configs/gates.yaml`)
H1 no collapse (rank $\ge 8$; $R^2$: energy $\ge0.887$, $C_{\text{string}}\ge0.99$, $P_{\text{meson}}\ge0.95$, $P_{\text{baryonic}}\ge0.98$; semigroup $<10^{-3}$; 5 seeds) — **already measured, not met**. H2 forecasting (MAE $\le 0.05$ at +4 and +8 steps on each held-out family; within $1.1\times$ of ridge and autoregressive on at least 2 of 3 targets) — **not met (J2 FAIL)**. H3 label-free error signal (on at least 24 points: Spearman(`jepa_twin`, exact error) $\ge0.7$ at 512 shots; non-inferior to `raw_twin` by margin 0.05; AUROC $\ge0.8$ at full shots; 3 calibration days) — **NOT RUN on hardware**. H4 depth extrapolation, H5 resonance within 0.05 of $\mu^*=3/8$ — **NOT RUN**.

### 2.4 Preregistration and its deviations
Signed by Digonto on 15 Oct 2026 22:02 UTC; annotated git tag `prereg-2026-10-16` on commit `d7655e2` (tag object `496f958`). Frozen: `configs/gates.yaml` (sha256 `dbb297336a329b723326fd736b93ce7b6e06b473128c1c2aa4e4f4144b0aa078`), the three dataset checksums, the model configuration (sha256 `cd4faece6fcb3dafd4f84e112e6028fb228c4fa8d809f6d0061cafc8a4ec968c`), the analysis commands (§3 of the document). Hashes: `evidence/prereg/hashes.json`.

| # | date | what changed | why | made before | record |
|---|---|---|---|---|---|
| (pre) | 5 Oct | J1 energy threshold 0.99 to 0.887 ($=0.97\times0.9145$, the best $R^2$ any regressor reaches from one clean observation) | the old threshold was unreachable: the observation lacks the off-diagonal hopping and plaquette terms | any J1 run, and before the tag (so not a deviation) | `decisions/005` |
| D1 | 21 Oct | dataset-equivalence rule: per-trajectory-sum bound $10^{-12}$ corrected to $\le10^{-12}$ per value and $\le10^{-10}$ per trajectory sum (inputs still bit-identical) | the signed bound contradicted the rebuild quoted in the same row ($5.7\times10^{-12}$, rounding) | `v1_final` existed | `decisions/007` |
| D2 | 22 Oct | J3 gate code scores the low-shot rows at 512 shots (the preregistered level) instead of the lowest level present (256) | code and preregistration disagreed; thresholds and commands unchanged | any hardware data | `decisions/008` |
| D3 | 28 Oct | J3 model becomes `v2_final`: same configuration, encoder reads only the 18 physical observables, master seed 16180339 (`JEPAConfig.encoder_inputs=18`, `train_jepa.py --physics-only`) | cross-carrier check: `v1_final` is off-distribution on twin/hardware records | any hardware data (no hardware data exist) | `decisions/010` |

The J2 result (`v1_final`, FAIL) **stands**; J2 is not repeated on `v2_final` (its forecast and J1 numbers will be "for information"). The preregistered J3 command (`docs/PREREGISTRATION.md` §3) is used with `runs/v2_final/seed0/model.pt` in place of `runs/v1_final/seed0/model.pt`. Not frozen and still open: the pilot QPU cap (90 s in `prompts/004`, 120 s in `configs/hardware_budget.yaml`), and the estimator-bias rule (2.5 vs 4.0 standard errors; the gate file governs; measured 2.36 and 1.44).

**Disclosure the paper must carry.** J1 failed before the preregistration; 13 configurations were searched on the same validation split that J1 scores (only `v1_confirm` is free of that selection); the preliminary forecast numbers of `v1_confirm` were seen before the tag, so J2 was scored on a fresh run (`v1_final`); the twin rehearsals informed D3.

---

## 3. Physics and methods (short; depth in `reports/012` §2–§4)

**Model.** Hard-core SU(2) Kogut–Susskind plaquette: link flux $j_\ell\in\{0,\tfrac12\}$ on 4 links, two-colour staggered fermions on 4 vertices, open boundaries, in units of $g_E$:
$$\frac{H}{g_E}=c_E\mathcal E+c_M\mathcal M+2c_H\mathcal T+c_B\mathcal B,$$
with electric, mass, hopping and plaquette terms; staggered phases $\eta=(+1,+1,+1,-1)$ and a *negative* magnetic coefficient as one joint convention (frozen, `decisions/000`, `src/su2qc_jepa/physics/conventions.py`). On-family couplings: $c_E=1$, $c_M=\mu$, $c_H=1/(2g_E)$, $c_B=-1/(4g_E^2)$. Points: P-A ($g_E=2$, $\mu=3/8$): $(1,0.375,0.25,-0.0625)$; strong coupling P-S: $(1,0.375,0.02,-0.02)$.

**Verified (tests or J0).** 82 states, sectors 2/20/38/20/2, electric degeneracies 16/16/18/16/16; two independent routes agree to $4.4\times10^{-16}$; Gauss law exact; the $g_E=1$ dynamics table of the physics notes reproduced ($P_{\text{baryonic}}(t=1,2,3)=0.43185, 0.73219, 0.82096$); cross-check against the earlier verified code `su2qc` PASS, max deviation $7.3\times10^{-14}$ (`evidence/J0_data/crosscheck_su2qc.json`). Strong-coupling resonance at $\mu^*=3/8$: breaking fraction 0.554 at $\mu=0.375$ against 0.0715 at 0.30 and 0.0676 at 0.45 at $t=33.3$ (`reports/012` P11d). On-family mass dependence is weak and **not monotone** (0.628, 0.635, 0.625, 0.596, 0.531 for $\mu=0.15\ldots0.65$ at $t=3$; the plan wrongly says monotone).

**Chain carrier.** Lanczos from S3 in the 38-state sector gives a tridiagonal $H_K$; one-hot encoding on $K=12$ qubits makes it an XY chain. Strang circuits equal the in-sector unitary to $10^{-15}$; $K=12$ reproduces the P-A window ($t\le 3/g_E$) to $1.05\times10^{-4}$. CZ count $2[(r+1)\lceil (K-1)/2\rceil+r\lfloor (K-1)/2\rfloor]=34,56,100,188$ for $r=1,2,4,8$. Measurement settings Z (populations and flag) and X (real coherences).

**Observation and model.** Observation vector, dimension 24 (frozen, `data/records.py: ObservationSpec`): 18 physical observables (4 vertex occupations, 4 link $j(j+1)$, $P_{\text{pair}},P_{\text{meson}},P_{\text{baryonic}},P_{\text{vacmatter}},P_{S3},P_{S1},P_{\text{hopped}},P_{B\bar B},P_{\text{antivac}},C_{\text{string}}$) + flag rate (1) + source one-hot (3: exact/twin/hardware) + carrier one-hot (2: diagonal/chain). Actions $a_t=(\Delta t,c_M,c_H,c_B)$. Training rule: context = noisy record ($S\in\{256,512,1024,4096\}$ shots), target = encoding of the clean exact record. Encoder: non-affine BatchNorm then MLP $24\to128\to128\to16$ (`v2_final`: the first layer reads only the first 18 columns); predictor: action MLP and GRU (128); 5 grounding heads. 90,309 trainable parameters for latent 16 (`reports/012` §7.6; the count for `v2_final` is not recorded). Loss $\mathcal L=w_{\text{pred}}\mathcal L_{\text{pred}}+w_{\text{sigreg}}\mathcal L_{\text{sigreg}}+w_{\text{ground}}\mathcal L_{\text{ground}}+w_{\text{semigroup}}\mathcal L_{\text{semigroup}}$. Preregistered weights $(1,3,1,10)$, AdamW lr $2\times10^{-3}$, weight decay $10^{-5}$, batch 64, 200 epochs, cosine schedule, gradient clipping 1.0, 5 spawned seeds + masked-coupling runs.

**Datasets** (`evidence/J0_data/datasets.json`; master seed 20261005): `main` (20,000 trajectories, diagonal carrier, on-family + strong coupling, checksum `73fff8e5a7b7`, laptop reference), `chain_onfam` (5,000, `bdcd6e895a06`), `chain_strong` (3,000, `935692f343d8`, built on Perlmutter). Splits are by coupling label (held-out $g_E$ 1.3, 1.75, validation 1.45; held-out $\mu$ 0.3, 0.42, 0.5, validation 0.45), never by row. Build command: `python scripts/make_dataset.py --name main --n-traj 20000 --steps 8 12 --families onfam strong --carrier diagonal --starts S3 S3 S3 S1 random --quench-fraction 0.2 --seed 20261005 --out data/main`.

**Twin campaign.** `scripts/run_twin.py --name <twin> --K 12 --seeds 5 [--noise ideal | --noise-model <file>]`; grid $\mu\in\{0.3,0.375,0.5\}$ x arms A/B x depths $r\in\{1,2,4,6,8\}$ x 5 seeds, step $\Delta t=0.375$ (`--dt`), $K=12$ (the coupling point is set inside `scripts/run_twin.py`, not recorded here); 4,000 shots; `scripts/residual_eval.py --model <model.pt> --records <records.json> --out <residual_eval.json> --shots-levels 0 512 256` computes the scores `jepa_twin` (latent distance to the reference twin record), `jepa_self`, `jepa_t0`, `raw_twin` (observation-space distance), `flag_rate`, against `exact_error`; `scripts/run_gate.py J3 --eval <file> --rehearsal` scores them (the rehearsal reference is arm A / seed 0, which is therefore left out: 135 of 150 points per shot level).

---

## 4. Infrastructure and how to operate it

### 4.1 Rules of the house (read `CLAUDE.md` and `~/.claude/CLAUDE.md` first)
- **Reporting (Digonto's rules):** plain English; define jargon at first use; never invent physics-sounding terms (if a label is yours, say so); order = what was asked, actions, what the result means, problems; maths in LaTeX; every number with unit, uncertainty and the file or command that produced it.
- **Priorities (project `CLAUDE.md` §1):** physics correctness beats speed; evidence beats prose (every claim points to a file under `evidence/`, `runs/` or `figures/`); honesty about status (PASS/FAIL/PARTIAL/NOT RUN/VOID only; emulated numbers labelled EMULATED; nothing is "hardware" without an IBM job id).
- **The "physics loop" of the global file** (builder/tester/fixer/auditor/planner agents, `notes/STATUS.md`) applies only if `notes/STATUS.md` exists. It does not exist in this repository; the project `CLAUDE.md` governs, and where the two conflict the project file wins.
- **Frozen things** (change needs a `decisions/` record and a new version tag): `physics/conventions.py`; `configs/gates.yaml` after the tag; `data/records.py: ObservationSpec`; dataset checksums in `evidence/J0_data/`; artifact and graph conventions and the pinned `graphifyy`.
- **Stop conditions** (write the reason in the report, then end): a physics fingerprint test fails; two routes disagree above $10^{-12}$; a gate threshold would have to change to pass; the hardware budget file does not approve the manifest; 8 hours of wall time. Ask Digonto before: deleting data, rewriting history, pushing in ways not already part of the workflow, spending cluster allocation not in the prompt, and whenever an agent thinks a threshold itself is wrong.

### 4.2 Three machines
| machine | role | how it is used | state now |
|---|---|---|---|
| **Laptop** (Dell G7 7588, 64 GB RAM, i7-8750H, 6 cores / 12 threads; GTX 1060 not used; conda env `su2qc-jepa`, Python 3.12.14) | where Claude Code runs; light work; the only place with the Nexus login | **every** computation through `python scripts/run.py -- <command>` (never directly, never background jobs, never two at once); shared with other Claude sessions, whose protection comes first | in use |
| **Desktop** (Digonto's Linux box, RTX 3070 8 GB, `sm_86`, host `SupremeCommander`; env `~/.su2qc-jepa-env`) | queue worker for heavy and GPU jobs (`where: desktop`, the default since 21 Oct) | cron tick every 15 minutes; fetches GitHub, runs one job at a time at `nice 10` with `SU2QC_DEVICE=cuda`; interrupted jobs (the desktop is sometimes switched off) are rerun, up to 3 runs, then LOST; pushes status, log tail and declared outputs (at most 50 MB, never `.npz`) to the `results` branch; deploy key `~/.ssh/su2qc_deploy_desktop` (write access to this repo only; no IBM token on it) | last heartbeat 2026-10-28 23:07 UTC; job 032 RUNNING since 23:15 |
| **Perlmutter** (NERSC, A100, account `m4135_g`, `scrontab` every 15 min) | the original heavy worker | 4.318 of 50 node-hours used | **stopped**: no heartbeat since 2026-10-08 18:45 UTC. Needs `scrontab -l; cat $SCRATCH/su2qc-worker/tick_errors.log` on Perlmutter; not needed while the desktop works. Never connect to Perlmutter yourself |

### 4.3 The runner (`scripts/run.py`, `decisions/004`, `configs/compute.yaml`)
- It classifies the command: a GPU need or an estimated laptop time over 20 minutes means "heavy", which writes a numbered job file `jobs/NNN_*.yaml` (with a step that rebuilds the dataset from the same seed) and, with `--push`, commits and pushes it; otherwise "light".
- It admits light work only if at least 16 GB of memory stay free and the load plus its threads leaves 2 of the 12 logical CPUs free; otherwise waits up to 20 minutes, then queues (a command that cannot be queued is not run: exit 2).
- It runs capped: nice 19, idle I/O, 2 threads by default (4 max), memory ceiling 4 GB (16 GB max), a time limit, `oom_score_adj = 1000`. After a memory kill it retries once with double memory; a timeout goes to the queue; a program error is never retried.
- **Exit codes:** 0 done here, 10 queued, 1 failed, 2 not run (laptop busy: wait 60 s, retry), 3 bad usage. Ledger `.local_runs/ledger.jsonl`; per-attempt logs `.local_runs/logs/` (the script's standard output is in the log, not on the terminal).
- Allowed without the runner: `git`, `graphify`, `scripts/new_artifact.py`, `scripts/check_artifacts.py`, `scripts/jobs/*`, `scripts/env_check.py`, reading files. `--no-queue --threads 1` is the pattern for small analysis scripts.

### 4.4 The job queue
- **Queue a heavy job:** commit and push the code first, then `python scripts/run.py --push --where desktop -- <command>` (or `python scripts/jobs/enqueue.py ... --where desktop --push`). The job file is committed as `job: NNN_...`. **Never edit a job file after it is pushed.** A job that failed by a program error is fixed in code and queued again under a new number.
- **Follow:** `python scripts/jobs/status.py` (job table plus one heartbeat per worker; it warns that the Perlmutter worker looks stopped, which is known).
- **Fetch:** `python scripts/jobs/fetch.py NNN` copies the job's outputs into place; a local file that differs is kept and the job's copy goes to `evidence/jobs/NNN/outputs/` (so ledger files must be merged by hand, see section 9). Raw results are on branch `results` (`git fetch; git show origin/results:NNN/status.json`, `.../log.txt`, `.../outputs/...`). **Never push to `results` or merge it into `main`.**
- **"FAILED" in `status.py` does not always mean broken:** a gate that returns FAIL exits with code 1, so jobs 021, 022, 026–029, 031 show FAILED although they ran to a result. Read the log tail.
- Jobs may only run allowlisted scripts (`ALLOWED_SCRIPTS` in `src/su2qc_jepa/jobs.py`); the hardware-submission script is excluded.
- Each job file lists `steps`, `outputs`, `resources` (gpus, time) and the exact `commit` it runs at. Datasets are rebuilt on the worker from the manifest and seed and checked by fingerprint against the laptop reference (`decisions/007`).

### 4.5 Repository layout (details in Appendix B)
`plans/` `prompts/` `reports/` `decisions/` `figures/` `jobs/` are **numbered, append-only** artifacts created only by `python scripts/new_artifact.py <series> "<title>" --milestone Mx [--author ...] [--ext .png] [--supersedes prompts/NNN]` (never choose a name yourself; revisions are new numbers; `scripts/check_artifacts.py` must print `OK`). Living documents (`README.md`, `CLAUDE.md`, `docs/*`, `configs/*`, `STATE.json`) are edited in place. `evidence/` holds immutable UTC-stamped machine records; `data/` and `runs/` (datasets and models) are local and not committed, except the files deliberately copied into `evidence/runs/` so that queue workers can read them.

### 4.6 Code graph (Graphify)
`graphify-out/graph.json` and `GRAPH_REPORT.md` are committed. Use `graphify query "<question>"`, `graphify explain "<symbol>"`, `graphify path "<A>" "<B>"`, `graphify affected "<symbol>"` before grepping; rebuild with `bash scripts/graph_update.sh` (pins `PYTHONHASHSEED=0`; `--check` says FRESH or STALE; writes `evidence/graph/stats.json`). Latest committed stats (`evidence/graph/stats.json`, built at `72a15b4`): 1,243 nodes, 2,279 edges, 101 communities, 137 files; top hubs `PlaquetteModel` (degree 43), `trajectories.py` (38), `test_pipeline.py`. A graph is navigation, never evidence that code is correct.

### 4.7 CI and environment pins
GitHub Actions workflow `.github/workflows/ci.yml` (lint with ruff, artifact conventions, tests, graph freshness, physics fingerprints). Last three runs on `main` all `success` (latest: commit `db8ab2c`, run 40786421424). Run `ruff check src tests scripts` before pushing (CI lint failed unnoticed from 5 to 15 Oct because the session protocol only ran pytest). Pins (`pyproject.toml`): `qiskit>=2.5,<2.6`; `qiskit-aer>=0.17,<0.18` (aer 0.18.0 fails to load next to PyTorch in CI); `torch>=2.2` (laptop 2.14.1+cpu, desktop 2.14.1 with CUDA 13.0); extras `ml`, `ibm` (`qiskit-ibm-runtime`; CI installs it for the Kingston loading test; `evidence/ENV.json` shows 0.50.0), `quantinuum` (`qnexus==0.51.2`, laptop only), `dev` (`graphifyy==0.9.74`). Laptop environment on 15 Oct (`evidence/ENV.json`): Python 3.12.14, numpy 2.5.3, scipy 1.18.1, qiskit 2.5.2, qiskit-aer 0.17.2, scikit-learn 1.9.1.

### 4.8 Credentials and hardware rules (`CLAUDE.md` §4)
- Nothing goes to a QPU without, in this order: a dry-run manifest (`scripts/hw_dry_run.py`), a **human** editing `configs/hardware_budget.yaml` (`approved: true`, manifest hash, caps; currently `approved: false`, backend `ibm_torino`, `max_qpu_seconds: 120`, `max_jobs: 1`, `max_cz_per_circuit: 200`, `shots: 4000`), then `scripts/hw_submit.py submit --confirm`. Claude never edits `approved`, `approved_by`, `approved_utc`, `manifest_hash`; it proposes values in the report. One job per approval; raw counts immutable after `collect`; the QPU ledger `evidence/hardware/QPU_LEDGER.json` does not exist (spent: 0 s).
- **IBM account no longer available (21 Oct).** The IBM token was never to leave the laptop and is not on any worker.
- **Quantinuum (`decisions/009`):** Digonto has Nexus access. Device specifications were read once with `scripts/qtm_list_devices.py` (needs the Nexus login: **laptop only**). Nothing is ever submitted to Quantinuum hardware or cloud emulators, and IonQ or any paid provider is forbidden unless a session prompt contains "paid provider approved by Digonto".
- Seeds: `numpy.random.SeedSequence` with a recorded master seed; adjacent integer seeds are forbidden (that bug voided the v0.5.0 error bars).

### 4.9 Session protocol (project `CLAUDE.md` §2, condensed)
Start: read the two instruction files, the session prompt, `STATE.json`, newest report; `python scripts/env_check.py`; `bash scripts/graph_update.sh --check` and the first screen of `GRAPH_REPORT.md`; `python scripts/run.py -- python -m pytest -q` before touching physics. During: graph first; `graphify affected "<symbol>"` before changing a function. End: pytest and the milestone gate; `bash scripts/graph_update.sh`; session report via `new_artifact.py reports` with `status: done`; `python scripts/check_artifacts.py` prints OK; update `STATE.json`; scoped commits with prefixes `physics: data: model: twin: hw: gate: docs: chore:`, the graph refresh last as `chore(graph): refresh code graph`; show `git log --oneline -6`; never rewrite history. Committing and pushing happen only when asked (global rule); ask before pushing tags.

---

## 5. Chronology (compact; commit hashes from `git log`)

| date (2026) | event | commits / records |
|---|---|---|
| 1 Oct | planner sessions; `reports/000` audit of the v1 plan (15 problems, 5 severe); plan v2 with the Krylov-chain carrier, two coupling families and label-free baselines | `plans/001`, `reports/000` |
| 2 Oct | numbered artifacts and the code graph (`decisions/001`); compute policy laptop + Perlmutter (`decisions/002`–`004`); worker installed; laptop envs repaired; **M0 PASS** (repo public, CI green, 47 tests) | `88dc52d` (bootstrap), `reports/001`–`008` |
| 3–4 Oct | **M1:** cross-check against `su2qc` PASS ($7.3\times10^{-14}$); three datasets; **J0 PASS 9/9** | `reports/009`, `evidence/J0_data/20261003T201012Z.json` |
| 5 Oct | M2a: EMA/curriculum options, spawned seeds (`0a76800`); energy ceiling 0.9145 and threshold change (`decisions/005`, `2b10e5b`); ablation ladder queued (jobs 002–008); GPU baseline bug fixed (`3fd0a65`); dataset fingerprints (`ade81b0`); `fetch.py` fix (`3010090`) | `reports/010`–`012` |
| 5–8 Oct | 14 configurations trained on Perlmutter (jobs 002–008, 011–017) and gated; all **J1 FAIL**; `v1_wsig3_wsg10` passes on its selection seeds (`600197b`), fresh-seed `v1_confirm` fails (`8b384ac`); figures 000/001 (`76f4c6b`); model card; M2a closed (`29a04ee`); Perlmutter worker last heartbeat 8 Oct | `reports/013` |
| 15 Oct | CI lint repair (`c9ddfe6`); gates hashes (`09d6221`); preregistration draft (`5119b7a`), **signed** (`d7655e2`), tag `prereg-2026-10-16` | `reports/014` |
| 21 Oct | desktop worker (`bc7ba86`, `decisions/006`); `decisions/007`; `v1_final` trained (job 019, 1.156 h); dataset EQUIVALENT (job 020); **J2 FAIL** and J1-on-`v1_final` FAIL (`07c13ca`); `v1_final` seed0 model committed (`6479fb1`); noiseless twin `ideal0`, all known-answer checks PASS (`63a42ff`, job 023); IBM account gone | `reports/015` |
| 21–22 Oct | calibrated IBM twin noise from stored snapshots (`fd35c18`); Kraus-loading bug found and fixed (`2e26d37`; jobs 024, 025 FAILED); reruns (jobs 026, 027); J3 rehearsal mode (`ff559cf`); rehearsals scored at 256 shots (`1b81156`, files forgotten and added in `b8600a6`) | `evidence/J3_twin_rehearsal/20261022T*.json` |
| 22–26 Oct | `decisions/008` (512-shot low level, `efcdac9`, `467b4a9`); re-scored at 512 (`5f28dfe`): both FAIL; same-second record overwrite fixed (`ce4238f`, `b92e08c`) | `20261026T181452Z.json`, `20261026T181636Z.json` |
| 28 Oct | cross-carrier check (`4423047`, job 030, `ac7e920`): `v1_final` encoder off-distribution; Quantinuum noise model and twins from Nexus specs (`3be8941`, `31a0cd1`, `decisions/009`); jobs 031 (done), 032 (running); physics-only encoder option (`aef9885`); `decisions/010` (`72a15b4`); job 033 queued (`db8ab2c`) | this report |

Note: the repository's first commit is `88dc52d` (2 Oct 2026); `git log --oneline | wc -l` gave 138 commits at the time of writing.

---

## 6. Results in full

Status of every gate, from `evidence/GATE_LEDGER.md` and the records it points to: **J0 PASS · J1 FAIL · J2 FAIL · J3 NOT RUN (twin rehearsals on three distinct twins, all FAIL, `v1_final`; Helios-1 pending) · J4 NOT RUN (optional)**. Nothing below is a hardware result.

### 6.1 J0, the data and physics gate: PASS, 9 of 9 rows (`evidence/J0_data/20261003T201012Z.json`)
| row | status | measured | threshold |
|---|---|---|---|
| D1 state counts | PASS | 82; sectors 2/20/38/20/2; electric 16/16/18/16/16 | same |
| D2 two-route agreement | PASS | $4.44\times10^{-16}$ | $10^{-12}$ |
| D2 Gauss-law commutator | PASS | 0 | $10^{-12}$ |
| D3 estimator bias, diagonal carrier (1,024 shots, 200 trials; max over 18 observables of $|\text{bias}|/\text{SE}$) | PASS | 2.36 SE | 4.0 SE |
| D3 estimator bias, chain carrier (Z+X) | PASS | 1.44 SE | 4.0 SE |
| D4 Krylov $K=12$ reproduces the P-A window $t\le 3/g_E$ | PASS | $1.05\times10^{-4}$ | $10^{-3}$ |
| D5 twin repeats independent | PASS | 5 of 5 distinct, $\sigma(p_1)=0.0147$ | 5 |
| D6 split leakage | PASS | 0 | 0 |
| D6 checksum recorded | PASS | `73fff8e5a7b7` | present |

Plus the independent cross-check against `su2qc` (`evidence/J0_data/crosscheck_su2qc.json`): PASS, max deviation $7.3\times10^{-14}$, tolerance $10^{-10}$ (J0 was run on the laptop copy of `data/main` only).

### 6.2 Energy ceiling (J1 input; `evidence/J1_training/ceiling_main.json`, `data/main` `73fff8e5a7b7`, validation split 26,348 rows)
Best validation $R^2$ for predicting each grounding target from **one clean observation** (and with the step's couplings $(c_M,c_H,c_B)$ appended):

| target | ridge | 5-NN | boosted trees | MLP | with couplings (best) |
|---|---|---|---|---|---|
| energy | 0.88684 | 0.85088 | 0.89016 | **0.91445** | 0.99412 (MLP; trees 0.9851, 5-NN 0.9696, ridge 0.9509) |
| $C_{\text{string}}$ | 1.00000 | 0.99720 | 0.99997 | 0.99990 | 1.0000 |
| $P_{\text{meson}}$ | 1.00000 | 0.98865 | 0.99598 | 0.99998 | 1.0000 |
| $P_{\text{baryonic}}$ | 1.00000 | 0.99685 | 0.99996 | 0.99995 | 1.0000 |

The energy $E=\langle c_E\mathcal E+c_M\mathcal M+2c_H\mathcal T+c_B\mathcal B\rangle$ contains the off-diagonal hopping and plaquette terms, which the 18 diagonal observables do not contain; hence the cap 0.9145. This gave the J1 energy threshold $0.887=0.97\times0.9145$ (`decisions/005`). Weakness: a better regressor could raise the ceiling slightly; the 10-epoch laptop check already reached 0.895.

### 6.3 J1, the training-health gate: FAIL after 14 configurations plus a fresh-seed confirmation
Each configuration = 5 seeds x 200 epochs on `data/main`; values = final epoch on the validation split, min (or max for the semigroup) over seeds, exactly as the gate compares them. Source: `evidence/GATE_LEDGER.md`, `evidence/J1_training/*.json`, and my recomputation from `runs/<run>/seed*/history.json` (table P8y in §7, which agrees with the ledger). Thresholds: rank $\ge8$; $R^2$ energy $\ge0.887$, $C_{\text{string}}\ge0.99$, $P_{\text{meson}}\ge0.95$, $P_{\text{baryonic}}\ge0.98$; semigroup $<10^{-3}$.

| # | run (change) | job | rank min (max) | $R^2$ $P_{\text{meson}}$ min | semigroup max | gate |
|---|---|---|---|---|---|---|
| 1 | `v1_base` ($w_{\text{sigreg}}=0.5,w_{\text{sg}}=0.1$) | 002 | 5.156 (6.154) | 0.978 | 3.29e-3 | FAIL |
| 2 | `v1_wsigreg2` | 003 | 8.263 (9.104) | 0.972 | 5.34e-3 | FAIL |
| 3 | `v1_wsigreg5` | 004 | 10.525 (10.943) | 0.968 | 8.47e-3 | FAIL |
| 4 | `v1_latent32` (latent 32) | 005 | 6.116 (6.575) | 0.977 | 4.72e-3 | FAIL |
| 5 | `v1_ema` (EMA target, $\tau=0.996$) | 006 | 13.086 (13.475) | **0.915 (row FAIL)** | 2.21e-2 | FAIL |
| 6 | `v1_wground3` ($w_{\text{ground}}=3$) | 007 | 5.629 (6.142) | 0.983 | 6.94e-3 | FAIL |
| 7 | `v1_curriculum` (50 epochs on horizons 1–2 first) | 008 | 6.176 (7.128) | 0.979 | 2.86e-3 | FAIL |
| 8 | `v1_wsemigroup1` ($w_{\text{sg}}=1$) | 011 | 4.938 (5.799) | 0.979 | 1.72e-3 | FAIL |
| 9 | `v1_wsig2_wsg1` | 012 | 8.560 (9.621) | 0.973 | 5.57e-3 | FAIL |
| 10 | `v1_wsig2_wsg3` | 013 | 8.071 (8.950) | 0.974 | 1.17e-3 | FAIL |
| 11 | `v1_wsig2_wsg5` | 015 | 7.804 (8.517) | 0.977 | 1.01e-3 | FAIL |
| 12 | `v1_wsig2_wsg10` | 014 | 7.415 (7.748) | 0.973 | 9.2e-4 | FAIL (rank) |
| 13 | `v1_wsig3_wsg10` ($w_{\text{sg}}=10,w_{\text{sigreg}}=3$) | 016 | 8.257 (9.098) | 0.971 | 7.8e-4 | **PASS** (on its selection seeds) |
| 14 | `v1_confirm` (= 13, master seed 31415926) | 017 | 8.447 (8.682) | 0.968 | **1.482e-3** (seed 3; others 3.2e-4 to 7.3e-4) | **FAIL** |
| F | `v1_final` (= 13, master seed 27182818; information only) | 019 | **7.967** (8.896) | 0.976 | 8.6e-4 | FAIL (rank, by 0.03, one seed) |

Energy, $C_{\text{string}}$ and $P_{\text{baryonic}}$ $R^2$ pass in all 15 rows; $P_{\text{meson}}$ passes in all but `v1_ema`. Energy $R^2\approx0.90$ is within 0.015 of the ceiling.

**What it means.**
1. The latent does not collapse and the grounding works; the failure is the predictor's consistency (semigroup) and, in some rows, the rank.
2. Raising the SIGReg weight raises the rank (5.2 to 6.2 at weight 0.5; 8.3 to 9.1 at 2; 10.5 to 10.9 at 5; EMA 13.1 to 13.5). The semigroup residual rises with the rank (Pearson $r=0.898$ between rank and $\log_{10}$ residual over the 30 unmasked final points of rungs 1–6; correlation across runs that also differ in loss weights, not a proven mechanism) and falls with $w_{\text{sg}}$.
3. The residual varies about 5x between seeds, so "worst of 5 seeds" depends on one unlucky seed. With the couplings masked the residual is about $2\times10^{-4}$, so the inconsistency comes from how the predictor uses the coupling inputs.
4. Configuration 13 was found by searching on the validation split that J1 scores; the fresh-seed confirmation shows its pass was partly luck. Rule agreed before that run: J1 = **FAIL**. The plan's PARTIAL fallback is written for the rank row only, so the status stays FAIL (Digonto's decision).
5. Working model for M3: $(w_{\text{pred}},w_{\text{sigreg}},w_{\text{ground}},w_{\text{semigroup}})=(1,3,1,10)$, latent 16 (`docs/MODEL_CARD.md`, describes the v1 era).

Cost: about 1.0 h and 0.27 node-hours per rung of 5 unmasked seeds on an A100 (2.1 h with masked seeds); desktop RTX 3070: 1.16 h for `v1_final` including masked seeds.

### 6.4 Dataset reproducibility (laptop vs workers)
Source: `evidence/J0_data/fingerprint_compare_*.json`; rule `decisions/007` (inputs `ctx`, `act`, `valid` bit-identical; `tgt`, `energy` within $10^{-12}$ per value and $10^{-10}$ per trajectory sum).

| comparison | inputs | `tgt` max per sampled value / per trajectory sum | `energy` max per sampled value / per sum | verdict |
|---|---|---|---|---|
| `main` laptop (`73fff8e5a7b7`) vs Perlmutter (`76f4c9055591`) | bit-identical | $5.7\times10^{-14}$ / $5.7\times10^{-12}$ (2,513 of 20,000 trajectories above $10^{-12}$) | $1.9\times10^{-13}$ / $2.5\times10^{-12}$ (37 above) | equivalent under `decisions/007` |
| `main` laptop vs desktop (`v1_final`, job 019) | bit-identical | same numbers (the desktop equals the Perlmutter rebuild) | same | **EQUIVALENT** (job 020) |
| `gpu_smoke` laptop vs desktop | bit-identical | $5.0\times10^{-14}$ / $2.7\times10^{-12}$ | $2.0\times10^{-13}$ / $1.6\times10^{-12}$ | equivalent |
| `gpu_smoke` desktop vs Perlmutter | bit-identical | 0 / 0 | 0 / 0 | identical |

Consequence: the noisy training inputs of laptop, Perlmutter and desktop runs are the same; only the clean targets carry rounding noise of order $10^{-13}$.

### 6.5 J2, the preregistered forecasting gate: FAIL (`evidence/J2_forecast/20261021T201507Z.json`, model `v1_final`)
MAE (mean absolute error, dimensionless probabilities), mean of 5 seeds, held-out split, context step 4 with 512 shots, scored 4 and 8 steps later, for $P_{\text{baryonic}}$ / $P_{\text{meson}}$ / $C_{\text{string}}$ (full table with sources in §7.5). Gate rows: on-family (2,935 trajectories) JEPA MAE $\le0.05$ PASS at +4 (0.032) and +8 (0.049); not worse than ridge PASS (3 of 3 targets at both horizons); not worse than autoregressive **FAIL at +4** (1 of 3; JEPA 0.032/0.014/0.020 vs autoregressive 0.030/0.011/0.014) and PASS at +8. Strong coupling (3,134 trajectories): JEPA MAE $\le0.05$ **FAIL** at +4 (0.105 from $P_{\text{baryonic}}$) and +8 (0.123); not worse than ridge **FAIL at +4** (0 of 3), PASS at +8; not worse than autoregressive PASS at both.

What it means: H2 is not met. On-family, JEPA meets the bound and beats ridge. At strong coupling, $P_{\text{baryonic}}$ is off by more than twice the bound. JEPA's advantage grows with horizon: at +8 it beats ridge and autoregressive on every target in both families. The supervised MLP (reported, not gated) is about as good as JEPA, so the results support parity, not superiority. With couplings masked, JEPA's error at +8 is 2 to 5 times lower than masked ridge's. Per the plan (§9) the forecasting claim is "mixed" and J3 becomes the primary outcome. Not yet done: the resonance estimator ($\mu^*$ from forecasts) and figures F1 and F2 (`prompts/003`).

### 6.6 Noiseless twin `ideal0`: all known-answer checks PASS (job 023; `evidence/twin/ideal0/null_check.json`, `63a42ff`)
150 points (3 masses x 5 depths x 2 arms x 5 seeds, $K=12$, 4,000 shots), no noise, `v1_final` seed 0.
- Flag rate exactly 0 at all 150 points. PASS.
- Post-selected populations consistent with $|c_k|^2$: KS statistic 0.0754, p-value 0.343; fraction of points with p<0.01 = 0.0067; 0 points with p<$10^{-3}$; minimum p = 0.0023. PASS.
- Arms A and B not separated by any score: $|\text{AUROC}-0.5|$ at most 1.17 null sigma (`jepa_twin` 1.17, `raw_twin` 0.98, `jepa_self` 0.05, `jepa_t0` 0.08; null sigma 0.0502). PASS.
- Max |twin - ideal| = 0.0653 (shot noise only); max |ideal - exact| = 0.0127 (Trotter error). Reported.
- **Null floor for the Spearman rows.** Even without any device noise, Spearman(score, exact error) is 0.15 to 0.29 for `jepa_twin` and 0.29 to 0.41 for `raw_twin` (shared shot noise correlates the score with the error). A value of 0.7 therefore means "far above the floor" only in combination with a noise level much larger than shot noise (table T3 in §7.3).

### 6.7 IBM-calibration twin rehearsals with `v1_final` (job 026/027 campaigns, EMULATED): FAIL
Twins use IBM's **stored** calibration snapshots in `qiskit-ibm-runtime` 0.50.0 (no IBM account): `day0_kingston` (device Kingston, calibration measured 2026-04-15, 12-qubit line score 0.130) and `day1_marrakesh` (Marrakesh, 2025-02-26, score 0.090), noise files `evidence/twin/<name>/noise_model.json`. Gate records: `evidence/J3_twin_rehearsal/`.

| twin | shots | Spearman `jepa_twin` | Spearman `raw_twin` | rows | record |
|---|---|---|---|---|---|
| Kingston | 256 (before `decisions/008`) | 0.305 | 0.651 | FAIL, FAIL | `20261022T163228Z.json` |
| Marrakesh | 256 | 0.222 | 0.607 | FAIL, FAIL | `20261022T165512Z.json` |
| Kingston | **512** | **0.326** | **0.656** | FAIL (0.326 < 0.7), FAIL (non-inferiority: 0.326 < 0.656 - 0.05) | `20261026T181636Z.json` |
| Marrakesh | **512** | **0.253** | **0.498** | FAIL, FAIL | `20261026T181452Z.json` |

AUROC of `jepa_twin` separating arm B from arm A at 4,000 shots: 1.00 on both (PASS, threshold 0.8); `raw_twin`: 0.644 (Kingston), 0.539 (Marrakesh). Spearman at 4,000 shots: Kingston `jepa_twin` 0.420 vs `raw_twin` 0.748; Marrakesh 0.505 vs 0.471. Full per-score tables for 256/512/4,000 shots are in §7.1 (T1). Reading: the model separates the degraded arm perfectly but ranks the individual errors worse than the raw observation-space distance. **This result is dominated by the artifact of §6.9 and must not be quoted as evidence about the method** (`decisions/010`). Calibration "days" in the rehearsal are the 5 twin seeds, not real days (the days row is report-only).

### 6.8 Quantinuum-noise twins (EMULATED; `decisions/009`)
Noise from Nexus device specifications, all-to-all connectivity, circuits compiled to `rzz/rx/ry/rz` with the same 2-qubit counts 34/56/100/188; arm B = all errors x2. Parameter files `evidence/twin/qtm_h2_2/noise_model.json` (H2-2, specs of 2025-08-28: $p_1=2.8\times10^{-5}$, $p_2=8.3\times10^{-4}$, $p_{\text{meas},0}=6.7\times10^{-4}$, $p_{\text{meas},1}=1.2\times10^{-3}$, memory $1.2\times10^{-4}$) and `qtm_helios_1` (Helios-1, specs of 2025-11-05: $p_1=2.5\times10^{-5}$, $p_2=7.9\times10^{-4}$, $p_{\text{meas},0}=8\times10^{-4}$, $p_{\text{meas},1}=1.6\times10^{-4}$, memory $6\times10^{-4}$).
- **`qtm_h2_2` (job 031, finished 2026-10-28 23:07 UTC; outputs on branch `results`, not yet in `main`; gate record `20261028T230734Z.json`): rehearsal FAIL.** Spearman `jepa_twin` 0.193 vs `raw_twin` 0.479 at 512 shots (0.319 vs 0.617 at 256; 0.353 vs 0.606 at 4,000); AUROC `jepa_twin` 1.00 vs `raw_twin` 0.553. Elapsed 0.125 h on the desktop.
- **`qtm_helios_1` (job 032): RUNNING** (started 23:15:05 UTC, attempt 1). No result yet.
- The Quantinuum noise is much lower than IBM's (two-qubit error about 2x lower, readout error roughly 5 to 10x lower than the IBM medians in §7.7), and `jepa_twin` still gives AUROC 1.00 with Spearman below `raw_twin`, which again points at the encoder artifact rather than at the noise regime.

### 6.9 Cross-carrier check on `v1_final` seed 0 (job 030; `evidence/twin/cross_carrier/cross_carrier.json`, commit `ac7e920`)
Setup (docstring of `scripts/cross_carrier_check.py`): 72 exact states (on-family $g_E\in\{1.3,1.75,2.0\}$, $\mu\in\{0.3,0.375,0.5\}$, S3 start, $t=r\,0.375/g_E$ for $r=1\ldots8$), master seed 20261028, shot levels 512 and 4,000. For each state two independent diagonal and two independent chain records (exact sampling, no device noise); latent distances $\|E(o)-E(o')\|$. Medians (full table T4 in §7.4):

| quantity | 512 shots | x `noise_diag` | 4,000 shots | x `noise_diag` |
|---|---|---|---|---|
| `noise_diag` (two diagonal records, same labels: the scale the model knows) | 0.394 | 1 | 0.108 | 1 |
| `noise_chain` (two chain records) | 0.0287 | 0.073 | 0.0114 | 0.105 |
| `label_carrier` (same chain estimate, carrier label chain vs diagonal) | **7.91** | **20.1** | 8.21 | 76.0 |
| `label_source` (same diagonal estimate, source label exact vs twin) | **9.23** | **23.4** | 9.29 | 85.9 |
| `twin_vs_train` (what J3 compares) | 10.66 | 27.1 | 10.69 | 98.9 |
| `err_diag` (noisy vs clean diagonal record) | 0.278 | 0.71 | 0.121 | 1.12 |
| `err_chain` (noisy vs clean chain record) | 8.23 | 20.9 | 8.22 | 76.1 |

Findings: relabelling alone moves the latent 20 to 23 times the 512-shot noise scale; two chain records of the same state differ by only 0.03 (the encoder is saturated and nearly blind to their content). Cause (`decisions/010`): the flag and the source/carrier one-hot columns were constant in training (variance $5.6\times10^{-45}$), so the input normalisation maps any other value $x$ to about $316x$. Hence all `v1_final` twin rehearsals, and a hardware J3 with `v1_final`, are dominated by this artifact; the AUROC of 1.00 is probably an amplified flag rate (PROPOSED explanation; not separately tested). Expectation for `v2_final` (physics-only encoder): label distances exactly 0 (test `test_physics_only_encoder_ignores_flag_and_labels`: latent bit-identical when flag or labels change).

### 6.10 Device parameter tables
IBM (stored snapshots) and Quantinuum (Nexus specs): see §7.7 (T5, T6 and the compact bar-chart table T7).

### 6.11 Overall reading (what the results mean today)
1. The physics and data layer is solid (J0 PASS; two independent codes agree to $10^{-13}$ to $10^{-16}$).
2. The learned model is healthy except for one consistency row; forecasting is good on-family and not good enough at strong coupling, and is matched by a plain supervised network. The paper's forecasting claim can only be "mixed".
3. The label-free error signal (the main remaining scientific question) has **not** been tested fairly yet: with `v1_final` it is contaminated by the label artifact. The first fair test is the `v2_final` twin rehearsals. Even then the null floor (§6.6) means the 0.7 Spearman threshold needs a device error clearly above shot noise.
4. No hardware exists in this project. H3 (on hardware), H4 and H5 are NOT RUN; their twin analogues are EMULATED.

---

## 7. Plot data (the data to re-make every figure, for example on claude.ai)

### 7.0 How to use this section
- Every table is a Markdown pipe table with a header row; paste it into a spreadsheet or give it to a charting tool. Each table names its source file and the script that produced it (Appendix D; run with `python scripts/run.py --no-queue --threads 1 -- python .local_runs/probe/<script>.py`; the standard output lands in the runner log under `.local_runs/logs/`).
- All values are **EMULATED or simulated**; no hardware.
- **Where the J1 curves are.** `reports/012` §9 holds, for the first six ladder rungs plus the masked `v1_base` runs (7 series) and at 23 epochs (1, 2, 5, 10, 20, 30, ..., 200), the tables P1 (effective rank, mean/min/max over seeds), P2 to P5 (grounding $R^2$ of energy, $C_{\text{string}}$, $P_{\text{meson}}$, $P_{\text{baryonic}}$), P6 (semigroup residual), P7 and P7b (loss terms), P8 and P8b (final epoch per seed and per rung), P9 (rank vs semigroup scatter), P10 (energy ceiling bars), P11a to P11g (physics curves: dynamics from S3 at P-A on a fine time grid, $g_E=1$ table, on-family mass scan, strong-coupling resonance scan, Lanczos coefficients, $P_{S3}(t)$, carrier cost table) and P12 (10-epoch laptop check). Those tables and the exact scripts (`plot_tables.py`, `physics_curves.py`, `evidence_tables.py`) are in `reports/012` §9 and Appendix A there. **This report adds** (a) the final epoch per seed and the per-configuration summary for **all 14 configurations plus `v1_final`** (§7.6), (b) the seed-mean curves of rank, semigroup residual and energy $R^2$ at nine epochs for all 15 runs (§7.6), and (c) every new table below. The full per-epoch curves of configurations 7 to 14 are only in the local `runs/<name>/seed*/history.json` (not committed); `v1_final`'s are in `evidence/runs/v1_final/seed*/history.json`. The sidecar data of figures 000 and 001 (J1 diagnostics images) are `evidence/figures/000_*.json` and `001_*.json`.
- **Plot catalogue (new):** P13 Spearman and AUROC bars per twin, score and shot level (T1); P14 flag rate and exact error versus depth $r$, arm A vs B, per twin (T2); P15 noiseless null-check bars (T3); P16 cross-carrier distance bars on a log axis with the `noise_diag` line (T4); P17 J2 MAE grouped bars by model, family, horizon, target (§7.5); P18 J1 rank and semigroup scatter or curves for all 15 runs (§7.6); P19 device-error bars (T7). Suggested drawing: P13 grouped bars, y from 0 to 1, horizontal lines at 0.7 (Spearman threshold) and 0.8 (AUROC threshold); P16 log y axis; P17 log y axis for the autoregressive +8 values (up to 1.14); thresholds as dashed lines.

### 7.1 T1 Spearman(score, exact_error) and AUROC(score separates arm B from arm A), per twin, shot level and score

Rule (as run_j3 rehearsal): points of arm A / seed 0 (self-reference, score exactly 0) are left out, so n = 135 per shot level (150 for the noiseless file in T3, which uses all points). Model in every file: evidence/runs/v1_final/seed0/model.pt

| twin | shots | n | score | Spearman | AUROC (B vs A) |
|---|---|---|---|---|---|
| ideal0 (noiseless) | 256 | 135 | jepa_twin | 0.292 | 0.431 |
| ideal0 (noiseless) | 256 | 135 | raw_twin | 0.408 | 0.454 |
| ideal0 (noiseless) | 256 | 135 | jepa_self | -0.125 | 0.505 |
| ideal0 (noiseless) | 256 | 135 | jepa_t0 | -0.141 | 0.494 |
| ideal0 (noiseless) | 256 | 135 | flag_rate | nan | 0.500 |
| ideal0 (noiseless) | 512 | 135 | jepa_twin | 0.215 | 0.499 |
| ideal0 (noiseless) | 512 | 135 | raw_twin | 0.410 | 0.457 |
| ideal0 (noiseless) | 512 | 135 | jepa_self | 0.005 | 0.504 |
| ideal0 (noiseless) | 512 | 135 | jepa_t0 | -0.000 | 0.496 |
| ideal0 (noiseless) | 512 | 135 | flag_rate | nan | 0.500 |
| ideal0 (noiseless) | 4000 | 135 | jepa_twin | 0.146 | 0.441 |
| ideal0 (noiseless) | 4000 | 135 | raw_twin | 0.285 | 0.451 |
| ideal0 (noiseless) | 4000 | 135 | jepa_self | 0.075 | 0.498 |
| ideal0 (noiseless) | 4000 | 135 | jepa_t0 | 0.088 | 0.496 |
| ideal0 (noiseless) | 4000 | 135 | flag_rate | nan | 0.500 |
| day0_kingston (IBM, 2026-04-15) | 256 | 135 | jepa_twin | 0.305 | 0.950 |
| day0_kingston (IBM, 2026-04-15) | 256 | 135 | raw_twin | 0.651 | 0.580 |
| day0_kingston (IBM, 2026-04-15) | 256 | 135 | jepa_self | 0.490 | 0.505 |
| day0_kingston (IBM, 2026-04-15) | 256 | 135 | jepa_t0 | 0.463 | 0.487 |
| day0_kingston (IBM, 2026-04-15) | 256 | 135 | flag_rate | 0.521 | 0.760 |
| day0_kingston (IBM, 2026-04-15) | 512 | 135 | jepa_twin | 0.326 | 0.997 |
| day0_kingston (IBM, 2026-04-15) | 512 | 135 | raw_twin | 0.656 | 0.550 |
| day0_kingston (IBM, 2026-04-15) | 512 | 135 | jepa_self | 0.525 | 0.497 |
| day0_kingston (IBM, 2026-04-15) | 512 | 135 | jepa_t0 | 0.493 | 0.486 |
| day0_kingston (IBM, 2026-04-15) | 512 | 135 | flag_rate | 0.594 | 0.756 |
| day0_kingston (IBM, 2026-04-15) | 4000 | 135 | jepa_twin | 0.420 | 1.000 |
| day0_kingston (IBM, 2026-04-15) | 4000 | 135 | raw_twin | 0.748 | 0.644 |
| day0_kingston (IBM, 2026-04-15) | 4000 | 135 | jepa_self | 0.615 | 0.483 |
| day0_kingston (IBM, 2026-04-15) | 4000 | 135 | jepa_t0 | 0.605 | 0.488 |
| day0_kingston (IBM, 2026-04-15) | 4000 | 135 | flag_rate | 0.689 | 0.760 |
| day1_marrakesh (IBM, 2025-02-26) | 256 | 135 | jepa_twin | 0.222 | 0.947 |
| day1_marrakesh (IBM, 2025-02-26) | 256 | 135 | raw_twin | 0.607 | 0.521 |
| day1_marrakesh (IBM, 2025-02-26) | 256 | 135 | jepa_self | 0.417 | 0.540 |
| day1_marrakesh (IBM, 2025-02-26) | 256 | 135 | jepa_t0 | 0.428 | 0.511 |
| day1_marrakesh (IBM, 2025-02-26) | 256 | 135 | flag_rate | 0.440 | 0.771 |
| day1_marrakesh (IBM, 2025-02-26) | 512 | 135 | jepa_twin | 0.253 | 0.979 |
| day1_marrakesh (IBM, 2025-02-26) | 512 | 135 | raw_twin | 0.498 | 0.577 |
| day1_marrakesh (IBM, 2025-02-26) | 512 | 135 | jepa_self | 0.450 | 0.510 |
| day1_marrakesh (IBM, 2025-02-26) | 512 | 135 | jepa_t0 | 0.437 | 0.494 |
| day1_marrakesh (IBM, 2025-02-26) | 512 | 135 | flag_rate | 0.503 | 0.750 |
| day1_marrakesh (IBM, 2025-02-26) | 4000 | 135 | jepa_twin | 0.505 | 1.000 |
| day1_marrakesh (IBM, 2025-02-26) | 4000 | 135 | raw_twin | 0.471 | 0.539 |
| day1_marrakesh (IBM, 2025-02-26) | 4000 | 135 | jepa_self | 0.615 | 0.530 |
| day1_marrakesh (IBM, 2025-02-26) | 4000 | 135 | jepa_t0 | 0.564 | 0.488 |
| day1_marrakesh (IBM, 2025-02-26) | 4000 | 135 | flag_rate | 0.659 | 0.760 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | 256 | 135 | jepa_twin | 0.319 | 0.919 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | 256 | 135 | raw_twin | 0.617 | 0.540 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | 256 | 135 | jepa_self | 0.206 | 0.565 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | 256 | 135 | jepa_t0 | 0.191 | 0.521 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | 256 | 135 | flag_rate | 0.260 | 0.784 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | 512 | 135 | jepa_twin | 0.193 | 0.966 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | 512 | 135 | raw_twin | 0.479 | 0.542 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | 512 | 135 | jepa_self | 0.285 | 0.577 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | 512 | 135 | jepa_t0 | 0.275 | 0.522 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | 512 | 135 | flag_rate | 0.285 | 0.793 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | 4000 | 135 | jepa_twin | 0.353 | 1.000 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | 4000 | 135 | raw_twin | 0.606 | 0.553 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | 4000 | 135 | jepa_self | 0.449 | 0.574 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | 4000 | 135 | jepa_t0 | 0.454 | 0.529 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | 4000 | 135 | flag_rate | 0.446 | 0.800 |


Reading T1: Spearman = correlation of the score with the exact error of the twin's observables; AUROC = chance that arm B scores higher than arm A. The 'ideal0' rows are the noiseless control (flag_rate is constant 0, so its Spearman is undefined: nan). Points of arm A / seed 0 are excluded as in the gate (n = 135). Differences of up to 0.002 from the gate ledger come only from rounding.

### 7.2 T2 mean flag rate and mean exact error by arm and depth (4000 shots)

| twin | arm | depth r | mean flag rate | mean exact_error | mean ideal_error |
|---|---|---|---|---|---|
| ideal0 (noiseless) | A | 1 | 0.0000 | 0.0539 | 0.0540 |
| ideal0 (noiseless) | A | 2 | 0.0000 | 0.0504 | 0.0505 |
| ideal0 (noiseless) | A | 4 | 0.0000 | 0.0479 | 0.0478 |
| ideal0 (noiseless) | A | 6 | 0.0000 | 0.0424 | 0.0397 |
| ideal0 (noiseless) | A | 8 | 0.0000 | 0.0549 | 0.0477 |
| ideal0 (noiseless) | B | 1 | 0.0000 | 0.0497 | 0.0497 |
| ideal0 (noiseless) | B | 2 | 0.0000 | 0.0431 | 0.0431 |
| ideal0 (noiseless) | B | 4 | 0.0000 | 0.0463 | 0.0470 |
| ideal0 (noiseless) | B | 6 | 0.0000 | 0.0460 | 0.0446 |
| ideal0 (noiseless) | B | 8 | 0.0000 | 0.0552 | 0.0507 |
| day0_kingston (IBM, 2026-04-15) | A | 1 | 0.2015 | 0.0667 | 0.0668 |
| day0_kingston (IBM, 2026-04-15) | A | 2 | 0.2592 | 0.0645 | 0.0656 |
| day0_kingston (IBM, 2026-04-15) | A | 4 | 0.3623 | 0.0771 | 0.0780 |
| day0_kingston (IBM, 2026-04-15) | A | 6 | 0.4491 | 0.0974 | 0.1017 |
| day0_kingston (IBM, 2026-04-15) | A | 8 | 0.5188 | 0.1367 | 0.1483 |
| day0_kingston (IBM, 2026-04-15) | B | 1 | 0.3104 | 0.0722 | 0.0725 |
| day0_kingston (IBM, 2026-04-15) | B | 2 | 0.3815 | 0.0908 | 0.0914 |
| day0_kingston (IBM, 2026-04-15) | B | 4 | 0.4959 | 0.0982 | 0.1015 |
| day0_kingston (IBM, 2026-04-15) | B | 6 | 0.5855 | 0.1603 | 0.1675 |
| day0_kingston (IBM, 2026-04-15) | B | 8 | 0.6581 | 0.2953 | 0.3084 |
| day1_marrakesh (IBM, 2025-02-26) | A | 1 | 0.1474 | 0.0551 | 0.0552 |
| day1_marrakesh (IBM, 2025-02-26) | A | 2 | 0.1988 | 0.0637 | 0.0650 |
| day1_marrakesh (IBM, 2025-02-26) | A | 4 | 0.2893 | 0.0766 | 0.0771 |
| day1_marrakesh (IBM, 2025-02-26) | A | 6 | 0.3655 | 0.0854 | 0.0913 |
| day1_marrakesh (IBM, 2025-02-26) | A | 8 | 0.4359 | 0.1036 | 0.1122 |
| day1_marrakesh (IBM, 2025-02-26) | B | 1 | 0.2419 | 0.0594 | 0.0597 |
| day1_marrakesh (IBM, 2025-02-26) | B | 2 | 0.3091 | 0.0752 | 0.0759 |
| day1_marrakesh (IBM, 2025-02-26) | B | 4 | 0.4140 | 0.0946 | 0.0965 |
| day1_marrakesh (IBM, 2025-02-26) | B | 6 | 0.5075 | 0.1141 | 0.1183 |
| day1_marrakesh (IBM, 2025-02-26) | B | 8 | 0.5819 | 0.1545 | 0.1649 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | A | 1 | 0.0454 | 0.0480 | 0.0481 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | A | 2 | 0.0670 | 0.0482 | 0.0484 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | A | 4 | 0.1099 | 0.0560 | 0.0564 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | A | 6 | 0.1497 | 0.0618 | 0.0619 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | A | 8 | 0.1917 | 0.0642 | 0.0641 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | B | 1 | 0.0892 | 0.0490 | 0.0490 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | B | 2 | 0.1315 | 0.0603 | 0.0605 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | B | 4 | 0.2139 | 0.0555 | 0.0557 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | B | 6 | 0.2810 | 0.0802 | 0.0854 |
| qtm_h2_2 (Quantinuum H2-2, 2025-08-28) | B | 8 | 0.3398 | 0.0871 | 0.0936 |


### 7.3 T3 noiseless null check by shot level (evidence/twin/ideal0/null_check.json)

| shots | n_A | n_B | null sigma | score | AUROC | Spearman vs exact error |
|---|---|---|---|---|---|---|
| 256 | 60 | 75 | 0.0502 | jepa_twin | 0.431 | 0.292 |
| 256 | 60 | 75 | 0.0502 | raw_twin | 0.454 | 0.408 |
| 256 | 60 | 75 | 0.0502 | jepa_self | 0.505 | -0.125 |
| 256 | 60 | 75 | 0.0502 | jepa_t0 | 0.494 | -0.141 |
| 256 | 60 | 75 | 0.0502 | flag_rate | 0.500 | 0.067 |
| 512 | 60 | 75 | 0.0502 | jepa_twin | 0.499 | 0.215 |
| 512 | 60 | 75 | 0.0502 | raw_twin | 0.457 | 0.410 |
| 512 | 60 | 75 | 0.0502 | jepa_self | 0.504 | 0.005 |
| 512 | 60 | 75 | 0.0502 | jepa_t0 | 0.496 | -0.000 |
| 512 | 60 | 75 | 0.0502 | flag_rate | 0.500 | -0.035 |
| 4000 | 60 | 75 | 0.0502 | jepa_twin | 0.441 | 0.146 |
| 4000 | 60 | 75 | 0.0502 | raw_twin | 0.451 | 0.285 |
| 4000 | 60 | 75 | 0.0502 | jepa_self | 0.498 | 0.074 |
| 4000 | 60 | 75 | 0.0502 | jepa_t0 | 0.496 | 0.088 |
| 4000 | 60 | 75 | 0.0502 | flag_rate | 0.500 | -0.028 |


### 7.4 T4 cross-carrier summary (v1_final seed0; evidence/twin/cross_carrier/cross_carrier.json; median / p90 / median over noise_diag)

n_states 72 master_seed 20261028 gE [1.3, 1.75, 2.0] masses [0.3, 0.375, 0.5] depths [1, 2, 3, 4, 5, 6, 7, 8] dt 0.375 keys ['what', 'model', 'K', 'dt', 'gE', 'masses', 'depths', 'shots', 'master_seed', 'n_states', 'rows', 'seconds', 'commit', 'utc']

| shots | quantity | median | p90 | median / noise_diag median |
|---|---|---|---|---|
| 512 | noise_diag | 0.3936 | 1.043 | 1 |
| 512 | noise_chain | 0.02872 | 0.0429 | 0.073 |
| 512 | cross | 8.186 | 9.812 | 20.8 |
| 512 | label_carrier | 7.906 | 9.855 | 20.1 |
| 512 | label_source | 9.229 | 10.65 | 23.4 |
| 512 | twin_vs_train | 10.66 | 12.62 | 27.1 |
| 512 | err_diag | 0.2778 | 0.6802 | 0.706 |
| 512 | err_chain | 8.229 | 9.91 | 20.9 |
| 512 | obs_noise_diag | 0.07895 | 0.1363 |  |
| 512 | obs_noise_chain | 0.1626 | 0.2513 |  |
| 512 | obs_err_diag | 0.05631 | 0.09841 |  |
| 512 | obs_err_chain | 0.1211 | 0.198 |  |
| 4000 | noise_diag | 0.1081 | 0.2958 | 1 |
| 4000 | noise_chain | 0.01139 | 0.01904 | 0.105 |
| 4000 | cross | 8.227 | 9.903 | 76.1 |
| 4000 | label_carrier | 8.211 | 9.867 | 76 |
| 4000 | label_source | 9.289 | 10.75 | 85.9 |
| 4000 | twin_vs_train | 10.69 | 12.72 | 98.9 |
| 4000 | err_diag | 0.121 | 0.2202 | 1.12 |
| 4000 | err_chain | 8.224 | 9.909 | 76.1 |
| 4000 | obs_noise_diag | 0.02641 | 0.04968 |  |
| 4000 | obs_noise_chain | 0.06566 | 0.111 |  |
| 4000 | obs_err_diag | 0.02083 | 0.03759 |  |
| 4000 | obs_err_chain | 0.04408 | 0.07116 |  |


### 7.5 J2 MAE (evidence/runs/v1_final/forecast_eval.json = input of evidence/J2_forecast/20261021T201507Z.json; mean of 5 seeds; n_test {'onfam': 2935, 'strong': 3134} ; context_step 4 ; master_seed 27182818 )

| family | model | horizon | P_baryonic | P_meson | C_string | mean of 3 |
|---|---|---|---|---|---|---|
| onfam | jepa | +4 | 0.0321 | 0.0140 | 0.0198 | 0.0219 |
| onfam | jepa | +8 | 0.0493 | 0.0202 | 0.0274 | 0.0323 |
| onfam | ridge | +4 | 0.0598 | 0.0190 | 0.0305 | 0.0364 |
| onfam | ridge | +8 | 0.1437 | 0.0301 | 0.1360 | 0.1032 |
| onfam | autoregressive | +4 | 0.0297 | 0.0110 | 0.0143 | 0.0183 |
| onfam | autoregressive | +8 | 0.4036 | 0.1880 | 1.1351 | 0.5756 |
| onfam | supervised_mlp | +4 | 0.0225 | 0.0099 | 0.0119 | 0.0148 |
| onfam | supervised_mlp | +8 | 0.0482 | 0.0197 | 0.0241 | 0.0307 |
| onfam | jepa_masked | +4 | 0.0578 | 0.0151 | 0.0335 | 0.0355 |
| onfam | jepa_masked | +8 | 0.0914 | 0.0215 | 0.0589 | 0.0573 |
| onfam | ridge_masked | +4 | 0.0628 | 0.0195 | 0.0305 | 0.0376 |
| onfam | ridge_masked | +8 | 0.4579 | 0.0478 | 0.2638 | 0.2565 |
| strong | jepa | +4 | 0.1050 | 0.0165 | 0.0479 | 0.0564 |
| strong | jepa | +8 | 0.1229 | 0.0209 | 0.0610 | 0.0683 |
| strong | ridge | +4 | 0.0853 | 0.0139 | 0.0377 | 0.0456 |
| strong | ridge | +8 | 0.1854 | 0.0239 | 0.2482 | 0.1525 |
| strong | autoregressive | +4 | 0.1284 | 0.0146 | 0.0539 | 0.0657 |
| strong | autoregressive | +8 | 0.3675 | 0.0772 | 0.2366 | 0.2271 |
| strong | supervised_mlp | +4 | 0.1086 | 0.0133 | 0.0455 | 0.0558 |
| strong | supervised_mlp | +8 | 0.1529 | 0.0183 | 0.0682 | 0.0798 |
| strong | jepa_masked | +4 | 0.0869 | 0.0127 | 0.0394 | 0.0463 |
| strong | jepa_masked | +8 | 0.1370 | 0.0180 | 0.0657 | 0.0736 |
| strong | ridge_masked | +4 | 0.0906 | 0.0139 | 0.0382 | 0.0476 |
| strong | ridge_masked | +8 | 0.1946 | 0.0238 | 0.2746 | 0.1643 |

train_seeds: [1706464724, 1858437526, 683048278, 1024775132, 3168869543] checksum: 76f4c90555918e7e75f89562de7b6383fda49998818fe6da3a626e48aa828b8a dataset: main



### 7.6 J1 data for all 14 configurations and v1_final

Source: runs/<run>/seed0..4/history.json (local; v1_final also evidence/runs/v1_final/); script j1_tables.py (Appendix D). "#" is the configuration number of section 6.3; "F" = v1_final. nan in ground_r2 flag entry is ignored.

#### P8x final epoch (200), per seed, all configurations (runs/<run>/seed0..4/history.json, unmasked)

| # | run | seed | eff_rank | R2_energy | R2_C_string | R2_P_meson | R2_P_baryonic | semigroup_resid | isotropy | pred_loss |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | v1_base | 0 | 5.6538 | 0.90055 | 0.99841 | 0.98184 | 0.99759 | 0.0018857 | 0.0030296 | 0.0045908 |
| 1 | v1_base | 1 | 6.1539 | 0.89943 | 0.99820 | 0.97786 | 0.99741 | 0.0021573 | 0.013128 | 0.0042442 |
| 1 | v1_base | 2 | 5.1562 | 0.89954 | 0.99843 | 0.98546 | 0.99733 | 0.0032023 | 0.0018968 | 0.0039533 |
| 1 | v1_base | 3 | 5.8895 | 0.90343 | 0.99824 | 0.98143 | 0.99722 | 0.0024169 | 0.0080982 | 0.0042795 |
| 1 | v1_base | 4 | 5.8507 | 0.90150 | 0.99825 | 0.98159 | 0.99707 | 0.0032928 | 0.0063634 | 0.0043925 |
| 2 | v1_wsigreg2 | 0 | 8.2625 | 0.90128 | 0.99771 | 0.97928 | 0.99706 | 0.0039475 | 0.026515 | 0.011113 |
| 2 | v1_wsigreg2 | 1 | 9.1040 | 0.89999 | 0.99787 | 0.97285 | 0.99719 | 0.0051619 | 0.02452 | 0.01114 |
| 2 | v1_wsigreg2 | 2 | 8.9244 | 0.89994 | 0.99763 | 0.97650 | 0.99662 | 0.003647 | 0.047643 | 0.011253 |
| 2 | v1_wsigreg2 | 3 | 8.9336 | 0.90088 | 0.99778 | 0.97519 | 0.99685 | 0.0053439 | 0.068916 | 0.011042 |
| 2 | v1_wsigreg2 | 4 | 9.0766 | 0.90228 | 0.99785 | 0.97205 | 0.99654 | 0.0034857 | 0.029621 | 0.010897 |
| 3 | v1_wsigreg5 | 0 | 10.6635 | 0.90170 | 0.99758 | 0.97456 | 0.99678 | 0.0062859 | 0.17709 | 0.021374 |
| 3 | v1_wsigreg5 | 1 | 10.8359 | 0.90070 | 0.99687 | 0.96767 | 0.99661 | 0.0083137 | 0.13562 | 0.020745 |
| 3 | v1_wsigreg5 | 2 | 10.9431 | 0.89929 | 0.99691 | 0.97443 | 0.99605 | 0.0072521 | 0.25555 | 0.020579 |
| 3 | v1_wsigreg5 | 3 | 10.8282 | 0.90147 | 0.99709 | 0.97123 | 0.99616 | 0.0067471 | 0.31023 | 0.020748 |
| 3 | v1_wsigreg5 | 4 | 10.5254 | 0.90190 | 0.99706 | 0.97109 | 0.99573 | 0.0084698 | 0.094874 | 0.020122 |
| 4 | v1_latent32 | 0 | 6.5275 | 0.90201 | 0.99865 | 0.98514 | 0.99751 | 0.0047161 | 0.00038727 | 0.0045495 |
| 4 | v1_latent32 | 1 | 6.1165 | 0.90166 | 0.99819 | 0.97725 | 0.99718 | 0.0027028 | 0.00082769 | 0.0043562 |
| 4 | v1_latent32 | 2 | 6.5754 | 0.90223 | 0.99831 | 0.98698 | 0.99738 | 0.0015498 | 0.00055248 | 0.0044224 |
| 4 | v1_latent32 | 3 | 6.3543 | 0.90304 | 0.99852 | 0.97963 | 0.99747 | 0.0020761 | 0.00031021 | 0.0044773 |
| 4 | v1_latent32 | 4 | 6.2198 | 0.90219 | 0.99848 | 0.98562 | 0.99707 | 0.0017529 | 0.00084261 | 0.0042445 |
| 5 | v1_ema | 0 | 13.3825 | 0.90175 | 0.99324 | 0.92188 | 0.99536 | 0.016267 | 0.076712 | 0.071916 |
| 5 | v1_ema | 1 | 13.2660 | 0.89656 | 0.99495 | 0.93294 | 0.99347 | 0.015838 | 0.097372 | 0.069123 |
| 5 | v1_ema | 2 | 13.3142 | 0.89818 | 0.99396 | 0.91464 | 0.99458 | 0.021326 | 0.11124 | 0.066807 |
| 5 | v1_ema | 3 | 13.0857 | 0.89985 | 0.99444 | 0.93262 | 0.99477 | 0.022098 | 0.1666 | 0.064924 |
| 5 | v1_ema | 4 | 13.4745 | 0.89849 | 0.99454 | 0.95215 | 0.99437 | 0.016387 | 0.22544 | 0.06749 |
| 6 | v1_wground3 | 0 | 5.7862 | 0.90268 | 0.99859 | 0.98666 | 0.99796 | 0.0069369 | 0.0022643 | 0.0048044 |
| 6 | v1_wground3 | 1 | 6.1419 | 0.90001 | 0.99796 | 0.98338 | 0.99765 | 0.0037939 | 0.0035023 | 0.0050111 |
| 6 | v1_wground3 | 2 | 5.7342 | 0.90064 | 0.99823 | 0.98864 | 0.99754 | 0.0027285 | 0.0022924 | 0.0046309 |
| 6 | v1_wground3 | 3 | 6.1304 | 0.90256 | 0.99844 | 0.98451 | 0.99758 | 0.0029573 | 0.0027246 | 0.0050436 |
| 6 | v1_wground3 | 4 | 5.6294 | 0.90160 | 0.99852 | 0.98616 | 0.99717 | 0.0023 | 0.0032934 | 0.0044146 |
| 7 | v1_curriculum | 0 | 6.8045 | 0.90145 | 0.99844 | 0.98154 | 0.99768 | 0.0028572 | 0.0055824 | 0.0046589 |
| 7 | v1_curriculum | 1 | 6.1758 | 0.89780 | 0.99805 | 0.97911 | 0.99740 | 0.0014645 | 0.0066259 | 0.0043651 |
| 7 | v1_curriculum | 2 | 6.4579 | 0.90066 | 0.99862 | 0.98376 | 0.99743 | 0.001467 | 0.0075264 | 0.0043524 |
| 7 | v1_curriculum | 3 | 6.5827 | 0.90302 | 0.99846 | 0.98119 | 0.99716 | 0.0012 | 0.021261 | 0.0045768 |
| 7 | v1_curriculum | 4 | 7.1281 | 0.90248 | 0.99841 | 0.98001 | 0.99677 | 0.0026553 | 0.010215 | 0.0045129 |
| 8 | v1_wsemigroup1 | 0 | 5.7992 | 0.90212 | 0.99820 | 0.98292 | 0.99771 | 0.00050822 | 0.0017597 | 0.0045265 |
| 8 | v1_wsemigroup1 | 1 | 5.5094 | 0.90003 | 0.99824 | 0.97971 | 0.99768 | 0.0010463 | 0.015526 | 0.0042793 |
| 8 | v1_wsemigroup1 | 2 | 5.5536 | 0.90145 | 0.99855 | 0.98490 | 0.99718 | 0.00066186 | 0.004569 | 0.0041709 |
| 8 | v1_wsemigroup1 | 3 | 4.9382 | 0.90397 | 0.99827 | 0.98257 | 0.99728 | 0.001722 | 0.0027579 | 0.0040456 |
| 8 | v1_wsemigroup1 | 4 | 5.7311 | 0.90112 | 0.99838 | 0.97918 | 0.99705 | 0.00065295 | 0.0059001 | 0.0042471 |
| 9 | v1_wsig2_wsg1 | 0 | 8.5604 | 0.90119 | 0.99763 | 0.97779 | 0.99699 | 0.0021455 | 0.032886 | 0.011071 |
| 9 | v1_wsig2_wsg1 | 1 | 9.6209 | 0.90042 | 0.99751 | 0.98174 | 0.99693 | 0.0014073 | 0.016911 | 0.01161 |
| 9 | v1_wsig2_wsg1 | 2 | 8.6102 | 0.89912 | 0.99806 | 0.97942 | 0.99713 | 0.0013842 | 0.035181 | 0.010902 |
| 9 | v1_wsig2_wsg1 | 3 | 8.8130 | 0.90068 | 0.99778 | 0.97467 | 0.99646 | 0.0055676 | 0.079989 | 0.01138 |
| 9 | v1_wsig2_wsg1 | 4 | 9.4954 | 0.90197 | 0.99818 | 0.97307 | 0.99646 | 0.0019227 | 0.076706 | 0.011556 |
| 10 | v1_wsig2_wsg3 | 0 | 8.3163 | 0.90205 | 0.99788 | 0.97758 | 0.99745 | 0.0011654 | 0.013396 | 0.011112 |
| 10 | v1_wsig2_wsg3 | 1 | 8.9498 | 0.90117 | 0.99796 | 0.98084 | 0.99691 | 0.0011268 | 0.014031 | 0.01137 |
| 10 | v1_wsig2_wsg3 | 2 | 8.3047 | 0.89942 | 0.99837 | 0.98150 | 0.99662 | 0.0005254 | 0.055259 | 0.011085 |
| 10 | v1_wsig2_wsg3 | 3 | 8.0709 | 0.90215 | 0.99785 | 0.97999 | 0.99702 | 0.0010021 | 0.050055 | 0.010892 |
| 10 | v1_wsig2_wsg3 | 4 | 8.3288 | 0.90260 | 0.99811 | 0.97373 | 0.99708 | 0.00053059 | 0.047541 | 0.010673 |
| 11 | v1_wsig2_wsg5 | 0 | 8.5165 | 0.90325 | 0.99789 | 0.98188 | 0.99744 | 0.0010129 | 0.066244 | 0.012072 |
| 11 | v1_wsig2_wsg5 | 1 | 7.8409 | 0.89978 | 0.99779 | 0.97875 | 0.99701 | 0.00068117 | 0.024522 | 0.011094 |
| 11 | v1_wsig2_wsg5 | 2 | 8.2288 | 0.90019 | 0.99817 | 0.97878 | 0.99677 | 0.0006833 | 0.063394 | 0.011198 |
| 11 | v1_wsig2_wsg5 | 3 | 7.9976 | 0.90202 | 0.99797 | 0.97910 | 0.99716 | 0.00048904 | 0.041005 | 0.010981 |
| 11 | v1_wsig2_wsg5 | 4 | 7.8045 | 0.90219 | 0.99804 | 0.97690 | 0.99696 | 0.00097555 | 0.033796 | 0.010614 |
| 12 | v1_wsig2_wsg10 | 0 | 7.5588 | 0.90297 | 0.99784 | 0.98114 | 0.99730 | 0.00042161 | 0.022036 | 0.011441 |
| 12 | v1_wsig2_wsg10 | 1 | 7.4155 | 0.90066 | 0.99793 | 0.97731 | 0.99712 | 0.00031298 | 0.011101 | 0.011017 |
| 12 | v1_wsig2_wsg10 | 2 | 7.7479 | 0.89867 | 0.99807 | 0.98073 | 0.99683 | 0.00092216 | 0.0067473 | 0.011138 |
| 12 | v1_wsig2_wsg10 | 3 | 7.4676 | 0.90107 | 0.99816 | 0.97894 | 0.99691 | 0.00025469 | 0.038435 | 0.011248 |
| 12 | v1_wsig2_wsg10 | 4 | 7.6393 | 0.90177 | 0.99798 | 0.97342 | 0.99646 | 0.00034679 | 0.12957 | 0.010863 |
| 13 | v1_wsig3_wsg10 | 0 | 9.0983 | 0.90312 | 0.99720 | 0.97130 | 0.99680 | 0.00029845 | 0.081109 | 0.014987 |
| 13 | v1_wsig3_wsg10 | 1 | 8.3967 | 0.90120 | 0.99777 | 0.97610 | 0.99671 | 0.00029428 | 0.016798 | 0.014447 |
| 13 | v1_wsig3_wsg10 | 2 | 8.3710 | 0.89861 | 0.99760 | 0.97743 | 0.99639 | 0.00048195 | 0.082286 | 0.014079 |
| 13 | v1_wsig3_wsg10 | 3 | 8.2566 | 0.90045 | 0.99770 | 0.97241 | 0.99639 | 0.0007841 | 0.061055 | 0.014426 |
| 13 | v1_wsig3_wsg10 | 4 | 8.3498 | 0.90189 | 0.99762 | 0.97438 | 0.99666 | 0.00052287 | 0.17183 | 0.014388 |
| 14 | v1_confirm | 0 | 8.4497 | 0.90207 | 0.99739 | 0.98078 | 0.99750 | 0.00073219 | 0.065737 | 0.014357 |
| 14 | v1_confirm | 1 | 8.5250 | 0.90177 | 0.99776 | 0.98096 | 0.99705 | 0.00044059 | 0.059833 | 0.014236 |
| 14 | v1_confirm | 2 | 8.6529 | 0.90017 | 0.99754 | 0.97672 | 0.99721 | 0.00032309 | 0.13907 | 0.01423 |
| 14 | v1_confirm | 3 | 8.4467 | 0.90316 | 0.99787 | 0.96840 | 0.99719 | 0.0014818 | 0.058289 | 0.013944 |
| 14 | v1_confirm | 4 | 8.6822 | 0.90006 | 0.99772 | 0.97742 | 0.99702 | 0.00056428 | 0.087851 | 0.013729 |
| F | v1_final | 0 | 8.6711 | 0.90045 | 0.99792 | 0.97560 | 0.99663 | 0.00039198 | 0.055732 | 0.01422 |
| F | v1_final | 1 | 8.6460 | 0.89847 | 0.99813 | 0.97722 | 0.99631 | 0.00064134 | 0.053893 | 0.014159 |
| F | v1_final | 2 | 8.8959 | 0.90062 | 0.99791 | 0.97678 | 0.99712 | 0.00067902 | 0.031399 | 0.013982 |
| F | v1_final | 3 | 8.5550 | 0.89936 | 0.99694 | 0.98023 | 0.99608 | 0.00042675 | 0.062663 | 0.01406 |
| F | v1_final | 4 | 7.9672 | 0.89973 | 0.99820 | 0.97676 | 0.99535 | 0.0008625 | 0.010702 | 0.013639 |

#### P8y per-configuration summary of the final epoch (what the J1 gate compares: min over seeds, max for semigroup)

| # | run | n seeds | rank min | rank max | R2 energy min | R2 C_string min | R2 P_meson min | R2 P_baryonic min | semigroup max | semigroup min |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | v1_base | 5 | 5.156 | 6.154 | 0.89943 | 0.99820 | 0.97786 | 0.99707 | 0.003293 | 0.001886 |
| 2 | v1_wsigreg2 | 5 | 8.263 | 9.104 | 0.89994 | 0.99763 | 0.97205 | 0.99654 | 0.005344 | 0.003486 |
| 3 | v1_wsigreg5 | 5 | 10.525 | 10.943 | 0.89929 | 0.99687 | 0.96767 | 0.99573 | 0.00847 | 0.006286 |
| 4 | v1_latent32 | 5 | 6.116 | 6.575 | 0.90166 | 0.99819 | 0.97725 | 0.99707 | 0.004716 | 0.00155 |
| 5 | v1_ema | 5 | 13.086 | 13.475 | 0.89656 | 0.99324 | 0.91464 | 0.99347 | 0.0221 | 0.01584 |
| 6 | v1_wground3 | 5 | 5.629 | 6.142 | 0.90001 | 0.99796 | 0.98338 | 0.99717 | 0.006937 | 0.0023 |
| 7 | v1_curriculum | 5 | 6.176 | 7.128 | 0.89780 | 0.99805 | 0.97911 | 0.99677 | 0.002857 | 0.0012 |
| 8 | v1_wsemigroup1 | 5 | 4.938 | 5.799 | 0.90003 | 0.99820 | 0.97918 | 0.99705 | 0.001722 | 0.0005082 |
| 9 | v1_wsig2_wsg1 | 5 | 8.560 | 9.621 | 0.89912 | 0.99751 | 0.97307 | 0.99646 | 0.005568 | 0.001384 |
| 10 | v1_wsig2_wsg3 | 5 | 8.071 | 8.950 | 0.89942 | 0.99785 | 0.97373 | 0.99662 | 0.001165 | 0.0005254 |
| 11 | v1_wsig2_wsg5 | 5 | 7.804 | 8.517 | 0.89978 | 0.99779 | 0.97690 | 0.99677 | 0.001013 | 0.000489 |
| 12 | v1_wsig2_wsg10 | 5 | 7.415 | 7.748 | 0.89867 | 0.99784 | 0.97342 | 0.99646 | 0.0009222 | 0.0002547 |
| 13 | v1_wsig3_wsg10 | 5 | 8.257 | 9.098 | 0.89861 | 0.99720 | 0.97130 | 0.99639 | 0.0007841 | 0.0002943 |
| 14 | v1_confirm | 5 | 8.447 | 8.682 | 0.90006 | 0.99739 | 0.96840 | 0.99702 | 0.001482 | 0.0003231 |
| F | v1_final | 5 | 7.967 | 8.896 | 0.89847 | 0.99694 | 0.97560 | 0.99535 | 0.0008625 | 0.000392 |

#### P-curve: effective rank (seed mean; band min..max in P1 of reports/012 for configs 1-6) at selected epochs (all configurations)

| # | run | ep 1 | ep 2 | ep 5 | ep 10 | ep 20 | ep 50 | ep 100 | ep 150 | ep 200 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | v1_base | 4.002 | 4.151 | 4.051 | 3.997 | 4.036 | 4.959 | 5.413 | 5.732 | 5.741 |
| 2 | v1_wsigreg2 | 4.545 | 4.662 | 5.732 | 6.45 | 7.258 | 8.401 | 8.811 | 8.886 | 8.86 |
| 3 | v1_wsigreg5 | 6.314 | 6.851 | 7.694 | 8.63 | 9.494 | 10.22 | 10.6 | 10.75 | 10.76 |
| 4 | v1_latent32 | 4.965 | 4.867 | 4.484 | 4.341 | 4.166 | 5.358 | 6.197 | 6.388 | 6.359 |
| 5 | v1_ema | 7.161 | 7.818 | 8.959 | 9.782 | 10.87 | 12.43 | 13.16 | 13.34 | 13.3 |
| 6 | v1_wground3 | 4.409 | 4.31 | 4.292 | 4.288 | 4.108 | 5.15 | 5.617 | 5.854 | 5.884 |
| 7 | v1_curriculum | 4.266 | 4.245 | 4.16 | 4.528 | 5.397 | 6.519 | 6.525 | 6.637 | 6.63 |
| 8 | v1_wsemigroup1 | 3.887 | 4.082 | 3.97 | 3.904 | 3.857 | 4.838 | 5.26 | 5.498 | 5.506 |
| 9 | v1_wsig2_wsg1 | 4.486 | 4.558 | 5.572 | 6.292 | 6.919 | 8.161 | 8.899 | 9.036 | 9.02 |
| 10 | v1_wsig2_wsg3 | 4.391 | 4.421 | 5.172 | 5.98 | 6.459 | 7.675 | 8.281 | 8.404 | 8.394 |
| 11 | v1_wsig2_wsg5 | 4.212 | 4.257 | 4.958 | 5.794 | 6.227 | 7.319 | 7.958 | 8.08 | 8.078 |
| 12 | v1_wsig2_wsg10 | 4.019 | 4.033 | 4.322 | 5.176 | 5.806 | 6.702 | 7.485 | 7.582 | 7.566 |
| 13 | v1_wsig3_wsg10 | 4.321 | 4.546 | 5.687 | 6.154 | 6.689 | 7.856 | 8.376 | 8.503 | 8.494 |
| 14 | v1_confirm | 4.426 | 4.508 | 5.541 | 6.203 | 6.783 | 7.833 | 8.516 | 8.57 | 8.551 |
| F | v1_final | 4.648 | 4.762 | 5.509 | 5.98 | 6.548 | 7.93 | 8.457 | 8.531 | 8.547 |

#### P-curve: semigroup residual (seed mean; log axis) at selected epochs (all configurations)

| # | run | ep 1 | ep 2 | ep 5 | ep 10 | ep 20 | ep 50 | ep 100 | ep 150 | ep 200 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | v1_base | 0.001993 | 0.001341 | 0.001023 | 0.0009361 | 0.0006207 | 0.001885 | 0.001989 | 0.002304 | 0.002591 |
| 2 | v1_wsigreg2 | 0.002965 | 0.001684 | 0.001565 | 0.001693 | 0.002299 | 0.004641 | 0.004495 | 0.00403 | 0.004317 |
| 3 | v1_wsigreg5 | 0.004415 | 0.003183 | 0.003133 | 0.003716 | 0.006445 | 0.007117 | 0.007279 | 0.007098 | 0.007414 |
| 4 | v1_latent32 | 0.001711 | 0.001366 | 0.001055 | 0.001022 | 0.0007533 | 0.00192 | 0.002206 | 0.002216 | 0.00256 |
| 5 | v1_ema | 0.03175 | 0.01124 | 0.005739 | 0.01249 | 0.01476 | 0.01516 | 0.01691 | 0.01841 | 0.01838 |
| 6 | v1_wground3 | 0.002465 | 0.001292 | 0.001625 | 0.0009745 | 0.000878 | 0.002729 | 0.003629 | 0.003427 | 0.003743 |
| 7 | v1_curriculum | 0.002535 | 0.001082 | 0.0006785 | 0.0005706 | 0.000726 | 0.0015 | 0.001671 | 0.001921 | 0.001929 |
| 8 | v1_wsemigroup1 | 0.001206 | 0.0008909 | 0.0006126 | 0.0004605 | 0.000208 | 0.0005091 | 0.0008306 | 0.0009077 | 0.0009183 |
| 9 | v1_wsig2_wsg1 | 0.00155 | 0.001081 | 0.0007188 | 0.0009664 | 0.0009984 | 0.002061 | 0.002394 | 0.002455 | 0.002485 |
| 10 | v1_wsig2_wsg3 | 0.0008385 | 0.000614 | 0.0005118 | 0.0005621 | 0.0005181 | 0.0008221 | 0.0009015 | 0.0008371 | 0.0008701 |
| 11 | v1_wsig2_wsg5 | 0.0006244 | 0.0003229 | 0.000273 | 0.0004093 | 0.0003116 | 0.0005364 | 0.0007152 | 0.0007412 | 0.0007684 |
| 12 | v1_wsig2_wsg10 | 0.0005217 | 0.0002119 | 0.0001384 | 0.0001964 | 0.0002367 | 0.0004187 | 0.0004886 | 0.0004266 | 0.0004516 |
| 13 | v1_wsig3_wsg10 | 0.0005461 | 0.0002662 | 0.0003061 | 0.0002898 | 0.0002839 | 0.0005144 | 0.0005537 | 0.0004993 | 0.0004763 |
| 14 | v1_confirm | 0.0005166 | 0.0003072 | 0.0002909 | 0.0003202 | 0.0003867 | 0.0005361 | 0.0007212 | 0.0006667 | 0.0007084 |
| F | v1_final | 0.0005415 | 0.00032 | 0.0002977 | 0.0002555 | 0.0002687 | 0.0005935 | 0.0006579 | 0.0005779 | 0.0006003 |

#### P-curve: grounding R2 of energy (seed mean) at selected epochs

| # | run | ep 1 | ep 2 | ep 5 | ep 10 | ep 20 | ep 50 | ep 100 | ep 150 | ep 200 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | v1_base | 0.8774 | 0.8763 | 0.8858 | 0.8873 | 0.8943 | 0.8911 | 0.8980 | 0.8979 | 0.9009 |
| 2 | v1_wsigreg2 | 0.8806 | 0.8751 | 0.8791 | 0.8906 | 0.8897 | 0.8898 | 0.8959 | 0.8998 | 0.9009 |
| 3 | v1_wsigreg5 | 0.8770 | 0.8767 | 0.8800 | 0.8854 | 0.8877 | 0.8880 | 0.8951 | 0.8991 | 0.9010 |
| 4 | v1_latent32 | 0.8729 | 0.8711 | 0.8836 | 0.8852 | 0.8925 | 0.8912 | 0.8990 | 0.9022 | 0.9022 |
| 5 | v1_ema | 0.8809 | 0.8725 | 0.8769 | 0.8844 | 0.8918 | 0.8902 | 0.8964 | 0.8985 | 0.8990 |
| 6 | v1_wground3 | 0.8703 | 0.8853 | 0.8915 | 0.8853 | 0.8939 | 0.8916 | 0.8987 | 0.9009 | 0.9015 |
| 7 | v1_curriculum | 0.8810 | 0.8772 | 0.8876 | 0.8880 | 0.8921 | 0.8920 | 0.8985 | 0.9004 | 0.9011 |
| 8 | v1_wsemigroup1 | 0.8769 | 0.8759 | 0.8860 | 0.8877 | 0.8942 | 0.8908 | 0.8981 | 0.8968 | 0.9017 |
| 9 | v1_wsig2_wsg1 | 0.8808 | 0.8758 | 0.8795 | 0.8907 | 0.8909 | 0.8892 | 0.8966 | 0.9000 | 0.9007 |
| 10 | v1_wsig2_wsg3 | 0.8812 | 0.8752 | 0.8774 | 0.8900 | 0.8918 | 0.8911 | 0.8965 | 0.9003 | 0.9015 |
| 11 | v1_wsig2_wsg5 | 0.8807 | 0.8746 | 0.8772 | 0.8900 | 0.8922 | 0.8898 | 0.8971 | 0.9003 | 0.9015 |
| 12 | v1_wsig2_wsg10 | 0.8818 | 0.8733 | 0.8805 | 0.8902 | 0.8913 | 0.8900 | 0.8970 | 0.8999 | 0.9010 |
| 13 | v1_wsig3_wsg10 | 0.8806 | 0.8768 | 0.8782 | 0.8893 | 0.8889 | 0.8875 | 0.8951 | 0.8995 | 0.9011 |
| 14 | v1_confirm | 0.8743 | 0.8717 | 0.8669 | 0.8791 | 0.8836 | 0.8926 | 0.8946 | 0.9000 | 0.9014 |
| F | v1_final | 0.8666 | 0.8813 | 0.8847 | 0.8737 | 0.8870 | 0.8941 | 0.8972 | 0.8990 | 0.8997 |

#### P-curve: training loss terms (unweighted, seed mean) at epoch 200, all configurations

| # | run | pred | sigreg | ground | semigroup | total (weighted) |
|---|---|---|---|---|---|---|
| 1 | v1_base | 0.004292 | 0.032281 | 0.040567 | 0.0006352 | 0.061063 |
| 2 | v1_wsigreg2 | 0.011089 | 0.01963 | 0.040595 | 0.0016877 | 0.091113 |
| 3 | v1_wsigreg5 | 0.020714 | 0.015004 | 0.040891 | 0.0031062 | 0.13693 |
| 4 | v1_latent32 | 0.00441 | 0.032837 | 0.040545 | 0.00065444 | 0.061439 |
| 5 | v1_ema | 0.068052 | 0.016078 | 0.04149 | 0.010561 | 0.11864 |
| 6 | v1_wground3 | 0.0047809 | 0.033251 | 0.040451 | 0.00068714 | 0.14283 |
| 7 | v1_curriculum | 0.0044932 | 0.029752 | 0.040637 | 0.00057467 | 0.060064 |
| 8 | v1_wsemigroup1 | 0.0042539 | 0.032975 | 0.040532 | 0.00011643 | 0.06139 |
| 9 | v1_wsig2_wsg1 | 0.011304 | 0.019562 | 0.040651 | 0.00036086 | 0.09144 |
| 10 | v1_wsig2_wsg3 | 0.011026 | 0.020483 | 0.040624 | 0.00013692 | 0.093027 |
| 11 | v1_wsig2_wsg5 | 0.011192 | 0.020635 | 0.040618 | 8.8955e-05 | 0.093525 |
| 12 | v1_wsig2_wsg10 | 0.011141 | 0.02125 | 0.040602 | 4.6397e-05 | 0.094708 |
| 13 | v1_wsig3_wsg10 | 0.014466 | 0.01863 | 0.04083 | 6.2607e-05 | 0.11181 |
| 14 | v1_confirm | 0.014099 | 0.018688 | 0.040683 | 5.7466e-05 | 0.11142 |
| F | v1_final | 0.014012 | 0.01882 | 0.040644 | 5.8429e-05 | 0.1117 |

#### args.json of v1_final and v1_confirm

v1_final {"data": "data/main", "name": "v1_final", "epochs": 200, "seeds": 5, "latent": 16, "w_sigreg": 3.0, "w_ground": 1.0, "w_semigroup": 10.0, "ema_target": null, "curriculum_epochs": 0, "master_seed": 27182818, "context_steps": 4, "eval_steps": [4, 8], "device": "cuda", "threads": 18, "baseline_epochs": 100, "masked": true, "train_seeds": [1706464724, 1858437526, 683048278, 1024775132, 3168869543]}
v1_confirm {"data": "data/main", "name": "v1_confirm", "epochs": 200, "seeds": 5, "latent": 16, "w_sigreg": 3.0, "w_ground": 1.0, "w_semigroup": 10.0, "ema_target": null, "curriculum_epochs": 0, "master_seed": 31415926, "context_steps": 4, "eval_steps": [4, 8], "device": "cuda", "threads": null, "baseline_epochs": 100, "masked": true, "train_seeds": [788512632, 3846163361, 669117117, 1958259924, 352388378]}

### 7.7 T5 Quantinuum device parameters (evidence/hardware/quantinuum_devices_20261028T220635Z.json)

H2-2E emulator {"1q_fault_probability": {"p1": 7.3e-05}, "2q_fault_probability": {"p2": 0.00129}, "bit_flip_measurement_probability": {"p_meas_0": 0.0009, "p_meas_1": 0.0018}, "coherent_to_incoherent_factor": 2.0, "crosstalk_probability": {"p_crosstalk_init": 9.6e-06, "p_crosstalk_meas": 8.8e-06}, "dephasing_rates": {"linear_dephasing_rate": 0.0028, "quadratic_dephasing_rate": 0.043}, "fit_parameters": {"przz_a": 1.518, "przz_b": 0.241, "przz_c": 1.518, "przz_d": 0.241, "przz_power": 1.0}, "init_fault_probability": {"p_init": 4e-05}, "ratio_spontaneous_emission": {"p1_emission_ratio": 0.32, "p2_emission_ratio": 0.59}}
H2-1E emulator {"1q_fault_probability": {"p1": 1.89e-05}, "2q_fault_probability": {"p2": 0.00105}, "bit_flip_measurement_probability": {"p_meas_0": 0.0006, "p_meas_1": 0.00139}, "coherent_to_incoherent_factor": 2.0, "crosstalk_probability": {"p_crosstalk_init": 3.3e-06, "p_crosstalk_meas": 3.3e-06}, "dephasing_rates": {"linear_dephasing_rate": 0.0028, "quadratic_dephasing_rate": 0.043}, "fit_parameters": {"przz_a": 1.518, "przz_b": 0.241, "przz_c": 1.518, "przz_d": 0.241, "przz_power": 1.0}, "init_fault_probability": {"p_init": 4e-05}, "ratio_spontaneous_emission": {"p1_emission_ratio": 0.54, "p2_emission_ratio": 0.255}}
H2-1 hardware {"1q_gate_error": {"p1": 1.89e-05, "p1_unc": 4.23e-06}, "2q_gate_error": {"p2": 0.00105, "p2_unc": 8.08e-05}, "crosstalk_error": {"p_crosstalk_meas": 6.65e-06, "p_crosstalk_meas_unc": 8.98e-07}, "date": "2025-04-30", "memory_error": {"memory_error": 0.000203, "memory_error_unc": 2.34e-05}, "spam_error": {"p_meas_0": 0.0006, "p_meas_0_unc": 8.16e-05, "p_meas_1": 0.00139, "p_meas_1_unc": 0.000124}}
H2-2 hardware {"1q_gate_error": {"p1": 2.8e-05, "p1_unc": 3.6e-06}, "2q_gate_error": {"p2": 0.00083, "p2_unc": 4.8e-05}, "crosstalk_error": {"p_crosstalk_meas": 2.2e-05, "p_crosstalk_meas_unc": 5.3e-07}, "date": "2025-08-28", "memory_error": {"memory_error": 0.00012, "memory_error_unc": 2e-05}, "spam_error": {"p_meas_0": 0.00067, "p_meas_0_unc": 8.7e-05, "p_meas_1": 0.0012, "p_meas_1_unc": 0.00011}}
Helios-1 hardware {"date": "2025-11-05", "spam_error": {"p_meas_1_unc": 5e-05, "p_meas_0": 0.0008, "p_meas_1": 0.00016, "p_meas_0_unc": 0.0001}, "crosstalk_error": {"p_crosstalk_meas_unc": 1e-06, "p_crosstalk_meas": 4.8e-05}, "memory_error": {"memory_error_unc": 3e-05, "memory_error": 0.0006}, "1q_gate_error": {"p1": 2.5e-05, "p1_unc": 1e-06}, "2q_gate_error": {"p2_unc": 2e-05, "p2": 0.00079}}
H1-Emulator local_emulator {"date": "2024-06-04", "1q_fault_probability": {"p1": 2.1e-05}, "2q_fault_probability": {"p2": 0.00088}, "bit_flip_measurement_probability": {"p_meas_0": 0.001, "p_meas_1": 0.004}, "init_fault_probability": {"p_init": 3.62e-05}, "crosstalk_probability": {"p_crosstalk_meas": 1.45e-05, "p_crosstalk_init": 5.02e-06}, "ratio_spontaneous_emission": {"p1_emission_ratio": 0.54, "p2_emission_ratio": 0.43}, "dephasing_rates": {"linear_dephasing_rate": 0.0, "quadratic_dephasing_rate": 0.122}, "fit_parameters": {"przz_a": 1.651, "przz_b": 0.175, "przz_c": 1.651, "przz_d": 0.175, "przz_power": 1.0}, "coherent_to_incoherent_factor": 2.5}
H2-Emulator local_emulator {"date": "2024-06-04", "1q_fault_probability": {"p1": 2.9e-05}, "2q_fault_probability": {"p2": 0.00128}, "bit_flip_measurement_probability": {"p_meas_0": 0.0005, "p_meas_1": 0.0025}, "init_fault_probability": {"p_init": 4e-05}, "crosstalk_probability": {"p_crosstalk_meas": 7.4e-06, "p_crosstalk_init": 9.6e-06}, "ratio_spontaneous_emission": {"p1_emission_ratio": 0.32, "p2_emission_ratio": 0.48}, "dephasing_rates": {"linear_dephasing_rate": 0.0028, "quadratic_dephasing_rate": 0.043}, "fit_parameters": {"przz_a": 1.518, "przz_b": 0.241, "przz_c": 1.518, "przz_d": 0.241, "przz_power": 1.0}, "coherent_to_incoherent_factor": 2.0}

(Twin parameter files:)
qtm_h2_2 H2-2 2025-08-28 {"p1": 2.8e-05, "p2": 0.00083, "p_meas_0": 0.00067, "p_meas_1": 0.0012, "memory_error": 0.00012} {"1q_gate_error": {"p1": 2.8e-05, "p1_unc": 3.6e-06}, "2q_gate_error": {"p2": 0.00083, "p2_unc": 4.8e-05}, "crosstalk_error": {"p_crosstalk_meas": 2.2e-05, "p_crosstalk_meas_unc": 5.3e-07}, "date": "2025-08-28", "memory_error": {"memory_error": 0.00012, "memory_error_unc": 2e-05}, "spam_error": {"p_meas_0": 0.00067, "p_meas_0_unc": 8.7e-05, "p_meas_1": 0.0012, "p_meas_1_unc": 0.00011}}
qtm_helios_1 Helios-1 2025-11-05 {"p1": 2.5e-05, "p2": 0.00079, "p_meas_0": 0.0008, "p_meas_1": 0.00016, "memory_error": 0.0006} {"date": "2025-11-05", "spam_error": {"p_meas_1_unc": 5e-05, "p_meas_0": 0.0008, "p_meas_1": 0.00016, "p_meas_0_unc": 0.0001}, "crosstalk_error": {"p_crosstalk_meas_unc": 1e-06, "p_crosstalk_meas": 4.8e-05}, "memory_error": {"memory_error_unc": 3e-05, "memory_error": 0.0006}, "1q_gate_error": {"p1": 2.5e-05, "p1_unc": 1e-06}, "2q_gate_error": {"p2_unc": 2e-05, "p2": 0.00079}}

#### T6 IBM twin line parameters (evidence/twin/*/noise_model.json; evidence/hardware/backends_fake_*.json)

| twin | backend | calibration measured | line score | median line CZ error | max line CZ error | median line readout error |
|---|---|---|---|---|---|---|
| day0_kingston | fake_kingston | 2026-04-15 09:15:15+02:00 | 0.130 | 0.00168 | 0.00362 | 0.00763 |
| day1_marrakesh | fake_marrakesh | 2025-02-26 14:52:45-05:00 | 0.090 | 0.00169 | 0.00364 | 0.00525 |

| fake backend | qubits | median 2q error | median readout error | best 12-qubit line score |
|---|---|---|---|---|
| fake_marrakesh | 156 | 0.00329 | 0.00952 | 0.090 |
| fake_fez | 156 | 0.00390 | 0.00757 | 0.117 |
| fake_kingston | 156 | 0.00183 | 0.00952 | 0.130 |
| fake_torino | 133 | 0.00419 | 0.02295 | 0.266 |

#### T7 compact device-parameter table (bar-chart data)

| device | spec date | 1q error p1 | 2q error p2 | readout p_meas_0 | readout p_meas_1 | memory error | source |
|---|---|---|---|---|---|---|---|
| Quantinuum H2-1 | 2025-04-30 | 1.89e-05 | 0.00105 | 0.0006 | 0.00139 | 0.000203 | quantinuum_devices_20261028T220635Z.json |
| Quantinuum H2-2 | 2025-08-28 | 2.8e-05 | 0.00083 | 0.00067 | 0.0012 | 0.00012 | quantinuum_devices_20261028T220635Z.json |
| Quantinuum Helios-1 | 2025-11-05 | 2.5e-05 | 0.00079 | 0.0008 | 0.00016 | 0.0006 | quantinuum_devices_20261028T220635Z.json |
| IBM fake_kingston (twin day0_kingston) | 2026-04-15 | not recorded | line median CZ 0.00168 (max 0.00362) | line median readout 0.00763 (both outcomes) | | not recorded (T1, T2 per qubit are in the file) | evidence/twin/day0_kingston/noise_model.json |
| IBM fake_marrakesh (twin day1_marrakesh) | 2025-02-26 | not recorded | line median CZ 0.00169 (max 0.00364) | line median readout 0.00525 (both outcomes) | | not recorded (T1, T2 per qubit are in the file) | evidence/twin/day1_marrakesh/noise_model.json |

---

## 8. Current in-flight state (28 Oct 2026, 23:22 UTC; `python scripts/jobs/status.py`, `git show origin/results:...`)

| item | state | what it does | what to do when it finishes |
|---|---|---|---|
| `jobs/031` `qtm_h2_2` | finished 23:07 UTC (status FAILED because the rehearsal gate exits 1; science complete); outputs only on branch `results` (`031/outputs/evidence/twin/qtm_h2_2/residual_eval.json`, `.../J3_twin_rehearsal/20261028T230734Z.json`, ledger) | Quantinuum H2-2 twin campaign (150 circuits), residual evaluation with `v1_final`, J3 rehearsal | `python scripts/jobs/fetch.py 031`, merge the ledger block, commit (section 9, step 1) |
| `jobs/032` `qtm_helios_1` | **RUNNING** on the desktop since 23:15:05 UTC, attempt 1, at code commit `2e56cea` | same for Helios-1; expected about 8 min (031 took 0.125 h) | fetch, merge ledger, commit; report whatever is there (a rehearsal FAIL is the expected outcome with `v1_final`) |
| `jobs/033` `v2_final` | **QUEUED** (job file at `db8ab2c`, code commit `35bcf61`); the desktop worker takes it after 032 on its next 15-minute tick | rebuilds `data/main` from seed 20261005, then `python scripts/train_jepa.py --data data/main --name v2_final --epochs 200 --seeds 5 --masked --w-sigreg 3 --w-semigroup 10 --master-seed 16180339 --physics-only`; outputs `runs/v2_final`, `data/main/manifest.json`, `data/main/fingerprint.json`; time limit 08:28:00; expected about 1.2 h (as `v1_final`) | step 2 below |
| desktop | heartbeat 2026-10-28 23:07:35 UTC; may be switched off; interrupted jobs rerun automatically (up to 3 runs) | | if no heartbeat for hours and jobs wait, tell Digonto; do not touch the desktop |
| Perlmutter | worker silent since 2026-10-08 | | ignore |
| local repository | branch `main` at `db8ab2c`, in sync with GitHub before this session; **this report (`reports/016`) and the regenerated `reports/INDEX.md` are uncommitted** | | commit them as `docs: hand-over report (reports/016)` when Digonto asks |
| CI | last three runs on `main` success | | `gh run list --limit 3` |
| not in `main` yet | `evidence/twin/qtm_h2_2/residual_eval.json`, rehearsal record `20261028T230734Z.json`, their ledger block, `evidence/jobs/031`, `032`, `033` | | fetch as above (also `evidence/jobs/024` and `025`, the two jobs that failed on the Kraus bug, were never fetched; nothing needed from them) |

Open decisions that only Digonto can take: (1) **hardware access** (a new free IBM account, or the simulation-and-twin paper; they said "decide later"; the planned pilot week 26 Oct – 1 Nov has already passed); (2) the pilot QPU cap 90 s vs 120 s (moot without IBM); (3) permission to push anything not already part of the workflow.

---

## 9. How to continue (step by step, exact commands)

All commands run from `/home/digimonk/Projects/su2qc-jepa`. Computation goes through `python scripts/run.py --no-queue --threads 1 -- ...` (light) or `python scripts/run.py --push --where desktop -- ...` (heavy). Exit 2 = laptop busy (wait 60 s, retry); exit 1 = read the log tail in `.local_runs/logs/`.

**Step 0 — orient.** Read this report; `python scripts/env_check.py`; `bash scripts/graph_update.sh --check`; `git status`; `python scripts/jobs/status.py`; `git fetch`; `python scripts/run.py -- python -m pytest -q` (before touching physics; expected: all pass, one CUDA-only case skipped on the laptop); `ruff check src tests scripts`.

**Step 1 — fetch the Quantinuum twins (031, then 032 when COMPLETED/FAILED-with-outputs).**
```
python scripts/jobs/fetch.py 031
python scripts/jobs/fetch.py 032
```
Check that the new files exist: `evidence/twin/qtm_h2_2/residual_eval.json`, `evidence/twin/qtm_helios_1/residual_eval.json`, `evidence/J3_twin_rehearsal/<new stamp>.json`. `GATE_LEDGER.md` differs locally, so the job's copy lands in `evidence/jobs/NNN/outputs/evidence/GATE_LEDGER.md`: check that it equals the local ledger plus exactly the new rehearsal block (diff them), then append that block to `evidence/GATE_LEDGER.md` (the method used for jobs 021 and 022, `reports/015`). Commit with `twin: Quantinuum H2-2 / Helios-1 twin rehearsals with v1_final (jobs/031, 032), EMULATED`. Update this report's section 6.8 numbers only through a new report, never by editing this one.

**Step 2 — `v2_final` (job 033).** When `status.py` shows COMPLETED:
```
python scripts/jobs/fetch.py 033
python scripts/run.py --no-queue --threads 1 -- python scripts/compare_fingerprints.py evidence/J0_data/fingerprint_main_laptop_reference.json evidence/jobs/033/outputs/data/main/fingerprint.json --out evidence/J0_data/fingerprint_compare_main_laptop_vs_desktop_v2_final.json
```
(must print EQUIVALENT; same pattern as job 020). Copy, like commits `75e834d` and `6479fb1` did for `v1_final`, `runs/v2_final/args.json`, `forecast_eval.json`, `seed0..4/history.json` and `seed0/model.pt` (370 KB) into `evidence/runs/v2_final/` (queue workers can only read what is in git), and commit as `data: v2_final ... (jobs/033, desktop)`.

**Step 3 — information-only numbers for `v2_final` (decisions/010 §4).** J1: `python scripts/run.py --no-queue --threads 1 -- python scripts/run_gate.py J1 --runs evidence/runs/v2_final/seed0 evidence/runs/v2_final/seed1 evidence/runs/v2_final/seed2 evidence/runs/v2_final/seed3 evidence/runs/v2_final/seed4` (appends a J1 block; label it "v2_final, information only"). Forecasting: tabulate `evidence/runs/v2_final/forecast_eval.json` with a copy of `.local_runs/probe/j2_dev_tables.py` pointed at that file; **prefer not to run `run_gate.py J2` on it**, because a second J2 row in the ledger could be mistaken for a repeated gate (if it is run, say "information only, decisions/010" in the commit and report). Compare with the `v1_final` tables in §7.5 and §7.6.

**Step 4 — cross-carrier check with `v2_final`.** Expect `label_carrier` and `label_source` medians exactly 0 (the physics-only encoder ignores labels and flag). The script reads the encoder size from the checkpoint (`ck["jcfg"]`). Queue on the desktop (model file must be in git first):
```
python scripts/run.py --push --where desktop -- python scripts/cross_carrier_check.py --model evidence/runs/v2_final/seed0/model.pt --out evidence/twin/cross_carrier/cross_carrier_v2.json
```
(a new output name so the `v1_final` file is not overwritten). If the label distances are not exactly 0, stop: the physics-only path is broken (`tests/test_pipeline.py::test_physics_only_encoder_ignores_flag_and_labels` should have caught it).

**Step 5 — redo the twin rehearsals with `v2_final`** (the stored `records.json` files are not in git, so `run_twin.py` must run again; it is deterministic given its seeds). One desktop job per twin, copying the steps of jobs 023, 026 and 031 with `--model evidence/runs/v2_final/seed0/model.pt` and a new output name so the `v1_final` evidence stays:
```
python scripts/run_twin.py --name day0_kingston --K 12 --seeds 5 --noise-model evidence/twin/day0_kingston/noise_model.json
python scripts/residual_eval.py --model evidence/runs/v2_final/seed0/model.pt --records evidence/twin/day0_kingston/records.json --out evidence/twin/day0_kingston/residual_eval_v2.json --shots-levels 0 512 256
python scripts/run_gate.py J3 --eval evidence/twin/day0_kingston/residual_eval_v2.json --rehearsal
```
Do the same for `day1_marrakesh`, `qtm_h2_2`, `qtm_helios_1`, and for `ideal0` (`run_twin.py --name ideal0 --K 12 --seeds 5 --noise ideal`, then `residual_eval.py`, then `twin_null_check.py --records evidence/twin/ideal0/records.json --residual evidence/twin/ideal0/residual_eval_v2.json --out evidence/twin/ideal0/null_check_v2.json`). Queue with `python scripts/jobs/enqueue.py twin "<title>" --where desktop --prompt prompts/003 --time 06:00:00 --step "python scripts/run_twin.py ..." --step "python scripts/residual_eval.py ..." --step "python scripts/run_gate.py J3 ..." --output evidence/twin/<name>/residual_eval_v2.json --output evidence/J3_twin_rehearsal --output evidence/GATE_LEDGER.md --push` (commit and push the code and the model file first), following the layout of `jobs/031` (title, `outputs:` list, `resources` time 06:00:00). The ledger has no model column, but each J3 row cites its `residual_eval*.json`; put "v2_final" in the job title, commit message and report. Questions to answer: do `jepa_twin` Spearman and AUROC change once the label artifact is gone; is `jepa_twin` still a perfect separator of arm B (AUROC 1.00) with a non-flag-driven latent; how does Spearman compare with the null floor (§6.6) and with `raw_twin`. **Report the outcome whichever way it goes**; the thresholds are frozen.

**Step 6 — finish M3 (`prompts/003`).** (a) `scripts/resonance_eval.py` (does not exist yet): for each held-out $\mu$ forecast the breaking fraction at $t=20,30,50/g_E$ from the context at $t=8/g_E$ for the strong family; fit a Lorentzian or parabola over $\mu$ to the forecast and to the exact curve; report both maxima and their difference (the hardware version of H5 is defined in `docs/PREREGISTRATION.md` §3: parabola vertex of the breaking fraction over $\mu\in\{0.3,0.375,0.42,0.5\}$ at $t=20/g_E$, success if within 0.05 of 0.375). (b) Figures F1 (held-out $g_E$ forecasts vs exact, all baselines) and F2 (resonance curve, forecast vs exact) saved with `python scripts/new_artifact.py figures "<caption>" --ext .png`, data sidecar in `evidence/figures/`, and the plan's F3 baseline-comparison figure. (c) The plan's W4 ablation table (no SIGReg / no grounding / no semigroup / EMA) is only partly covered by the J1 ladder; decide whether it is still needed. (d) Dry runs of the hardware pipeline (`scripts/hw_dry_run.py`, `scripts/hw_list_backends.py`) work against fake backends (`evidence/hardware/backends_fake_*.json`). (e) Close M3 with a session report and update `STATE.json` (it still says M3 report `reports/015`, `hardware`, and does not list the new decisions).

**Step 7 — the hardware decision (Digonto).**
- Option A, **new free IBM account** (Open Plan: 600 QPU-seconds per 28 days as `CLAUDE.md` states; the plan quotes 10 minutes): then `QiskitRuntimeService.save_account` on the laptop only, `scripts/hw_list_backends.py` for real backends, `scripts/hw_dry_run.py --backend <name> --K 12 --depths 1 8 --masses 0.375 --settings Z X --out evidence/hardware/pilot` (12 circuits, 4,000 shots, one job), Digonto edits `configs/hardware_budget.yaml`, then `scripts/hw_submit.py submit --confirm`. Real calibration days would replace the twin seeds in H3 (3 days required).
- Option B, **simulation-and-twin paper**: write a decision record (`python scripts/new_artifact.py decisions "..." --milestone M5`) that H3 to H5 are tested on twins only (IBM-snapshot and Quantinuum-spec noise), labelled EMULATED throughout, that "calibration days" are replaced by distinct device snapshots, and what the paper may then claim (only: a validated method on a simulated twin). This changes the preregistered J3 meaning, so it needs Digonto's explicit approval and a preregistration deviation entry. Never describe twin numbers as hardware.
- Quantinuum hardware or emulators: forbidden unless a session prompt contains "paid provider approved by Digonto" and a budget procedure exists.

**Step 8 — M4 to M8 per the plan, with adjustments** (`plans/001` §10, `prompts/004`–`008`): M4a J2 is already done (FAIL); M4b pilot depends on step 7. M5 hardware days 1 and 2 (or the twin analogue). M6: day 3, J3 over all days, `scripts/depth_extrapolation.py` (H4; to be written to the exact definition in the preregistration §3) and the hardware `resonance_eval.py --source hardware` (H5), the error budget table (truncation, Krylov $1.05\times10^{-4}$, Trotter, shot noise, device, twin mismatch, model forecast). M7 one stretch item chosen by Digonto on 15 Nov (2x3 ladder, quantum encoder J4, or IonQ only with credits; already late). M8 paper under `paper/`, release with checksums, clean-environment replication with `scripts/replicate.sh`, preprint target 27 Nov (hep-lat, cross-list quant-ph, cs.LG). Because J1 and J2 failed, the paper's primary outcome is J3 (or its twin analogue) plus the benchmark and the carrier; the plan's own risk list allows reporting parity.

**Risks and open questions.** (1) No hardware access: schedule slip of about one week already. (2) The label-free signal may still fail with `v2_final`; the null floor of Spearman 0.15 to 0.4 means the 0.7 threshold is demanding for small device errors (the Quantinuum twins have errors only a few times shot noise). (3) The J1 semigroup row and the strong-coupling forecast remain open scientific problems; the supervised MLP matches JEPA. (4) `docs/MODEL_CARD.md` still describes the v1 era; update it after `v2_final`. (5) `STATE.json` is out of date (section 10). (6) The desktop is a single point of failure for heavy work (and is sometimes off); Perlmutter would need Digonto to restart its worker. (7) Preregistration disclosure obligations (section 2.4) must appear in the paper.

---

## 10. Problems log and open problems

**Errors found and fixed (with the lesson)**
| when | problem | fix | lesson |
|---|---|---|---|
| 2 Oct | a `data/` ignore pattern also hid `src/su2qc_jepa/data/`; a cgroup memory limit not enforced; a job could outlive its runner | fixed in the runner (`reports/002`–`004`) | test the guards, not just the happy path |
| 5 Oct | baselines built networks on the CPU while data were on CUDA; jobs 002–008 crashed after training (models and histories saved) | `3fd0a65`, test with CPU and CUDA cases, verified by `jobs/009` | a laptop without GPU cannot reveal device bugs: smoke-test on the worker |
| 5 Oct | adjacent integer training seeds (shuffle seed $s+e$) | spawned `SeedSequence` seeds (`0a76800`) | forbidden by `CLAUDE.md` §5 |
| 5–6 Oct | a retry loop re-ran a gate 10 times because a gate FAIL exit code looked like "laptop busy"; the runner turned a gate run into an unwanted job file `jobs/013` | duplicates removed before commit; file deleted | gate exit 1 means FAIL, not error |
| 5 Oct | J1 energy threshold unreachable | `decisions/005` | measure the ceiling before setting a threshold |
| 5–15 Oct | CI lint failed 10 days unnoticed (ruff I001) | `c9ddfe6` | run `ruff` and check `gh run list` before ending a session |
| 15 Oct | rule "$\le10^{-12}$ per trajectory sum" contradicted the measured $5.7\times10^{-12}$ | `decisions/007` | check a rule against its own example |
| 21 Oct | qiskit-aer 0.18.0 clashes with torch (static TLS error); the graph-freshness test used an older `graphify` from PATH | pins; test uses the environment's graphify | pin the tested series |
| 21 Oct | saving Kraus parameters as `[re, im]` pairs broke loading of IBM noise models (490 Kraus errors in Kingston); jobs 024, 025 FAILED | `2e26d37`, test on FakeKingston, CI installs `qiskit-ibm-runtime` | test the loader on a real-format file |
| 22 Oct | J3 code scored 256 shots, the preregistration says 512 | `decisions/008` | read the gate against the hypothesis text |
| 23 Oct | a `git add` naming unfetched paths aborted and staged nothing; re-score jobs 028, 029 found no input file | `b8600a6` | check `git status` after staging |
| 26 Oct | two gate runs in the same second overwrote each other's record | `ce4238f`, `b92e08c` | unique record names |
| 28 Oct | encoder normalises constant columns to about 316x | `decisions/010`, `v2_final` | check what constant inputs do under normalisation; run a cross-carrier test before any twin or hardware campaign |
| 21 Oct | IBM arm B docstring called $15\lambda/16$ an average infidelity (it is the process infidelity; average adds $3\lambda/4$, so CZ is about 1.8x) | corrected in `decisions/009` | |

**Open problems**
1. **Hardware access** (above). 2. **J1 semigroup row / rank edge:** no tested configuration passes all rows on fresh seeds; `v1_final` misses the rank by 0.03 on one seed. 3. **Strong-coupling forecast** (J2 FAIL): $P_{\text{baryonic}}$ MAE 0.105/0.123 vs bound 0.05. 4. **`v2_final` unproven:** its J1 behaviour, its forecasts and its twin rehearsals are unknown; the encoder has less input information (no flag), so grounding or forecast quality could change. 5. **The explanation "AUROC 1.00 = amplified flag rate" is a hypothesis**, not tested. 6. **Disagreements between sources** still open: pilot QPU cap 90 s vs 120 s; estimator-bias rule 2.5 vs 4.0 SE (gate file governs); `docs/CLAIMS.md` C6 promises `evidence/J0_data/mass_dependence.json`, which does not exist; the plan calls the on-family mass dependence monotone (it is not); `STATE.json` outdated (lists M3 report `reports/015`, no jobs 023–033, `v1_confirm` as the working model while the J2/J3 model is now `v1_final`/`v2_final`, no Quantinuum or `decisions/008`–`010` entries); `docs/MODEL_CARD.md` is v1-era. 7. The `reports/012` plot tables P1–P7 cover configurations 1–6 only (see section 7); epoch curves for all 15 runs are given at nine epochs in §7.6, and the complete per-epoch histories for `v1_final` are in `evidence/runs/v1_final/seed*/history.json`; other runs' histories are only in local `runs/` (not committed). Not recorded: the parameter count of `v2_final`; the Perlmutter-side time per rung beyond the job table; the J0 gate re-run on a worker copy of `data/main`.

---

## Appendix A. Decisions (`decisions/INDEX.md`; one line each)
- **000** frozen conventions and coupling points (geometry, staggered phases, Jordan–Wigner order, negative magnetic coefficient, fingerprints).
- **001** numbered artifacts and the Graphify code graph (`new_artifact.py`, `check_artifacts.py`, pinned `graphifyy`).
- **002** compute: laptop for light work, Perlmutter for heavy jobs (superseded by 003, then 004).
- **003** compute: a safe laptop and a pull-based job queue for Perlmutter (superseded by 004).
- **004** compute: laptop and Perlmutter only; admission-controlled laptop runner (in force, amended by 006).
- **005** J1 energy grounding threshold 0.887 = 0.97 x measured ceiling 0.9145.
- **006** desktop RTX 3070 added as a second queue worker (default `where: desktop`).
- **007** preregistration deviation: dataset-equivalence tolerance corrected to rounding scale.
- **008** J3 gate scores the low-shot rows at the preregistered 512 shots.
- **009** twin with Quantinuum noise from Nexus device specifications (simulation only).
- **010** preregistration deviation: J3 model `v2_final` reads only the 18 physical observables.

## Appendix B. File map
| path | contents |
|---|---|
| `CLAUDE.md`, `~/.claude/CLAUDE.md` | project and personal rules (read first) |
| `plans/001_gauge-jepa-p-v2.md` | the plan in force (schedule §10, hypotheses §11, error budget §12, risks §14, compute §16) |
| `prompts/000`–`010` | session prompts (`003` = M3, `010` = M2a continuation) |
| `reports/000`–`016` | session reports (this is 016; 012 is the big one); `reports/INDEX.md` |
| `decisions/000`–`010` | decision records |
| `docs/` | `PREREGISTRATION.md` (signed; §7 deviations), `CLAIMS.md`, `MODEL_CARD.md` (v1 era), `PHYSICS.md`, `DESKTOP.md`, `PERLMUTTER.md`, `PAPER_OUTLINE.md` |
| `configs/` | `gates.yaml` (frozen), `compute.yaml`, `hardware_budget.yaml` (`approved: false`) |
| `STATE.json` | machine-readable state (partly outdated) |
| `src/su2qc_jepa/` | `physics/` (plaquette, su2, dynamics, chain, observables, conventions), `repo/` (artifacts, graph), `data/` (records, trajectories), `models/` (jepa, train), `twin/` (noise, run, layout), `hardware/` (ibm), `gates/` (j0_data, j1_training, j2_forecast, j3_hardware, ledger), `jobs.py`, `localrun.py`, `compute.py` |
| `scripts/` | `run.py` (runner), `make_dataset.py`, `train_jepa.py`, `run_twin.py`, `residual_eval.py`, `run_gate.py`, `twin_null_check.py`, `cross_carrier_check.py`, `build_noise_model.py`, `build_qtm_noise_model.py`, `qtm_list_devices.py`, `hw_list_backends.py`, `hw_dry_run.py`, `hw_submit.py`, `compare_fingerprints.py`, `j1_ceiling.py`, `plot_j1_diagnostics.py`, `prereg_hashes.py`, `graph_update.sh`, `replicate.sh`, `jobs/{enqueue,fetch,status}.py`, `worker/` |
| `jobs/000`–`033` | queue job files; results on branch `results` |
| `evidence/GATE_LEDGER.md` | every gate run; `evidence/J0_data`, `J1_training`, `J2_forecast`, `J3_twin_rehearsal` (gate records) |
| `evidence/twin/{ideal0,day0_kingston,day1_marrakesh,qtm_h2_2,qtm_helios_1,cross_carrier}` | noise models, residual evaluations, null check, cross-carrier check |
| `evidence/hardware/` | `backends_fake_*.json`, `quantinuum_devices_*.json` (no IBM job records exist) |
| `evidence/runs/v1_final/` | `args.json`, `forecast_eval.json`, `seed0..4/history.json`, `seed0/model.pt` |
| `evidence/figures/`, `figures/000`, `001` | J1 diagnostics figures and their data sidecars |
| `evidence/prereg/hashes.json`, `evidence/graph/stats.json`, `evidence/ENV.json`, `evidence/jobs/NNN/` | hashes, graph stats, environment, fetched job records |
| `data/{main,chain_onfam,chain_strong,gpu_smoke}`, `runs/<name>/` | local datasets and models (git-ignored) |
| `.local_runs/` | runner ledger and logs (git-ignored); `.local_runs/probe/` helper scripts of this report |

Key commits (full list in Appendix C): `88dc52d` bootstrap; `d7655e2` preregistration signed (tag `prereg-2026-10-16`); `bc7ba86` desktop worker; `07c13ca` J2 FAIL; `63a42ff` noiseless twin; `ac7e920` cross-carrier check; `aef9885` physics-only encoder; `72a15b4` decisions/010; `db8ab2c` job 033.

## Appendix C. Commit list (`git log --oneline | head -80`, newest first; 138 commits in all at the time of writing)

```
db8ab2c job: 033_v2-final-estimated-1017-min-20-min-on-the-laptop-queue-worke (train on desktop)
35bcf61 chore(graph): refresh code graph
72a15b4 docs: decisions/010, preregistration deviation: J3 model v2_final reads only the physical observables
aef9885 model: physics-only encoder option (JEPAConfig.encoder_inputs, train_jepa.py --physics-only) (decisions/010)
ac7e920 model: cross-carrier check (jobs/030): v1_final's encoder is off-distribution on twin/hardware records
9267d81 job: 032_qtm-helios-1-quantinuum-noise-twin-campaign-residual-eval-j3 (twin on desktop)
2e56cea job: 031_qtm-h2-2-quantinuum-noise-twin-campaign-residual-eval-j3-twi (twin on desktop)
89500e4 chore(graph): refresh code graph
31a0cd1 twin: Quantinuum H2-2 (specs 2025-08-28) and Helios-1 (specs 2025-11-05) twin noise files from Nexus; decisions/009
3be8941 twin: Quantinuum ion-trap noise (decisions/009): all-to-all runner, rzz-native model from Nexus noise_specs
3f01c81 job: 030_cross-carrier-check-on-v1-final-seed0-prompts-003-step-4 (eval on desktop)
ef837c4 chore(graph): refresh code graph
4423047 model: cross-carrier check (prompts/003 step 4): latent distances between diagonal, chain and twin-labelled records of the same states; allowlisted for queue workers
f0a2c4c chore(graph): refresh code graph
b92e08c twin: Kingston J3 rehearsal at 512 shots re-run for its own record (20261026T181636Z)
ce4238f gate: two gate runs in the same second no longer overwrite each other's record file
5f28dfe twin: J3 twin rehearsals re-scored at the preregistered 512 shots (decisions/008): FAIL on both calibrations
b8600a6 twin: add the files missing from 1b81156 (ledger rows, rehearsal records, residual_eval.json of both twins)
14b4c50 job: 029_day1-marrakesh-j3-twin-rehearsal-re-scored-at-512-shots-deci (eval on desktop)
1f1917c job: 028_day0-kingston-j3-twin-rehearsal-re-scored-at-512-shots-decis (eval on desktop)
1b81156 twin: J3 twin rehearsals on the Kingston (jobs/026) and Marrakesh (jobs/027) calibrations, scored at 256 shots (before decisions/008)
406ee75 chore(graph): refresh code graph
efcdac9 docs: decisions/008 (J3 low-shot level aligned with the preregistration); preregistration section 7
467b4a9 gate: J3 scores the low-shot rows at the preregistered low_shot_level (512) (decisions/008)
27d666e job: 027_day1-marrakesh-rerun-after-the-kraus-decoding-fix-calibrated (twin on desktop)
65f30eb job: 026_day0-kingston-rerun-after-the-kraus-decoding-fix-calibrated (twin on desktop)
44699e2 chore(graph): refresh code graph
2e26d37 twin: decode complex Kraus/unitary parameters when loading a saved noise model (fixes jobs/024)
579f95d job: 025_day1-marrakesh-calibrated-twin-campaign-residual-eval-j3-twi (twin on desktop)
1cc1017 job: 024_day0-kingston-calibrated-twin-campaign-residual-eval-j3-twin (twin on desktop)
d4e1aea chore(graph): refresh code graph
fd35c18 twin: calibrated line noise models from IBM's stored snapshots (no IBM account available)
ff559cf gate: J3 twin-rehearsal mode (recorded as J3_twin_rehearsal; self-compared reference points excluded); noise files record the device's own calibration date
9e18bb2 chore(graph): refresh code graph
041b262 twin: calibrated line noise models (build on the laptop, run on queue workers)
63a42ff twin: noiseless twin campaign ideal0 (jobs/023, desktop): all known-answer checks PASS
432c925 job: 023_ideal0-noiseless-twin-campaign-residual-eval-known-answer-ch (twin on desktop)
e505dfd chore(graph): refresh code graph
6479fb1 data: v1_final seed0 model (the preregistered J3 model) committed for desktop twin jobs
2b6c762 twin: noiseless twin campaign (run_twin.py --noise ideal) and known-answer checks (twin_null_check.py)
6c81795 chore(graph): refresh code graph
4a44a69 docs: session report (reports/015): desktop worker, v1_final, J2 FAIL; STATE, C8 not met
07c13ca gate: preregistered J2 FAIL on v1_final; J1 on v1_final FAIL (information only); v1_final dataset EQUIVALENT
7be3833 job: 022_j1-training-gate-on-v1-final-information-only-preregistratio (eval on desktop)
0b73384 job: 021_j2-forecasting-gate-on-v1-final-preregistration-section-3 (eval on desktop)
75e834d data: v1_final gate inputs (forecast_eval.json, args.json, seed0-4 history.json) committed for the desktop gate jobs
497217e job: 020_v1-final-dataset-equivalence-check-decisions-007 (eval on desktop)
c74cac7 chore(graph): refresh code graph
44125ef chore: allow compare_fingerprints.py on queue workers (read-only dataset comparison, decisions/007)
9a99cee data: v1_final (jobs/019, desktop) evidence and the laptop reference fingerprint of data/main (73fff8e5a7b7)
5870154 job: 019_train-jepa-estimated-1017-min-20-min-on-the-laptop-queue-wor (train on desktop)
f864bba chore(graph): refresh code graph
4b71bc0 data: compare_fingerprints.py prints the decisions/007 equivalence verdict; test
858487c docs: decisions/007, preregistration deviation: dataset-equivalence tolerance corrected to rounding scale
f68cea5 data: desktop GPU check jobs/018 COMPLETED; desktop dataset build is bit-identical to Perlmutter's
426893f chore: runner messages say 'queue worker' instead of Perlmutter (decisions/006)
6008bf4 job: 018_desktop-gpu-check-needs-a-gpu-the-laptop-gpu-is-not-used-per (train on desktop)
09f931e chore: desktop installer survives a missing user session bus and offers a cron schedule
79f9768 chore(graph): refresh code graph
80da45a chore: graph-freshness test uses the graphify of the test environment, not the first one on PATH
a94463b chore: pin qiskit 2.5.x and qiskit-aer 0.17.x (the tested series on laptop and Perlmutter)
de0c765 chore(graph): refresh code graph
f2498e3 docs: decisions/006 (desktop worker), docs/DESKTOP.md, CLAUDE.md section 5, STATE compute.desktop
bc7ba86 chore: desktop RTX 3070 as a second job-queue worker (decisions/006)
5833881 chore(graph): refresh code graph
6ef16d5 docs: M2b session report (reports/014), STATE M2 done, preregistration tag recorded
d7655e2 docs: preregistration signed (approved by Digonto 2026-10-15)
f932488 chore(graph): refresh code graph
5119b7a docs: preregistration draft for review (M2b): disclosure of known results, H1-H5, frozen inputs, exact analysis, exclusions
09d6221 gate: preregistration hashes (gates.yaml, datasets, model configuration) and a test freezing gates.yaml
a2086ad chore(graph): refresh code graph
c9ddfe6 chore: fix import order in test_pipeline.py (ruff I001), which failed CI lint since 5000bc9
030bcdc chore(graph): refresh code graph
29a04ee docs: M2a closing report (reports/013), model card, C7 not met, STATE M2a DONE with J1 FAIL
76f4c6b model: J1 diagnostics figures 000 (ablation ladder) and 001 (semigroup series + confirmation)
8b384ac gate: J1 FAIL on the confirmation run v1_confirm (fresh master seed 31415926)
d3b40ca job: 017_v1-confirm-estimated-1017-min-20-min-on-the-laptop-perlmutte (train on perlmutter)
600197b gate: J1 PASS for v1_wsig3_wsg10 (first pass); FAIL for v1_wsig2_wsg5 (rank 7.80, semigroup 1.01e-3)
7511864 job: 016_v1-wsig3-wsg10-estimated-510-min-20-min-on-the-laptop-perlmu (train on perlmutter)
1fb355a job: 015_v1-wsig2-wsg5-estimated-510-min-20-min-on-the-laptop-perlmut (train on perlmutter)
```

## Appendix D. Helper scripts (verbatim; in `.local_runs/probe/`, git-ignored; run each with `python scripts/run.py --no-queue --threads 1 -- python .local_runs/probe/<name>.py`, then read the runner log)

### D.twin_tables.py
```python
"""Twin / device tables for the hand-over report (reads evidence + results-branch copies; writes markdown to stdout)."""
import json, subprocess, warnings, numpy as np
warnings.filterwarnings("ignore")
from scipy.stats import spearmanr, rankdata
R = "/home/digimonk/Projects/su2qc-jepa/"
def gitshow(p):
    return json.loads(subprocess.check_output(["git","-C",R,"show","origin/results:"+p]))
def auroc(score, label):  # label 1 = arm B; P(score_B > score_A)
    s = np.asarray(score, float); l = np.asarray(label)
    r = rankdata(s); n1 = l.sum(); n0 = len(l)-n1
    return (r[l==1].sum()-n1*(n1+1)/2)/(n1*n0)
SC = ["jepa_twin","raw_twin","jepa_self","jepa_t0","flag_rate"]
srcs = {"ideal0 (noiseless)": json.load(open(R+"evidence/twin/ideal0/residual_eval.json")),
        "day0_kingston (IBM, 2026-04-15)": json.load(open(R+"evidence/twin/day0_kingston/residual_eval.json")),
        "day1_marrakesh (IBM, 2025-02-26)": json.load(open(R+"evidence/twin/day1_marrakesh/residual_eval.json")),
        "qtm_h2_2 (Quantinuum H2-2, 2025-08-28)": gitshow("031/outputs/evidence/twin/qtm_h2_2/residual_eval.json")}
print("## T1 Spearman(score, exact_error) and AUROC(score separates arm B from arm A), per twin, shot level and score\n")
print("Rule (as run_j3 rehearsal): points of arm A / seed 0 (self-reference, score exactly 0) are left out, so n = 135 per shot level (150 for the noiseless file in T3, which uses all points). Model in every file: evidence/runs/v1_final/seed0/model.pt\n")
print("| twin | shots | n | score | Spearman | AUROC (B vs A) |\n|---|---|---|---|---|---|")
for name, d in srcs.items():
    P = d["points"]
    for sh in (256, 512, 4000):
        pts = [p for p in P if p["shots"] == sh and not (p["arm"] == "A" and p.get("seed", 0) == 0)]
        lab = np.array([1 if p["arm"]=="B" else 0 for p in pts])
        err = np.array([p["exact_error"] for p in pts])
        for s in SC:
            x = np.array([p[s] for p in pts])
            print(f"| {name} | {sh} | {len(pts)} | {s} | {spearmanr(x, err)[0]:.3f} | {auroc(x, lab):.3f} |")
print("\n## T2 mean flag rate and mean exact error by arm and depth (4000 shots)\n")
print("| twin | arm | depth r | mean flag rate | mean exact_error | mean ideal_error |\n|---|---|---|---|---|---|")
for name, d in srcs.items():
    P = [p for p in d["points"] if p["shots"]==4000]
    for arm in "AB":
        for r in sorted({p["depth"] for p in P}):
            q = [p for p in P if p["arm"]==arm and p["depth"]==r]
            print(f"| {name} | {arm} | {r} | {np.mean([p['flag_rate'] for p in q]):.4f} | {np.mean([p['exact_error'] for p in q]):.4f} | {np.mean([p['ideal_error'] for p in q]):.4f} |")
print("\n## T3 noiseless null check by shot level (evidence/twin/ideal0/null_check.json)\n")
n = json.load(open(R+"evidence/twin/ideal0/null_check.json"))
print("| shots | n_A | n_B | null sigma | score | AUROC | Spearman vs exact error |\n|---|---|---|---|---|---|---|")
for sh, v in n["by_shots_level"].items():
    for s in SC:
        print(f"| {sh} | {v['n_A']} | {v['n_B']} | {v['null_sigma']:.4f} | {s} | {v['auroc_'+s]:.3f} | {v['spearman_'+s+'_vs_exact_error']:.3f} |")
print("\n## T4 cross-carrier summary (v1_final seed0; evidence/twin/cross_carrier/cross_carrier.json; median / p90 / median over noise_diag)\n")
c = json.load(open(R+"evidence/twin/cross_carrier/cross_carrier.json"))
print("n_states", c["n_states"], "master_seed", c["master_seed"], "gE", c["gE"], "masses", c["masses"], "depths", c["depths"], "dt", c["dt"], "keys", [k for k in c if k not in ("summary",)])
print("\n| shots | quantity | median | p90 | median / noise_diag median |\n|---|---|---|---|---|")
for sh, v in c["summary"].items():
    for k, q in v.items():
        r = q["median_over_noise_diag"]
        print(f"| {sh} | {k} | {q['median']:.4g} | {q['p90']:.4g} | {'' if r is None else format(r,'.3g')} |")
print("\n## T5 Quantinuum device parameters (evidence/hardware/quantinuum_devices_20261028T220635Z.json)\n")
q = json.load(open(R+"evidence/hardware/quantinuum_devices_20261028T220635Z.json"))
for k, v in q["devices"].items():
    if v.get("noise_specs"):
        print(k, v["system_type"], json.dumps(v["noise_specs"]))
print("\n(Twin parameter files:)")
for nme in ("qtm_h2_2","qtm_helios_1"):
    m = json.load(open(R+f"evidence/twin/{nme}/noise_model.json"))
    print(nme, m["backend"], m["calibration_measured"], json.dumps(m["params"]), json.dumps(m["noise_specs"]))
print("\n## T6 IBM twin line parameters (evidence/twin/*/noise_model.json; evidence/hardware/backends_fake_*.json)\n")
print("| twin | backend | calibration measured | line score | median line CZ error | max line CZ error | median line readout error |\n|---|---|---|---|---|---|---|")
for nme in ("day0_kingston","day1_marrakesh"):
    m = json.load(open(R+f"evidence/twin/{nme}/noise_model.json"))
    z = m["line_cz_errors"]; ro = m["line_readout_errors"]
    print(f"| {nme} | {m['backend']} | {m['calibration_measured']} | {m['line_score']:.3f} | {np.median(z):.5f} | {max(z):.5f} | {np.median(ro):.5f} |")
b = json.load(open(R+"evidence/hardware/backends_fake_20261021T221803Z.json"))
print("\n| fake backend | qubits | median 2q error | median readout error | best 12-qubit line score |\n|---|---|---|---|---|")
for x in b["backends"]:
    print(f"| {x['name']} | {x['num_qubits']} | {x['median_2q_error']:.5f} | {x['median_readout_error']:.5f} | {x['best_line_score']:.3f} |")
```

### D.j1_tables.py
```python
"""J1 plot data for all 14 configurations + v1_final (final epoch per seed; seed-mean curves at selected epochs)."""
import json, glob, numpy as np
R = "/home/digimonk/Projects/su2qc-jepa/"
RUNS = [("1","v1_base"),("2","v1_wsigreg2"),("3","v1_wsigreg5"),("4","v1_latent32"),("5","v1_ema"),("6","v1_wground3"),
        ("7","v1_curriculum"),("8","v1_wsemigroup1"),("9","v1_wsig2_wsg1"),("10","v1_wsig2_wsg3"),("11","v1_wsig2_wsg5"),
        ("12","v1_wsig2_wsg10"),("13","v1_wsig3_wsg10"),("14","v1_confirm"),("F","v1_final")]
H = {}
for n, r in RUNS:
    H[r] = [json.load(open(f)) for f in sorted(glob.glob(R+f"runs/{r}/seed[0-9]/history.json"))]
EP = [1,2,5,10,20,50,100,150,200]
print("## P8x final epoch (200), per seed, all configurations (runs/<run>/seed0..4/history.json, unmasked)\n")
print("| # | run | seed | eff_rank | R2_energy | R2_C_string | R2_P_meson | R2_P_baryonic | semigroup_resid | isotropy | pred_loss |\n|---|---|---|---|---|---|---|---|---|---|---|")
for n, r in RUNS:
    for i, h in enumerate(H[r]):
        e = h[-1]; g = e["ground_r2"]
        print(f"| {n} | {r} | {i} | {e['eff_rank']:.4f} | {g[0]:.5f} | {g[1]:.5f} | {g[2]:.5f} | {g[3]:.5f} | {e['semigroup_resid']:.5g} | {e['isotropy']:.5g} | {e['pred']:.5g} |")
print("\n## P8y per-configuration summary of the final epoch (what the J1 gate compares: min over seeds, max for semigroup)\n")
print("| # | run | n seeds | rank min | rank max | R2 energy min | R2 C_string min | R2 P_meson min | R2 P_baryonic min | semigroup max | semigroup min |\n|---|---|---|---|---|---|---|---|---|---|---|")
for n, r in RUNS:
    L = [h[-1] for h in H[r]]
    G = np.array([x["ground_r2"][:4] for x in L]); sg = [x["semigroup_resid"] for x in L]; rk = [x["eff_rank"] for x in L]
    print(f"| {n} | {r} | {len(L)} | {min(rk):.3f} | {max(rk):.3f} | {G[:,0].min():.5f} | {G[:,1].min():.5f} | {G[:,2].min():.5f} | {G[:,3].min():.5f} | {max(sg):.4g} | {min(sg):.4g} |")
for key, title in (("eff_rank","effective rank (seed mean; band min..max in P1 of reports/012 for configs 1-6)"),("semigroup_resid","semigroup residual (seed mean; log axis)")):
    print(f"\n## P-curve: {title} at selected epochs (all configurations)\n")
    print("| # | run | " + " | ".join(f"ep {e}" for e in EP) + " |\n|---|---|" + "---|"*len(EP))
    for n, r in RUNS:
        v = [np.mean([h[e-1][key] for h in H[r]]) for e in EP]
        print(f"| {n} | {r} | " + " | ".join(f"{x:.4g}" for x in v) + " |")
print("\n## P-curve: grounding R2 of energy (seed mean) at selected epochs\n")
print("| # | run | " + " | ".join(f"ep {e}" for e in EP) + " |\n|---|---|" + "---|"*len(EP))
for n, r in RUNS:
    v = [np.mean([h[e-1]["ground_r2"][0] for h in H[r]]) for e in EP]
    print(f"| {n} | {r} | " + " | ".join(f"{x:.4f}" for x in v) + " |")
print("\n## P-curve: training loss terms (unweighted, seed mean) at epoch 200, all configurations\n")
print("| # | run | pred | sigreg | ground | semigroup | total (weighted) |\n|---|---|---|---|---|---|---|")
for n, r in RUNS:
    print(f"| {n} | {r} | " + " | ".join(f"{np.mean([h[-1][k] for h in H[r]]):.5g}" for k in ("pred","sigreg","ground","semigroup","total")) + " |")
print("\n## args.json of v1_final and v1_confirm\n")
for r in ("v1_final","v1_confirm"):
    print(r, json.dumps(json.load(open(R+f"runs/{r}/args.json"))))
```

### D.j2_dev_tables.py
```python
"""J2 MAE table (all models, families, horizons, targets) and compact device-parameter table for the bar charts."""
import json, numpy as np
R = "/home/digimonk/Projects/su2qc-jepa/"
f = json.load(open(R+"evidence/runs/v1_final/forecast_eval.json"))
print("## J2 MAE (evidence/runs/v1_final/forecast_eval.json = input of evidence/J2_forecast/20261021T201507Z.json; mean of 5 seeds; n_test", f["n_test"], "; context_step", f["context_step"], "; master_seed", f["master_seed"], ")\n")
print("| family | model | horizon | P_baryonic | P_meson | C_string | mean of 3 |\n|---|---|---|---|---|---|---|")
for fam in ("onfam","strong"):
    for m in ("jepa","ridge","autoregressive","supervised_mlp","jepa_masked","ridge_masked"):
        for h in ("+4","+8"):
            v = f["mae"][fam][m][h]; a = [v["P_baryonic"], v["P_meson"], v["C_string"]]
            print(f"| {fam} | {m} | {h} | {a[0]:.4f} | {a[1]:.4f} | {a[2]:.4f} | {np.mean(a):.4f} |")
print("\ntrain_seeds:", f["train_seeds"], "checksum:", f["checksum"], "dataset:", f["dataset"])
print("\n## T7 compact device-parameter table (bar-chart data)\n")
q = json.load(open(R+"evidence/hardware/quantinuum_devices_20261028T220635Z.json"))["devices"]
print("| device | spec date | 1q error p1 | 2q error p2 | readout p_meas_0 | readout p_meas_1 | memory error | source |\n|---|---|---|---|---|---|---|---|")
for k in ("H2-1","H2-2","Helios-1"):
    n = q[k]["noise_specs"]; s = n["spam_error"]
    print(f"| Quantinuum {k} | {n['date']} | {n['1q_gate_error']['p1']:.3g} | {n['2q_gate_error']['p2']:.3g} | {s['p_meas_0']:.3g} | {s['p_meas_1']:.3g} | {n['memory_error']['memory_error']:.3g} | quantinuum_devices_20261028T220635Z.json |")
for nme in ("day0_kingston","day1_marrakesh"):
    m = json.load(open(R+f"evidence/twin/{nme}/noise_model.json"))
    print(f"| IBM {m['backend']} (twin {nme}) | {m['calibration_measured'][:10]} | not recorded | line median CZ {np.median(m['line_cz_errors']):.3g} (max {max(m['line_cz_errors']):.3g}) | line median readout {np.median(m['line_readout_errors']):.3g} (both outcomes) | | not recorded (T1, T2 per qubit are in the file) | evidence/twin/{nme}/noise_model.json |")
```
