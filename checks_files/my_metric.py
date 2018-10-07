# Author: Abdullah Khan

__version__ = "0.0.1"

from checks import AgentCheck
from random import SystemRandom

# HelloCheck inherits from AgentCheck
class my_metric_check(AgentCheck):
    '''
    A custom check that submits a metric named "my_metric" with a random value
    between 0 and 1000.
    '''
    def check(self, instance):
        self.gauge('my_metric', SystemRandom().randint(0,1000), tags=['rng'])
