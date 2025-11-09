# Contributing to Python Remove Background Provider

Thank you for your interest in contributing to Python Remove Background Provider! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Docker Testing](#docker-testing)
- [Submitting Changes](#submitting-changes)
- [Issue Guidelines](#issue-guidelines)
- [Pull Request Guidelines](#pull-request-guidelines)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/python-remove-bg-provider.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose
- Git

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/python-remove-bg-provider.git
   cd python-remove-bg-provider
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install development dependencies:**
   ```bash
   pip install pytest pytest-cov flake8 mypy
   ```

5. **Run the service:**
   ```bash
   python main.py
   ```

### Docker Development

1. **Build the Docker image:**
   ```bash
   docker build -t python-remove-bg-provider .
   ```

2. **Run with Docker:**
   ```bash
   docker run -d -p 8001:8001 --name python-remove-bg-provider python-remove-bg-provider
   ```

3. **Or use Docker Compose:**
   ```bash
   docker-compose up -d
   ```

## Making Changes

### Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused

### File Structure

```
python-remove-bg-provider/
├── main.py                 # Main FastAPI application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── test-docker.sh         # Docker test script
├── Makefile              # Development commands
├── tests/                # Test files
├── .github/              # GitHub workflows and templates
└── README.md             # Project documentation
```

## Testing

### Unit Tests

Run the test suite:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=main --cov-report=html
```

### Linting

Check code style:
```bash
flake8 .
```

Type checking:
```bash
mypy main.py
```

### Test Coverage

We aim for at least 80% test coverage. Run coverage analysis:
```bash
pytest --cov=main --cov-report=term-missing --cov-report=html
```

## Docker Testing

### Automated Docker Tests

Run the comprehensive Docker test suite:
```bash
./test-docker.sh
```

### Manual Docker Testing

1. **Build and test:**
   ```bash
   make docker-build
   make docker-run
   ```

2. **Test endpoints:**
   ```bash
   curl http://localhost:8001/health
   curl -X POST -F "file=@test.png" http://localhost:8001/bg/remove -o result.png
   ```

3. **Clean up:**
   ```bash
   make docker-clean
   ```

## Submitting Changes

### Commit Messages

Use clear and descriptive commit messages:

```
feat: add support for new rembg model
fix: resolve memory leak in background removal
docs: update API documentation
test: add unit tests for image processing
```

### Branch Naming

Use descriptive branch names:
- `feature/add-new-model`
- `fix/memory-leak`
- `docs/update-readme`
- `test/add-coverage`

## Issue Guidelines

### Before Creating an Issue

1. Search existing issues to avoid duplicates
2. Check if it's already been reported
3. Verify you're using the latest version

### Bug Reports

When reporting bugs, please include:

- **Version**: What version are you running?
- **Environment**: Docker, local Python, etc.
- **Steps to reproduce**: Clear steps to reproduce the issue
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Logs**: Relevant error logs
- **Screenshots**: If applicable

### Feature Requests

When requesting features, please include:

- **Problem**: What problem does this solve?
- **Solution**: Describe your proposed solution
- **Alternatives**: Any alternative solutions considered
- **Use case**: How would this feature be used?
- **Additional context**: Any other relevant information

## Pull Request Guidelines

### Before Submitting

1. **Test your changes:**
   - Run unit tests: `pytest`
   - Run Docker tests: `./test-docker.sh`
   - Test manually with different images

2. **Update documentation:**
   - Update README if needed
   - Add/update docstrings
   - Update API documentation

3. **Check code quality:**
   - Run linting: `flake8 .`
   - Check types: `mypy main.py`
   - Ensure good test coverage

### PR Description

Include in your PR description:

- **What**: Brief description of changes
- **Why**: Reason for the changes
- **How**: How you implemented the changes
- **Testing**: How you tested the changes
- **Screenshots**: If applicable

### Review Process

1. All PRs require review
2. CI/CD must pass
3. Code must meet quality standards
4. Tests must pass
5. Documentation must be updated

## Development Commands

### Using Makefile

```bash
make help              # Show all available commands
make install           # Install dependencies
make dev               # Start development server
make test              # Run tests
make test-cov          # Run tests with coverage
make docker-build      # Build Docker image
make docker-run        # Run Docker container
make docker-test       # Run Docker tests
make compose-up        # Start with Docker Compose
make compose-down      # Stop Docker Compose
make clean             # Clean build artifacts
```

### Manual Commands

```bash
# Development
python main.py                    # Start service
pytest                           # Run tests
pytest --cov=main                # Run with coverage
flake8 .                         # Check code style
mypy main.py                     # Type checking

# Docker
docker build -t python-remove-bg-provider .
docker run -d -p 8001:8001 python-remove-bg-provider
docker-compose up -d
./test-docker.sh
```

## Getting Help

- **Documentation**: Check the README.md
- **Issues**: Search existing issues or create a new one
- **Discussions**: Use GitHub Discussions for questions
- **API Docs**: Visit http://localhost:8001/docs when running the service

## Release Process

1. Update version in relevant files
2. Update CHANGELOG.md
3. Create a release tag
4. GitHub Actions will automatically build and publish Docker images

## License

By contributing to Python Remove Background Provider, you agree that your contributions will be licensed under the same license as the project.




