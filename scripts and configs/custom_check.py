# Project: Custom check script to send a random number to datadog
import random


try:
    from datadog_checks.base import AgentCheck
except ImportError:
    from checks import AgentCheck



class HelloCheck(AgentCheck):
    def check(self, instance):
        num = random.randint(1,1000)
        self.gauge('my_metric', num, tags=['metric:custom_check3'])
