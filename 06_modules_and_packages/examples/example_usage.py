#!/usr/bin/env python3

"""
Example usage of mypackage.
"""

from mypackage import process_data, DataProcessor
from mypackage.utils import debug_print


def main():
    # Example data
    data = [
        "Hello, World!",
        42,
        {"name": "Alice", "age": 30},
        3.14
    ]
    
    # Using the convenience function
    debug_print("Processing data using convenience function...")
    result1 = process_data(data)
    print("\nResults from process_data():")
    for item in result1:
        print(f"- {item}")
    
    # Using the class directly
    debug_print("\nProcessing data using DataProcessor class...")
    processor = DataProcessor({"debug": True})
    result2 = processor.process(data)
    print("\nResults from DataProcessor:")
    for item in result2:
        print(f"- {item}")
    
    # Example with invalid data
    debug_print("\nTrying to process invalid data...", "WARNING")
    try:
        process_data(None)
    except ValueError as e:
        debug_print(f"Error: {e}", "ERROR")


if __name__ == "__main__":
    main() 