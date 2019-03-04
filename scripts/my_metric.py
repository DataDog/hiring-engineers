#!/usr/bin/python
import random
from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

class My_Metric(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric',random.randint(0,1000))