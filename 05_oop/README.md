# 🏗️ Object-Oriented Programming in Python

## 📖 Introduction

This section explores Python's object-oriented programming (OOP) features, comparing them with Java and Go. Python's OOP model is more flexible than Java's and offers features not found in Go, while maintaining simplicity and readability.

## Examples

This section includes two comprehensive examples demonstrating Python's OOP features:

1. [Library Management System](examples/library_system.py)
   - Demonstrates abstract base classes, data classes, descriptors, and the Observer pattern
   - Shows how to implement a real-world system using OOP principles
   - Includes comprehensive tests in [test_library_system.py](examples/test_library_system.py)

2. [Geometric Shapes](examples/shapes.py)
   - Demonstrates inheritance, composition, protocols, and mixins
   - Shows how to implement a flexible shape hierarchy
   - Includes comprehensive tests in [test_shapes.py](examples/test_shapes.py)

Both examples are thoroughly documented and tested, making them excellent learning resources for developers coming from Java or Go backgrounds.

## Class Basics

### Class Definition and Instantiation

```python
from typing import List, Optional
from dataclasses import dataclass

# Basic class definition
class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
    
    def greet(self) -> str:
        return f"Hello, I'm {self.name}!"

# Using dataclass (Python 3.7+)
@dataclass
class Point:
    x: float
    y: float
    label: Optional[str] = None

# Instantiation
person = Person("Alice", 30)
point = Point(1.0, 2.0, "Origin")
```

### Class and Instance Variables

```python
class Counter:
    # Class variable (shared by all instances)
    count: int = 0
    
    def __init__(self, name: str) -> None:
        # Instance variables (unique to each instance)
        self.name = name
        self.value = 0
        Counter.count += 1
    
    @classmethod
    def get_total_counters(cls) -> int:
        return cls.count
```

## Inheritance and Polymorphism

### Single Inheritance

```python
from abc import ABC, abstractmethod
from typing import List

class Shape(ABC):
    def __init__(self, color: str) -> None:
        self.color = color
    
    @abstractmethod
    def area(self) -> float:
        """Calculate shape area."""
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        """Calculate shape perimeter."""
        pass

class Circle(Shape):
    def __init__(self, radius: float, color: str) -> None:
        super().__init__(color)
        self.radius = radius
    
    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2
    
    def perimeter(self) -> float:
        import math
        return 2 * math.pi * self.radius
```

### Multiple Inheritance

```python
class Printable:
    def print_info(self) -> None:
        print(f"Object: {self.__class__.__name__}")

class Serializable:
    def to_dict(self) -> dict:
        return self.__dict__

class Document(Printable, Serializable):
    def __init__(self, title: str, content: str) -> None:
        self.title = title
        self.content = content
```

### Method Resolution Order (MRO)

```python
class A:
    def method(self) -> str:
        return "A"

class B(A):
    def method(self) -> str:
        return f"B -> {super().method()}"

class C(A):
    def method(self) -> str:
        return f"C -> {super().method()}"

class D(B, C):
    def method(self) -> str:
        return f"D -> {super().method()}"

# View MRO
print(D.mro())  # [D, B, C, A, object]
```

## Special Methods (Magic Methods)

### Object Representation

```python
class Book:
    def __init__(self, title: str, author: str) -> None:
        self.title = title
        self.author = author
    
    def __str__(self) -> str:
        """Informal string representation."""
        return f"{self.title} by {self.author}"
    
    def __repr__(self) -> str:
        """Official string representation."""
        return f"Book(title='{self.title}', author='{self.author}')"
```

### Container Methods

```python
class Library:
    def __init__(self) -> None:
        self.books: List[Book] = []
    
    def __len__(self) -> int:
        return len(self.books)
    
    def __getitem__(self, index: int) -> Book:
        return self.books[index]
    
    def __iter__(self) -> Iterator[Book]:
        return iter(self.books)
    
    def __contains__(self, book: Book) -> bool:
        return book in self.books
```

## Properties and Descriptors

### Properties

```python
class Temperature:
    def __init__(self, celsius: float) -> None:
        self._celsius = celsius
    
    @property
    def celsius(self) -> float:
        """Get temperature in Celsius."""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value
    
    @property
    def fahrenheit(self) -> float:
        """Get temperature in Fahrenheit."""
        return (self.celsius * 9/5) + 32
```

### Descriptors

```python
class ValidString:
    """Descriptor for string validation."""
    def __init__(self, minlen: int = 0, maxlen: Optional[int] = None) -> None:
        self.minlen = minlen
        self.maxlen = maxlen
    
    def __get__(
        self,
        instance: Any,
        owner: Optional[type] = None
    ) -> Optional[str]:
        if instance is None:
            return None
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance: Any, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Value must be a string")
        if len(value) < self.minlen:
            raise ValueError(f"String too short (min {self.minlen})")
        if self.maxlen and len(value) > self.maxlen:
            raise ValueError(f"String too long (max {self.maxlen})")
        instance.__dict__[self.name] = value
    
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

class User:
    username = ValidString(minlen=3, maxlen=20)
    email = ValidString(minlen=5, maxlen=50)
```

## Class Decorators and Metaclasses

### Class Decorators

```python
from functools import wraps
from typing import Type, TypeVar, Callable

T = TypeVar('T')

def singleton(cls: Type[T]) -> Type[T]:
    """Decorator to create singleton classes."""
    instances = {}
    
    @wraps(cls)
    def get_instance(*args: Any, **kwargs: Any) -> T:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton
class Configuration:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
```

### Metaclasses

