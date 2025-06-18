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
import contextlib
from typing import (
    Any, Callable, Generator, Iterator, Protocol, TypeVar, Generic,
    Union, Optional, List, Dict, Type, runtime_checkable
)
from abc import ABC, abstractmethod
import json
import sqlite3
from dataclasses import dataclass
from collections.abc import Iterable


# ============================================================================
# DECORATORS
# ============================================================================

F = TypeVar('F', bound=Callable[..., Any])

def performance_monitor(func: F) -> F:
    """Decorator to monitor function performance."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)
            raise
        finally:
            end_time = time.time()
            print(f"[PERF] {func.__name__}: {end_time - start_time:.4f}s, {success}")
        
        return result
    
    return wrapper

def cache_with_ttl(ttl_seconds: float = 60.0):
    """Decorator that caches function results with TTL."""
    def decorator(func: F) -> F:
        cache: Dict[tuple, tuple] = {}  # key -> (result, timestamp)
        
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (args, tuple(sorted(kwargs.items())))
            current_time = time.time()
            
            if key in cache:
                result, timestamp = cache[key]
                if current_time - timestamp < ttl_seconds:
                    print(f"Cache hit for {func.__name__}")
                    return result
            
            result = func(*args, **kwargs)
            cache[key] = (result, current_time)
            print(f"Cache miss for {func.__name__}")
            return result
        
        wrapper.cache_clear = lambda: cache.clear()
        return wrapper
    return decorator

def add_string_representation(cls: Type) -> Type:
    """Class decorator that adds a string representation."""
    def __str__(self) -> str:
        attrs = ', '.join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"
    
    cls.__str__ = __str__
    return cls


# ============================================================================
# CONTEXT MANAGERS
# ============================================================================

@contextlib.contextmanager
def timer_context(operation_name: str) -> Generator[Dict[str, float], None, None]:
    """Context manager that times operations."""
    start_time = time.time()
    timing_info = {'start': start_time}
    
    try:
        yield timing_info
    finally:
        end_time = time.time()
        timing_info['end'] = end_time
        timing_info['duration'] = end_time - start_time
        print(f"{operation_name} took {timing_info['duration']:.4f} seconds")


# ============================================================================
# GENERATORS AND ITERATORS
# ============================================================================

def fibonacci_sequence(limit: Optional[int] = None) -> Generator[int, None, None]:
    """Generate Fibonacci numbers up to limit."""
    a, b = 0, 1
    count = 0
    
    while limit is None or count < limit:
        yield a
        a, b = b, a + b
        count += 1

def batch_iterator(iterable: Iterable, batch_size: int) -> Generator[List[Any], None, None]:
    """Yield batches of items from an iterable."""
    iterator = iter(iterable)
    while True:
        batch = []
        for _ in range(batch_size):
            try:
                batch.append(next(iterator))
            except StopIteration:
                if batch:
                    yield batch
                return
        yield batch


# ============================================================================
# METACLASSES
# ============================================================================

class SingletonMeta(type):
    """Metaclass for singleton pattern."""
    _instances: Dict[Type, Any] = {}
    
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# ============================================================================
# DESCRIPTORS
# ============================================================================

class TypedDescriptor:
    """Descriptor that enforces type checking."""
    
    def __init__(self, expected_type: Type, default: Any = None) -> None:
        self.expected_type = expected_type
        self.default = default
        self.name = ""
    
    def __set_name__(self, owner: Type, name: str) -> None:
        self.name = name
    
    def __get__(self, instance: Any, owner: Type) -> Any:
        if instance is None:
            return self
        return getattr(instance, f"_{self.name}", self.default)
    
    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.name} must be of type {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        setattr(instance, f"_{self.name}", value)


# ============================================================================
# PROTOCOLS AND TYPE HINTS
# ============================================================================

@runtime_checkable
class Drawable(Protocol):
    """Protocol for drawable objects."""
    def draw(self) -> str: ...


# ============================================================================
# EXAMPLE CLASSES USING ADVANCED FEATURES
# ============================================================================

class ConfigManager(metaclass=SingletonMeta):
    """Configuration manager using singleton pattern."""
    
    def __init__(self) -> None:
        self._settings: Dict[str, Any] = {}
    
    def set(self, key: str, value: Any) -> None:
        self._settings[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        return self._settings.get(key, default)

class Rectangle:
    """Rectangle class demonstrating descriptors."""
    
    color = TypedDescriptor(str, default="black")
    
    def __init__(self, width: float, height: float, color: str = "black") -> None:
        self.width = width
        self.height = height
        self.color = color
    
    @property
    def area(self) -> float:
        return self.width * self.height
    
    def draw(self) -> str:
        return f"Rectangle({self.width}x{self.height}, {self.color})"

class DataProcessor:
    """Data processor with cached properties."""
    
    def __init__(self, data: List[int]) -> None:
        self.data = data
    
    @functools.cached_property
    def mean(self) -> float:
        """Cached mean calculation."""
        print("Computing mean...")
        return sum(self.data) / len(self.data)
    
    @performance_monitor
    @cache_with_ttl(ttl_seconds=30)
    def expensive_computation(self, factor: float) -> List[float]:
        """Expensive computation with caching and monitoring."""
        time.sleep(0.1)  # Simulate expensive operation
        return [x * factor for x in self.data]


# ============================================================================
# DEMONSTRATION FUNCTIONS
# ============================================================================

def demonstrate_decorators() -> None:
    """Demonstrate decorator usage."""
    print("=== DECORATOR DEMONSTRATION ===")
    
    processor = DataProcessor([1, 2, 3, 4, 5])
    
    # First call - cache miss
    result1 = processor.expensive_computation(2.0)
    
    # Second call - cache hit
    result2 = processor.expensive_computation(2.0)
    
    print(f"Results equal: {result1 == result2}")

def demonstrate_context_managers() -> None:
    """Demonstrate context manager usage."""
    print("\n=== CONTEXT MANAGER DEMONSTRATION ===")
    
    with timer_context("Simulation") as timer:
        time.sleep(0.1)

def demonstrate_generators() -> None:
    """Demonstrate generator usage."""
    print("\n=== GENERATOR DEMONSTRATION ===")
    
    # Fibonacci generator
    fib = fibonacci_sequence(10)
    print(f"First 10 Fibonacci numbers: {list(fib)}")
    
    # Batch processing
    data = range(20)
    for i, batch in enumerate(batch_iterator(data, 5)):
        print(f"Batch {i}: {batch}")

def demonstrate_metaclasses() -> None:
    """Demonstrate metaclass usage."""
    print("\n=== METACLASS DEMONSTRATION ===")
    
    # Singleton
    config1 = ConfigManager()
    config2 = ConfigManager()
    print(f"Same instance: {config1 is config2}")
    
    config1.set("debug", True)
    print(f"Config value: {config2.get('debug')}")

def demonstrate_descriptors() -> None:
    """Demonstrate descriptor usage."""
    print("\n=== DESCRIPTOR DEMONSTRATION ===")
    
    rect = Rectangle(10, 5, "blue")
    print(f"Rectangle: {rect.draw()}")
    print(f"Area: {rect.area}")
    
    try:
        rect.color = 123  # Should raise TypeError
    except TypeError as e:
        print(f"Validation error: {e}")

def demonstrate_protocols() -> None:
    """Demonstrate protocol usage."""
    print("\n=== PROTOCOL DEMONSTRATION ===")
    
    rect = Rectangle(8, 6)
    
    # Check if rectangle implements Drawable protocol
    if isinstance(rect, Drawable):
        print(f"Rectangle is drawable: {rect.draw()}")

def main() -> None:
    """Main demonstration function."""
    print("Advanced Python Features Demonstration")
    print("=" * 50)
    
    try:
        demonstrate_decorators()
        demonstrate_context_managers()
        demonstrate_generators()
        demonstrate_metaclasses()
        demonstrate_descriptors()
        demonstrate_protocols()
        
    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 