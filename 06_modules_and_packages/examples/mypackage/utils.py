"""
Utility functions for the mypackage package.
"""

from typing import List, Any
import json


def validate_input(data: List[Any]) -> bool:
    """
    Validate input data.
    
    Args:
        data: List of data items to validate
    
    Returns:
        bool: True if data is valid, False otherwise
    """
    if not isinstance(data, list):
        return False
    
    if not data:  # Empty list is invalid
        return False
    
    return all(isinstance(item, (str, int, float, dict)) for item in data)


def format_output(data: List[Any]) -> List[Any]:
    """
    Format output data.
    
    Args:
        data: List of processed data items
    
    Returns:
        List[Any]: Formatted data
    """
    formatted = []
    for item in data:
        if isinstance(item, dict):
            # Convert dict to JSON string
            formatted.append(json.dumps(item))
        else:
            # Convert to string
            formatted.append(str(item))
    return formatted


def debug_print(message: str, level: str = "INFO") -> None:
    """
    Print debug messages.
    
    Args:
        message: Debug message
        level: Debug level (INFO, WARNING, ERROR)
    """
    print(f"[{level}] {message}") 