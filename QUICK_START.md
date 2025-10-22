# Ariadne Quick Start

This guide will get you up and running with Ariadne in just a few minutes.

## 1. Installation

Install Ariadne from PyPI:

```bash
pip install ariadne-router
```

For hardware acceleration, install the appropriate extras:

```bash
# For Apple Silicon (M1/M2/M3/M4)
pip install ariadne-router[apple]

# For NVIDIA GPUs (CUDA)
pip install ariadne-router[cuda]
```

## 2. Your First Simulation

Create a file named `intro.py` and add the following code:

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

Run the script from your terminal:

```bash
python intro.py
```

You'll see that Ariadne automatically routes the simulation to the `stim` backend, which is highly optimized for this type of circuit.

## 3. Understanding the Routing

Ariadne's magic is in its intelligent routing. The `explain_routing` function tells you exactly why a particular backend was chosen. For the example above, the explanation will indicate that a Clifford circuit was detected, making `stim` the ideal choice.

## 4. Using the CLI

Ariadne also comes with a powerful command-line interface.

First, save your quantum circuit to a QASM file named `my_circuit.qasm`.

Then, you can use the `ariadne` command to simulate it:

```bash
ariadne simulate my_circuit.qasm --shots 1000
```

You can also use the CLI to get a routing explanation:

```bash
ariadne explain my_circuit.qasm
```

## Next Steps

Now that you've had a taste of Ariadne, here are a few things you can try:

-   **Experiment with different circuits:** Try creating a circuit with non-Clifford gates and see how the routing changes.
-   **Explore the `USER_GUIDE.md`:** For a more in-depth look at Ariadne's features, including advanced routing strategies and performance benchmarking.
