"""
Virtual Environment Management Demo

This script demonstrates virtual environment concepts and provides
utilities for managing Python virtual environments effectively.

Key concepts covered:
1. Environment detection
2. Package management
3. Dependency analysis
4. Environment health checks
5. Automation utilities
"""

import os
import sys
import subprocess
import json
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple, NamedTuple
from dataclasses import dataclass


class PackageInfo(NamedTuple):
    """Information about an installed package."""
    name: str
    version: str
    location: str


@dataclass
class EnvironmentInfo:
    """Information about the current Python environment."""
    is_virtual: bool
    python_version: str
    python_executable: str
    virtual_env_path: Optional[str]
    site_packages: List[str]
    installed_packages: List[PackageInfo]


class VirtualEnvironmentManager:
    """Utility class for managing virtual environments."""
    
    def __init__(self) -> None:
        self.current_env = self._get_environment_info()
    
    def _get_environment_info(self) -> EnvironmentInfo:
        """Get comprehensive information about the current environment."""
        # Check if we're in a virtual environment
        is_virtual = self._is_virtual_environment()
        
        # Get virtual environment path
        venv_path = None
        if is_virtual:
            venv_path = self._get_virtual_env_path()
        
        # Get site packages directories
        site_packages = self._get_site_packages()
        
        # Get installed packages
        installed_packages = self._get_installed_packages()
        
        return EnvironmentInfo(
            is_virtual=is_virtual,
            python_version=sys.version,
            python_executable=sys.executable,
            virtual_env_path=venv_path,
            site_packages=site_packages,
            installed_packages=installed_packages
        )
    
    def _is_virtual_environment(self) -> bool:
        """Check if we're running in a virtual environment."""
        return (
            hasattr(sys, 'real_prefix') or  # virtualenv
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)  # venv
        )
    
    def _get_virtual_env_path(self) -> Optional[str]:
        """Get the path to the virtual environment."""
        if not self._is_virtual_environment():
            return None
        
        # Try to get from environment variables
        venv_path = os.environ.get('VIRTUAL_ENV')
        if venv_path:
            return venv_path
        
        # Try to infer from sys.prefix
        if hasattr(sys, 'real_prefix'):
            return sys.prefix
        elif hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix:
            return sys.prefix
        
        return None
    
    def _get_site_packages(self) -> List[str]:
        """Get list of site-packages directories."""
        import site
        return site.getsitepackages() + [site.getusersitepackages()]
    
    def _get_installed_packages(self) -> List[PackageInfo]:
        """Get list of installed packages."""
        try:
            import pkg_resources
            packages = []
            for dist in pkg_resources.working_set:
                packages.append(PackageInfo(
                    name=dist.project_name,
                    version=dist.version,
                    location=dist.location
                ))
            return sorted(packages, key=lambda p: p.name.lower())
        except ImportError:
            return []
    
    def print_environment_info(self) -> None:
        """Print comprehensive environment information."""
        print("=" * 60)
        print("PYTHON VIRTUAL ENVIRONMENT INFORMATION")
        print("=" * 60)
        
        env = self.current_env
        
        print(f"Virtual Environment: {'Yes' if env.is_virtual else 'No'}")
        if env.virtual_env_path:
            print(f"Environment Path: {env.virtual_env_path}")
        
        print(f"Python Version: {env.python_version.split()[0]}")
        print(f"Python Executable: {env.python_executable}")
        
        print(f"\nSite Packages Directories:")
        for path in env.site_packages:
            print(f"  - {path}")
        
        print(f"\nInstalled Packages ({len(env.installed_packages)}):")
        for pkg in env.installed_packages[:10]:  # Show first 10
            print(f"  - {pkg.name} {pkg.version}")
        
        if len(env.installed_packages) > 10:
            print(f"  ... and {len(env.installed_packages) - 10} more packages")


class VirtualEnvironmentCreator:
    """Utility for creating and managing virtual environments."""
    
    @staticmethod
    def create_project_structure(project_name: str) -> None:
        """Create a complete project structure with virtual environment."""
        project_path = Path(project_name)
        
        if project_path.exists():
            print(f"Project '{project_name}' already exists!")
            return
        
        # Create project directory
        project_path.mkdir()
        
        # Create virtual environment
        venv_path = project_path / 'venv'
        subprocess.run([sys.executable, '-m', 'venv', str(venv_path)], check=True)
        
        # Create project structure
        (project_path / 'src').mkdir()
        (project_path / 'src' / project_name).mkdir()
        (project_path / 'tests').mkdir()
        (project_path / 'docs').mkdir()
        
        # Create initial files
        (project_path / 'src' / project_name / '__init__.py').touch()
        (project_path / 'tests' / '__init__.py').touch()
        
        # Create requirements.txt
        requirements_content = """# Production dependencies
requests>=2.28.0
"""
        (project_path / 'requirements.txt').write_text(requirements_content)
        
        # Create .gitignore
        gitignore_content = """# Virtual environment
venv/
env/

# Python
__pycache__/
*.py[cod]
*.so
.Python
build/
dist/
*.egg-info/

# Testing
.coverage
.pytest_cache/

# Environment variables
.env

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
"""
        (project_path / '.gitignore').write_text(gitignore_content)
        
        # Create README.md
        readme_content = f"""# {project_name}

## Setup

1. Activate virtual environment:
   ```bash
   source venv/bin/activate  # On macOS/Linux
   venv\\Scripts\\activate    # On Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
"""
        (project_path / 'README.md').write_text(readme_content)
        
        print(f"Project '{project_name}' created with virtual environment!")
        print(f"Activate with: source {project_name}/venv/bin/activate")


