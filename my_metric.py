import random

from datadog_checks.checks import AgentCheck

class CustomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('custom.mycheck', random.randint(0,1000))