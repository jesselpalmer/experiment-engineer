.PHONY: help install install-dev test test-unit test-integration lint format type-check clean run

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package in development mode
	pip install -e .

install-dev: ## Install with development dependencies
	pip install -e ".[dev]"
	pre-commit install

test: ## Run all tests
	pytest

test-unit: ## Run unit tests only
	pytest tests/unit -m unit

test-integration: ## Run integration tests only
	pytest tests/integration -m integration

test-cov: ## Run tests with coverage report
	pytest --cov=src --cov-report=html --cov-report=term

lint: ## Run linters
	ruff check src tests
	mypy src

format: ## Format code with black and isort
	black src tests
	isort src tests

type-check: ## Run type checker
	mypy src

clean: ## Clean build artifacts
	rm -rf build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.pytest_cache" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +

run: ## Run the main example
	python main.py

