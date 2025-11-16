"""Metrics collection for observability."""

import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable

from src.config import get_settings


@dataclass
class Metric:
    """Represents a single metric."""

    name: str
    value: float
    tags: dict[str, str] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class MetricsCollector:
    """Collects and tracks metrics for observability."""

    def __init__(self, enabled: bool = True):
        """Initialize metrics collector."""
        self.enabled = enabled
        self.metrics: list[Metric] = []
        self.counters: dict[str, int] = defaultdict(int)
        self.timers: dict[str, list[float]] = defaultdict(list)
        self.hooks: list[Callable[[Metric], None]] = []

    def increment(self, name: str, value: int = 1, tags: dict[str, str] | None = None):
        """Increment a counter metric."""
        if not self.enabled:
            return

        self.counters[name] += value
        metric = Metric(name=name, value=float(self.counters[name]), tags=tags or {})
        self.metrics.append(metric)
        self._notify_hooks(metric)

    def record_timing(
        self, name: str, duration: float, tags: dict[str, str] | None = None
    ):
        """Record a timing metric."""
        if not self.enabled:
            return

        self.timers[name].append(duration)
        metric = Metric(name=name, value=duration, tags=tags or {})
        self.metrics.append(metric)
        self._notify_hooks(metric)

    def record_value(
        self, name: str, value: float, tags: dict[str, str] | None = None
    ):
        """Record a value metric."""
        if not self.enabled:
            return

        metric = Metric(name=name, value=value, tags=tags or {})
        self.metrics.append(metric)
        self._notify_hooks(metric)

    def add_hook(self, hook: Callable[[Metric], None]):
        """Add a hook to be called when metrics are recorded."""
        self.hooks.append(hook)

    def _notify_hooks(self, metric: Metric):
        """Notify all hooks of a new metric."""
        for hook in self.hooks:
            try:
                hook(metric)
            except Exception:
                pass  # Don't let hook errors break metrics collection

    def get_stats(self, name: str) -> dict[str, Any] | None:
        """Get statistics for a metric."""
        if name not in self.timers or not self.timers[name]:
            return None

        values = self.timers[name]
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "mean": sum(values) / len(values),
            "sum": sum(values),
        }

    def reset(self):
        """Reset all metrics."""
        self.metrics.clear()
        self.counters.clear()
        self.timers.clear()


# Global metrics collector instance
_metrics_collector: MetricsCollector | None = None


def get_metrics() -> MetricsCollector:
    """Get the global metrics collector instance."""
    global _metrics_collector
    if _metrics_collector is None:
        settings = get_settings()
        _metrics_collector = MetricsCollector(enabled=settings.enable_metrics)
    return _metrics_collector

