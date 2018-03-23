from checks import AgentCheck
import random

class MyMetric(AgentCheck):
    def check(self, instance):
        random.seed()
        gauge_val = random.randint(0,1000)
        self.gauge('my_metric', gauge_val)
