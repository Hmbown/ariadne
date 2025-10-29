# Ariadne Benchmark Report
**Timestamp:** 2025-10-28 22:23:56
**Environment:** macOS-26.0.1-arm64-arm-64bit
**Tests:** 13/13 passed

**Average execution time:** 0.2989s
## Backend Usage
- **mps:** 2 circuits (15.4%)
- **pennylane:** 1 circuits (7.7%)
- **stim:** 9 circuits (69.2%)
- **tensor_network:** 1 circuits (7.7%)
## Detailed Results
| Circuit | Backend | Time (s) | Status |
|---------|---------|----------|--------|
| small_clifford_ghz | stim | 0.0535 | ✅ Pass |
| small_clifford_ladder | stim | 0.0077 | ✅ Pass |
| medium_clifford_ghz | stim | 0.0115 | ✅ Pass |
| medium_clifford_stabilizer | stim | 0.0121 | ✅ Pass |
| large_clifford_ghz | stim | 0.0267 | ✅ Pass |
| large_clifford_surface_code | stim | 0.0401 | ✅ Pass |
| small_non_clifford | mps | 0.6747 | ✅ Pass |
| medium_non_clifford | tensor_network | 0.3044 | ✅ Pass |
| mixed_vqe_ansatz | mps | 0.4184 | ✅ Pass |
| mixed_qaoa | pennylane | 2.3303 | ✅ Pass |
| single_qubit | stim | 0.0018 | ✅ Pass |
| no_gates | stim | 0.0023 | ✅ Pass |
| measurement_only | stim | 0.0022 | ✅ Pass |
