from Checks import AgentCheck
import random 


class HelloCheck(AgentCheck):
  def check(self, instance):
    self.count('my_metric', random.randint(0,1000))