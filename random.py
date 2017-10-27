from checks import AgentCheck
import random
class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('rand.num', random.randint(0, 1000))