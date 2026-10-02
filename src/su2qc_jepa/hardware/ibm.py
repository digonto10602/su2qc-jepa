"""IBM Quantum submission path with a dry-run-first, budget-guarded discipline.

Nothing here talks to a QPU unless ``submit(..., confirm=True)`` is called with an approved
budget file.  The sequence Claude Code must follow (CLAUDE.md, hardware rules):

1. ``dry_run``  - transpile to the backend's ISA on the chosen qubit line, count CZ and
                   two-qubit depth, estimate QPU seconds, write a manifest with circuit hashes.
2. human reads the manifest and edits configs/hardware_budget.yaml (approved: true).
3. ``submit``   - re-checks the manifest hash against the budget file, the running ledger of
                   QPU seconds, takes a calibration snapshot, submits one Sampler job, records
                   job id + options + snapshot in evidence/hardware/jobs/<job_id>.json.
4. ``collect``  - fetches results, writes raw counts (immutable) and usage.

The quantum-seconds estimate is a *prior*; the pilot job's measured usage replaces it.
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

import yaml

__all__ = ["DryRunSummary", "dry_run", "check_budget", "submit", "collect", "BudgetError"]


class BudgetError(RuntimeError):
    pass


@dataclass
class DryRunSummary:
    backend: str
    line: list[int]
    n_circuits: int
    shots: int
    cz_counts: list[int]
    two_qubit_depths: list[int]
    est_qpu_seconds: float
    circuit_hashes: list[str]
    options: dict = field(default_factory=dict)
    created_utc: str = ""
    manifest_hash: str = ""


def _hash_circuits(isa_circuits) -> list[str]:
    from qiskit import qasm3

    out = []
    for c in isa_circuits:
        try:
            s = qasm3.dumps(c)
        except Exception:  # pragma: no cover
            s = str(c)
        out.append(hashlib.sha256(s.encode()).hexdigest())
    return out


def estimate_qpu_seconds(n_circuits: int, shots: int, shots_per_second: float = 2000.0, per_job_overhead_s: float = 15.0) -> float:
    """Crude prior: shots / rate + fixed overhead.  Replace `shots_per_second` by the pilot's measured value."""
    return n_circuits * shots / shots_per_second + per_job_overhead_s


