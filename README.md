# ExperimentKit

Open-source agentic infrastructure for planning, running, and evaluating product
experiments.

## Features

- **Agent-Based Architecture**: Extensible agent system with base classes and
  registry
- **Multi-Provider LLM Support**: Works with OpenAI, Anthropic, and Mistral
- **Workflow Orchestration**: Build multi-step experiment workflows with
  dependencies, conditional execution, and data flow between steps
- **Production Ready**: Logging, metrics, error handling, and retry logic
- **CLI Interface**: Command-line tools for quick experimentation
- **Web API**: FastAPI-based REST API for integration
- **Type Safe**: Full type hints and Pydantic models

## Setup

1. Ensure that you have **Python 3.10+** installed.

```bash
python -V
```

2. (Recommended) Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate     # On Windows: venv\Scripts\activate

```

3. Install the package:

```bash
# For development (includes dev dependencies)
pip install -e ".[dev]"

# Or for production only
pip install -e .
```

   **Note:** Dependencies are managed in `pyproject.toml`. The `[dev]` extra
   includes testing, linting, and development tools.

4. **Configure API Keys**

   ExperimentKit requires API keys from at least one LLM provider to
   function. Supported providers:

   - **OpenAI** (default) - Get your API key from
     [OpenAI Platform](https://platform.openai.com/api-keys)
   - **Anthropic** - Get your API key from
     [Anthropic Console](https://console.anthropic.com/)
   - **Mistral** - Get your API key from
     [Mistral AI Platform](https://console.mistral.ai/)

   Create a `.env` file in the project root directory:

   ```bash
   # .env file
   OPENAI_API_KEY=your_openai_api_key_here
   # ANTHROPIC_API_KEY=your_anthropic_api_key_here
   # MISTRAL_API_KEY=your_mistral_api_key_here
   ```

   **Note:** You only need to set the API key for the provider(s) you plan
   to use. The default provider is OpenAI. Uncomment and set the API keys
   for other providers if you want to use them.

   **Security:** Never commit your `.env` file to version control. It
   should already be in `.gitignore`.

## Usage

### Command Line Interface

```bash
# Refine a hypothesis
experimentkit refine \
  "Users who see personalized onboarding screens are more likely to upgrade."

# Analyze a hypothesis
experimentkit analyze "Refined hypothesis text here"

# Run the complete workflow
experimentkit workflow "Your hypothesis here"

# Show configuration
experimentkit config
```

### Python API

```python
from src.workflows.hypothesis import HypothesisRefinementWorkflow

# Run the complete workflow
workflow = HypothesisRefinementWorkflow()
result = workflow.execute(initial_inputs={"hypothesis": "Your hypothesis"})

print(result.steps["refine"]["result"])  # Refined hypothesis
print(result.steps["analyze"]["result"])  # Analysis
print(result.steps["revise"]["result"])  # Revised hypothesis
```

### Using Individual Agents

```python
from src.agents import hypothesis_refiner, hypothesis_analyzer, hypothesis_reviser

# Refine a hypothesis
refined = hypothesis_refiner("Your hypothesis")

# Analyze it
analysis = hypothesis_analyzer(refined)

# Revise based on analysis
revised = hypothesis_reviser(refined, analysis)
```

### Web API

Start the API server:

```bash
uvicorn src.api.app:create_app --reload
```

Then access the API at `http://localhost:8000`:

- `GET /api/v1/agents/list` - List available agents
- `POST /api/v1/agents/execute` - Execute an agent
- `POST /api/v1/workflows/hypothesis-refinement/execute` - Run workflow

See the interactive API docs at `http://localhost:8000/docs`.

### Building Custom Workflows

Create multi-step workflows with dependencies and conditional execution:

```python
from src.workflows.workflow import Workflow

class MyWorkflow(Workflow):
    def __init__(self):
        super().__init__("my_workflow")
        
        self.add_step(
            name="step1",
            agent_name="agent1",
            inputs={"data": "$input"},
        ).add_step(
            name="step2",
            agent_name="agent2",
            inputs={"data": "$step1"},  # Uses result from step1
            depends_on=["step1"],  # Must run after step1
        )
```

See [docs/WORKFLOWS.md](docs/WORKFLOWS.md) for detailed workflow documentation.

## Project Structure

```bash
experimentkit/
├── src/
│   ├── agents/          # Agent implementations
│   │   └── hypothesis/  # Hypothesis-related agents
│   ├── api/             # FastAPI web application
│   ├── config/          # Configuration management
│   ├── core/             # Core components (agents, registry, etc.)
│   ├── models/           # Pydantic data models
│   ├── services/         # Service layer
│   ├── utils/            # Utility functions
│   └── workflows/        # Workflow orchestration
├── tests/                # Test suite
├── examples/             # Example scripts
└── docs/                 # Documentation
```

## Development

### Running Tests

```bash
# All tests
make test

# Unit tests only
make test-unit

# Integration tests only
make test-integration

# With coverage
make test-cov
```

### Code Quality

```bash
# Format code
make format

# Run linters
make lint

# Type checking
make type-check
```

### Pre-commit Hooks

Pre-commit hooks are automatically installed with development dependencies.
They will run formatting, linting, and type checking before each commit.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to
ExperimentKit.

## License

MIT License - see [LICENSE](LICENSE) for details.
