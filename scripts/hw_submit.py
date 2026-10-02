#!/usr/bin/env python
"""Submit the approved dry run (one job) or collect a finished job.
  python scripts/hw_submit.py submit --dry-run-dir evidence/hardware/day1 --confirm [--dd] [--twirl]
  python scripts/hw_submit.py collect --job-id <id>
"""
import argparse

from su2qc_jepa.hardware.ibm import collect, submit

p = argparse.ArgumentParser()
p.add_argument("mode", choices=("submit", "collect"))
p.add_argument("--dry-run-dir", default="evidence/hardware/dry_run")
p.add_argument("--budget", default="configs/hardware_budget.yaml")
p.add_argument("--ledger", default="evidence/hardware/QPU_LEDGER.json")
p.add_argument("--job-id")
p.add_argument("--confirm", action="store_true")
p.add_argument("--dd", action="store_true", help="arm B: dynamical decoupling")
p.add_argument("--twirl", action="store_true", help="arm B: Pauli gate twirling")
a = p.parse_args()

from qiskit_ibm_runtime import QiskitRuntimeService  # noqa: E402

service = QiskitRuntimeService()
if a.mode == "submit":
    import json

    man = json.load(open(f"{a.dry_run_dir}/dry_run_manifest.json"))
    backend = service.backend(man["backend"])
    jid = submit(f"{a.dry_run_dir}/isa_circuits.qpy", f"{a.dry_run_dir}/dry_run_manifest.json", a.budget, a.ledger, backend,
                 confirm=a.confirm, sampler_options={"dynamical_decoupling": a.dd, "twirling": a.twirl})
    print("submitted job", jid)
else:
    raw = collect(a.job_id, service, a.ledger)
    print("collected", a.job_id, "measured QPU seconds:", raw["measured_qpu_seconds"])
