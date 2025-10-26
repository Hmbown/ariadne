"""
Test 2: Backend Equivalence Validation

This test verifies that different backends produce statistically equivalent
results for the same quantum circuit.
"""

import numpy as np
from qiskit import QuantumCircuit
from ariadne import simulate
from ariadne.types import BackendType
from scipy.stats import chisquare

print("=" * 80)
print("TEST 2: BACKEND EQUIVALENCE VALIDATION")
print("=" * 80)

def normalize_counts(counts, shots):
    """Convert counts dict to probability distribution."""
    return {k: v/shots for k, v in counts.items()}

def compare_distributions(dist1, dist2, name1, name2, tolerance=0.05):
    """
    Compare two probability distributions using chi-square test.
    Returns (are_equivalent, p_value, max_deviation)
    """
    # Get all bitstrings
    all_keys = set(dist1.keys()) | set(dist2.keys())

    probs1 = np.array([dist1.get(k, 0) for k in sorted(all_keys)])
    probs2 = np.array([dist2.get(k, 0) for k in sorted(all_keys)])

    # Calculate max deviation
    max_dev = np.max(np.abs(probs1 - probs2))

    # Chi-square test (if we have enough samples)
    try:
        # Need observed counts, so convert back
        obs1 = probs1 * 1000  # Assuming 1000 shots basis
        obs2 = probs2 * 1000
        chi2, p_value = chisquare(obs1 + 1e-10, obs2 + 1e-10)  # Add small value to avoid zeros
    except:
        p_value = 1.0  # If test fails, assume distributions are different

    are_equivalent = max_dev < tolerance

    print(f"    Comparing {name1} vs {name2}:")
    print(f"      Max deviation: {max_dev:.4f}")
    print(f"      P-value: {p_value:.4f}")
    print(f"      Status: {'✓ EQUIVALENT' if are_equivalent else '✗ DIFFERENT'} (tolerance={tolerance})")

    return are_equivalent, p_value, max_dev

# Test 2.1: Bell state on multiple backends
print("\n2.1: Bell State Equivalence Test")
print("-" * 80)

qc_bell = QuantumCircuit(2, 2)
qc_bell.h(0)
qc_bell.cx(0, 1)
qc_bell.measure([0, 1], [0, 1])

shots = 2000

# Test on available backends
backends_to_test = [
    BackendType.QISKIT,
]

# Check for Stim (Clifford circuits)
try:
    result_stim = simulate(qc_bell, shots=shots, backend=BackendType.STIM)
    backends_to_test.append(BackendType.STIM)
except Exception as e:
    print(f"  Stim not available: {e}")

# Check for CUDA
try:
    result_cuda = simulate(qc_bell, shots=shots, backend=BackendType.CUDA)
    backends_to_test.append(BackendType.CUDA)
except Exception as e:
    print(f"  CUDA not available: {e}")

# Run simulations
results = {}
for backend in backends_to_test:
    try:
        result = simulate(qc_bell, shots=shots, backend=backend)
        results[backend] = result
        print(f"\n  {backend.value}: {result.counts}")
    except Exception as e:
        print(f"\n  {backend.value}: FAILED - {e}")

# Compare all pairs
print("\n  Statistical Comparison:")
equivalent_count = 0
total_comparisons = 0

backend_list = list(results.keys())
for i in range(len(backend_list)):
    for j in range(i+1, len(backend_list)):
        b1, b2 = backend_list[i], backend_list[j]
        dist1 = normalize_counts(results[b1].counts, shots)
        dist2 = normalize_counts(results[b2].counts, shots)

        are_eq, p_val, max_dev = compare_distributions(
            dist1, dist2, b1.value, b2.value, tolerance=0.1  # 10% tolerance for shot noise
        )

        if are_eq:
            equivalent_count += 1
        total_comparisons += 1

print(f"\n  Results: {equivalent_count}/{total_comparisons} pairs are equivalent")

# Test 2.2: GHZ state equivalence
print("\n\n2.2: GHZ State Equivalence Test")
print("-" * 80)

qc_ghz = QuantumCircuit(3, 3)
qc_ghz.h(0)
qc_ghz.cx(0, 1)
qc_ghz.cx(1, 2)
qc_ghz.measure([0, 1, 2], [0, 1, 2])

