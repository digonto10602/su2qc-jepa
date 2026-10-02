---
id: reports/000
title: 'Package build: plan audit, Gauge-JEPA-P v2 and the starter package'
series: reports
created_utc: '2026-10-01T17:55:00Z'
author: planner
milestone: null
status: done
supersedes: null
superseded_by: null
---

# Package build: plan audit, Gauge-JEPA-P v2 and the starter package

**Milestone:** before M0 · **Prompt:** the user's request of 1 Oct 2026 (Cowork) · **Commit range:** not yet under git

## What was asked
Check the 1 Oct Gauge-JEPA-P plan (`plans/000`) for problems, fix them, rewrite the plan with full detail of every step (what is tested, what Claude Code does, what outcomes to expect), say whether a better plan exists that is feasible on real hardware (the 2×2 plaquette being the realistic device limit), and build a `su2qc-*` starter package for Claude Code whose first session creates and pushes the public repository `digonto10602/su2qc-jepa`.

## Actions taken
1. Read the project's physics-setup notes (9 Sept), the v0.5.0 review, the Sufian overlap note, the Hanada assessment, the Nine-Month Plan and the GI-Cost prompts; checked external facts (IBM plan limits, IonQ/Braket prices, LeJEPA/SIGReg, tool versions).
2. Implemented the physics core: SU(2) Clebsch–Gordan and spin matrices; the gauge-invariant basis from vertex singlets (route A) and the full gauge-redundant space with Gauss-law generators (route B); observables and channel projectors; exact evolution and Lanczos.
3. Implemented the Krylov-chain carrier (one-hot Lanczos basis as an XY chain; Strang circuits; a state-preparation cascade) with an exact in-sector reference and exact Z/X samplers.
4. Implemented estimators, a two-family dataset generator with rule-based splits, the JEPA model (encoder, GRU predictor, SIGReg, grounding heads, semigroup loss) with ridge/autoregressive/supervised baselines, a seeded Aer twin, a qubit-line chooser, the IBM dry-run/budget/submit/collect path, gates J0–J3, the smoke pipeline and CI.
5. Wrote the v2 plan (`plans/001`), `CLAUDE.md`, nine session prompts, preregistration and claims templates.

## Results and what they mean
- Fingerprints reproduced: 82 states; sectors 2/20/38/20/2; electric degeneracies 16/16/18/16/16; 152 states at $j_{\max}=1$; routes A and B agree to $4\times10^{-16}$; $\|[G^a_n,H]\|=0$; the notes' $g_E=1$ dynamics ($P_{\text{baryonic}}=0.432/0.732/0.821$ at $t=1/2/3$) reproduced.
- Carrier at P-A, $K=12$, $\Delta t=0.375$: 34/56/100/188 CZ for $r=1,2,4,8$ (two-qubit depth 6/10/18/34); Krylov error $1.1\times10^{-4}$; Strang infidelity $\le1.2\times10^{-3}$; FakeTorino dry run selected a 12-qubit line with no routing overhead.
- Mass dependence at P-A is weak (breaking fraction at $t=3/g_E$: 0.63 → 0.53 over $\mu\in[0.15,0.65]$); the resonance is sharp only at strong coupling — the reason for the two-family design.
- Gate J0 PASS in full mode; smoke pipeline end to end in about one minute; JEPA v0 not yet healthy (effective rank 4–6/16), which is week 2's job.
- Full numbers: `plans/001` Appendix B.

## Code graph
| | before | after |
|---|---|---|
| nodes / edges / communities | — | not yet built (Graphify adopted 2 Oct, `reports/001`) |

## Problems and assumptions
No hardware job submitted; all noisy numbers EMULATED. IBM Open Plan access, the RTX 3070 desktop and availability of the SU2ZX code for the M1 cross-check are assumed. The JEPA v0 is a scaffold.

## Next action
`reports/001` (conventions update), then `prompts/000` in the first Claude Code session.
