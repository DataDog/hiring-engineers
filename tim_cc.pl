import random
from checks import AgentCheck

class rndValue(AgentCheck):
	
	def check(self, instance):
	
		rndvalue = random.random()
		self.gauge('test.support.random', rndvalue)
		