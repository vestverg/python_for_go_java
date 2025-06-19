# 📦 Modules and Packages in Python

## 📖 Introduction

This section explores Python's module and package system, which provides a way to organize code into reusable components. Python's approach to modularity is more flexible than Java's package system and more structured than Go's package model, offering powerful features for code organization and distribution.

## Module Basics

### What is a Module?

A module in Python is simply a Python file containing Python definitions and statements. The file name is the module name with the suffix `.py` added.

```python
# math_utils.py
"""A simple math utilities module."""

import math
from typing import Union, List

PI = 3.14159265359

def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

def factorial(n: int) -> int:
    """Calculate factorial of n."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    return math.factorial(n)

class Calculator:
    """A simple calculator class."""
    
    def __init__(self) -> None:
        self.history: List[str] = []
    
    def calculate(self, expression: str) -> float:
        """Evaluate a mathematical expression."""
        try:
            result = eval(expression)
            self.history.append(f"{expression} = {result}")
            return result
        except Exception as e:
            raise ValueError(f"Invalid expression: {e}")
```

### Importing Modules

```python
# Different ways to import modules

# 1. Import entire module
import math_utils
result = math_utils.add(5, 3)

# 2. Import specific functions
from math_utils import add, multiply
result = add(5, 3)

# 3. Import with alias
import math_utils as mu
result = mu.add(5, 3)

# 4. Import specific items with alias
from math_utils import Calculator as Calc
calc = Calc()

# 5. Import all (not recommended)
from math_utils import *
```

### Module Search Path

Python searches for modules in the following order:

1. Current directory
2. PYTHONPATH environment variable directories
3. Standard library directories
4. Site-packages directory

```python
import sys

# View module search path
print(sys.path)

# Add custom path
sys.path.append('/path/to/custom/modules')

# View loaded modules
print(sys.modules.keys())
```

## Package Structure

### Creating Packages

A package is a directory containing an `__init__.py` file (can be empty) and other Python files or subdirectories.

```
mypackage/
    __init__.py
    core.py
    utils.py
    subpackage/
        __init__.py
        helpers.py
        advanced.py
```

### Package Initialization

```python
# mypackage/__init__.py
"""
MyPackage - A comprehensive Python package example.

This package demonstrates various packaging concepts including:
- Package initialization
- Subpackages
- Public APIs
- Version management
"""

from .core import DataProcessor, APIClient
from .utils import validate_email, format_date
from . import subpackage

__version__ = "1.0.0"
__author__ = "Python Tutorial"
__all__ = ["DataProcessor", "APIClient", "validate_email", "format_date"]

# Package-level initialization
def _initialize_package():
    """Initialize package-level settings."""
    import logging
    logging.getLogger(__name__).info("MyPackage initialized")

_initialize_package()
```

### Core Module

```python
# mypackage/core.py
"""Core functionality for mypackage."""

import json
import requests
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class APIResponse:
    """Response from API calls."""
    status_code: int
    data: Dict[str, Any]
    headers: Dict[str, str]
    success: bool = True
    error_message: Optional[str] = None


class DataProcessor(ABC):
    """Abstract base class for data processors."""
    
    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process data and return result."""
        pass
    
    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate input data."""
        pass


class JSONProcessor(DataProcessor):
    """JSON data processor implementation."""
    
    def process(self, data: str) -> Dict[str, Any]:
        """Process JSON string and return dictionary."""
        if not self.validate(data):
            raise ValueError("Invalid JSON data")
        return json.loads(data)
    
    def validate(self, data: str) -> bool:
        """Validate JSON string."""
        try:
            json.loads(data)
            return True
        except (json.JSONDecodeError, TypeError):
            return False


class APIClient:
    """Generic API client with common functionality."""
    
    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        headers: Optional[Dict[str, str]] = None
    ) -> None:
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.headers = headers or {}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """Make GET request to API."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.get(
                url,
                params=params,
                timeout=self.timeout
            )
            return APIResponse(
                status_code=response.status_code,
                data=response.json() if response.content else {},
                headers=dict(response.headers),
                success=response.ok
            )
        except requests.RequestException as e:
            return APIResponse(
                status_code=0,
                data={},
                headers={},
                success=False,
                error_message=str(e)
            )
    
    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """Make POST request to API."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.post(
                url,
                data=data,
                json=json_data,
                timeout=self.timeout
            )
            return APIResponse(
                status_code=response.status_code,
                data=response.json() if response.content else {},
                headers=dict(response.headers),
                success=response.ok
            )
        except requests.RequestException as e:
            return APIResponse(
                status_code=0,
                data={},
                headers={},
                success=False,
                error_message=str(e)
            )
```

