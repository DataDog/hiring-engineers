import random
from datadog_checks.base import AgentCheck

__version__ = "0.0.2"

class CustomMetricCheck(AgentCheck):
    """
    CustomMetricCheck plucks a random number between 1 & 1000.
    """
    def check(self, instance):
        my_metric = random.randrange(1001)
        self.gauge(
            'mc.my_metric', 
            my_metric, 
            tags=[]
        )