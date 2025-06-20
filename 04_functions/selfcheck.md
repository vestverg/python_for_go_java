# 🔧 Functions - Knowledge Check

> **Unlock Python's functional power!** ⚡  
> Master functions, decorators, and Python's unique functional features.

---

## 📊 **Progress Tracker**
**Section:** Functions | **Questions:** 6 | **Difficulty:** Intermediate+ | **Time:** ~6 min

---

### 🎯 **Question 1 of 6**
**What's the correct function definition syntax?**

```python
# Function definition patterns:
# Java: public static void foo() { }
# Go: func foo() { }
# Python: ???
```

**A.** `function foo():`  
**B.** `def foo():`  
**C.** `func foo() {}`  

---

### 🎯 **Question 2 of 6**
**What does a function return without an explicit `return` statement?**

```python
def greet(name):
    print(f"Hello, {name}!")
    # No return statement

result = greet("Python")
print(result)  # What prints here?
```

**A.** `0`  
**B.** `None`  
**C.** `False`  

---

### 🎯 **Question 3 of 6**
**What is a lambda function?**

```python
# Traditional function:
def square(x):
    return x ** 2

# Lambda equivalent:
square = lambda x: x ** 2
```

**A.** A function with no name (anonymous)  
**B.** A function with multiple return values  
**C.** A function that calls itself (recursive)  

---

### 🎯 **Question 4 of 6**
**How do you set default parameter values?**

```python
# Default arguments in action:
def greet(name, greeting=???):
    return f"{greeting}, {name}!"

print(greet("Alice"))  # Should work
print(greet("Bob", "Hi"))  # Should also work
```

**A.** `def greet(name, greeting := "Hello"):`  
**B.** `def greet(name, greeting = "Hello"):`  
**C.** `def greet(name, greeting == "Hello"):`  

---

### 🎯 **Question 5 of 6**
**What does `*args` do in a function?**

```python
def calculate(*args):
    print(f"Received: {args}")
    return sum(args)

result = calculate(1, 2, 3, 4, 5)
# args becomes: (1, 2, 3, 4, 5)
```

**A.** Accepts variable positional arguments  
**B.** Accepts variable keyword arguments  
**C.** Requires exactly one argument  

---

### 🎯 **Question 6 of 6**
**What's a decorator in Python?**

```python
@timer
def slow_function():
    time.sleep(1)
    return "Done!"

# The @ symbol applies a decorator
```

**A.** A function that modifies another function  
**B.** A special type of class  
**C.** A built-in Python keyword

---

## 🎉 **Function Mastery Achieved!**

### 🔥 **Python Function Superpowers:**
- **First-class objects** → Functions can be stored in variables
- **Decorators** → Modify function behavior elegantly  
- **Lambda expressions** → Concise anonymous functions
- **Flexible arguments** → `*args` and `**kwargs`

### 🔄 **vs Java/Go:**
| Feature | Java | Go | Python |
|---------|------|----|---------| 
| **Functions as values** | ⚠️ (complex) | ✅ | ✅ |
| **Decorators** | Annotations | ❌ | ✅ |
| **Default params** | ❌ | ❌ | ✅ |
| **Variable args** | `...` | `...interface{}` | `*args, **kwargs` |

### 📈 **Next Steps:**
- ✅ **Function master?** → Dive into [OOP](../05_oop/)
- 🎨 **Try decorators?** → Experiment with `@property`, `@staticmethod`
- 🔍 **See examples?** → Run [functions.py](./examples/functions.py)

### 🔍 **Answer Key:**
*Test your functional programming knowledge!*

<details>
<summary>🔓 Show Answers</summary>

1. **B** - `def foo():` defines functions in Python
2. **B** - Functions return `None` without explicit return
3. **A** - Lambda creates anonymous functions: `lambda x: x**2`
4. **B** - `def func(param="default"):` sets default values
5. **A** - `*args` collects variable positional arguments into tuple
6. **A** - Decorators are functions that modify other functions

