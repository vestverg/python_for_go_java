"""
Utility functions for the mypackage package.
"""

import re
from datetime import datetime


def validate_email(email: str) -> bool:
    """Validate an email address."""
    if not isinstance(email, str):
        return False
    # A simple regex for email validation
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def format_date(dt: datetime) -> str:
    """Format a datetime object into a string."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")