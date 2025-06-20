# 📝 Basic Syntax - Knowledge Check

> **Level up your Python syntax skills!** 🎯  
> Master the fundamentals that separate Python from Java/Go.

---

## 📊 **Progress Tracker**
**Section:** Basic Syntax | **Questions:** 5 | **Difficulty:** Beginner | **Time:** ~4 min

---

### 🎯 **Question 1 of 5**
**Which Python data type can be modified after creation?**

```python
# Examine these data types:
my_tuple = (1, 2, 3)
my_list = [1, 2, 3]
my_string = "Hello"
```

**A.** `tuple`  
**B.** `list`  
**C.** `str`  

---

### 🎯 **Question 2 of 5**
**What's the modern way to declare a typed variable?**

```python
# Python 3.6+ type hint syntax:
```

**A.** `int x = 5`  
**B.** `x: int = 5`  
**C.** `x := 5`  

---

### 🎯 **Question 3 of 5**
**What does this code output?**

```python
print(type(3.14))
```

**A.** `<class 'float'>`  
**B.** `<type 'float'>`  
**C.** `float`  

---

### 🎯 **Question 4 of 5**
**Which string formatting methods work in Python?**

```python
name = "Python"
version = 3.9

# All valid approaches:
```

**A.** `%` formatting only  
**B.** `.format()` method only  
**C.** `%`, `.format()`, and f-strings  

---

### 🎯 **Question 5 of 5**
**How do you write comments in Python?**

```python
# Different comment styles:
```

**A.** `// single line comment`  
**B.** `# single line comment`  
**C.** `<!-- HTML style -->`

---

## 🎉 **Syntax Mastery Check!**

### 🔄 **Compare with Java/Go:**
- **Java:** `int x = 5;` → **Python:** `x: int = 5`
- **Go:** `var x int = 5` → **Python:** `x: int = 5`
- **Dynamic typing** makes Python more flexible! 🚀

### 📈 **Next Steps:**
- ✅ **Confident?** → Tackle [Control Flow](../03_control_flow/)
- 🔄 **Need practice?** → Run the [examples](./examples/data_types.py)
- 📚 **Want theory?** → Review the [README](./README.md)

### 🔍 **Answer Key:**
*Click to reveal when you're ready to check*

<details>
<summary>🔓 Show Answers</summary>

1. **B** - `list` is mutable (can be modified)
2. **B** - `x: int = 5` uses type hints (PEP 484)
3. **A** - Python shows `<class 'float'>` for type info
4. **C** - All three methods work: `%`, `.format()`, f-strings
5. **B** - `#` creates single-line comments in Python

**💡 Pro tip:** Python's dynamic typing + type hints = best of both worlds!

</details>

---

*🎨 **Style matters:** Clean syntax leads to clean thinking!* ✨🐍 

## 🌟 Expert Challenge

**Question**: Given your experience with Go's value types and pointer types, explain the following Python behavior and implement a solution:

```python
def modify_list(lst):
    lst.append(4)
    lst = [7, 8, 9]  # This doesn't affect the original list
    lst.append(10)

def modify_int(x):
    x += 1  # This doesn't affect the original number

my_list = [1, 2, 3]
my_num = 42

modify_list(my_list)
modify_int(my_num)

print(my_list)  # [1, 2, 3, 4] - Why not [7, 8, 9, 10]?
print(my_num)   # 42 - Why not 43?
```

Create a class that mimics Go's pointer behavior for both mutable and immutable types, with proper `__str__` and `__repr__` methods.

**Hint**: Consider Python's object references, mutability, and the `id()` function.

<details>
<summary>Show Answer</summary>

```python
class Ptr:
    def __init__(self, value):
        self._value = value
    
    def get(self):
        return self._value
    
    def set(self, new_value):
        self._value = new_value
    
    def __str__(self):
        return f"Ptr({self._value})"
    
    def __repr__(self):
        return f"Ptr(id={id(self)}, value={self._value})"

# Now we can have Go-like behavior:
def modify_with_ptr(x: Ptr):
    x.set(x.get() + 1)  # Actually modifies the value

num_ptr = Ptr(42)
modify_with_ptr(num_ptr)
print(num_ptr.get())  # 43

# Key differences from Go:
# 1. Python variables are references to objects
# 2. Assignment operations rebind references
# 3. Mutable objects can be modified through any reference
# 4. Immutable objects create new instances on modification
```

The original behavior occurs because:
1. `lst = [7, 8, 9]` creates a new list object and rebinds the local name `lst`
2. The original reference in `my_list` is unaffected
3. Integers are immutable, so `x += 1` creates a new integer object
4. Python lacks Go's explicit pointer semantics, but everything is effectively a reference

</details> 