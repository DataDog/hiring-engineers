

from random import *
# the following try/except block will make the custom check compatible with any Agent version

try:
    # first, try to import the base class from old versions of the Agent...

    from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later

    from datadog_checks.checks import AgentChecks

# content of the special variable __version__ will be shown in the Agent status page

__version__ = '1.0.0'

class RandomCheck(AgentCheck):
    def check(self, instance):
        value = randint(0,1000)
        self.gauge('my_metric', value)