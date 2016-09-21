import random
from checks import AgentCheck

class RandomValueCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())
