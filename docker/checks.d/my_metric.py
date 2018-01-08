from random import random
from checks import AgentCheck
class RandomInteger(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', 1000 * random())
