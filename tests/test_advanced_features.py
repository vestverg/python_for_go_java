"""
Test module for advanced Python features examples.
"""
import pytest
from typing import Any, Iterator
from pathlib import Path
import sys
import time

# Add the parent directory to the Python path to import advanced features
sys.path.append(str(Path(__file__).parent.parent / "08_python_features" / "examples"))


def test_decorators() -> None:
    """Test decorator functionality."""
    try:
        from advanced_features_demo import timer_decorator, retry_decorator
        
        @timer_decorator
        def test_function() -> str:
            time.sleep(0.1)
            return "test"
        
        result = test_function()
        assert result == "test"
        
        # Test retry decorator
        attempt_count = 0
        
        @retry_decorator(max_attempts=3)
        def flaky_function() -> str:
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 2:
                raise ValueError("Temporary failure")
            return "success"
        
        result = flaky_function()
        assert result == "success"
        assert attempt_count == 2
        
    except ImportError:
        pytest.skip("Advanced features demo not available")


def test_context_managers() -> None:
    """Test context manager functionality."""
    try:
        from advanced_features_demo import ManagedResource, timer_context
        
        # Test custom context manager
        with ManagedResource("test_resource") as resource:
            assert resource == "test_resource"
        
        # Test timer context manager
        with timer_context("test operation") as timer:
            time.sleep(0.1)
        
        # Timer should have recorded some time
        assert timer['elapsed'] > 0
        
    except ImportError:
        pytest.skip("Advanced features demo not available")


def test_generators() -> None:
    """Test generator functionality."""
    try:
        from advanced_features_demo import fibonacci_generator, infinite_counter
        
        # Test Fibonacci generator
        fib_gen = fibonacci_generator()
        fib_sequence = [next(fib_gen) for _ in range(10)]
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        assert fib_sequence == expected
        
        # Test infinite counter
        counter = infinite_counter(start=5, step=2)
        assert next(counter) == 5
        assert next(counter) == 7
        assert next(counter) == 9
        
    except ImportError:
        pytest.skip("Advanced features demo not available")


def test_metaclasses() -> None:
    """Test metaclass functionality."""
    try:
        from advanced_features_demo import SingletonMeta, AutoPropertyMeta
        
        # Test singleton metaclass
        class TestSingleton(metaclass=SingletonMeta):
            def __init__(self, value: str) -> None:
                self.value = value
        
        instance1 = TestSingleton("first")
        instance2 = TestSingleton("second")
        
        # Should be the same instance
        assert instance1 is instance2
        assert instance1.value == "first"  # First initialization wins
        
    except ImportError:
        pytest.skip("Advanced features demo not available")


def test_descriptors() -> None:
    """Test descriptor functionality."""
    try:
        from advanced_features_demo import ValidatedAttribute, TypedAttribute
        
        class TestClass:
            validated_attr = ValidatedAttribute(min_value=0, max_value=100)
            typed_attr = TypedAttribute(int)
        
        obj = TestClass()
        
        # Test validated attribute
        obj.validated_attr = 50
        assert obj.validated_attr == 50
        
        with pytest.raises(ValueError):
            obj.validated_attr = -10  # Below minimum
        
        with pytest.raises(ValueError):
            obj.validated_attr = 150  # Above maximum
        
        # Test typed attribute
        obj.typed_attr = 42
        assert obj.typed_attr == 42
        
        with pytest.raises(TypeError):
            obj.typed_attr = "not an integer"
        
    except ImportError:
        pytest.skip("Advanced features demo not available")


def test_property_decorators() -> None:
    """Test property decorator functionality."""
    try:
        from advanced_features_demo import Temperature
        
        temp = Temperature(25.0)
        
        # Test property getter
        assert temp.celsius == 25.0
        assert abs(temp.fahrenheit - 77.0) < 0.1
        assert abs(temp.kelvin - 298.15) < 0.1
        
        # Test property setter
        temp.fahrenheit = 86.0
        assert abs(temp.celsius - 30.0) < 0.1
        
        temp.kelvin = 273.15
        assert abs(temp.celsius - 0.0) < 0.1
        
    except ImportError:
        pytest.skip("Advanced features demo not available")


def test_generator_expressions() -> None:
    """Test generator expression functionality."""
    # Test memory efficiency of generator expressions
    def large_range_sum() -> int:
        return sum(x * x for x in range(1000) if x % 2 == 0)
    
    result = large_range_sum()
    assert isinstance(result, int)
    assert result > 0
    
    # Test generator expression with complex logic
    def process_data() -> Iterator[str]:
        data = ["apple", "banana", "cherry", "date"]
        return (item.upper() for item in data if len(item) > 4)
    
    processed = list(process_data())
    assert processed == ["APPLE", "BANANA", "CHERRY"]


def test_lambda_functions() -> None:
    """Test lambda function functionality."""
    # Test basic lambda
    square = lambda x: x * x
    assert square(5) == 25
    
    # Test lambda with built-in functions
    numbers = [1, 2, 3, 4, 5]
    squared = list(map(lambda x: x * x, numbers))
    assert squared == [1, 4, 9, 16, 25]
    
    # Test lambda with filter
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    assert evens == [2, 4]
    
    # Test lambda with sort
    words = ["python", "java", "go", "rust"]
    sorted_by_length = sorted(words, key=lambda x: len(x))
    assert sorted_by_length == ["go", "java", "rust", "python"]


def test_comprehensions() -> None:
    """Test various comprehension types."""
    # List comprehension
    squares = [x * x for x in range(5)]
    assert squares == [0, 1, 4, 9, 16]
    
    # Dict comprehension
    square_dict = {x: x * x for x in range(5)}
    assert square_dict == {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
    
    # Set comprehension
    unique_squares = {x * x for x in [-2, -1, 0, 1, 2]}
    assert unique_squares == {0, 1, 4}
    
    # Nested comprehension
    matrix = [[i + j for j in range(3)] for i in range(3)]
    expected = [[0, 1, 2], [1, 2, 3], [2, 3, 4]]
    assert matrix == expected


if __name__ == "__main__":
    pytest.main([__file__]) 