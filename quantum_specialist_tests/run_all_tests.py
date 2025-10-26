"""
Master Test Runner for Quantum Specialist Validation

Runs all comprehensive tests and generates a summary report.
"""

import subprocess
import sys
import time
from datetime import datetime

print("=" * 80)
print("ARIADNE QUANTUM SPECIALIST COMPREHENSIVE TEST SUITE")
print("=" * 80)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

tests = [
    ("Test 1: Clifford Detection", "test_1_clifford_detection.py"),
    ("Test 2: Backend Equivalence", "test_2_backend_equivalence.py"),
    ("Test 3: Edge Cases", "test_3_edge_cases.py"),
    ("Test 4: Performance Benchmarks", "test_4_performance_benchmarks.py"),
    ("Test 5: Real Algorithms", "test_5_real_algorithms.py"),
]

results = []
total_time = 0

for test_name, test_file in tests:
    print(f"\n\n{'='*80}")
    print(f"RUNNING: {test_name}")
    print(f"{'='*80}\n")

    start_time = time.time()

    try:
        result = subprocess.run(
            [sys.executable, test_file],
            cwd="/home/user/ariadne/quantum_specialist_tests",
            capture_output=False,
            text=True,
            timeout=600  # 10 minute timeout per test
        )

        elapsed = time.time() - start_time
        total_time += elapsed

        if result.returncode == 0:
            status = "✓ PASSED"
        else:
            status = "✗ FAILED"

        results.append((test_name, status, elapsed))

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        total_time += elapsed
        results.append((test_name, "✗ TIMEOUT", elapsed))
        print(f"\n✗ TEST TIMEOUT after {elapsed:.1f}s")

    except Exception as e:
        elapsed = time.time() - start_time
        total_time += elapsed
        results.append((test_name, f"✗ ERROR: {e}", elapsed))
        print(f"\n✗ TEST ERROR: {e}")

# Summary Report
print("\n\n" + "=" * 80)
print("COMPREHENSIVE TEST SUITE SUMMARY")
print("=" * 80)

print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Total execution time: {total_time:.1f}s ({total_time/60:.1f} minutes)")

print("\n" + "-" * 80)
print("Test Results:")
print("-" * 80)

passed = 0
failed = 0

for test_name, status, elapsed in results:
    print(f"  {status:15} {test_name:40} ({elapsed:.1f}s)")

    if "PASSED" in status:
        passed += 1
    else:
        failed += 1

total = len(results)
pass_rate = 100 * passed / total if total > 0 else 0

print("\n" + "-" * 80)
print(f"Overall: {passed}/{total} tests passed ({pass_rate:.1f}%)")
print("-" * 80)

if passed == total:
    print("\n✓ ALL TESTS PASSED")
    print("Ariadne has been validated by quantum specialist testing.")
elif pass_rate >= 80:
    print("\n⚠ MOST TESTS PASSED")
    print(f"{failed} test(s) failed. Review individual test output for details.")
else:
    print("\n✗ MULTIPLE TESTS FAILED")
    print("Significant issues found. Detailed review required.")

print("\n" + "=" * 80)
print("END OF TEST SUITE")
print("=" * 80)
