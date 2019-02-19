from datadog_checks.checks import AgentCheck
from random import randint

__version__ = "1.0.0"


class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('custom_my_metric', randint(0, 1000))
