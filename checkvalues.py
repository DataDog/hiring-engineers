from checks import AgentCheck
import random
import time
class MetricCheckk(AgentCheck):
  def check(self, instance):
	self.gauge('my_metric', random.randint(0,1001))