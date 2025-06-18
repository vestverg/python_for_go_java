# Python Basic Syntax and Data Types

## Introduction

This section provides a comprehensive overview of Python's basic syntax and data types, with detailed comparisons to Java and Go. We'll explore how Python's dynamic typing system differs from the static typing systems you're familiar with, while showing how type hints bridge this gap.

## Python's Type System

### Dynamic Typing with Type Hints

Python combines dynamic typing with optional static type hints, offering flexibility while maintaining code clarity:

```python
# Dynamic typing (traditional Python)
x = 42              # Type inferred at runtime
x = "Hello"         # Type can change dynamically

# Static type hints (modern Python)
x: int = 42         # Type hint for better tooling
y: str = "Hello"    # Clear intention, but not enforced
```

### Type Hints vs Java/Go Types

Detailed comparison of type annotations across languages:

| Category | Python | Java | Go | Notes |
|----------|--------|------|-----|-------|
| Integer | `int` | `int`, `long` | `int`, `int64` | Python's int is unlimited |
| Float | `float` | `double` | `float64` | Python float is double precision |
| String | `str` | `String` | `string` | Python strings are immutable |
| Boolean | `bool` | `boolean` | `bool` | Python uses `True`/`False` |
| Array | `List[T]` | `List<T>` | `[]T` | Python lists are dynamic |
| Map | `Dict[K, V]` | `Map<K,V>` | `map[K]V` | Python dicts are hashable |
| Optional | `Optional[T]` | `Optional<T>` | `*T` | Python uses `None` |
| Any | `Any` | `Object` | `interface{}` | Python's dynamic typing |
| Union | `Union[T1, T2]` | N/A | `interface{}` | Multiple possible types |
| Generic | `TypeVar('T')` | `<T>` | N/A | Type parameters |

## Data Structures Deep Dive

### Numbers

Python's numeric types offer more flexibility than Java or Go:

```python
# Integers (unlimited size)
x: int = 1000000000000000000000000  # No long needed
y: int = 0xFF  # Hexadecimal
z: int = 0o777  # Octal
b: int = 0b1010  # Binary

# Float (double precision)
pi: float = 3.14159
scientific: float = 1.23e-4

# Complex numbers (not in Java/Go)
c: complex = 1 + 2j
```

### Strings

Python's string handling is more feature-rich than Java or Go:

```python
# String creation
single: str = 'Single quotes'
double: str = "Double quotes"
multi: str = """
Multiple
lines
"""

# String operations
name = "Python"
print(f"Hello, {name}!")  # f-strings (like Go's fmt.Sprintf)
print("Hello, %s!" % name)  # Old style (like C's printf)
print("Hello, {}!".format(name))  # str.format method

# String methods
print(name.upper())  # PYTHON
print(name.lower())  # python
print(name.replace('P', 'J'))  # Jython
```

### Collections

#### Lists (Dynamic Arrays)

```python
# List creation and type hints
from typing import List

numbers: List[int] = [1, 2, 3]
mixed: List[Any] = [1, "two", 3.0]

# List operations
numbers.append(4)        # Add element
numbers.extend([5, 6])   # Add multiple elements
numbers.pop()           # Remove and return last element
numbers.insert(0, 0)    # Insert at index
```

#### Dictionaries (Hash Maps)

```python
from typing import Dict, Any

# Dictionary creation
person: Dict[str, Any] = {
    "name": "Alice",
    "age": 30,
    "skills": ["Python", "Java"]
}

# Dictionary operations
person["location"] = "NYC"  # Add/update
del person["age"]          # Delete
skills = person.get("skills", [])  # Safe get with default
```

#### Sets (Unique Collections)

```python
from typing import Set

# Set creation
unique_numbers: Set[int] = {1, 2, 3, 2}  # {1, 2, 3}

# Set operations
unique_numbers.add(4)     # Add element
unique_numbers.remove(1)  # Remove element
```

### Type Checking and Validation

#### Using mypy

```bash
# Install mypy
pip install mypy

# Run type checking
mypy your_file.py

# Common flags
mypy --strict your_file.py  # Strict mode
mypy --ignore-missing-imports your_file.py  # Ignore missing stubs
```

#### Runtime Type Checking

```python
from typing import runtime_checkable, Protocol

@runtime_checkable
class Printable(Protocol):
    def print(self) -> None: ...

def process_printable(item: Printable) -> None:
    if isinstance(item, Printable):
        item.print()
```

## Object-Oriented Features

### Classes and Objects

```python
from dataclasses import dataclass
from typing import List

@dataclass
class Person:
    name: str
    age: int
    skills: List[str] = field(default_factory=list)

    def greet(self) -> str:
        return f"Hello, {self.name}!"
```

