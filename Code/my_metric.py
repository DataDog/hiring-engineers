from random import randint
from checks import AgentCheck

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(1,1000))
