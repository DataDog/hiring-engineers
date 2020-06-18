# the following try/except block will make the custom check compatible with any Agent version
import random

from random import randint
try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

class MyMetric(AgentCheck):
    def check(self, instance):
    	randomValue = randint(0,1000)
        self.gauge('my.metric', randomValue, tags=['test:my_new_key'])