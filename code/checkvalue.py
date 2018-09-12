from checks import AgentCheck
import random

class HelloCheck(AgentCheck):
  def check(self, instance):
    instance['check_name']
    self.gauge('my_metric', random.randint(1,1000))
