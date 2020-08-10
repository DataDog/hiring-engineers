# /etc/datadog-agent/checks.d/hello.py
# agent check that submits a random number between 0 and 1000.

import random

try:
    from datadog_checks.base import AgentCheck
except ImportError:
    from checks import AgentCheck

__version__ = "1.0.0"

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('hello.world', random.randint(0,1000), tags=['foo:bar'])