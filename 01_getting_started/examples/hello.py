#!/usr/bin/env python3

"""
This is a simple Python program demonstrating basic syntax.
Python uses docstrings (triple quotes) for module and function documentation.
"""

def main():
    # In Python, we don't need to declare variable types
    message = "Hello, Python!"
    
    # Simple print statement (no System.out.println or fmt.Println needed)
    print(message)
    
    # Demonstrate some basic Python features
    # List (similar to ArrayList in Java or slice in Go)
    languages = ["Python", "Java", "Go"]
    
    # For loop with enumeration (similar to for i, v := range slice in Go)
    for i, lang in enumerate(languages):
        print(f"{i + 1}. {lang}")  # f-strings for string formatting (Python 3.6+)

# This is Python's equivalent to Java's public static void main(String[] args)
# or Go's func main()
if __name__ == "__main__":
    main() 