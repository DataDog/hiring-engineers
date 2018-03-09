import random

from checks import AgentCheck

class HelloCheck(AgentCheck):
    def check(self, instance):
    	n = random.randint(1, 1000)
        self.gauge('my_metric', n)