### Utility Module

```python
# mypackage/utils.py
"""Utility functions for mypackage."""

import re
import datetime
from typing import Optional, Union, Any
from functools import wraps
import logging


# Module-level logger
logger = logging.getLogger(__name__)


def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if email is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def format_date(
    date: Union[datetime.datetime, datetime.date, str],
    format_string: str = "%Y-%m-%d"
) -> str:
    """
    Format date to string.
    
    Args:
        date: Date to format
        format_string: Format string
        
    Returns:
        Formatted date string
    """
    if isinstance(date, str):
        # Try to parse string date
        try:
            date = datetime.datetime.fromisoformat(date)
        except ValueError:
            raise ValueError(f"Cannot parse date string: {date}")
    
    if isinstance(date, datetime.date):
        date = datetime.datetime.combine(date, datetime.time())
    
    return date.strftime(format_string)


def retry(max_attempts: int = 3, delay: float = 1.0):
    """
    Decorator to retry function calls.
    
    Args:
        max_attempts: Maximum number of attempts
        delay: Delay between attempts in seconds
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(
                        f"Attempt {attempt + 1} failed for {func.__name__}: {e}"
                    )
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
            
            logger.error(f"All {max_attempts} attempts failed for {func.__name__}")
            raise last_exception
        
        return wrapper
    return decorator


def memoize(func):
    """
    Decorator to cache function results.
    
    Args:
        func: Function to memoize
    """
    cache = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Create cache key from arguments
        key = (args, tuple(sorted(kwargs.items())))
        
        if key not in cache:
            cache[key] = func(*args, **kwargs)
            logger.debug(f"Cached result for {func.__name__}")
        else:
            logger.debug(f"Retrieved cached result for {func.__name__}")
        
        return cache[key]
    
    # Add cache management methods
    wrapper.cache = cache
    wrapper.clear_cache = lambda: cache.clear()
    wrapper.cache_info = lambda: {
        'hits': len([k for k in cache.keys()]),
        'size': len(cache)
    }
    
    return wrapper


class ConfigManager:
    """Configuration manager for the package."""
    
    _instance = None
    _config = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self._config[key] = value
    
    def load_from_dict(self, config: dict) -> None:
        """Load configuration from dictionary."""
        self._config.update(config)
    
    def load_from_file(self, filepath: str) -> None:
        """Load configuration from JSON file."""
        import json
        with open(filepath, 'r') as f:
            config = json.load(f)
            self.load_from_dict(config)
```

### Subpackage

```python
# mypackage/subpackage/__init__.py
"""Subpackage with advanced functionality."""

from .helpers import StringHelper, NumberHelper
from .advanced import DataAnalyzer, AdvancedProcessor

__all__ = ["StringHelper", "NumberHelper", "DataAnalyzer", "AdvancedProcessor"]
```

