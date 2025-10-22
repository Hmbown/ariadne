# Ariadne User Guide

Welcome to the Ariadne User Guide! This guide provides a deep dive into the advanced features of Ariadne. For a quick introduction, please see the [README.md](README.md) and the [QUICK_START.md](QUICK_START.md).

## Table of Contents
1. [Advanced Simulation Control](#advanced-simulation-control)
2. [Educational Tools](#educational-tools)
3. [Benchmarking Tools](#benchmarking-tools)
4. [Command-Line Interface (CLI)](#command-line-interface-cli)
5. [API Reference](#api-reference)
6. [How-To Guides](#how-to-guides)

---

## 1. Advanced Simulation Control

Ariadne provides fine-grained control over the simulation process.

### Forcing a Backend

You can bypass Ariadne's automatic routing and force a specific backend:

```python
from ariadne import simulate
from qiskit import QuantumCircuit

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Force the use of the Qiskit backend
result = simulate(qc, shots=1000, backend='qiskit')
```

### Custom Routing Strategies

You can also choose from a variety of routing strategies to suit your needs:

```python
from ariadne import ComprehensiveRoutingTree, RoutingStrategy

router = ComprehensiveRoutingTree()
decision = router.route_circuit(circuit, strategy=RoutingStrategy.MEMORY_EFFICIENT)
```

Available strategies include `SPEED_FIRST`, `ACCURACY_FIRST`, `MEMORY_EFFICIENT`, and more.

### Tensor Network Bitstring Ordering

When using the tensor-network backend, you can control the bitstring ordering in the returned counts.

```python
from ariadne.backends.tensor_network_backend import TensorNetworkBackend, TensorNetworkOptions

tn = TensorNetworkBackend(TensorNetworkOptions(bitstring_order="qiskit"))  # or "msb"
counts = tn.simulate(qc, shots=1024)
```

The default is `"qiskit"` (little-endian), matching Qiskit’s Statevector sampling.

### Disabling Resource Checks (CI/Constrained Hosts)

If the resource manager reports overly conservative memory on your host or CI, you can disable feasibility/reservation checks:

- Environment variable: set `ARIADNE_DISABLE_RESOURCE_CHECKS=1`
- Programmatic toggle:
  ```python
  from ariadne.config import get_config
  get_config().analysis.enable_resource_estimation = False
  ```

This is useful for small circuits (e.g., 7-qubit codes) where checks might erroneously block execution.

---

## 2. Educational Tools

Ariadne includes a suite of educational tools for learning quantum computing.

### Interactive Circuit Builder

Build quantum circuits step-by-step with explanations:

```python
from ariadne.education import InteractiveCircuitBuilder

builder = InteractiveCircuitBuilder(2, "Bell State")
builder.add_hadamard(0, "Create Superposition", "Apply H gate to qubit 0")
builder.add_cnot(0, 1, "Create Entanglement", "Apply CNOT to entangle qubits")

print(builder.get_circuit().draw())
```

### Algorithm Explorer

Explore a library of over 15 quantum algorithms:

```python
from ariadne.education import AlgorithmExplorer

explorer = AlgorithmExplorer()
print(explorer.list_algorithms())

info = explorer.get_algorithm_info('bell')
print(info['metadata'].description)
```

---

## 3. Benchmarking Tools

Ariadne provides powerful tools for performance analysis.

### Backend Comparison

Compare the performance of different backends for a given circuit:

```python
from ariadne.enhanced_benchmarking import EnhancedBenchmarkSuite

site = EnhancedBenchmarkSuite()
comparison = suite.benchmark_backend_comparison(
    algorithm_name='bell',
    qubit_count=2,
    backends=['auto', 'qiskit', 'stim'],
    shots=1000
)

for backend, result in comparison.items():
    if result.counts:
        print(f"{backend}: {result.execution_time:.4f}s")
```

### Scalability Testing

Test how a backend's performance scales with the number of qubits:

```python
scalability_result = suite.scalability_test(
    algorithm_name='bell',
    qubit_range=(2, 8, 2),
    backend_name='auto',
    shots=1000
)

print(f"Qubit Counts: {scalability_result.qubit_counts}")
print(f"Execution Times: {scalability_result.execution_times}")
```

---

## 4. Command-Line Interface (CLI)

Ariadne's CLI provides access to all of its features from the command line.

- `ariadne simulate <file>`: Simulate a quantum circuit from a QASM file.
- `ariadne explain <file>`: Get a routing explanation for a circuit.
- `ariadne benchmark <file>`: Run a performance benchmark for a circuit.
- `ariadne status`: Check the status of available backends.
- `ariadne education`: Access educational tools and demos.

For a full list of commands and options, use `ariadne --help`.

---

## 5. API Reference

For detailed information on Ariadne's classes and functions, please refer to the source code and docstrings.

---

## 6. How-To Guides

This section provides guides for common advanced tasks.

### How to Add a Custom Backend

To add a new backend, you need to create a new class that inherits from `ariadne.backends.base.QuantumBackend` and implement the `simulate` method. Then, register your backend with the `BackendRegistry`.

### How to Create a Custom Routing Strategy

To create a custom routing strategy, you can create a new function that takes a `QuantumCircuit` as input and returns a `RoutingDecision` object.
