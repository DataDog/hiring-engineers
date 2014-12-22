from checks import AgentCheck
import random
class support(AgentCheck):
    def check(self, instance):
        x = random.random()
        self.gauge('test.support.random', x)