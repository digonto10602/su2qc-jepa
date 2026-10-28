---
id: decisions/009
title: Twin with Quantinuum noise from Nexus device specifications
series: decisions
created_utc: '2026-10-28T22:20:30Z'
author: claude-code
milestone: M3
status: active
supersedes: null
superseded_by: null
---

# Twin with Quantinuum noise from Nexus device specifications

**Decided by:** Digonto, 2026-10-28 ("twin with quantinuum noise, i have access to nexus portal now"). **Drafted by:** claude-code. **Context:** the IBM account is no longer available (21 Oct), so the IBM twins use the stored snapshots in `qiskit-ibm-runtime` (`day0_kingston`, `day1_marrakesh`).

## Decision
1. **A second hardware family for the twin.** The twin campaign and the J3 twin rehearsal also run with the noise of Quantinuum ion-trap machines. These are trapped ions: all-to-all connectivity, the native two-qubit ZZ interaction (`rzz`) plus single-qubit rotations. The circuits are the same Krylov-chain circuits, compiled to `rzz`/`rx`/`ry`/`rz`, and need exactly as many two-qubit gates as on IBM's CZ line (34/56/100/188 for $r = 1, 2, 4, 8$).
2. **Source of the numbers.** Each machine's dated `noise_specs` as reported by Quantinuum Nexus:
   - read with `scripts/qtm_list_devices.py` (needs the Nexus login, laptop only);
   - saved to `evidence/hardware/quantinuum_devices_<UTC>.json`;
   - turned into twin files by `scripts/build_qtm_noise_model.py`, which needs no login.

   The first two machines: H2-2 (specs of 2025-08-28) and Helios-1 (specs of 2025-11-05).
3. **Model** (`twin/noise.quantinuum_noise_model`):
   - depolarising gate errors whose average infidelity equals the published $p_2$ (two-qubit, $\lambda = \tfrac43 p_2$) and $p_1$ (single-qubit, $\lambda = 2p_1$);
   - asymmetric readout flips $p_{\text{meas},0}$, $p_{\text{meas},1}$;
   - the memory error as one phase flip per qubit per two-qubit gate;
   - measurement crosstalk ($\sim10^{-5}$) and leakage left out;
   - arm B: every error ×2.
4. **Strictly simulation.** Nothing is submitted to Quantinuum hardware, and nothing to Quantinuum's cloud emulators. Submitting remains forbidden by `CLAUDE.md` §4 unless a session prompt contains "paid provider approved by Digonto", together with a budget and approval procedure like IBM's, which does not exist for Quantinuum. The Nexus login stays on the laptop, as the IBM token did; queue workers only read the committed specification files.
5. **New dependency:** `qnexus==0.51.2`, as the optional extra `quantinuum` in `pyproject.toml`, installed only in the laptop environment. It is not needed on workers or in CI.

## Why
- Without the IBM account, the twin is the only remaining stand-in for hardware. Quantinuum's published specifications are current to within a year. They come with uncertainties, and they describe a very different noise regime: about 2× lower two-qubit error and about 10× lower readout error than the IBM Heron lines.
- That tests whether the J3 rehearsal findings depend on the noise regime. Those findings are AUROC 1.00 for detecting the degraded arm, but Spearman below the raw baseline.

## Alternatives considered
- **Quantinuum's own emulator (H2-1E etc.) via Nexus:** a more faithful noise model, including transport and memory effects, but it consumes emulator credits and runs remote jobs. Not chosen now; it could be added with a decision record and a budget.
- **Hand-picked "typical" ion-trap numbers:** not traceable. Rejected.

## Consequences
- Code: `QUANTINUUM_BASIS`, `quantinuum_noise_model`, `save_quantinuum_noise_file`, `load_twin_noise` (twin/noise.py); `TwinRunner.coupling` ("line" | "all"); `run_twin.py` loads either file type; `scripts/qtm_list_devices.py`; `scripts/build_qtm_noise_model.py`. Test: `test_quantinuum_noise_model`.
- Correction made with this change: the description of the IBM degraded arm wrongly called $15\lambda/16$ an *average* infidelity. It is the process infidelity; the average infidelity added is $3\lambda/4$, which is why that arm's CZ error is about 1.8×, not 2×. The values recorded so far are unaffected.
- Twin results on these files are labelled with the machine and the specification date, and they are never presented as hardware results.
