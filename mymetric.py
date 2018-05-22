import random
from checks import AgentCheck
class MyCheck(AgentCheck):
#  def randomize(x):
#    for x in range(1):
#    print random.randint(1,1001)
  def check(self, instance):
    name = instance['name']
    self.gauge(name, random.randint(1,1001))
