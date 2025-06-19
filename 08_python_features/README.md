# ✨ Advanced Python Features

## 📖 Introduction

This section explores advanced Python features that make the language unique and powerful. These features distinguish Python from Java and Go, offering expressive syntax and powerful abstractions for complex programming tasks.

## Decorators

### Function Decorators

```python
from functools import wraps
import time
from typing import Callable, Any, TypeVar, cast

F = TypeVar('F', bound=Callable[..., Any])

def timer(func: F) -> F:
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return cast(F, wrapper)

def retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorator factory for retrying failed operations."""
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)
            return None
        return cast(F, wrapper)
    return decorator

@timer
@retry(max_attempts=3, delay=0.5)
def unreliable_operation(x: int) -> int:
    """Example function that might fail."""
    import random
    if random.random() < 0.7:
        raise ValueError("Random failure")
    return x * 2
```

### Class Decorators

```python
from dataclasses import dataclass
from typing import Type, TypeVar

T = TypeVar('T')

def singleton(cls: Type[T]) -> Type[T]:
    """Singleton decorator for classes."""
    instances = {}
    def get_instance(*args: Any, **kwargs: Any) -> T:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class DatabaseConnection:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        print(f"Creating connection to {host}:{port}")
```

## Context Managers

### Using Context Managers

```python
from contextlib import contextmanager
from typing import Iterator, Any
import sqlite3

@contextmanager
def database_transaction(db_path: str) -> Iterator[sqlite3.Cursor]:
    """Context manager for database transactions."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

class ManagedResource:
    """Example resource that needs cleanup."""
    
    def __init__(self, name: str) -> None:
        self.name = name
        self.resource = None
    
    def __enter__(self):
        print(f"Acquiring resource: {self.name}")
        self.resource = f"resource_{self.name}"
        return self.resource
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Releasing resource: {self.name}")
        self.resource = None
        if exc_type:
            print(f"Exception occurred: {exc_val}")
        return False  # Don't suppress exceptions
```

## Generators and Iterators

### Generator Functions

```python
from typing import Iterator, Generator
import itertools

def fibonacci_generator() -> Generator[int, None, None]:
    """Generate Fibonacci numbers infinitely."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def read_large_file(filename: str) -> Generator[str, None, None]:
    """Read file line by line without loading into memory."""
    with open(filename, 'r') as file:
        for line in file:
            yield line.strip()

def batch_processor(iterable, batch_size: int):
    """Process items in batches."""
    iterator = iter(iterable)
    while True:
        batch = list(itertools.islice(iterator, batch_size))
        if not batch:
            break
        yield batch

# Usage examples
fib = fibonacci_generator()
first_10_fibs = [next(fib) for _ in range(10)]

for batch in batch_processor(range(100), 10):
    print(f"Processing batch: {batch}")
```

### Generator Expressions

```python
# Memory-efficient data processing
numbers = range(1000000)
squares = (x * x for x in numbers if x % 2 == 0)
sum_of_squares = sum(squares)

# Pipeline processing
def process_data(filename: str) -> int:
    lines = (line.strip() for line in open(filename))
    numbers = (int(line) for line in lines if line.isdigit())
    filtered = (n for n in numbers if n > 100)
    return sum(filtered)
```

## Metaclasses

### Understanding Metaclasses

```python
class SingletonMeta(type):
    """Metaclass that creates singleton instances."""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self, url: str) -> None:
        self.url = url

class AutoPropertyMeta(type):
    """Metaclass that automatically creates properties."""
    
    def __new__(mcs, name, bases, dct):
        # Find attributes that should become properties
        for key, value in list(dct.items()):
            if key.startswith('_') and not key.startswith('__'):
                prop_name = key[1:]  # Remove leading underscore
                
                def make_property(attr_name):
                    def getter(self):
                        return getattr(self, attr_name)
                    
                    def setter(self, value):
                        setattr(self, attr_name, value)
                    
                    return property(getter, setter)
                
                if prop_name not in dct:
                    dct[prop_name] = make_property(key)
        
        return super().__new__(mcs, name, bases, dct)

class Person(metaclass=AutoPropertyMeta):
    def __init__(self, name: str, age: int) -> None:
        self._name = name
        self._age = age
```

## Descriptors

### Creating Descriptors

