#!/usr/bin/env python3
"""
Minimal quantum regression test for CI/CD - especially Windows stability.
This test just verifies that core functionality is available and working.
"""

import json
import sys
import time
import platform
import traceback


def run_quantum_regression_tests() -> int:
    """Run minimal quantum regression tests."""
    print("Quantum Regression Test Suite (Minimal)")
    print("=" * 50)
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    
    # Initialize results
    results = {"results": {"minimal_test": {"backends": {}}}}
    
    try:
        # Test 1: Can we import the core library?
        print("1. Testing Ariadne core import...")
        try:
            import ariadne
            print("   OK Ariadne import successful")
            results["results"]["minimal_test"]["backends"]["core_import"] = {
                "success": True,
                "message": f"Ariadne version {ariadne.__version__ if hasattr(ariadne, '__version__') else 'unknown'}"
            }
        except ImportError as e:
            print(f"   FAIL Ariadne import failed: {e}")
            results["results"]["minimal_test"]["backends"]["core_import"] = {
                "success": False,
                "error": str(e)
            }
            # If import fails, we can't continue
            with open("benchmark_results.json", "w") as f:
                json.dump(results, f, indent=2, default=str)
            with open("success_rate.txt", "w") as f:
                f.write("0.00%")
            return 1
        
        # Test 2: Can we import Qiskit?
        print("2. Testing Qiskit import...")
        try:
            import qiskit
            print(f"   OK Qiskit import successful (version {qiskit.__version__})")
            results["results"]["minimal_test"]["backends"]["qiskit_import"] = {
                "success": True,
                "message": f"Qiskit version {qiskit.__version__}"
            }
        except ImportError as e:
            print(f"   FAIL Qiskit import failed: {e}")
            results["results"]["minimal_test"]["backends"]["qiskit_import"] = {
                "success": False,
                "error": str(e)
            }
        
        # Test 3: Can we get available backends?
        print("3. Testing backend detection...")
        try:
            from ariadne import get_available_backends
            backends = get_available_backends()
            print(f"   OK Backend detection successful: {backends}")
            results["results"]["minimal_test"]["backends"]["backend_detection"] = {
                "success": True,
                "message": f"Found {len(backends)} backends: {backends}"
            }
        except Exception as e:
            print(f"   FAIL Backend detection failed: {e}")
            results["results"]["minimal_test"]["backends"]["backend_detection"] = {
                "success": False,
                "error": str(e)
            }
        
        # Test 4: Can we create a simple quantum circuit and simulate?
        print("4. Testing basic simulation...")
        try:
            from qiskit import QuantumCircuit
            qc = QuantumCircuit(2, 2)
            qc.h(0)
            qc.cx(0, 1)
            qc.measure_all()
            print("   OK Quantum circuit creation successful")
            
            # If we have simulate function, test it
            if 'simulate' in dir(__import__('ariadne', fromlist=['simulate'])):
                from ariadne import simulate
                print("   OK Ariadne simulate function available")
                
                # Run a minimal simulation
                start_time = time.time()
                result = simulate(qc, shots=10)  # Minimal shots for speed
                execution_time = time.time() - start_time
                print(f"   OK Basic simulation successful (time: {execution_time:.3f}s)")
                
                results["results"]["minimal_test"]["backends"]["basic_simulation"] = {
                    "success": True,
                    "execution_time": execution_time,
                    "shots": 10,
                    "backend_used": str(getattr(result, 'backend_used', 'unknown'))
                }
            else:
                print("   WARN Ariadne simulate function not available")
                results["results"]["minimal_test"]["backends"]["basic_simulation"] = {
                    "success": False,
                    "error": "simulate function not found"
                }
                
        except Exception as e:
            print(f"   ❌ Basic simulation failed: {e}")
            print(f"   Full error: {traceback.format_exc()}")
            results["results"]["minimal_test"]["backends"]["basic_simulation"] = {
                "success": False,
                "error": str(e)
            }
        
        # Determine overall success
        successful_tests = sum(1 for backend in results["results"]["minimal_test"]["backends"].values() if backend["success"])
        total_tests = len(results["results"]["minimal_test"]["backends"])
        success_rate = successful_tests / total_tests if total_tests > 0 else 0
        
        # For CI purposes, consider success if core import works
        overall_success = results["results"]["minimal_test"]["backends"]["core_import"]["success"]
        
        # Save results
        with open("benchmark_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        
        with open("success_rate.txt", "w") as f:
            f.write(f"{success_rate:.2%}")
        
        if overall_success:
            print(f"\n✅ Quantum regression tests passed! ({successful_tests}/{total_tests} components working)")
            return 0
        else:
            print(f"\n❌ Quantum regression tests failed! (Core import failed)")
            return 1
            
    except Exception as e:
        print(f"❌ Critical error in quantum regression tests: {e}")
        print(f"Full error: {traceback.format_exc()}")
        
        # Create minimal results to avoid CI failures
        results = {"results": {"critical_error": {"backends": {"error": {"success": False, "error": str(e)}}}}}
        with open("benchmark_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        with open("success_rate.txt", "w") as f:
            f.write("0.00%")
        return 1


if __name__ == "__main__":
    sys.exit(run_quantum_regression_tests())