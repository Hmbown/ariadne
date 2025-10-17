"""Ariadne: intelligent quantum circuit routing."""

from ._version import __version__

__all__ = ["__version__"]

# Configuration system data classes
from .config import (
    AnalysisConfig,
    AriadneConfig,
    BackendConfig,
    ConfigManager,
    ErrorMitigationConfig,
    OptimizationConfig,
    PerformanceConfig,
    configure_ariadne,
    get_config,
    get_config_manager,
)

# Core systems - always available
from .core import (
    AriadneError,
    BackendUnavailableError,
    CircuitAnalysisCache,
    CircuitTooLargeError,
    ResourceExhaustionError,
    ResourceManager,
    SimulationError,
    configure_logging,
    get_logger,
    get_resource_manager,
)

# Enhanced router
from .route.enhanced_router import EnhancedQuantumRouter

# NEW: Comprehensive routing tree
from .route.routing_tree import (
    ComprehensiveRoutingTree,
    RoutingStrategy,
    explain_routing,
    get_routing_tree,
    route_with_tree,
    show_routing_tree,
)

# Main simulation interface
from .router import simulate
from .types import BackendCapacity, BackendType, RoutingDecision, SimulationResult

# Create alias for backward compatibility
QuantumRouter = EnhancedQuantumRouter

# Optional backends - may not be available
try:
    from .backends.cuda_backend import CUDABackend, get_cuda_info, simulate_cuda

    _CUDA_AVAILABLE = True
except ImportError:
    _CUDA_AVAILABLE = False
    CUDABackend = None
    get_cuda_info = None
    simulate_cuda = None

try:
    from .backends.metal_backend import MetalBackend, get_metal_info, simulate_metal

    _METAL_AVAILABLE = True
except ImportError:
    _METAL_AVAILABLE = False
    MetalBackend = None
    get_metal_info = None
    simulate_metal = None

__all__ = [
    # Core functionality
    "simulate",
    "BackendType",
    "RoutingDecision",
    "SimulationResult",
    "BackendCapacity",
    "EnhancedQuantumRouter",
    "QuantumRouter",  # Alias for backward compatibility
    # NEW: Comprehensive routing tree
    "ComprehensiveRoutingTree",
    "RoutingStrategy", 
    "explain_routing",
    "get_routing_tree",
    "route_with_tree",
    "show_routing_tree",
    # Configuration system
    "AriadneConfig",
    "BackendConfig",
    "OptimizationConfig",
    "ErrorMitigationConfig",
    "AnalysisConfig",
    "PerformanceConfig",
    "ConfigManager",
    "get_config",
    "get_config_manager",
    "configure_ariadne",
    # Error handling
    "AriadneError",
    "BackendUnavailableError",
    "CircuitTooLargeError",
    "ResourceExhaustionError",
    "SimulationError",
    # Core systems
    "CircuitAnalysisCache",
    "ResourceManager",
    "get_logger",
    "get_resource_manager",
    "configure_logging",
]

# Add optional backends if available
if _CUDA_AVAILABLE:
    __all__.extend(
        [
            "CUDABackend",
            "simulate_cuda",
            "get_cuda_info",
        ]
    )

if _METAL_AVAILABLE:
    __all__.extend(
        [
            "MetalBackend",
            "simulate_metal",
            "get_metal_info",
        ]
    )
