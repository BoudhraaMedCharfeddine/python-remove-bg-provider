# Makefile for Python Remove Background Provider

.PHONY: help install dev test test-cov load-test load-test-heavy load-test-stress docker-build docker-run docker-stop docker-clean test-docker compose-up compose-down compose-logs compose-restart clean logs ci-local ci-test ci-lint ci-security ci-docker ci-all ci-script setup-git-hooks

# Default target
help:
	@echo "Python Remove Background Provider - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  make install          Install dependencies"
	@echo "  make dev              Start development server"
	@echo "  make test             Run tests"
	@echo "  make test-cov         Run tests with coverage"
	@echo "  make load-test         Run load test (5 users, 50 requests)"
	@echo "  make load-test-heavy   Run heavy load test (10 users, 100 requests)"
	@echo "  make load-test-stress  Run stress test (20 users, 200 requests)"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build     Build Docker image"
	@echo "  make docker-run       Run Docker container"
	@echo "  make docker-stop      Stop Docker container"
	@echo "  make docker-clean     Remove Docker container and image"
	@echo "  make test-docker      Run automated Docker tests"
	@echo ""
	@echo "Docker Compose:"
	@echo "  make compose-up       Start services with docker-compose"
	@echo "  make compose-down     Stop services with docker-compose"
	@echo "  make compose-logs     View docker-compose logs"
	@echo "  make compose-restart  Restart services with docker-compose"
	@echo ""
	@echo "CI/CD Local Testing:"
	@echo "  make ci-local         Run all CI checks locally"
	@echo "  make ci-test          Run tests (same as CI)"
	@echo "  make ci-lint          Run linting (same as CI)"
	@echo "  make ci-security      Run security checks (same as CI)"
	@echo "  make ci-docker        Run Docker tests (same as CI)"
	@echo "  make ci-script        Run comprehensive CI script"
	@echo "  make ci-all           Run all checks with cleanup"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean            Clean build artifacts and logs"
	@echo "  make logs             View application logs"
	@echo "  make setup-git-hooks  Setup Git pre-commit hooks"

# Development commands
install:
	python3 -m pip install -r requirements.txt

dev:
	python main.py

test:
	pytest

test-cov:
	pytest --cov=main --cov-report=html --cov-report=term-missing

# Load Testing commands
load-test:
	python load_test.py

load-test-heavy:
	python load_test.py --users 10 --requests 100

load-test-stress:
	python load_test.py --users 20 --requests 200

# Docker commands
docker-build:
	docker build -t python-remove-bg-provider .

docker-run:
	docker run -d -p 8001:8001 --name python-remove-bg-provider python-remove-bg-provider

docker-stop:
	docker stop python-remove-bg-provider || true
	docker rm python-remove-bg-provider || true

docker-clean: docker-stop
	docker rmi python-remove-bg-provider || true

test-docker:
	./test-docker.sh

# Docker Compose commands
compose-up:
	docker-compose up -d

compose-down:
	docker-compose down

compose-logs:
	docker-compose logs -f

compose-restart:
	docker-compose down
	docker-compose up -d

# Utility commands
clean:
	rm -rf __pycache__/
	rm -rf *.pyc
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf logs/
	rm -f *.log

logs:
	docker logs python-remove-bg-provider -f

# CI/CD Local Testing Commands
# These commands replicate the GitHub Actions workflows locally

ci-local: ci-lint ci-test ci-security ci-docker
	@echo "✅ All CI checks passed locally!"

ci-test:
	@echo "🧪 Running CI Tests..."
	@echo "Testing with Python 3.11..."
	python -m pytest --cov=main --cov-report=xml --cov-report=term-missing
	@echo "✅ CI Tests completed!"

ci-lint:
	@echo "🔍 Running CI Linting..."
	@echo "Installing linting dependencies..."
	python3 -m pip install flake8 mypy > /dev/null 2>&1 || true
	@echo "Running flake8..."
	python3 -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	python3 -m flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	@echo "Running mypy type checking..."
	python3 -m mypy main.py --ignore-missing-imports
	@echo "✅ CI Linting completed!"

ci-security:
	@echo "🔒 Running CI Security Checks..."
	@echo "Installing security dependencies..."
	python3 -m pip install safety bandit > /dev/null 2>&1 || true
	@echo "Running safety check..."
	python3 -m safety check || echo "⚠️  Safety check completed with warnings"
	@echo "Running bandit security linter..."
	python3 -m bandit -r . -f json -o bandit-report.json || echo "⚠️  Bandit check completed with warnings"
	python3 -m bandit -r . || echo "⚠️  Bandit check completed with warnings"
	@echo "✅ CI Security checks completed!"

ci-docker:
	@echo "🐳 Running CI Docker Tests..."
	@echo "Building Docker image..."
	docker build -t python-remove-bg-provider .
	@echo "Testing Docker container..."
	docker run -d -p 8001:8001 --name ci-test-container python-remove-bg-provider
	@echo "Waiting for service to start..."
	sleep 15
	@echo "Testing health endpoint..."
	curl -f http://localhost:8001/health || (docker stop ci-test-container && docker rm ci-test-container && exit 1)
	@echo "Creating test image..."
	python3 -c "from PIL import Image; import io; img = Image.new('RGB', (100, 100), color='red'); img_bytes = io.BytesIO(); img.save(img_bytes, format='PNG'); open('/tmp/ci_test.png', 'wb').write(img_bytes.getvalue()); print('Test image created')" || (docker stop ci-test-container && docker rm ci-test-container && exit 1)
	@echo "Testing background removal..."
	curl -X POST -F "file=@/tmp/ci_test.png" http://localhost:8001/bg/remove -o /tmp/ci_result.png || (docker stop ci-test-container && docker rm ci-test-container && exit 1)
	@echo "Verifying result..."
	file /tmp/ci_result.png | grep -q "PNG image" || (docker stop ci-test-container && docker rm ci-test-container && exit 1)
	@echo "Cleaning up..."
	docker stop ci-test-container
	docker rm ci-test-container
	rm -f /tmp/ci_test.png /tmp/ci_result.png
	@echo "✅ CI Docker tests completed!"

ci-all: clean ci-local
	@echo "🎉 All CI checks completed successfully!"
	@echo "Ready to push to GitHub! 🚀"

ci-script:
	@echo "🚀 Running comprehensive CI script..."
	./test-ci-local.sh

setup-git-hooks:
	@echo "🔧 Setting up Git hooks..."
	git config core.hooksPath .githooks
	@echo "✅ Git hooks configured!"
	@echo "Pre-commit checks will now run automatically"