try:
    from checks import AgentCheck
except ImportError:
    from datadog_checks.checks import AgentCheck
import random


class MetricCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0, 1000))
