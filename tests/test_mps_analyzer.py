from __future__ import annotations

from collections.abc import Callable

from qiskit import QuantumCircuit

from ariadne.route.mps_analyzer import should_use_mps


def _apply_nearest_neighbor_layers(circuit: QuantumCircuit, gate_name: str, cycles: int) -> None:
    """Apply staggered nearest-neighbor gates for a specified number of cycles."""
    method: Callable[[int, int], QuantumCircuit] = getattr(circuit, gate_name)
    for _ in range(cycles):
        for start in (0, 1):
            for qubit in range(start, circuit.num_qubits - 1, 2):
                method(qubit, qubit + 1)


def _grid_connectivity_circuit(rows: int, cols: int) -> QuantumCircuit:
    """Return a circuit with 2D grid connectivity using nearest-neighbor CX gates."""
    total_qubits = rows * cols
    qc = QuantumCircuit(total_qubits)

    def idx(r: int, c: int) -> int:
        return r * cols + c

    for r in range(rows):
        for c in range(cols):
            node = idx(r, c)
            if c + 1 < cols:
                qc.cx(node, idx(r, c + 1))
            if r + 1 < rows:
                qc.cx(node, idx(r + 1, c))
    return qc


def test_mps_analyzer_grid_topology() -> None:
    """MPS analyzer should accept shallow grid-like circuits."""
    grid_circuit = _grid_connectivity_circuit(4, 4)
    assert should_use_mps(grid_circuit) is True


def test_mps_analyzer_weighted_entanglement() -> None:
    """Heavier entangling gates should eventually exceed the heuristic threshold."""
    light_circuit = QuantumCircuit(12)
    _apply_nearest_neighbor_layers(light_circuit, "cx", cycles=8)
    assert should_use_mps(light_circuit) is True

    heavy_circuit = QuantumCircuit(12)
    _apply_nearest_neighbor_layers(heavy_circuit, "swap", cycles=8)
    assert should_use_mps(heavy_circuit) is False
