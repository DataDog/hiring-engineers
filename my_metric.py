import random
import datadog_checks.base import AgentCheck

class MyCheck(AgentCheck):
      def check(self, instance):
              self.gauge('my_metric', random.randint(0, 1000))
