import random

from checks import AgentCheck


class RandomCheck(AgentCheck):
    """ Create a random sample. """

    def check(self, instance):
        self.gauge('test.support.random', random.random())