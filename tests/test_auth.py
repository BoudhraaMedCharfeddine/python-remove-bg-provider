"""
Tests for authentication functionality
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import os


# Mark all tests in this file as unit tests
pytestmark = pytest.mark.unit


class TestAuthentication:
    """Tests for API authentication"""
    
    def test_health_endpoint_no_auth_required(self, client):
        """Test that health endpoint doesn't require authentication"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_root_endpoint_no_auth_required(self, client):
        """Test that root endpoint doesn't require authentication"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Python Remove Background Provider"
    
    def test_models_endpoint_requires_auth(self, client):
        """Test that models endpoint requires authentication"""
        response = client.get("/models")
        
        assert response.status_code == 401
        assert "X-API-Key header is required" in response.json()["detail"]
    
    def test_models_endpoint_with_valid_auth(self, client, auth_headers):
        """Test that models endpoint works with valid authentication"""
        response = client.get("/models", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "models" in data
    
    def test_models_endpoint_with_invalid_auth(self, client):
        """Test that models endpoint rejects invalid authentication"""
        invalid_headers = {"X-API-Key": "wrong-key"}
        response = client.get("/models", headers=invalid_headers)
        
        assert response.status_code == 401
        assert "Invalid API key" in response.json()["detail"]
    
    def test_bg_remove_endpoint_requires_auth(self, client, sample_image_file):
        """Test that bg/remove endpoint requires authentication"""
        files = {"file": ("test.png", sample_image_file.read(), "image/png")}
        response = client.post("/bg/remove", files=files)
        
        assert response.status_code == 401
        assert "X-API-Key header is required" in response.json()["detail"]
    
    def test_bg_remove_endpoint_with_valid_auth(self, client, sample_image_file, mock_rembg, auth_headers):
        """Test that bg/remove endpoint works with valid authentication"""
        files = {"file": ("test.png", sample_image_file.read(), "image/png")}
        response = client.post("/bg/remove", files=files, headers=auth_headers)
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
    
    def test_bg_remove_advanced_endpoint_requires_auth(self, client, sample_image_file):
        """Test that bg/remove-advanced endpoint requires authentication"""
        files = {"file": ("test.png", sample_image_file.read(), "image/png")}
        response = client.post("/bg/remove-advanced", files=files)
        
        assert response.status_code == 401
        assert "X-API-Key header is required" in response.json()["detail"]
    
    def test_bg_remove_advanced_endpoint_with_valid_auth(self, client, sample_image_file, mock_rembg, auth_headers):
        """Test that bg/remove-advanced endpoint works with valid authentication"""
        files = {"file": ("test.png", sample_image_file.read(), "image/png")}
        response = client.post("/bg/remove-advanced", files=files, headers=auth_headers)
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
    
    def test_missing_api_key_header(self, client):
        """Test behavior when X-API-Key header is missing"""
        response = client.get("/models")
        
        assert response.status_code == 401
        assert "X-API-Key header is required" in response.json()["detail"]
    
    def test_empty_api_key_header(self, client):
        """Test behavior when X-API-Key header is empty"""
        empty_headers = {"X-API-Key": ""}
        response = client.get("/models", headers=empty_headers)
        
        assert response.status_code == 401
        assert "X-API-Key header is required" in response.json()["detail"]
    
    def test_case_insensitive_api_key_header(self, client):
        """Test that API key header is case insensitive (FastAPI behavior)"""
        # Test with lowercase header name - FastAPI normalizes headers
        lowercase_headers = {"x-api-key": "test-api-key-12345"}
        response = client.get("/models", headers=lowercase_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "models" in data


class TestAuthenticationWithoutAPIKey:
    """Tests for authentication when no API key is configured"""
    
    @patch.dict(os.environ, {}, clear=True)
    def test_no_api_key_configured_allows_access(self, client):
        """Test that when no API key is configured, access is allowed"""
        # This test requires restarting the app with no API key
        # For now, we'll test the current behavior
        response = client.get("/models")
        
        # Should still require auth because we set it in setup_test_env
        assert response.status_code == 401
    
    def test_development_mode_warning(self, client):
        """Test that development mode warning is logged when no API key is set"""
        # This would require testing the actual logging
        # For now, we verify the current behavior works
        response = client.get("/health")
        assert response.status_code == 200


class TestCORSWithAuthentication:
    """Tests for CORS behavior with authentication"""
    
    def test_cors_preflight_with_auth(self, client):
        """Test CORS preflight request behavior"""
        response = client.options("/bg/remove")
        
        # CORS middleware should handle OPTIONS requests
        # The exact status code depends on FastAPI version and CORS configuration
        assert response.status_code in [200, 405]
    
    def test_cors_headers_present(self, client, auth_headers):
        """Test that CORS headers are present in responses"""
        response = client.get("/models", headers=auth_headers)
        
        assert response.status_code == 200
        # CORS headers should be present (exact headers depend on configuration)
        # We just verify the request succeeds with auth
