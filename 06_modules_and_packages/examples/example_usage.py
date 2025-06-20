#!/usr/bin/env python3

"""
Example usage of mypackage.
"""

from mypackage.core import JSONProcessor, APIClient
from mypackage.utils import validate_email, format_date
from datetime import datetime


def demonstrate_package_usage():
    """Demonstrates usage of the mypackage module."""
    # Demonstrate JSONProcessor
    json_processor = JSONProcessor()
    valid_json = '{"name": "test", "value": 123}'
    invalid_json = '{"name": "test", "value":}'
    
    print(f"Validating valid JSON: {json_processor.validate(valid_json)}")
    print(f"Validating invalid JSON: {json_processor.validate(invalid_json)}")
    print(f"Processing valid JSON: {json_processor.process(valid_json)}")
    
    # Demonstrate APIClient
    api_client = APIClient("https://api.example.com")
    api_client.get("test")
    
    # Demonstrate utils
    print(f"Validating email 'test@example.com': {validate_email('test@example.com')}")
    print(f"Formatting date: {format_date(datetime.now())}")


if __name__ == "__main__":
    demonstrate_package_usage() 