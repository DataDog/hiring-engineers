from checks import AgentCheck
import random
class my_metric(AgentCheck):
  def check(self, instance):

    randomNumber = random.randint(0, 1000)

    self.gauge('my_metric', randomNumber)
