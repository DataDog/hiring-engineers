import random

from checks import AgentCheck
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('hello.world', 1)
        self.gauge('my_metric', random.randint(0,1001))