# 🔄 Control Flow in Python

## 📖 Introduction

This section covers Python's control flow mechanisms, including conditionals, loops, and exception handling. We'll explore how Python's approach differs from Java and Go, highlighting unique features like pattern matching and context managers.

## ⚖️ Conditional Statements

### 🔀 If-Elif-Else

Python's conditional statements are more concise than Java/Go:

```python
# Python
def check_value(x: int) -> str:
    if x > 0:
        return "positive"
    elif x < 0:
        return "negative"
    else:
        return "zero"

# Java equivalent
public String checkValue(int x) {
    if (x > 0) {
        return "positive";
    } else if (x < 0) {
        return "negative";
    } else {
        return "zero";
    }
}

# Go equivalent
func checkValue(x int) string {
    if x > 0 {
        return "positive"
    } else if x < 0 {
        return "negative"
    } else {
        return "zero"
    }
}
```

### 🎯 Pattern Matching (Python 3.10+)

Pattern matching is similar to Java's switch expressions or Go's switch statements but more powerful:

```python
def analyze_value(value: object) -> str:
    match value:
        case int() as x if x > 0:
            return f"positive integer: {x}"
        case int() as x if x < 0:
            return f"negative integer: {x}"
        case str() as s:
            return f"string of length {len(s)}"
        case list() | tuple() as seq:
            return f"sequence of length {len(seq)}"
        case dict() as d:
            return f"dictionary with {len(d)} items"
        case _:
            return "unknown type"
```

### ❓ Ternary Operator

Python's ternary operator is more readable than Java/Go:

```python
# Python
result = "even" if x % 2 == 0 else "odd"

# Java equivalent
String result = x % 2 == 0 ? "even" : "odd";

# Go equivalent
result := map[bool]string{true: "even", false: "odd"}[x%2 == 0]
```

## 🔁 Loops and Iterations

### 🔢 For Loops

Python's for loops are more versatile than Java/Go:

```python
# Basic range loop
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# Iterating over collections
names = ["Alice", "Bob", "Charlie"]
for name in names:
    print(name)

# Enumerate for index and value
for i, name in enumerate(names):
    print(f"{i}: {name}")

# Dictionary iteration
person = {"name": "Alice", "age": 30}
for key, value in person.items():
    print(f"{key}: {value}")
```

### 📊 List Comprehensions

A powerful feature not found in Java/Go:

```python
# List comprehension
squares = [x * x for x in range(10)]

# With condition
even_squares = [x * x for x in range(10) if x % 2 == 0]

# Dictionary comprehension
square_map = {x: x * x for x in range(5)}

# Set comprehension
unique_chars = {c for c in "hello world"}
```

### ⏳ While Loops

Similar to Java/Go but with Python's cleaner syntax:

```python
# Basic while loop
count = 0
while count < 5:
    print(count)
    count += 1

# Break and continue
while True:
    value = input("Enter number (q to quit): ")
    if value == 'q':
        break
    if not value.isdigit():
        continue
    print(int(value) * 2)
```

## 🚨 Exception Handling

### 🛡️ Try-Except Blocks

More flexible than Java's try-catch or Go's error handling:

```python
def safe_divide(x: float, y: float) -> float:
    try:
        result = x / y
    except ZeroDivisionError:
        print("Division by zero!")
        raise
    except TypeError as e:
        print(f"Type error: {e}")
        raise
    else:
        print("Division successful")
        return result
    finally:
        print("Cleanup code")
```

### ⚠️ Custom Exceptions

Creating custom exceptions is easier than in Java/Go:

```python
class ValidationError(Exception):
    """Custom exception for validation errors."""
    def __init__(self, message: str, code: int = 400) -> None:
        self.message = message
        self.code = code
        super().__init__(self.message)

def validate_age(age: int) -> None:
    if age < 0:
        raise ValidationError("Age cannot be negative")
    if age > 150:
        raise ValidationError("Age seems unrealistic")
```

### 🔒 Context Managers

Python's with statement is more powerful than Java's try-with-resources or Go's defer:

```python
# File handling with context manager
def process_file(filename: str) -> None:
    with open(filename, 'r') as file:
        content = file.read()
        # File automatically closed after block

# Custom context manager
from contextlib import contextmanager
from typing import Generator

@contextmanager
def temporary_state() -> Generator[None, None, None]:
    try:
        # Setup
        print("Entering context")
        yield
    finally:
        # Cleanup
        print("Exiting context")
```

## ⭐ Control Flow Best Practices

### 1. 🤷 EAFP (Easier to Ask for Forgiveness than Permission)

