from checks import AgentCheck
from random import randint

class MyMetricCheck(AgentCheck):
  def check(self, instance):
    num = randint(1, 1000)
    self.gauge('app.my_metric', num)
