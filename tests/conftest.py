"""
Test configuration and fixtures for PixForge Python Service
"""
import pytest
import io
from PIL import Image
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import tempfile
import os

from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def auth_headers():
    """Create authentication headers for testing"""
    return {"X-API-Key": "test-api-key-12345"}


@pytest.fixture
def authenticated_client(client, auth_headers):
    """Create a test client with authentication headers"""
    # We'll use this fixture in tests that need authentication
    # The client will be used with auth_headers in individual tests
    return client, auth_headers


@pytest.fixture
def sample_image():
    """Create a sample image for testing"""
    # Create a simple 100x100 RGB image
    image = Image.new('RGB', (100, 100), color='red')
    
    # Save to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return img_bytes.getvalue()


@pytest.fixture
def sample_image_file(sample_image):
    """Create a sample image file for upload testing"""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        tmp_file.write(sample_image)
        tmp_file.flush()
        
        # Create a mock UploadFile
        upload_file = Mock()
        upload_file.filename = "test_image.png"
        upload_file.content_type = "image/png"
        upload_file.read = Mock(return_value=sample_image)
        upload_file.__aenter__ = Mock(return_value=upload_file)
        upload_file.__aexit__ = Mock(return_value=None)
        
        yield upload_file
        
        # Cleanup
        os.unlink(tmp_file.name)


@pytest.fixture
def mock_rembg():
    """Mock the rembg library for testing"""
    with patch('rembg.remove') as mock_remove, \
         patch('rembg.new_session') as mock_session:
        
        # Configure mocks
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        
        # Mock the remove function to return a simple PNG
        mock_output = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00d\x00\x00\x00d\x08\x06\x00\x00\x00p\xe2\xb8\x84\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x19tEXtSoftware\x00Adobe ImageReadyq\xc9e<\x00\x00\x00\x0cIDATx\xdab\xf8\x0f\x00\x00\x01\x00\x01\x00\x18\xdd\x8d\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        mock_remove.return_value = mock_output
        
        yield {
            'remove': mock_remove,
            'new_session': mock_session,
            'session': mock_session_instance
        }


@pytest.fixture
def invalid_file():
    """Create an invalid file for testing error cases"""
    upload_file = Mock()
    upload_file.filename = "test.txt"
    upload_file.content_type = "text/plain"
    upload_file.read = Mock(return_value=b"not an image")
    upload_file.__aenter__ = Mock(return_value=upload_file)
    upload_file.__aexit__ = Mock(return_value=None)
    
    return upload_file


@pytest.fixture(autouse=True)
def setup_test_env():
    """Set up test environment variables"""
    # Set test API key for authentication tests
    os.environ["X_API_KEY"] = "test-api-key-12345"
    os.environ["ALLOWED_ORIGINS"] = "http://localhost:3000,http://localhost:3001"
    yield
    # Clean up is handled by the cleanup_env fixture


@pytest.fixture(autouse=True)
def cleanup_env():
    """Clean up environment variables after each test"""
    original_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(original_env)
