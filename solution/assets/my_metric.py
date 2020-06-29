# Custom check that returns a random number between 1-1000
__version__ = "0.0.1"
import random

# Make sure AgentCheck is compatible with versions 6/7
try:
    from datadog_checks.base import AgentCheck
except ImportError:
    from checks import AgentCheck

class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge(
            "my_metric.gauge",
            random.randint(0, 1000),
            tags=["metric_submission_type:gauge"],
        )
