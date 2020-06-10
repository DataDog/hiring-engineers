# a custom check that emits a random value

try:
	from datadog_checks.base import AgentCheck
except ImportError:
	from checks import AgentCheck

import random

__version__ = "1.0.0"

class MyCheck(AgentCheck):
	def check(self, instance):
		metric = random.randrange(1, 1000)
		self.gauge('my_check', metric, tags=['type:check'])
