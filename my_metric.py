#!/usr/bin/python
try:
	from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

class My_MetricCheck(AgentCheck):
	def check(self, instance):
		import random
		self.gauge("my_metric",random.randint(0,1000))
