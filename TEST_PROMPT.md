# Ariadne Quantum Simulator Router - Test Prompt

## TASK: Comprehensive Testing of Updated Ariadne Quantum Simulator Router

You are tasked with thoroughly testing the latest version of the Ariadne quantum simulator router that has been enhanced with additional features. The repository is located at `/Volumes/VIXinSSD/ariadne`.

## NEW FEATURES TO TEST

### 1. Missing Function Added
- [ ] Test the new `get_available_backends()` function
- [ ] Verify it returns a list of actually available backends
- [ ] Test that it's properly exported in the public API

### 2. Expanded Quantum Platform Support
- [ ] Check that optional dependencies for PennyLane, PyQuil, Braket, Q#, and OpenCL are properly defined in pyproject.toml
- [ ] Verify quantum_platforms dependency group exists
- [ ] Test that the package still installs with core dependencies only

### 3. Quantum-Full Docker Environment
- [ ] Review the Dockerfile for the new `quantum-full` stage
- [ ] Check docker-compose.yml for the new `ariadne-quantum-full` service
- [ ] Verify README.md has been updated with quantum-full Docker instructions (file: `/Volumes/VIXinSSD/ariadne/README.md`)
- [ ] Test that the Dockerfile builds with all target stages

### 4. Core Functionality Verification
- [ ] Verify basic installation still works: `pip install -e .`
- [ ] Test basic simulation: `from ariadne import simulate; result = simulate(circuit, shots=100)`
- [ ] Test routing functionality: `from ariadne import explain_routing; explain_routing(circuit)`
- [ ] Verify backend selection works correctly
- [ ] Test error handling remains robust

### 5. Documentation Quality
- [ ] Verify README.md Docker usage instructions are clear (`/Volumes/VIXinSSD/ariadne/README.md`)
- [ ] Check that all code examples in README work
- [ ] Verify CHANGELOG.md accurately reflects all changes (`/Volumes/VIXinSSD/ariadne/CHANGELOG.md`)
- [ ] Confirm installation instructions are up-to-date

### 6. Package Quality Assessment
Rate 1-10 on:
- [ ] Code quality and organization
- [ ] Documentation completeness
- [ ] Ease of use for end users
- [ ] Professional packaging
- [ ] Docker environment completeness

## ADDITIONAL TEST SCENARIOS

### Docker Testing (if possible):
- [ ] Build quantum-full stage: `docker build --target quantum-full -t ariadne-quantum-full .`
- [ ] Test running the quantum-full container
- [ ] Verify all quantum libraries are accessible inside container

### Dependency Testing:
- [ ] Install with quantum platforms: `pip install ariadne-router[quantum_platforms]`
- [ ] Install with all optional deps: `pip install ariadne-router[dev,quantum_platforms,apple,cuda,advanced]`
- [ ] Verify the package works with minimal dependencies

## EXPECTED RESULTS

- All new features work without breaking existing functionality
- Docker quantum-full environment includes all quantum libraries
- Installation succeeds with or without optional dependencies
- Documentation matches actual behavior
- The `get_available_backends()` function works as expected

## REPORT FORMAT

Please provide:

1. ✅/❌ for each test item
2. Any error messages encountered
3. Specific recommendations for improvement
4. Overall assessment (Professional/Amateur/Broken)
5. Performance notes where applicable

Focus on whether the new features are properly implemented and whether existing functionality remains intact.
