try:
    from datadog_checks.base import AgentCheck
except ImportError:
    from checks import AgentCheck

import random

__version__ = "1.0.0"

class my_metric(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(1,1000), tags=['TAG_KEY:TAG_VALUE'])


