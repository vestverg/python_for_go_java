#!/usr/bin/env python3
"""
Project verification script to ensure all examples work correctly.
"""
import sys
import importlib.util
from pathlib import Path
from typing import List, Tuple


def test_import(module_path: Path, module_name: str) -> Tuple[bool, str]:
    """Test if a module can be imported successfully."""
    try:
        # Add the module's directory to sys.path temporarily
        original_path = sys.path.copy()
        module_dir = module_path.parent
        if str(module_dir) not in sys.path:
            sys.path.insert(0, str(module_dir))
        
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None:
            return False, f"Could not create spec for {module_name}"
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Restore original path
        sys.path = original_path
        
        return True, f"✅ {module_name} imported successfully"
    except Exception as e:
        # Restore original path on error
        sys.path = original_path
        return False, f"❌ {module_name} failed: {str(e)}"


def verify_project_structure() -> List[Tuple[bool, str]]:
    """Verify that all expected files exist and can be imported."""
    results = []
    
    # Define expected example files
    examples = [
        ("01_getting_started/examples/hello.py", "hello"),
        ("02_basic_syntax/examples/data_types.py", "data_types"),
        ("03_control_flow/examples/control_flow.py", "control_flow"),
        ("04_functions/examples/functions.py", "functions"),
        ("05_oop/examples/library_system.py", "library_system"),
        ("05_oop/examples/shapes.py", "shapes"),
        ("06_modules_and_packages/examples/example_usage.py", "example_usage"),
        ("07_concurrency/examples/threading_example.py", "threading_example"),
        ("07_concurrency/examples/multiprocessing_example.py", "multiprocessing_example"),
        ("07_concurrency/examples/asyncio_example.py", "asyncio_example"),
        ("08_python_features/examples/advanced_features_demo.py", "advanced_features_demo"),
    ]
    
    for file_path, module_name in examples:
        path = Path(file_path)
        if path.exists():
            success, message = test_import(path, module_name)
            results.append((success, message))
        else:
            results.append((False, f"❌ File not found: {file_path}"))
    
    return results


def verify_tests() -> List[Tuple[bool, str]]:
    """Verify that test files exist."""
    results = []
    
    test_files = [
        "tests/test_hello.py",
        "tests/test_data_types.py",
        "tests/test_control_flow.py",
        "tests/test_functions.py",
        "tests/test_oop.py",
        "tests/test_modules.py",
        "tests/test_concurrency.py",
        "tests/test_advanced_features.py",
    ]
    
    for test_file in test_files:
        path = Path(test_file)
        if path.exists():
            results.append((True, f"✅ {test_file} exists"))
        else:
            results.append((False, f"❌ {test_file} missing"))
    
    return results


def main():
    """Main verification function."""
    print("🔍 Verifying Python Tutorial Project Structure")
    print("=" * 50)
    
    # Check examples
    print("\n📚 Checking Example Files:")
    example_results = verify_project_structure()
    for success, message in example_results:
        print(f"  {message}")
    
    # Check tests
    print("\n🧪 Checking Test Files:")
    test_results = verify_tests()
    for success, message in test_results:
        print(f"  {message}")
    
    # Summary
    total_checks = len(example_results) + len(test_results)
    successful_checks = sum(1 for success, _ in example_results + test_results if success)
    
    print(f"\n📊 Summary:")
    print(f"  Total checks: {total_checks}")
    print(f"  Successful: {successful_checks}")
    print(f"  Failed: {total_checks - successful_checks}")
    
    if successful_checks == total_checks:
        print("\n🎉 All checks passed! Project structure is complete and consistent.")
        return 0
    else:
        print(f"\n⚠️  {total_checks - successful_checks} checks failed. See details above.")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 