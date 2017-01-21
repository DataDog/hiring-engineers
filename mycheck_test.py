from checks import AgentCheck
import random

class Mytestcheck(AgentCheck):
    def check(self, instance):
	testmetric = random.random()
        self.gauge('test.support.random', testmetric)