import random

from checks import AgentCheck
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('raimbault.my_metric', random.uniform(0,1000))
