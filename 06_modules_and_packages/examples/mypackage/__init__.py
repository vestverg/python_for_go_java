"""
MyPackage - A sample package demonstrating Python's module system.
"""

from .core import process_data, DataProcessor
from .utils import format_output, validate_input

# Version information
__version__ = "0.1.0"
__author__ = "Your Name"

# Control what gets imported with 'from mypackage import *'
__all__ = ['process_data', 'DataProcessor', 'format_output', 'validate_input'] 