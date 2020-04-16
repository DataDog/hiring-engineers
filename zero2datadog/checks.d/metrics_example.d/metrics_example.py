import random

from datadog_checks.base import AgentCheck

__version__ = "1.0.0"

""" Create a custom agent check that sends all metrics periodically.

    https://docs.datadoghq.com/developers/metrics/agent_metrics_submission/?tab=count#tutorial
"""
class MyClass(AgentCheck):
    def check(self, instance):
        self.count(
            "example_metric.count",
            2,
            tags=["env:dev", "metric_submission_type:count"],
        )
        self.count(
            "example_metric.decrement",
            -1,
            tags=["env:dev", "metric_submission_type:count"],
        )
        self.count(
            "example_metric.increment",
            1,
            tags=["env:dev", "metric_submission_type:count"],
        )
        self.rate(
            "example_metric.rate",
            1,
            tags=["env:dev", "metric_submission_type:rate"],
        )
        self.gauge(
            "example_metric.gauge",
            random.randint(0, 10),
            tags=["env:dev", "metric_submission_type:gauge"],
        )
        self.monotonic_count(
            "example_metric.monotonic_count",
            2,
            tags=["env:dev", "metric_submission_type:monotonic_count"],
        )

        # Calling the functions below twice simulates
        # several metrics submissions during one Agent run.
        self.histogram(
            "example_metric.histogram",
            random.randint(0, 10),
            tags=["env:dev", "metric_submission_type:histogram"],
        )
        self.histogram(
            "example_metric.histogram",
            random.randint(0, 10),
            tags=["env:dev", "metric_submission_type:histogram"],
        )
