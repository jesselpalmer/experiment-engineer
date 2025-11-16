# Contributing to ExperimentKit

Thank you for your interest in contributing to ExperimentKit! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/experimentkit.git`
3. Create a virtual environment: `python -m venv .venv`
4. Activate it: `source .venv/bin/activate` (or `venv\Scripts\activate` on Windows)
5. Install in development mode: `make install-dev` or `pip install -e ".[dev]"`
6. Create a branch for your changes: `git checkout -b feature/your-feature-name`

## Development Setup

After installing development dependencies, pre-commit hooks will be installed automatically. These will run code formatting and linting checks before each commit.

## Code Style

- We use **Black** for code formatting (line length: 100)
- We use **isort** for import sorting (Black profile)
- We use **ruff** for linting
- We use **mypy** for type checking

Run `make format` to automatically format your code.

## Testing

- Write tests for new features
- Ensure all tests pass: `make test`
- Run unit tests only: `make test-unit`
- Run integration tests only: `make test-integration`
- Check coverage: `make test-cov`

## Pull Request Process

1. Update the README.md or documentation if needed
2. Add tests for new functionality
3. Ensure all tests pass and code is properly formatted
4. Update CHANGELOG.md with your changes
5. Submit a pull request with a clear description

## Architecture

See the main README.md for architecture overview. Key principles:

- Agents inherit from `BaseAgent`
- Use the registry system for agent discovery
- Follow the workflow pattern for multi-step processes
- Use Pydantic models for structured data
- Logging and metrics are built-in

## Questions?

Open an issue for questions or discussions about contributions.