```python
# mypackage/subpackage/helpers.py
"""Helper classes and functions."""

import string
import random
from typing import List, Union, Optional
from collections import Counter


class StringHelper:
    """Helper class for string operations."""
    
    @staticmethod
    def generate_random_string(
        length: int = 10,
        include_digits: bool = True,
        include_punctuation: bool = False
    ) -> str:
        """Generate random string."""
        chars = string.ascii_letters
        if include_digits:
            chars += string.digits
        if include_punctuation:
            chars += string.punctuation
        
        return ''.join(random.choice(chars) for _ in range(length))
    
    @staticmethod
    def camel_to_snake(text: str) -> str:
        """Convert CamelCase to snake_case."""
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    @staticmethod
    def snake_to_camel(text: str) -> str:
        """Convert snake_case to CamelCase."""
        components = text.split('_')
        return ''.join(word.capitalize() for word in components)
    
    @staticmethod
    def count_words(text: str) -> dict:
        """Count word frequencies in text."""
        words = text.lower().split()
        # Remove punctuation
        words = [''.join(c for c in word if c.isalnum()) for word in words]
        words = [word for word in words if word]  # Remove empty strings
        return dict(Counter(words))


class NumberHelper:
    """Helper class for number operations."""
    
    @staticmethod
    def is_prime(n: int) -> bool:
        """Check if number is prime."""
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    @staticmethod
    def fibonacci(n: int) -> List[int]:
        """Generate Fibonacci sequence up to n terms."""
        if n <= 0:
            return []
        elif n == 1:
            return [0]
        elif n == 2:
            return [0, 1]
        
        fib = [0, 1]
        for i in range(2, n):
            fib.append(fib[i-1] + fib[i-2])
        return fib
    
    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Calculate greatest common divisor."""
        while b:
            a, b = b, a % b
        return a
    
    @staticmethod
    def lcm(a: int, b: int) -> int:
        """Calculate least common multiple."""
        return abs(a * b) // NumberHelper.gcd(a, b)
    
    @staticmethod
    def prime_factors(n: int) -> List[int]:
        """Find prime factors of a number."""
        factors = []
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.append(d)
                n //= d
            d += 1
        if n > 1:
            factors.append(n)
        return factors
```

```python
# mypackage/subpackage/advanced.py
"""Advanced data processing functionality."""

import statistics
import json
from typing import List, Dict, Any, Optional, Union, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod
import numpy as np  # External dependency


@dataclass
class DataPoint:
    """Represents a single data point."""
    value: Union[int, float]
    timestamp: str
    category: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class AnalysisResult:
    """Result of data analysis."""
    mean: float
    median: float
    std_dev: float
    min_value: float
    max_value: float
    count: int
    outliers: List[float]
    summary: str


class DataAnalyzer:
    """Advanced data analysis functionality."""
    
    def __init__(self, outlier_threshold: float = 2.0) -> None:
        self.outlier_threshold = outlier_threshold
    
    def analyze_numeric_data(
        self,
        data: List[Union[int, float]]
    ) -> AnalysisResult:
        """Perform comprehensive analysis of numeric data."""
        if not data:
            raise ValueError("Data cannot be empty")
        
        # Basic statistics
        mean = statistics.mean(data)
        median = statistics.median(data)
        std_dev = statistics.stdev(data) if len(data) > 1 else 0.0
        min_value = min(data)
        max_value = max(data)
        count = len(data)
        
        # Find outliers using z-score
        outliers = []
        if std_dev > 0:
            for value in data:
                z_score = abs(value - mean) / std_dev
                if z_score > self.outlier_threshold:
                    outliers.append(value)
        
        # Generate summary
        summary = (
            f"Analysis of {count} data points: "
            f"mean={mean:.2f}, median={median:.2f}, "
            f"std_dev={std_dev:.2f}, outliers={len(outliers)}"
        )
        
        return AnalysisResult(
            mean=mean,
            median=median,
            std_dev=std_dev,
            min_value=min_value,
            max_value=max_value,
            count=count,
            outliers=outliers,
            summary=summary
        )
    
    def correlation_analysis(
        self,
        x_data: List[float],
        y_data: List[float]
    ) -> Tuple[float, str]:
        """Calculate correlation between two datasets."""
        if len(x_data) != len(y_data):
            raise ValueError("Datasets must have the same length")
        
        if len(x_data) < 2:
            raise ValueError("Need at least 2 data points")
        
        # Calculate Pearson correlation coefficient
        correlation = np.corrcoef(x_data, y_data)[0, 1]
        
        # Interpret correlation strength
        abs_corr = abs(correlation)
        if abs_corr >= 0.8:
            strength = "very strong"
        elif abs_corr >= 0.6:
            strength = "strong"
        elif abs_corr >= 0.4:
            strength = "moderate"
        elif abs_corr >= 0.2:
            strength = "weak"
        else:
            strength = "very weak"
        
        direction = "positive" if correlation > 0 else "negative"
        interpretation = f"{strength} {direction} correlation"
        
        return correlation, interpretation


class AdvancedProcessor:
    """Advanced data processing with multiple strategies."""
    
    def __init__(self) -> None:
        self.processors: Dict[str, Any] = {}
    
    def register_processor(
        self,
        name: str,
        processor: callable
    ) -> None:
        """Register a custom processor."""
        self.processors[name] = processor
    
    def process_batch(
        self,
        data: List[Any],
        processor_name: str,
        **kwargs
    ) -> List[Any]:
        """Process data in batches."""
        if processor_name not in self.processors:
            raise ValueError(f"Unknown processor: {processor_name}")
        
        processor = self.processors[processor_name]
        return [processor(item, **kwargs) for item in data]
    
    def chain_processors(
        self,
        data: Any,
        processor_chain: List[str],
        **kwargs
    ) -> Any:
        """Chain multiple processors together."""
        result = data
        for processor_name in processor_chain:
            if processor_name not in self.processors:
                raise ValueError(f"Unknown processor: {processor_name}")
            
            processor = self.processors[processor_name]
            result = processor(result, **kwargs)
        
        return result
    
    def parallel_process(
        self,
        data: List[Any],
        processor_name: str,
        workers: int = 4,
        **kwargs
    ) -> List[Any]:
        """Process data in parallel using multiple workers."""
        from concurrent.futures import ThreadPoolExecutor
        
        if processor_name not in self.processors:
            raise ValueError(f"Unknown processor: {processor_name}")
        
        processor = self.processors[processor_name]
        
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [
                executor.submit(processor, item, **kwargs)
                for item in data
            ]
            return [future.result() for future in futures]
```

