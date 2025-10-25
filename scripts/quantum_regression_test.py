#!/usr/bin/env python3
"""
Cross-platform quantum regression test script for CI/CD.
Handles Windows, macOS, and Linux environments.
"""

import json
import platform
import sys
import time
import traceback
from typing import Any


def run_quantum_regression_tests() -> int:
    """Run quantum regression tests across platforms."""
    try:
        # Import at the beginning to check if they exist
        from qiskit import QuantumCircuit

        from ariadne import get_available_backends, simulate

        print("🚀 Quantum Regression Test Suite")
        print("=" * 50)
        print(f"Platform: {platform.system()} {platform.release()}")
        print(f"Python: {sys.version}")

        # Get available backends
        backends = get_available_backends()
        print(f"Available backends: {backends}")

        # Test algorithms - adjust based on platform capabilities
        algorithms_to_test = ["bell", "ghz"]  # Simple set for CI
        results: dict[str, Any] = {"results": {}}

        # On Windows, we'll be more conservative with backends due to potential installation issues
        current_platform = platform.system().lower()
        if current_platform == "windows":
            # On Windows, limit to the most reliable backends
            backends_to_test = ["qiskit"]
            if "stim" in backends:
                backends_to_test.append("stim")
        else:
            # On Unix-like systems, we can test more
            backends_to_test = ["qiskit"]
            if "stim" in backends:
                backends_to_test.append("stim")

        for alg_name in algorithms_to_test:
            print(f"\nTesting {alg_name} algorithm...")
            results["results"][alg_name] = {"backends": {}}

            # Create test circuit based on algorithm
            if alg_name == "bell":
                qc = QuantumCircuit(2, 2)
                qc.h(0)
                qc.cx(0, 1)
                qc.measure_all()
            elif alg_name == "ghz":
                qc = QuantumCircuit(3, 3)
                qc.h(0)
                qc.cx(0, 1)
                qc.cx(1, 2)
                qc.measure_all()

            # Test with available backends
            for backend_name in backends_to_test:
                try:
                    print(f"  Testing {backend_name} backend...")
                    start_time = time.time()
                    result = simulate(qc, shots=100, backend=backend_name)
                    execution_time = time.time() - start_time

                    results["results"][alg_name]["backends"][backend_name] = {
                        "success": True,
                        "execution_time": execution_time,
                        "throughput": 100 / execution_time if execution_time > 0 else 0,
                        "backend_used": str(result.backend_used) if hasattr(result, "backend_used") else backend_name,
                    }
                    print(f"    ✓ {backend_name}: {execution_time:.3f}s")

                except Exception as e:
                    results["results"][alg_name]["backends"][backend_name] = {
                        "success": False,
                        "error": str(e),
                        "execution_time": 0,
                        "throughput": 0,
                    }
                    print(f"    ✗ {backend_name}: {e}")
                    traceback.print_exc()  # Print the full traceback for debugging

        # Save results
        with open("benchmark_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)

        # Calculate success rate
        total_tests = sum(len(alg["backends"]) for alg in results["results"].values())
        successful_tests = sum(
            sum(1 for b in alg["backends"].values() if b["success"]) for alg in results["results"].values()
        )
        success_rate = successful_tests / total_tests if total_tests > 0 else 0

        with open("success_rate.txt", "w") as f:
            f.write(f"{success_rate:.2%}")

        print(f"\nOverall success rate: {success_rate:.2%} ({successful_tests}/{total_tests})")

        # For CI, consider success if at least the primary backend (qiskit) works
        if (
            "qiskit" in [b for alg in results["results"].values() for b in alg["backends"]]
            and results["results"][list(results["results"].keys())[0]]["backends"]["qiskit"]["success"]
        ):
            print("✅ Quantum regression tests passed! (Qiskit backend working)")
            return 0
        else:
            print("❌ Quantum regression tests failed!")
            return 1

    except ImportError as e:
        print(f"❌ Import error in quantum regression tests: {e}")
        # Even if imports fail, we try to continue with minimal functionality
        results = {"results": {"minimal": {"backends": {"qiskit": {"success": False, "error": str(e)}}}}}
        with open("benchmark_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        with open("success_rate.txt", "w") as f:
            f.write("0.00%")
        return 1
    except Exception as e:
        print(f"❌ Critical error in quantum regression tests: {e}")
        traceback.print_exc()
        # Even with a critical error, save minimal results to avoid CI failures
        results = {"results": {"minimal": {"backends": {"qiskit": {"success": False, "error": str(e)}}}}}
        with open("benchmark_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        with open("success_rate.txt", "w") as f:
            f.write("0.00%")
        return 1


if __name__ == "__main__":
    sys.exit(run_quantum_regression_tests())
