import random
from checks import AgentCheck

class my_metric(AgentCheck):
    def check(self, instance):
        randvalue=random.randint(0, 1000)
        self.gauge('my_metric', randvalue)