```python
class TypedProperty:
    """Descriptor that enforces type checking."""
    
    def __init__(self, expected_type: type, default=None) -> None:
        self.expected_type = expected_type
        self.default = default
    
    def __set_name__(self, owner, name):
        self.name = f"_{name}"
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name, self.default)
    
    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"Expected {self.expected_type.__name__}, got {type(value).__name__}")
        setattr(instance, self.name, value)

class BoundedProperty:
    """Descriptor with value bounds."""
    
    def __init__(self, min_value=None, max_value=None) -> None:
        self.min_value = min_value
        self.max_value = max_value
    
    def __set_name__(self, owner, name):
        self.name = f"_{name}"
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name, 0)
    
    def __set__(self, instance, value):
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Value must be >= {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Value must be <= {self.max_value}")
        setattr(instance, self.name, value)

class Rectangle:
    width = BoundedProperty(min_value=0)
    height = BoundedProperty(min_value=0)
    color = TypedProperty(str, default="black")
    
    def __init__(self, width: float, height: float, color: str = "black") -> None:
        self.width = width
        self.height = height
        self.color = color
    
    @property
    def area(self) -> float:
        return self.width * self.height
```

## Lambda Functions and Functional Programming

### Lambda Expressions

```python
from functools import reduce, partial
from typing import List, Callable, Any

# Basic lambda usage
square = lambda x: x ** 2
add = lambda x, y: x + y

# Higher-order functions
def apply_operation(func: Callable, *args) -> Any:
    return func(*args)

result = apply_operation(lambda x, y: x * y + 1, 5, 3)

# Functional programming patterns
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Map, filter, reduce
squares = list(map(lambda x: x ** 2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
sum_all = reduce(lambda x, y: x + y, numbers)

# Partial application
multiply_by_2 = partial(lambda x, y: x * y, 2)
doubled = list(map(multiply_by_2, numbers))
```

### Functional Utilities

```python
from functools import reduce
from itertools import accumulate, chain, combinations
from operator import add, mul

def compose(*functions):
    """Compose multiple functions."""
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def curry(func):
    """Curry a function."""
    def curried(*args, **kwargs):
        if len(args) + len(kwargs) >= func.__code__.co_argcount:
            return func(*args, **kwargs)
        return lambda *more_args, **more_kwargs: curried(*(args + more_args), **{**kwargs, **more_kwargs})
    return curried

@curry
def add_three(a, b, c):
    return a + b + c

# Usage
add_5_and_3 = add_three(5)(3)
result = add_5_and_3(2)  # 10
```

## Comprehensions

### Advanced Comprehensions

```python
from typing import Dict, List, Set, Any

# Nested list comprehensions
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [item for row in matrix for item in row]
transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]

# Dictionary comprehensions with conditions
text = "hello world"
char_counts = {char: text.count(char) for char in set(text) if char.isalpha()}

# Set comprehensions
squares_set = {x**2 for x in range(10) if x % 2 == 0}

# Generator expressions for memory efficiency
large_squares = (x**2 for x in range(1000000) if x % 1000 == 0)

# Complex comprehensions
students = [
    {"name": "Alice", "grades": [85, 92, 78]},
    {"name": "Bob", "grades": [79, 85, 88]},
    {"name": "Charlie", "grades": [92, 95, 89]}
]

# Calculate averages
averages = {
    student["name"]: sum(student["grades"]) / len(student["grades"])
    for student in students
}

# Find high performers
high_performers = [
    student["name"] 
    for student in students 
    if sum(student["grades"]) / len(student["grades"]) > 85
]
```

## Property Decorators

### Advanced Property Usage

