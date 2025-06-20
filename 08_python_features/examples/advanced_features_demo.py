"""
Advanced Python Features Demonstration

This module showcases advanced Python features including:
1. Decorators (function and class)
2. Context managers
3. Generators and iterators
4. Metaclasses
5. Descriptors
6. Properties
7. Type hints and protocols
8. Functional programming features
"""

import time
import functools
from typing import Any, Callable, Generator, Type, Dict
import contextlib


# ============================================================================
# DECORATORS
# ============================================================================

F = functools.partial(type, bound=Callable[..., Any])

def timer_decorator(func: F) -> F:
    """Decorator that prints the execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def retry_decorator(max_attempts: int = 3, delay: float = 1.0):
    """Decorator that retries a function on failure."""
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt + 1 == max_attempts:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator


# ============================================================================
# CONTEXT MANAGERS
# ============================================================================

class ManagedResource:
    """A simple managed resource context manager."""
    def __init__(self, name: str):
        self.name = name

    def __enter__(self):
        print(f"Acquiring resource {self.name}")
        return self.name

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Releasing resource {self.name}")

@contextlib.contextmanager
def timer_context(operation_name: str) -> Generator[Dict[str, float], None, None]:
    """Context manager that times operations."""
    start_time = time.time()
    timing_info = {'start': start_time, 'elapsed': 0}
    
    try:
        yield timing_info
    finally:
        end_time = time.time()
        timing_info['end'] = end_time
        timing_info['elapsed'] = end_time - start_time
        print(f"{operation_name} took {timing_info['elapsed']:.4f} seconds")

# ============================================================================
# GENERATORS
# ============================================================================

def fibonacci_generator() -> Generator[int, None, None]:
    """Generate an infinite sequence of Fibonacci numbers."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def infinite_counter(start: int = 0, step: int = 1) -> Generator[int, None, None]:
    """Generate an infinite sequence of numbers."""
    n = start
    while True:
        yield n
        n += step

# ============================================================================
# METACLASSES
# ============================================================================

class SingletonMeta(type):
    """Metaclass for creating singleton classes."""
    _instances: Dict[Type, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class AutoPropertyMeta(type):
    """Metaclass that automatically creates properties for private attributes."""
    def __new__(cls, name, bases, dct):
        for attr_name, value in dct.items():
            if attr_name.startswith('_') and not attr_name.startswith('__'):
                prop_name = attr_name[1:]
                if prop_name not in dct:
                    dct[prop_name] = property(lambda self, name=attr_name: getattr(self, name))
        return super().__new__(cls, name, bases, dct)

# ============================================================================
# DESCRIPTORS
# ============================================================================

class ValidatedAttribute:
    """Descriptor for an attribute that must be within a given range."""
    def __init__(self, min_value: float, max_value: float):
        self.min_value = min_value
        self.max_value = max_value
        self._values = {}

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        return self._values.get(instance)

    def __set__(self, instance, value):
        if not self.min_value <= value <= self.max_value:
            raise ValueError(f"{self._name} must be between {self.min_value} and {self.max_value}")
        self._values[instance] = value

class TypedAttribute:
    """Descriptor that enforces a specific type."""
    def __init__(self, expected_type: Type):
        self.expected_type = expected_type
        self._values = {}

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        return self._values.get(instance)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{self._name} must be of type {self.expected_type.__name__}")
        self._values[instance] = value

# ============================================================================
# PROPERTIES
# ============================================================================

class Temperature:
    """A class that uses properties to handle temperature conversions."""
    def __init__(self, celsius: float):
        self.celsius = celsius

    @property
    def fahrenheit(self) -> float:
        return self.celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float):
        self.celsius = (value - 32) * 5/9

    @property
    def kelvin(self) -> float:
        return self.celsius + 273.15

    @kelvin.setter
    def kelvin(self, value: float):
        self.celsius = value - 273.15

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Demonstrate all the advanced features."""
    print("Demonstrating Advanced Python Features")
    
    @timer_decorator
    def example_function():
        print("Executing example function")
        time.sleep(0.1)

    example_function()

    with ManagedResource("test") as r:
        print(f"Inside with block for {r}")

    fib = fibonacci_generator()
    print(f"First 5 Fibonacci numbers: {[next(fib) for _ in range(5)]}")

    class MySingleton(metaclass=SingletonMeta):
        pass

    a = MySingleton()
    b = MySingleton()
    print(f"Are singletons the same? {a is b}")

    class MyClass:
        validated = ValidatedAttribute(0, 100)
        typed = TypedAttribute(int)

    mc = MyClass()
    mc.validated = 50
    mc.typed = 10
    print(f"Validated: {mc.validated}, Typed: {mc.typed}")

    temp = Temperature(25)
    print(f"Celsius: {temp.celsius}, Fahrenheit: {temp.fahrenheit}, Kelvin: {temp.kelvin}")
    temp.fahrenheit = 32
    print(f"New Celsius: {temp.celsius}")


if __name__ == "__main__":
    main()