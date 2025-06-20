#!/usr/bin/env python3

"""
This example demonstrates Python's control flow mechanisms,
with comparisons to Java and Go concepts.
"""

from typing import Any, List, Optional, Dict
from dataclasses import dataclass
import sys
from contextlib import contextmanager


class ValidationError(Exception):
    """Custom exception for validation errors."""
    def __init__(self, message: str, code: int):
        super().__init__(message)
        self.code = code

    def __str__(self) -> str:
        return super().__str__()


def check_grade(score: int) -> str:
    """Returns a letter grade based on a numeric score."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def analyze_data(data: List[Any]) -> Dict[str, Any]:
    """Analyzes a list of data and returns a summary."""
    if not data:
        return {"type": "empty", "count": 0}

    if all(isinstance(x, (int, float)) for x in data):
        return {"type": "numbers", "count": len(data), "sum": sum(data)}
    
    if all(isinstance(x, str) for x in data):
        return {"type": "strings", "count": len(data), "total_length": sum(len(s) for s in data)}
    
    return {"type": "mixed", "count": len(data)}


def safe_divide(a: float, b: float) -> float:
    """Divides two numbers, raising an error if the divisor is zero."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b


@dataclass
class User:
    """Simple user class for demonstration"""
    name: str
    age: int


def demonstrate_conditionals(value: Any) -> None:
    print("\n=== Conditionals ===")
    
    # Basic if-elif-else
    if isinstance(value, str):
        print(f"Got a string: {value}")
    elif isinstance(value, int):
        print(f"Got an integer: {value}")
    else:
        print(f"Got something else: {type(value)}")
    
    # Ternary operator
    result = ("even" if value % 2 == 0 else "odd") if isinstance(value, int) else "not a number"
    print(f"Value is: {result}")


def demonstrate_loops() -> None:
    print("\n=== Loops ===")
    
    # For loop over a list
    print("Basic for loop:")
    fruits = ["apple", "banana", "cherry"]
    for fruit in fruits:
        print(f"- {fruit}")
    
    # For loop with enumerate (similar to Go's for range with index)
    print("\nFor loop with index:")
    for i, fruit in enumerate(fruits):
        print(f"{i + 1}. {fruit}")
    
    # Range-based for loop (similar to C-style for loop)
    print("\nRange-based loop:")
    for i in range(3):
        print(f"Count: {i}")
    
    # While loop
    print("\nWhile loop:")
    count = 0
    while count < 3:
        print(f"While count: {count}")
        count += 1


def demonstrate_exception_handling(filename: str) -> None:
    print("\n=== Exception Handling ===")
    
    try:
        # Attempt to read a file (potentially risky operation)
        with open(filename, 'r') as f:
            content = f.read()
            print(f"File contents: {content}")
    except FileNotFoundError as e:
        # Handle specific exception (like catch in Java)
        print(f"Error: File not found - {e}")
    except Exception as e:
        # Handle any other exception (like catch Exception in Java)
        print(f"Error: An unexpected error occurred - {e}")
    else:
        # Runs if no exception occurred
        print("File was read successfully")
    finally:
        # Always runs (like finally in Java)
        print("Cleanup complete")


@contextmanager
def temporary_file(content: str) -> None:
    """Custom context manager (similar to AutoCloseable in Java)"""
    filename = "temp.txt"
    try:
        with open(filename, 'w') as f:
            f.write(content)
        yield filename
    finally:
        try:
            import os
            os.remove(filename)
        except OSError:
            pass


def demonstrate_context_managers() -> None:
    print("\n=== Context Managers ===")
    
    # Using our custom context manager
    with temporary_file("Hello, World!") as filename:
        print(f"Temporary file created: {filename}")
        # File is automatically cleaned up after the with block
    print("Temporary file cleaned up")


def process_value(value: Any) -> None:
    """Demonstrate pattern matching (Python 3.10+)"""
    print("\n=== Pattern Matching ===")
    
    # Pattern matching (similar to switch but more powerful)
    match value:
        case str():
            print(f"Got a string: {value}")
        case int():
            print(f"Got an integer: {value}")
        case list() | tuple():
            print(f"Got a sequence: {value}")
        case User(name=name, age=age):
            print(f"Got a user: {name}, {age} years old")
        case _:
            print(f"Got something else: {value}")


def find_user(users: List[User], target_name: str) -> Optional[User]:
    """Example of control flow in a practical function"""
    # List comprehension with conditional (filter)
    matching_users = [user for user in users if user.name.lower() == target_name.lower()]
    
    # Return first match if found, None otherwise
    return matching_users[0] if matching_users else None


def main() -> None:
    # Demonstrate conditionals
    demonstrate_conditionals(42)
    demonstrate_conditionals("Hello")
    
    # Demonstrate loops
    demonstrate_loops()
    
    # Demonstrate exception handling
    demonstrate_exception_handling("nonexistent.txt")
    
    # Demonstrate context managers
    demonstrate_context_managers()
    
    # Demonstrate pattern matching
    process_value(42)
    process_value("Hello")
    process_value([1, 2, 3])
    process_value(User("Alice", 30))
    
    # Practical example
    users = [
        User("Alice", 30),
        User("Bob", 25),
        User("Charlie", 35)
    ]
    
    # Find a user
    if user := find_user(users, "Alice"):  # Assignment expression (Python 3.8+)
        print(f"\nFound user: {user.name}, {user.age} years old")
    else:
        print("\nUser not found")


if __name__ == "__main__":
    main() 