## Package Configuration

### setup.py

```python
# setup.py
"""Setup script for mypackage."""

from setuptools import setup, find_packages
import pathlib

# Read README file
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

# Read requirements
with open("requirements.txt", "r") as f:
    requirements = [line.strip() for line in f if line.strip()]

setup(
    name="mypackage",
    version="1.0.0",
    description="A comprehensive Python package example",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/example/mypackage",
    author="Python Tutorial",
    author_email="tutorial@example.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "mypy>=0.900",
            "flake8>=3.8",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=0.5",
        ],
    },
    entry_points={
        "console_scripts": [
            "mypackage-cli=mypackage.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
```

### pyproject.toml

```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage"
description = "A comprehensive Python package example"
authors = [{name = "Python Tutorial", email = "tutorial@example.com"}]
license = {file = "LICENSE"}
readme = "README.md"
requires-python = ">=3.8"
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
dependencies = [
    "requests>=2.25.0",
    "numpy>=1.20.0",
]
dynamic = ["version"]

[project.optional-dependencies]
dev = [
    "pytest>=6.0",
    "pytest-cov>=2.0",
    "black>=21.0",
    "mypy>=0.900",
    "flake8>=3.8",
]
docs = [
    "sphinx>=4.0",
    "sphinx-rtd-theme>=0.5",
]

[project.scripts]
mypackage-cli = "mypackage.cli:main"

[tool.setuptools_scm]
write_to = "mypackage/_version.py"

[tool.black]
line-length = 88
target-version = ['py38']
include = '\.pyi?$'

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q --strict-markers --strict-config"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]

[tool.coverage.run]
source = ["mypackage"]
omit = ["*/tests/*", "*/test_*.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
    "class .*\bProtocol\):",
    "@(abc\\.)?abstractmethod",
]
```

## Best Practices

### 1. Package Structure

