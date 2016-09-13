import random

from checks import AgentCheck

#Third Party
import whois

class RandomGen(AgentCheck):
    def check(self, instance):
        num = random.randrange(0,100)/100.0
        self.gauge('test.support.random', num)
        self.gauge('test.support.random.inverse', 1-num)
