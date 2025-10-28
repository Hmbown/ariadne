## Ariadne v0.4.1 — Stability and Release Polish

Highlights:
- 283 tests passing, 40 skipped across the full suite
- CPU backend stability improvements (consistent timings, robust measurement handling)
- Clean linting and typing (ruff + mypy)
- Accurate README and changelog reflecting current results

Changes:
- Stabilized CPU statevector path by stripping measurements prior to simulation, added warm-up to reduce first-run jitter
- Tightened return types across optional backends to ensure consistent `dict[str, int]`
- Improved performance validation framework with explicit typing and float conversions
- CLI cleanup: removed unused legacy benchmark parser helpers to avoid confusion
- Docs: updated test counts and added precise license classifier for PyPI

Verification:
- Build: `sdist` and `wheel` produced; `twine check` passed
- Demo: Bell state example outputs 00/11 with ~50/50 distribution
- CLI: help/version work; integration tests pass

Upgrade Notes:
- No breaking changes to the public API
- Optional backends remain optional; CLI will suggest extras to install when selected

Thank you to contributors and testers who helped validate this release.
