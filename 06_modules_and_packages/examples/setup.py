"""
Setup configuration for mypackage.
"""

from setuptools import setup, find_packages

setup(
    name="mypackage",
    version="0.1.0",
    description="A sample package demonstrating Python's module system",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[],  # No external dependencies for this example
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
) 