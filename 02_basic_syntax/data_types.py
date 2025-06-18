#!/usr/bin/env python3
"""
Demonstration of Python's data types with comparisons to Java and Go.
This module shows how Python's type system differs from static typing.
"""
from typing import List, Dict, Set, Tuple, Optional, Union, Any
from dataclasses import dataclass
from datetime import datetime


# Equivalent to Java record or Go struct
@dataclass
class Person:
    """
    Example of a data class, similar to:
    Java: public record Person(String name, int age) {}
    Go: type Person struct { name string; age int }
    """
    name: str
    age: int
    
    def greet(self) -> str:
        """Returns a greeting for the person."""
        return f"Hello, {self.name}!"


def demonstrate_numeric_types() -> None:
    """
    Demonstrates Python's numeric types.
    Unlike Java/Go, Python has arbitrary precision integers.
    """
    # Integer (arbitrary precision, unlike Java/Go)
    x: int = 1000000000000000000000000
    print(f"Large integer: {x}")
    
    # Float (similar to Java double/Go float64)
    y: float = 3.14159
    print(f"Float: {y}")
    
    # Complex numbers (not in Java/Go)
    z: complex = 1 + 2j
    print(f"Complex: {z}")


def demonstrate_collections() -> None:
    """
    Demonstrates Python's collection types with type hints.
    Shows equivalents in Java and Go.
    """
    # List (Java: ArrayList, Go: slice)
    numbers: List[int] = [1, 2, 3]
    numbers.append(4)
    print(f"List: {numbers}")
    
    # Tuple (Java: no direct equivalent, Go: no direct equivalent)
    # Immutable sequence
    point: Tuple[int, int] = (10, 20)
    print(f"Tuple: {point}")
    
    # Set (Java: HashSet, Go: no direct equivalent)
    unique_numbers: Set[int] = {1, 2, 2, 3}  # Duplicates removed
    print(f"Set: {unique_numbers}")
    
    # Dictionary (Java: HashMap, Go: map)
    person: Dict[str, Any] = {
        "name": "Alice",
        "age": 30,
        "skills": ["Python", "Java", "Go"]
    }
    print(f"Dictionary: {person}")


def demonstrate_optional_and_union() -> None:
    """
    Demonstrates Optional and Union types.
    Similar to Java Optional and Go pointer/interface{}.
    """
    # Optional (can be None)
    maybe_name: Optional[str] = None
    print(f"Optional (None): {maybe_name}")
    
    maybe_name = "Alice"
    print(f"Optional (with value): {maybe_name}")
    
    # Union (multiple possible types)
    # Similar to Java Object or Go interface{}
    value: Union[int, str] = 42
    print(f"Union (int): {value}")
    
    value = "Hello"
    print(f"Union (str): {value}")


def main() -> None:
    print("Python Data Types Demo\n")
    
    # Numeric types
    print("=== Numeric Types ===")
    demonstrate_numeric_types()
    print()
    
    # Collections
    print("=== Collections ===")
    demonstrate_collections()
    print()
    
    # Optional and Union types
    print("=== Optional and Union Types ===")
    demonstrate_optional_and_union()
    print()
    
    # Data class example
    print("=== Data Class Example ===")
    person = Person(name="Alice", age=30)
    print(f"Person: {person}")
    print(f"Greeting: {person.greet()}")


if __name__ == "__main__":
    main() 