#!/usr/bin/python

import random

# the following try/except block will make the custom check compatible with any Agent version
try:
    from datadog_checks.base import AgentCheck
except ImportError:
    from checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

class MyCheck(AgentCheck):
    def check(self, instance):
        value = random.randrange(0,1000)
        self.gauge('my_metric', value=value)
