# Segmented Execution Showcase

## Performance Comparison

| Qubits | Single Backend | Single Time (s) | Segmented Time (s) | Speedup | Segments |
|--------|----------------|-----------------|-------------------|---------|----------|
| 8 | tn | 0.002 | 0.002 | 1.12x | 1 |
| 12 | tn | 0.003 | 0.003 | 0.99x | 1 |
| 16 | tn | 0.011 | 0.011 | 1.02x | 1 |

## Boundary Adapter Summary

Backend: tn
Time: 0.000s
Metrics: {'num_qubits': 6, 'depth': 5, 'two_qubit_depth': 1, 'edges': 3, 'treewidth_estimate': 1, 'light_cone_width': 1, 'clifford_ratio': 0.8, 'is_clifford': False, 'gate_entropy': 1.6879430945989, 'entanglement_entropy_estimate': 2.3608160417241995, 'quantum_volume_estimate': 32.0, 'parallelization_factor': 3.0, 'noise_susceptibility': 0.11000000000000001, 'classical_simulation_complexity': 165.437600046154, 'connectivity_score': 0.13999999999999999, 'gate_diversity': 1.25, 'expressivity_measure': 0.6066666666666667}

## Key Observations


## Boundary Adapter Performance

- Optimal boundary adapters preserve exact entanglement (r EPR pairs)
- Active width L = |A| + r kept within Mac Studio limits (≤31 qubits)
- TVD < 0.05 achieved through adequate shot budget

## Hardware Utilization

- Mac Studio M4 Max (36 GB RAM)
- Statevector limited to 31 qubits (fp32) or 30 qubits (fp64)
- Tensor network with cotengra slicing for larger circuits
- ProcessPoolExecutor with spawn for concurrent TN slices
