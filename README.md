<div align="center">

# Ariadne

**Intelligent Quantum Circuit Routing**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![CI/CD Pipeline](https://img.shields.io/github/actions/workflow/status/Hmbown/ariadne/ci.yml?branch=main&label=CI%2FCD&style=for-the-badge)](https://github.com/Hmbown/ariadne/actions/workflows/ci.yml)
[![codecov](https://img.shields.io/codecov/c/github/Hmbown/ariadne/main?style=for-the-badge)](https://codecov.io/gh/Hmbown/ariadne)
[![Code Style](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI version](https://badge.fury.io/py/ariadne-quantum.svg)](https://badge.fury.io/py/ariadne-quantum)

</div>

---

**Quantum computing is still in its early days.** As the ecosystem evolves rapidly with new simulators, hardware platforms, and optimization techniques, developers face an increasingly complex landscape of choices. Each quantum circuit might run best on a different backend, but who has time to manually benchmark across 15+ simulators?

Ariadne attempts to solve this by automatically analyzing your quantum circuits and routing them to optimal backends. Instead of wrestling with import statements and performance tuning, you can focus on your algorithms.

This is an experiment in simplifying quantum development workflows. **Feedback, contributions, and real-world testing are very welcome** - I'm genuinely curious whether this approach helps or just adds another layer of complexity.

---

Ariadne is an intelligent quantum circuit routing system that automatically analyzes circuit properties and selects the optimal simulator backend. Like the mythological thread that guided Theseus through the labyrinth, Ariadne guides developers through the complex landscape of quantum simulators to find optimal performance paths.

The routing system prioritizes transparency and determinism - every routing decision is based on measurable circuit characteristics and can be audited for correctness.

[📚 Documentation Site](https://hmbown.github.io/ariadne) • [📖 Local Docs](docs/README.md) • [💡 Examples](examples/README.md) • [🚀 Getting Started](#-getting-started) • [📊 Performance](#-performance) • [🤝 Contributing](#-contributing)

---

## ✨ Key Features

| Capability | Impact |
|---|---|
| **🧠 Intelligent Routing** | Mathematical analysis of circuit properties automatically selects the optimal backend without user intervention. |
| **⚡ Stim Auto-Detection** | Pure Clifford circuits are automatically routed to Stim, enabling the simulation of circuits that are too large for other backends. |
| **🍎 Apple Silicon Acceleration** | JAX-Metal backend can provide speedups for general-purpose circuits on M-series chips. |
| **🚀 CUDA Support** | NVIDIA GPU acceleration is supported, with expected speedups depending on the hardware and circuit structure. |
| **🔄 Zero Configuration** | `simulate(circuit, shots)` just works—no vendor imports or backend selection logic required. |
| **🔢 Universal Fallback** | Always returns a result, even when specialized backends fail. |
| **📊 Transparent Decisions** | Every routing decision can be inspected and validated with detailed reasoning. |
| **🔌 Extensible** | Apache 2.0 licensed with a modular backend interface for community contributions. |

---

## 🧰 Use Cases

- **Education and workshops**
  - Run canonical circuits (Bell/GHZ/Clifford, shallow variational) without choosing simulators. Ariadne routes to `stim`/`MPS`/`Qiskit`/`Metal` as appropriate.
  - One command demo: `python examples/quickstart.py`.

- **Research prototyping**
  - Iterate on algorithms with `simulate(qc, shots)` and let Ariadne pick the best backend by structure (Clifford ratio, entanglement heuristics).
  - Override when needed with `simulate(qc, backend='mps')` and compare.

- **CI/regression testing**
  - Same tests run across macOS/Linux/Windows. Missing backends fail over cleanly; logs record decisions.
  - Good for ensuring algorithms don’t silently degrade across environments.

- **Benchmarking and feasibility checks**
  - Large stabilizer circuits route to `stim` (feasible when statevector fails).
  - Low-entanglement shallow circuits route to `MPS` for speed/memory wins.

- **Apple Silicon acceleration**
  - On M-series Macs, try `Metal` for general-purpose circuits; otherwise fall back to CPU.

---

## 🧭 Routing at a glance

| Circuit characteristics | Expected backend | Why |
|---|---|---|
| Pure Clifford (e.g., GHZ, stabilizers) | `stim` | Specialized, extremely fast stabilizer simulation |
| Low entanglement, shallow depth | `MPS` | Efficient tensor-network representation |
| General circuits on Apple Silicon | `Metal` | Leverage JAX/Metal when available |
| General circuits (portable) | `Qiskit` | Robust CPU statevector/density matrix |

You can always override:

```python
simulate(qc, shots=1000, backend='mps')
```

And CLI:

```bash
ariadne simulate path/to/circuit.qasm --shots 1000
ariadne status --detailed
```

---

### Routing matrix (auto-generated)

![Routing matrix](docs/source/_static/routing_matrix.png)

Regenerate with:

```bash
python examples/routing_matrix.py --shots 256 --generate-image docs/source/_static/routing_matrix.png
```

---

## 🎯 The Ariadne Advantage: Intelligent Automation

Ariadne's core innovation is its ability to mathematically analyze a circuit's structure to determine the optimal execution environment. This eliminates the need for quantum developers to manually select backends based on circuit characteristics.

### Transparent Decision Making

Ariadne provides complete transparency into why a circuit was routed to a specific backend. You can inspect the entire decision path through the routing tree.

```python
from ariadne import explain_routing, show_routing_tree
from qiskit import QuantumCircuit

# Create a circuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Get a detailed, human-readable explanation of the routing decision
explanation = explain_routing(qc)
print(explanation)

# You can also visualize the entire routing tree
print(show_routing_tree())
```

---

## 🚀 Getting Started

### Installation

**Quick Install:**
```bash
git clone https://github.com/Shannon-Labs/ariadne.git
cd ariadne
pip install -e .
```

**With Hardware Acceleration:**
```bash
# Apple Silicon (M1/M2/M3/M4)
pip install -e .[apple]

# NVIDIA GPU (CUDA)
pip install -e .[cuda]

# All optional dependencies
pip install -e .[apple,cuda,viz]
```

📖 **For detailed installation instructions, see the [Comprehensive Installation Guide](docs/comprehensive_installation.md)**

### Your First Simulation

Ariadne automatically routes your circuit to the optimal simulator without any code changes.

```python
from ariadne import simulate
from qiskit import QuantumCircuit

# Create any circuit - let Ariadne handle the rest
qc = QuantumCircuit(20, 20)
qc.h(range(10))
for i in range(9):
    qc.cx(i, i + 1)
qc.measure_all()

# One simple call that handles all backend complexity
result = simulate(qc, shots=1000)
print(f"Backend used: {result.backend_used}")
print(f"Execution time: {result.execution_time:.4f}s")
print(f"Unique outcomes: {len(result.counts)}")
```

### Quickstart Demo

Run the complete quickstart example to see Ariadne in action:

```bash
python examples/quickstart.py
```

This demo showcases:
- Automatic backend selection for different circuit types
- Performance comparisons
- Routing decision transparency
- Hardware acceleration when available

---

### Quickstart GIF

![Quickstart Routing Demo](docs/source/_static/quickstart.gif)

Regenerate with:

```bash
python examples/generate_quickstart_gif.py --output docs/source/_static/quickstart.gif
```

---

## 📊 Performance

Ariadne's primary value is not raw speed, but **intelligent routing** and **developer productivity**. By automatically selecting the best backend for a given circuit, Ariadne saves developers from having to manually manage different simulation environments.

While Ariadne can provide significant speedups in certain scenarios (e.g., using the Stim backend for large Clifford circuits), the overhead of circuit analysis means that for small circuits, direct simulation with a specific backend may be faster.

The true advantage of Ariadne is its ability to **extend your capabilities** by seamlessly routing circuits to backends that can handle them, such as simulating very large Clifford circuits with Stim, which would be impossible with a standard statevector simulator.

For detailed, up-to-date performance data, please refer to the benchmark reports in the `benchmarks/results` directory.

---

## 🔧 Usage Examples

### Automatic Detection of Specialized Circuits

Ariadne recognizes when circuits can benefit from specialized simulators like Stim.

```python
from ariadne import simulate
from qiskit import QuantumCircuit

# Large Clifford circuit that would crash plain Qiskit
qc = QuantumCircuit(40, 40)
qc.h(0)
for i in range(39):
    qc.cx(i, i + 1)  # Creates a 40-qubit GHZ state
qc.measure_all()

# Ariadne automatically routes to Stim for optimal performance
result = simulate(qc, shots=1000)
print(f"Backend used: {result.backend_used}")  # -> stim
```

### Advanced Routing Control

For users who need fine-grained control over the routing process:

```python
from ariadne import ComprehensiveRoutingTree, RoutingStrategy

# Initialize routing system
router = ComprehensiveRoutingTree()

# Use specific routing strategies
decision = router.route_circuit(
    circuit,
    strategy=RoutingStrategy.MEMORY_EFFICIENT
)

print(f"Selected: {decision.recommended_backend.value}")
print(f"Confidence: {decision.confidence_score:.2f}")
print(f"Expected speedup: {decision.expected_speedup:.1f}x")
```

Available routing strategies:
- `SPEED_FIRST` - Prioritize execution speed
- `MEMORY_EFFICIENT` - Optimize for memory usage
- `CLIFFORD_OPTIMIZED` - Specialized for Clifford circuits
- `APPLE_SILICON_OPTIMIZED` - Hardware-aware for M-series chips
- `CUDA_OPTIMIZED` - GPU acceleration focused
- `AUTO_DETECT` - Intelligent analysis (default)


```

---

## 🛡️ Project Maturity

### Test Coverage
- **Unit Tests**: 85%+ coverage across core modules.
- **Integration Tests**: The test suite is run continuously and is expected to pass, with the exception of one known flaky performance test.
- **Backend Tests**: All major backends are tested.

### Documentation
- **Comprehensive Guides**: Installation, usage, and API documentation.
- **Examples Gallery**: 15+ working examples for different use cases.
- **Performance Reports**: Detailed benchmarking and validation.
- **API Reference**: Complete API documentation with examples.

### Development Infrastructure
- **CI/CD Pipeline**: Automated testing on Python 3.11-3.12.
- **Code Quality**: Ruff linting, mypy type checking, pre-commit hooks.
- **Security**: Bandit security scanning, dependency safety checks.
- **Release Management**: Automated versioning and changelog generation.

---

## 🤝 Contributing

We welcome contributions of all kinds, from bug fixes to new features. Please read our [**Contributing Guidelines**](docs/project/CONTRIBUTING.md) to get started.

### Development Setup

```bash
git clone https://github.com/Shannon-Labs/ariadne.git
cd ariadne
pip install -e .[dev]

# Set up pre-commit hooks
pre-commit install

# Run unit tests
make test
```

📖 **For detailed development setup instructions, see the [Comprehensive Installation Guide](docs/comprehensive_installation.md#development-setup)**

---

## 💬 Community

- **GitHub Discussions:** [Ask questions and share ideas](https://github.com/Shannon-Labs/ariadne/discussions)
- **Issue Tracker:** [Report bugs and request features](https://github.com/Shannon-Labs/ariadne/issues)
- **Twitter:** [Follow @ShannonLabs for updates](https://twitter.com/shannonlabs)

---

## 📜 License

Ariadne is released under the [Apache 2.0 License](LICENSE).

### Policies

- [CHANGELOG](CHANGELOG.md)
- [SECURITY](SECURITY.md)
- [CODE OF CONDUCT](CODE_OF_CONDUCT.md)

---

## 🙏 Acknowledgments

Ariadne builds upon excellent open-source quantum computing frameworks:
- [Qiskit](https://qiskit.org/) for quantum circuit representation
- [Stim](https://github.com/quantumlib/Stim) for Clifford circuit simulation
- [Quimb](https://github.com/quimb/quimb) for tensor network operations
- [JAX](https://github.com/google/jax) for hardware acceleration

---

*Ariadne: Intelligent Quantum Routing - No ML, Just Math*
