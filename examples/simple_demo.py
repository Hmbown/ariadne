#!/usr/bin/env python3
"""SIMPLE DEMO: See Ariadne's intelligent routing in action."""

from __future__ import annotations

from qiskit import QuantumCircuit

from ariadne import QuantumRouter, simulate
from ariadne.route.analyze import analyze_circuit


def main() -> None:
    print("🔮 ARIADNE: Intelligent Quantum Router Demo")
    print("=" * 50)

    print("\n1️⃣ Creating Clifford circuit (30 qubits)...")
    qc = QuantumCircuit(30, 30)
    for idx in range(30):
        qc.h(idx)
        if idx < 29:
            qc.cx(idx, idx + 1)
    qc.measure_all()

    # Analyze circuit using the analyze_circuit function
    analysis = analyze_circuit(qc)

    # Get routing decision separately
    router = QuantumRouter()
    routing_decision = router.select_optimal_backend(qc)

    print("\n📊 Circuit Analysis:")
    print(f"  • Gate entropy: {analysis['gate_entropy']:.2f} bits")
    print(f"  • Is Clifford? {analysis.get('is_clifford', 'N/A')}")
    print(f"  • Recommended backend: {routing_decision.recommended_backend.value}")
    print(f"  • Expected speedup: {routing_decision.expected_speedup:.1f}x")

    print("\n2️⃣ Running simulation...")
    result = simulate(qc, shots=1000)
    print("  ✅ Simulation complete!")
    print(f"  Backend used: {result.backend_used.value}")
    print(f"  Time: {result.execution_time:.3f}s")
    print(f"  Shots: {result.metadata['shots']}")

    print("\n" + "=" * 50)
    print("🎯 Ariadne automatically chose the fastest backend!")
    print("Without Ariadne, you'd have to know this manually.")


if __name__ == "__main__":
    main()
