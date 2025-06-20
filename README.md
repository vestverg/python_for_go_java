# 🐍 Python Tutorial for Java and Go Developers

A comprehensive Python tutorial specifically designed for developers with Java or Go experience. This tutorial focuses on Python's unique features while drawing parallels to concepts you already know.

## 📚 Table of Contents

1. [🚀 Getting Started](./01_getting_started/) - Python installation, setup, virtual environments, and basic concepts
2. [📝 Basic Syntax](./02_basic_syntax/) - Variables, data types, and basic operations
3. [🔄 Control Flow](./03_control_flow/) - Conditionals, loops, and exception handling
4. [🔧 Functions](./04_functions/) - Function definition, arguments, and advanced features
5. [🏗️ Object-Oriented Programming](./05_oop/) - Classes, inheritance, and OOP patterns
6. [📦 Modules and Packages](./06_modules_and_packages/) - Code organization and distribution
7. [⚡ Concurrency](./07_concurrency/) - Threading, multiprocessing, and async programming
8. [✨ Advanced Python Features](./08_python_features/) - Decorators, generators, and metaprogramming

## ✅ Prerequisites

- Experience with Java or Go programming
- Basic understanding of programming concepts
- Familiarity with command-line interface

## 🎯 Learning Approach

This tutorial is structured to:

1. **🔄 Compare and Contrast**: Each section shows how Python concepts relate to Java/Go equivalents
2. **👨‍💻 Hands-on Examples**: Practical code examples you can run and experiment with
3. **⭐ Best Practices**: Modern Python practices including type hints, testing, and tooling
4. **🌍 Real-world Applications**: Complete examples like library management systems and data processors

## 🚀 Quick Start

1. **📥 Install Python 3.8+**

   ```bash
   # Check if Python is installed
   python3 --version
   
   # Install if needed (varies by OS)
   # macOS: brew install python
   # Ubuntu: sudo apt update && sudo apt install python3
   # Windows: Download from python.org
   ```