def dry_run(circuits: list, backend, line: list[int], shots: int, out_dir: str | Path, options: dict | None = None,
            shots_per_second: float = 2000.0) -> DryRunSummary:
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1, initial_layout=line, seed_transpiler=7)
    isa = pm.run(circuits)
    two_q = []
    czs = []
    for c in isa:
        ops = c.count_ops()
        czs.append(int(sum(v for k, v in ops.items() if k in ("cz", "ecr", "cx"))))
        two_q.append(int(c.depth(lambda i: len(i.qubits) == 2)))
    summary = DryRunSummary(backend=backend.name, line=list(line), n_circuits=len(isa), shots=shots, cz_counts=czs,
                            two_qubit_depths=two_q, est_qpu_seconds=estimate_qpu_seconds(len(isa), shots, shots_per_second),
                            circuit_hashes=_hash_circuits(isa), options=options or {},
                            created_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    d = asdict(summary)
    d.pop("manifest_hash")
    summary.manifest_hash = hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()
    (out_dir / "dry_run_manifest.json").write_text(json.dumps(asdict(summary), indent=2))
    from qiskit import qpy

    with open(out_dir / "isa_circuits.qpy", "wb") as f:
        qpy.dump(isa, f)
    return summary


def check_budget(manifest: DryRunSummary | dict, budget_path: str | Path, ledger_path: str | Path) -> dict:
    """Raise BudgetError unless the budget file approves exactly this manifest and the ledger has room."""
    m = asdict(manifest) if isinstance(manifest, DryRunSummary) else manifest
    b = yaml.safe_load(Path(budget_path).read_text())
    if not b.get("approved", False):
        raise BudgetError("budget file not approved (approved: false)")
    if b.get("manifest_hash") != m["manifest_hash"]:
        raise BudgetError("budget file approves a different manifest hash")
    ledger = json.loads(Path(ledger_path).read_text()) if Path(ledger_path).exists() else {"jobs": [], "qpu_seconds_spent": 0.0}
    if len(ledger["jobs"]) + 1 > int(b.get("max_jobs", 0)):
        raise BudgetError("job cap reached")
    if ledger["qpu_seconds_spent"] + m["est_qpu_seconds"] > float(b.get("max_qpu_seconds", 0)):
        raise BudgetError("estimated QPU seconds would exceed the approved budget")
    if max(m["cz_counts"]) > int(b.get("max_cz_per_circuit", 10**9)):
        raise BudgetError("a circuit exceeds the approved CZ cap")
    return ledger


def submit(isa_path: str | Path, manifest_path: str | Path, budget_path: str | Path, ledger_path: str | Path, backend,
           confirm: bool = False, out_dir: str | Path = "evidence/hardware/jobs", sampler_options: dict | None = None) -> str:
    """Submit one Sampler job.  Refuses without confirm=True and an approved budget."""
    if not confirm:
        raise BudgetError("submit called without confirm=True")
    manifest = json.loads(Path(manifest_path).read_text())
    ledger = check_budget(manifest, budget_path, ledger_path)
    from qiskit import qpy
    from qiskit_ibm_runtime import SamplerV2 as Sampler

    with open(isa_path, "rb") as f:
        isa = qpy.load(f)
    if _hash_circuits(isa) != manifest["circuit_hashes"]:
        raise BudgetError("ISA circuits do not match the manifest hashes")
    snapshot = calibration_snapshot(backend)
    sampler = Sampler(mode=backend)
    opts = sampler_options or {}
    if opts.get("dynamical_decoupling"):
        sampler.options.dynamical_decoupling.enable = True
        sampler.options.dynamical_decoupling.sequence_type = opts.get("dd_sequence", "XpXm")
    if opts.get("twirling"):
        sampler.options.twirling.enable_gates = True
        sampler.options.twirling.num_randomizations = int(opts.get("num_randomizations", 32))
        sampler.options.twirling.shots_per_randomization = "auto"
    job = sampler.run([(c,) for c in isa], shots=int(manifest["shots"]))
    jid = job.job_id()
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rec = {"job_id": jid, "backend": backend.name, "submitted_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "manifest_hash": manifest["manifest_hash"], "options": opts, "calibration_snapshot": snapshot,
           "est_qpu_seconds": manifest["est_qpu_seconds"], "status": "submitted"}
    (out_dir / f"{jid}.json").write_text(json.dumps(rec, indent=2, default=str))
    ledger["jobs"].append({"job_id": jid, "est_qpu_seconds": manifest["est_qpu_seconds"], "measured_qpu_seconds": None})
    ledger["qpu_seconds_spent"] = float(ledger["qpu_seconds_spent"]) + float(manifest["est_qpu_seconds"])
    Path(ledger_path).write_text(json.dumps(ledger, indent=2))
    return jid


def collect(job_id: str, service, ledger_path: str | Path, out_dir: str | Path = "evidence/hardware/jobs") -> dict:
    """Fetch results; write immutable raw counts and the measured usage; update the ledger."""
    job = service.job(job_id)
    result = job.result()
    counts = []
    for pub in result:
        data = pub.data
        creg = next(iter(data.__dict__)) if hasattr(data, "__dict__") else "c"
        bits = getattr(data, creg)
        counts.append(dict(bits.get_counts()))
    usage = None
    try:
        usage = job.metrics().get("usage", {}).get("quantum_seconds")
    except Exception:  # pragma: no cover
        pass
    out_dir = Path(out_dir)
    raw = {"job_id": job_id, "counts": counts, "collected_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "measured_qpu_seconds": usage}
    p = out_dir / f"{job_id}.raw.json"
    if p.exists():
        raise RuntimeError("raw record exists; hardware records are immutable")
    p.write_text(json.dumps(raw))
    ledger = json.loads(Path(ledger_path).read_text())
    for j in ledger["jobs"]:
        if j["job_id"] == job_id:
            j["measured_qpu_seconds"] = usage
    if usage is not None:
        ledger["qpu_seconds_spent"] = float(sum((j["measured_qpu_seconds"] or j["est_qpu_seconds"]) for j in ledger["jobs"]))
    Path(ledger_path).write_text(json.dumps(ledger, indent=2))
    return raw


def calibration_snapshot(backend) -> dict:
    """Per-qubit T1/T2/readout and per-edge two-qubit errors from the backend target (best effort)."""
    snap = {"backend": backend.name, "taken_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "qubits": {}, "edges": {}}
    try:
        target = backend.target
        for q in range(target.num_qubits):
            qp = target.qubit_properties[q] if target.qubit_properties else None
            snap["qubits"][q] = {"t1": getattr(qp, "t1", None), "t2": getattr(qp, "t2", None)}
        if "measure" in target.operation_names:
            for q, props in target["measure"].items():
                snap["qubits"][q[0]]["readout_error"] = getattr(props, "error", None)
        for name in ("cz", "ecr", "cx"):
            if name in target.operation_names:
                for q, props in target[name].items():
                    snap["edges"][f"{q[0]}-{q[1]}"] = getattr(props, "error", None)
                break
    except Exception as e:  # pragma: no cover
        snap["error"] = repr(e)
    return snap
