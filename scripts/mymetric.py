import random
from checks import AgentCheck

class HelloCheck(AgentCheck):
  def check(self, instance):
    self.gauge('hello.world', random.randint(0, 1000))
