import random
import time
from checks import AgentCheck


class MyCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my metric value', random.randint(1, 1000))
