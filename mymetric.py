import time
from random import randint
from random import seed
from checks import AgentCheck

class MyMetric(AgentCheck):
  def check(self,instance):
    now = int(time.time())
    seed(now)
    rand = randint(0, 1000)
    self.log.info(now)
    self.log.info(rand)
    self.gauge('my_metric',rand)
