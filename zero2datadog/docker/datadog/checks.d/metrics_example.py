import random
from datadog_checks.base import AgentCheck

__version__ = "1.0.0"

""" Create a custom agent check that sends all metrics periodically.

    https://docs.datadoghq.com/developers/metrics/agent_metrics_submission/?tab=count#tutorial
"""
class MyClass(AgentCheck):
    def check(self, instance):
        self.gauge(
            "my_metric",
            random.randint(0, 1000),
            tags=["env:dev",
                  "admin_email:jitkelme@gmail.com",
                  "project:zero2datadog",
                  "metric_submission_type:gauge"],
        )


