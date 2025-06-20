# ✨ Advanced Python Features - Knowledge Check

> **Master Python's magic!** 🎩  
> Unlock decorators, generators, context managers, and metaprogramming.

---

## 📊 **Progress Tracker**
**Section:** Advanced Features | **Questions:** 6 | **Difficulty:** Expert | **Time:** ~10 min

---

### 🎯 **Question 1 of 6**
**Which magic methods create a context manager?**

```python
class FileManager:
    def __enter__(self):
        print("Opening file")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing file")
        return False

# Usage:
with FileManager() as fm:
    print("Working with file")
```

**A.** `__enter__` and `__exit__`  
**B.** `__init__` and `__del__`  
**C.** `__call__` and `__return__`  

---

### 🎯 **Question 2 of 6**
**How do you inspect an object's attributes?**

```python
class Person:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"Hello, I'm {self.name}"

person = Person("Alice")
# How to see all attributes and methods?
```

**A.** `dir(person)`  
**B.** `list(person)`  
**C.** `attrs(person)`  

---

### 🎯 **Question 3 of 6**
**What is a decorator fundamentally?**

```python
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end-start:.2f}s")
        return result
    return wrapper

@timer  # This is syntactic sugar for what?
def slow_function():
    time.sleep(1)
```

**A.** A function that modifies another function  
**B.** A special type of class  
**C.** A built-in Python construct  

---

### 🎯 **Question 4 of 6**
**What makes a function a generator?**

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a  # This keyword!
        a, b = b, a + b

# Usage:
fib = fibonacci()
print(next(fib))  # 0
print(next(fib))  # 1
```

**A.** The `yield` keyword  
**B.** Returning a list  
**C.** Using a loop  

---

### 🎯 **Question 5 of 6**
**What is metaprogramming?**

```python
# Creating classes dynamically:
def create_class(name, methods):
    return type(name, (), methods)

# Introspection:
if hasattr(obj, 'method_name'):
    getattr(obj, 'method_name')()

# Code that manipulates code!
```

**A.** Writing code that manipulates code  
**B.** Programming mathematical formulas  
**C.** Creating graphical interfaces  

---

### 🎯 **Question 6 of 6**
**What's the difference between `__str__` and `__repr__`?**

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def __str__(self):
        return f"Point at ({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

p = Point(1, 2)
print(str(p))   # Uses __str__
print(repr(p))  # Uses __repr__
```

**A.** No difference at all  
**B.** `__str__` for humans, `__repr__` for developers  
**C.** `__repr__` is deprecated

---

## 🎉 **Python Wizard Achieved!**

### 🎩 **Advanced Python Arsenal:**
- **Decorators** → `@property`, `@staticmethod`, `@functools.wraps`
- **Generators** → Memory-efficient iterators with `yield`
- **Context managers** → `with` statement magic
- **Metaclasses** → Classes that create classes
- **Descriptors** → Control attribute access
- **Magic methods** → Operator overloading (`__add__`, `__eq__`, etc.)

### 🔄 **Unique to Python:**
| Feature | Java | Go | Python |
|---------|------|----|---------| 
| **Decorators** | Annotations (limited) | ❌ | ✅ (powerful) |
| **Generators** | Streams (Java 8+) | Channels | `yield` |
| **Context managers** | try-with-resources | `defer` | `with` |
| **Metaclasses** | Reflection | ❌ | ✅ |
| **Magic methods** | Operator overloading | Methods | `__dunder__` |

### 🎯 **When to Use Advanced Features:**
- **Decorators** → Cross-cutting concerns (logging, timing, auth)
- **Generators** → Large datasets, streaming data
- **Context managers** → Resource management (files, connections)
- **Metaclasses** → Frameworks, ORMs (use sparingly!)

### 📈 **Next Steps:**
- ✅ **Python expert?** → Build production applications!
- 🔍 **See examples?** → Study [advanced_features_demo.py](./examples/advanced_features_demo.py)
- 🚀 **Level up?** → Contribute to open-source Python projects

### 🔍 **Answer Key:**
*Test your Python mastery!*

<details>
<summary>🔓 Show Answers</summary>

1. **A** - `__enter__` and `__exit__` implement context manager protocol
2. **A** - `dir(obj)` lists all attributes and methods of an object  
3. **A** - Decorators are functions that modify other functions
4. **A** - `yield` keyword makes a function a generator
5. **A** - Metaprogramming is code that manipulates code
6. **B** - `__str__` for end users, `__repr__` for developers/debugging

**🔥 Master insights:**
- **Context managers:** Also available via `@contextmanager` decorator
- **Generators:** Can be infinite, lazy evaluation saves memory
- **Decorators:** Can be stacked: `@decorator1 @decorator2`
- **Metaclasses:** "Magic that 99% of users should never need" - Tim Peters

</details>

---

*✨ **With great power:** Advanced features make Python truly magical!* 🎩🐍 

## 🌟 Expert Challenge

**Question**: Create a framework that combines Python's most powerful features to implement a type-safe, aspect-oriented programming system similar to Java Spring or Go's wire. Your solution should:

1. Use metaclasses and descriptors to:
   - Implement dependency injection
   - Provide compile-time type checking
   - Support aspect-oriented programming
   - Handle circular dependencies

