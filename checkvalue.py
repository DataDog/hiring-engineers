from checks import AgentCheck
import random
class HelloCheck(AgentCheck):
	def check(self, instance):
			self.gauge('my_metric2', random.randint(0,1000))