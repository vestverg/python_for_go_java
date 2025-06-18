# Python Functions and Methods

## Introduction

This section covers Python's function and method system, including advanced features like decorators, type hints, and functional programming concepts. We'll explore how Python's approach to functions differs from Java and Go, highlighting unique features and best practices.

## Function Basics

### Function Definition and Type Hints

Python functions can be defined with or without type hints:

```python
# Basic function definition
def greet(name):
    return f"Hello, {name}!"

# With type hints (Python 3.5+)
def greet_typed(name: str) -> str:
    return f"Hello, {name}!"

# Multiple parameters
def calculate_total(
    items: List[float],
    tax_rate: float = 0.1,
    discount: Optional[float] = None
) -> float:
    subtotal = sum(items)
    if discount:
        subtotal *= (1 - discount)
    return subtotal * (1 + tax_rate)
```

### Default Arguments and Keyword Arguments

Python offers flexible parameter handling:

```python
def create_user(
    username: str,
    email: str,
    *,  # Keyword-only arguments after this
    is_active: bool = True,
    role: str = "user"
) -> Dict[str, Any]:
    return {
        "username": username,
        "email": email,
        "is_active": is_active,
        "role": role
    }

# Different ways to call
user1 = create_user("alice", "alice@example.com")
user2 = create_user("bob", "bob@example.com", role="admin")
user3 = create_user(
    username="charlie",
    email="charlie@example.com",
    is_active=False
)
```

## Advanced Function Features

### Decorators

Python's decorator syntax provides elegant metaprogramming:

```python
from functools import wraps
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

def log_calls(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@log_calls
def add(x: int, y: int) -> int:
    return x + y

# Class method decorators
class Timer:
    def __init__(self, description: str) -> None:
        self.description = description
    
    def __call__(self, func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            import time
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"{self.description}: {end - start:.2f}s")
            return result
        return wrapper

@Timer("Sorting time")
def sort_list(items: List[int]) -> List[int]:
    return sorted(items)
```

### Generator Functions

Python's generators provide memory-efficient iteration:

```python
from typing import Generator, Iterator

def fibonacci(n: int) -> Generator[int, None, None]:
    """Generate first n Fibonacci numbers."""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Using the generator
for num in fibonacci(10):
    print(num)

# Generator expression
squares = (x * x for x in range(1000))
```

### Lambda Functions

Concise anonymous functions:

```python
from typing import Callable

# Lambda function
square: Callable[[int], int] = lambda x: x * x

# With higher-order functions
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x * x, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
```

## Functional Programming Features

### Higher-Order Functions

Python supports functional programming patterns:

```python
from typing import Callable, TypeVar, List

T = TypeVar('T')
R = TypeVar('R')

def map_list(func: Callable[[T], R], items: List[T]) -> List[R]:
    return [func(item) for item in items]

def filter_list(pred: Callable[[T], bool], items: List[T]) -> List[T]:
    return [item for item in items if pred(item)]

def compose(
    f: Callable[[T], R],
    g: Callable[[R], T]
) -> Callable[[T], T]:
    return lambda x: g(f(x))
```

### Partial Functions

Creating new functions with fixed arguments:

```python
from functools import partial
from typing import Callable

def power(base: float, exponent: float) -> float:
    return base ** exponent

# Create new function with fixed base
square: Callable[[float], float] = partial(power, exponent=2)
cube: Callable[[float], float] = partial(power, exponent=3)
```

## Type Hints and Function Annotations

### Type Variables and Generics

```python
from typing import TypeVar, Generic, List

T = TypeVar('T')
S = TypeVar('S')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self.items: List[T] = []
    
    def push(self, item: T) -> None:
        self.items.append(item)
    
    def pop(self) -> T:
        return self.items.pop()

def map_optional(
    func: Callable[[T], S],
    value: Optional[T]
) -> Optional[S]:
    return None if value is None else func(value)
```

### Protocol Classes

Defining interfaces with protocols:

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> None: ...

@runtime_checkable
class Sizeable(Protocol):
    def get_size(self) -> tuple[float, float]: ...

def render(item: Drawable & Sizeable) -> None:
    size = item.get_size()
    print(f"Rendering item of size {size}")
    item.draw()
```

## Best Practices

### 1. Function Design

```python
# Good - Single Responsibility
def process_user_data(user_data: Dict[str, Any]) -> User:
    """Process and validate user data."""
    validate_user_data(user_data)
    return create_user(user_data)

