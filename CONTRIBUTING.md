# Contributing to Python TTS

Thank you for your interest in contributing to Python TTS! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Style](#code-style)
- [Commit Messages](#commit-messages)
- [Pull Requests](#pull-requests)

## Code of Conduct

This project follows a Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/py-tts.git
   cd py-tts
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/optrader8/py-tts.git
   ```

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Make (optional, for convenience)

### Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e ".[dev,all]"

# Install pre-commit hooks (optional)
pre-commit install
```

### Verify Setup

```bash
# Run tests
pytest tests/

# Check code style
make lint

# Format code
make format
```

## Making Changes

### Create a Branch

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create a feature branch
git checkout -b feature/your-feature-name
```

### Branch Naming Convention

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test improvements
- `chore/` - Maintenance tasks

### Development Workflow

1. **Make your changes**
   - Write code following our style guidelines
   - Add tests for new features
   - Update documentation as needed

2. **Test your changes**
   ```bash
   # Run all tests
   pytest tests/ -v

   # Run specific test
   pytest tests/test_engines.py -v

   # Run with coverage
   pytest tests/ --cov=src
   ```

3. **Check code quality**
   ```bash
   # Lint
   flake8 src/ tests/

   # Format
   black src/ tests/ examples/

   # Type check
   mypy src/
   ```

## Testing

### Writing Tests

- Place tests in `tests/` directory
- Follow naming convention: `test_*.py`
- Use pytest fixtures for common setup
- Aim for >80% code coverage

### Test Structure

```python
import pytest
from src.module import YourClass

class TestYourClass:
    """Tests for YourClass."""

    @pytest.fixture
    def instance(self):
        """Create instance for testing."""
        return YourClass()

    def test_feature(self, instance):
        """Test specific feature."""
        result = instance.method()
        assert result == expected
```

### Running Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_engines.py

# Specific test
pytest tests/test_engines.py::TestBaseTTSEngine::test_synthesize

# With coverage
pytest --cov=src --cov-report=html

# Verbose mode
pytest -v

# Stop on first failure
pytest -x
```

## Code Style

### Python Style Guide

- Follow PEP 8
- Use Black for formatting (line length: 100)
- Use type hints where possible
- Write docstrings for all public functions/classes

### Docstring Format

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of function.

    Longer description if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: Description of when this is raised

    Example:
        >>> function_name("test", 42)
        True
    """
    pass
```

### Import Order

1. Standard library imports
2. Third-party imports
3. Local application imports

Use `isort` to automatically organize imports:

```bash
isort src/ tests/
```

## Commit Messages

### Format

```
type(scope): Short description

Longer description if needed.

- Bullet points for details
- Can span multiple lines

Fixes #123
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Maintenance tasks

### Examples

```
feat(engines): Add support for new TTS engine

- Implement NewTTSEngine class
- Add configuration options
- Update documentation

Closes #45
```

```
fix(preprocessing): Fix Korean text normalization

Fixed bug where numbers weren't being converted correctly
for Korean text.

Fixes #78
```

## Pull Requests

### Before Submitting

- [ ] Tests pass (`pytest tests/`)
- [ ] Code is formatted (`black src/ tests/`)
- [ ] Linting passes (`flake8 src/ tests/`)
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated (for significant changes)

### Submission Process

1. **Push your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request** on GitHub
   - Use a clear title
   - Describe your changes
   - Link related issues
   - Add screenshots if applicable

3. **PR Template**
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing
   Describe how you tested your changes

   ## Checklist
   - [ ] Tests pass
   - [ ] Code formatted
   - [ ] Documentation updated
   - [ ] CHANGELOG updated
   ```

### Review Process

- Maintainers will review your PR
- Address any requested changes
- Once approved, maintainer will merge

### After Merge

```bash
# Update your main branch
git checkout main
git pull upstream main

# Delete feature branch
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

## Adding New Features

### New TTS Engine

1. Create file in `src/engines/`
2. Inherit from `BaseTTSEngine`
3. Implement required methods
4. Add tests in `tests/test_engines.py`
5. Update documentation

### New Preprocessing Module

1. Create file in `src/preprocessing/`
2. Implement processing logic
3. Add tests
4. Update `__init__.py`

## Documentation

### Building Docs

```bash
# Install docs dependencies
pip install -e ".[docs]"

# Build docs
make docs

# View docs
open docs/_build/index.html
```

### Documentation Style

- Use Markdown for guides
- Use docstrings for API documentation
- Include examples where helpful
- Keep it clear and concise

## Getting Help

- **Questions**: Open a Discussion on GitHub
- **Bugs**: Create an Issue with bug template
- **Features**: Create an Issue with feature template
- **Chat**: Join our Discord (if available)

## Resources

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Black Documentation](https://black.readthedocs.io/)
- [Type Hints (PEP 484)](https://www.python.org/dev/peps/pep-0484/)

## Recognition

Contributors will be acknowledged in:
- README.md
- Release notes
- Contributors page

Thank you for contributing to Python TTS!
