#!/bin/bash

# create_project.sh - Python Project Creation Script
# This script creates a complete Python project structure with virtual environment
# Usage: ./create_project.sh <project_name> [python_version]

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to get Python version
get_python_version() {
    local python_cmd="$1"
    if command_exists "$python_cmd"; then
        "$python_cmd" --version 2>&1 | cut -d' ' -f2
    else
        echo "not found"
    fi
}

# Main function
main() {
    # Check arguments
    if [ $# -lt 1 ]; then
        print_error "Usage: $0 <project_name> [python_version]"
        print_error "Examples:"
        print_error "  $0 myproject"
        print_error "  $0 myproject 3.10"
        exit 1
    fi

    PROJECT_NAME="$1"
    PYTHON_VERSION="${2:-3}"

    # Validate project name
    if [[ ! "$PROJECT_NAME" =~ ^[a-zA-Z][a-zA-Z0-9_-]*$ ]]; then
        print_error "Invalid project name. Use only letters, numbers, underscores, and hyphens."
        print_error "Project name must start with a letter."
        exit 1
    fi

    # Check if project directory already exists
    if [ -d "$PROJECT_NAME" ]; then
        print_error "Directory '$PROJECT_NAME' already exists!"
        exit 1
    fi

    print_status "Creating Python project: $PROJECT_NAME"

    # Determine Python command
    PYTHON_CMD=""
    if [ "$PYTHON_VERSION" = "3" ]; then
        if command_exists python3; then
            PYTHON_CMD="python3"
        elif command_exists python; then
            # Check if it's Python 3
            PYTHON_VER=$(python --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1)
            if [ "$PYTHON_VER" = "3" ]; then
                PYTHON_CMD="python"
            fi
        fi
    else
        # Try specific version
        if command_exists "python$PYTHON_VERSION"; then
            PYTHON_CMD="python$PYTHON_VERSION"
        elif command_exists "python3.$PYTHON_VERSION"; then
            PYTHON_CMD="python3.$PYTHON_VERSION"
        fi
    fi

    if [ -z "$PYTHON_CMD" ]; then
        print_error "Python $PYTHON_VERSION not found!"
        print_error "Available Python versions:"
        for cmd in python python3 python3.8 python3.9 python3.10 python3.11; do
            if command_exists "$cmd"; then
                VERSION=$(get_python_version "$cmd")
                echo "  $cmd -> $VERSION"
            fi
        done
        exit 1
    fi

    DETECTED_VERSION=$(get_python_version "$PYTHON_CMD")
    print_status "Using Python $DETECTED_VERSION ($PYTHON_CMD)"

    # Create project directory
    print_status "Creating project structure..."
    mkdir -p "$PROJECT_NAME"
    cd "$PROJECT_NAME"

    # Create virtual environment
    print_status "Creating virtual environment..."
    "$PYTHON_CMD" -m venv venv

    # Activate virtual environment (for script purposes)
    source venv/bin/activate

    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip

    # Create directory structure
    print_status "Creating directory structure..."
    mkdir -p src/"$PROJECT_NAME"
    mkdir -p tests
    mkdir -p docs
    mkdir -p scripts

    # Create __init__.py files
    touch src/"$PROJECT_NAME"/__init__.py
    touch tests/__init__.py

    # Create main.py
    cat > src/"$PROJECT_NAME"/main.py << EOF
"""
Main module for $PROJECT_NAME.

This is the entry point for your application.
"""

def main() -> None:
    """Main function."""
    print("Hello from $PROJECT_NAME!")

if __name__ == "__main__":
    main()
EOF

    # Create requirements.txt
    cat > requirements.txt << EOF
# Production dependencies
# Add your project dependencies here
# Example: requests>=2.28.0
EOF

    # Create requirements-dev.txt
    cat > requirements-dev.txt << EOF
-r requirements.txt

# Development dependencies
pytest>=7.2.0
pytest-cov>=4.0.0
black>=22.12.0
mypy>=0.991
flake8>=6.0.0
isort>=5.11.0
pre-commit>=2.20.0
EOF

    # Create .gitignore
    cat > .gitignore << 'EOF'
# Virtual Environment
venv/
env/
ENV/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Testing
.coverage
.pytest_cache/
htmlcov/
.tox/
.nox/

# Type checking
.mypy_cache/
.dmypy.json
dmypy.json

# Environments
.env
.env.local
.env.development
.env.test
.env.production
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/

# Database
*.db
*.sqlite3

# Documentation
docs/_build/
EOF

    # Create .env.example
    cat > .env.example << EOF
# Environment Variables Template
# Copy this file to .env and update with your actual values

# Development settings
DEBUG=True
LOG_LEVEL=DEBUG

# Database (example)
# DATABASE_URL=sqlite:///db.sqlite3

# API Keys (example)
# API_KEY=your_api_key_here
# SECRET_KEY=your_secret_key_here
EOF

    # Create pyproject.toml
    cat > pyproject.toml << EOF
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "$PROJECT_NAME"
version = "0.1.0"
description = "A Python project"
readme = "README.md"
requires-python = ">=$DETECTED_VERSION"
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7.2.0",
    "pytest-cov>=4.0.0",
    "black>=22.12.0",
    "mypy>=0.991",
    "flake8>=6.0.0",
    "isort>=5.11.0",
    "pre-commit>=2.20.0",
]

[project.scripts]
$PROJECT_NAME = "$PROJECT_NAME.main:main"

[tool.black]
line-length = 88
target-version = ['py38']
include = '\.pyi?$'

[tool.isort]
profile = "black"
multi_line_output = 3

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --cov=src --cov-report=html --cov-report=term"

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
]
EOF

    # Create README.md
    cat > README.md << EOF
