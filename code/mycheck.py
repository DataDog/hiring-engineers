import random

from checks import AgentCheck

class myCheck(AgentCheck):
    def my_metric(self):
        return random.randint(0, 1000)

    def check(self, instance):
        self.gauge('my_metric', self.my_metric())