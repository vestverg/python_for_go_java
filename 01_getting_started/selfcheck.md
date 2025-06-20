# 🚀 Getting Started - Knowledge Check

> **Welcome to your first Python checkpoint!** 🎯  
> Test your understanding of Python fundamentals before moving forward.

---

## 📊 **Progress Tracker**
**Section:** Getting Started | **Questions:** 5 | **Time:** ~3 min

---

### 🎯 **Question 1 of 5**
**Which command creates a virtual environment in Python?**

```bash
# Choose the correct command:
```

**A.** `python3 -m venv venv`  
**B.** `pip install venv`  
**C.** `python create venv`  

---

### 🎯 **Question 2 of 5**
**Which file manages your project dependencies?**

```python
# In a Python project structure:
my_project/
├── src/
├── tests/
└── ??? # Which file lists dependencies?
```

**A.** `requirements.txt`  
**B.** `dependencies.txt`  
**C.** `setup.py`  

---

### 🎯 **Question 3 of 5**
**How do you activate a virtual environment on macOS/Linux?**

```bash
# After creating venv, which command activates it?
```

**A.** `activate venv`  
**B.** `source venv/bin/activate`  
**C.** `venv/activate`  

---

### 🎯 **Question 4 of 5**
**What is "The Zen of Python"?**

```python
# Try this in Python REPL:
import this
```

**A.** A set of Python design principles  
**B.** A Python package for meditation  
**C.** A type of virtual environment  

---

### 🎯 **Question 5 of 5**
**Which command executes a Python script?**

```bash
# Given a file: hello.py
```

**A.** `python run hello.py`  
**B.** `python3 hello.py`  
**C.** `run hello.py`

---

## 🎉 **Checkpoint Complete!**

### 📈 **Next Steps:**
- ✅ **80%+ correct?** → Move to [Basic Syntax](../02_basic_syntax/)
- ❓ **Need review?** → Check out the [examples](./examples/) folder
- 💡 **Want more practice?** → Try the hands-on exercises

### 🔍 **Answer Key:**
*Hover or click to reveal answers when ready*

<details>
<summary>🔓 Show Answers</summary>

1. **A** - `python3 -m venv venv` creates a virtual environment
2. **A** - `requirements.txt` lists project dependencies  
3. **B** - `source venv/bin/activate` activates the environment
4. **A** - The Zen of Python contains design principles
5. **B** - `python3 hello.py` runs a Python script

</details>

---

*💪 **Remember:** Every expert was once a beginner. Keep coding!* 🐍✨ 

## 🌟 Expert Challenge

**Question**: In Go, dependency management is handled through `go.mod` and `go.sum` files. Compare and contrast this with Python's virtual environments and `requirements.txt`. How would you implement a system that:
1. Automatically activates the correct virtual environment when entering a project directory
2. Ensures all developers use exactly the same package versions (like Go's vendoring)
3. Handles both development and production dependencies separately
4. Provides a lockfile mechanism similar to `go.sum`

**Hint**: Consider tools like `poetry`, `pipenv`, and `pyproject.toml`

<details>
<summary>Show Answer</summary>

A complete solution would involve:

1. Using `direnv` with a `.envrc` file:
```bash
layout python3
```

2. Using Poetry for dependency management:
```toml
[tool.poetry]
name = "myproject"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.8"
requests = "^2.28.0"

[tool.poetry.dev-dependencies]
pytest = "^7.1.0"
```

3. Poetry automatically generates `poetry.lock` (equivalent to `go.sum`)

4. Key differences from Go:
   - Python needs isolated environments (unlike Go's global GOPATH)
   - Poetry/pipenv provide deterministic builds (like Go modules)
   - Python's setup is more flexible but requires more configuration
   - Go's approach is more standardized across projects

</details> 