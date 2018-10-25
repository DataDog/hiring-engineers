from checks import AgentCheck
from random import randint
import time
class CustomAgentCheck(AgentCheck):
  def check(self, instance):
    random_num = randint(0, 1000)
    self.gauge('my_metric', random_num)
    time.sleep(45)

