"""
Test 1: Comprehensive Clifford Detection Validation

This test validates that Ariadne correctly identifies Clifford-only circuits
and routes them appropriately to the Stim backend.
"""

import time
from qiskit import QuantumCircuit
from ariadne import simulate
from ariadne.route.enhanced_router import EnhancedQuantumRouter
from ariadne.route.analyze import is_clifford_circuit, analyze_circuit
from ariadne.types import BackendType

router = EnhancedQuantumRouter()

print("=" * 80)
print("TEST 1: CLIFFORD DETECTION ACCURACY")
print("=" * 80)

# Test 1.1: Pure Clifford circuits should be detected
print("\n1.1: Testing Pure Clifford Circuits")
print("-" * 80)

pure_clifford_circuits = []

# Bell state (H + CNOT)
qc_bell = QuantumCircuit(2)
qc_bell.h(0)
qc_bell.cx(0, 1)
pure_clifford_circuits.append(("Bell State", qc_bell))

# Stabilizer preparation (H + S gates)
qc_stabilizer = QuantumCircuit(3)
qc_stabilizer.h(0)
qc_stabilizer.s(1)
qc_stabilizer.cx(0, 2)
qc_stabilizer.cz(1, 2)
pure_clifford_circuits.append(("Stabilizer State", qc_stabilizer))

# Complex Clifford circuit (many gates)
qc_complex_clifford = QuantumCircuit(5)
for i in range(5):
    qc_complex_clifford.h(i)
for i in range(4):
    qc_complex_clifford.cx(i, i+1)
    qc_complex_clifford.s(i)
qc_complex_clifford.sdg(4)
qc_complex_clifford.x(2)
qc_complex_clifford.y(3)
qc_complex_clifford.z(1)
qc_complex_clifford.swap(0, 4)
pure_clifford_circuits.append(("Complex Clifford", qc_complex_clifford))

# Surface code-like circuit
qc_surface = QuantumCircuit(9)
# Data qubits in grid
for i in range(0, 9, 3):
    qc_surface.h(i)
# Syndrome measurements
qc_surface.cx(0, 1)
qc_surface.cx(2, 1)
qc_surface.cx(3, 4)
qc_surface.cx(5, 4)
qc_surface.cx(6, 7)
qc_surface.cx(8, 7)
pure_clifford_circuits.append(("Surface Code Syndrome", qc_surface))

clifford_detection_passed = 0
clifford_detection_failed = 0
routing_stim_passed = 0
routing_stim_failed = 0

for name, circuit in pure_clifford_circuits:
    # Test detection
    is_cliff = is_clifford_circuit(circuit)

    # Test routing
    decision = router.select_optimal_backend(circuit, strategy="speed")

    print(f"\n  {name}:")
    print(f"    Qubits: {circuit.num_qubits}, Gates: {sum(1 for _ in circuit.data)}")
    print(f"    Detected as Clifford: {is_cliff}")
    print(f"    Routed to: {decision.recommended_backend.value}")
    print(f"    Confidence: {decision.confidence_score:.3f}")

    if is_cliff:
        clifford_detection_passed += 1
        print(f"    ✓ Clifford detection CORRECT")
    else:
        clifford_detection_failed += 1
        print(f"    ✗ Clifford detection FAILED (should be True)")

    if decision.recommended_backend == BackendType.STIM:
        routing_stim_passed += 1
        print(f"    ✓ Routing to Stim CORRECT")
    else:
        routing_stim_failed += 1
        print(f"    ✗ Routing FAILED (should route to Stim, got {decision.recommended_backend.value})")

print(f"\n  Summary:")
print(f"    Clifford Detection: {clifford_detection_passed}/{len(pure_clifford_circuits)} passed")
print(f"    Stim Routing: {routing_stim_passed}/{len(pure_clifford_circuits)} passed")

# Test 1.2: Non-Clifford circuits should NOT be detected as Clifford
print("\n\n1.2: Testing Non-Clifford Circuits (should NOT be Clifford)")
print("-" * 80)

non_clifford_circuits = []

# T gate (most common non-Clifford)
qc_t = QuantumCircuit(2)
qc_t.h(0)
qc_t.t(0)  # Non-Clifford!
qc_t.cx(0, 1)
non_clifford_circuits.append(("T Gate Circuit", qc_t))

# Toffoli gate
qc_toffoli = QuantumCircuit(3)
qc_toffoli.h(0)
qc_toffoli.ccx(0, 1, 2)  # Toffoli = non-Clifford
non_clifford_circuits.append(("Toffoli Circuit", qc_toffoli))

# Rotation gates
qc_rotation = QuantumCircuit(2)
qc_rotation.rx(0.5, 0)  # Arbitrary rotation
qc_rotation.ry(0.3, 1)
qc_rotation.cx(0, 1)
non_clifford_circuits.append(("Rotation Circuit", qc_rotation))

# Phase gate (not π/2)
qc_phase = QuantumCircuit(2)
qc_phase.h(0)
qc_phase.p(0.7, 0)  # Arbitrary phase
qc_phase.cx(0, 1)
non_clifford_circuits.append(("Phase Gate Circuit", qc_phase))

# U gate (general unitary)
qc_u = QuantumCircuit(1)
qc_u.u(0.1, 0.2, 0.3, 0)  # General unitary
non_clifford_circuits.append(("U Gate Circuit", qc_u))

# Mixed Clifford + non-Clifford
qc_mixed = QuantumCircuit(3)
qc_mixed.h(0)
qc_mixed.cx(0, 1)
qc_mixed.s(1)
qc_mixed.t(2)  # This one gate makes it non-Clifford
qc_mixed.cx(1, 2)
non_clifford_circuits.append(("Mixed Clifford+T", qc_mixed))

