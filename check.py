from checks import AgentCheck
import random

class RandomCheck(AgentCheck):
    def check(self, instance):
        rand = random.randint(0, 1001)
        self.gauge('my_metric', rand)