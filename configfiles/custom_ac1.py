# William Karges custom Agent Check

# Uses python 'random' function with data dog 'guage' metric submission to
# submit my_metric with a random integer value between 0 and 1000.

# The custom .yaml file sets this Agent Check to run every 45 seconds.

import random

try:
	from datadog_checks.base import AgentCheck
except ImportError :
	from checks import AgentCheck
	
__version__ = "1.0"

class myCheck(AgentCheck):
	def check(self, instance):
		self.gauge('my_metric', random.randint(0, 1000), tags=['env:test','ac:mycheck','checktype:guage'])