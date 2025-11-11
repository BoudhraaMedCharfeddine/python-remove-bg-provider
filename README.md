# Python Remove Background Provider

A FastAPI service for background removal using Python's `rembg` library.

## Features

- 🚀 **FastAPI** - Modern, fast web framework
- 🔐 **X-API-Key Authentication** - Secure API access control
- 🎨 **Multiple Models** - Support for different rembg models
- ⚡ **High Performance** - Optimized for production use
- 🔧 **Configurable** - Alpha matting and advanced options
- 📊 **Health Checks** - Built-in monitoring endpoints
- 🌐 **CORS Support** - Configurable cross-origin resource sharing
- 🧪 **Comprehensive Testing** - 70+ tests with 86% code coverage

## Installation

1. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp env.example .env
# Edit .env with your configuration
```

**Important Security Configuration:**
- Set `X_API_KEY` to a secure random string for API authentication
- Configure `ALLOWED_ORIGINS` with your domain(s) for CORS security
- Example: `ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com`

## Docker Usage

### Quick Start with Docker

#### Build and Run with Docker
```bash
# Build the Docker image
docker build -t python-remove-bg-provider .

# Run the container
docker run -d -p 8001:8001 --name python-remove-bg-provider python-remove-bg-provider

# Check if container is running
docker ps

# View logs
docker logs python-remove-bg-provider
```

#### Docker Commands

##### Using Makefile (Recommended)
```bash
# Build Docker image
make docker-build

# Run container
make docker-run

# Stop container
make docker-stop

# Clean up (remove container and image)
make docker-clean

# Run automated tests
make test-docker

# Show all available commands
make help
```

##### Using Docker directly
```bash
# Stop the container
docker stop python-remove-bg-provider

# Start the container
docker start python-remove-bg-provider

# Remove the container
docker rm python-remove-bg-provider

# Remove the image
docker rmi python-remove-bg-provider
```

#### Docker Compose (Recommended)
```bash
# Start services
make compose-up

# View logs
make compose-logs

# Stop services
make compose-down

# Restart services
make compose-restart
```

Or using docker-compose directly:
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### Testing Docker Deployment

##### Automated Testing
```bash
# Run automated Docker test script
./test-docker.sh
```

##### Manual Testing
```bash
# Test the API is working
curl http://localhost:8001/health

# Test background removal
curl -X POST -F "file=@sample.jpg" http://localhost:8001/bg/remove -o result.png

# Test advanced background removal
curl -X POST -F "file=@sample.jpg" -F "model=u2net" -F "alpha_matting=true" http://localhost:8001/bg/remove-advanced -o result_advanced.png

# View API documentation
open http://localhost:8001/docs
```

#### Docker Usage Examples

##### Basic Usage
```bash
# Start the service
docker-compose up -d

# Check service status
curl http://localhost:8001/health

# Remove background from an image
curl -X POST -F "file=@your-image.jpg" http://localhost:8001/bg/remove -o output.png
```

##### Advanced Usage with Custom Models
```bash
# Use specific rembg model
curl -X POST -F "file=@image.jpg" -F "model=u2net_human_seg" http://localhost:8001/bg/remove-advanced -o result.png

# Enable alpha matting for better edge quality
curl -X POST -F "file=@image.jpg" -F "alpha_matting=true" -F "alpha_matting_foreground_threshold=240" http://localhost:8001/bg/remove-advanced -o result.png

# Use ISNet model for general use
curl -X POST -F "file=@image.jpg" -F "model=isnet-general-use" http://localhost:8001/bg/remove-advanced -o result.png
```

##### Batch Processing
```bash
# Process multiple images
for image in *.jpg; do
  curl -X POST -F "file=@$image" http://localhost:8001/bg/remove -o "${image%.*}_bg_removed.png"
done
```

##### Using with Different Programming Languages

**Python:**
```python
import requests

# Remove background
with open('image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8001/bg/remove', files=files)
    
with open('result.png', 'wb') as f:
    f.write(response.content)
```

**JavaScript/Node.js:**
```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const form = new FormData();
form.append('file', fs.createReadStream('image.jpg'));

axios.post('http://localhost:8001/bg/remove', form, {
  headers: form.getHeaders(),
  responseType: 'arraybuffer'
}).then(response => {
  fs.writeFileSync('result.png', response.data);
});
```

**cURL with Progress:**
```bash
# Show upload/download progress
curl -X POST -F "file=@large-image.jpg" http://localhost:8001/bg/remove -o result.png --progress-bar
```

#### Available Models

The service supports multiple rembg models for different use cases:

| Model | Best For | Size | Quality | Speed |
|-------|----------|------|---------|-------|
| `u2net` | General purpose (default) | ~176MB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| `u2net_human_seg` | Human portraits | ~176MB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| `silueta` | Silhouettes | ~176MB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| `isnet-general-use` | General use (newer) | ~176MB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**Model Selection Examples:**
```bash
# For portraits and people
curl -X POST -F "file=@portrait.jpg" -F "model=u2net_human_seg" http://localhost:8001/bg/remove-advanced -o portrait_bg_removed.png

