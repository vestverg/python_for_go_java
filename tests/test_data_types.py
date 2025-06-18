"""
Test module for data_types.py demonstrating Python's testing capabilities.
"""
import pytest
from typing import Dict, Any
from pathlib import Path
import sys

# Add the parent directory to the Python path to import data_types.py
sys.path.append(str(Path(__file__).parent.parent / "02_basic_syntax"))
from data_types import Person, demonstrate_numeric_types


def test_person_creation() -> None:
    """Test Person data class creation and methods."""
    person = Person(name="Test", age=25)
    assert person.name == "Test"
    assert person.age == 25
    assert person.greet() == "Hello, Test!"


def test_person_equality() -> None:
    """Test Person data class equality comparison."""
    person1 = Person(name="Alice", age=30)
    person2 = Person(name="Alice", age=30)
    person3 = Person(name="Bob", age=30)
    
    assert person1 == person2  # Same values should be equal
    assert person1 != person3  # Different names should not be equal


def test_numeric_types(capsys) -> None:
    """
    Test numeric types demonstration.
    Uses capsys fixture to capture stdout.
    """
    demonstrate_numeric_types()
    captured = capsys.readouterr()
    
    # Check that the output contains our expected values
    assert "Large integer: 1000000000000000000000000" in captured.out
    assert "Float: 3.14159" in captured.out
    assert "Complex: (1+2j)" in captured.out


def test_person_repr() -> None:
    """Test Person string representation."""
    person = Person(name="Test", age=25)
    repr_str = repr(person)
    
    assert "Person" in repr_str
    assert "name='Test'" in repr_str
    assert "age=25" in repr_str


if __name__ == "__main__":
    pytest.main([__file__]) 