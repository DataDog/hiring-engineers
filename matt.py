from checks import AgentCheck
import random

class MattCheck(AgentCheck):
  def check(self, instance):
    self.gauge('test.support.random', random.random())