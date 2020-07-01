# Reference: https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7
# The following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck

__version__ = "1.0.0"

import random


class MyMetricCheck(AgentCheck):

    def check(self, instance):
        random_number = random.randint(0, 1000)
        self.gauge('random.my_metric', random_number)
