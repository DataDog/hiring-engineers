from random import randint

try:
    from checks import AgentCheck
except ImportError:
    from datadog_checks.checks import AgentChecks

__version__ = '1.0.0'

class MetricCheck(AgentCheck):
    def check(self, instance):
        value = randint(0,1000)
        self.gauge('my_metric', value)
