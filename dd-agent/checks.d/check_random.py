import random

from checks import AgentCheck


class CheckRandom(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randrange(0, 1000))
