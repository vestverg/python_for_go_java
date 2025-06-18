# Functions in Python

This section covers Python's function features, with comparisons to Java and Go.

## Function Definitions

### Basic Functions

```python
# Python
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Multiple return values
def divide_and_remainder(x: int, y: int) -> tuple[int, int]:
    return x // y, x % y
```

```go
// Go - multiple return values
func divideAndRemainder(x, y int) (int, int) {
    return x / y, x % y
}
```

```java
// Java - needs wrapper class for multiple returns
public class DivisionResult {
    public final int quotient;
    public final int remainder;
    
    public DivisionResult(int q, int r) {
        quotient = q;
        remainder = r;
    }
}
```

### Default Arguments

```python
# Python
def create_user(name: str, age: int = 18, is_admin: bool = False) -> dict:
    return {"name": name, "age": age, "is_admin": is_admin}

# Different ways to call
user1 = create_user("Alice")
user2 = create_user("Bob", 25)
user3 = create_user("Charlie", is_admin=True)  # Named arguments
```

### Args and Kwargs

```python
# Python - variable arguments
def sum_all(*args: int) -> int:
    return sum(args)

# Keyword arguments
def create_config(**kwargs: str) -> dict:
    return kwargs

# Usage
total = sum_all(1, 2, 3, 4, 5)
config = create_config(host="localhost", port="8080")
```

## Lambda Functions

```python
# Python
square = lambda x: x * x
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x * x, numbers))

# Sorting with lambda
points = [(1, 2), (3, 1), (2, 5)]
sorted_points = sorted(points, key=lambda p: p[1])  # Sort by y coordinate
```

## Decorators

### Basic Decorators

```python
# Python
def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@log_call
def add(x: int, y: int) -> int:
    return x + y
```

### Decorators with Arguments

```python
# Python
def retry(attempts: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == attempts - 1:
                        raise e
                    print(f"Attempt {i+1} failed, retrying...")
            return None
        return wrapper
    return decorator

@retry(attempts=3)
def unstable_function():
    # Some potentially failing operation
    pass
```

## Type Hints

### Basic Type Hints

```python
from typing import List, Dict, Optional, Union

def process_data(
    items: List[str],
    config: Dict[str, int],
    debug: Optional[bool] = None
) -> Union[str, int]:
    pass
```

### Generic Types

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self.items: List[T] = []
    
    def push(self, item: T) -> None:
        self.items.append(item)
    
    def pop(self) -> Optional[T]:
        return self.items.pop() if self.items else None
```

### Protocol Classes (Structural Typing)

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None:
        pass

def render(item: Drawable) -> None:
    item.draw()  # Works with any class that has a draw method
```

## Function Annotations

```python
# Python
def process_item(
    item: str,
    *,           # Force keyword arguments after this
    count: int,
    debug: bool = False
) -> str:
    """
    Process an item with the given parameters.
    
    Args:
        item: The item to process
        count: Number of times to process
        debug: Enable debug output
    
    Returns:
        Processed item string
    
    Raises:
        ValueError: If count is negative
    """
    if count < 0:
        raise ValueError("Count must be non-negative")
    return item * count
```

## Next Steps

1. Practice writing decorators
2. Experiment with type hints
3. Try implementing generic classes
4. Move on to the OOP section 