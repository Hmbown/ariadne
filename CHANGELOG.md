# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-10-15

- macOS-first launch; Apple Silicon supported via Metal (falls back to CPU gracefully).
- Automatic backend routing:
  - Clifford → Stim
  - Low entanglement → MPS
  - Apple Silicon → Metal (when available)
  - General → Qiskit (CPU)
- CLI wired to `ariadne.cli.main:main`; `ariadne --help` now exposes subcommands.
- Fixed Metal backend sampling without JAX by converting statevector to NumPy.
- Docs: added Use Cases and Routing Matrix to README; added routing rules page and examples gallery.
- Packaging verified: `python -m build` and `twine check` pass.
- Docker: development and production stages updated for editable and standard installs.