# For general images
curl -X POST -F "file=@product.jpg" -F "model=u2net" http://localhost:8001/bg/remove-advanced -o product_bg_removed.png

# For silhouettes
curl -X POST -F "file=@silhouette.jpg" -F "model=silueta" http://localhost:8001/bg/remove-advanced -o silhouette_bg_removed.png
```

#### Docker Environment Variables

You can customize the service behavior using environment variables:

```bash
# Run with custom environment variables
docker run -d -p 8001:8001 \
  -e HOST=0.0.0.0 \
  -e PORT=8001 \
  -e LOG_LEVEL=INFO \
  --name python-remove-bg-provider \
  python-remove-bg-provider
```

**Available Environment Variables:**
- `HOST`: Server host (default: `0.0.0.0`)
- `PORT`: Server port (default: `8001`)
- `LOG_LEVEL`: Logging level - DEBUG, INFO, WARNING, ERROR (default: `INFO`)

**Docker Compose with Environment Variables:**
```yaml
services:
  python-remove-bg-provider:
    image: python-remove-bg-provider
    ports:
      - "8001:8001"
    environment:
      - HOST=0.0.0.0
      - PORT=8001
      - LOG_LEVEL=INFO
    restart: unless-stopped
```

**Using Environment File:**
```bash
# Copy the example environment file
cp docker.env.example .env

# Edit the environment variables
nano .env

# Run with environment file
docker run -d -p 8001:8001 --env-file .env --name python-remove-bg-provider python-remove-bg-provider
```

Or with docker-compose:
```yaml
services:
  python-remove-bg-provider:
    image: python-remove-bg-provider
    ports:
      - "8001:8001"
    env_file:
      - .env
    restart: unless-stopped
```

#### Docker Production Deployment
```bash
# Build for production
docker build -t python-remove-bg-provider:latest .

# Run with production settings
docker run -d \
  --name python-remove-bg-provider \
  --restart unless-stopped \
  -p 8001:8001 \
  -e LOG_LEVEL=INFO \
  python-remove-bg-provider:latest

# Monitor container
docker stats python-remove-bg-provider
```

#### Docker Troubleshooting
```bash
# Check container status
docker ps -a

# View detailed logs
docker logs python-remove-bg-provider --tail 100

# Access container shell
docker exec -it python-remove-bg-provider bash

# Check container resources
docker stats python-remove-bg-provider

# Restart container
docker restart python-remove-bg-provider

# Remove and recreate
docker rm -f python-remove-bg-provider
docker run -d -p 8001:8001 --name python-remove-bg-provider python-remove-bg-provider
```

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment:

### Workflows

- **CI Pipeline** (`ci.yml`): Runs on every push and pull request
  - Unit tests with pytest across Python 3.11 and 3.12
  - Coverage reporting with pytest
- **Code Quality Analysis** (`codeql.yml`): Static analysis via GitHub CodeQL on pushes, PRs, and weekly schedule

### Status Badges

[![CI Pipeline](https://github.com/your-username/python-remove-bg-provider/workflows/CI%20Pipeline/badge.svg)](https://github.com/your-username/python-remove-bg-provider/actions)
[![CodeQL](https://github.com/your-username/python-remove-bg-provider/workflows/CodeQL/badge.svg)](https://github.com/your-username/python-remove-bg-provider/actions)

### Local CI Testing

Test all CI checks locally before pushing to GitHub:

**Quick CI Check:**
```bash
make ci-local
```

**Comprehensive CI Script:**
```bash
make ci-script
```

**Individual CI Components:**
```bash
make ci-lint      # Code linting (flake8, mypy)
make ci-test      # Unit tests with coverage
make ci-security  # Security checks (safety, bandit)
make ci-docker    # Optional local Docker build and container tests
```

**Full CI with Cleanup:**
```bash
make ci-all       # Clean + all CI checks
```

**Setup Git Hooks:**
```bash
make setup-git-hooks  # Enable pre-commit checks
```

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

### Load Testing

The project includes comprehensive load testing capabilities:

**Quick Load Test:**
```bash
make load-test
```

**Heavy Load Test:**
```bash
make load-test-heavy
```

**Stress Test:**
```bash
make load-test-stress
```

**Custom Load Test:**
```bash
python load_test.py --url http://localhost:8001 --users 15 --requests 150 --endpoint /bg/remove
```

The load testing script provides detailed metrics including:
- Requests per second
- Response time percentiles (95th, 99th)
- Success rates
- Error analysis
- Performance recommendations

## Usage

### Start the service:
```bash
python main.py
```

The service will start on `http://localhost:8001` by default.