Python prefers EAFP over LBYL (Look Before You Leap):

```python
# EAFP (Pythonic)
def get_value(data: dict, key: str) -> Any:
    try:
        return data[key]
    except KeyError:
        return None

# LBYL (Less Pythonic)
def get_value_lbyl(data: dict, key: str) -> Any:
    if key in data:
        return data[key]
    return None
```

### 2. 🔧 Using Context Managers

Always use context managers for resource management:

```python
# Good
with open('file.txt') as f:
    data = f.read()

# Bad
f = open('file.txt')
try:
    data = f.read()
finally:
    f.close()
```

### 3. 📋 Exception Handling Guidelines

```python
# Handle specific exceptions
try:
    value = int(input("Enter a number: "))
except ValueError:
    print("Not a valid number")

# Avoid bare except
try:
    risky_operation()
except Exception as e:  # Too broad!
    print(f"Error: {e}")

# Better
try:
    risky_operation()
except (ValueError, TypeError) as e:
    print(f"Invalid input: {e}")
except IOError as e:
    print(f"IO error: {e}")
```

## 🚀 Advanced Control Flow Features

### 1. ⚡ Generator Expressions

Memory-efficient iteration:

```python
# Generator expression
squares = (x * x for x in range(1000000))
# Values generated on demand

# List comprehension (creates full list in memory)
squares_list = [x * x for x in range(1000000)]
```

### 2. ⏱️ Async/Await

Modern asynchronous control flow:

```python
import asyncio
from typing import List

async def fetch_data(url: str) -> str:
    # Simulated async operation
    await asyncio.sleep(1)
    return f"Data from {url}"

async def main() -> None:
    urls = ["url1", "url2", "url3"]
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    print(results)

# Run async code
asyncio.run(main())
```

### 3. 🎯 Pattern Matching with Guards

Complex pattern matching scenarios:

```python
def analyze_point(point: tuple) -> str:
    match point:
        case (x, y) if x == y == 0:
            return "Origin"
        case (x, y) if x == 0:
            return "On Y axis"
        case (x, y) if y == 0:
            return "On X axis"
        case (x, y) if x > 0 and y > 0:
            return "First quadrant"
        case _:
            return "Other position"
```

## ⚠️ Common Gotchas

### 1. 🔍 Variable Scope in Loops

```python
# List comprehension scope
[x for x in range(5)]  # x is not accessible outside
print(x)  # NameError

# For loop scope
for x in range(5): pass
print(x)  # Prints 4 (x persists)
```

### 2. 🚫 Exception Handling Anti-patterns

```python
# Don't do this
try:
    do_something()
except:  # Bare except clause
    pass  # Silently swallowing errors

# Better
try:
    do_something()
except Exception as e:
    logger.error(f"Error in do_something: {e}")
    raise  # Re-raise the exception
```

### 3. 🎮 Loop Control Flow

```python
# Break vs Return
def find_item(items: List[str], target: str) -> Optional[int]:
    for i, item in enumerate(items):
        if item == target:
            return i  # Better than break for functions
    return None

# Continue vs Nested If
for item in items:
    if not item.is_valid():
        continue  # Better than nested if
    process_item(item)
```

## 🧪 Testing Examples

```python
import pytest
from typing import Any

def test_pattern_matching() -> None:
    def process_value(value: Any) -> str:
        match value:
            case int() as n if n > 0:
                return "positive"
            case str() as s:
                return "string"
            case _:
                return "other"
    
    assert process_value(42) == "positive"
    assert process_value("hello") == "string"
    assert process_value(None) == "other"

def test_exception_handling() -> None:
    with pytest.raises(ValueError):
        raise ValueError("test error")
```

## 📚 Additional Resources

1. **📖 Official Documentation**
   - [Python Control Flow](https://docs.python.org/3/tutorial/controlflow.html)
   - [Pattern Matching Tutorial](https://docs.python.org/3/tutorial/controlflow.html#match-statements)
   - [Context Managers](https://docs.python.org/3/reference/datamodel.html#context-managers)

2. **📝 PEPs (Python Enhancement Proposals)**
   - [PEP 634 – Structural Pattern Matching](https://www.python.org/dev/peps/pep-0634/)
   - [PEP 343 – The "with" Statement](https://www.python.org/dev/peps/pep-0343/)

3. **🌐 External Resources**
   - [Real Python - Python Control Flow](https://realpython.com/python-control-flow/)
   - [Python Exception Handling Best Practices](https://realpython.com/python-exceptions/) 