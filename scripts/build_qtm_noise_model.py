#!/usr/bin/env python
"""Twin noise file of a Quantinuum machine from the Nexus specifications saved by scripts/qtm_list_devices.py.

Needs no login (it reads the committed evidence file).  Writes evidence/twin/<name>/noise_model.json with the device's
dated noise_specs; run_twin.py --noise-model rebuilds the Aer model from them (twin/noise.quantinuum_noise_model):
native rzz + rx/ry/rz gates, all-to-all connectivity, arm B = every error doubled.
  python scripts/build_qtm_noise_model.py --specs evidence/hardware/quantinuum_devices_<UTC>.json --device H2-2 --name qtm_h2_2
"""
import argparse
import json
from pathlib import Path

from su2qc_jepa.twin.noise import save_quantinuum_noise_file

p = argparse.ArgumentParser()
p.add_argument("--specs", required=True)
p.add_argument("--device", required=True)
p.add_argument("--K", type=int, default=12)
p.add_argument("--name", required=True)
a = p.parse_args()

dev = json.loads(Path(a.specs).read_text())["devices"][a.device]
assert dev["system_type"] == "hardware", f"{a.device} is not a hardware machine"
assert dev["connectivity"] == "all-to-all" and dev["n_qubits"] >= a.K
d = save_quantinuum_noise_file(f"evidence/twin/{a.name}/noise_model.json", a.device, dev["noise_specs"], a.K, a.specs)
print(f"{a.device}: specs {d['calibration_measured']}  " + "  ".join(f"{k}={v}" for k, v in d["params"].items()))
print("wrote", f"evidence/twin/{a.name}/noise_model.json")
