# As my Agent version is greater than 6.6.0, only `datadog_checks.base` is needed.
from datadog_checks.base import AgentCheck
import random

__version__ = "1.0.0"


class MyCheck(AgentCheck):
    def check(self, instance):
        self.gauge("my_metric", random.uniform(0, 1000), tags=["team:hiringtest"])
