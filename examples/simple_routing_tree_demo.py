#!/usr/bin/env python3
"""
Simple Routing Tree Demo

Demonstrates the new comprehensive routing tree with simple examples.
"""

import sys
from pathlib import Path

# Add src to path for local development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from qiskit import QuantumCircuit

try:
    from ariadne import (
        ComprehensiveRoutingTree,
        RoutingStrategy,
        explain_routing,
        show_routing_tree,
        route_with_tree,
    )
    
    print("🌳 Ariadne Comprehensive Routing Tree Demo")
    print("=" * 45)
    
    # Show available routing strategies
    print("\n🎯 Available Routing Strategies:")
    for strategy in RoutingStrategy:
        print(f"  • {strategy.value}")
    
    print("\n📊 Routing Tree Structure (simplified):")
    print(show_routing_tree()[:1000] + "..." if len(show_routing_tree()) > 1000 else show_routing_tree())
    
    print("\n🔄 Routing Demonstrations:")
    print("-" * 30)
    
    # Create circuits here since functions aren't defined yet
    def create_clifford_circuit(num_qubits: int) -> QuantumCircuit:
        """Create a simple Clifford circuit."""
        qc = QuantumCircuit(num_qubits)
        qc.h(0)
        for i in range(num_qubits - 1):
            qc.cx(i, i + 1)
        return qc

    def create_general_circuit(num_qubits: int) -> QuantumCircuit:
        """Create a general quantum circuit."""
        qc = QuantumCircuit(num_qubits)
        qc.h(0)
        for i in range(num_qubits - 1):
            qc.cx(i, i + 1)
            qc.ry(0.5, i)
        return qc
    
    # Test circuits
    circuits = {
        "Small Clifford": create_clifford_circuit(5),
        "Small General": create_general_circuit(8),
        "Medium Circuit": create_general_circuit(20),
        "Large Circuit": create_general_circuit(40),
    }
    
    print("\n🔄 Routing Demonstrations:")
    print("-" * 30)
    
    for name, circuit in circuits.items():
        print(f"\n🔍 {name} ({circuit.num_qubits} qubits, {len(circuit)} gates)")
        
        # Test default routing
        decision = route_with_tree(circuit)
        print(f"   Default: {decision.recommended_backend.value} (confidence: {decision.confidence_score:.2f})")
        
        # Test specific strategies
        for strategy in [RoutingStrategy.SPEED_FIRST, RoutingStrategy.MEMORY_EFFICIENT]:
            try:
                strategy_decision = route_with_tree(circuit, strategy)
                if strategy_decision.recommended_backend != decision.recommended_backend:
                    print(f"   {strategy.value}: {strategy_decision.recommended_backend.value}")
            except Exception:
                pass
    
    print("\n📋 Detailed Explanation Example:")
    print("-" * 35)
    test_circuit = create_general_circuit(15)
    explanation = explain_routing(test_circuit)
    print(explanation[:800] + "..." if len(explanation) > 800 else explanation)
    
    print("\n✅ Routing tree is working and comprehensive!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Run this from the ariadne root directory")
except Exception as e:
    print(f"❌ Error: {e}")


def create_clifford_circuit(num_qubits: int) -> QuantumCircuit:
    """Create a simple Clifford circuit."""
    qc = QuantumCircuit(num_qubits)
    qc.h(0)
    for i in range(num_qubits - 1):
        qc.cx(i, i + 1)
    return qc


def create_general_circuit(num_qubits: int) -> QuantumCircuit:
    """Create a general quantum circuit."""
    qc = QuantumCircuit(num_qubits)
    qc.h(0)
    for i in range(num_qubits - 1):
        qc.cx(i, i + 1)
        qc.ry(0.5, i)
    return qc


if __name__ == "__main__":
    pass  # Code runs at import time for simplicity