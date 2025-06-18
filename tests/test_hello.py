"""
Test module for hello.py demonstrating Python's testing capabilities.
"""
import pytest
from typing import Dict, Any
from pathlib import Path
import sys

# Add the parent directory to the Python path to import hello.py
sys.path.append(str(Path(__file__).parent.parent / "01_getting_started"))
from hello import greet, process_data


def test_greet_basic() -> None:
    """Test basic greeting functionality."""
    assert greet("World") == "Hello, World!"


def test_greet_multiple_times() -> None:
    """Test greeting with multiple repetitions."""
    result = greet("Python", 3)
    assert result.count("Hello") == 3
    assert result.count("Python") == 3


def test_greet_zero_times() -> None:
    """Test greeting with zero repetitions."""
    assert greet("Test", 0) == ""


def test_process_data_basic() -> None:
    """Test basic data processing without config."""
    items = ["test"]
    result = process_data(items)
    
    assert isinstance(result, dict)
    assert result["count"] == 1
    assert result["items"] == items
    assert result["has_config"] is False


def test_process_data_with_config() -> None:
    """Test data processing with configuration."""
    items = ["apple", "banana"]
    config: Dict[str, Any] = {"sort": True}
    result = process_data(items, config)
    
    assert result["count"] == 2
    assert result["has_config"] is True
    assert result["sort"] is True


if __name__ == "__main__":
    pytest.main([__file__]) 