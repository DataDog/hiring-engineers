import random
from checks import AgentCheck
class MyCheck(AgentCheck):
    def check(self, instance):
        self.gauge('mymetric', random.randint(0,1000))