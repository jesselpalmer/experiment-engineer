"""Custom exception hierarchy for ExperimentKit."""


class ExperimentKitError(Exception):
    """Base exception for all ExperimentKit errors."""

    pass


class ConfigurationError(ExperimentKitError):
    """Raised when there's a configuration issue."""

    pass


class LLMError(ExperimentKitError):
    """Raised when there's an error with LLM API calls."""

    pass


class AgentError(ExperimentKitError):
    """Raised when there's an error in agent execution."""

    pass


class WorkflowError(ExperimentKitError):
    """Raised when there's an error in workflow execution."""

    pass

