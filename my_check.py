import random

try:
    from checks import AgentCheck
except ImportError:
    from datadog_checks.checks import AgentCheck


__version__ = "1.0.0"


class MyCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0, 1001))