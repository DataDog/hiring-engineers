import random

from checks import AgentCheck
class MyMetric(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randrange(0, 1001, 1))