2. Create a declarative configuration system that:
   - Uses dataclasses and type annotations
   - Supports runtime validation
   - Provides hot reloading
   - Handles environment-specific configs

**Hint**: Look into `typing.get_type_hints`, `dataclasses.dataclass`, `__set_name__`, and `typing.Protocol`.

<details>
<summary>Show Answer</summary>

```python
from dataclasses import dataclass, field
from typing import (
    Any, Callable, Dict, Generic, Optional, Protocol, Type, TypeVar, get_type_hints
)
import inspect
import threading
from functools import wraps
import weakref

T = TypeVar('T')
C = TypeVar('C', bound='Component')

class Inject(Generic[T]):
    """Descriptor for dependency injection"""
    
    def __init__(self, component_type: Optional[Type[T]] = None):
        self.component_type = component_type
        self.name: str = ""
    
    def __set_name__(self, owner: Type, name: str):
        self.name = name
        if self.component_type is None:
            # Infer type from annotation
            hints = get_type_hints(owner)
            self.component_type = hints[name]
    
    def __get__(self, instance: Any, owner: Type) -> T:
        if instance is None:
            return self
        
        if not hasattr(instance, f'_{self.name}'):
            container = Container.get_instance()
            setattr(
                instance,
                f'_{self.name}',
                container.get_component(self.component_type)
            )
        
        return getattr(instance, f'_{self.name}')

class Component(Protocol):
    """Base protocol for all components"""
    def initialize(self) -> None: ...
    def destroy(self) -> None: ...

@dataclass
class ComponentConfig:
    """Configuration for a component"""
    component_type: Type[Component]
    singleton: bool = True
    lazy: bool = False
    aspects: list[Callable] = field(default_factory=list)

class Container:
    _instance = None
    _lock = threading.Lock()
    
    def __init__(self):
        self._components: Dict[Type, ComponentConfig] = {}
        self._instances: Dict[Type, weakref.ref] = {}
    
    @classmethod
    def get_instance(cls) -> 'Container':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    
    def register(
        self,
        component_type: Type[C],
        *,
        singleton: bool = True,
        lazy: bool = False,
        aspects: list[Callable] = None
    ) -> None:
        """Register a component type"""
        self._components[component_type] = ComponentConfig(
            component_type=component_type,
            singleton=singleton,
            lazy=lazy,
            aspects=aspects or []
        )
    
    def get_component(self, component_type: Type[C]) -> C:
        """Get or create a component instance"""
        if component_type not in self._components:
            raise ValueError(f"Component {component_type} not registered")
        
        config = self._components[component_type]
        
        if config.singleton:
            instance_ref = self._instances.get(component_type)
            instance = instance_ref() if instance_ref else None
            
            if instance is None:
                instance = self._create_component(config)
                self._instances[component_type] = weakref.ref(instance)
            
            return instance
        else:
            return self._create_component(config)
    
    def _create_component(self, config: ComponentConfig) -> Component:
        """Create a new component instance with aspects"""
        instance = config.component_type()
        
        # Apply aspects
        for aspect in config.aspects:
            # Wrap all public methods
            for name, method in inspect.getmembers(
                instance,
                predicate=inspect.ismethod
            ):
                if not name.startswith('_'):
                    setattr(instance, name, aspect(method))
        
        instance.initialize()
        return instance

def aspect(func: Callable) -> Callable:
    """Decorator to create an aspect"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Before {func.__name__}")
        try:
            result = func(*args, **kwargs)
            print(f"After {func.__name__}")
            return result
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")
            raise
    return wrapper

# Example usage:
@dataclass
class DatabaseConfig:
    url: str
    max_connections: int = 10
    timeout: float = 30.0

class Database(Component):
    def __init__(self, config: Optional[DatabaseConfig] = None):
        self.config = config or DatabaseConfig(url="default://db")
    
    def initialize(self) -> None:
        print(f"Connecting to {self.config.url}")
    
    def destroy(self) -> None:
        print("Closing database connection")
    
    def query(self, sql: str) -> list:
        print(f"Executing: {sql}")
        return []

class UserService(Component):
    db: Database = Inject()  # Type inferred from annotation
    
    def initialize(self) -> None:
        print("Initializing user service")
    
    def destroy(self) -> None:
        print("Cleaning up user service")
    
    def get_user(self, user_id: int) -> dict:
        return self.db.query(f"SELECT * FROM users WHERE id = {user_id}")[0]

# Set up the container
container = Container.get_instance()

# Register components with aspects
container.register(
    Database,
    singleton=True,
    aspects=[aspect]
)
container.register(
    UserService,
    singleton=True,
    aspects=[aspect]
)

# Use the services
user_service = container.get_component(UserService)
user = user_service.get_user(123)
```

Key differences from Go/Java:
1. Python's type hints provide runtime type information
2. Descriptors offer more powerful dependency injection
3. Metaclasses enable compile-time validation
4. Aspects can be applied dynamically
5. Weak references prevent memory leaks
6. Configuration is more flexible with dataclasses
7. Protocol types are structural (like Go interfaces)

</details>

---

*✨ **With great power:** Advanced features make Python truly magical!* 🎩🐍 