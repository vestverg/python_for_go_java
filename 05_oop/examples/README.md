# Library Management System Example

This example demonstrates a comprehensive implementation of Object-Oriented Programming concepts in Python through a library management system. The example showcases various OOP features and best practices, making it particularly useful for developers coming from Java or Go backgrounds.

## Features Demonstrated

1. **Abstract Base Classes**
   - `LibraryItem` as an abstract base class
   - Abstract methods with `@abstractmethod` decorator
   - Type hints and return types

2. **Multiple Inheritance and Protocols**
   - `Observable` and `Observer` for event handling
   - `Searchable` and `Reservable` protocols
   - Method Resolution Order (MRO)

3. **Properties and Descriptors**
   - `EmailValidator` descriptor for email validation
   - Property decorators for controlled attribute access
   - Type-safe attribute management

4. **Data Classes**
   - `Book` and `DVD` as data classes
   - Field customization with `field()`
   - Default values and factory functions

5. **Special Methods**
   - `__str__` for string representation
   - `__init__` for initialization
   - `__get__`, `__set__`, and `__set_name__` for descriptors

6. **Design Patterns**
   - Observer Pattern for event logging
   - Factory Pattern for item creation
   - Composition over inheritance

7. **Type Hints and Protocols**
   - Static typing with `typing` module
   - Runtime protocol checking
   - Generic types and type variables

8. **Testing**
   - Pytest fixtures and parametrization
   - Mock objects and patching
   - Test organization and best practices

## Code Structure

```
examples/
├── library_system.py     # Main implementation
├── test_library_system.py # Test suite
└── README.md            # This file
```

## Key Classes

### LibraryItem (Abstract Base Class)
```python
class LibraryItem(ABC):
    @abstractmethod
    def get_loan_period(self) -> timedelta:
        """Return the loan period for this item."""
        pass
```

### Book and DVD (Data Classes)
```python
@dataclass
class Book(LibraryItem):
    author: str
    isbn: str
    pages: int
    publisher: str
    year: int

@dataclass
class DVD(LibraryItem):
    director: str
    runtime: int
    rating: str
```

### Library (Observer Pattern)
```python
class Library(Observable):
    def add_item(self, item: LibraryItem) -> None:
        self.items[item.item_id] = item
        self.notify(f"New item added: {item}")
```

### EmailValidator (Descriptor)
```python
class EmailValidator:
    def __set__(self, instance: object, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email format")
        setattr(instance, f"_{self.name}", value.lower())
```

## Running the Example

1. Run the main program:
   ```bash
   python library_system.py
   ```

2. Run the tests:
   ```bash
   pytest test_library_system.py -v
   ```

## Key Differences from Java/Go

### Java Differences
1. **Multiple Inheritance**
   - Python: Supports multiple inheritance and MRO
   - Java: Single inheritance with interfaces

2. **Properties**
   - Python: Built-in property decorators
   - Java: Getter/setter methods

3. **Data Classes**
   - Python: `@dataclass` decorator
   - Java: Lombok or record classes (Java 14+)

### Go Differences
1. **Inheritance**
   - Python: Class-based inheritance
   - Go: Interface composition

2. **Access Control**
   - Python: Convention-based (_protected, __private)
   - Go: Exported/unexported based on capitalization

3. **Generics**
   - Python: Type hints with `typing` module
   - Go: Built-in generics (Go 1.18+)

## Best Practices Demonstrated

1. **SOLID Principles**
   - Single Responsibility: Each class has one purpose
   - Open/Closed: Easy to extend through inheritance
   - Liskov Substitution: Proper use of abstract classes
   - Interface Segregation: Small, focused protocols
   - Dependency Inversion: High-level modules depend on abstractions

2. **Clean Code**
   - Descriptive naming
   - Comprehensive documentation
   - Type hints for better IDE support
   - Proper error handling

3. **Testing**
   - Unit tests for each class
   - Fixtures for common setup
   - Edge case testing
   - Mocking external dependencies

## Learning Objectives

After studying this example, you should understand:

1. How to design class hierarchies in Python
2. When to use abstract classes vs protocols
3. How to implement and use descriptors
4. How to leverage data classes
5. How to apply design patterns in Python
6. How to write comprehensive tests
7. How to use type hints effectively

## Additional Resources

1. [Python Data Classes](https://docs.python.org/3/library/dataclasses.html)
2. [Abstract Base Classes](https://docs.python.org/3/library/abc.html)
3. [Type Hints](https://docs.python.org/3/library/typing.html)
4. [Property Decorators](https://docs.python.org/3/library/functions.html#property)
5. [Pytest Documentation](https://docs.pytest.org/) 