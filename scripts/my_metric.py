
from checks import AgentCheck
import random

class MyMetricCheck(AgentCheck):
    def check(self, instance):
            self.gauge('my_metric', random.randint(1,1000))
