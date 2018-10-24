__version__ = "1.0.2"
import random

from checks import AgentCheck

class MyCheck(AgentCheck):
    def check(self, instance):
        timing = random.randint(0,1001) 
        self.gauge('tobel.mymetric', timing, tags=['datadogtest'])
