"""
Initialization file for the mypackage package.

This file makes the core components of the package available for import.
"""

from .core import JSONProcessor, APIClient
from . import utils

# Version information
__version__ = "0.1.0"
__author__ = "Your Name"

# Control what gets imported with 'from mypackage import *'
__all__ = ['JSONProcessor', 'APIClient', 'utils']