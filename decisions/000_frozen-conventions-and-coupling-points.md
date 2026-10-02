---
id: decisions/000
title: Frozen conventions and coupling points
series: decisions
created_utc: '2026-10-01T17:40:00Z'
author: planner
milestone: M0
status: active
supersedes: null
superseded_by: null
---

# Frozen conventions and coupling points

**Decision.** `src/su2qc_jepa/physics/conventions.py` freezes: geometry and link order $(l_a,l_1,l_2,l_3)$; loop $U_\square=U_aU_3U_2^\dagger U_1^\dagger$; staggered phases with $\prod_\square\eta=-1$ jointly with a *negative* magnetic coefficient $c_B=-1/(4g_E^2)$ on-family and $c_B=-0.02$ at P-S; Jordan–Wigner order; P-A $=(1,3/8,0.25,-0.0625)$ (the v0.6.1 ruling, $g_E=2$), P-S $=(1,3/8,0.02,-0.02)$.

**Why.** The physics-setup notes (9 Sept 2026) §2.3 state that $\prod\eta$ and the magnetic sign are one joint convention; the v0.6.1 ruling fixes P-A as the v0.5.0 window. The package reproduces the notes' $g_E=1$ dynamics table to three digits, which pins the joint convention.

**Consequences.** Any change needs a new ADR, a new fingerprint test and a re-run of J0. The L12 encoding map (3793) is not used by v2 and remains an open point of the SU2ZX repository, not of this one.
