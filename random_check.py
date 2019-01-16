from datadog_checks.checks import AgentCheck
import random

__version__ = "1.0.0"

class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(1,1000))