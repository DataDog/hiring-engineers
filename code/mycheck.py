from checks import AgentCheck
from random import *


class MyAgentCheck(AgentCheck):
    def check(self, instance):
        self.gauge('se-exercise.my_metric', randint(0, 1000))