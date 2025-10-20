#!/usr/bin/env python3
"""
Ariadne Quickstart Example

This example demonstrates the basic usage of Ariadne's intelligent routing
with the specific examples highlighted in the README.
"""

from qiskit import QuantumCircuit

from ariadne import explain_routing, show_routing_tree, simulate


def main() -> None:
    print("=== Ariadne: 'Google Maps' for Quantum Circuits ===\n")

    # Example 1: The 40-qubit GHZ from README (demonstrates Stim routing)
    print("1. Large Clifford Circuit (40-qubit GHZ) → Expected: Stim")
    print("   (This would crash regular Qiskit but Ariadne routes to Stim)")

    qc_large = QuantumCircuit(40, 40)
    qc_large.h(0)
    for i in range(39):
        qc_large.cx(i, i + 1)
    qc_large.measure_all()

    result = simulate(qc_large, shots=1000)
    print(f"   Backend used: {result.backend_used}")
    print(f"   Execution time: {result.execution_time:.4f}s")
    print(f"   Sample counts: {dict(list(result.counts.items())[:3])}")
    print()

    # Example 2: Low-entanglement circuit (should route to MPS/TN)
    print("2. Low-Entanglement Circuit → Expected: MPS/TN")

    qc_low_ent = QuantumCircuit(8, 8)
    # Create a low-entanglement circuit
    for i in range(8):
        qc_low_ent.h(i)
    # Only a few entangling gates
    qc_low_ent.cx(0, 1)
    qc_low_ent.cx(2, 3)
    qc_low_ent.measure_all()

    result = simulate(qc_low_ent, shots=1000)
    print(f"   Backend used: {result.backend_used}")
    print(f"   Execution time: {result.execution_time:.4f}s")
    print()

    # Example 3: General circuit (fallback to Aer CPU)
    print("3. General Circuit with T Gates → Expected: Qiskit/Aer")

    qc_general = QuantumCircuit(3, 3)
    qc_general.h(0)
    qc_general.t(1)  # T gate makes it non-Clifford
    qc_general.cx(0, 1)
    qc_general.cx(1, 2)
    qc_general.measure_all()

    result = simulate(qc_general, shots=1000)
    print(f"   Backend used: {result.backend_used}")
    print(f"   Execution time: {result.execution_time:.4f}s")
    print()

    # Example 4: Routing explanations (key differentiator)
    print("4. Transparent Routing Decisions")
    print("   Clifford circuit analysis:")
    explanation = explain_routing(qc_large)
    print(f"   {explanation}")
    print()

    print("   General circuit analysis:")
    explanation = explain_routing(qc_general)
    print(f"   {explanation}")
    print()

    # Example 5: Routing tree visualization
    print("5. Ariadne's Routing Tree:")
    print(show_routing_tree())
    print()

    # Example 6: Force specific backend (when you need override)
    print("6. Backend Override Examples")

    # Simple Bell state for quick tests
    bell = QuantumCircuit(2, 2)
    bell.h(0)
    bell.cx(0, 1)
    bell.measure_all()

    result_qiskit = simulate(bell, shots=100, backend="qiskit")
    print(f"   Forced Qiskit: {result_qiskit.backend_used}")

    # Try other backends if available
    try:
        result_stim = simulate(bell, shots=100, backend="stim")
        print(f"   Forced Stim: {result_stim.backend_used}")
    except Exception:
        print("   Stim backend not available for this circuit type")

    try:
        result_mps = simulate(bell, shots=100, backend="mps")
        print(f"   Forced MPS: {result_mps.backend_used}")
    except Exception:
        print("   MPS backend not available")

    try:
        result_metal = simulate(bell, shots=100, backend="jax_metal")
        print(f"   Forced JAX-Metal: {result_metal.backend_used}")
    except Exception:
        print("   JAX-Metal backend not available (Apple Silicon only)")

    print("\n=== Key Takeaways ===")
    print("✓ Ariadne automatically routes to optimal backends")
    print("✓ Large Clifford circuits → Stim (would crash regular Qiskit)")
    print("✓ Low-entanglement circuits → MPS/TN for efficiency")
    print("✓ General circuits → Reliable Qiskit fallback")
    print("✓ Complete transparency with explain_routing()")
    print("✓ Cross-ecosystem routing (not just within Aer)")

    print("\n🎯 Next Steps:")
    print("• Try: ariadne simulate your_circuit.qasm --shots 1000")
    print("• Try: ariadne benchmark-suite --algorithms qft,grover,qpe")
    print("• Try: ariadne status --detailed")
    print("• Explore: examples/ directory for more demos")


if __name__ == "__main__":
    main()
