# sample random value check 

from checks import AgentCheck
import random, time

class RandomValCheck(AgentCheck):
    def check(self, instance):
        self.histogram('test.support.random', random.random())


