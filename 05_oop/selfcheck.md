# 🏗️ Object-Oriented Programming - Knowledge Check

> **Build with Python OOP!** 🎯  
> Master classes, inheritance, and Python's unique OOP features vs Java/Go.

---

## 📊 **Progress Tracker**
**Section:** OOP | **Questions:** 6 | **Difficulty:** Advanced | **Time:** ~7 min

---

### 🎯 **Question 1 of 6**
**What's the correct class definition syntax?**

```python
# Class definition comparison:
# Java: public class MyClass { }
# Go: type MyStruct struct { }
# Python: ???
```

**A.** `class MyClass {}`  
**B.** `class MyClass:`  
**C.** `def class MyClass:`  

---

### 🎯 **Question 2 of 6**
**Which method initializes a new object?**

```python
class Person:
    def ???(self, name):
        self.name = name
    
    def greet(self):
        return f"Hello, I'm {self.name}"

person = Person("Alice")  # Which method gets called?
```

**A.** `__init__`  
**B.** `__new__`  
**C.** `__create__`  

---

### 🎯 **Question 3 of 6**
**How do you create a property in Python?**

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    ??? # How to make 'area' a computed property?
    def area(self):
        return 3.14159 * self._radius ** 2
```

**A.** `@property`  
**B.** `@computed`  
**C.** `@getter`  

---

### 🎯 **Question 4 of 6**
**What makes Python's inheritance special?**

```python
class A: pass
class B: pass
class C(A, B):  # Multiple inheritance!
    pass

# Java: class C extends A implements B
# Go: No inheritance, use composition
# Python: ???
```

**A.** Single inheritance only  
**B.** Multiple inheritance support  
**C.** No inheritance at all  

---

### 🎯 **Question 5 of 6**
**What does `super()` do?**

```python
class Animal:
    def speak(self):
        return "Some sound"

class Dog(Animal):
    def speak(self):
        base = super().speak()  # What does this do?
        return f"{base} - Woof!"
```

**A.** Calls the parent class method  
**B.** Creates a new class instance  
**C.** Deletes the current object  

---

### 🎯 **Question 6 of 6**
**What's the difference between `__str__` and `__repr__`?**

```python
class Book:
    def __str__(self):
        return "A book for humans to read"
    
    def __repr__(self):
        return "Book(title='Python Guide')"