```python
class Circle:
    """Circle with computed properties."""
    
    def __init__(self, radius: float) -> None:
        self._radius = radius
        self._diameter = None
        self._area = None
    
    @property
    def radius(self) -> float:
        return self._radius
    
    @radius.setter
    def radius(self, value: float) -> None:
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value
        # Invalidate cached values
        self._diameter = None
        self._area = None
    
    @property
    def diameter(self) -> float:
        if self._diameter is None:
            self._diameter = 2 * self._radius
        return self._diameter
    
    @property
    def area(self) -> float:
        if self._area is None:
            import math
            self._area = math.pi * self._radius ** 2
        return self._area
    
    @property
    def circumference(self) -> float:
        import math
        return 2 * math.pi * self._radius

class LazyProperty:
    """Descriptor for lazy-loaded properties."""
    
    def __init__(self, func: Callable) -> None:
        self.func = func
        self.name = func.__name__
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        # Check if value is cached
        cache_name = f"_cached_{self.name}"
        if not hasattr(instance, cache_name):
            # Compute and cache the value
            value = self.func(instance)
            setattr(instance, cache_name, value)
        
        return getattr(instance, cache_name)

class DataProcessor:
    def __init__(self, data: List[int]) -> None:
        self.data = data
    
    @LazyProperty
    def sorted_data(self) -> List[int]:
        """Expensive sorting operation, computed only when needed."""
        print("Computing sorted data...")
        return sorted(self.data)
    
    @LazyProperty
    def statistics(self) -> Dict[str, float]:
        """Expensive statistical computation."""
        print("Computing statistics...")
        return {
            'mean': sum(self.data) / len(self.data),
            'min': min(self.data),
            'max': max(self.data),
        }
```

## Type Hints and Protocols

### Advanced Type Hints

```python
from typing import Protocol, TypeVar, Generic, Union, Optional, overload
from abc import ABC, abstractmethod

# Protocol definition
class Drawable(Protocol):
    def draw(self) -> str: ...
    def get_area(self) -> float: ...

# Generic types
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

class Container(Generic[T]):
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def add(self, item: T) -> None:
        self._items.append(item)
    
    def get(self, index: int) -> T:
        return self._items[index]

# Overloaded functions
@overload
def process_data(data: str) -> str: ...

@overload
def process_data(data: int) -> int: ...

@overload
def process_data(data: List[str]) -> List[str]: ...

def process_data(data: Union[str, int, List[str]]) -> Union[str, int, List[str]]:
    if isinstance(data, str):
        return data.upper()
    elif isinstance(data, int):
        return data * 2
    elif isinstance(data, list):
        return [item.upper() for item in data]
    else:
        raise TypeError("Unsupported type")

# Runtime protocol checking
from typing import runtime_checkable

@runtime_checkable
class Serializable(Protocol):
    def serialize(self) -> str: ...

class JSONSerializable:
    def __init__(self, data: dict) -> None:
        self.data = data
    
    def serialize(self) -> str:
        import json
        return json.dumps(self.data)

# Check at runtime
obj = JSONSerializable({"key": "value"})
assert isinstance(obj, Serializable)
```

## Error Handling Patterns

### Custom Exceptions and Error Handling

```python
class APIError(Exception):
    """Base exception for API-related errors."""
    def __init__(self, message: str, status_code: Optional[int] = None) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class ValidationError(APIError):
    """Exception for validation errors."""
    def __init__(self, field: str, message: str) -> None:
        super().__init__(f"Validation error in field '{field}': {message}")
        self.field = field

class RetryableError(APIError):
    """Exception that indicates an operation should be retried."""
    pass

def safe_execute(func: Callable, *args, **kwargs) -> tuple:
    """Execute function safely and return result or error."""
    try:
        result = func(*args, **kwargs)
        return result, None
    except Exception as e:
        return None, e

# Context manager for error handling
@contextmanager
def error_handler(error_callback: Optional[Callable] = None):
    """Context manager for centralized error handling."""
    try:
        yield
    except Exception as e:
        if error_callback:
            error_callback(e)
        else:
            print(f"Error occurred: {e}")
        raise

# Usage
def risky_operation():
    raise ValueError("Something went wrong")

with error_handler(lambda e: print(f"Logged error: {e}")):
    risky_operation()
```

## Performance Optimization Features

### Slots and Memory Optimization

```python
class RegularClass:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

class SlottedClass:
    __slots__ = ['x', 'y']
    
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

# Memory usage comparison
import sys

regular = RegularClass(1, 2)
slotted = SlottedClass(1, 2)

print(f"Regular class size: {sys.getsizeof(regular)} bytes")
print(f"Slotted class size: {sys.getsizeof(slotted)} bytes")
```

### Caching Decorators