non_clifford_detection_passed = 0
non_clifford_detection_failed = 0
routing_non_stim_passed = 0
routing_non_stim_failed = 0

for name, circuit in non_clifford_circuits:
    is_cliff = is_clifford_circuit(circuit)
    decision = router.select_optimal_backend(circuit, strategy="speed")

    print(f"\n  {name}:")
    print(f"    Qubits: {circuit.num_qubits}, Gates: {sum(1 for _ in circuit.data)}")
    print(f"    Detected as Clifford: {is_cliff}")
    print(f"    Routed to: {decision.recommended_backend.value}")
    print(f"    Confidence: {decision.confidence_score:.3f}")

    if not is_cliff:
        non_clifford_detection_passed += 1
        print(f"    ✓ Non-Clifford detection CORRECT")
    else:
        non_clifford_detection_failed += 1
        print(f"    ✗ Non-Clifford detection FAILED (should be False)")

    if decision.recommended_backend != BackendType.STIM:
        routing_non_stim_passed += 1
        print(f"    ✓ Routing CORRECT (avoided Stim)")
    else:
        routing_non_stim_failed += 1
        print(f"    ✗ Routing FAILED (should NOT route to Stim)")

print(f"\n  Summary:")
print(f"    Non-Clifford Detection: {non_clifford_detection_passed}/{len(non_clifford_circuits)} passed")
print(f"    Non-Stim Routing: {routing_non_stim_passed}/{len(non_clifford_circuits)} passed")

# Test 1.3: Edge case - Clifford with measurements and barriers
print("\n\n1.3: Testing Edge Cases (Clifford + Measurements/Barriers)")
print("-" * 80)

qc_with_measurement = QuantumCircuit(2, 2)
qc_with_measurement.h(0)
qc_with_measurement.cx(0, 1)
qc_with_measurement.measure([0, 1], [0, 1])

is_cliff = is_clifford_circuit(qc_with_measurement)
decision = router.select_optimal_backend(qc_with_measurement, strategy="speed")

print(f"\n  Clifford + Measurement:")
print(f"    Detected as Clifford: {is_cliff}")
print(f"    Routed to: {decision.recommended_backend.value}")
print(f"    Status: {'✓ PASS' if is_cliff else '✗ FAIL (measurements should be ignored)'}")

qc_with_barrier = QuantumCircuit(3)
qc_with_barrier.h(0)
qc_with_barrier.barrier()
qc_with_barrier.cx(0, 1)
qc_with_barrier.barrier()
qc_with_barrier.s(2)

is_cliff = is_clifford_circuit(qc_with_barrier)
decision = router.select_optimal_backend(qc_with_barrier, strategy="speed")

print(f"\n  Clifford + Barriers:")
print(f"    Detected as Clifford: {is_cliff}")
print(f"    Routed to: {decision.recommended_backend.value}")
print(f"    Status: {'✓ PASS' if is_cliff else '✗ FAIL (barriers should be ignored)'}")

# Test 1.4: Clifford ratio metric
print("\n\n1.4: Testing Clifford Ratio Metric")
print("-" * 80)

test_circuits = [
    ("100% Clifford", qc_bell, 1.0),
    ("90% Clifford", qc_mixed, None),  # Will calculate actual
    ("0% Clifford", qc_rotation, 0.0)
]

for name, circuit, expected_ratio in test_circuits:
    analysis = analyze_circuit(circuit)
    actual_ratio = analysis.get('clifford_ratio', 0.0)

    print(f"\n  {name}:")
    print(f"    Clifford Ratio: {actual_ratio:.3f}")
    print(f"    Total Gates: {analysis.get('total_gates', 0)}")
    print(f"    Clifford Gates: {analysis.get('clifford_gates', 0)}")

    if expected_ratio is not None:
        if abs(actual_ratio - expected_ratio) < 0.1:
            print(f"    ✓ PASS (expected ~{expected_ratio:.1f})")
        else:
            print(f"    ✗ FAIL (expected ~{expected_ratio:.1f})")

# Overall Results
print("\n\n" + "=" * 80)
print("TEST 1 OVERALL RESULTS")
print("=" * 80)

total_clifford_tests = clifford_detection_passed + clifford_detection_failed
total_non_clifford_tests = non_clifford_detection_passed + non_clifford_detection_failed
total_routing_tests = routing_stim_passed + routing_stim_failed + routing_non_stim_passed + routing_non_stim_failed

print(f"\nClifford Detection Accuracy: {clifford_detection_passed}/{total_clifford_tests} = {100*clifford_detection_passed/total_clifford_tests:.1f}%")
print(f"Non-Clifford Detection Accuracy: {non_clifford_detection_passed}/{total_non_clifford_tests} = {100*non_clifford_detection_passed/total_non_clifford_tests:.1f}%")
print(f"Routing Accuracy: {(routing_stim_passed + routing_non_stim_passed)}/{total_routing_tests} = {100*(routing_stim_passed + routing_non_stim_passed)/total_routing_tests:.1f}%")

all_passed = (
    clifford_detection_failed == 0 and
    non_clifford_detection_failed == 0 and
    routing_stim_failed == 0 and
    routing_non_stim_failed == 0
)

if all_passed:
    print("\n✓ TEST 1: PASSED - Clifford detection is accurate and routing is correct")
else:
    print("\n✗ TEST 1: FAILED - Issues found in Clifford detection or routing")

print("=" * 80)
