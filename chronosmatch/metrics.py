"""Latency and throughput measurements."""
from __future__ import annotations
import statistics
import time


class Metrics:
    def __init__(self):
        self.latencies_us = []
        self.started_ns = time.perf_counter_ns()
        self.finished_ns = self.started_ns
        self.processed = 0
        self.filled_units = 0

    def record(self, enqueue_ns: int, fill_units: int):
        now = time.perf_counter_ns()
        self.latencies_us.append((now - enqueue_ns) / 1000.0)
        self.finished_ns = now
        self.processed += 1
        self.filled_units += fill_units

    @staticmethod
    def percentile(values, p):
        if not values:
            return 0.0
        ordered = sorted(values)
        index = min(len(ordered) - 1, max(0, int((p / 100) * len(ordered) + 0.999999) - 1))
        return ordered[index]

    def report(self):
        elapsed = max((self.finished_ns - self.started_ns) / 1e9, 1e-9)
        vals = self.latencies_us
        return {
            "processed": self.processed,
            "elapsed_s": elapsed,
            "throughput_ops_s": self.processed / elapsed,
            "latency_avg_us": statistics.fmean(vals) if vals else 0.0,
            "latency_p50_us": self.percentile(vals, 50),
            "latency_p95_us": self.percentile(vals, 95),
            "latency_p99_us": self.percentile(vals, 99),
            "filled_units": self.filled_units,
        }
