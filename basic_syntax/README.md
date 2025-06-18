# Basic Python Syntax and Data Types

This section covers Python's basic syntax and data types, with comparisons to Java and Go.

## Dynamic vs Static Typing

Python uses dynamic typing, unlike Java and Go's static typing:

```python
# Python - types are determined at runtime
x = 42        # int
x = "hello"   # can change to str
x = [1, 2, 3] # can change to list
```

```go
// Go - types must be declared
var x int = 42
x = "hello"   // Compilation error!
```

```java
// Java - types must be declared
int x = 42;
x = "hello";  // Compilation error!
```

## Basic Data Types

### Numbers

```python
# Python
integer = 42
float_num = 3.14
complex_num = 1 + 2j  # Complex numbers built-in!
```

### Strings

```python
# Python - multiple string syntaxes
single = 'Single quotes'
double = "Double quotes"
multi = """
Multi-line
string
"""
formatted = f"Value is {integer}"
```

### Lists (Similar to Java ArrayList / Go Slice)

```python
# Python
numbers = [1, 2, 3]
numbers.append(4)
first = numbers[0]
last_two = numbers[-2:]  # Slicing!
```

### Tuples (Immutable Lists)

```python
# Python - no direct equivalent in Java/Go
point = (x, y)
x, y = point  # Tuple unpacking
```

### Dictionaries (Similar to Java HashMap / Go map)

```python
# Python
person = {
    "name": "Alice",
    "age": 30
}
name = person["name"]
age = person.get("age", 0)  # With default value
```

### Sets

```python
# Python
unique_numbers = {1, 2, 3}
unique_numbers.add(2)  # No effect - already exists
```

## Type Hints (for Java/Go developers)

Python 3.5+ supports optional type hints:

```python
from typing import List, Dict, Optional

def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}

def maybe_get_name(user_id: int) -> Optional[str]:
    # Optional is like Java's Optional or Go's pointer
    return None if user_id < 0 else f"User{user_id}"
```

## Common Operations

### List/Array Operations

```python
# Python
numbers = [1, 2, 3, 4, 5]
doubled = [x * 2 for x in numbers]  # List comprehension
filtered = [x for x in numbers if x > 2]
```

### String Operations

```python
# Python
text = "Hello, World!"
upper = text.upper()
words = text.split(",")
joined = ", ".join(["Hello", "World"])
```

### Dictionary Operations

```python
# Python
person = {"name": "Bob", "age": 25}
keys = person.keys()
values = person.values()
items = person.items()  # Key-value pairs

# Dict comprehension
squares = {x: x*x for x in range(5)}
```

## Next Steps

1. Try the examples in Python's REPL
2. Experiment with type hints
3. Practice list and dictionary comprehensions
4. Move on to the Control Flow section 