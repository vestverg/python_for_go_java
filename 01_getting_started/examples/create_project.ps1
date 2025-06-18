# create_project.ps1 - Python Project Creation Script for Windows
# This script creates a complete Python project structure with virtual environment
# Usage: .\create_project.ps1 <project_name> [python_version]

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectName,
    
    [Parameter(Mandatory=$false)]
    [string]$PythonVersion = "3"
)

# Function to write colored output
function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Function to check if command exists
function Test-Command {
    param([string]$CommandName)
    return (Get-Command $CommandName -ErrorAction SilentlyContinue) -ne $null
}

# Function to get Python version
function Get-PythonVersion {
    param([string]$PythonCmd)
    try {
        if (Test-Command $PythonCmd) {
            $versionOutput = & $PythonCmd --version 2>&1
            return $versionOutput.ToString().Split(' ')[1]
        }
        return "not found"
    }
    catch {
        return "not found"
    }
}

# Validate project name
if ($ProjectName -notmatch "^[a-zA-Z][a-zA-Z0-9_-]*$") {
    Write-Error "Invalid project name. Use only letters, numbers, underscores, and hyphens."
    Write-Error "Project name must start with a letter."
    exit 1
}

# Check if project directory already exists
if (Test-Path $ProjectName) {
    Write-Error "Directory '$ProjectName' already exists!"
    exit 1
}

Write-Status "Creating Python project: $ProjectName"

# Determine Python command
$PythonCmd = ""
if ($PythonVersion -eq "3") {
    if (Test-Command "python") {
        # Check if it's Python 3
        $version = Get-PythonVersion "python"
        if ($version -like "3.*") {
            $PythonCmd = "python"
        }
    }
    elseif (Test-Command "py") {
        # Try Python launcher
        $PythonCmd = "py"
    }
    elseif (Test-Command "python3") {
        $PythonCmd = "python3"
    }
}
else {
    # Try specific version
    if (Test-Command "python$PythonVersion") {
        $PythonCmd = "python$PythonVersion"
    }
    elseif (Test-Command "py") {
        # Try Python launcher with version
        $PythonCmd = "py -$PythonVersion"
    }
}

if ($PythonCmd -eq "") {
    Write-Error "Python $PythonVersion not found!"
    Write-Error "Available Python versions:"
    
    $pythonCommands = @("python", "py", "python3")
    foreach ($cmd in $pythonCommands) {
        if (Test-Command $cmd) {
            $version = Get-PythonVersion $cmd
            Write-Host "  $cmd -> $version"
        }
    }
    exit 1
}

$DetectedVersion = Get-PythonVersion $PythonCmd.Split(' ')[0]
Write-Status "Using Python $DetectedVersion ($PythonCmd)"

# Create project directory
Write-Status "Creating project structure..."
New-Item -ItemType Directory -Path $ProjectName | Out-Null
Set-Location $ProjectName

# Create virtual environment
Write-Status "Creating virtual environment..."
if ($PythonCmd -like "py *") {
    & py -m venv venv
} else {
    & $PythonCmd -m venv venv
}

# Activate virtual environment
Write-Status "Activating virtual environment..."
& "venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Status "Upgrading pip..."
python -m pip install --upgrade pip

# Create directory structure
Write-Status "Creating directory structure..."
New-Item -ItemType Directory -Path "src\$ProjectName" -Force | Out-Null
New-Item -ItemType Directory -Path "tests" -Force | Out-Null
New-Item -ItemType Directory -Path "docs" -Force | Out-Null
New-Item -ItemType Directory -Path "scripts" -Force | Out-Null

# Create __init__.py files
New-Item -ItemType File -Path "src\$ProjectName\__init__.py" | Out-Null
New-Item -ItemType File -Path "tests\__init__.py" | Out-Null

# Create main.py
$mainPyContent = @"
"""
Main module for $ProjectName.

This is the entry point for your application.
"""

def main() -> None:
    """Main function."""
    print("Hello from $ProjectName!")

if __name__ == "__main__":
    main()
"@
Set-Content -Path "src\$ProjectName\main.py" -Value $mainPyContent

# Create requirements.txt
$requirementsContent = @"
# Production dependencies
# Add your project dependencies here
# Example: requests>=2.28.0
"@
Set-Content -Path "requirements.txt" -Value $requirementsContent

# Create requirements-dev.txt
$devRequirementsContent = @"
-r requirements.txt

# Development dependencies
pytest>=7.2.0
pytest-cov>=4.0.0
black>=22.12.0
mypy>=0.991
flake8>=6.0.0
isort>=5.11.0
pre-commit>=2.20.0
"@
Set-Content -Path "requirements-dev.txt" -Value $devRequirementsContent

