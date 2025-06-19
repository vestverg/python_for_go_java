"""
Test module for control_flow.py demonstrating Python's testing capabilities.
"""
import pytest
from typing import Any
from pathlib import Path
import sys

# Add the parent directory to the Python path to import control_flow.py
sys.path.append(str(Path(__file__).parent.parent / "03_control_flow" / "examples"))
from control_flow import (
    check_grade, 
    analyze_data, 
    safe_divide,
    ValidationError
)


def test_check_grade() -> None:
    """Test grade checking function."""
    assert check_grade(95) == "A"
    assert check_grade(85) == "B"
    assert check_grade(75) == "C"
    assert check_grade(65) == "D"
    assert check_grade(55) == "F"


def test_check_grade_edge_cases() -> None:
    """Test edge cases for grade checking."""
    assert check_grade(90) == "A"  # Boundary test
    assert check_grade(80) == "B"  # Boundary test
    assert check_grade(0) == "F"   # Minimum value
    assert check_grade(100) == "A" # Maximum value


def test_analyze_data_with_numbers() -> None:
    """Test data analysis with numeric values."""
    result = analyze_data([1, 2, 3, 4, 5])
    assert result["type"] == "numbers"
    assert result["count"] == 5
    assert result["sum"] == 15


def test_analyze_data_with_strings() -> None:
    """Test data analysis with string values."""
    result = analyze_data(["hello", "world"])
    assert result["type"] == "strings"
    assert result["count"] == 2
    assert result["total_length"] == 10


def test_analyze_data_empty() -> None:
    """Test data analysis with empty list."""
    result = analyze_data([])
    assert result["type"] == "empty"
    assert result["count"] == 0


def test_safe_divide_success() -> None:
    """Test successful division."""
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(7, 2) == 3.5


def test_safe_divide_by_zero() -> None:
    """Test division by zero handling."""
    with pytest.raises(ZeroDivisionError):
        safe_divide(10, 0)


def test_validation_error() -> None:
    """Test custom validation error."""
    error = ValidationError("Test message", 400)
    assert str(error) == "Test message"
    assert error.code == 400


if __name__ == "__main__":
    pytest.main([__file__]) 