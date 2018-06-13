from checks import AgentCheck
from random import randint

class MetricCheck(AgentCheck):
	def check(self, instance):
		randomInt = randint(0, 1000)
		self.gauge('my_metric',  randomInt)