```python
from functools import lru_cache, cached_property
import time

class ExpensiveComputation:
    def __init__(self, data: List[int]) -> None:
        self.data = data
    
    @lru_cache(maxsize=128)
    def fibonacci(self, n: int) -> int:
        """Cached Fibonacci computation."""
        if n < 2:
            return n
        return self.fibonacci(n-1) + self.fibonacci(n-2)
    
    @cached_property
    def mean(self) -> float:
        """Cached property that's computed once."""
        print("Computing mean...")
        return sum(self.data) / len(self.data)

# Custom caching decorator
def timed_cache(seconds: float):
    """Cache with time-based expiration."""
    def decorator(func):
        cache = {}
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()
            
            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < seconds:
                    return result
            
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        
        wrapper.cache_clear = lambda: cache.clear()
        return wrapper
    return decorator

@timed_cache(seconds=60)
def expensive_api_call(url: str) -> dict:
    """Simulated expensive API call with time-based caching."""
    print(f"Making API call to {url}")
    time.sleep(1)  # Simulate network delay
    return {"data": f"response from {url}"}
```

## Comparison with Java and Go

### Feature Comparison Table

| Feature | Python | Java | Go |
|---------|--------|------|-----|
| **Decorators** | Built-in syntax | Annotations (limited) | Not built-in |
| **Generators** | Built-in `yield` | Not built-in | Channels (different concept) |
| **Context Managers** | `with` statement | try-with-resources | `defer` (different) |
| **Metaclasses** | Full support | Reflection API | Reflection (limited) |
| **Duck Typing** | Built-in | Interface-based | Interface-based |
| **Comprehensions** | List/Dict/Set/Generator | Streams (Java 8+) | Not built-in |
| **Properties** | `@property` decorator | Getter/setter methods | Method conventions |
| **Lambda Functions** | Full support | Limited lambdas | Function literals |

### Idiomatic Patterns

```python
# Python: Using decorators and context managers
@retry(max_attempts=3)
@timer
def process_file(filename: str) -> dict:
    with open(filename) as f:
        return {"lines": len(f.readlines())}

# Python: Generator expressions
total = sum(x**2 for x in range(1000) if x % 2 == 0)

# Python: Dictionary comprehension with conditions
word_lengths = {word: len(word) for word in text.split() if len(word) > 3}

# Python: Using protocols for duck typing
def process_drawable(item: Drawable) -> None:
    print(item.draw())
    print(f"Area: {item.get_area()}")
```

## Best Practices

### 1. Use Decorators Wisely

```python
# Good: Simple, focused decorators
@timer
@cache
def expensive_function():
    pass

# Avoid: Complex decorators that obscure functionality
```

### 2. Leverage Context Managers

```python
# Good: Always use context managers for resources
with open('file.txt') as f:
    content = f.read()

# Good: Custom context managers for cleanup
with database_transaction() as cursor:
    cursor.execute("INSERT INTO table VALUES (?)", (value,))
```

### 3. Use Generators for Large Data

```python
# Good: Memory-efficient processing
def process_large_file(filename):
    with open(filename) as f:
        for line in f:
            yield process_line(line)

# Avoid: Loading everything into memory
```

### 4. Type Hints for Clarity

```python
from typing import List, Dict, Optional, Protocol

# Good: Clear type annotations
def process_users(users: List[Dict[str, str]]) -> Optional[str]:
    return users[0]['name'] if users else None

# Use protocols for flexible interfaces
class Processable(Protocol):
    def process(self) -> str: ...
```

## Additional Resources

1. **Official Documentation**
   - [Decorators](https://docs.python.org/3/glossary.html#term-decorator)
   - [Context Managers](https://docs.python.org/3/reference/datamodel.html#context-managers)
   - [Generators](https://docs.python.org/3/glossary.html#term-generator)

2. **PEPs**
   - [PEP 318 – Decorators](https://www.python.org/dev/peps/pep-0318/)
   - [PEP 343 – Context Managers](https://www.python.org/dev/peps/pep-0343/)
   - [PEP 484 – Type Hints](https://www.python.org/dev/peps/pep-0484/)

3. **Advanced Topics**
   - [Metaclasses](https://docs.python.org/3/reference/datamodel.html#metaclasses)
   - [Descriptors](https://docs.python.org/3/howto/descriptor.html)
   - [Functional Programming](https://docs.python.org/3/howto/functional.html) 