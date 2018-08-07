import random
from checks import AgentCheck
class my_metricCheck(AgentCheck):
  def check(self, instance):
  
    data=random.randrange(0, 1000, 1)

    self.gauge('my_check.update.value', data)

