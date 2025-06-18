# Python Modules and Packages

This section covers Python's module and package system, with comparisons to Java and Go.

## Module Basics

### Simple Module

```python
# math_utils.py
def add(x: int, y: int) -> int:
    return x + y

def multiply(x: int, y: int) -> int:
    return x * y

PI = 3.14159
```

### Importing Modules

```python
# Different ways to import
import math_utils
from math_utils import add, multiply
from math_utils import PI as MY_PI
```

## Package Structure

### Basic Package Structure

```
my_package/
├── __init__.py
├── module1.py
├── module2.py
└── subpackage/
    ├── __init__.py
    └── module3.py
```

### Package Initialization

```python
# __init__.py
from .module1 import function1
from .module2 import function2

__all__ = ['function1', 'function2']
```

## Import System

### Absolute vs Relative Imports

```python
# Absolute imports
from my_package.module1 import function1
from my_package.subpackage.module3 import function3

# Relative imports
from .module1 import function1
from ..module2 import function2
```

### Import Resolution

1. Built-in modules
2. Modules in PYTHONPATH
3. Modules in current directory

## Package Distribution

### setup.py

```python
from setuptools import setup, find_packages

setup(
    name="my_package",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'pandas>=1.2.0'
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A short description",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/my_package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)
```

### requirements.txt

```
requests>=2.25.1
pandas>=1.2.0
numpy>=1.19.2
```

## Namespace Packages

```
project/
├── pkg.db/
│   └── db.py
└── pkg.api/
    └── api.py
```

```python
# Using namespace packages
from pkg.db import Database
from pkg.api import APIClient
```

## Module vs Package Comparison

### Python vs Java

```python
# Python
from mypackage.subpackage import module

# Java
import com.example.mypackage.subpackage.Module;
```

### Python vs Go

```python
# Python
from mypackage.utils import helper

# Go
import "github.com/user/project/pkg/utils"
```

## Virtual Environments

### Creating Virtual Environments

```bash
# Create virtual environment
python -m venv myenv

# Activate (Unix)
source myenv/bin/activate

# Activate (Windows)
myenv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

## Best Practices

1. Use `__init__.py` to define package interface
2. Prefer absolute imports over relative
3. Keep modules focused and single-purpose
4. Use virtual environments for isolation
5. Document dependencies in requirements.txt

## Example Package Structure

```
my_project/
├── README.md
├── setup.py
├── requirements.txt
├── my_package/
│   ├── __init__.py
│   ├── core.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── helpers.py
│   │   └── validators.py
│   └── api/
│       ├── __init__.py
│       ├── client.py
│       └── models.py
└── tests/
    ├── __init__.py
    ├── test_core.py
    └── test_utils.py
```

## Next Steps

1. Create a simple package
2. Practice importing modules
3. Set up virtual environments
4. Move on to the Concurrency section 

# Example Package

This package demonstrates Python's module and package system, with a focus on modern Python features and best practices.

## Features

- Email and phone number validation
- REST API client with type hints
- Pydantic models for data validation
- Modern Python packaging

## Installation

```bash
pip install -e .
```

## Usage

### Validation

```python
from example_package.utils import validate_email, validate_phone

# Validate email
is_valid = validate_email("user@example.com")

# Validate phone
is_valid = validate_phone("+1234567890")
```

### API Client

```python
from example_package.api import APIClient, User, Post

# Create API client
client = APIClient("https://api.example.com", api_key="your-api-key")

# Get user
user = client.get_user(1)
print(f"User: {user.username}")

# Create post
post = client.create_post(
    PostCreate(
        title="Hello World",
        content="My first post",
        tags=["python", "tutorial"]
    ),
    author_id=1
)
```

## Development

### Setup

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Unix
   venv\Scripts\activate     # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Tests

```bash
pytest tests/
```

## Project Structure

```
example_package/
├── __init__.py          # Package initialization
├── utils/
│   ├── __init__.py     # Utils package
│   └── validators.py    # Validation functions
└── api/
    ├── __init__.py     # API package
    ├── client.py       # API client
    └── models.py       # Pydantic models
```

## Dependencies

- Python >= 3.10
- requests >= 2.31.0
- pydantic >= 2.5.0

## License

MIT License 