# Bad - Multiple Responsibilities
def process_and_save_user(
    user_data: Dict[str, Any],
    send_email: bool = True
) -> None:
    """Do too many things."""
    validate_user_data(user_data)
    user = create_user(user_data)
    save_to_database(user)
    if send_email:
        send_welcome_email(user)
```

### 2. Error Handling

```python
from typing import Optional

def find_user(user_id: int) -> Optional[User]:
    """
    Find a user by ID.
    
    Args:
        user_id: The user's unique identifier
    
    Returns:
        User object if found, None otherwise
    
    Raises:
        ValueError: If user_id is negative
    """
    if user_id < 0:
        raise ValueError("User ID cannot be negative")
    
    try:
        return database.get_user(user_id)
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        return None
```

### 3. Documentation

```python
def calculate_statistics(
    numbers: List[float],
    *,
    include_mode: bool = False
) -> Dict[str, float]:
    """
    Calculate basic statistics for a list of numbers.
    
    Args:
        numbers: List of numbers to analyze
        include_mode: Whether to include mode in results
    
    Returns:
        Dictionary containing statistics:
        - mean: Arithmetic mean
        - median: Middle value
        - std_dev: Standard deviation
        - mode: Most common value (if include_mode is True)
    
    Raises:
        ValueError: If numbers is empty
    
    Example:
        >>> stats = calculate_statistics([1, 2, 2, 3])
        >>> stats['mean']
        2.0
    """
    if not numbers:
        raise ValueError("Cannot calculate statistics of empty list")
    
    result = {
        "mean": sum(numbers) / len(numbers),
        "median": calculate_median(numbers),
        "std_dev": calculate_std_dev(numbers)
    }
    
    if include_mode:
        result["mode"] = calculate_mode(numbers)
    
    return result
```

## Testing Functions

### Unit Testing with pytest

```python
import pytest
from typing import List, Dict, Any

def test_calculate_statistics() -> None:
    """Test statistics calculation."""
    numbers = [1, 2, 2, 3, 4]
    result = calculate_statistics(numbers, include_mode=True)
    
    assert isinstance(result, dict)
    assert result["mean"] == 2.4
    assert result["mode"] == 2
    
    with pytest.raises(ValueError):
        calculate_statistics([])

@pytest.mark.parametrize("input,expected", [
    ([1, 2, 3], 2),
    ([1, 1, 1], 1),
    ([5, 5, 5, 5], 5),
])
def test_calculate_mode(
    input: List[int],
    expected: int
) -> None:
    """Test mode calculation with different inputs."""
    assert calculate_mode(input) == expected
```

## Common Pitfalls

### 1. Mutable Default Arguments

```python
# Wrong
def append_to_list(item: T, items: List[T] = []) -> List[T]:
    items.append(item)
    return items

# Right
def append_to_list(item: T, items: Optional[List[T]] = None) -> List[T]:
    if items is None:
        items = []
    items.append(item)
    return items
```

### 2. Late Binding Closures

```python
# Wrong
def create_multipliers() -> List[Callable[[int], int]]:
    return [lambda x: i * x for i in range(4)]

# Right
def create_multipliers() -> List[Callable[[int], int]]:
    return [lambda x, i=i: i * x for i in range(4)]
```

### 3. Overusing Lambda Functions

```python
# Wrong - hard to read
process_data(lambda x: x.strip().lower().replace(' ', '_'))

# Right - more readable
def clean_string(s: str) -> str:
    return s.strip().lower().replace(' ', '_')
process_data(clean_string)
```

## Additional Resources

1. **Official Documentation**
   - [Python Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
   - [Function Annotations](https://docs.python.org/3/howto/annotations.html)
   - [Decorators](https://docs.python.org/3/glossary.html#term-decorator)

2. **PEPs**
   - [PEP 484 – Type Hints](https://www.python.org/dev/peps/pep-0484/)
   - [PEP 3107 – Function Annotations](https://www.python.org/dev/peps/pep-3107/)
   - [PEP 612 – Parameter Specification Variables](https://www.python.org/dev/peps/pep-0612/)

3. **External Resources**
   - [Real Python - Decorators](https://realpython.com/primer-on-python-decorators/)
   - [Real Python - Type Checking](https://realpython.com/python-type-checking/)
   - [Python Design Patterns](https://python-patterns.guide/) 