import random

from checks import AgentCheck

class RandomTestCheck(AgentCheck):
	def check(self, instance):
		self.gauge('test.support.random', random.random())