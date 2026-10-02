#!/usr/bin/env python
"""Report the software environment and write evidence/ENV.json (run at the start of every session)."""
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

info = {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "python": sys.version.split()[0], "platform": platform.platform()}
for mod in ("numpy", "scipy", "qiskit", "qiskit_aer", "qiskit_ibm_runtime", "torch", "sklearn", "yaml", "mthree"):
    try:
        m = __import__(mod)
        info[mod] = getattr(m, "__version__", "present")
    except Exception as e:  # noqa: BLE001
        info[mod] = f"MISSING ({type(e).__name__})"
try:
    from su2qc_jepa.compute import pick_device

    info["torch_device_used"] = pick_device()
except Exception as e:  # noqa: BLE001
    info["torch_device_used"] = f"error {e!r}"
try:
    import torch

    info["cuda"] = torch.cuda.is_available()
    info["gpu"] = torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
except Exception:  # noqa: BLE001
    pass
try:
    from qiskit_aer import AerSimulator

    info["aer_devices"] = AerSimulator().available_devices()
except Exception as e:  # noqa: BLE001
    info["aer_devices"] = f"error {e!r}"
try:
    info["git_head"] = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
    info["git_dirty"] = bool(subprocess.check_output(["git", "status", "--porcelain"], text=True).strip())
except Exception:  # noqa: BLE001
    info["git_head"] = None
try:
    subprocess.check_output(["graphify", "--help"], text=True, stderr=subprocess.STDOUT)
    import importlib.metadata as md

    info["graphify"] = md.version("graphifyy")
except Exception as e:  # noqa: BLE001
    info["graphify"] = f"MISSING ({type(e).__name__}) - pip install graphifyy==0.9.74"
gp = Path("graphify-out/graph.json")
if gp.exists():
    import json as _json

    g = _json.loads(gp.read_text())
    info["graph"] = {"nodes": len(g.get("nodes", [])), "edges": len(g.get("links", [])), "built_at_commit": g.get("built_at_commit")}
else:
    info["graph"] = "none - run bash scripts/graph_update.sh"
try:
    info["ibm_account_saved"] = Path.home().joinpath(".qiskit", "qiskit-ibm.json").exists()
except Exception:  # noqa: BLE001
    pass
Path("evidence").mkdir(exist_ok=True)
Path("evidence/ENV.json").write_text(json.dumps(info, indent=2))
print(json.dumps(info, indent=2))
missing = [k for k, v in info.items() if isinstance(v, str) and v.startswith("MISSING") and k in ("numpy", "scipy", "qiskit", "qiskit_aer", "torch", "yaml")]
if missing:
    print("MISSING required packages:", missing)
    sys.exit(1)