2. **🔧 Set up virtual environment** (Essential for Python development!)

   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   source venv/bin/activate          # On macOS/Linux
   venv\Scripts\activate             # On Windows Command Prompt
   venv\Scripts\Activate.ps1         # On Windows PowerShell
   
   # Install dependencies
   pip install -r requirements.txt
   
   # For development (includes testing, linting tools)
   pip install -r requirements-dev.txt
   ```

3. **▶️ Run examples**

   ```bash
   cd 01_getting_started/examples
   python hello.py
   ```

4. **🏗️ Create new projects** (Use provided scripts)

   ```bash
   # Unix/Linux/macOS
   ./01_getting_started/examples/create_project.sh my_project
   
   # Windows PowerShell
   .\01_getting_started\examples\create_project.ps1 my_project
   ```

## 🌟 Key Python Features Covered

### ☕ For Java Developers

- **🔄 Dynamic typing** vs static typing
- **🦆 Duck typing** vs interface-based typing
- **🔗 Multiple inheritance** vs single inheritance + interfaces
- **🎯 Properties** vs getter/setter methods
- **🎨 Decorators** vs annotations
- **🔒 Context managers** vs try-with-resources
- **📊 List comprehensions** vs streams

### 🐹 For Go Developers

- **🏗️ Object-oriented programming** vs struct-based design
- **⚠️ Exception handling** vs error values
- **🔄 Dynamic typing** vs static typing
- **🔗 Inheritance** vs composition
- **🧵 Threading model** and the GIL vs goroutines
- **📦 Package management** vs modules

## 📁 Project Structure

```text
📁 python_for_go_java/
├── 📁 01_getting_started/          # Python basics and setup
│   ├── 📁 examples/
│   │   ├── 🐍 hello.py             # First Python program
│   │   ├── 🐍 virtual_env_demo.py   # Environment demo
│   │   ├── 📜 create_project.ps1   # Windows setup script
│   │   ├── 📜 create_project.sh    # Unix setup script
│   │   └── 📄 README.md            # Examples guide
│   └── 📄 README.md                # Installation and concepts
├── 📁 02_basic_syntax/            # Variables and data types
│   ├── 📁 examples/
│   │   └── 🐍 data_types.py        # Type system examples
│   └── 📄 README.md                # Syntax fundamentals
├── 📁 03_control_flow/            # Conditionals and loops
│   ├── 📁 examples/
│   │   └── 🐍 control_flow.py      # Flow control examples
│   └── 📄 README.md                # Control structures
├── 📁 04_functions/               # Function definition and usage
│   ├── 📁 examples/
│   │   └── 🐍 functions.py         # Function examples
│   └── 📄 README.md                # Functions and scope
├── 📁 05_oop/                     # Object-oriented programming
│   ├── 📁 examples/
│   │   ├── 🐍 library_system.py    # Library management system
│   │   ├── 🐍 shapes.py            # Inheritance example
│   │   ├── 🐍 test_library_system.py # System tests
│   │   ├── 🐍 test_shapes.py       # Shape tests
│   │   ├── 📝 library.log          # Log file
│   │   └── 📄 README.md            # Examples guide
│   └── 📄 README.md                # OOP concepts
├── 📁 06_modules_and_packages/    # Code organization
│   ├── 📁 examples/
│   │   ├── 🐍 example_usage.py     # Usage examples
│   │   ├── 📁 mypackage/          # Complete package example
│   │   │   ├── 🐍 __init__.py      # Package initialization
│   │   │   ├── 🐍 core.py          # Core functionality
│   │   │   ├── 📁 subpackage/      # Nested package
│   │   │   │   ├── 🐍 __init__.py  # Subpackage initialization
│   │   │   │   └── 🐍 helpers.py   # Helper functions
│   │   │   └── 🐍 utils.py         # Utility functions
│   │   └── ⚙️ setup.py             # Package setup
│   └── 📄 README.md                # Modules and packaging
├── 📁 07_concurrency/             # Parallel programming
│   ├── 📁 docs/                   # Detailed documentation
│   │   ├── 📄 01-gil-and-concepts.md
│   │   ├── 📄 02-threading.md
│   │   ├── 📄 03-multiprocessing.md
│   │   ├── 📄 04-async-await.md
│   │   ├── 📄 05-performance.md
│   │   ├── 📄 06-debugging.md
│   │   ├── 📄 07-production-patterns.md
│   │   └── 📄 08-troubleshooting.md
│   ├── 📁 examples/
│   │   ├── 🐍 asyncio_example.py   # Async programming
│   │   ├── 🐍 threading_example.py # Threading examples
│   │   └── 🐍 multiprocessing_example.py # Process examples
│   └── 📄 README.md                # Concurrency models
├── 📁 08_python_features/         # Advanced features
│   ├── 📁 examples/
│   │   └── 🐍 advanced_features_demo.py # Decorators, generators, etc.
│   └── 📄 README.md                # Python-specific features
├── 📁 .github/                    # GitHub configuration
│   └── 📁 workflows/              # GitHub Actions workflows
├── 📁 tests/                      # Comprehensive test suite
│   ├── 🐍 test_advanced_features.py
│   ├── 🐍 test_concurrency.py
│   ├── 🐍 test_control_flow.py
│   ├── 🐍 test_data_types.py
│   ├── 🐍 test_functions.py
│   ├── 🐍 test_hello.py
│   ├── 🐍 test_modules.py
│   └── 🐍 test_oop.py
├── 📄 Makefile                   # Build automation
├── 📄 README.md                  # This file
├── ⚙️ .gitignore                 # Git ignore patterns
├── ⚙️ .pylintrc                  # Pylint configuration
├── ⚙️ mypy.ini                   # Type checking config
├── ⚙️ pyproject.toml             # Project configuration
├── ⚙️ pytest.ini                 # Test configuration
├── 📄 requirements-dev.txt       # Dev dependencies
├── 📄 requirements.txt           # Project dependencies
└── 🐍 verify_project.py          # Project verification
```

## 🌟 Features of This Tutorial

### 📚 Comprehensive Examples
- **📖 Library Management System**: Complete OOP example with abstract classes, protocols, and design patterns
- **📐 Geometric Shapes**: Inheritance and composition demonstrations
- **⚡ Concurrency Examples**: Threading, multiprocessing, and async/await patterns
- **📦 Package Examples**: Full package structure with setup.py and pyproject.toml

### 🔧 Modern Python Practices
- **🏷️ Type Hints**: Throughout all examples for better code clarity
- **🧪 Testing**: pytest examples with fixtures, mocking, and parametrization
- **📝 Documentation**: Comprehensive docstrings and README files
- **🛠️ Tooling**: Configuration for mypy, black, flake8, and pytest
- **📦 Packaging**: Modern packaging with pyproject.toml

### 📊 Comparison Tables
Each section includes detailed comparison tables showing:
- **💡 Syntax differences** between Python, Java, and Go
- **🔄 Conceptual mappings** between language features
- **⭐ Best practices** for each language
- **⚡ Performance considerations** and trade-offs

## 🛠️ Development Setup

### 🔧 Required Tools
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Type checking
mypy .

# Code formatting
black .

# Linting
flake8 .

# Testing
pytest --cov=. --cov-report=html
```

