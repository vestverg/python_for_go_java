from typing import List, Tuple, Union, Optional
from dataclasses import dataclass
import random

@dataclass
class Point:
    x: float
    y: float

def demonstrate_conditionals(value: int) -> None:
    """Demonstrate conditional statements."""
    # Basic if-elif-else
    if value > 0:
        print(f"{value} is positive")
    elif value < 0:
        print(f"{value} is negative")
    else:
        print(f"{value} is zero")
    
    # Match statement (Python 3.10+)
    match value:
        case 0:
            print("Found zero")
        case x if x > 0:
            print(f"Found positive number: {x}")
        case x if x < 0:
            print(f"Found negative number: {x}")
        case _:
            print("This should never happen")

def demonstrate_loops() -> List[int]:
    """Demonstrate different types of loops."""
    results: List[int] = []
    
    # For loop with range
    print("Range loop:")
    for i in range(3):
        print(f"Count: {i}")
        results.append(i)
    
    # For loop with list
    print("\nList loop:")
    fruits = ["apple", "banana", "cherry"]
    for i, fruit in enumerate(fruits):
        print(f"Fruit {i}: {fruit}")
    
    # While loop
    print("\nWhile loop:")
    count = 0
    while count < 3:
        print(f"While count: {count}")
        count += 1
    
    # Loop control
    print("\nLoop control:")
    for i in range(5):
        if i == 2:
            continue  # Skip 2
        if i == 4:
            break    # Stop at 4
        print(f"Number: {i}")
    
    return results

def demonstrate_exception_handling(filename: str) -> Optional[str]:
    """Demonstrate exception handling."""
    try:
        # Try to open and read a file
        with open(filename, 'r') as file:
            content = file.read()
            number = int(content)
            result = 10 / number
            return f"Result: {result}"
            
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except ValueError:
        print("Error: File content is not a valid number")
    except ZeroDivisionError:
        print("Error: Cannot divide by zero")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        print("Cleanup complete")
    
    return None

def demonstrate_pattern_matching(command: Union[Tuple, Point]) -> str:
    """Demonstrate pattern matching with different types."""
    match command:
        # Match tuples
        case ("quit",):
            return "Goodbye!"
        case ("greet", name):
            return f"Hello, {name}!"
        case ("move", x, y):
            return f"Moving to ({x}, {y})"
        # Match Point class
        case Point(x=0, y=0):
            return "At origin"
        case Point(x=x, y=y) if x == y:
            return f"On diagonal at ({x}, {y})"
        case Point(x=x, y=y):
            return f"At point ({x}, {y})"
        case _:
            return "Unknown command"

if __name__ == "__main__":
    print("=== Conditionals ===")
    demonstrate_conditionals(42)
    demonstrate_conditionals(-17)
    demonstrate_conditionals(0)
    
    print("\n=== Loops ===")
    results = demonstrate_loops()
    print(f"Loop results: {results}")
    
    print("\n=== Exception Handling ===")
    demonstrate_exception_handling("nonexistent.txt")
    
    print("\n=== Pattern Matching ===")
    commands = [
        ("quit",),
        ("greet", "Alice"),
        ("move", 10, 20),
        Point(0, 0),
        Point(3, 3),
        Point(1, 2)
    ]
    
    for cmd in commands:
        result = demonstrate_pattern_matching(cmd)
        print(f"Command {cmd}: {result}") 