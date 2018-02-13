# This check will  send a pseudorandom integer

from checks import AgentCheck
from random import randint

class RandomCheck(AgentCheck):
	def check(self, instance):
		# get a random number and send it as a guaged metric to datadog
		randnum=randint(0, 1000)
		self.gauge('agent.random.num', randnum)