```python
# Good package structure
mypackage/
    __init__.py          # Package initialization
    core.py              # Core functionality
    utils.py             # Utility functions
    exceptions.py        # Custom exceptions
    constants.py         # Package constants
    config.py           # Configuration management
    cli.py              # Command line interface
    subpackage/
        __init__.py
        module1.py
        module2.py
    tests/
        __init__.py
        test_core.py
        test_utils.py
    docs/
        conf.py
        index.rst
    setup.py
    pyproject.toml
    requirements.txt
    README.md
    LICENSE
    MANIFEST.in
```

### 2. Import Best Practices

```python
# Explicit imports (preferred)
from mypackage.core import APIClient
from mypackage.utils import validate_email

# Relative imports within package
from .core import APIClient  # Same level
from ..utils import helper_function  # Parent level
from .subpackage.helpers import StringHelper  # Child level

# Avoid wildcard imports
from mypackage import *  # Don't do this

# Use __all__ to control what gets imported
__all__ = ["APIClient", "DataProcessor", "validate_email"]
```

### 3. Namespace Packages

```python
# PEP 420 namespace packages (no __init__.py required)
namespace_package/
    subpackage1/
        module1.py
    subpackage2/
        module2.py

# Traditional namespace package
namespace_package/
    __init__.py  # Contains: __path__ = __import__('pkgutil').extend_path(__path__, __name__)
    subpackage1/
        __init__.py
        module1.py
```

### 4. Version Management

```python
# mypackage/_version.py (generated by setuptools_scm)
__version__ = "1.0.0"

# mypackage/__init__.py
from ._version import __version__

# Or use importlib.metadata for Python 3.8+
try:
    from importlib.metadata import version
    __version__ = version("mypackage")
except ImportError:
    from importlib_metadata import version
    __version__ = version("mypackage")
```

## Testing Packages

### Test Structure

```python
# tests/test_core.py
"""Tests for core functionality."""

import pytest
from unittest.mock import Mock, patch
from mypackage.core import APIClient, JSONProcessor
from mypackage.exceptions import APIError


class TestAPIClient:
    """Test cases for APIClient."""
    
    @pytest.fixture
    def client(self) -> APIClient:
        """Fixture providing API client."""
        return APIClient("https://api.example.com")
    
    def test_client_initialization(self, client: APIClient) -> None:
        """Test client initialization."""
        assert client.base_url == "https://api.example.com"
        assert client.timeout == 30
    
    @patch('requests.Session.get')
    def test_get_request(self, mock_get: Mock, client: APIClient) -> None:
        """Test GET request."""
        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}
        mock_response.headers = {"Content-Type": "application/json"}
        mock_get.return_value = mock_response
        
        response = client.get("/users")
        
        assert response.success
        assert response.status_code == 200
        assert response.data == {"status": "success"}


class TestJSONProcessor:
    """Test cases for JSONProcessor."""
    
    @pytest.fixture
    def processor(self) -> JSONProcessor:
        """Fixture providing JSON processor."""
        return JSONProcessor()
    
    def test_valid_json_processing(self, processor: JSONProcessor) -> None:
        """Test processing valid JSON."""
        json_str = '{"name": "test", "value": 123}'
        result = processor.process(json_str)
        assert result == {"name": "test", "value": 123}
    
    def test_invalid_json_processing(self, processor: JSONProcessor) -> None:
        """Test processing invalid JSON."""
        json_str = '{"name": "test", "value": }'
        with pytest.raises(ValueError):
            processor.process(json_str)
```

### Integration Tests

```python
# tests/test_integration.py
"""Integration tests for mypackage."""

import pytest
import tempfile
import json
from mypackage import APIClient, ConfigManager
from mypackage.utils import validate_email, format_date


@pytest.mark.integration
class TestPackageIntegration:
    """Integration tests for the entire package."""
    
    def test_config_and_api_integration(self) -> None:
        """Test configuration and API client integration."""
        # Create temporary config file
        config_data = {
            "api_base_url": "https://api.example.com",
            "timeout": 60,
            "retry_attempts": 3
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        # Load configuration
        config = ConfigManager()
        config.load_from_file(config_file)
        
        # Create API client with config
        client = APIClient(
            base_url=config.get("api_base_url"),
            timeout=config.get("timeout", 30)
        )
        
        assert client.base_url == "https://api.example.com"
        assert client.timeout == 60
    
    def test_utility_functions_integration(self) -> None:
        """Test utility functions work together."""
        from datetime import datetime
        
        # Test email validation
        valid_email = "test@example.com"
        assert validate_email(valid_email)
        
        # Test date formatting
        now = datetime.now()
        formatted = format_date(now, "%Y-%m-%d %H:%M")
        assert len(formatted) > 10
```

