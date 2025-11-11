# Makefile for Python TTS Project

.PHONY: help install install-dev test test-cov lint format clean docs

help:
	@echo "Python TTS Project - Makefile Commands"
	@echo "======================================="
	@echo "install        - Install package and dependencies"
	@echo "install-dev    - Install package with dev dependencies"
	@echo "test           - Run tests with pytest"
	@echo "test-cov       - Run tests with coverage report"
	@echo "lint           - Run linting (flake8)"
	@echo "format         - Format code (black)"
	@echo "clean          - Remove build artifacts"
	@echo "docs           - Build documentation"
	@echo "run-examples   - Run example scripts"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pip install -e ".[all]"

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

lint:
	flake8 src/ tests/ --max-line-length=100 --exclude=__pycache__

format:
	black src/ tests/ examples/ --line-length=100

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf output/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docs:
	@echo "Building documentation..."
	# sphinx-build -b html docs/ docs/_build/

run-examples:
	@echo "Running basic examples..."
	python examples/basic_usage.py
