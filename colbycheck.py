import random
from checks import AgentCheck
class RandomCheck(AgentCheck):
 def check(self, instance):
  self.gauge('my_metric', random.randint(0,1000))