# $PROJECT_NAME

A Python project created with the Python tutorial project generator.

## Setup

### Prerequisites

- Python $DETECTED_VERSION or higher
- pip

### Installation

1. Clone this repository or download the project files
2. Navigate to the project directory:
   \`\`\`bash
   cd $PROJECT_NAME
   \`\`\`

3. Create and activate a virtual environment:
   \`\`\`bash
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\\Scripts\\activate
   \`\`\`

4. Install dependencies:
   \`\`\`bash
   # Production dependencies
   pip install -r requirements.txt
   
   # Development dependencies (for testing, linting, etc.)
   pip install -r requirements-dev.txt
   \`\`\`

### Usage

Run the main application:
\`\`\`bash
python -m src.$PROJECT_NAME.main
\`\`\`

Or using the installed script (after installing with pip):
\`\`\`bash
$PROJECT_NAME
\`\`\`

### Development

#### Running Tests

\`\`\`bash
pytest
\`\`\`

#### Code Formatting

\`\`\`bash
# Format code
black src tests

# Sort imports
isort src tests
\`\`\`

#### Linting

\`\`\`bash
# Type checking
mypy src

# Style checking
flake8 src tests
\`\`\`

#### Pre-commit Hooks

Set up pre-commit hooks to automatically run checks:

\`\`\`bash
pre-commit install
\`\`\`

## Project Structure

\`\`\`
$PROJECT_NAME/
├── src/$PROJECT_NAME/          # Main package
│   ├── __init__.py
│   └── main.py
├── tests/                      # Test files
│   └── __init__.py
├── docs/                       # Documentation
├── scripts/                    # Utility scripts
├── venv/                       # Virtual environment (not in git)
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── pyproject.toml             # Project configuration
├── .gitignore                 # Git ignore file
├── .env.example               # Environment variables template
└── README.md                  # This file
\`\`\`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
EOF

    # Create a simple test
    cat > tests/test_main.py << EOF
"""
Tests for the main module.
"""

from src.$PROJECT_NAME.main import main


def test_main():
    """Test the main function runs without error."""
    # This is a placeholder test
    try:
        main()
        assert True
    except Exception:
        assert False, "main() should not raise an exception"
EOF

    # Create activation script
    cat > scripts/activate.sh << 'EOF'
#!/bin/bash
# Activation script with environment setup

# Check if we're in the project directory
if [ ! -f "pyproject.toml" ]; then
    echo "Error: Not in project root directory"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Set PYTHONPATH to include src directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Load environment variables if .env exists
if [ -f ".env" ]; then
    set -a
    source .env
    set +a
    echo "Loaded environment variables from .env"
fi

echo "Virtual environment activated!"
echo "Python version: $(python --version)"
echo "Project: $(basename $(pwd))"
echo ""
echo "To deactivate: deactivate"
echo "To run tests: pytest"
echo "To format code: black src tests"
EOF

    chmod +x scripts/activate.sh

    # Create Windows activation script
    cat > scripts/activate.bat << 'EOF'
@echo off
REM Activation script for Windows

REM Check if we're in the project directory
if not exist pyproject.toml (
    echo Error: Not in project root directory
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Set PYTHONPATH to include src directory
set PYTHONPATH=%PYTHONPATH%;%CD%\src

REM Load environment variables if .env exists
if exist .env (
    for /f "delims=" %%x in (.env) do (set "%%x")
    echo Loaded environment variables from .env
)

echo Virtual environment activated!
python --version
echo Project: %CD%
echo.
echo To deactivate: deactivate
echo To run tests: pytest
echo To format code: black src tests
EOF

    # Install development dependencies
    print_status "Installing development dependencies..."
    pip install -r requirements-dev.txt

    # Initialize git repository
    if command_exists git; then
        print_status "Initializing git repository..."
        git init
        git add .
        git commit -m "Initial commit: Project structure created"
    else
        print_warning "Git not found. Skipping repository initialization."
    fi

    # Deactivate virtual environment
    deactivate

    print_success "Project '$PROJECT_NAME' created successfully!"
    echo
    print_status "Next steps:"
    echo "  1. cd $PROJECT_NAME"
    echo "  2. source venv/bin/activate  (or use scripts/activate.sh)"
    echo "  3. Edit src/$PROJECT_NAME/main.py to add your code"
    echo "  4. Add dependencies to requirements.txt"
    echo "  5. Run tests with: pytest"
    echo
    print_status "Quick start:"
    echo "  cd $PROJECT_NAME && source venv/bin/activate && python -m src.$PROJECT_NAME.main"
}

# Run main function
main "$@" 