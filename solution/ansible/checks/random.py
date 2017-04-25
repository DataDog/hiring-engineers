from random import random

from checks import AgentCheck

class RandomMetric(AgentCheck):
    """sends a random number > 0 < 1"""

    def check(self, instance):
        self.gauge('test.support.random', random())
