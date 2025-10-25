# Windows CI/CD Troubleshooting Guide for Ariadne

This guide addresses the most common CI/CD issues encountered on Windows systems and provides specific solutions for the Ariadne project.

## Common Windows CI/CD Issues

### 1. PowerShell vs Command Prompt Issues

**Problem**: The CI workflow uses PowerShell commands that may behave differently on different Windows systems.

**Solution**:
- Ensure PowerShell 7+ is installed (PowerShell Core)
- Check PowerShell execution policy: `Get-ExecutionPolicy` (may need to run as admin: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)
- In CI configuration, be explicit about shell: `shell: pwsh` or `shell: powershell`

**Check in workflow**: The current workflow already uses `shell: pwsh` correctly.

### 2. Path Separator Issues

**Problem**: Windows uses backslashes (`\`) while Unix systems use forward slashes (`/`). This can cause issues with PYTHONPATH and file operations.

**Solution**:
```powershell
# Convert backslashes to forward slashes in CI scripts
$env:PYTHONPATH = ($env:PYTHONPATH -replace '\\\', '/')
```

**Check in workflow**: The current workflow already addresses this with:
```yaml
if ($env:PLATFORM -eq "windows") {
  # Fix path separators
  $env:PYTHONPATH = ($env:PYTHONPATH -replace '\\\', '/')
}
```

### 3. Package Installation Issues

**Problem**: Some Python packages with C extensions (like `qiskit-aer`, `quimb`) may fail to install on Windows.

**Solutions**:
1. Ensure Microsoft C++ Build Tools are installed
2. Try installing pre-compiled wheels: `pip install --only-binary=all`
3. Use conda instead of pip if available: `conda install -c conda-forge qiskit-aer`

**Check**: Test installation order and dependencies:
```bash
pip install --upgrade pip
pip install wheel setuptools
pip install -e ".[dev,viz]"
```

### 4. Git Line Ending Issues

**Problem**: Windows uses CRLF while Unix uses LF, causing checksum or test failures.

**Solution**:
```bash
git config --global core.autocrlf true  # For Windows
git config --global core.eol lf         # Force LF in repository
```

### 5. Memory and Resource Constraints

**Problem**: Windows CI runners may have different memory or CPU configurations.

**Solution**:
- Adjust pytest parallelization: `pytest -n 2` instead of `pytest -n auto`
- Add timeout limits to prevent hanging
- Monitor memory usage during tests

### 6. Special Character Handling

**Problem**: Windows file system and command shells handle special characters differently.

**Solution**: Ensure file paths and test data don't contain problematic characters

## Quick Diagnostic Steps

### 1. Run the diagnostic script:
```powershell
python windows_ci_diagnostic.py
```

### 2. Manually test the CI workflow locally:
```powershell
# Create a virtual environment
python -m venv ci_test_env
ci_test_env\Scripts\Activate.ps1

# Install dependencies
python -m pip install --upgrade pip
pip install -e ".[dev,viz]"

# Run tests
pytest tests/ -v --tb=short -n 2 --cov=src/ariadne --cov-report=xml --cov-fail-under=60
```

### 3. Verify each dependency individually:
```powershell
python -c "import ariadne; print('Ariadne import successful')"
python -c "import qiskit; print('Qiskit version:', qiskit.__version__)"
python -c "import stim; print('Stim import successful')"
python -c "import numpy; print('NumPy version:', numpy.__version__)"
```

## CI YAML Configuration Checks

### 1. Verify Windows-specific configurations:
```yaml
# The workflow should handle Windows-specific path issues
- name: Fix path separators
  shell: pwsh
  run: |
    $env:PYTHONPATH = ($env:PYTHONPATH -replace '\\\', '/')
```

### 2. Check dependency installation:
```yaml
# Should handle Windows package installation
- name: Install dependencies
  shell: pwsh
  run: |
    python -m pip install --upgrade pip
    pip install -e ".[dev,viz]"
```

### 3. Verify test execution:
```yaml
# Should handle Windows-specific test execution
- name: Run tests
  shell: pwsh
  run: |
    $env:PYTHONPATH = ($env:PYTHONPATH -replace '\\\', '/')
    pytest tests/ -v --tb=short -n 2 --cov=src/ariadne --cov-report=xml --cov-fail-under=60
```

## Resolution Steps

### Immediate Actions:
1. **Run the diagnostic script** to identify specific issues
2. **Verify PowerShell access** and execution policy
3. **Test package installations** individually
4. **Check for antivirus interference** blocking installations
5. **Verify path configuration** and separators

### Configuration Fixes:
1. **Update the CI workflow** if needed (the current one looks good)
2. **Add Windows-specific environment variables** if required
3. **Adjust test parallelization** for Windows systems
4. **Add timeout handling** for potentially hanging tests

### Verification Steps:
1. **Test the full CI workflow** on a Windows system
2. **Run the same test suite** that fails in CI
3. **Validate dependency installation** order and method
4. **Confirm all path manipulations** work as expected

## Additional Resources

- [GitHub Actions on Windows](https://docs.github.com/en/actions/using-github-hosted-runners/using-github-hosted-runners/about-github-hosted-runners#supported-runners-and-hardware-resources)
- [Python on Windows](https://docs.python.org/3/using/windows.html)
- [PowerShell Execution Policies](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy)

## When to Seek Help

If issues persist after following these troubleshooting steps:

1. Collect the output from the diagnostic script
2. Document which specific tests or installations fail
3. Note any error messages and their context
4. Share the Windows version and Python version being used
5. Provide the exact commands that are failing

This information will help identify unusual Windows environment configurations that may be causing the CI/CD issues.