results_ghz = {}
for backend in backends_to_test:
    try:
        result = simulate(qc_ghz, shots=shots, backend=backend)
        results_ghz[backend] = result
        print(f"\n  {backend.value}: {result.counts}")
    except Exception as e:
        print(f"\n  {backend.value}: FAILED - {e}")

print("\n  Statistical Comparison:")
equivalent_count_ghz = 0
total_comparisons_ghz = 0

backend_list_ghz = list(results_ghz.keys())
for i in range(len(backend_list_ghz)):
    for j in range(i+1, len(backend_list_ghz)):
        b1, b2 = backend_list_ghz[i], backend_list_ghz[j]
        dist1 = normalize_counts(results_ghz[b1].counts, shots)
        dist2 = normalize_counts(results_ghz[b2].counts, shots)

        are_eq, p_val, max_dev = compare_distributions(
            dist1, dist2, b1.value, b2.value, tolerance=0.1
        )

        if are_eq:
            equivalent_count_ghz += 1
        total_comparisons_ghz += 1

print(f"\n  Results: {equivalent_count_ghz}/{total_comparisons_ghz} pairs are equivalent")

# Test 2.3: Superposition + Measurement
print("\n\n2.3: Uniform Superposition Equivalence")
print("-" * 80)

qc_superposition = QuantumCircuit(4, 4)
for i in range(4):
    qc_superposition.h(i)
qc_superposition.measure([0, 1, 2, 3], [0, 1, 2, 3])

results_super = {}
for backend in backends_to_test:
    try:
        result = simulate(qc_superposition, shots=shots, backend=backend)
        results_super[backend] = result

        # Check uniformity (all 16 outcomes should be roughly equal)
        expected_prob = 1/16
        actual_probs = normalize_counts(result.counts, shots)
        max_deviation = max(abs(actual_probs.get(f"{i:04b}", 0) - expected_prob)
                           for i in range(16))

        print(f"\n  {backend.value}:")
        print(f"    Outcomes observed: {len(result.counts)}/16")
        print(f"    Max deviation from uniform: {max_deviation:.4f}")
        print(f"    Status: {'✓ UNIFORM' if max_deviation < 0.05 else '✗ NOT UNIFORM'}")

        results_super[backend] = result
    except Exception as e:
        print(f"\n  {backend.value}: FAILED - {e}")

# Test 2.4: Deterministic circuit (should give exact same result)
print("\n\n2.4: Deterministic Circuit (X gates only)")
print("-" * 80)

qc_deterministic = QuantumCircuit(3, 3)
qc_deterministic.x(0)
qc_deterministic.x(1)
# Qubit 2 stays in |0>
qc_deterministic.measure([0, 1, 2], [0, 1, 2])

results_det = {}
all_match = True

for backend in backends_to_test:
    try:
        result = simulate(qc_deterministic, shots=shots, backend=backend)
        results_det[backend] = result

        # Should only see "011" (LSB first in Qiskit)
        expected_outcome = "011"
        actual_counts = result.counts

        print(f"\n  {backend.value}:")
        print(f"    Result: {actual_counts}")

        if len(actual_counts) == 1 and expected_outcome in actual_counts:
            print(f"    ✓ CORRECT (deterministic {expected_outcome})")
        else:
            print(f"    ✗ INCORRECT (expected only {expected_outcome})")
            all_match = False

    except Exception as e:
        print(f"\n  {backend.value}: FAILED - {e}")
        all_match = False

# Overall Results
print("\n\n" + "=" * 80)
print("TEST 2 OVERALL RESULTS")
print("=" * 80)

total_equiv = equivalent_count + equivalent_count_ghz
total_comps = total_comparisons + total_comparisons_ghz

if total_comps > 0:
    equiv_rate = 100 * total_equiv / total_comps
else:
    equiv_rate = 0

print(f"\nStatistical Equivalence: {total_equiv}/{total_comps} = {equiv_rate:.1f}%")
print(f"Deterministic Test: {'✓ PASSED' if all_match else '✗ FAILED'}")

if equiv_rate >= 80 and all_match:
    print("\n✓ TEST 2: PASSED - Backends produce equivalent results")
else:
    print("\n✗ TEST 2: FAILED - Backends show significant differences")

print("\nNOTE: Some variation is expected due to:")
print("  - Shot noise (statistical sampling)")
print("  - Different RNG implementations")
print("  - Numerical precision differences")
print("  - Acceptable tolerance: ±10% for probabilistic outcomes")

print("=" * 80)
