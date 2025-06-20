# 🔄 Control Flow - Knowledge Check

> **Master Python's flow control!** 🌊  
> Learn how Python handles decisions, loops, and exceptions differently from Java/Go.

---

## 📊 **Progress Tracker**
**Section:** Control Flow | **Questions:** 5 | **Difficulty:** Intermediate | **Time:** ~5 min

---

### 🎯 **Question 1 of 5**
**What's Python's exception handling syntax?**

```python
# Exception handling comparison:
# Java: try { } catch (Exception e) { }
# Go: if err != nil { }
# Python: ???
```

**A.** `try/catch`  
**B.** `try/except`  
**C.** `handle/except`  

---

### 🎯 **Question 2 of 5**
**Which loop type continues while a condition is true?**

```python
# Loop types in Python:
for item in collection:    # iterate over items
while condition:           # continue while true
# Note: No do-while in Python!
```

**A.** `for`  
**B.** `while`  
**C.** `do-while`  

---

### 🎯 **Question 3 of 5**
**What does this code print?**

```python
for i in range(3):
    print(i)
```

**A.** `1 2 3`  
**B.** `0 1 2`  
**C.** `0 1 2 3`  

---

### 🎯 **Question 4 of 5**
**How do you manually trigger an exception?**

```python
# Creating custom exceptions:
if age < 0:
    ??? Exception("Age cannot be negative")
```

**A.** `throw Exception()`  
**B.** `raise Exception()`  
**C.** `error Exception()`  

---

### 🎯 **Question 5 of 5**
**When does the `else` block execute in a loop?**

```python
for i in range(3):
    print(i)
    if i == 5:  # Never true
        break
else:
    print("Loop completed!")  # When does this run?
```

**A.** If loop never executes  
**B.** When loop completes normally  
**C.** Only when loop breaks

---

## 🎉 **Flow Control Mastery!**

### 🔄 **Language Comparison:**
| Feature | Java | Go | Python |
|---------|------|----|---------| 
| **Exceptions** | `try/catch` | `if err != nil` | `try/except` |
| **Loops** | `for/while` | `for/range` | `for/while` |
| **No semicolons** | ❌ | ✅ | ✅ |

### 📈 **Next Steps:**
- ✅ **Ready for more?** → Explore [Functions](../04_functions/)
- 🔍 **Need examples?** → Check [control_flow.py](./examples/control_flow.py)
- 🎲 **Practice loops?** → Try different `range()` patterns

### 🔍 **Answer Key:**
*Ready to check your Python flow control knowledge?*

<details>
<summary>🔓 Show Answers</summary>

1. **B** - `try/except` is Python's exception syntax
2. **B** - `while` loops continue until condition becomes false
3. **B** - `range(3)` produces `[0, 1, 2]` (excludes end)
4. **B** - `raise` triggers exceptions in Python
5. **B** - `else` runs when loop completes without `break`

**🔥 Advanced tip:** Python's `for/else` and `while/else` are unique features!

</details>

---

*🌊 **Flow like water:** Master control flow, master programming logic!* ✨🐍 

## 🌟 Expert Challenge

**Question**: In Go, you can create custom iterators by implementing the `Iterator` interface. In Python, implement a custom iterator that:

1. Generates Fibonacci numbers infinitely (like Go's channels)
2. Allows for multiple independent iterations
3. Supports the `async for` protocol
4. Implements a custom context manager for cleanup

Compare this with Go's iteration patterns.

**Hint**: Look into `__iter__`, `__next__`, `__aiter__`, `__anext__`, `__enter__`, and `__exit__`.

<details>
<summary>Show Answer</summary>

```python
import asyncio
from typing import AsyncIterator, Iterator, Optional
from contextlib import contextmanager

class FibonacciIterator:
    def __init__(self, max_value: Optional[int] = None):
        self.max_value = max_value
        self.reset()
    
    def reset(self):
        self.a, self.b = 0, 1
        self.count = 0
    
    def __iter__(self) -> Iterator[int]:
        return self
    
    def __next__(self) -> int:
        if self.max_value and self.count >= self.max_value:
            raise StopIteration
        
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return result
    
    async def __aiter__(self) -> AsyncIterator[int]:
        return self
    
    async def __anext__(self) -> int:
        await asyncio.sleep(0.1)  # Simulate async work
        try:
            return next(self)
        except StopIteration:
            raise StopAsyncIteration
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.reset()

# Usage examples:

# 1. Basic iteration
fib = FibonacciIterator(5)
print(list(fib))  # [0, 1, 1, 2, 3]

# 2. Context manager
with FibonacciIterator(3) as fib:
    for n in fib:
        print(n)  # 0, 1, 1

# 3. Async iteration
async def demo():
    async with FibonacciIterator(4) as fib:
        async for n in fib:
            print(n)  # 0, 1, 1, 2

# 4. Generator expression (unique to Python)
fib = FibonacciIterator(6)
squares = (n * n for n in fib)
print(list(squares))  # [0, 1, 1, 4, 9, 25]
```

Key differences from Go:
1. Python's iteration protocol is more flexible with `__iter__` and `__next__`
2. Async iteration is built into the language with `async for`
3. Context managers provide resource cleanup (similar to Go's `defer`)
4. Generator expressions offer lazy evaluation (no direct Go equivalent)
5. No need for explicit channel creation like in Go

</details>

---

*🌊 **Flow like water:** Master control flow, master programming logic!* ✨🐍 