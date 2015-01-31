# stdlib
import random

# project
from checks import AgentCheck

class RandomCheck(AgentCheck):
    
    def check(self, instance):
        rand = random.randint(0,100)
        self.gauge('test.support.random', rand)