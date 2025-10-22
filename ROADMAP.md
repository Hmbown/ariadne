# Ariadne 6-Month Roadmap: Production-Ready Implementation Plan

Thank you for approving the plan! This document outlines the complete, actionable 6-month roadmap for making Ariadne production-ready. It's based on the project's current state (beta status, 38% test coverage, solid Qiskit/Stim integration, cross-platform CI) and addresses key gaps (unpinned deps, flaky tests, incomplete Windows support). Community tasks (e.g., Discord, full PyPI prep) are deprioritized as requested.

The plan is phased, with **prioritized sub-tasks**, **estimated effort** (person-weeks, 1 FTE), **dependencies**, **success metrics**, and **risks/mitigations**. Total effort: ~20-24 weeks over 6 months.

## Overall Goals
- **Short-term (Months 1-2)**: Stabilize core (tests >60% coverage, pinned deps, robust CI). Focus: Reliability.
- **Medium-term (Months 3-4)**: Enhance features (async/reproducibility, experimental backends). Focus: Advanced usage.
- **Long-term (Months 5-6)**: Scale and polish (metrics, optimizations). Focus: Production deployment.
- **Cross-cutting**: Risk mitigation, docs updates, feedback loops.
- **Success Metrics**: 80%+ coverage; zero CI flakiness; Windows/macOS/Linux parity; >50% routing accuracy via benchmarks.
- **Tools/Resources**: pytest-cov, pip-tools, GitHub Actions, Sphinx. Budget: 1 FTE.

## Phase 1: Short-term Stabilization (Months 1-2)
**Goal**: Reliable, reproducible builds/tests. Effort: 8-10 weeks. Priority: High.

### 1. Pin Dependencies (Week 1, 0.5 weeks)
- Generate pinned `requirements.txt` from pyproject.toml using pip-tools.
- Pin core deps (e.g., `qiskit==2.1.1`, `stim==1.15.0`); add lockfiles to CI.
- Test multi-platform installs.
- **Dependencies**: None.
- **Metrics**: No conflicts; passes CI installs.
- **Risks**: Version breakage → Use tox for compatibility testing.

### 2. Stabilize Test Suite (Weeks 1-3, 2 weeks)
- Audit 23 test files (e.g., `test_backends.py`, `test_routing.py`); fix flakiness (e.g., add seeds/timeouts to `test_performance_validation.py`).
- Add tests: GHZ/Steane in `src/ariadne/algorithms/`; Braket/PyQuil integrations in `tests/test_backends.py`.
- Enforce >60% coverage in CI.yml (add `--cov` to pytest).
- Enhance async/reproducibility tests in `src/ariadne/async_/` and `src/ariadne/verify/`.
- **Dependencies**: Pinned deps.
- **Metrics**: >60% coverage; 95% Windows pass rate.
- **Risks**: Parallelism issues → Use pytest-xdist.

### 3. Expand CI Cross-Platform (Weeks 3-4, 1.5 weeks)
- Update ci.yml: Windows path fixes; full matrix (os/Python).
- Add notebook/example validation; coverage upload for all platforms.
- **Dependencies**: Tests.
- **Metrics**: Passes on 6 combos; <5min jobs.
- **Risks**: Env issues → pwsh for Windows.

### 4. Enhance Documentation (Weeks 4-5, 1 week)
- Create `docs/guides/windows.md` (CUDA/path tips).
- Add alt-text to images (e.g., routing matrix); CI-validate examples.
- Update Sphinx for API docs; add badges.
- **Dependencies**: CI.
- **Metrics**: Builds clean; 100% alt-text.
- **Risks**: Sphinx errors → Local previews.

### 5. Validate Experimental Backends (Weeks 5-6, 1 week)
- Tests for Braket/PyQuil (mock services); add to router with fallbacks.
- **Dependencies**: Tests.
- **Metrics**: 90% pass rate; docs on limits.
- **Risks**: API instability → Optional deps.

### 6. Initial Analytics (Weeks 7-8, 1 week)
- Script for GitHub metrics (`scripts/track_metrics.py`); opt-in logging in `simulate()`.
- **Dependencies**: None.
- **Metrics**: CSV reports; no PII.
- **Risks**: Privacy → Opt-in only.

**Milestones**: Stable CI, >60% coverage, Windows guide. Demo: Full test suite run.

## Phase 2: Medium-term Enhancements (Months 3-4)
**Goal**: Advanced features. Effort: 6-8 weeks. Priority: Medium.

### 1. Async & Reproducibility (Weeks 9-10, 1.5 weeks)
- Async routing in `src/ariadne/async_/simulation.py` (asyncio.gather).
- Seed/variance checks in `src/ariadne/verify/`.
- **Metrics**: 2x speedup; 100% reproducibility.
- **Risks**: Deadlocks → pytest-asyncio.

### 2. Backend Optimizations (Weeks 11-12, 2 weeks)
- JAX-Metal/CUDA auto-detect; hybrid Stim+TN routing.
- **Metrics**: 20% perf gain; >80% coverage.
- **Risks**: Hardware variance → Platform CI.

### 3. Algorithm Routing (Weeks 13-14, 1.5 weeks)
- VQE/QAOA routers; add 5 algos (Shor's, HHL) to `src/ariadne/algorithms/`.
- **Metrics**: 15+ algos; benchmark docs.
- **Risks**: Complexity → Sprint limits.

### 4. Docs Polish (Weeks 15-16, 1 week)
- Advanced guides; CI for examples.
- **Metrics**: 10+ notebooks.

**Milestones**: Async support, 80%+ coverage, hybrid routing. Demo: Parallel sims.

## Phase 3: Long-term Scalability (Months 5-6)
**Goal**: Production-scale. Effort: 6-8 weeks. Priority: Low.

### 1. Scalability (Weeks 17-19, 2 weeks)
- 100+ qubit support (Ray for TN); memory estimators.
- **Metrics**: 128-qubit <10min; scalability report.
- **Risks**: Compute → More RAM runners.

### 2. Risk & Monitoring (Weeks 20-21, 1 week)
- Top 5 risks doc; Sentry integration.
- **Metrics**: Zero high vulns.
- **Risks**: Over-doc → Focus key risks.

### 3. Release Prep (Weeks 22-24, 2 weeks)
- v1.0 candidate: Changelog, metrics dashboard.
- **Metrics**: Stable API; adoption baseline.
- **Risks**: Blockers → Staged rollouts.

**Milestones**: Production-ready. Demo: Benchmark suite.

## Timeline & Resources
- **M1-2**: 100% stabilization.
- **M3-4**: 70% features, 30% testing/docs.
- **M5-6**: 50% scale, 30% monitoring, 20% polish.
- **Cadence**: Weekly reviews; bi-weekly demos.
- **Tools**: GitHub Projects, pytest, Ruff/Mypy.

## Risks (Overall)
- **High**: Flakiness/CI fails → Seeds/timeouts.
- **Medium**: Dep conflicts → Pip-tools/tox.
- **Low**: Hardware → GitHub runners.
- **Buffer**: 20% per phase.

This is now implemented as ROADMAP.md. Next: Proceed to Phase 1 Task 1 (pin deps)—I'll suggest exact pyproject.toml changes in a follow-up MD patch file.
