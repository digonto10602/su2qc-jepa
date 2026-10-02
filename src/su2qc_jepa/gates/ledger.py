"""Gate results and the ledger.  Gate scripts are the only arbiters of pass/fail."""
from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

import yaml

__all__ = ["GateRow", "GateResult", "load_thresholds", "write_gate"]


@dataclass
class GateRow:
    name: str
    status: str  # PASS / FAIL / PARTIAL / NOT RUN / VOID
    measured: object
    threshold: object
    evidence: str = ""
    note: str = ""


@dataclass
class GateResult:
    gate: str
    rows: list[GateRow] = field(default_factory=list)
    started_utc: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

    def add(self, name, ok, measured, threshold, evidence="", note=""):
        self.rows.append(GateRow(name, "PASS" if ok else "FAIL", measured, threshold, evidence, note))

    def add_status(self, name, status, measured=None, threshold=None, evidence="", note=""):
        self.rows.append(GateRow(name, status, measured, threshold, evidence, note))

    @property
    def status(self) -> str:
        st = [r.status for r in self.rows]
        if not st or any(s == "NOT RUN" for s in st):
            return "PARTIAL" if any(s == "PASS" for s in st) else "NOT RUN"
        if all(s == "PASS" for s in st):
            return "PASS"
        if any(s == "FAIL" for s in st):
            return "FAIL"
        return "PARTIAL"


def load_thresholds(path: str | Path = "configs/gates.yaml") -> dict:
    return yaml.safe_load(Path(path).read_text())


def write_gate(res: GateResult, evidence_dir: str | Path = "evidence") -> Path:
    evidence_dir = Path(evidence_dir)
    gdir = evidence_dir / res.gate
    gdir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    p = gdir / f"{stamp}.json"
    p.write_text(json.dumps({"gate": res.gate, "status": res.status, "started_utc": res.started_utc,
                             "rows": [asdict(r) for r in res.rows]}, indent=2, default=str))
    ledger = evidence_dir / "GATE_LEDGER.md"
    lines = [f"\n## {res.gate} — {res.status} — {stamp}\n", "| row | status | measured | threshold | evidence | note |", "|---|---|---|---|---|---|"]
    for r in res.rows:
        lines.append(f"| {r.name} | {r.status} | {_fmt(r.measured)} | {_fmt(r.threshold)} | {r.evidence} | {r.note} |")
    with open(ledger, "a") as f:
        f.write("\n".join(lines) + "\n")
    return p


def _fmt(x) -> str:
    if isinstance(x, float):
        return f"{x:.3g}"
    if isinstance(x, (list, tuple)):
        return ", ".join(_fmt(v) for v in x)
    if isinstance(x, dict):
        return "; ".join(f"{k}={_fmt(v)}" for k, v in x.items())
    return str(x)
