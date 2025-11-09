# Tests for PixForge Python Service

This directory contains comprehensive unit and integration tests for the PixForge Python Service.

## Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Pytest configuration and fixtures
├── test_main.py             # Tests for main FastAPI endpoints
├── test_models.py           # Tests for Pydantic models and validation
├── test_integration.py      # Integration tests
├── test_utils.py            # Utility function tests
└── README.md               # This file
```

## Running Tests

### Install Test Dependencies
```bash
pip install -r requirements.txt
```

### Run All Tests
```bash
pytest
```

### Run Tests with Coverage
```bash
pytest --cov=main --cov-report=html --cov-report=term-missing
```

### Run Specific Test Types
```bash
# Unit tests only
pytest -m "not integration"

# Integration tests only
pytest -m integration

# Specific test file
pytest tests/test_main.py

# Specific test class
pytest tests/test_main.py::TestRootEndpoint

# Specific test method
pytest tests/test_main.py::TestRootEndpoint::test_root_endpoint
```

### Using Make Commands
```bash
make test          # Run all tests
make test-cov      # Run tests with coverage
make test-unit     # Run unit tests only
make test-integration  # Run integration tests only
```

## Test Categories

### 1. Unit Tests (`test_main.py`)
- **Root Endpoint**: Tests for the basic service endpoint
- **Health Check**: Tests for health monitoring
- **Models Endpoint**: Tests for model listing
- **Background Removal**: Tests for core functionality
- **Error Handling**: Tests for various error scenarios

### 2. Model Tests (`test_models.py`)
- **Validation**: Tests for Pydantic model validation
- **Default Values**: Tests for default parameter values
- **Edge Cases**: Tests for boundary conditions
- **Serialization**: Tests for JSON serialization/deserialization

### 3. Integration Tests (`test_integration.py`)
- **Full Workflow**: Tests for complete request/response cycles
- **Multiple Requests**: Tests for concurrent request handling
- **Different Formats**: Tests for various image formats
- **Performance**: Tests for large image handling
- **Error Recovery**: Tests for error handling and recovery

### 4. Utility Tests (`test_utils.py`)
- **Image Creation**: Tests for test image generation
- **File Handling**: Tests for temporary file management
- **Mock Utilities**: Tests for mock object creation
- **Validation Helpers**: Tests for validation utility functions

## Test Fixtures

### Core Fixtures (in `conftest.py`)
- `client`: FastAPI test client
- `sample_image`: Sample PNG image bytes
- `sample_image_file`: Mock upload file with image data
- `mock_rembg`: Mock rembg library for testing
- `invalid_file`: Invalid file for error testing

### Custom Fixtures
Each test file may define additional fixtures specific to its needs.

## Mocking Strategy

### rembg Library Mocking
The `mock_rembg` fixture provides:
- `remove`: Mock function that returns fake processed image data
- `new_session`: Mock function that returns a mock session
- `session`: Mock session object

This allows testing without requiring the actual rembg library to be installed.

### File Upload Mocking
The `sample_image_file` fixture creates a mock `UploadFile` object that behaves like a real file upload, including async context manager support.

## Coverage Requirements

The test suite aims for:
- **Minimum 80% code coverage**
- **100% endpoint coverage**
- **All error paths tested**
- **All model validation scenarios**

## Continuous Integration

Tests are designed to run in CI environments:
- No external dependencies required (mocked)
- Fast execution (< 30 seconds)
- Deterministic results
- Clear failure reporting

## Test Data

### Sample Images
Tests use programmatically generated images to avoid storing large binary files in the repository:
- Different sizes (10x10 to 500x500)
- Different formats (PNG, JPEG, BMP, TIFF)
- Different colors for visual distinction

### Mock Data
All external dependencies are mocked to ensure:
- Tests run without network access
- No external API calls
- Predictable test results
- Fast execution

## Debugging Tests

### Verbose Output
```bash
pytest -v
```

### Stop on First Failure
```bash
pytest -x
```

### Show Local Variables on Failure
```bash
pytest -l
```

### Run Specific Test with Debugging
```bash
pytest tests/test_main.py::TestRootEndpoint::test_root_endpoint -v -s
```

## Adding New Tests

### Test Naming Convention
- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`

### Test Structure
```python
class TestFeatureName:
    """Tests for feature description"""
    
    def test_specific_scenario(self, fixture_name):
        """Test description"""
        # Arrange
        # Act
        # Assert
```

### Adding Fixtures
Add new fixtures to `conftest.py` if they're used across multiple test files, or define them locally if they're specific to one test file.

## Performance Considerations

- Tests use small images (10x10 to 100x100 pixels) for speed
- Mock objects are reused where possible
- Database/external service calls are mocked
- Tests run in parallel when possible

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Mock Failures**: Check that mocks are properly configured
3. **File Path Issues**: Use absolute paths in tests
4. **Async Issues**: Ensure async fixtures are properly awaited

### Getting Help
- Check pytest documentation: https://docs.pytest.org/
- Review FastAPI testing guide: https://fastapi.tiangolo.com/tutorial/testing/
- Check existing test patterns in the codebase
