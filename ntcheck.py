from datadog_checks.checks import AgentCheck
import random

class NTCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000), tags=['TAG_KEY:TAG_VALUE'])
