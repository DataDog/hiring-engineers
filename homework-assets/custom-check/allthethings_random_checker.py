import random
from checks import AgentCheck
class AllTheThingsRandomChecker(AgentCheck):
    def check(self, instance):
        self.gauge('allthethings.checker.random', random.randrange(0, 1000))