### Authentication

The API uses X-API-Key authentication for all endpoints except health checks:

```bash
# Include the API key in your requests
curl -H "X-API-Key: your-secret-api-key-here" \
     -X POST "http://localhost:8001/bg/remove" \
     -F "file=@image.jpg"
```

**Security Notes:**
- Set `X_API_KEY` in your `.env` file
- If no API key is configured, the service will log a warning but remain accessible (development mode)
- Always use HTTPS in production
- Keep your API key secure and rotate it regularly

### API Endpoints

#### 1. Health Check
```bash
curl http://localhost:8001/health
```

#### 2. Remove Background (Simple)
```bash
curl -X POST "http://localhost:8001/bg/remove" \
  -H "accept: image/png" \
  -H "X-API-Key: your-secret-api-key-here" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@input.jpg" \
  -F "model=u2net" \
  --output output.png
```

#### 3. Remove Background (Advanced)
```bash
curl -X POST "http://localhost:8001/bg/remove-advanced" \
  -H "accept: image/png" \
  -H "X-API-Key: your-secret-api-key-here" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@input.jpg" \
  -F "model=u2net" \
  -F "alpha_matting=true" \
  -F "alpha_matting_foreground_threshold=240" \
  --output output.png
```

#### 4. List Available Models
```bash
curl -H "X-API-Key: your-secret-api-key-here" \
     http://localhost:8001/models
```

### Available Models

- **u2net** - General purpose model (default)
- **u2net_human_seg** - Optimized for human subjects
- **silueta** - Good for portraits and people
- **isnet-general-use** - High quality general purpose model

## Usage Examples

### Python Client Example

```python
import requests

# Configure your API key
API_KEY = "your-secret-api-key-here"
BASE_URL = "http://localhost:8001"

# Headers for authentication
headers = {
    "X-API-Key": API_KEY
}

# Remove background from an image
def remove_background(image_path, output_path):
    with open(image_path, 'rb') as f:
        files = {'file': f}
        data = {'model': 'u2net'}
        
        response = requests.post(
            f"{BASE_URL}/bg/remove",
            files=files,
            data=data,
            headers=headers
        )
        
        if response.status_code == 200:
            with open(output_path, 'wb') as out_f:
                out_f.write(response.content)
            print(f"Background removed successfully: {output_path}")
        else:
            print(f"Error: {response.status_code} - {response.text}")

# List available models
def list_models():
    response = requests.get(f"{BASE_URL}/models", headers=headers)
    if response.status_code == 200:
        models = response.json()['models']
        for model in models:
            print(f"- {model['name']}: {model['description']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Usage
list_models()
remove_background("input.jpg", "output.png")
```

### JavaScript/Node.js Example

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const API_KEY = 'your-secret-api-key-here';
const BASE_URL = 'http://localhost:8001';

const headers = {
    'X-API-Key': API_KEY
};

async function removeBackground(inputPath, outputPath) {
    const form = new FormData();
    form.append('file', fs.createReadStream(inputPath));
    form.append('model', 'u2net');
    
    try {
        const response = await axios.post(`${BASE_URL}/bg/remove`, form, {
            headers: {
                ...form.getHeaders(),
                ...headers
            },
            responseType: 'stream'
        });
        
        response.data.pipe(fs.createWriteStream(outputPath));
        console.log(`Background removed successfully: ${outputPath}`);
    } catch (error) {
        console.error('Error:', error.response?.data || error.message);
    }
}

async function listModels() {
    try {
        const response = await axios.get(`${BASE_URL}/models`, { headers });
        response.data.models.forEach(model => {
            console.log(`- ${model.name}: ${model.description}`);
        });
    } catch (error) {
        console.error('Error:', error.response?.data || error.message);
    }
}

// Usage
listModels();
removeBackground('input.jpg', 'output.png');
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `8001` | Server port |
| `X_API_KEY` | - | **Required** - API key for authentication |
| `ALLOWED_ORIGINS` | `*` | Comma-separated list of allowed CORS origins |
| `LOG_LEVEL` | `INFO` | Logging level |
| `MAX_FILE_SIZE` | `10485760` | Maximum file size in bytes (10MB) |
| `REQUEST_TIMEOUT` | `300` | Request timeout in seconds (5 minutes) |

### Authentication & Security

The API uses X-API-Key authentication for all endpoints except health checks:

**Required Headers:**
```
X-API-Key: your-secret-api-key-here
```

