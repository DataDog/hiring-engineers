import random
from checks import AgentCheck

class MyRandomCheck(AgentCheck):
    def check(self, instance):
	self.gauge('test.support.random', random.random())
