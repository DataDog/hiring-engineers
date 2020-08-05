import random
from datadog_checks.base import AgentCheck

class TestSupportRandom(AgentCheck):
  def check(self, instance):
    val = random.randrange(1,1000)
    self.gauge('test.support.random',val)
