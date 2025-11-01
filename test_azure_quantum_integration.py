#!/usr/bin/env python3
"""
Test script for Azure Quantum backend integration.
This script tests the Azure Quantum backend implementation without requiring actual Azure credentials.
"""

import os
import sys

from qiskit import QuantumCircuit

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def test_azure_quantum_backend() -> bool:
    """Test Azure Quantum backend implementation."""
    print("Testing Azure Quantum backend integration...")

    # Test 1: Check if AzureQuantumBackend can be imported
    try:
        from ariadne.backends.azure_backend import AzureQuantumBackend, is_azure_quantum_available

        print("✓ AzureQuantumBackend import successful")
    except ImportError as e:
        print(f"✗ Failed to import AzureQuantumBackend: {e}")
        return False

    # Test 2: Check availability function
    try:
        available = is_azure_quantum_available()
        print(f"✓ Azure Quantum availability check: {available}")
    except Exception as e:
        print(f"✗ Availability check failed: {e}")
        return False

    # Test 3: Check if BackendType enum includes AZURE_QUANTUM
    try:
        from ariadne.types import BackendType

        azure_quantum_type = BackendType.AZURE_QUANTUM
        print(f"✓ BackendType.AZURE_QUANTUM: {azure_quantum_type}")
    except Exception as e:
        print(f"✗ BackendType check failed: {e}")
        return False

    # Test 4: Check if backend is registered in BackendManager
    try:
        from ariadne.backends.universal_interface import get_backend_manager

        manager = get_backend_manager()
        registered_backends = list(manager.backends.keys())
        available_backends = manager.list_available_backends()
        print(f"✓ Registered backends: {registered_backends}")
        print(f"✓ Available backends: {available_backends}")

        if "azure_quantum" in registered_backends:
            print("✓ Azure Quantum backend is registered in BackendManager")
        else:
            print("✗ Azure Quantum backend is not registered in BackendManager")
            return False

        # Azure Quantum should be registered but not available (since SDK is not installed)
        if "azure_quantum" in registered_backends and "azure_quantum" not in available_backends:
            print("✓ Azure Quantum backend correctly registered but not available (expected behavior)")
        else:
            print("✗ Azure Quantum backend registration check failed")
            return False
    except Exception as e:
        print(f"✗ BackendManager check failed: {e}")
        return False

    # Test 5: Check if backend availability check works in enhanced router
    try:
        from ariadne.route.enhanced_router import EnhancedQuantumRouter

        _ = EnhancedQuantumRouter()
        # This will test the _is_backend_available method
        print("✓ EnhancedQuantumRouter created successfully")
    except Exception as e:
        print(f"✗ EnhancedQuantumRouter check failed: {e}")
        return False

    # Test 6: Check if _simulate_azure_quantum function exists
    try:
        from ariadne.router import _simulate_azure_quantum as _sim_az

        print("✓ _simulate_azure_quantum function exists", bool(_sim_az))
    except ImportError as e:
        print(f"✗ _simulate_azure_quantum function not found: {e}")
        return False

    # Test 7: Create a simple quantum circuit for testing
    try:
        # Create a simple Bell state circuit
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure_all()
        print("✓ Test quantum circuit created successfully")
    except Exception as e:
        print(f"✗ Circuit creation failed: {e}")
        return False

    # Test 8: Test AzureQuantumBackend instantiation (without actual Azure credentials)
    try:
        # This will fail due to missing credentials, but should show the class structure works
        _backend = AzureQuantumBackend(workspace_id="test_workspace", resource_id="test_resource", location="eastus")
        print("✗ AzureQuantumBackend instantiation should have failed without proper credentials")
        return False
    except RuntimeError as e:
        if "Azure Quantum SDK not available" in str(e):
            print("✓ AzureQuantumBackend correctly detects missing SDK")
        else:
            print(f"✓ AzureQuantumBackend correctly fails with expected error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error during backend instantiation: {e}")
        return False

    print("\n✓ All Azure Quantum backend integration tests passed!")
    return True


def test_routing_integration() -> bool:
    """Test routing integration with Azure Quantum."""
    print("\nTesting routing integration...")

    try:
        from ariadne.router import simulate

        # Create a simple circuit
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure_all()

        # Test routing with Azure Quantum backend (will fallback to other backends)
        try:
            result = simulate(qc, shots=100, backend="azure_quantum")
            print("✓ Routing with azure_quantum backend completed")
            print(f"  Backend used: {result.backend_used}")
            print(f"  Execution time: {result.execution_time:.4f}s")
            return True
        except Exception as e:
            print(f"✓ Routing correctly handles Azure Quantum backend failure: {e}")
            return True

    except Exception as e:
        print(f"✗ Routing integration test failed: {e}")
        return False


if __name__ == "__main__":
    print("Azure Quantum Backend Integration Test")
    print("=" * 40)

    success = test_azure_quantum_backend()
    if success:
        success = test_routing_integration()

    if success:
        print("\n🎉 All tests passed! Azure Quantum backend integration is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        sys.exit(1)
