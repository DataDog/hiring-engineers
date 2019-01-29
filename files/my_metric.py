#This file was created in checks.d directory under datadog-agent directory
from checks import AgentCheck
import random

__version__ = "1.0.0"

class MetricCheck(AgentCheck):
        def check(self, instance):
                self.gauge('my_metric',random.randint(0,1000))

