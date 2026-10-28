#!/usr/bin/env python
"""Quantinuum device specifications from Nexus (laptop only: uses the saved Nexus login, never pushed to workers).

Writes evidence/hardware/quantinuum_devices_<UTC>.json: per real H-series/Helios machine its qubit count, connectivity,
native gate set and the dated noise_specs block (1q/2q gate errors, SPAM, memory, crosstalk, with uncertainties) - the
inputs of scripts/build_qtm_noise_model.py.  Read-only: nothing is submitted.
  python scripts/qtm_list_devices.py
"""
import json
import time
from pathlib import Path

import qnexus as qnx

devs = qnx.devices.get_all(issuers=[qnx.devices.IssuerEnum.QUANTINUUM]).df()
out = {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "source": "Quantinuum Nexus (qnexus.devices.get_all)", "devices": {}}
for _, row in devs.iterrows():
    bi = row["backend_info"]
    misc = dict(bi.misc or {})
    out["devices"][row["device_name"]] = {
        "system_type": misc.get("system_type"), "n_qubits": len(bi.architecture.nodes) if bi.architecture else None,
        "connectivity": misc.get("connectivity"), "gate_set": sorted(str(g).replace("OpType.", "") for g in bi.gate_set),
        "noise_specs": misc.get("noise_specs"), "emulator": misc.get("emulator"), "benchmarks": misc.get("benchmarks"),
        "max_n_shots": misc.get("max_n_shots")}
p = Path("evidence/hardware") / f"quantinuum_devices_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}.json"
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text(json.dumps(out, indent=1, default=str))
for name, d in out["devices"].items():
    ns = d["noise_specs"] or {}
    if d["system_type"] == "hardware":
        g2 = (ns.get("2q_gate_error") or {}).get("p2")
        g1 = (ns.get("1q_gate_error") or {}).get("p1")
        sp = ns.get("spam_error") or {}
        me = (ns.get("memory_error") or {}).get("memory_error")
        print(f"{name:10s} specs {ns.get('date')}  qubits {d['n_qubits']}  p1 {g1}  p2 {g2}  "
              f"SPAM 0->1 {sp.get('p_meas_0')} 1->0 {sp.get('p_meas_1')}  memory {me}")
print("wrote", p)
