#!/usr/bin/env python3
"""
Comprehensive Routing Tree Demo

This demo showcases the new comprehensive routing tree that consolidates
all the different routing strategies and backends into a unified system.
"""

import sys
from pathlib import Path

# Add src to path for local development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from qiskit import QuantumCircuit
from qiskit.circuit.library import QuantumFourierTransform, EfficientSU2
from qiskit.quantum_info import random_clifford

from ariadne.route.routing_tree import (
    ComprehensiveRoutingTree,
    RoutingStrategy,
    explain_routing,
    show_routing_tree,
)


def create_test_circuits():
    """Create a variety of test circuits to demonstrate routing."""
    
    circuits = {}
    
    # 1. Small Clifford circuit (should go to Stim)
    clifford_qc = QuantumCircuit(5)
    clifford_qc.h(0)
    clifford_qc.cx(0, 1)
    clifford_qc.cx(1, 2)
    clifford_qc.cx(2, 3)
    clifford_qc.cx(3, 4)
    clifford_qc.h(4)
    circuits["Small Clifford (5 qubits)"] = clifford_qc
    
    # 2. Small general circuit (should go to hardware-optimized backend)
    small_qc = QuantumCircuit(8)
    small_qc.h(0)
    for i in range(7):
        small_qc.cx(i, i+1)
        small_qc.ry(0.5, i)
    circuits["Small General (8 qubits)"] = small_qc
    
    # 3. Medium low-entanglement circuit (should go to MPS)
    medium_low_ent = QuantumCircuit(25)
    for i in range(24):
        medium_low_ent.ry(0.1, i)
        medium_low_ent.cx(i, i+1)
    circuits["Medium Low-Entanglement (25 qubits)"] = medium_low_ent
    
    # 4. Medium high-entanglement circuit (should go to GPU if available)
    medium_high_ent = EfficientSU2(20, reps=3)
    circuits["Medium High-Entanglement (20 qubits)"] = medium_high_ent
    
    # 5. Large low-entanglement circuit (should go to MPS or fail gracefully)
    large_low_ent = QuantumCircuit(50)
    for i in range(49):
        large_low_ent.ry(0.05, i)
        large_low_ent.cx(i, i+1)
    circuits["Large Low-Entanglement (50 qubits)"] = large_low_ent
    
    # 6. Quantum Fourier Transform (structured circuit)
    qft = QuantumFourierTransform(12)
    circuits["QFT (12 qubits)"] = qft
    
    return circuits


def demonstrate_routing_strategies():
    """Demonstrate different routing strategies."""
    
    print("🌳 Ariadne Comprehensive Routing Tree Demo")
    print("=" * 50)
    
    # Initialize the routing tree
    tree = ComprehensiveRoutingTree()
    
    # Show the tree structure
    print("\n📊 Routing Tree Structure:")
    print(show_routing_tree())
    
    # Create test circuits
    circuits = create_test_circuits()
    
    print("\n🔄 Circuit Routing Demonstrations:")
    print("-" * 40)
    
    for name, circuit in circuits.items():
        print(f"\n🔍 {name}")
        print(f"   Qubits: {circuit.num_qubits}, Gates: {len(circuit)}, Depth: {circuit.depth()}")
        
        # Default routing
        decision = tree.route_circuit(circuit)
        print(f"   ✅ Default: {decision.backend.value} (confidence: {decision.confidence:.2f})")
        print(f"      Reason: {decision.reason}")
        
        # Try different strategies
        strategies_to_test = [
            RoutingStrategy.SPEED_FIRST,
            RoutingStrategy.MEMORY_EFFICIENT,
            RoutingStrategy.CLIFFORD_OPTIMIZED,
        ]
        
        for strategy in strategies_to_test:
            try:
                strategy_decision = tree.route_circuit(circuit, strategy)
                if strategy_decision.backend != decision.backend:
                    print(f"   🎯 {strategy.value}: {strategy_decision.backend.value} (confidence: {strategy_decision.confidence:.2f})")
                    print(f"      Reason: {strategy_decision.reason}")
            except Exception as e:
                print(f"   ⚠️  {strategy.value}: Error - {e}")
    
    print("\n📋 Detailed Routing Explanation Example:")
    print("-" * 40)
    
    # Pick one circuit for detailed explanation
    test_circuit = circuits["Medium High-Entanglement (20 qubits)"]
    explanation = explain_routing(test_circuit)
    print(explanation)
    
    print("\n🔧 Backend Availability:")
    print("-" * 25)
    for backend, available in tree.backend_availability.items():
        status = "✅ Available" if available else "❌ Not Available"
        print(f"{backend.value:15} : {status}")
    
    print("\n🎯 Routing Strategies Available:")
    print("-" * 30)
    for strategy in RoutingStrategy:
        print(f"• {strategy.value:25} : {strategy.name}")


def test_specific_scenarios():
    """Test specific routing scenarios."""
    
    print("\n🧪 Specific Scenario Tests:")
    print("-" * 30)
    
    tree = ComprehensiveRoutingTree()
    
    # Test 1: Pure Clifford should always prefer Stim
    clifford_circuit = QuantumCircuit(10)
    clifford_circuit.h(0)
    for i in range(9):
        clifford_circuit.cx(i, i+1)
    clifford_circuit.h(9)
    
    clifford_decision = tree.route_circuit(clifford_circuit, RoutingStrategy.CLIFFORD_OPTIMIZED)
    print(f"✅ Clifford Test: {clifford_decision.backend.value} (expected: stim)")
    
    # Test 2: Large low-entanglement should prefer MPS
    large_circuit = QuantumCircuit(40)
    for i in range(39):
        large_circuit.ry(0.1, i)
        large_circuit.cx(i, i+1)
    
    large_decision = tree.route_circuit(large_circuit, RoutingStrategy.MEMORY_EFFICIENT)
    print(f"✅ Large Low-Ent Test: {large_decision.backend.value} (expected: mps or tensor_network)")
    
    # Test 3: Hardware-specific routing
    small_circuit = QuantumCircuit(5)
    small_circuit.h(0)
    small_circuit.cx(0, 1)
    small_circuit.ry(0.5, 2)
    
    apple_decision = tree.route_circuit(small_circuit, RoutingStrategy.APPLE_SILICON_OPTIMIZED)
    cuda_decision = tree.route_circuit(small_circuit, RoutingStrategy.CUDA_OPTIMIZED)
    
    print(f"✅ Apple Silicon Test: {apple_decision.backend.value}")
    print(f"✅ CUDA Test: {cuda_decision.backend.value}")


def main():
    """Main demo function."""
    try:
        demonstrate_routing_strategies()
        test_specific_scenarios()
        
        print("\n🎉 Comprehensive Routing Tree Demo Complete!")
        print("\nKey Benefits:")
        print("• ✅ Unified routing across all backends")
        print("• ✅ Intelligent circuit analysis and classification")
        print("• ✅ Hardware-aware optimization")
        print("• ✅ Strategy-based routing options")
        print("• ✅ Graceful fallbacks and error handling")
        print("• ✅ Detailed explanations and transparency")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running from the correct directory with Ariadne installed")
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()