# Create .gitignore
$gitignoreContent = @"
# Virtual Environment
venv/
env/
ENV/

# Python
__pycache__/
*.py[cod]
*`$py.class
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
"@
Set-Content -Path ".gitignore" -Value $gitignoreContent

# Create .env.example
$envExampleContent = @"
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
"@
Set-Content -Path ".env.example" -Value $envExampleContent

# Create pyproject.toml
$pyprojectContent = @"
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "$ProjectName"
version = "0.1.0"
description = "A Python project"
readme = "README.md"
requires-python = ">=$DetectedVersion"
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
$ProjectName = "$ProjectName.main:main"

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
"@
Set-Content -Path "pyproject.toml" -Value $pyprojectContent

# Create README.md
$readmeContent = @"
# $ProjectName

A Python project created with the Python tutorial project generator.

## Setup

### Prerequisites

- Python $DetectedVersion or higher
- pip

### Installation

1. Clone this repository or download the project files
2. Navigate to the project directory:
   ``````powershell
   cd $ProjectName
   ``````

3. Create and activate a virtual environment:
   ``````powershell
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   venv\Scripts\activate
   ``````

4. Install dependencies:
   ``````powershell
   # Production dependencies
   pip install -r requirements.txt
   
   # Development dependencies (for testing, linting, etc.)
   pip install -r requirements-dev.txt
   ``````

### Usage

Run the main application:
``````powershell
python -m src.$ProjectName.main
``````

Or using the installed script (after installing with pip):
``````powershell
$ProjectName
``````

### Development

#### Running Tests

``````powershell
pytest
``````

#### Code Formatting

``````powershell
# Format code
black src tests

# Sort imports
isort src tests
``````

#### Linting

``````powershell
# Type checking
mypy src

# Style checking
flake8 src tests
``````

#### Pre-commit Hooks

Set up pre-commit hooks to automatically run checks:

``````powershell
pre-commit install
``````

## Project Structure

``````
$ProjectName/
├── src/$ProjectName/          # Main package
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
``````

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
"@
Set-Content -Path "README.md" -Value $readmeContent

# Create a simple test
$testContent = @"
"""
Tests for the main module.
"""

from src.$ProjectName.main import main


def test_main():
    """Test the main function runs without error."""
    # This is a placeholder test
    try:
        main()
        assert True
    except Exception:
        assert False, "main() should not raise an exception"
"@
Set-Content -Path "tests\test_main.py" -Value $testContent

# Create activation script for PowerShell
$activateScriptContent = @"
# activation script for PowerShell

# Check if we're in the project directory
if (-not (Test-Path "pyproject.toml")) {
    Write-Error "Error: Not in project root directory"
    exit 1
}

# Activate virtual environment
& "venv\Scripts\Activate.ps1"

# Set PYTHONPATH to include src directory
`$env:PYTHONPATH = "`$env:PYTHONPATH;`$(Get-Location)\src"

# Load environment variables if .env exists
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if (`$_ -match "^([^=]+)=(.*)$") {
            [Environment]::SetEnvironmentVariable(`$matches[1], `$matches[2])
        }
    }
    Write-Host "Loaded environment variables from .env"
}

Write-Host "Virtual environment activated!"
Write-Host "Python version: `$(python --version)"
Write-Host "Project: `$(Split-Path -Leaf `$(Get-Location))"
Write-Host ""
Write-Host "To deactivate: deactivate"
Write-Host "To run tests: pytest"
Write-Host "To format code: black src tests"
"@
Set-Content -Path "scripts\activate.ps1" -Value $activateScriptContent

# Install development dependencies
Write-Status "Installing development dependencies..."
pip install -r requirements-dev.txt

# Initialize git repository
if (Test-Command "git") {
    Write-Status "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: Project structure created"
} else {
    Write-Warning "Git not found. Skipping repository initialization."
}

# Deactivate virtual environment
deactivate

Write-Success "Project '$ProjectName' created successfully!"
Write-Host ""
Write-Status "Next steps:"
Write-Host "  1. cd $ProjectName"
Write-Host "  2. venv\Scripts\activate  (or use scripts\activate.ps1)"
Write-Host "  3. Edit src\$ProjectName\main.py to add your code"
Write-Host "  4. Add dependencies to requirements.txt"
Write-Host "  5. Run tests with: pytest"
Write-Host ""
Write-Status "Quick start:"
Write-Host "  cd $ProjectName; venv\Scripts\activate; python -m src.$ProjectName.main" 