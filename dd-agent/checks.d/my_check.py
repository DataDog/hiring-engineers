import random
from checks import AgentCheck

class MyMetricCheck(AgentCheck):
    def check(self, instance):
        random.seed()
        self.gauge('my_metric', random.randint(0,1000))
