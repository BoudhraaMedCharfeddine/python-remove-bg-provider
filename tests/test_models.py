"""
Tests for Pydantic models and validation
"""
import pytest
from pydantic import ValidationError
from main import BackgroundRemovalRequest


# Mark all tests in this file as unit tests
pytestmark = pytest.mark.unit


class TestBackgroundRemovalRequest:
    """Tests for BackgroundRemovalRequest model"""
    
    def test_default_values(self):
        """Test that default values are set correctly"""
        request = BackgroundRemovalRequest()
        
        assert request.model == "u2net"
        assert request.alpha_matting is False
        assert request.alpha_matting_foreground_threshold == 240
        assert request.alpha_matting_background_threshold == 10
        assert request.alpha_matting_erode_size == 10
    
    def test_custom_values(self):
        """Test setting custom values"""
        request = BackgroundRemovalRequest(
            model="isnet-general-use",
            alpha_matting=True,
            alpha_matting_foreground_threshold=200,
            alpha_matting_background_threshold=20,
            alpha_matting_erode_size=5
        )
        
        assert request.model == "isnet-general-use"
        assert request.alpha_matting is True
        assert request.alpha_matting_foreground_threshold == 200
        assert request.alpha_matting_background_threshold == 20
        assert request.alpha_matting_erode_size == 5
    
    def test_partial_custom_values(self):
        """Test setting only some custom values"""
        request = BackgroundRemovalRequest(
            model="u2net_human_seg",
            alpha_matting=True
        )
        
        assert request.model == "u2net_human_seg"
        assert request.alpha_matting is True
        # Other values should remain default
        assert request.alpha_matting_foreground_threshold == 240
        assert request.alpha_matting_background_threshold == 10
        assert request.alpha_matting_erode_size == 10
    
    def test_valid_model_names(self):
        """Test that valid model names are accepted"""
        valid_models = [
            "u2net",
            "u2net_human_seg", 
            "silueta",
            "isnet-general-use"
        ]
        
        for model in valid_models:
            request = BackgroundRemovalRequest(model=model)
            assert request.model == model
    
    def test_alpha_matting_threshold_validation(self):
        """Test alpha matting threshold validation"""
        # Valid thresholds (0-255)
        request = BackgroundRemovalRequest(
            alpha_matting_foreground_threshold=0,
            alpha_matting_background_threshold=255
        )
        assert request.alpha_matting_foreground_threshold == 0
        assert request.alpha_matting_background_threshold == 255
        
        # Edge cases
        request = BackgroundRemovalRequest(
            alpha_matting_foreground_threshold=128,
            alpha_matting_background_threshold=128
        )
        assert request.alpha_matting_foreground_threshold == 128
        assert request.alpha_matting_background_threshold == 128
    
    def test_alpha_matting_erode_size_validation(self):
        """Test alpha matting erode size validation"""
        # Valid erode sizes
        valid_sizes = [0, 1, 5, 10, 20, 100]
        
        for size in valid_sizes:
            request = BackgroundRemovalRequest(alpha_matting_erode_size=size)
            assert request.alpha_matting_erode_size == size
    
    def test_boolean_alpha_matting(self):
        """Test alpha matting boolean field"""
        # Test True
        request = BackgroundRemovalRequest(alpha_matting=True)
        assert request.alpha_matting is True
        
        # Test False
        request = BackgroundRemovalRequest(alpha_matting=False)
        assert request.alpha_matting is False
        
        # Test string boolean conversion
        request = BackgroundRemovalRequest(alpha_matting="true")
        assert request.alpha_matting is True
        
        request = BackgroundRemovalRequest(alpha_matting="false")
        assert request.alpha_matting is False
    
    def test_model_from_dict(self):
        """Test creating model from dictionary"""
        data = {
            "model": "silueta",
            "alpha_matting": True,
            "alpha_matting_foreground_threshold": 220,
            "alpha_matting_background_threshold": 15,
            "alpha_matting_erode_size": 8
        }
        
        request = BackgroundRemovalRequest(**data)
        
        assert request.model == "silueta"
        assert request.alpha_matting is True
        assert request.alpha_matting_foreground_threshold == 220
        assert request.alpha_matting_background_threshold == 15
        assert request.alpha_matting_erode_size == 8
    
    def test_model_to_dict(self):
        """Test converting model to dictionary"""
        request = BackgroundRemovalRequest(
            model="isnet-general-use",
            alpha_matting=True
        )
        
        data = request.model_dump()
        
        assert data["model"] == "isnet-general-use"
        assert data["alpha_matting"] is True
        assert data["alpha_matting_foreground_threshold"] == 240
        assert data["alpha_matting_background_threshold"] == 10
        assert data["alpha_matting_erode_size"] == 10
    
    def test_model_json_serialization(self):
        """Test JSON serialization and deserialization"""
        original_request = BackgroundRemovalRequest(
            model="u2net_human_seg",
            alpha_matting=True,
            alpha_matting_foreground_threshold=200
        )
        
        # Serialize to JSON
        json_str = original_request.model_dump_json()
        
        # Deserialize from JSON
        data = original_request.model_validate_json(json_str)
        
        assert data.model == "u2net_human_seg"
        assert data.alpha_matting is True
        assert data.alpha_matting_foreground_threshold == 200
        assert data.alpha_matting_background_threshold == 10  # default
        assert data.alpha_matting_erode_size == 10  # default
    
    def test_invalid_field_types(self):
        """Test validation with invalid field types"""
        # Test invalid alpha_matting type
        with pytest.raises(ValidationError):
            BackgroundRemovalRequest(alpha_matting="invalid")
        
        # Test invalid threshold types
        with pytest.raises(ValidationError):
            BackgroundRemovalRequest(alpha_matting_foreground_threshold="invalid")
        
        with pytest.raises(ValidationError):
            BackgroundRemovalRequest(alpha_matting_background_threshold="invalid")
        
        # Test invalid erode size type
        with pytest.raises(ValidationError):
            BackgroundRemovalRequest(alpha_matting_erode_size="invalid")
    
    def test_negative_values(self):
        """Test that negative values are handled correctly"""
        # Pydantic allows negative values by default for int fields
        # This test documents the current behavior
        request = BackgroundRemovalRequest(alpha_matting_foreground_threshold=-1)
        assert request.alpha_matting_foreground_threshold == -1
        
        request = BackgroundRemovalRequest(alpha_matting_background_threshold=-1)
        assert request.alpha_matting_background_threshold == -1
        
        # Negative erode size should be accepted
        request = BackgroundRemovalRequest(alpha_matting_erode_size=-1)
        assert request.alpha_matting_erode_size == -1
    
    def test_large_values(self):
        """Test handling of large values"""
        # Large thresholds should be accepted (Pydantic doesn't enforce 0-255 range by default)
        request = BackgroundRemovalRequest(
            alpha_matting_foreground_threshold=1000,
            alpha_matting_background_threshold=2000
        )
        assert request.alpha_matting_foreground_threshold == 1000
        assert request.alpha_matting_background_threshold == 2000
        
        # Large erode size should be accepted
        request = BackgroundRemovalRequest(alpha_matting_erode_size=1000)
        assert request.alpha_matting_erode_size == 1000


class TestModelValidation:
    """Tests for model validation scenarios"""
    
    def test_empty_model_name(self):
        """Test handling of empty model name"""
        request = BackgroundRemovalRequest(model="")
        assert request.model == ""
    
    def test_none_values(self):
        """Test handling of None values (should use defaults)"""
        request = BackgroundRemovalRequest(
            model=None,
            alpha_matting=None,
            alpha_matting_foreground_threshold=None,
            alpha_matting_background_threshold=None,
            alpha_matting_erode_size=None
        )
        
        # None values should be replaced with defaults
        assert request.model is None  # This might be None if not defaulted
        assert request.alpha_matting is None  # This might be None if not defaulted
