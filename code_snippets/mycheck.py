from checks import AgentCheck
import random

class MyCheck(AgentCheck):
    def check(self, instance):
      rand = random.randint(0,1001)
      print(rand)
      self.gauge('my_metric', rand)