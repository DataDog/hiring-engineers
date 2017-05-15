import random

from checks import AgentCheck
class RandomCheck(AgentCheck):
    def check(self, instance):
        print('test.support.random', random.random())
