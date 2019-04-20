import random
try:
    from checks import AgentCheck
except ImportError:
    from datadog_checks.checks import AgentCheck

__version__ = "1.0.0"

class AjpCheck(AgentCheck):
    def check(self, instance):
        self.gauge('ajp.my_metric', random.randint(0, 1001), tags=['TAG_KEY:TAG_VALUE'])
