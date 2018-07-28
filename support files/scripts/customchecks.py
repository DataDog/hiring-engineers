from datadog_checks.checks import AgentCheck
from random import randrange

class RandomCheck(AgentCheck):
    def check(self, instance):
		self.gauge('my_metric', randrange(0, 1000))