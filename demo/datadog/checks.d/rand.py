import random
from checks import AgentCheck
class RandCheck(AgentCheck):
    def check(self, instances):
        self.gauge('test.support.random', random.random())
