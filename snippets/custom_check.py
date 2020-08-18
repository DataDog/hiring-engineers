import random
from datadog_checks.base import AgentCheck

__version__ = "2.0.1"

class CustomMetricCheck(AgentCheck):
    """
    CustomMetricCheck plucks a random number between 1 & 1000.
    """
    def check(self, instance):
        my_metric = random.randrange(0, 1001)
        self.gauge(
            'custom_metric.my_metric', 
            my_metric, 
            tags=[]
        )