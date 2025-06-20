"""
Core functionality for the mypackage package.
"""

from typing import List, Dict, Any, Optional
import json


class JSONProcessor:
    """Class for processing JSON data"""

    def validate(self, data: str) -> bool:
        """Validate if the string is valid JSON."""
        try:
            json.loads(data)
            return True
        except json.JSONDecodeError:
            return False

    def process(self, data: str) -> Dict[str, Any]:
        """Process a JSON string into a dictionary."""
        if not self.validate(data):
            raise ValueError("Invalid JSON data")
        return json.loads(data)


class APIClient:
    """A simple client for interacting with an API."""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, endpoint: str) -> Dict[str, Any]:
        """Simulates a GET request."""
        print(f"GET {self.base_url}/{endpoint}")
        return {"status": "success"}

    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulates a POST request."""
        print(f"POST {self.base_url}/{endpoint} with data: {data}")
        return {"status": "success", "data": data}