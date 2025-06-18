"""
Validation utilities for common data types.
"""

import re
from typing import Optional

def validate_email(email: str) -> bool:
    """
    Validate an email address.
    
    Args:
        email: The email address to validate
        
    Returns:
        True if the email is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """
    Validate a phone number.
    
    Args:
        phone: The phone number to validate
        
    Returns:
        True if the phone number is valid, False otherwise
    """
    # Simple validation for demonstration
    pattern = r'^\+?1?\d{9,15}$'
    return bool(re.match(pattern, phone))

def sanitize_email(email: str) -> Optional[str]:
    """
    Sanitize and validate an email address.
    
    Args:
        email: The email address to sanitize
        
    Returns:
        The sanitized email address if valid, None otherwise
    """
    email = email.strip().lower()
    return email if validate_email(email) else None

def sanitize_phone(phone: str) -> Optional[str]:
    """
    Sanitize and validate a phone number.
    
    Args:
        phone: The phone number to sanitize
        
    Returns:
        The sanitized phone number if valid, None otherwise
    """
    # Remove all non-digit characters except +
    phone = ''.join(c for c in phone if c.isdigit() or c == '+')
    return phone if validate_phone(phone) else None 