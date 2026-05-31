"""Prometheus metrics for Phantom-Veil monitoring."""
import time
import logging
from typing import Dict
from dataclasses import dataclass, field

logger = logging.getLogger("phantom-veil.metrics")

class MetricsCollector:
    """Collect and expose Prometheus-compatible metrics."""

    def __init__(self):
        self.counters: Dict[str, int] = {}
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, list] = {}

    def inc_counter(self, name: str, value: int = 1):
        self.counters[name] = self.counters.get(name, 0) + value

    def set_gauge(self, name: str, value: float):
        self.gauges[name] = value

    def observe_histogram(self, name: str, value: float):
        self.histograms.setdefault(name, []).append(value)

    def export_prometheus(self) -> str:
        """Export metrics in Prometheus text format."""
        lines = []
        for name, value in self.counters.items():
            lines.append(f"phantom_veil_{name} {value}")
        for name, value in self.gauges.items():
            lines.append(f"phantom_veil_{name} {value}")
        for name, values in self.histograms.items():
            if values:
                lines.append(f"phantom_veil_{name}_count {len(values)}")
                lines.append(f"phantom_veil_{name}_sum {sum(values)}")
                lines.append(f"phantom_veil_{name}_avg {sum(values)/len(values)}")
        return "\n".join(lines) + "\n"

    def get_summary(self) -> dict:
        """Get metrics summary as dict."""
        return {
            "counters": self.counters.copy(),
            "gauges": self.gauges.copy(),
            "histograms": {k: {"count": len(v), "avg": sum(v)/len(v) if v else 0} for k, v in self.histograms.items()},
        }

# Global metrics instance
metrics = MetricsCollector()
