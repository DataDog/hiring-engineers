"""
AgentCheck generates a random value between 0 and 1000 for SE test.
Author:
  Mike McLaughlin
"""

import random # for generating a random number

# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from old versions of the Agent...
    from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck

__version__ = "1.0.0"

class RandomValueCheck(AgentCheck):
    """
    Datadog AgentCheck object for SE test.  This agent check submits a new metric
    named my_metric with a random value between 0 and 1000.
    """
    def check(self, instance):
        """
        check() submits a random value between 0 and 1000
        """
        self.gauge('my_metric', random.randint(0, 1001))
