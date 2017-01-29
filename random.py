from checks import AgentCheck
import random
class RandomCheck(AgentCheck):
    def check(self, instance):
        random_value = random.random()
        self.gauge('test.support.random', random_value)