### 💻 IDE Configuration
The tutorial includes configuration for:
- **🆚 VS Code**: `.vscode/settings.json` with Python extensions
- **🔷 PyCharm**: Project configuration and code style settings
- **📝 Vim/Neovim**: LSP and plugin recommendations

## 🎓 Learning Path

### 🌱 Beginner (Coming from Java/Go)
1. Start with [🚀 Getting Started](./01_getting_started/) to understand Python philosophy
2. Work through [📝 Basic Syntax](./02_basic_syntax/) focusing on dynamic typing
3. Practice [🔄 Control Flow](./03_control_flow/) with pattern matching
4. Master [🔧 Functions](./04_functions/) including decorators and closures

### 🚀 Intermediate
1. Dive deep into [🏗️ OOP](./05_oop/) comparing with Java/Go patterns
2. Learn [📦 Modules and Packages](./06_modules_and_packages/) for code organization
3. Explore [⚡ Concurrency](./07_concurrency/) understanding the GIL and async model

### 🎯 Advanced
1. Master [✨ Advanced Features](./08_python_features/) like metaclasses and descriptors
2. Build the complete library management system
3. Contribute to open-source Python projects

## 💡 Key Concepts by Section

### 1. 🚀 Getting Started
- Python philosophy (The Zen of Python)
- Virtual environments and package management
- REPL and interactive development
- IDE setup and tooling

### 2. 📝 Basic Syntax
- Dynamic typing vs static typing
- Built-in data types and collections
- String handling and formatting
- Type hints and mypy

### 3. 🔄 Control Flow
- Pythonic conditionals and loops
- Exception handling vs error codes
- Pattern matching (Python 3.10+)
- Context managers

### 4. 🔧 Functions

- First-class functions and closures
- Decorators and higher-order functions
- Generators and iterators
- Functional programming features

### 5. 🏗️ Object-Oriented Programming

- Classes and inheritance
- Abstract base classes and protocols
- Multiple inheritance and MRO
- Properties and descriptors

### 6. 📦 Modules and Packages

- Import system and PYTHONPATH
- Package structure and __init__.py
- Distribution and packaging
- Virtual environments

### 7. ⚡ Concurrency

- Threading and the GIL
- Multiprocessing for CPU-bound tasks
- Async/await for I/O-bound tasks
- Comparison with Java threads and Go goroutines

### 8. ✨ Advanced Features

- Metaclasses and class creation
- Descriptors and properties
- Context managers and protocols
- Introspection and metaprogramming

## 🧪 Testing and Quality Assurance

### 📊 Test Coverage

- **🔬 Unit tests** for all major examples
- **🔗 Integration tests** for complex systems
- **🎲 Property-based testing** with Hypothesis
- **⚡ Performance benchmarks** for concurrency examples

### ✅ Code Quality

- **🏷️ Type checking** with mypy (100% coverage)
- **🎨 Code formatting** with black
- **🔍 Linting** with flake8 and pylint
- **🛡️ Security scanning** with bandit

### 📚 Documentation

- **📖 Comprehensive README** files for each section
- **💬 Inline documentation** with detailed docstrings
- **💻 Code examples** with expected output
- **📊 Comparison tables** for Java/Go developers

## 🤝 Contributing

This tutorial is designed to be:

- **✅ Accurate**: All examples tested with Python 3.8+
- **📚 Comprehensive**: Covers beginner to advanced topics
- **🎯 Practical**: Real-world examples and best practices
- **🔄 Comparative**: Always relates to Java/Go concepts

### 🚀 Areas for Improvement

- Additional real-world examples
- More performance comparisons
- Extended testing examples
- Advanced asyncio patterns

## 📚 Resources

### 📖 Official Documentation

- [Python Documentation](https://docs.python.org/3/)
- [Python Package Index (PyPI)](https://pypi.org/)
- [Python Enhancement Proposals (PEPs)](https://www.python.org/dev/peps/)

### 📚 Books and Tutorials

- "Effective Python" by Brett Slatkin
- "Fluent Python" by Luciano Ramalho
- "Python Tricks" by Dan Bader

### 🛠️ Tools and Libraries

- [pytest](https://docs.pytest.org/) - Testing framework
- [mypy](http://mypy-lang.org/) - Static type checker
- [black](https://black.readthedocs.io/) - Code formatter
- [Poetry](https://python-poetry.org/) - Dependency management

## 📜 License

This tutorial is released under the MIT License. Feel free to use, modify, and distribute as needed for educational purposes.

## 💬 Support

- Open an issue for questions or corrections
- Submit pull requests for improvements
- Share feedback on the learning experience

---

**Happy Python coding!** 🐍