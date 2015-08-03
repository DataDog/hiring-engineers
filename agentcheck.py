from checks import AgentCheck
import random

class Check(AgentCheck):
	"""Samples a random value using 'test.support.random' as the metric"""
	def check(self, instance):
		self.gauge('test.support.random', random.random())