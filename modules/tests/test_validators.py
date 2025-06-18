"""
Tests for the validators module.
"""

import pytest
from example_package.utils import validate_email, validate_phone, sanitize_email, sanitize_phone

# Email validation tests
@pytest.mark.parametrize("email,expected", [
    ("user@example.com", True),
    ("user.name@example.co.uk", True),
    ("user+tag@example.com", True),
    ("invalid.email", False),
    ("@example.com", False),
    ("user@.com", False),
    ("user@example.", False),
    ("", False),
])
def test_validate_email(email: str, expected: bool):
    """Test email validation with various cases."""
    assert validate_email(email) == expected

# Phone validation tests
@pytest.mark.parametrize("phone,expected", [
    ("+1234567890", True),
    ("1234567890", True),
    ("+44123456789", True),
    ("123", False),
    ("abc", False),
    ("", False),
])
def test_validate_phone(phone: str, expected: bool):
    """Test phone validation with various cases."""
    assert validate_phone(phone) == expected

# Email sanitization tests
@pytest.mark.parametrize("email,expected", [
    ("User@Example.COM", "user@example.com"),
    ("  user@example.com  ", "user@example.com"),
    ("invalid.email", None),
    ("", None),
])
def test_sanitize_email(email: str, expected: str | None):
    """Test email sanitization with various cases."""
    assert sanitize_email(email) == expected

# Phone sanitization tests
@pytest.mark.parametrize("phone,expected", [
    ("+1-234-567-890", "+1234567890"),
    ("(123) 456-7890", "1234567890"),
    ("123.456.7890", "1234567890"),
    ("abc", None),
    ("", None),
])
def test_sanitize_phone(phone: str, expected: str | None):
    """Test phone sanitization with various cases."""
    assert sanitize_phone(phone) == expected

def test_validate_email_type_error():
    """Test that validate_email raises TypeError for non-string input."""
    with pytest.raises(AttributeError):
        validate_email(123)

def test_validate_phone_type_error():
    """Test that validate_phone raises TypeError for non-string input."""
    with pytest.raises(AttributeError):
        validate_phone(123) 