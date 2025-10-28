# Ariadne Benchmark Report
**Timestamp:** 2025-10-27 10:09:00
**Environment:** macOS-14.6.1-arm64-arm-64bit
**Tests:** 13/13 passed

**Average execution time:** 0.2427s
## Backend Usage
- **mps:** 4 circuits (30.8%)
- **stim:** 9 circuits (69.2%)
## Detailed Results
| Circuit | Backend | Time (s) | Status |
|---------|---------|----------|--------|
| small_clifford_ghz | stim | 0.0112 | ✅ Pass |
| small_clifford_ladder | stim | 0.0078 | ✅ Pass |
| medium_clifford_ghz | stim | 0.0113 | ✅ Pass |
| medium_clifford_stabilizer | stim | 0.0119 | ✅ Pass |
| large_clifford_ghz | stim | 0.0268 | ✅ Pass |
| large_clifford_surface_code | stim | 0.0410 | ✅ Pass |
| small_non_clifford | mps | 1.1684 | ✅ Pass |
| medium_non_clifford | mps | 0.8281 | ✅ Pass |
| mixed_vqe_ansatz | mps | 0.6407 | ✅ Pass |
| mixed_qaoa | mps | 0.4010 | ✅ Pass |
| single_qubit | stim | 0.0022 | ✅ Pass |
| no_gates | stim | 0.0028 | ✅ Pass |
| measurement_only | stim | 0.0023 | ✅ Pass |
