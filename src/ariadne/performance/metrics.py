"""Telemetry helpers for benchmarking and performance measurement."""

from __future__ import annotations

import time
import tracemalloc
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from statistics import mean, median, pstdev
from typing import Any


@dataclass
class ExecutionTelemetry:
    """Telemetry captured for a single benchmark execution."""

    backend: str
    iteration: int
    shots: int
    duration_s: float
    start_time: float
    end_time: float
    peak_memory_kb: float
    success: bool
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert telemetry data to a serialisable dictionary."""

        return {
            "backend": self.backend,
            "iteration": self.iteration,
            "shots": self.shots,
            "duration_s": self.duration_s,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "peak_memory_kb": self.peak_memory_kb,
            "success": self.success,
            "error": self.error,
        }


@dataclass
class BenchmarkSummary:
    """Aggregated statistics for a benchmark run."""

    backend: str
    iterations: int
    successes: int
    failures: int
    avg_time_s: float | None
    min_time_s: float | None
    max_time_s: float | None
    median_time_s: float | None
    std_time_s: float | None
    peak_memory_kb: float | None
    throughput_shots_per_s: float | None
    success_rate: float

    def to_dict(self) -> dict[str, Any]:
        """Convert the summary into a serialisable dictionary."""

        return {
            "backend": self.backend,
            "iterations": self.iterations,
            "successes": self.successes,
            "failures": self.failures,
            "avg_time_s": self.avg_time_s,
            "min_time_s": self.min_time_s,
            "max_time_s": self.max_time_s,
            "median_time_s": self.median_time_s,
            "std_time_s": self.std_time_s,
            "peak_memory_kb": self.peak_memory_kb,
            "throughput_shots_per_s": self.throughput_shots_per_s,
            "success_rate": self.success_rate,
        }


class BenchmarkMetricsAggregator:
    """Aggregate telemetry samples into a summary."""

    def __init__(self, backend: str, shots: int) -> None:
        self.backend = backend
        self.shots = shots
        self._telemetry: list[ExecutionTelemetry] = []

    @property
    def telemetry(self) -> Iterable[ExecutionTelemetry]:
        """Return recorded telemetry samples."""

        return tuple(self._telemetry)

    def add(self, sample: ExecutionTelemetry) -> None:
        """Record a telemetry sample."""

        self._telemetry.append(sample)

    def summary(self) -> BenchmarkSummary:
        """Compute a summary over collected telemetry."""

        iterations = len(self._telemetry)
        successes = [sample for sample in self._telemetry if sample.success]
        failures = iterations - len(successes)

        if successes:
            durations = [sample.duration_s for sample in successes]
            avg_time = mean(durations)
            min_time = min(durations)
            max_time = max(durations)
            median_time = median(durations)
            std_time = pstdev(durations) if len(durations) > 1 else 0.0
            throughput = self.shots / avg_time if avg_time > 0 else None
        else:
            avg_time = min_time = max_time = median_time = std_time = throughput = None

        peak_memory_kb = (
            max(sample.peak_memory_kb for sample in self._telemetry)
            if self._telemetry
            else None
        )

        success_rate = len(successes) / iterations if iterations else 0.0

        return BenchmarkSummary(
            backend=self.backend,
            iterations=iterations,
            successes=len(successes),
            failures=failures,
            avg_time_s=avg_time,
            min_time_s=min_time,
            max_time_s=max_time,
            median_time_s=median_time,
            std_time_s=std_time,
            peak_memory_kb=peak_memory_kb,
            throughput_shots_per_s=throughput,
            success_rate=success_rate,
        )


def measure_simulation_run(
    func: Callable[[], Any],
    *,
    backend: str,
    iteration: int,
    shots: int,
) -> tuple[Any | None, ExecutionTelemetry]:
    """Execute ``func`` while capturing performance telemetry."""

    tracemalloc.start()
    start_wall = time.time()
    start_perf = time.perf_counter()

    try:
        result = func()
        success = True
        error: str | None = None
    except Exception as exc:  # pragma: no cover - telemetry should still be recorded
        result = None
        success = False
        error = str(exc)
    finally:
        _, peak_bytes = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    end_perf = time.perf_counter()
    end_wall = time.time()

    telemetry = ExecutionTelemetry(
        backend=backend,
        iteration=iteration,
        shots=shots,
        duration_s=end_perf - start_perf,
        start_time=start_wall,
        end_time=end_wall,
        peak_memory_kb=peak_bytes / 1024,
        success=success,
        error=error,
    )

    return result, telemetry


def format_duration(duration: float | None) -> str:
    """Format a duration value for human readable output."""

    if duration is None:
        return "n/a"
    return f"{duration:.4f}s"


def format_memory(kilobytes: float | None) -> str:
    """Format a memory size in kilobytes."""

    if kilobytes is None:
        return "n/a"
    if kilobytes >= 1024:
        return f"{kilobytes / 1024:.2f} MB"
    return f"{kilobytes:.1f} KB"
