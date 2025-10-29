# Ariadne: Automatic Quantum Simulation Backend Selection

Ariadne automatically selects the optimal quantum simulation backend for your circuits based on circuit analysis. Instead of manually choosing between different simulators, Ariadne evaluates your circuit and routes it to the most appropriate backend.

After extensive benchmarking and testing, Ariadne is available with 326 tests passing (25 skipped for optional dependencies).

### Real Performance Data from Benchmarks

Based on our comprehensive test suite (13 circuits across different types):

- **Clifford circuits** (~69% of benchmarks): Automatically routed to Stim backend with execution times of ~0.001s - ~0.005s and throughput of ~200,000 - ~900,000 shots/second
- **Non-Clifford circuits**: Routed to MPS, tensor network, or other backends depending on structure
- Average execution time across all circuit types: ~0.22s

### How It Works

Ariadne analyzes quantum circuits using information theory principles and topology analysis to determine the optimal simulation backend:

1. **Circuit Analysis**: Evaluates entropy, gate structure, and entanglement patterns
2. **Backend Selection**: Routes to Stim for Clifford circuits, MPS for low-entanglement circuits, tensor networks for specific structures, and fallbacks for everything else

### Getting Started

```python
from ariadne import simulate
from qiskit import QuantumCircuit

# Create your quantum circuit
qc = QuantumCircuit(40, 40)
qc.h(0)
for i in range(39):
    qc.cx(i, i + 1)
qc.measure_all()

# Simulate with automatic backend selection
result = simulate(qc, shots=1000)
print(f"Backend used: {result.backend_used}")
print(f"Execution time: {result.execution_time:.3f}s")
```

### Technical Details

- **Implementation**: Built on established quantum simulation backends (Stim, Qiskit, MPS, tensor networks, etc.)
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Well-tested**: 326 tests passing with comprehensive benchmarking
- **Analysis-driven**: Routing decisions based on mathematical analysis rather than heuristics

### Try It Out

```bash
pip install ariadne-router
```

GitHub: https://github.com/Hmbown/ariadne
PyPI: https://pypi.org/project/ariadne-router/
License: Apache 2.0
