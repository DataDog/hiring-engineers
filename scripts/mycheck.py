from datadog_checks.base import AgentCheck
from checks import AgentCheck
import random

class MyCheck(AgentCheck):
  def check(self, instance):
    self.gauge('mycheck', random.randrange(1000))