book = Book()
print(book)        # Uses __str__
print(repr(book))  # Uses __repr__
```

**A.** They're exactly the same  
**B.** `__str__` for humans, `__repr__` for developers  
**C.** `__str__` is deprecated

---

## 🎉 **OOP Architecture Master!**

### 🏗️ **Python OOP Superpowers:**
- **Multiple inheritance** with Method Resolution Order (MRO)
- **Properties** replace getter/setter boilerplate  
- **Magic methods** (`__str__`, `__eq__`, etc.) for operator overloading
- **Abstract Base Classes** for interface-like behavior

### 🔄 **Language Comparison:**
| Feature | Java | Go | Python |
|---------|------|----|---------| 
| **Multiple inheritance** | ❌ (interfaces only) | ❌ | ✅ |
| **Properties** | Getters/Setters | Struct fields | `@property` |
| **Abstract classes** | `abstract` keyword | Interfaces | `ABC` module |
| **Operator overloading** | Limited | ❌ | ✅ (magic methods) |

### 📈 **Next Steps:**
- ✅ **OOP expert?** → Master [Modules & Packages](../06_modules_and_packages/)
- 🔍 **See examples?** → Check [library_system.py](./examples/library_system.py)
- 🎨 **Advanced OOP?** → Try abstract classes and protocols

### 🔍 **Answer Key:**
*Test your Python OOP mastery!*

<details>
<summary>🔓 Show Answers</summary>

1. **B** - `class MyClass:` defines classes in Python
2. **A** - `__init__` is the constructor method (initializer)
3. **A** - `@property` decorator creates computed properties
4. **B** - Python supports multiple inheritance (unlike Java/Go)
5. **A** - `super()` calls methods from parent classes
6. **B** - `__str__` for user display, `__repr__` for debugging

**🔥 Advanced concepts:**
- **MRO:** Method Resolution Order determines inheritance chain
- **Descriptors:** Power behind properties and methods
- **Metaclasses:** Classes that create classes (advanced!)

</details>

---

*🏗️ **Build with purpose:** Great OOP design creates maintainable code!* ✨🐍 

## 🌟 Expert Challenge

**Question**: Create a metaclass-based framework that combines Go's interfaces with Java's abstract classes. Your solution should:

1. Implement a metaclass that:
   - Enforces interface contracts (like Go)
   - Supports multiple inheritance (unlike Java)
   - Provides abstract method enforcement (like Java)
   - Handles method resolution order (MRO) conflicts

2. Use this framework to create a real-world example of a plugin system where:
   - Plugins must implement specific interfaces
   - Some functionality is provided in abstract base classes
   - Multiple inheritance is used safely
   - Type hints and runtime checks are enforced

**Hint**: Look into `type`, `abc.ABCMeta`, `__subclasshook__`, and method resolution order (MRO).

<details>
<summary>Show Answer</summary>

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Type, TypeVar, cast
import inspect

T = TypeVar('T')

class InterfaceEnforcer(type):
    """Metaclass that enforces interface contracts like Go"""
    
    def __new__(mcs, name: str, bases: tuple, namespace: dict) -> Type:
        # Collect abstract methods from bases
        abstract_methods = set()
        for base in bases:
            if hasattr(base, '__abstractmethods__'):
                abstract_methods.update(base.__abstractmethods__)
        
        # Check if all abstract methods are implemented
        for method_name in abstract_methods:
            if method_name not in namespace:
                raise TypeError(
                    f"Can't instantiate abstract class {name} with abstract "
                    f"method {method_name}"
                )
        
        # Validate method signatures match interface
        for base in bases:
            if hasattr(base, '__annotations__'):
                for method_name, expected_type in base.__annotations__.items():
                    if method_name in namespace:
                        actual = namespace[method_name]
                        if not isinstance(actual, (staticmethod, classmethod)):
                            actual_sig = inspect.signature(actual)
                            expected_sig = inspect.signature(expected_type)
                            if actual_sig != expected_sig:
                                raise TypeError(
                                    f"Method {method_name} signature does not match "
                                    f"interface. Expected {expected_sig}, got {actual_sig}"
                                )
        
        return super().__new__(mcs, name, bases, namespace)

class Plugin(metaclass=InterfaceEnforcer):
    """Base interface for plugins"""
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the plugin"""
        pass
    
    @abstractmethod
    def execute(self, data: Dict[str, Any]) -> Any:
        """Execute plugin functionality"""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Cleanup plugin resources"""
        pass

class LoggingMixin:
    """Mixin providing logging functionality"""
    
    def log(self, message: str) -> None:
        print(f"[{self.__class__.__name__}] {message}")

class AbstractPlugin(Plugin, ABC):
    """Abstract base class providing common functionality"""
    
    def __init__(self):
        self._initialized = False
    
    def initialize(self) -> None:
        if self._initialized:
            raise RuntimeError("Plugin already initialized")
        self._initialize_impl()
        self._initialized = True
    
    @abstractmethod
    def _initialize_impl(self) -> None:
        """Implementation of initialization logic"""
        pass
    
    def cleanup(self) -> None:
        if not self._initialized:
            raise RuntimeError("Plugin not initialized")
        self._cleanup_impl()
        self._initialized = False
    
    @abstractmethod
    def _cleanup_impl(self) -> None:
        """Implementation of cleanup logic"""
        pass

class DataProcessor(AbstractPlugin, LoggingMixin):
    """Concrete plugin implementing both interface and abstract class"""
    
    def _initialize_impl(self) -> None:
        self.log("Initializing data processor")
        self._data = []
    
    def execute(self, data: Dict[str, Any]) -> Any:
        if not self._initialized:
            raise RuntimeError("Plugin not initialized")
        
        self.log(f"Processing data: {data}")
        result = self._process_data(data)
        self._data.append(result)
        return result
    
    def _process_data(self, data: Dict[str, Any]) -> Any:
        # Example processing
        return {k.upper(): v * 2 if isinstance(v, (int, float)) else v
                for k, v in data.items()}
    
    def _cleanup_impl(self) -> None:
        self.log("Cleaning up data processor")
        self._data.clear()

# Usage example:
processor = DataProcessor()
processor.initialize()

try:
    result = processor.execute({"name": "test", "value": 42})
    print(f"Processed result: {result}")
finally:
    processor.cleanup()
```

Key differences from Go/Java:
1. Python's metaclasses provide more control than Java's reflection
2. Multiple inheritance with mixins is more flexible than Go's interface composition
3. Method resolution order (MRO) handles multiple inheritance conflicts
4. Runtime type checking vs Go's compile-time interface satisfaction
5. Abstract base classes can provide partial implementations (like Java)
6. Duck typing allows for more flexible plugin architectures

</details>