**💡 Pro tip:** Master `*args`, `**kwargs`, and decorators for Pythonic code!

</details>

---

*⚡ **Functions are power:** Clean functions = clean architecture!* ✨🐍 

## 🌟 Expert Challenge

**Question**: Create a sophisticated decorator system that mimics Go's middleware pattern and Java's annotations. Your solution should:

1. Implement a caching decorator that:
   - Uses weak references to prevent memory leaks
   - Supports TTL (time-to-live) for cached values
   - Is thread-safe
   - Handles async functions correctly

2. Create a method decorator that:
   - Enforces type checking (like Go's static typing)
   - Validates return values
   - Logs performance metrics
   - Supports dependency injection

**Hint**: Look into `functools.wraps`, `weakref`, `threading.Lock`, and `inspect.signature`.

<details>
<summary>Show Answer</summary>

```python
import asyncio
import functools
import inspect
import threading
import time
import weakref
from typing import Any, Callable, Dict, Optional, TypeVar, cast

T = TypeVar('T')

class CacheItem:
    def __init__(self, value: Any, ttl: Optional[float]):
        self.value = value
        self.timestamp = time.time()
        self.ttl = ttl

class SmartCache:
    def __init__(self):
        self._cache: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()
        self._lock = threading.Lock()
    
    def get(self, key: Any) -> Optional[Any]:
        with self._lock:
            if key not in self._cache:
                return None
            
            item = self._cache[key]
            if item.ttl and time.time() - item.timestamp > item.ttl:
                del self._cache[key]
                return None
            
            return item.value
    
    def set(self, key: Any, value: Any, ttl: Optional[float] = None):
        with self._lock:
            self._cache[key] = CacheItem(value, ttl)

def cached(ttl: Optional[float] = None):
    cache = SmartCache()
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        sig = inspect.signature(func)
        
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> T:
            key = (func.__name__, args, frozenset(kwargs.items()))
            result = cache.get(key)
            if result is not None:
                return cast(T, result)
            
            result = await func(*args, **kwargs)
            cache.set(key, result, ttl)
            return result
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> T:
            key = (func.__name__, args, frozenset(kwargs.items()))
            result = cache.get(key)
            if result is not None:
                return cast(T, result)
            
            result = func(*args, **kwargs)
            cache.set(key, result, ttl)
            return result
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    
    return decorator

def validate_types(func: Callable[..., T]) -> Callable[..., T]:
    sig = inspect.signature(func)
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        bound_args = sig.bind(*args, **kwargs)
        for param_name, value in bound_args.arguments.items():
            param = sig.parameters[param_name]
            if param.annotation != inspect.Parameter.empty:
                if not isinstance(value, param.annotation):
                    raise TypeError(
                        f"Parameter {param_name} must be {param.annotation.__name__}, "
                        f"got {type(value).__name__}"
                    )
        
        result = func(*args, **kwargs)
        if sig.return_annotation != inspect.Parameter.empty:
            if not isinstance(result, sig.return_annotation):
                raise TypeError(
                    f"Return value must be {sig.return_annotation.__name__}, "
                    f"got {type(result).__name__}"
                )
        return result
    
    return wrapper

# Usage example:
@cached(ttl=60)
@validate_types
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# This will use cache and validate types
result = fibonacci(10)

# This will raise TypeError
try:
    fibonacci("not a number")
except TypeError as e:
    print(f"Caught error: {e}")

# Async example
@cached(ttl=60)
async def fetch_data(url: str) -> dict:
    await asyncio.sleep(1)  # Simulate API call
    return {"data": "example"}
```

Key differences from Go/Java:
1. Python decorators are more flexible than Java annotations
2. Type hints are optional and runtime-checked (unlike Go's compile-time checking)
3. Decorators can modify function behavior (not just metadata like Java annotations)
4. Python's metaprogramming is more powerful but requires careful memory management
5. Async support requires special handling (unlike Go's goroutines)

</details> 