""" Custom AgentCheck """
from checks import AgentCheck
from random import random


class CustomCheck(AgentCheck):
    """ Simple check for sending a random value """

    def check(self, instance):
        value = random()
        self.log.info("Generated random value: '%s'" % value)
        self.gauge('test.support.random', value)
