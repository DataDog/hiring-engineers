#!/usr/bin/env python

__version__="1.0.0.1"

from checks import AgentCheck
from random import randint
class MyMetricCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(0, 1000))
