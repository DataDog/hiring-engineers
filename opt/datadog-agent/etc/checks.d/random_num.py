__version__ = "1.0.0"

from checks import AgentCheck
from random import randint

class random_num(AgentCheck):
    def check(self, instance):
        self.gauge('girish.random', randint(0,1000))
