from setuptools import setup, find_packages

setup(
    name="example_package",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'requests>=2.31.0',
        'pydantic>=2.5.0'
    ],
    author="Python Tutorial",
    author_email="tutorial@example.com",
    description="Example package for Python tutorial",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/example_package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10'
) 