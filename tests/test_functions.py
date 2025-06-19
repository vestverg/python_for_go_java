"""
Test module for functions.py demonstrating Python's testing capabilities.
"""
import pytest
from typing import List, Dict, Any
from pathlib import Path
import sys

# Add the parent directory to the Python path to import functions.py
sys.path.append(str(Path(__file__).parent.parent / "04_functions" / "examples"))
from functions import (
    calculate_total,
    factorial,
    fibonacci_generator,
    process_with_callback,
    TimerDecorator
)


def test_calculate_total_basic() -> None:
    """Test basic total calculation."""
    result = calculate_total([10.0, 20.0, 30.0])
    expected = 60.0 * 1.1  # With default 10% tax
    assert abs(result - expected) < 0.01


def test_calculate_total_with_discount() -> None:
    """Test total calculation with discount."""
    result = calculate_total([100.0], tax_rate=0.1, discount=0.2)
    expected = 100.0 * 0.8 * 1.1  # 20% discount, 10% tax
    assert abs(result - expected) < 0.01


def test_calculate_total_no_tax() -> None:
    """Test total calculation without tax."""
    result = calculate_total([50.0, 25.0], tax_rate=0.0)
    assert result == 75.0


def test_factorial_basic() -> None:
    """Test factorial calculation."""
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120
    assert factorial(10) == 3628800


def test_factorial_negative() -> None:
    """Test factorial with negative number."""
    with pytest.raises(ValueError, match="Factorial is not defined for negative numbers"):
        factorial(-1)


def test_fibonacci_generator() -> None:
    """Test Fibonacci number generation."""
    fib_gen = fibonacci_generator(10)
    fib_numbers = list(fib_gen)
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert fib_numbers == expected


def test_fibonacci_generator_zero() -> None:
    """Test Fibonacci generator with zero count."""
    fib_gen = fibonacci_generator(0)
    fib_numbers = list(fib_gen)
    assert fib_numbers == []


def test_process_with_callback() -> None:
    """Test function with callback."""
    def square(x: int) -> int:
        return x * x
    
    result = process_with_callback([1, 2, 3, 4], square)
    assert result == [1, 4, 9, 16]


def test_process_with_callback_empty() -> None:
    """Test callback processing with empty list."""
    def double(x: int) -> int:
        return x * 2
    
    result = process_with_callback([], double)
    assert result == []


def test_timer_decorator(capsys) -> None:
    """Test timer decorator functionality."""
    import time
    
    @TimerDecorator("Test operation")
    def slow_function() -> str:
        time.sleep(0.1)  # Sleep for 100ms
        return "done"
    
    result = slow_function()
    captured = capsys.readouterr()
    
    assert result == "done"
    assert "Test operation:" in captured.out
    assert "seconds" in captured.out


@pytest.mark.parametrize("items,expected", [
    ([10.0], 11.0),
    ([5.0, 5.0], 11.0),
    ([100.0, 200.0], 330.0),
])
def test_calculate_total_parametrized(items: List[float], expected: float) -> None:
    """Parametrized test for total calculation with default tax."""
    result = calculate_total(items)
    assert abs(result - expected) < 0.01


if __name__ == "__main__":
    pytest.main([__file__]) 