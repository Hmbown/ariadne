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
from ariadne import list_algorithms, get_algorithm

# List all available algorithms
algorithms = list_algorithms()
print(f"Available algorithms: {algorithms}")

# Get information about a specific algorithm
info = get_algorithm('bell')
print(f"Description: {info['metadata'].description}")
```

---

## 3. Benchmarking Tools

Ariadne provides powerful tools for performance analysis.

### Backend Comparison

Compare the performance of different backends for a given circuit:

```python
from ariadne.enhanced_benchmarking import EnhancedBenchmarkSuite

suite = EnhancedBenchmarkSuite()
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

For detailed information on Ariadne's classes and functions, please refer to our [API Reference](docs/source).

The API reference is automatically generated from the docstrings in the source code. To generate the documentation locally, please see the instructions in the [Contributing Guide](CONTRIBUTING.md).

---

## 6. How-To Guides

This section provides guides for common advanced tasks.

### How to Add a Custom Backend

To add a new backend, you need to create a new class that inherits from `ariadne.backends.base.QuantumBackend` and implement the `simulate` method. Then, register your backend with the `BackendRegistry`.

**Step 1: Create the Backend Class**

Create a new Python file for your backend, for example, `my_custom_backend.py`. In this file, define your backend class:

```python
from ariadne.backends.base import QuantumBackend
from ariadne.circuit import QuantumCircuit
from ariadne.simulator import SimulationResult

class MyCustomBackend(QuantumBackend):
    """
    A custom backend for demonstrating how to add a new backend to Ariadne.
    """
    def __init__(self, options=None):
        super().__init__(options)
        self.backend_name = "my_custom_backend"

    def simulate(self, circuit: QuantumCircuit, shots: int) -> SimulationResult:
        """
        This is where you would implement the simulation logic for your backend.
        For this example, we will just return a dummy result.
        """
        print(f"Simulating circuit on {self.backend_name}...")
        # In a real backend, you would perform the simulation here.
        # For this example, we will just return a dummy result.
        counts = {"00": shots // 2, "11": shots // 2}
        return SimulationResult(
            backend_used=self.backend_name,
            shots=shots,
            counts=counts,
            execution_time=0.1,
        )
```

**Step 2: Register the Backend**

To make your backend available to Ariadne, you need to register it with the `BackendRegistry`. You can do this in your application code before you call the `simulate` function:

```python
from ariadne.backend_registry import BackendRegistry
from my_custom_backend import MyCustomBackend

# Register the custom backend
BackendRegistry.register_backend("my_custom_backend", MyCustomBackend)

# Now you can use your custom backend
result = simulate(qc, shots=1000, backend="my_custom_backend")
```

**Step 3: (Optional) Integrate with the Router**

To integrate your backend with Ariadne's automatic routing, you will need to create a new filter for the `RoutingTree`. This is a more advanced topic, and we recommend that you read the source code for the existing filters to understand how they work.

### How to Create a Custom Routing Strategy

To create a custom routing strategy, you can create a new function that takes a `QuantumCircuit` as input and returns a `RoutingDecision` object.

**Step 1: Create the Strategy Function**

Create a new Python file for your strategy, for example, `my_custom_strategy.py`. In this file, define your strategy function:

```python
from ariadne.circuit import QuantumCircuit
from ariadne.routing import RoutingDecision
from ariadne.routing import BackendType

def my_custom_strategy(circuit: QuantumCircuit) -> RoutingDecision:
    """
    A custom routing strategy that always chooses the 'my_custom_backend'.
    """
    # In a real strategy, you would analyze the circuit and make a decision.
    # For this example, we will always choose 'my_custom_backend'.
    if circuit.n_qubits > 10:
        return RoutingDecision(
            backend=BackendType.QISKIT,
            reason="Circuit is too large for my_custom_backend.",
        )
    else:
        return RoutingDecision(
            backend="my_custom_backend",
            reason="My custom strategy always chooses my_custom_backend for small circuits.",
        )
```

**Step 2: Use the Custom Strategy**

To use your custom strategy, you can pass it to the `ComprehensiveRoutingTree`'s `route_circuit` method:

```python
from ariadne import ComprehensiveRoutingTree
from my_custom_strategy import my_custom_strategy

router = ComprehensiveRoutingTree()
decision = router.route_circuit(circuit, strategy=my_custom_strategy)

print(f"Backend: {decision.backend}")
print(f"Reason: {decision.reason}")
```

This allows you to create complex routing logic that is tailored to your specific needs.
