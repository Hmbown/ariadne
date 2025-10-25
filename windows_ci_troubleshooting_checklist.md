# Windows CI/CD Troubleshooting Checklist for Ariadne

This checklist is for AI agents to systematically troubleshoot CI/CD issues on Windows devices for the Ariadne project.

## 1. Environment Setup Verification

### Python Installation
- [ ] Verify Python 3.11 or 3.12 is installed on the system
- [ ] Confirm Python is accessible from command line (`python --version` or `py --version`)
- [ ] Check that `pip` is installed and up-to-date (`pip --version`)

### PowerShell/Command Line Access
- [ ] Verify PowerShell 7+ is available (needed for CI scripts)
- [ ] Test that command line can execute basic Python commands
- [ ] Verify access to git (`git --version`)

## 2. Dependency Installation

### Core Dependencies
- [ ] Install core dependencies using: `pip install -e ".[dev,viz]"`
- [ ] Verify all dependencies install without errors
- [ ] Check for any Windows-specific installation issues with packages like:
  - `qiskit-aer`
  - `stim`
  - `quimb`
  - `numpy`
  - `scipy`

### Optional Dependencies
- [ ] Try installing visualization dependencies: `pip install ".[viz]"`
- [ ] Test installation of other optional dependencies if needed

## 3. Path and Environment Variables

### Python Path Issues
- [ ] Check if PYTHONPATH contains Windows-style backslashes that may need to be converted to forward slashes
- [ ] Verify Python can import installed packages (`python -c "import ariadne"`)

### Environment Variables
- [ ] Ensure PATH variable includes Python installation directory
- [ ] Check that Windows-specific environment variables are properly set

## 4. Testing Execution

### Run Basic Tests
- [ ] Execute basic unit tests: `pytest tests/ -v -k "not slow"`
- [ ] Check for Windows-specific test failures
- [ ] Verify test coverage command works: `pytest --cov=src/ariadne --cov-report=xml`

### Cross-Platform Specific Tests
- [ ] Run Windows-specific test configurations
- [ ] Check if any tests are marked with Windows-specific requirements

## 5. PowerShell Script Issues

### CI Script Compatibility
- [ ] Verify all PowerShell scripts in CI workflow run correctly on this Windows machine
- [ ] Check for any Unix/Linux-specific commands that don't work on Windows
- [ ] Test the exact commands from the CI workflow in local PowerShell

### Shell Commands
- [ ] Ensure shell commands in CI workflow are compatible with Windows PowerShell
- [ ] Verify any path manipulation (like the PYTHONPATH fix in the CI) works correctly

## 6. File System Issues

### Path Separators
- [ ] Check if any code or tests expect Unix-style path separators
- [ ] Verify file operations work correctly with Windows-style paths
- [ ] Test that the code handles cross-platform path differences

### Line Endings
- [ ] Verify git is configured to handle line endings properly (CRLF vs LF)
- [ ] Check if any tests fail due to line ending differences

## 7. Specialized Dependencies

### Quantum Packages
- [ ] Test installation and import of quantum simulation packages:
  - `qiskit`
  - `qiskit-aer` (Windows wheels available)
  - `stim`
  - Check for Windows-specific compilation issues

### CUDA (if available)
- [ ] Check if CUDA is installed on the Windows system
- [ ] Test CUDA-specific dependencies only if CUDA is present
- [ ] Verify `pip install ".[cuda]"` command works if CUDA is available

## 8. Build Process

### Package Build
- [ ] Test building the package locally: `python -m build`
- [ ] Verify the build process works on Windows
- [ ] Check for Windows-specific packaging issues

### Development Installation
- [ ] Test `pip install -e .` (editable install)
- [ ] Verify all entry points work as expected

## 9. Code Quality Checks

### Linting
- [ ] Run ruff linter: `ruff check src/ tests/`
- [ ] Fix any Windows-specific linting issues
- [ ] Run formatter: `ruff format --check src/ tests/`

### Type Checking
- [ ] Run mypy: `mypy src/ariadne/`
- [ ] Address any Windows-specific typing issues

## 10. Common Windows Issues

### Permission Issues
- [ ] Check if Windows Defender or antivirus is blocking operations
- [ ] Ensure PowerShell execution policy allows scripts to run

### Memory and Performance
- [ ] Monitor memory usage during tests (Windows may have different limits)
- [ ] Verify test timeouts are appropriate for Windows systems

### Networking
- [ ] Check if any tests require network access and if Windows firewall is blocking them

## 11. Verification Steps

### Final Validation
- [ ] Run a full test suite to verify all issues are resolved
- [ ] Confirm the same CI commands from the workflow file work on this system
- [ ] Verify all optional features work correctly on Windows

### Documentation
- [ ] Document any Windows-specific configuration needed
- [ ] Update README if Windows-specific instructions are needed
