import importlib.util

import pytest
from pytest import MonkeyPatch
from qiskit import QuantumCircuit

from ariadne.route.enhanced_router import EnhancedQuantumRouter
from ariadne.types import BackendType

# Skip entire module if mqt.ddsim is not available
try:
    dds_spec = importlib.util.find_spec("mqt.ddsim")
    ddsim_available = dds_spec is not None
except (ImportError, ModuleNotFoundError):
    ddsim_available = False

pytestmark = pytest.mark.skipif(not ddsim_available, reason="mqt.ddsim not available")


@pytest.mark.skipif(not ddsim_available, reason="MQT DDSIM not installed")
def test_router_prefers_ddsim_when_requested_and_available(monkeypatch: MonkeyPatch) -> None:
    # Prefer DDSIM via env hint
    monkeypatch.setenv("ARIADNE_ROUTING_PREFER_DDSIM", "1")

    # Build a small non-Clifford circuit that isn't trivially chain-like
    qc = QuantumCircuit(4, 4)
    qc.h(0)
    qc.t(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.cx(1, 3)
    qc.measure_all()

    router = EnhancedQuantumRouter()
    decision = router.select_optimal_backend(qc)

    assert decision.recommended_backend == BackendType.DDSIM, f"Expected DDSIM, got {decision.recommended_backend}"
