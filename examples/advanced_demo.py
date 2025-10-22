#!/usr/bin/env python3
"""
Ariadne Advanced Demo

This script demonstrates some of the more advanced features of Ariadne,
including forcing backends, using different routing strategies, and exploring
the educational tools.
"""

from qiskit import QuantumCircuit
from ariadne import simulate, explain_routing, show_routing_tree
from ariadne.education import InteractiveCircuitBuilder, AlgorithmExplorer
from ariadne.enhanced_benchmarking import EnhancedBenchmarkSuite

def main() -> None:
    """Ariadne advanced demo."""

    print("=== Ariadne Advanced Demo ===\n")

    # --- Backend Override ---
    print("1. Forcing a specific backend...")
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    result = simulate(qc, shots=1000, backend='qiskit')
    print(f"   - Forced backend: {result.backend_used}")

    # --- Routing Strategies ---
    print("\n2. Using a different routing strategy...")
    from ariadne import ComprehensiveRoutingTree, RoutingStrategy

    router = ComprehensiveRoutingTree()
    decision = router.route_circuit(qc, strategy=RoutingStrategy.MEMORY_EFFICIENT)
    print(f"   - Strategy: {RoutingStrategy.MEMORY_EFFICIENT.name}")
    print(f"   - Recommended Backend: {decision.recommended_backend}")

    # --- Educational Tools ---
    print("\n3. Exploring educational tools...")

    # Interactive Circuit Builder
    builder = InteractiveCircuitBuilder(2, "Bell State")
    builder.add_hadamard(0, "Create Superposition", "Apply H gate to qubit 0")
    builder.add_cnot(0, 1, "Create Entanglement", "Apply CNOT to entangle qubits")
    print("   - Interactive circuit builder created a Bell state circuit:")
    print(builder.get_circuit().draw())

    # Algorithm Explorer
    explorer = AlgorithmExplorer()
    algorithms = explorer.list_algorithms()
    print(f"   - Available algorithms: {algorithms[:5]}...")
    info = explorer.get_algorithm_info('bell')
    print(f"   - Info for 'bell' algorithm: {info['metadata'].description}")

    # --- Benchmarking ---
    print("\n4. Running a performance benchmark...")
    suite = EnhancedBenchmarkSuite()
    comparison = suite.benchmark_backend_comparison(
        algorithm_name='bell',
        qubit_count=2,
        backends=['auto', 'qiskit', 'stim'],
        shots=1000
    )

    for backend, result in comparison.items():
        if result.counts:
            print(f"   - {backend}: {result.execution_time:.4f}s")

if __name__ == "__main__":
    main()
