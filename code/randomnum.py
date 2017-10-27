import random
from checks import AgentCheck

class RandomNumCheck(AgentCheck):
    def check(self, instance):
       self.gauge('my_metric', random.random()*1000)
