
from datadog_checks.base import AgentCheck
import random

__version__ = "1.0.0"

class MyCheck(AgentCheck):
        def check(self,instance):
                self.gauge("test_metric", random.uniform(0,1000), tags=["team:techtest"])