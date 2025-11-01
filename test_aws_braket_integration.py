#!/usr/bin/env python3
"""
Test script to verify AWS Braket backend integration with Ariadne.
"""

import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

try:
    from qiskit import QuantumCircuit

    from ariadne.backends.braket_backend import is_aws_braket_available
    from ariadne.backends.universal_interface import get_backend_manager
    from ariadne.router import simulate
    # from ariadne.types import BackendType

    print("Testing AWS Braket Backend Integration")
    print("=" * 50)

    # Test 1: Check if AWS Braket is available
    print("\n1. Checking AWS Braket availability...")
    available = is_aws_braket_available()
    print(f"   AWS Braket available: {available}")

    # Test 2: Check if backend is registered
    print("\n2. Checking backend registration...")
    manager = get_backend_manager()
    available_backends = manager.list_available_backends()
    print(f"   Available backends: {available_backends}")
    print(f"   AWS Braket in list: {'aws_braket' in available_backends}")

    # Test 3: Try to create backend instance
    print("\n3. Creating AWS Braket backend instance...")
    try:
        backend = manager.get_backend("aws_braket")
        if backend:
            print("   ✓ AWS Braket backend created successfully")
            print(f"   Backend info: {backend.get_backend_info()}")
        else:
            print("   ✗ Failed to create AWS Braket backend")
    except Exception as e:
        print(f"   ✗ Error creating backend: {e}")

    # Test 4: Try to simulate a simple circuit
    print("\n4. Testing circuit simulation...")
    try:
        # Create a simple Bell state circuit
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure_all()

        print(f"   Circuit: {qc.num_qubits} qubits, {qc.depth()} depth")

        # Try simulation with AWS Braket backend
        result = simulate(qc, shots=100, backend="aws_braket")
        print("   ✓ Simulation successful")
        print(f"   Backend used: {result.backend_used}")
        print(f"   Execution time: {result.execution_time:.4f}s")
        print(f"   Counts: {result.counts}")

        # Check for fallback
        if result.fallback_reason:
            print(f"   Fallback reason: {result.fallback_reason}")

    except Exception as e:
        print(f"   ✗ Simulation failed: {e}")

    # Test 5: Test backend capabilities
    print("\n5. Testing backend capabilities...")
    try:
        backend = manager.get_backend("aws_braket")
        if backend:
            capabilities = backend.get_capabilities()
            print(f"   Capabilities: {[cap.value for cap in capabilities]}")

            metrics = backend.get_metrics()
            print(f"   Max qubits: {metrics.max_qubits}")
            print(f"   Speed rating: {metrics.speed_rating}")
            print(f"   Accuracy rating: {metrics.accuracy_rating}")

            # Test circuit compatibility
            can_sim, reason = backend.can_simulate(qc)
            print(f"   Can simulate test circuit: {can_sim}")
            if not can_sim:
                print(f"   Reason: {reason}")

    except Exception as e:
        print(f"   ✗ Error testing capabilities: {e}")

    print("\n" + "=" * 50)
    print("AWS Braket backend integration test completed!")

except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all required modules are installed and accessible.")
    sys.exit(1)

except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit(1)
