import random
from checks import AgentCheck

class HelloCheck(AgentCheck):
	def check(self, instance):
		number = random.random()
		self.gauge('test.support.random', number)

