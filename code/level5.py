from checks import AgentCheck
from random import random


class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge("test.support.random", random())