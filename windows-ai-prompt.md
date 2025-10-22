# Windows AI Prompt - Ariadne Quantum Simulator Router

## 🎯 MISSION: Fix Windows CI/CD Failures

You are tasked with fixing the Windows-specific failures in the Ariadne Quantum Simulator Router CI/CD pipeline. The package works perfectly on macOS and Linux, but Windows tests are failing.

## 📋 CURRENT STATUS

### ✅ WORKING PERFECTLY:
- **Ubuntu Tests**: All passing ✅
- **macOS Tests**: All passing ✅
- **Docker Builds**: Working ✅
- **Core Functionality**: 12 quantum backends, 179k+ shots/second ✅
- **Package Quality**: Professional-grade, production-ready ✅

### ❌ FAILING ON WINDOWS:
- **Windows Quantum Regression Tests**: 2 jobs failing
- **Likely Issues**: Shell compatibility, path separators, environment variables

## 🔧 PACKAGE OVERVIEW

**Ariadne** is an intelligent quantum circuit router that automatically selects the best backend for quantum simulations:

- **Core Backends**: Qiskit, Stim, Tensor Networks, MPS
- **Quantum Platforms**: PennyLane, PyQuil, Braket, Q#, OpenCL (10+ total)
- **Performance**: 40-qubit circuits in 0.051s, automatic Clifford→Stim routing
- **Docker**: Multi-stage builds (production + quantum-full environments)

## 🐛 WINDOWS-SPECIFIC ISSUES TO INVESTIGATE

### 1. **Quantum Regression Test Failures**
**Files to check:**
- `.github/workflows/quantum-regression.yml`
- `scripts/quantum_regression_test.py`
- `src/ariadne/benchmarking.py`

**Likely problems:**
- Path separator issues (Windows uses `\` vs `/`)
- PowerShell vs Bash compatibility
- Environment variable handling
- File I/O differences on Windows

### 2. **Python Environment Issues**
**Check:**
- Package installation: `pip install -e .[dev,viz]`
- Import paths and module loading
- Backend availability detection
- Dependency conflicts on Windows

### 3. **CI Configuration Problems**
**Investigate:**
- Windows runner environment setup
- Shell selection (bash vs PowerShell vs cmd)
- File permissions and execution
- Working directory issues

## 🛠️ DEBUGGING STEPS

### Step 1: Local Windows Testing
```powershell
# Clone and setup
git clone https://github.com/Hmbown/ariadne.git
cd ariadne

# Install and test core functionality
python -m pip install --upgrade pip
pip install -e .[dev,viz]

# Test core imports
python -c "from ariadne import get_available_backends, simulate; print(get_available_backends())"

# Test basic simulation
python -c "
from ariadne import simulate
from qiskit import QuantumCircuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()
result = simulate(qc, shots=100)
print(f'Success: {result.backend_used}')
"
```

### Step 2: Test Regression Script
```powershell
# Run the failing regression test locally
python scripts/quantum_regression_test.py

# Check for specific Windows errors
python -c "
import sys
print(f'Python: {sys.version}')
print(f'Platform: {sys.platform}')
print(f'Path separator: {sys.platform}')
"
```

### Step 3: Check Benchmarking Module
```powershell
# Test benchmarking functionality
python -c "
from ariadne.benchmarking import export_benchmark_report
report = export_benchmark_report(
    algorithms=['bell'],
    backends=['qiskit'],
    shots=10,
    fmt='json'
)
print('Benchmarking works!')
print(list(report.keys()))
"
```

## 🔍 FILES TO EXAMINE

### Critical Files:
1. **`.github/workflows/quantum-regression.yml`** - CI workflow
2. **`scripts/quantum_regression_test.py`** - Test script
3. **`src/ariadne/benchmarking.py`** - Benchmarking module
4. **`src/ariadne/route/routing_tree.py`** - Backend detection

### Windows-Specific Considerations:
- Line endings (CRLF vs LF)
- Path separators (`\` vs `/`)
- Case sensitivity differences
- Environment variable expansion
- Shell command execution

## 🎯 EXPECTED FIXES

### 1. **Path Handling**
```python
# Replace Unix-style paths
import os.path
path = os.path.join("scripts", "quantum_regression_test.py")  # Not "scripts/quantum_regression_test.py"
```

### 2. **Shell Compatibility**
```yaml
# In .github/workflows/quantum-regression.yml
- name: Run quantum regression tests
  run: python scripts\quantum_regression_test.py  # Windows path
  shell: cmd  # Or powershell
```

### 3. **Environment Variables**
```yaml
# Windows environment handling
env:
  PYTHONPATH: ${{ github.workspace }}\src  # Windows-style
```

## 📊 SUCCESS CRITERIA

### ✅ When Fixed, You Should See:
- All Windows quantum regression tests passing
- Local Windows testing: `python scripts/quantum_regression_test.py` works
- CI showing: **11 successful checks, 0 failing**
- Package working: `from ariadne import simulate` functions perfectly

### 📈 Performance Targets:
- **Backend Detection**: Should find 4+ backends on Windows
- **Simulation Speed**: Bell state <0.1s, GHZ state <0.2s
- **Success Rate**: 100% on basic qiskit + stim tests

## 🚀 FINAL VALIDATION

Once fixed, test:
```powershell
# Full functionality test
python -c "
from ariadne import get_available_backends, simulate, explain_routing
from qiskit import QuantumCircuit

print('🔧 Windows Validation Test')
print('========================')

backends = get_available_backends()
print(f'Backends: {len(backends)} found')
for b in backends:
    print(f'  ✅ {b}')

# Test 5-qubit GHZ
qc = QuantumCircuit(5, 5)
qc.h(0)
for i in range(4):
    qc.cx(i, i + 1)
qc.measure_all()

result = simulate(qc, shots=1000)
print(f'✅ Simulation: {result.backend_used} in {result.execution_time:.4f}s')

explanation = explain_routing(qc)
print(f'✅ Routing: {len(explanation)} chars of explanation')

print('🎉 Windows environment fully functional!')
"
```

## 💡 ADDITIONAL CONTEXT

**Repository Structure:**
```
ariadne/
├── .github/workflows/          # CI/CD pipelines
├── src/ariadne/               # Main package
├── scripts/                   # Utility scripts
├── tests/                     # Test suite
├── examples/                  # Usage examples
├── benchmarks/                # Performance tests
└── docker-compose.yml         # Container orchestration
```

**Key Dependencies:**
- qiskit 2.2.1 (quantum circuits)
- stim 1.15.0 (Clifford simulation)
- numpy, scipy (numerical)
- quimb, cotengra (tensor networks)

**Recent Changes:**
- Added cross-platform regression test script
- Fixed Docker multi-stage builds
- Enhanced backend detection with safe imports
- Added 10+ quantum platform support

## 🎯 YOUR GOAL

Fix the Windows CI failures so that Ariadne works perfectly across all platforms. The package is production-ready on Unix systems - we just need Windows compatibility.

**Success = All CI checks green + Windows local testing works flawlessly!**

---

*Good luck! The quantum computing community is counting on you to make Ariadne work seamlessly on Windows! 🚀*
