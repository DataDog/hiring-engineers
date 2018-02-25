import random
from checks import AgentCheck

class MetricCheck(AgentCheck):
	def check(self, instance):
		self.gauge('my_metric', random.randint(1, 1000))
