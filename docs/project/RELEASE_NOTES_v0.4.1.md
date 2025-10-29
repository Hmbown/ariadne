## Ariadne v0.4.1 — Stability and Release Polish

Highlights:
- 319 tests passing, 32 skipped across the full suite
- Stim Clifford conversion now runs in microseconds by emitting native program text
- Clean packaging metadata with canonical project URLs and build artifacts validated via `twine`
- Accurate README, benchmark report, and notebook guidance reflecting latest performance

Changes:
- Raised minimum supported Python to 3.11 (aligns with dependency support and `zip(..., strict=True)`)
- Rewrote Qiskit→Stim converter to emit Stim program text directly, removing Python append overhead (~100 ms → μs)
- Stabilized CPU statevector path by stripping measurements prior to simulation, added warm-up to reduce first-run jitter
- Tightened return types across optional backends to ensure consistent `dict[str, int]`
- Normalized performance validation framework to use plain floats, avoiding NumPy scalar warnings
- CLI cleanup: removed unused legacy benchmark parser helpers to avoid confusion
- Docs & examples: refreshed benchmark metrics, updated routing demo to use the analyzer helper, clarified honest speedup ranges (10–100×)

Verification:
- Build: `sdist` and `wheel` produced; `twine check` passed
- Tests: `pytest` reports 319 passed, 32 skipped on Apple Silicon (M4 Max)
- Demo: Bell state example outputs 00/11 with ~50/50 distribution
- CLI: help/version work; integration tests pass

Upgrade Notes:
- Python 3.11+ is now required (CI validated on 3.11/3.12)
- No breaking changes to the public API
- Optional backends remain optional; CLI will suggest extras to install when selected

Thank you to contributors and testers who helped validate this release.
