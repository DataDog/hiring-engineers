from checks import AgentCheck
import random
class RandomValueCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())
