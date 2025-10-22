<div align="center">

# Ariadne: The Google Maps of Quantum Simulation

**Ariadne is an intelligent router for quantum simulations.** Just as Google Maps finds the best route for a road trip, Ariadne automatically selects the most efficient backend for simulating your quantum circuit. It intelligently routes your simulation to the best-suited backend from a wide range of options, including Stim, Tensor Networks, Qiskit Aer, and hardware-accelerated backends like CUDA and JAX-Metal.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![CI/CD Pipeline](https://img.shields.io/github/actions/workflow/status/Hmbown/ariadne/ci.yml?branch=main&label=CI%2FCD)](https://github.com/Hmbown/ariadne/actions/workflows/ci.yml)
[![codecov](https://img.shields.io/codecov/c/github/Hmbown/ariadne/main)](https://codecov.io/gh/Hmbown/ariadne)
[![Code Style](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI version](https://img.shields.io/pypi/v/ariadne-router.svg)](https://pypi.org/project/ariadne-router/)
[![Container](https://img.shields.io/static/v1?label=container&message=GHCR&color=blue)](https://github.com/Hmbown/ariadne/pkgs/container/ariadne-router)
[![Pytest](https://img.shields.io/badge/tested%20with-pytest-yes.svg?logo=pytest)](https://pytest.org)

</div>

---

## Why Ariadne?

-   **Zero-Configuration:** A single `simulate(qc)` call works across macOS, Linux, and Windows, with or without hardware acceleration.
-   **Performance-Aware Routing:** Ariadne understands the structure of your circuit. It routes Clifford circuits to Stim, low-entanglement circuits to Matrix Product State (MPS) or Tensor Network (TN) simulators, and defaults to a robust general-purpose simulator for all other cases.
-   **Explainable Decisions:** Want to know why Ariadne chose a particular backend? `explain_routing(qc)` provides a clear, human-readable summary of the decision-making process.
-   **Cross-Ecosystem Support:** Ariadne is not tied to a single simulation framework. It seamlessly integrates with a variety of popular quantum libraries, including Qiskit, Cirq, PennyLane, and more.

> **Note**: Ariadne performs **simulator backend routing**, not hardware qubit routing. For mapping quantum circuits to physical hardware, consider tools like [QMAP](https://arxiv.org/abs/2301.11935).

---

## Getting Started

### Installation

Install Ariadne from PyPI:

```bash
pip install ariadne-router
```

To enable hardware acceleration, install the appropriate extras:

```bash
# For Apple Silicon (M1/M2/M3/M4)
pip install ariadne-router[apple]

# For NVIDIA GPUs (CUDA)
pip install ariadne-router[cuda]
```

### Docker Quick Start

Run a ready-to-use container from GHCR (if your project has access to images):

```bash
# Pull latest production image
docker pull ghcr.io/Hmbown/ariadne-router:latest

# Run a quick verification
docker run --rm ghcr.io/Hmbown/ariadne-router:latest \
  python -c "import ariadne; print('Ariadne OK:', ariadne.__version__)"
```

Develop and test with docker-compose:

```bash
docker-compose build
docker-compose up -d ariadne-dev
docker-compose exec ariadne-dev bash
# or run tests
docker-compose up --abort-on-container-exit ariadne-test
```

### Your First Simulation

Let's simulate a 40-qubit GHZ state. This is a classic example of a stabilizer circuit, which can be simulated efficiently with the right tools.

```python
from ariadne import simulate, explain_routing
from qiskit import QuantumCircuit

# Create a 40-qubit GHZ circuit
qc = QuantumCircuit(40, 40)
qc.h(0)
for i in range(39):
    qc.cx(i, i + 1)
qc.measure_all()

# Simulate the circuit
result = simulate(qc, shots=1000)

# See the results
print(f"Backend Used: {result.backend_used}")
print(f"Execution Time: {result.execution_time:.4f}s")
print(f"Routing Explanation: {explain_routing(qc)}")
```

Ariadne automatically identifies this as a Clifford circuit and routes it to the `stim` backend, resulting in a significant speedup compared to general-purpose simulators.

---

## Core Features

-   **Intelligent Routing:** Ariadne analyzes your circuit's properties (size, gate types, entanglement) to select the optimal simulation backend.
-   **Hardware Acceleration:** Automatically utilizes Apple Silicon (via JAX-Metal) and NVIDIA GPUs (via CUDA) when available.
-   **Transparent Decisions:** The `explain_routing` function provides a detailed breakdown of the routing decision, so you always know why a particular backend was chosen.
-   **Extensible Backend System:** Ariadne's modular design makes it easy to add new backends and routing strategies.

---

## Supported Backends

Ariadne supports a wide range of quantum simulation backends:

-   **Qiskit:** A reliable and feature-rich CPU-based simulator.
-   **Stim:** A high-performance simulator for Clifford circuits.
-   **Tensor Network (TN) / Matrix Product State (MPS):** For circuits with low entanglement, powered by `quimb` and `cotengra`.
-   **JAX-Metal:** For hardware acceleration on Apple Silicon.
-   **CUDA:** For GPU acceleration on NVIDIA hardware.
-   **And more:** DDSIM, Cirq, PennyLane, Qulacs, and experimental support for PyQuil, Braket, and Q#.

---

## Advanced Usage

### Forcing a Backend

You can override Ariadne's automatic routing and force a specific backend:

```python
result = simulate(qc, shots=1000, backend='qiskit')
```

### Custom Routing Strategies

Ariadne provides a variety of routing strategies to suit different needs:

```python
from ariadne import ComprehensiveRoutingTree, RoutingStrategy

router = ComprehensiveRoutingTree()
decision = router.route_circuit(circuit, strategy=RoutingStrategy.MEMORY_EFFICIENT)
```

Available strategies include `SPEED_FIRST`, `ACCURACY_FIRST`, `MEMORY_EFFICIENT`, and more.

---

## Configuration Tips

- Tensor-network bit ordering:
  - The tensor-network backend outputs Qiskit-compatible little-endian bitstrings by default.
  - You can control this via `TensorNetworkOptions(bitstring_order='qiskit'|'msb')`.
  - Example:
    ```python
    from ariadne.backends.tensor_network_backend import TensorNetworkBackend, TensorNetworkOptions
    backend = TensorNetworkBackend(TensorNetworkOptions(seed=123, bitstring_order='qiskit'))
    ```

- Resource checks in constrained environments:
  - If resource feasibility checks are overly conservative on your machine/CI, disable them for small circuits.
  - Set env var `ARIADNE_DISABLE_RESOURCE_CHECKS=1` or toggle `get_config().analysis.enable_resource_estimation = False`.

---

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) to get started.

---

## License

Ariadne is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.