### Inheritance and Interfaces

```python
from abc import ABC, abstractmethod
from typing import Protocol

# Abstract base class (like Java abstract class)
class Animal(ABC):
    @abstractmethod
    def speak(self) -> str:
        pass

# Protocol (like Go interface)
class Speakable(Protocol):
    def speak(self) -> str: ...

# Implementation
class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"
```

## Error Handling

### Exception Handling

Python's exception handling compared to Java and Go:

```python
# Python
try:
    result = dangerous_operation()
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"Other error: {e}")
else:
    print("Success!")
finally:
    cleanup()

# Java equivalent
try {
    result = dangerousOperation();
} catch (ValueError e) {
    System.out.println("Value error: " + e);
} catch (Exception e) {
    System.out.println("Other error: " + e);
} finally {
    cleanup();
}

# Go equivalent
if result, err := dangerousOperation(); err != nil {
    if errors.Is(err, ValueError) {
        fmt.Printf("Value error: %v\n", err)
    } else {
        fmt.Printf("Other error: %v\n", err)
    }
} else {
    fmt.Println("Success!")
}
defer cleanup()
```

## Best Practices

### Type Hints Usage

1. **Always Type Function Signatures**
   ```python
   def process_data(items: List[str], count: int = 0) -> Dict[str, Any]:
       pass
   ```

2. **Use Type Aliases for Complex Types**
   ```python
   from typing import TypeAlias
   
   JsonDict: TypeAlias = Dict[str, Any]
   UserID: TypeAlias = int
   ```

3. **Document Nullable Types**
   ```python
   from typing import Optional
   
   def find_user(user_id: int) -> Optional[User]:
       pass
   ```

### Code Style

1. **Follow PEP 8**
   - Use 4 spaces for indentation
   - Maximum line length of 79 characters
   - Two blank lines before top-level classes/functions

2. **Naming Conventions**
   ```python
   # Variables and functions (snake_case)
   user_name = "Alice"
   def calculate_total(): pass
   
   # Classes (PascalCase)
   class UserAccount: pass
   
   # Constants (UPPER_CASE)
   MAX_CONNECTIONS = 100
   ```

3. **Documentation**
   ```python
   def process_user(user_id: int) -> Dict[str, Any]:
       """
       Process user information.
       
       Args:
           user_id: The unique identifier of the user
           
       Returns:
           Dictionary containing processed user data
           
       Raises:
           ValueError: If user_id is negative
       """
       pass
   ```

## Common Pitfalls for Java/Go Developers

1. **Mutable Default Arguments**
   ```python
   # Wrong
   def add_item(item, items=[]):  # items is shared between calls
       items.append(item)
       return items
   
   # Right
   def add_item(item, items=None):
       if items is None:
           items = []
       items.append(item)
       return items
   ```

2. **Reference vs Value Semantics**
   ```python
   # Lists are mutable
   list1 = [1, 2, 3]
   list2 = list1  # Reference, not copy
   list2.append(4)  # Affects both lists
   
   # Use copy for independent lists
   list2 = list1.copy()  # Shallow copy
   list2 = copy.deepcopy(list1)  # Deep copy
   ```

3. **Truth Value Testing**
   ```python
   # Python's truthy/falsy values
   if value:  # Works for many types
       pass
   
   # Explicit comparisons
   if value is None:  # Instead of value == None
       pass
   
   if value == "":  # Instead of len(value) == 0
       pass
   ```

## Testing Your Knowledge

1. **Basic Types Exercise**
   ```python
   # Implement a function that demonstrates type conversion
   def convert_types(value: Any) -> Tuple[int, float, str]:
       pass
   ```

2. **Collections Exercise**
   ```python
   # Implement a function that processes different collection types
   def process_collections(
       items: List[int],
       mapping: Dict[str, int],
       unique: Set[int]
   ) -> Dict[str, Any]:
       pass
   ```

3. **Error Handling Exercise**
   ```python
   # Implement a function that demonstrates proper error handling
   def safe_operation(value: str) -> Optional[int]:
       pass
   ```

## Additional Resources

1. **Official Documentation**
   - [Python Data Model](https://docs.python.org/3/reference/datamodel.html)
   - [Built-in Types](https://docs.python.org/3/library/stdtypes.html)
   - [Type Hints](https://docs.python.org/3/library/typing.html)

2. **Style Guides**
   - [PEP 8](https://www.python.org/dev/peps/pep-0008/)
   - [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

3. **Type Checking**
   - [mypy Documentation](http://mypy-lang.org/)
   - [Python Type Checking Guide](https://realpython.com/python-type-checking/) 