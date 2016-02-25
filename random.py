import random

from checks import AgentCheck


class RandomCheck(AgentCheck):
     def check(self, instance):
         randomNum = random.random()
         self.gauge('test.support.random', randomNum)
