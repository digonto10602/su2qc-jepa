"""Twin runner with reproducible, *independent* seeds.

Lesson from the v0.5.0 campaign: Aer seeds shot k of a run with seed_simulator + k, so runs
seeded with seed + k overlapped in N-1 of N shots and every quoted sigma was void.  Here every
run gets its own seed from ``numpy.random.SeedSequence(master).spawn(...)``, and the variance
check (``twin_variance_check``) asserts that repeats are distinct.
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from ..data.records import Record
from ..physics.chain import ChainSpec, build_chain_circuit

__all__ = ["TwinRunner", "twin_variance_check", "chain_point_records"]


@dataclass
class TwinRunner:
    noise_model: object
    method: str = "density_matrix"
    master_seed: int = 20261005
    basis_gates: tuple[str, ...] = ("cz", "rz", "sx", "x")
    device: str = "CPU"  # 'GPU' with qiskit-aer-gpu
    _counter: int = field(default=0, init=False)

    def _sim(self):
        from qiskit_aer import AerSimulator

        kw = {"method": self.method, "noise_model": self.noise_model}
        if self.device == "GPU":
            kw["device"] = "GPU"
        return AerSimulator(**kw)

    def seeds(self, n: int, salt: str = "") -> list[int]:
        """n independent 31-bit seeds derived from the master seed and a salt (e.g. the run name)."""
        h = int(hashlib.sha256(salt.encode()).hexdigest(), 16) % (2**32)
        ss = np.random.SeedSequence([self.master_seed, h])
        return [int(c.generate_state(1)[0] % (2**31 - 1)) for c in ss.spawn(n)]

    def run(self, circuits: list, shots: int, salt: str, line: list[int] | None = None) -> list[dict[str, int]]:
        from qiskit import transpile
        from qiskit.transpiler import CouplingMap

        sim = self._sim()
        K = circuits[0].num_qubits
        cm = CouplingMap.from_line(K) if line is None else CouplingMap([[a, b] for a, b in zip(line[:-1], line[1:])] + [[b, a] for a, b in zip(line[:-1], line[1:])])
        tq = transpile(circuits, basis_gates=list(self.basis_gates), coupling_map=cm, optimization_level=1,
                       seed_transpiler=self.master_seed, initial_layout=line)
        out = []
        for qc, seed in zip(tq, self.seeds(len(tq), salt)):
            res = sim.run(qc, shots=shots, seed_simulator=seed).result()
            out.append(dict(res.get_counts()))
        return out


def chain_point_records(runner: TwinRunner, spec: ChainSpec, shots: int, settings=("Z", "X"), salt: str = "", source: str = "twin",
                        meta: dict | None = None) -> list[Record]:
    circs = [build_chain_circuit(spec, s) for s in settings]
    counts = runner.run(circs, shots, salt=salt or f"{spec}")
    return [Record(s, c, shots, source, "chain", dict(meta or {}, setting=s, cz=None)) for s, c in zip(settings, counts)]


def twin_variance_check(runner: TwinRunner, spec: ChainSpec, shots: int = 1024, repeats: int = 5, out: str | Path | None = None) -> dict:
    """Repeat one Z-setting circuit with spawned seeds; all count dictionaries must differ."""
    circ = build_chain_circuit(spec, "Z")
    t0 = time.time()
    counts = [runner.run([circ], shots, salt=f"variance-{r}")[0] for r in range(repeats)]
    hashes = [hashlib.sha256(json.dumps(c, sort_keys=True).encode()).hexdigest() for c in counts]
    distinct = len(set(hashes))
    pops = []
    for c in counts:
        tot = sum(c.values())
        p1 = sum(n for k, n in c.items() if k.count("1") == 1) / tot
        pops.append(p1)
    result = {"repeats": repeats, "distinct_count_dicts": distinct, "pass": distinct == repeats,
              "single_excitation_fraction": pops, "sigma": float(np.std(pops, ddof=1)) if repeats > 1 else None,
              "wall_seconds": round(time.time() - t0, 2), "hashes": hashes}
    if out:
        Path(out).write_text(json.dumps(result, indent=2))
    return result
