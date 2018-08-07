
from checks import AgentCheck
from random import randint

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(0,1000))
