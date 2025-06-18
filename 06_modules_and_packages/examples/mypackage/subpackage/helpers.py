"""
Helper functions for data processing.
"""

from typing import Any, Dict
import json


def helper_function(item: Any) -> Any:
    """
    Process a single data item.
    
    Args:
        item: Data item to process
    
    Returns:
        Processed data item
    """
    if isinstance(item, dict):
        return _process_dict(item)
    elif isinstance(item, (int, float)):
        return _process_number(item)
    elif isinstance(item, str):
        return _process_string(item)
    else:
        raise ValueError(f"Unsupported data type: {type(item)}")


def _process_dict(data: Dict) -> Dict:
    """Process a dictionary item"""
    # Add metadata
    result = data.copy()
    result['_processed'] = True
    result['_type'] = 'dict'
    return result


def _process_number(num: float) -> Dict:
    """Process a numeric item"""
    return {
        'value': num,
        'squared': num ** 2,
        '_type': 'number'
    }


def _process_string(text: str) -> Dict:
    """Process a string item"""
    return {
        'value': text,
        'length': len(text),
        'upper': text.upper(),
        '_type': 'string'
    } 