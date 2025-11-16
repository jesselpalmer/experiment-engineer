"""ExperimentKit - A toolkit for hypothesis refinement and experiment design."""

from .agents import (
    HypothesisAnalyzerAgent,
    HypothesisRefinerAgent,
    HypothesisReviserAgent,
    hypothesis_analyzer,
    hypothesis_refiner,
    hypothesis_reviser,
)
from .core import (
    AgentError,
    AgentRegistry,
    BaseAgent,
    ConfigurationError,
    ExperimentKitError,
    LLMError,
    WorkflowError,
    get_logger,
    get_metrics,
    get_registry,
    setup_logging,
)
from .workflows import (
    HypothesisRefinementWorkflow,
    Pipeline,
    Workflow,
    WorkflowStep,
)

__version__ = "0.1.0"

__all__ = [
    # Agents
    "HypothesisRefinerAgent",
    "HypothesisAnalyzerAgent",
    "HypothesisReviserAgent",
    "hypothesis_refiner",
    "hypothesis_analyzer",
    "hypothesis_reviser",
    # Core
    "BaseAgent",
    "AgentRegistry",
    "get_registry",
    "ExperimentKitError",
    "AgentError",
    "LLMError",
    "ConfigurationError",
    "WorkflowError",
    "get_logger",
    "setup_logging",
    "get_metrics",
    # Workflows
    "Workflow",
    "WorkflowStep",
    "Pipeline",
    "HypothesisRefinementWorkflow",
]
