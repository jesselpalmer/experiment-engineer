# ExperimentKit Architecture

## Overview

ExperimentKit is built with a modular, extensible architecture that supports
multiple agent types, workflow orchestration, and both CLI and web API interfaces.

## Core Components

### Agents

Agents are the core building blocks of ExperimentKit. All agents inherit from
`BaseAgent`, which provides:

- Standardized execution flow (template method pattern)
- Built-in logging and metrics
- Error handling and retry logic
- Input validation hooks
- Post-processing hooks

### Registry

The agent registry allows dynamic discovery and registration of agents. This
enables:

- Plugin-like extensibility
- Runtime agent discovery
- Agent dependency injection

### Workflows

Workflows orchestrate multiple agents in sequence:

- Step dependencies (topological sorting)
- Conditional execution
- Data flow between steps (via `$` references)
- Error handling and recovery
- Result aggregation

See [WORKFLOWS.md](WORKFLOWS.md) for detailed workflow documentation and examples.

### Configuration

Configuration is managed through Pydantic Settings:

- Environment variable support
- Type validation
- Default values
- API key management

## Design Patterns

ExperimentKit uses several well-established design patterns:

- **Strategy Pattern**: Different agent implementations can be swapped
  interchangeably through the BaseAgent interface. This allows runtime
  selection of different agent behaviors.

- **Registry Pattern**: Agent registry system allows dynamic discovery and
  registration of agents. This enables plugin-like extensibility where new
  agents can be added without modifying core code.

- **Factory Pattern**: LLM client factory (`get_llm_client`) creates appropriate
  client instances based on provider string. This abstracts client creation
  and allows easy addition of new providers.

- **Template Method Pattern**: BaseAgent defines the skeleton of agent
  execution (logging, metrics, error handling) with subclasses implementing
  specific `_execute` logic. This ensures consistent behavior across all
  agents.

- **Service Layer Pattern**: Business logic separated from API and data layers.
  Services (`AgentService`, `WorkflowService`) handle orchestration while API
  routes focus on HTTP concerns.

- **Repository Pattern**: Data access layer abstracts database operations (for
  future persistence). Keeps business logic independent of data storage.

- **Dependency Injection**: Configuration and clients injected rather than
  hard-coded. Makes testing easier and allows runtime configuration changes.

- **Observer Pattern**: Metrics and logging hooks allow monitoring systems to
  observe agent execution without modifying agent code.

- **Chain of Responsibility**: Workflow pipeline allows sequential processing
  with error handling at each step. Each step can pass or fail the chain.

## Extending ExperimentKit

### Adding a New Agent

1. Create a class inheriting from `BaseAgent`
2. Implement the `_execute` method
3. Register the agent in the registry

See `examples/custom_agent.py` for a complete example.

### Adding a New Workflow

1. Create a class inheriting from `Workflow`
2. Define steps using `add_step`
3. Set up dependencies and conditions

### Adding a New Agent Category

1. Create a new directory under `src/agents/`
2. Implement agents following the BaseAgent pattern
3. Export from `__init__.py`
4. Register in the main agents `__init__.py`

## Data Flow

```
User Input
    ↓
Workflow/Agent
    ↓
LLM Client (with retry logic)
    ↓
LLM Provider API
    ↓
Response Processing
    ↓
Result (with metrics/logging)
```

## Error Handling

- Custom exception hierarchy
- Retry logic with exponential backoff
- Graceful degradation
- Comprehensive logging

## Observability

- Structured logging (JSON or text)
- Metrics collection (counters, timers, values)
- Optional tracing support
- Request/response tracking

