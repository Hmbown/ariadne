#!/usr/bin/env python3
"""
Ariadne Quickstart Example

This example demonstrates the basic usage of Ariadne's intelligent routing.
"""

from qiskit import QuantumCircuit
from ariadne import simulate, explain_routing

def main() -> None:
    """Ariadne quickstart demo."""

    print("=== Ariadne: The Google Maps of Quantum Simulation ===\n")

    # 1. Create a quantum circuit
    # This is a 40-qubit GHZ state, a type of stabilizer circuit.
    # Simulating this with a general-purpose simulator would be very slow.
    print("1. Creating a 40-qubit GHZ circuit...")
    qc = QuantumCircuit(40, 40)
    qc.h(0)
    for i in range(39):
        qc.cx(i, i + 1)
    qc.measure_all()
    print("   Circuit created.")

    # 2. Simulate the circuit with Ariadne
    # Ariadne will automatically choose the best backend for this circuit.
    print("\n2. Simulating the circuit with Ariadne...")
    result = simulate(qc, shots=1000)
    print("   Simulation complete.")

    # 3. See the results
    # Ariadne provides detailed information about the simulation.
    print("\n3. Simulation Results:")
    print(f"   - Backend Used: {result.backend_used}")
    print(f"   - Execution Time: {result.execution_time:.4f}s")

    # 4. Understand the routing decision
    # The `explain_routing` function tells you why Ariadne chose a particular backend.
    print("\n4. Routing Explanation:")
    explanation = explain_routing(qc)
    print(f"   - {explanation}")

    print("\n=== Key Takeaway ===")
    print("Ariadne automatically routed the large, complex circuit to the high-performance 'stim' backend, without any configuration from the user.")

    print("\nNext Steps:")
    print("- Try running this script with different circuits.")
    print("- Explore the USER_GUIDE.md for more advanced features.")

if __name__ == "__main__":
    main()
