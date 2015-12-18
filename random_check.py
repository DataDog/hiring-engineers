__author__ = 'stephenlechner'

# This file sends a random metric to datadog through a custom agent-check.
# It can only be run through the agent. In order for it to run, this file must 
# be placed in the "check.d" directory, and the file "random_check.yaml" must 
# be placed in the "conf.d" directory.

from random import random
from checks import AgentCheck


class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random())
