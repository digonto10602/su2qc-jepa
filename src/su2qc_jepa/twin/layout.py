"""Choose the physical line of K qubits for the chain carrier from calibration data.

Score of a path = sum of CZ errors along its edges + sum of readout assignment errors of its
qubits (both are what the chain carrier is sensitive to).  Simple-path enumeration by DFS
with a cap, which is fine for K <= 16 on heavy-hex graphs of 127-156 qubits.
"""
from __future__ import annotations

import itertools

__all__ = ["best_line", "edge_errors_from_backend"]


def edge_errors_from_backend(backend) -> tuple[dict[tuple[int, int], float], dict[int, float], list[tuple[int, int]]]:
    """(two-qubit gate errors by edge, readout errors by qubit, edge list) from a qiskit-ibm-runtime backend."""
    target = backend.target
    edges, cz_err = [], {}
    for name in ("cz", "ecr", "cx"):
        if name in target.operation_names:
            for q, props in target[name].items():
                e = getattr(props, "error", None)
                if e is None:
                    continue
                edges.append(tuple(q))
                cz_err[tuple(q)] = float(e)
            break
    ro = {}
    if "measure" in target.operation_names:
        for q, props in target["measure"].items():
            ro[q[0]] = float(getattr(props, "error", 0.0) or 0.0)
    return cz_err, ro, edges


def best_line(edges: list[tuple[int, int]], cz_err: dict[tuple[int, int], float], ro_err: dict[int, float], K: int,
              max_paths: int = 200000) -> tuple[list[int], float]:
    """Best simple path of K qubits by total (CZ + readout) error. Returns (path, score)."""
    adj: dict[int, set[int]] = {}
    for a, b in edges:
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)

    def e(a, b):
        return cz_err.get((a, b), cz_err.get((b, a), 1.0))

    best, best_score = None, float("inf")
    count = 0
    for start in sorted(adj):
        stack = [([start], ro_err.get(start, 0.0))]
        while stack:
            path, score = stack.pop()
            count += 1
            if count > max_paths:
                return best or [], best_score
            if score >= best_score:
                continue
            if len(path) == K:
                best, best_score = path, score
                continue
            last = path[-1]
            for nb in adj[last]:
                if nb in path:
                    continue
                stack.append((path + [nb], score + e(last, nb) + ro_err.get(nb, 0.0)))
    return best or [], best_score


def heavy_hex_edges(n_rows: int = 2, n_cols: int = 4) -> list[tuple[int, int]]:
    """A tiny synthetic heavy-hex-like test graph (for unit tests only)."""
    edges = []
    n = n_rows * n_cols * 3
    for i in range(n - 1):
        edges.append((i, i + 1))
    for i, j in itertools.product(range(0, n, 6), range(1)):
        if i + 6 < n:
            edges.append((i, i + 6))
    return edges
