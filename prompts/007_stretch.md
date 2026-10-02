---
id: prompts/007
title: M7 — One stretch item (W7), chosen on 15 Nov by Digonto
series: prompts
created_utc: '2026-10-01T17:50:00Z'
author: planner
milestone: M7
status: active
supersedes: null
superseded_by: null
---

# M7 — One stretch item (W7), chosen on 15 Nov by Digonto

**Session protocol:** `CLAUDE.md` §2 — start with `scripts/env_check.py` and `bash scripts/graph_update.sh --check` (read the first screen of `graphify-out/GRAPH_REPORT.md`); use `graphify query/explain/affected` before broad searches; end with tests, the gate, `bash scripts/graph_update.sh`, a numbered session report (`python scripts/new_artifact.py reports "M7: <result>" --milestone M7`), `scripts/check_artifacts.py` OK, `STATE.json`, and a final `chore(graph):` commit. Any new prompt you write for a later session goes into `prompts/` via `scripts/new_artifact.py prompts ...`; every figure via `scripts/new_artifact.py figures ... --ext .png`.

Pick exactly one, in this priority order unless told otherwise:

**(a) 2×3 ladder (simulator only).** Generalise `physics/plaquette.py` to a `LadderModel` (6 vertices, 7 links; 3-link vertices with intertwiner multiplicity 2 at $j_{\max}=1/2$ — the vertex-singlet construction already supports multiplicities). Verify 1,727 states and the $N$-sector counts; find the ladder's stretched-string analogue; compute the Krylov dimension needed for $t\le3/g_E$ at $g_E=2$ and the chain cost; generate a 2,000-trajectory dataset; transfer test of the world model with 10 % fine-tuning (R7). No hardware.

**(b) Quantum encoder (J4).** Implement a gauge-respecting trainable circuit on the 12-qubit chain carrier (excitation-conserving XY layers + Rz), latent = 8 expectation values, trained on the same loss by parameter-shift on Aer/CUDA-Q statevector; preregistered matched-shot test vs the classical encoder and vs a classical simulation of the circuit. Report either way.

**(c) IonQ Forte via Amazon Braket — only if the session prompt contains "paid provider approved by Digonto".** 25 tasks × 2,500 shots of the on-family KC-prep block; cross-device residual sign/scale.
