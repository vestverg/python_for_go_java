"""
Example package demonstrating Python's module system.
"""

from .utils.validators import validate_email, validate_phone
from .api.client import APIClient
from .api.models import User, Post

__version__ = "0.1.0"
__all__ = ['validate_email', 'validate_phone', 'APIClient', 'User', 'Post'] 