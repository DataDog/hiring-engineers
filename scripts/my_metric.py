import random
from checks import AgentCheck

class HelloCheck(AgentCheck):
  def check(self, instance):
    self.gauge('my_metric', random.randint(0, 1000))
