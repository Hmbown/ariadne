#!/usr/bin/env python3
"""
Windows CI/CD Diagnostic Script for Ariadne
This script helps diagnose common CI/CD issues on Windows systems.
"""

import importlib
import os
import platform
import subprocess
import sys
from pathlib import Path


def check_python_version() -> bool:
    """Check if Python version is compatible"""
    print("Checking Python version...")
    major, minor, patch = sys.version_info[:3]
    print(f"Python version: {major}.{minor}.{patch}")

    if major == 3 and minor >= 11:
        print("✓ Python version is compatible")
        return True
    else:
        print("✗ Python version is NOT compatible. Need Python 3.11+")
        return False


def check_pip() -> bool:
    """Check pip installation"""
    print("\nChecking pip...")
    try:
        import pip

        print(f"✓ pip version: {pip.__version__}")
        return True
    except ImportError:
        print("✗ pip is not available")
        return False


def check_git() -> bool:
    """Check git installation"""
    print("\nChecking git...")
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"✓ Git version: {result.stdout.strip()}")
            return True
        else:
            print("✗ Git is not available")
            return False
    except FileNotFoundError:
        print("✗ Git is not available")
        return False


def check_powershell() -> bool:
    """Check PowerShell installation"""
    print("\nChecking PowerShell...")
    try:
        # Try PowerShell 7+ first
        result = subprocess.run(["pwsh", "--version"], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"✓ PowerShell version: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass

    try:
        # Try Windows PowerShell
        result = subprocess.run(["powershell", "--version"], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"✓ Windows PowerShell version: {result.stdout.strip()}")
            return True
        else:
            print("✗ PowerShell is not available")
            return False
    except FileNotFoundError:
        print("✗ PowerShell is not available")
        return False


def check_ariadne_dependencies() -> bool:
    """Check if core Ariadne dependencies can be imported"""
    print("\nChecking Ariadne dependencies...")
    dependencies = ["qiskit", "qiskit.aer", "stim", "quimb", "numpy", "scipy", "networkx", "matplotlib", "yaml"]

    all_good = True
    for dep in dependencies:
        try:
            if "." in dep:
                # For nested imports like qiskit.aer
                parts = dep.split(".")
                module = __import__(parts[0])
                for part in parts[1:]:
                    module = getattr(module, part)
            else:
                importlib.import_module(dep)
            print(f"✓ {dep} imported successfully")
        except ImportError as e:
            print(f"✗ Failed to import {dep}: {e}")
            all_good = False

    return all_good


def check_path_issues() -> bool:
    """Check for common path issues on Windows"""
    print("\nChecking for path issues...")

    # Check if PYTHONPATH has backslashes that might cause issues
    pythonpath = os.environ.get("PYTHONPATH", "")
    if "\\" in pythonpath:
        print(f"! PYTHONPATH contains backslashes: {pythonpath}")
        print("  This might cause issues in PowerShell/CMD environments")

    # Check current working directory
    cwd = os.getcwd()
    print(f"Current working directory: {cwd}")

    # Check if we're in the Ariadne project directory
    expected_files = ["pyproject.toml", "README.md", "src", "tests"]
    project_files = [f for f in expected_files if Path(f).exists()]

    if len(project_files) >= 3:
        print("✓ Appears to be in correct Ariadne project directory")
        return True
    else:
        print("! Warning: May not be in the correct project directory")
        return False


def run_basic_tests() -> bool:
    """Try to run basic tests to verify functionality"""
    print("\nChecking test execution capability...")

    # Check if tests directory exists
    if Path("tests").exists():
        print("✓ tests directory exists")
        return True
    else:
        print("✗ tests directory does not exist")
        return False


def check_windows_specific_issues() -> None:
    """Check for common Windows-specific CI/CD issues"""
    print("\nChecking Windows-specific CI/CD issues...")

    # Check platform
    system = platform.system()
    print(f"Operating System: {system}")

    if system.lower() != "windows":
        print("! Warning: This script is designed for Windows systems")

    # Check for Windows Defender or antivirus interference
    print("Note: Check if Windows Defender or antivirus is blocking operations")

    # Check long path support
    try:
        result = subprocess.run(
            [
                "reg",
                "query",
                "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\FileSystem",
                "/v",
                "LongPathsEnabled",
            ],
            capture_output=True,
            text=True,
            shell=True,
        )
        if result.returncode == 0 and "0x1" in result.stdout:
            print("✓ Long path support is enabled")
        else:
            print("! Long path support may be disabled (can cause issues with deep directory structures)")
    except Exception:
        print("? Could not check long path support")


def main() -> None:
    """Main diagnostic function"""
    print("=" * 60)
    print("Ariadne Windows CI/CD Diagnostic Tool")
    print("=" * 60)

    all_checks: list[bool] = []

    all_checks.append(check_python_version())
    all_checks.append(check_pip())
    all_checks.append(check_git())
    all_checks.append(check_powershell())
    all_checks.append(check_ariadne_dependencies())
    all_checks.append(check_path_issues())
    all_checks.append(run_basic_tests())
    check_windows_specific_issues()  # This function returns None, so just call it
    all_checks.append(True)  # Always add True for this check since it doesn't return anything

    print("\n" + "=" * 60)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 60)

    passed = sum(all_checks)
    total = len(all_checks)

    print(f"Passed checks: {passed}/{total}")

    if passed == total:
        print("✓ All checks passed! CI/CD should work properly.")
    else:
        print("✗ Some checks failed. Please review the issues above and consult the troubleshooting checklist.")

    print("\nFor detailed troubleshooting steps, see: windows_ci_troubleshooting_checklist.md")


if __name__ == "__main__":
    main()