## Distribution and Publishing

### Building and Publishing

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Check package
twine check dist/*

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

### GitHub Actions CI/CD

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10", "3.11"]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[dev]
    
    - name: Lint with flake8
      run: |
        flake8 mypackage tests
    
    - name: Type check with mypy
      run: |
        mypy mypackage
    
    - name: Test with pytest
      run: |
        pytest --cov=mypackage --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## Comparison with Java and Go

### Java Packages vs Python Modules

| Feature | Java | Python |
|---------|------|---------|
| **Package Declaration** | `package com.example.mypackage;` | Directory structure with `__init__.py` |
| **Import Statement** | `import com.example.MyClass;` | `from mypackage import MyClass` |
| **Access Control** | `public`, `private`, `protected` | Convention-based (`_private`, `__private`) |
| **Classpath** | JAR files, classpath | `sys.path`, site-packages |
| **Namespace** | Hierarchical, reverse domain | Flat, based on directory structure |

### Go Packages vs Python Modules

| Feature | Go | Python |
|---------|-----|---------|
| **Package Definition** | `package main` | Directory with `__init__.py` |
| **Import Statement** | `import "fmt"` | `import sys` |
| **Visibility** | Capitalized = exported | `__all__` or convention |
| **Dependency Management** | `go.mod`, `go.sum` | `requirements.txt`, `pyproject.toml` |
| **Module System** | Built-in module system | Import system with `sys.path` |

## Advanced Topics

### 1. Lazy Loading

```python
# Lazy loading of heavy modules
def _import_heavy_module():
    """Import heavy module only when needed."""
    global heavy_module
    if 'heavy_module' not in globals():
        import heavy_computation_module as heavy_module
    return heavy_module

def expensive_operation(data):
    """Use heavy module only when this function is called."""
    heavy = _import_heavy_module()
    return heavy.process(data)
```

### 2. Plugin Architecture

```python
# Plugin system using entry points
# setup.py
entry_points={
    'mypackage.plugins': [
        'csv_processor = mypackage_csv:CSVProcessor',
        'xml_processor = mypackage_xml:XMLProcessor',
    ]
}

# Loading plugins
import pkg_resources

def load_plugins():
    """Load all available plugins."""
    plugins = {}
    for entry_point in pkg_resources.iter_entry_points('mypackage.plugins'):
        plugins[entry_point.name] = entry_point.load()
    return plugins
```

### 3. Extension Modules

```python
# C extension module wrapper
try:
    from ._c_extensions import fast_algorithm
except ImportError:
    # Fallback to pure Python implementation
    def fast_algorithm(data):
        """Pure Python fallback."""
        return slow_python_algorithm(data)
```

## Additional Resources

1. **Official Documentation**
   - [Python Modules](https://docs.python.org/3/tutorial/modules.html)
   - [Python Packages](https://docs.python.org/3/tutorial/modules.html#packages)
   - [Packaging Python Projects](https://packaging.python.org/)

2. **PEPs**
   - [PEP 8 – Style Guide](https://www.python.org/dev/peps/pep-0008/)
   - [PEP 420 – Namespace Packages](https://www.python.org/dev/peps/pep-0420/)
   - [PEP 518 – Build System Requirements](https://www.python.org/dev/peps/pep-0518/)

3. **Tools and Resources**
   - [setuptools Documentation](https://setuptools.pypa.io/)
   - [pytest Documentation](https://docs.pytest.org/)
   - [Python Package Index (PyPI)](https://pypi.org/)
   - [TestPyPI](https://test.pypi.org/) 