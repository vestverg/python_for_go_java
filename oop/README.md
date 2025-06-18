# Object-Oriented Programming in Python

This section covers Python's OOP features, with comparisons to Java and Go.

## Class Definition

### Basic Class

```python
# Python
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def greet(self) -> str:
        return f"Hello, I'm {self.name}"
```

```java
// Java
public class Person {
    private String name;
    private int age;
    
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    public String greet() {
        return "Hello, I'm " + name;
    }
}
```

### Data Classes (Python 3.7+)

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
    
    def distance_from_origin(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5
```

## Inheritance

### Single Inheritance

```python
# Python
class Animal:
    def __init__(self, name: str):
        self.name = name
    
    def speak(self) -> str:
        raise NotImplementedError

class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name} says Woof!"

class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name} says Meow!"
```

### Multiple Inheritance

```python
# Python - multiple inheritance (not available in Java/Go)
class Flyable:
    def fly(self) -> str:
        return "Flying..."

class Swimmable:
    def swim(self) -> str:
        return "Swimming..."

class Duck(Animal, Flyable, Swimmable):
    def speak(self) -> str:
        return f"{self.name} says Quack!"
```

## Properties and Descriptors

### Properties

```python
class BankAccount:
    def __init__(self, initial_balance: float = 0):
        self._balance = initial_balance
    
    @property
    def balance(self) -> float:
        return self._balance
    
    @balance.setter
    def balance(self, value: float) -> None:
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value
```

### Descriptors

```python
class ValidString:
    def __init__(self, minlen: int = 1):
        self.minlen = minlen
    
    def __get__(self, obj, objtype=None):
        return obj._name
    
    def __set__(self, obj, value: str):
        if len(value) < self.minlen:
            raise ValueError(f"String must be at least {self.minlen} characters")
        obj._name = value

class User:
    name = ValidString(minlen=2)
    
    def __init__(self, name: str):
        self.name = name
```

## Special Methods

### Common Special Methods

```python
class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return f"Vector({self.x}, {self.y})"
    
    def __repr__(self) -> str:
        return f"Vector(x={self.x}, y={self.y})"
    
    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y
    
    def __len__(self) -> int:
        return int((self.x ** 2 + self.y ** 2) ** 0.5)
```

## Abstract Classes

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        pass

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)
```

## Class and Static Methods

```python
class DateUtil:
    @staticmethod
    def is_valid_date(year: int, month: int, day: int) -> bool:
        # Static method - doesn't need class or instance
        try:
            import datetime
            datetime.datetime(year, month, day)
            return True
        except ValueError:
            return False
    
    @classmethod
    def from_string(cls, date_str: str) -> 'DateUtil':
        # Class method - receives class as first argument
        year, month, day = map(int, date_str.split('-'))
        return cls(year, month, day)
```

## Context Managers

```python
class DatabaseConnection:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.conn = None
    
    def __enter__(self):
        # Set up connection
        print(f"Connecting to {self.host}:{self.port}")
        self.conn = True  # Simulate connection
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Clean up connection
        print("Closing connection")
        self.conn = None
```

## Next Steps

1. Implement a class hierarchy
2. Practice using properties and descriptors
3. Create custom context managers
4. Move on to the Modules section 