import random

try:
   from checks import AgentCheck
except ImportError:
   from datadog_check.check import AgentCheck

__version__ = "0.0.9"

class MyMetric(AgentCheck):
   def check(self, instance):
      self.gauge('my_metric', random.randint(1,1001)) 