**Security Best Practices:**
- Use a strong, randomly generated API key (32+ characters)
- Store the API key securely in environment variables
- Rotate API keys regularly
- Use HTTPS in production
- Configure `ALLOWED_ORIGINS` to restrict CORS access

**Development Mode:**
If no `X_API_KEY` is set, the service will log a warning but remain accessible for development purposes.

### Alpha Matting Options

For better edge quality, enable alpha matting:

- `alpha_matting`: Enable/disable alpha matting
- `alpha_matting_foreground_threshold`: Foreground threshold (0-255)
- `alpha_matting_background_threshold`: Background threshold (0-255)
- `alpha_matting_erode_size`: Erode size for edge refinement

## Testing

The project includes a comprehensive test suite with **70+ tests** covering all aspects of the service, including authentication, integration tests, and **86% code coverage**.

### Quick Start

Run all tests:
```bash
make test
```

Run tests with coverage report:
```bash
make test-cov
```

### Test Categories

#### Unit Tests
```bash
make test-unit
```
Tests individual components:
- API endpoints (root, health, models)
- **Authentication & Authorization** (X-API-Key validation)
- Background removal functionality
- Error handling scenarios
- Model validation
- CORS configuration

#### Integration Tests
```bash
make test-integration
```
Tests complete workflows:
- Full request/response cycles with authentication
- Multiple image formats
- Concurrent request handling
- Error recovery scenarios
- Concurrent requests
- Large image handling

#### Authentication Tests
```bash
# Tests specific to X-API-Key authentication
pytest tests/test_auth.py -v
```
Tests authentication scenarios:
- Valid API key acceptance
- Invalid API key rejection
- Missing API key handling
- Case-insensitive header support
- CORS with authentication

### Manual Testing

#### Using pytest directly
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_main.py

# Run specific test class
pytest tests/test_main.py::TestRootEndpoint

# Run specific test method
pytest tests/test_main.py::TestRootEndpoint::test_root_endpoint

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=main --cov-report=html --cov-report=term-missing
```

#### Test Coverage
The test suite achieves **86% code coverage**, exceeding the 80% requirement:
```bash
pytest --cov=main --cov-fail-under=80
```

### Test Structure

```
tests/
├── conftest.py              # Test configuration and fixtures
├── test_main.py             # Main API endpoint tests (13 tests)
├── test_models.py           # Pydantic model tests (15 tests)
├── test_integration.py      # Integration tests (12 tests)
├── test_utils.py            # Utility function tests (14 tests)
└── README.md               # Detailed test documentation
```

### Available Fixtures

- `client`: FastAPI test client
- `auth_headers`: Authentication headers with test API key
- `authenticated_client`: Client with authentication configured
- `sample_image`: Sample PNG image bytes
- `sample_image_file`: Mock upload file
- `mock_rembg`: Mock rembg library
- `invalid_file`: Invalid file for error testing

### Test Data

Tests use programmatically generated images to avoid storing large binary files:
- Different sizes (10x10 to 500x500 pixels)
- Multiple formats (PNG, JPEG, BMP, TIFF)
- Various colors for visual distinction

### Continuous Integration

Tests are designed for CI environments:
- No external dependencies (fully mocked)
- Fast execution (< 1 second)
- Deterministic results
- Clear failure reporting

### Debugging Tests

```bash
# Stop on first failure
pytest -x

# Show local variables on failure
pytest -l

# Run specific test with debugging
pytest tests/test_main.py::TestRootEndpoint::test_root_endpoint -v -s
```

For detailed test documentation, see [tests/README.md](tests/README.md).

## Integration with NestJS

Update your NestJS service to use the Python service:

```typescript
// In your NestJS provider
async remove(input: Buffer): Promise<Buffer> {
  const formData = new FormData();
  formData.append('file', new Blob([input]), 'image.jpg');
  formData.append('model', 'u2net');
  
  const response = await fetch('http://localhost:8001/bg/remove', {
    method: 'POST',
    body: formData,
  });
  
  if (!response.ok) {
    throw new Error(`Python service error: ${response.statusText}`);
  }
  
  return Buffer.from(await response.arrayBuffer());
}
```

## Docker Support

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["python", "main.py"]
```

## Performance Tips

1. **Model Selection**: Use `u2net` for speed, `isnet-general-use` for quality
2. **Alpha Matting**: Enable only when edge quality is critical
3. **File Size**: Keep input images under 10MB for optimal performance
4. **Caching**: Consider implementing model caching for production

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure `rembg` is installed: `pip install rembg`
2. **Model Download**: First request may be slow as models are downloaded
3. **Memory**: Large images may require more RAM

### Logs

Check logs for detailed error information:
```bash
tail -f logs/app.log  # If logging to file
```

## License

MIT License - see LICENSE file for details.
