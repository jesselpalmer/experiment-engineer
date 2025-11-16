# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-XX

### Added

- Initial release of ExperimentKit
- Base agent architecture with `BaseAgent` abstract class
- Agent registry system for dynamic discovery
- Configuration management with Pydantic Settings
- Hypothesis refinement agents:
  - `HypothesisRefinerAgent` - Refines hypotheses
  - `HypothesisAnalyzerAgent` - Analyzes hypotheses
  - `HypothesisReviserAgent` - Revises hypotheses based on feedback
- Workflow orchestration system
- LLM client utilities with support for OpenAI, Anthropic, and Mistral
- Retry logic with exponential backoff for API calls
- Structured logging infrastructure
- Metrics collection system
- CLI interface with Click
- Comprehensive test infrastructure
- Pre-commit hooks for code quality
- Documentation and contribution guidelines

### Changed

- Refactored from simple functions to class-based agent architecture
- Improved error handling with custom exception hierarchy
- Enhanced type safety throughout the codebase