def demonstrate_environment_management():
    """Demonstrate virtual environment management features."""
    print("Virtual Environment Management Demonstration")
    print("=" * 50)
    
    # Create environment manager
    env_manager = VirtualEnvironmentManager()
    
    # Show environment information
    env_manager.print_environment_info()


def demonstrate_project_creation():
    """Demonstrate project creation with virtual environment."""
    print("\n" + "=" * 60)
    print("PROJECT CREATION DEMONSTRATION")
    print("=" * 60)
    
    # Create a temporary project for demonstration
    temp_dir = tempfile.mkdtemp()
    project_name = "demo_project"
    project_path = Path(temp_dir) / project_name
    
    try:
        # Change to temp directory
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        # Create project
        creator = VirtualEnvironmentCreator()
        creator.create_project_structure(project_name)
        
        # Show created structure
        print(f"\nCreated project structure in {project_path}:")
        for item in sorted(project_path.rglob('*')):
            relative_path = item.relative_to(project_path)
            if item.is_dir():
                print(f"  📁 {relative_path}/")
            else:
                print(f"  📄 {relative_path}")
        
        # Show some file contents
        print(f"\nSample file contents:")
        print(f"\n--- requirements.txt ---")
        print((project_path / 'requirements.txt').read_text())
    
    finally:
        # Cleanup
        os.chdir(original_cwd)
        shutil.rmtree(temp_dir)
        print(f"\nCleaned up temporary project directory.")


def compare_environment_tools():
    """Compare different virtual environment tools."""
    print("\n" + "=" * 60)
    print("VIRTUAL ENVIRONMENT TOOLS COMPARISON")
    print("=" * 60)
    
    tools_comparison = {
        'venv': {
            'description': 'Built-in virtual environment tool',
            'pros': ['Built into Python 3.3+', 'Lightweight', 'Simple'],
            'cons': ['Basic features', 'No dependency resolution'],
            'use_case': 'Simple projects, learning Python'
        },
        'conda': {
            'description': 'Package and environment manager',
            'pros': ['Handles non-Python dependencies', 'Scientific packages'],
            'cons': ['Large installation', 'Slower'],
            'use_case': 'Data science, scientific computing'
        },
        'pipenv': {
            'description': 'High-level interface to pip and virtualenv',
            'pros': ['Pipfile instead of requirements.txt', 'Automatic activation'],
            'cons': ['Slower than pip', 'Can be complex'],
            'use_case': 'Modern Python development'
        },
        'poetry': {
            'description': 'Modern dependency management and packaging',
            'pros': ['Excellent dependency resolution', 'Built-in packaging'],
            'cons': ['Learning curve', 'Newer tool'],
            'use_case': 'Modern Python projects, library development'
        }
    }
    
    for tool, info in tools_comparison.items():
        print(f"\n{tool.upper()}:")
        print(f"  Description: {info['description']}")
        print(f"  Pros: {', '.join(info['pros'])}")
        print(f"  Cons: {', '.join(info['cons'])}")
        print(f"  Use case: {info['use_case']}")


def main():
    """Main demonstration function."""
    try:
        demonstrate_environment_management()
        demonstrate_project_creation()
        compare_environment_tools()
        
        print("\n" + "=" * 60)
        print("VIRTUAL ENVIRONMENT BEST PRACTICES")
        print("=" * 60)
        
        best_practices = [
            "Always use virtual environments for Python projects",
            "Keep requirements.txt files up to date",
            "Use separate requirements files for dev/prod",
            "Never commit virtual environment directories to git",
            "Use .env files for environment variables",
            "Regularly update packages and check for vulnerabilities",
            "Document environment setup in README",
            "Consider using Docker for complex dependencies",
            "Use tools like direnv for automatic activation",
            "Pin package versions for reproducible builds"
        ]
        
        for i, practice in enumerate(best_practices, 1):
            print(f"{i:2d}. {practice}")
        
    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 