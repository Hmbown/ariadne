import importlib.util

import pytest
from qiskit import QuantumCircuit

from ariadne.route.enhanced_router import EnhancedQuantumRouter
from ariadne.types import BackendType

dds_spec = importlib.util.find_spec("mqt.ddsim")

ddsim_installed = dds_spec is not None


@pytest.mark.skipif(not ddsim_installed, reason="MQT DDSIM not installed")
def test_router_prefers_ddsim_when_requested_and_available(monkeypatch):
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

    assert decision.recommended_backend == BackendType.DDSIM, (
        f"Expected DDSIM, got {decision.recommended_backend}"
    )
