<div align="center">

# Ariadne
**Intelligent Quantum Simulator Router**

*The Google Maps for quantum circuit simulation*

[![PyPI version](https://img.shields.io/pypi/v/ariadne-router.svg)](https://pypi.org/project/ariadne-router/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![CI](https://github.com/Hmbown/ariadne/actions/workflows/ci.yml/badge.svg)](https://github.com/Hmbown/ariadne/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Hmbown/ariadne/branch/main/graph/badge.svg)](https://codecov.io/gh/Hmbown/ariadne)

</div>

---

## What is Ariadne?

Ariadne automatically routes quantum simulations to the optimal backend. Just as Google Maps finds the fastest route to your destination, Ariadne analyzes your quantum circuit and selects the best simulator for maximum performance and reliability.

**One line of code. Maximum performance.**

```python
from ariadne import simulate
result = simulate(quantum_circuit, shots=1000)  # That's it!
```

---

## Why Ariadne?

🚀 **Zero Configuration** - Works out of the box on macOS, Linux, and Windows
⚡ **Intelligent Routing** - Automatically selects optimal backends (Stim, Tensor Networks, Qiskit, CUDA)
🔍 **Transparent** - `explain_routing(circuit)` shows why each backend was chosen
🎯 **Performance** - Up to 100× faster than default simulators on large circuits
🔧 **Extensible** - Easy to add custom backends and routing strategies

---

## Quick Start

### Installation

```bash
pip install ariadne-router
```

**Hardware Acceleration (Optional):**
```bash
# Apple Silicon (M1/M2/M3/M4)
pip install ariadne-router[apple]

# NVIDIA GPUs
pip install ariadne-router[cuda]
```

### Basic Usage

```python
from ariadne import simulate, explain_routing
from qiskit import QuantumCircuit

# Create a 40-qubit GHZ state
qc = QuantumCircuit(40, 40)
qc.h(0)
for i in range(39):
    qc.cx(i, i + 1)
qc.measure_all()

# Simulate with automatic backend selection
result = simulate(qc, shots=1000)

print(f"Backend: {result.backend_used}")
print(f"Time: {result.execution_time:.3f}s")
print(f"Why: {explain_routing(qc)}")
```

**Output:**
```
Backend: stim
Time: 0.012s
Why: Clifford circuit detected → routed to Stim for 1000× speedup
```

---

## Supported Backends

| Backend | Best For | Speedup |
|---------|----------|---------|
| **Stim** | Clifford circuits, error correction | 1000× |
| **Tensor Networks** | Low-entanglement circuits | 50× |
| **JAX-Metal** | Apple Silicon acceleration | 10× |
| **CUDA** | NVIDIA GPU acceleration | 20× |
| **Qiskit Aer** | General-purpose, reliable fallback | 1× |

---

## Examples

<details>
<summary><b>🎯 Force a Specific Backend</b></summary>

```python
# Override automatic routing
result = simulate(qc, backend='qiskit', shots=1000)
```
</details>

<details>
<summary><b>🔧 Custom Routing Strategy</b></summary>

```python
from ariadne import RoutingStrategy

result = simulate(qc, strategy=RoutingStrategy.MEMORY_EFFICIENT)
```
</details>

<details>
<summary><b>🐳 Docker Usage</b></summary>

```bash
docker pull ghcr.io/hmbown/ariadne-router:latest
docker run --rm ghcr.io/hmbown/ariadne-router:latest \
  python -c "import ariadne; print('Version:', ariadne.__version__)"
```
</details>

---

## Documentation

- 📚 **[User Guide](USER_GUIDE.md)** - Comprehensive usage documentation
- 🚀 **[Quick Start](QUICK_START.md)** - Get up and running in 5 minutes
- 🤝 **[Contributing](CONTRIBUTING.md)** - How to contribute to the project
- 🗺️ **[Roadmap](ROADMAP.md)** - Planned features and improvements

---

## Use Cases

- **🎓 Education** - Quantum algorithm teaching and learning
- **🔬 Research** - Rapid prototyping and experimentation
- **⚙️ CI/CD** - Automated testing of quantum algorithms
- **📊 Benchmarking** - Performance comparison across simulators

---

## Performance

Ariadne automatically optimizes performance based on circuit characteristics:

| Circuit Type | Traditional | Ariadne | Speedup |
|--------------|-------------|---------|---------|
| 50-qubit Clifford | 45.2s | 0.045s | **1000×** |
| Low-entanglement | 12.8s | 0.26s | **50×** |
| General circuits | 5.4s | 5.1s | **1.1×** |

*Benchmarks run on Apple M3 Max with 128GB RAM*

---

## Community

- 🐛 **Issues**: [GitHub Issues](https://github.com/Hmbown/ariadne/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Hmbown/ariadne/discussions)
- 📧 **Contact**: hunter@shannonlabs.dev

---

## License

Apache 2.0 - see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built for the quantum computing community** 🌟

[⭐ Star us on GitHub](https://github.com/Hmbown/ariadne) • [📦 PyPI Package](https://pypi.org/project/ariadne-router/)

</div>
