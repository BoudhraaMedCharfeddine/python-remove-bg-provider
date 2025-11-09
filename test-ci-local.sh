#!/bin/bash

# CI Local Testing Script for Python Remove Background Provider
# This script replicates the GitHub Actions CI pipeline locally

set -e  # Exit on any error

echo "🚀 Python Remove Background Provider - Local CI Testing"
echo "====================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
print_status "Checking prerequisites..."
if ! command_exists python3; then
    print_error "Python 3 is required but not installed"
    exit 1
fi

if ! command_exists docker; then
    print_error "Docker is required but not installed"
    exit 1
fi

if ! command_exists curl; then
    print_error "curl is required but not installed"
    exit 1
fi

print_success "All prerequisites found"

# Install dependencies
print_status "Installing Python dependencies..."
python3 -m pip install -r requirements.txt > /dev/null 2>&1
python3 -m pip install flake8 mypy safety bandit > /dev/null 2>&1 || true
print_success "Dependencies installed"

# Clean up previous runs
print_status "Cleaning up previous test artifacts..."
rm -rf __pycache__/ .pytest_cache/ htmlcov/ .coverage
rm -f *.pyc *.log bandit-report.json coverage.xml
docker stop ci-test-container > /dev/null 2>&1 || true
docker rm ci-test-container > /dev/null 2>&1 || true
rm -f /tmp/ci_test.png /tmp/ci_result.png
print_success "Cleanup completed"

# Run linting
print_status "Running code linting..."
echo "Running flake8..."
python3 -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
python3 -m flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
echo "Running mypy type checking..."
python3 -m mypy main.py --ignore-missing-imports
print_success "Linting completed"

# Run tests
print_status "Running tests..."
python3 -m pytest --cov=main --cov-report=xml --cov-report=term-missing
print_success "Tests completed"

# Run security checks
print_status "Running security checks..."
echo "Running safety check..."
python3 -m safety check || print_warning "Safety check completed with warnings"
echo "Running bandit security linter..."
python3 -m bandit -r . -f json -o bandit-report.json || print_warning "Bandit check completed with warnings"
python3 -m bandit -r . || print_warning "Bandit check completed with warnings"
print_success "Security checks completed"

# Build Docker image
print_status "Building Docker image..."
docker build -t python-remove-bg-provider .
print_success "Docker image built"

# Test Docker container
print_status "Testing Docker container..."
docker run -d -p 8001:8001 --name ci-test-container python-remove-bg-provider

# Wait for service to start
print_status "Waiting for service to start..."
sleep 20

# Test health endpoint
print_status "Testing health endpoint..."
if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    print_success "Health check passed"
else
    print_error "Health check failed"
    docker stop ci-test-container
    docker rm ci-test-container
    exit 1
fi

# Test root endpoint
print_status "Testing root endpoint..."
if curl -f http://localhost:8001/ > /dev/null 2>&1; then
    print_success "Root endpoint test passed"
else
    print_error "Root endpoint test failed"
    docker stop ci-test-container
    docker rm ci-test-container
    exit 1
fi

# Create test image
print_status "Creating test image..."
python3 -c "
from PIL import Image
import io
img = Image.new('RGB', (100, 100), color='blue')
img_bytes = io.BytesIO()
img.save(img_bytes, format='PNG')
with open('/tmp/ci_test.png', 'wb') as f:
    f.write(img_bytes.getvalue())
print('Test image created')
" || {
    print_error "Failed to create test image"
    docker stop ci-test-container
    docker rm ci-test-container
    exit 1
}

# Test background removal
print_status "Testing background removal..."
if curl -X POST -F "file=@/tmp/ci_test.png" http://localhost:8001/bg/remove -o /tmp/ci_result.png > /dev/null 2>&1; then
    print_success "Background removal test passed"
else
    print_error "Background removal test failed"
    docker stop ci-test-container
    docker rm ci-test-container
    exit 1
fi

# Verify result
print_status "Verifying result..."
if file /tmp/ci_result.png | grep -q "PNG image"; then
    print_success "Result verification passed"
else
    print_error "Result verification failed"
    docker stop ci-test-container
    docker rm ci-test-container
    exit 1
fi

# Test advanced endpoint
print_status "Testing advanced background removal..."
if curl -X POST -F "file=@/tmp/ci_test.png" -F "model=u2net" http://localhost:8001/bg/remove-advanced -o /tmp/ci_result_advanced.png > /dev/null 2>&1; then
    print_success "Advanced background removal test passed"
else
    print_warning "Advanced background removal test failed (this might be expected)"
fi

# Test documentation endpoints
print_status "Testing documentation endpoints..."
if curl -f http://localhost:8001/docs > /dev/null 2>&1; then
    print_success "Documentation endpoint test passed"
else
    print_error "Documentation endpoint test failed"
    docker stop ci-test-container
    docker rm ci-test-container
    exit 1
fi

if curl -f http://localhost:8001/openapi.json > /dev/null 2>&1; then
    print_success "OpenAPI endpoint test passed"
else
    print_error "OpenAPI endpoint test failed"
    docker stop ci-test-container
    docker rm ci-test-container
    exit 1
fi

# Cleanup
print_status "Cleaning up..."
docker stop ci-test-container
docker rm ci-test-container
rm -f /tmp/ci_test.png /tmp/ci_result.png /tmp/ci_result_advanced.png
print_success "Cleanup completed"

# Final report
echo ""
echo "🎉 Local CI Testing Completed Successfully!"
echo "==========================================="
echo "✅ Code linting passed"
echo "✅ Unit tests passed"
echo "✅ Security checks completed"
echo "✅ Docker build successful"
echo "✅ Docker container tests passed"
echo "✅ API endpoints functional"
echo ""
echo "🚀 Ready to push to GitHub!"
echo ""
echo "To run individual CI components:"
echo "  make ci-lint     - Run linting only"
echo "  make ci-test     - Run tests only"
echo "  make ci-security - Run security checks only"
echo "  make ci-docker   - Run Docker tests only"
echo "  make ci-local    - Run all CI checks"
echo "  make ci-all      - Run all checks with cleanup"