```python
class ValidationMeta(type):
    """Metaclass for adding validation to class attributes."""
    def __new__(
        mcs,
        name: str,
        bases: tuple,
        namespace: dict
    ) -> Type:
        # Validate class attributes
        for key, value in namespace.items():
            if key.startswith('__'):
                continue
            if isinstance(value, str):
                namespace[key] = value.strip()
        return super().__new__(mcs, name, bases, namespace)

class Model(metaclass=ValidationMeta):
    name = "  Example  "  # Will be stripped
    description = " Test "  # Will be stripped
```

## Advanced OOP Patterns

### Factory Pattern

```python
from abc import ABC, abstractmethod
from typing import Dict, Type

class Animal(ABC):
    @abstractmethod
    def speak(self) -> str:
        pass

class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"

class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"

class AnimalFactory:
    _animals: Dict[str, Type[Animal]] = {
        "dog": Dog,
        "cat": Cat
    }
    
    @classmethod
    def create(cls, animal_type: str) -> Animal:
        if animal_type not in cls._animals:
            raise ValueError(f"Unknown animal type: {animal_type}")
        return cls._animals[animal_type]()
```

### Observer Pattern

```python
from typing import Set, Protocol

class Observer(Protocol):
    def update(self, message: str) -> None:
        pass

class Subject:
    def __init__(self) -> None:
        self._observers: Set[Observer] = set()
        self._state: str = ""
    
    def attach(self, observer: Observer) -> None:
        self._observers.add(observer)
    
    def detach(self, observer: Observer) -> None:
        self._observers.discard(observer)
    
    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self._state)
    
    @property
    def state(self) -> str:
        return self._state
    
    @state.setter
    def state(self, value: str) -> None:
        self._state = value
        self.notify()
```

## Best Practices

### 1. SOLID Principles

```python
# Single Responsibility Principle
class UserManager:
    def __init__(self, db: Database) -> None:
        self.db = db
    
    def create_user(self, user: User) -> None:
        """Only handles user creation."""
        self.db.save(user)

# Open/Closed Principle
class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount: float) -> None:
        pass

class CreditCardProcessor(PaymentProcessor):
    def process(self, amount: float) -> None:
        # Process credit card payment
        pass
```

### 2. Composition Over Inheritance

```python
# Prefer composition
class Engine:
    def start(self) -> None:
        pass

class Car:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine  # Composition
    
    def start(self) -> None:
        self.engine.start()

# Instead of inheritance
class ElectricCar(Car):  # Might be too rigid
    pass
```

### 3. Type Hints and Protocols

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> None: ...

@runtime_checkable
class Movable(Protocol):
    def move(self, x: float, y: float) -> None: ...

class GameObject:
    def process(self, item: Drawable & Movable) -> None:
        item.draw()
        item.move(1.0, 2.0)
```

## Testing OOP Code

### Unit Testing Classes

```python
import pytest
from typing import Generator

class TestPerson:
    @pytest.fixture
    def person(self) -> Generator[Person, None, None]:
        p = Person("Test", 25)
        yield p
    
    def test_person_creation(self, person: Person) -> None:
        assert person.name == "Test"
        assert person.age == 25
    
    def test_person_greeting(self, person: Person) -> None:
        assert person.greet() == "Hello, I'm Test!"
```

### Mock Objects

```python
from unittest.mock import Mock, patch

def test_user_manager() -> None:
    mock_db = Mock()
    manager = UserManager(mock_db)
    user = User("test", "test@example.com")
    
    manager.create_user(user)
    mock_db.save.assert_called_once_with(user)

@patch('module.Database')
def test_with_patch(mock_db: Mock) -> None:
    manager = UserManager(mock_db)
    # Test with mocked database
```

## Common Pitfalls

### 1. Mutable Class Variables

```python
# Wrong
class Student:
    grades: List[int] = []  # Shared by all instances!
    
    def add_grade(self, grade: int) -> None:
        self.grades.append(grade)

# Right
class Student:
    def __init__(self) -> None:
        self.grades: List[int] = []  # Instance variable
```

### 2. Diamond Problem

```python
# Potential problem
class A:
    def method(self) -> str:
        return "A"

class B(A):
    def method(self) -> str:
        return "B"

class C(A):
    def method(self) -> str:
        return "C"

class D(B, C):  # Which method() will it inherit?
    pass

# Solution: Use super() and understand MRO
class D(B, C):
    def method(self) -> str:
        return f"D -> {super().method()}"
```

### 3. Circular Dependencies

```python
# Wrong
class A:
    def __init__(self) -> None:
        self.b = B()  # Circular dependency

class B:
    def __init__(self) -> None:
        self.a = A()  # Circular dependency

# Better
class A:
    def __init__(self) -> None:
        self.b: Optional[B] = None
    
    def set_b(self, b: 'B') -> None:
        self.b = b
```

## Additional Resources

1. **Official Documentation**
   - [Python Classes](https://docs.python.org/3/tutorial/classes.html)
   - [Data Classes](https://docs.python.org/3/library/dataclasses.html)
   - [Abstract Base Classes](https://docs.python.org/3/library/abc.html)

2. **PEPs**
   - [PEP 557 – Data Classes](https://www.python.org/dev/peps/pep-0557/)
   - [PEP 3119 – Abstract Base Classes](https://www.python.org/dev/peps/pep-3119/)
   - [PEP 3115 – Metaclasses](https://www.python.org/dev/peps/pep-3115/)

3. **Design Patterns**
   - [Python Patterns Guide](https://python-patterns.guide/)
   - [Real Python - OOP](https://realpython.com/python3-object-oriented-programming/)
   - [Python Design Patterns](https://refactoring.guru/design-patterns/python) 