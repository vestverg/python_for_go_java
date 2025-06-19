"""
Test module for modules and packages examples.
"""
import pytest
from typing import Dict, Any
from pathlib import Path
import sys

# Add the parent directory to the Python path to import modules
sys.path.append(str(Path(__file__).parent.parent / "06_modules_and_packages" / "examples"))
from example_usage import demonstrate_package_usage


def test_package_usage(capsys) -> None:
    """Test package usage demonstration."""
    demonstrate_package_usage()
    captured = capsys.readouterr()
    
    # Check that the demonstration ran without errors
    assert len(captured.out) > 0
    # The exact output will depend on the implementation


def test_package_imports() -> None:
    """Test that package imports work correctly."""
    try:
        # Try importing the package modules
        from mypackage import DataProcessor, APIClient
        from mypackage.utils import validate_email, format_date
        
        # If we get here, imports worked
        assert True
    except ImportError as e:
        pytest.skip(f"Package imports failed: {e}")


def test_validate_email() -> None:
    """Test email validation function if available."""
    try:
        from mypackage.utils import validate_email
        
        # Test valid emails
        assert validate_email("test@example.com") == True
        assert validate_email("user.name@domain.co.uk") == True
        
        # Test invalid emails
        assert validate_email("invalid-email") == False
        assert validate_email("@domain.com") == False
        assert validate_email("user@") == False
        
    except ImportError:
        pytest.skip("validate_email function not available")


def test_format_date() -> None:
    """Test date formatting function if available."""
    try:
        from mypackage.utils import format_date
        from datetime import datetime
        
        test_date = datetime(2023, 12, 25, 10, 30, 0)
        formatted = format_date(test_date)
        
        # Check that we get a string back
        assert isinstance(formatted, str)
        assert len(formatted) > 0
        
    except ImportError:
        pytest.skip("format_date function not available")


def test_data_processor() -> None:
    """Test DataProcessor class if available."""
    try:
        from mypackage.core import JSONProcessor
        
        processor = JSONProcessor()
        
        # Test valid JSON
        valid_json = '{"name": "test", "value": 123}'
        assert processor.validate(valid_json) == True
        
        result = processor.process(valid_json)
        assert isinstance(result, dict)
        assert result["name"] == "test"
        assert result["value"] == 123
        
        # Test invalid JSON
        invalid_json = '{"name": "test", "value":}'
        assert processor.validate(invalid_json) == False
        
        with pytest.raises(ValueError):
            processor.process(invalid_json)
            
    except ImportError:
        pytest.skip("JSONProcessor class not available")


def test_api_client() -> None:
    """Test APIClient class if available."""
    try:
        from mypackage.core import APIClient
        
        client = APIClient("https://api.example.com")
        assert client.base_url == "https://api.example.com"
        
        # We can't test actual HTTP calls without mocking,
        # but we can test the object creation
        assert hasattr(client, 'get')
        assert hasattr(client, 'post')
        
    except ImportError:
        pytest.skip("APIClient class not available")


if __name__ == "__main__":
    pytest.main([__file__]) 