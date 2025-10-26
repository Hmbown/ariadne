# Issues Found During Quantum Specialist Testing

## Priority 1: Must Fix Before Launch

### Issue #1: Performance Claims Need Qualification

**Location:** `README.md` lines 69-80
**Severity:** High (Marketing/Expectations)
**Type:** Documentation

**Current Text:**
```markdown
| Circuit Type | Traditional Approach | Ariadne | Speedup |
|--------------|---------------------|---------|---------|
| **50-qubit Clifford** | Crashes or 45+ seconds | 0.045s | **~1000× faster*** |
```

**Problem:**
The "~1000× faster" claim, while technically accurate for Clifford circuits, appears in a general performance table that may mislead users into expecting universal speedups.

**Recommendation:**
Add prominent qualifier:
```markdown
| Circuit Type | Traditional Approach | Ariadne | Speedup |
|--------------|---------------------|---------|---------|
| **50-qubit Clifford** | Crashes or 45+ seconds | 0.045s | **~1000× faster (Clifford only)*** |
| **Low-entanglement** | 12.8s | 0.26s | **~50× faster (specific cases)*** |
| **General circuits** | Manual tuning | Auto-optimized | **2-10× typical*** |
```

**Expected Impact:** Prevents user disappointment and GitHub issues asking "Why am I not getting 1000× speedup?"

---

## Priority 2: Should Fix

### Issue #2: Clifford Ratio Metric Calculation

**Location:** `src/ariadne/route/analyze.py`
**Severity:** Medium (Non-critical bug)
**Type:** Bug

**Problem:**
The `clifford_ratio()` metric returns incorrect values for some test circuits. Investigation needed.

**Test Case:**
```python
# Rotation circuit (100% non-Clifford)
qc = QuantumCircuit(2)
qc.rx(0.5, 0)
qc.ry(0.3, 1)

analysis = analyze_circuit(qc)
print(analysis['clifford_ratio'])  # Returns 0.333, expected ~0.0
```

**Recommendation:**
1. Add unit tests specifically for `clifford_ratio()`
2. Debug why non-Clifford gates contribute to ratio
3. Verify formula: `clifford_gates / total_gates`

**Workaround:** Routing decisions use `is_clifford_circuit()` which works correctly. This bug doesn't affect functionality, only metrics.

---

### Issue #3: Documentation Typo

**Location:** `docs/quantum_computing_primer.md` line 154
**Severity:** Low (Typo)
**Type:** Documentation

**Current:** "** measurement: Looking at a quantum state collapses it"
**Should be:** "Measurement: Looking at a quantum state collapses it"

**Fix:** Remove leading asterisks.

---

## Priority 3: Nice to Have

### Issue #4: Variational Circuit Detection Could Be Better

**Location:** `src/ariadne/route/enhanced_router.py`
**Severity:** Low (Optimization opportunity)
**Type:** Enhancement

**Observation:**
VQE circuits routed to `mps` backend instead of `pennylane` which is optimized for variational circuits.

**Current Behavior:**
```python
qc_vqe = create_vqe_circuit()
decision = router.select_optimal_backend(qc_vqe)
# Routes to: mps (works, but not optimal)
```

**Desired Behavior:**
```python
# Should route to: pennylane (optimized for gradients)
```

**Recommendation:**
Add specialized filter for parameterized circuits with many rotation gates:
```python
def _is_variational_circuit(circuit):
    rotation_gates = ["rx", "ry", "rz", "u", "u3"]
    rotation_count = sum(1 for inst in circuit.data
                        if inst.operation.name in rotation_gates)
    return rotation_count > 0.5 * len(circuit.data)
```

---

## Priority 4: Future Work

### Issue #5: No Built-in Statistical Analysis

**Location:** N/A (missing feature)
**Severity:** Low (Feature request)
**Type:** Missing Feature

**Need:**
Users simulating with shots need to understand statistical significance.

**Use Case:**
```python
result1 = simulate(circuit1, shots=1000)
result2 = simulate(circuit2, shots=1000)

# How different are these results?
# Is the difference statistically significant?
# What's the confidence interval?
```

**Recommendation:**
Add `ariadne.analysis` module:
```python
from ariadne import simulate, compare_results

result1 = simulate(circuit1, shots=1000)
result2 = simulate(circuit2, shots=1000)

comparison = compare_results(result1, result2)
print(f"Chi-square p-value: {comparison.p_value}")
print(f"Are different? {comparison.is_significantly_different(alpha=0.05)}")
```

---

### Issue #6: Routing Decision Visualization

**Location:** N/A (missing feature)
**Severity:** Low (Feature request)
**Type:** Missing Feature

**Need:**
Users want to understand *why* a specific backend was chosen.

**Current:** `explain_routing()` returns text explanation
**Desired:** Visual decision tree

**Recommendation:**
```python
from ariadne import RoutingDebugger

debugger = RoutingDebugger(circuit)
debugger.visualize()  # Shows graphical decision tree

# Output:
#   Circuit Analysis
#   ├─ Is Clifford? No
#   ├─ Is Parameterized? Yes
#   ├─ Low Entanglement? Yes
#   └─ → Routed to: pennylane (score: 8.5)
#
#   Alternatives:
#   - mps (score: 7.2)
#   - qiskit (score: 3.0)
```

---

### Issue #7: Batch Simulation API

**Location:** N/A (missing feature)
**Severity:** Low (Feature request)
**Type:** Missing Feature

**Need:**
VQE/QAOA requires running same circuit with different parameters.

**Current Approach:**
```python
for theta in parameter_sweep:
    qc_bound = qc.bind_parameters({param: theta})
    result = simulate(qc_bound, shots=1000)  # Serial, slow
```

**Desired API:**
```python
from ariadne import simulate_batch

parameter_values = [
    {param: 0.1},
    {param: 0.2},
    # ... 100 more
]

results = simulate_batch(qc, parameter_values, shots=1000, parallel=True)
# Automatically parallelizes across CPU cores
```

---

## Non-Issues (Working as Expected)

### "Different backends give slightly different results"

**Status:** ✓ Expected behavior
**Reason:**
- Different RNG seeds
- Floating-point precision varies
- Shot noise dominates

**Verdict:** Not a bug. Differences are within statistical tolerance.

---

### "Routing overhead is 5-20ms"

**Status:** ✓ Acceptable performance
**Reason:** Analysis includes circuit traversal, gate counting, entropy calculation
**Verdict:** <10% overhead for most circuits is excellent.

---

### "Some backends crash on conditional operations"

**Status:** ✓ Backend limitation, not Ariadne bug
**Reason:** Not all backends support mid-circuit measurements + classical control
**Verdict:** Ariadne falls back to Qiskit correctly.

---

## Summary

**Total Issues Found:** 7
- **Priority 1 (Must Fix):** 1 (documentation)
- **Priority 2 (Should Fix):** 3 (2 docs, 1 minor bug)
- **Priority 3 (Nice to Have):** 1 (optimization)
- **Priority 4 (Future):** 3 (feature requests)

**Critical Bugs:** 0 ✓
**Blocking Issues:** 0 ✓
**Launch Readiness:** ✓ APPROVED (with doc updates)

---

**Issue Reporting Date:** October 26, 2025
**Tested Version:** v0.1.dev144
**Reviewer:** Quantum Computing Specialist
