__version__ = "1.0"

from checks import AgentCheck
import random

class MyAgentCheck(AgentCheck):
	def check(self, instance):
		self.gauge('my_metric', random.randint(1, 1001))
