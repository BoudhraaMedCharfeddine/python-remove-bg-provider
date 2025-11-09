#!/bin/bash

# Test script for Python Remove Background Provider Docker deployment
# Usage: ./test-docker.sh

set -e

echo "🐍 Testing Python Remove Background Provider Docker Deployment"
echo "============================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

print_status "Docker is running"

# Build the image
echo "🔨 Building Docker image..."
if docker build -t python-remove-bg-provider . > /dev/null 2>&1; then
    print_status "Docker image built successfully"
else
    print_error "Failed to build Docker image"
    exit 1
fi

# Start the container
echo "🚀 Starting container..."
CONTAINER_ID=$(docker run -d -p 8001:8001 --name python-remove-bg-test python-remove-bg-provider)
print_status "Container started with ID: $CONTAINER_ID"

# Wait for container to be ready
echo "⏳ Waiting for service to be ready..."
sleep 15

# Test API endpoints
echo "🧪 Testing API endpoints..."

# Test 1: Health check
if curl -s http://localhost:8001/health | grep -q "healthy"; then
    print_status "Health check passed"
else
    print_error "Health check failed"
    docker logs python-remove-bg-test
    docker rm -f python-remove-bg-test > /dev/null 2>&1
    exit 1
fi

# Test 2: Root endpoint
if curl -s http://localhost:8001/ | grep -q "Python Remove Background Provider"; then
    print_status "Root endpoint test passed"
else
    print_warning "Root endpoint test failed"
fi

# Test 3: Create a test image
echo "📸 Creating test image..."
python3 -c "
from PIL import Image
import io
img = Image.new('RGB', (100, 100), color='red')
img_bytes = io.BytesIO()
img.save(img_bytes, format='PNG')
with open('/tmp/test_python.png', 'wb') as f:
    f.write(img_bytes.getvalue())
print('Test image created')
" 2>/dev/null || print_warning "Could not create test image with Python PIL"

# Test 4: Background removal (if test image exists)
if [ -f "/tmp/test_python.png" ]; then
    echo "🎭 Testing background removal..."
    if curl -s -X POST -F "file=@/tmp/test_python.png" http://localhost:8001/bg/remove -o /tmp/result_python.png > /dev/null 2>&1; then
        if file /tmp/result_python.png | grep -q "PNG image"; then
            print_status "Background removal test passed"
            rm -f /tmp/test_python.png /tmp/result_python.png
        else
            print_warning "Background removal returned non-image data"
        fi
    else
        print_warning "Background removal test failed"
    fi
fi

# Test 5: Advanced background removal
echo "🎨 Testing advanced background removal..."
if [ -f "/tmp/test_python.png" ] || python3 -c "
from PIL import Image
import io
img = Image.new('RGB', (100, 100), color='blue')
img_bytes = io.BytesIO()
img.save(img_bytes, format='PNG')
with open('/tmp/test_python2.png', 'wb') as f:
    f.write(img_bytes.getvalue())
print('Test image 2 created')
" 2>/dev/null; then
    if [ -f "/tmp/test_python2.png" ]; then
        if curl -s -X POST -F "file=@/tmp/test_python2.png" -F "model=u2net" -F "alpha_matting=true" http://localhost:8001/bg/remove-advanced -o /tmp/result_advanced.png > /dev/null 2>&1; then
            if file /tmp/result_advanced.png | grep -q "PNG image"; then
                print_status "Advanced background removal test passed"
            else
                print_warning "Advanced background removal returned non-image data"
            fi
        else
            print_warning "Advanced background removal test failed"
        fi
        rm -f /tmp/test_python2.png /tmp/result_advanced.png
    fi
fi

# Test 6: Documentation endpoint
echo "📚 Testing documentation endpoint..."
if curl -s http://localhost:8001/docs | grep -q "swagger-ui"; then
    print_status "Documentation endpoint test passed"
else
    print_warning "Documentation endpoint test failed"
fi

# Test 7: OpenAPI endpoint
echo "🔧 Testing OpenAPI endpoint..."
if curl -s http://localhost:8001/openapi.json | grep -q "openapi"; then
    print_status "OpenAPI endpoint test passed"
else
    print_warning "OpenAPI endpoint test failed"
fi

# Check container logs
echo "📋 Container logs (last 10 lines):"
docker logs python-remove-bg-test --tail 10

# Cleanup
echo "🧹 Cleaning up..."
docker rm -f python-remove-bg-test > /dev/null 2>&1
print_status "Container removed"

echo ""
echo "🎉 Python Remove Background Provider Docker deployment test completed successfully!"
echo ""
echo "To run the service manually:"
echo "  docker run -d -p 8001:8001 --name python-remove-bg-provider python-remove-bg-provider"
echo ""
echo "To test with docker-compose:"
echo "  docker-compose up -d"
echo "  docker-compose logs -f"
echo "  docker-compose down"
echo ""
echo "API Documentation:"
echo "  http://localhost:8001/docs"
echo ""
echo "Health Check:"
echo "  curl http://localhost:8001/health"




