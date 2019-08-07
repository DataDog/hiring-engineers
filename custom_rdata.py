from checks import AgentCheck
from random import randint
__version__ = "1.0.0"
class rdata(AgentCheck):
    def check(self, instance):
        self.gauge('rdata.my_metric', randint(0,1000))

