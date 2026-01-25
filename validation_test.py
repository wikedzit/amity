#!/usr/bin/env python3
"""
Repository Access Validation Test
This script validates that the repository access is working correctly.
"""

import os
import sys
import subprocess
from pathlib import Path

def test_file_read():
    """Test that we can read files from the repository."""
    print("✓ Testing file read access...")
    try:
        readme_path = Path(__file__).parent / "README.md"
        if readme_path.exists():
            content = readme_path.read_text()
            assert "Amity" in content, "README should contain 'Amity'"
            print("  ✓ Successfully read README.md")
            return True
        else:
            print("  ✗ README.md not found")
            return False
    except Exception as e:
        print(f"  ✗ File read failed: {e}")
        return False

def test_file_write():
    """Test that we can write files to the repository."""
    print("✓ Testing file write access...")
    try:
        test_file = Path(__file__).parent / ".validation_test_write"
        test_content = "Repository access validation test - write successful"
        test_file.write_text(test_content)
        
        # Verify we can read what we wrote
        read_back = test_file.read_text()
        assert read_back == test_content, "Written content doesn't match"
        
        # Clean up
        test_file.unlink()
        print("  ✓ Successfully wrote and verified test file")
        return True
    except Exception as e:
        print(f"  ✗ File write failed: {e}")
        return False

def test_git_operations():
    """Test that git operations are accessible."""
    print("✓ Testing git operations...")
    try:
        # Test git status
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        print(f"  ✓ Git status command successful (exit code: {result.returncode})")
        
        # Test git branch
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        branch = result.stdout.strip()
        print(f"  ✓ Current branch: {branch}")
        return True
    except Exception as e:
        print(f"  ✗ Git operations failed: {e}")
        return False

def test_python_imports():
    """Test that we can import project modules."""
    print("✓ Testing Python imports...")
    try:
        sys.path.insert(0, str(Path(__file__).parent / "app"))
        from model import Amity, Office, Living, Staff, Fellow
        from controller import Controller, RoomController
        print("  ✓ Successfully imported project modules")
        return True
    except Exception as e:
        print(f"  ✗ Python imports failed: {e}")
        return False

def main():
    """Run all validation tests."""
    print("=" * 60)
    print("Repository Access Validation Test")
    print("=" * 60)
    print()
    
    tests = [
        ("File Read", test_file_read),
        ("File Write", test_file_write),
        ("Git Operations", test_git_operations),
        ("Python Imports", test_python_imports),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n[{name}]")
        result = test_func()
        results.append((name, result))
    
    print("\n" + "=" * 60)
    print("Validation Test Summary")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {name}: {status}")
        if not result:
            all_passed = False
    
    print()
    if all_passed:
        print("✓ All validation tests passed!")
        return 0
    else:
        print("✗ Some validation tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
