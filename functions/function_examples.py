from typing import TypeVar, Generic, List, Dict, Optional, Union, Protocol
from dataclasses import dataclass
from functools import wraps
import time
import random

# Example of type variable for generics
T = TypeVar('T')

# Protocol example
class Drawable(Protocol):
    def draw(self) -> None:
        pass

# Example class implementing the protocol
@dataclass
class Circle:
    radius: float
    
    def draw(self) -> None:
        print(f"Drawing circle with radius {self.radius}")

# Generic class example
class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> Optional[T]:
        return self._items.pop() if self._items else None
    
    def is_empty(self) -> bool:
        return len(self._items) == 0

# Decorator examples
def timer(func):
    """Measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper

def retry(attempts: int, delay: float = 1.0):
    """Retry a function multiple times with delay."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == attempts - 1:
                        raise e
                    print(f"Attempt {i+1} failed, retrying in {delay} seconds...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

# Function with type hints and default arguments
def create_user(
    name: str,
    age: int = 18,
    *,  # Force remaining arguments to be keyword-only
    email: Optional[str] = None,
    is_admin: bool = False
) -> Dict[str, Union[str, int, bool]]:
    """
    Create a user dictionary with the given parameters.
    
    Args:
        name: User's name
        age: User's age (default: 18)
        email: User's email (optional)
        is_admin: Whether user is admin (default: False)
    
    Returns:
        Dictionary containing user information
    """
    return {
        "name": name,
        "age": age,
        "email": email,
        "is_admin": is_admin
    }

# Function using *args
def calculate_stats(*numbers: float) -> Dict[str, float]:
    """Calculate basic statistics for a series of numbers."""
    if not numbers:
        raise ValueError("At least one number is required")
    
    return {
        "sum": sum(numbers),
        "average": sum(numbers) / len(numbers),
        "min": min(numbers),
        "max": max(numbers)
    }

# Function using **kwargs
def create_config(**settings: str) -> Dict[str, str]:
    """Create a configuration dictionary from keyword arguments."""
    return settings

# Example of a potentially failing function
@retry(attempts=3, delay=0.1)
def unstable_operation() -> str:
    """Simulate an unstable operation that might fail."""
    if random.random() < 0.7:  # 70% chance of failure
        raise ConnectionError("Network error")
    return "Operation successful"

# Example using the Drawable protocol
def render_shapes(shapes: List[Drawable]) -> None:
    """Render a list of shapes that implement the Drawable protocol."""
    for shape in shapes:
        shape.draw()

@timer
def slow_operation(duration: float) -> None:
    """Simulate a slow operation."""
    time.sleep(duration)

def main() -> None:
    # Demonstrate basic function usage
    print("=== Basic Function Usage ===")
    user = create_user("Alice", 25, email="alice@example.com", is_admin=True)
    print(f"Created user: {user}")
    
    # Demonstrate *args
    print("\n=== Variable Arguments ===")
    stats = calculate_stats(1.0, 2.0, 3.0, 4.0, 5.0)
    print(f"Statistics: {stats}")
    
    # Demonstrate **kwargs
    print("\n=== Keyword Arguments ===")
    config = create_config(host="localhost", port="8080", debug="true")
    print(f"Configuration: {config}")
    
    # Demonstrate generic Stack
    print("\n=== Generic Stack ===")
    number_stack: Stack[int] = Stack()
    number_stack.push(1)
    number_stack.push(2)
    print(f"Popped: {number_stack.pop()}")
    
    # Demonstrate protocol usage
    print("\n=== Protocol Usage ===")
    shapes: List[Drawable] = [
        Circle(5.0),
        Circle(3.0)
    ]
    render_shapes(shapes)
    
    # Demonstrate decorators
    print("\n=== Decorators ===")
    slow_operation(0.1)  # Will show execution time
    
    print("\n=== Retry Decorator ===")
    try:
        result = unstable_operation()
        print(f"Result: {result}")
    except ConnectionError as e:
        print(f"Final error: {e}")

if __name__ == "__main__":
    main() 