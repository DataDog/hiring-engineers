from checks import AgentCheck
from random import randint
import time

class HelloCheck(AgentCheck):
    def check(self, instance):
        time.sleep(45)
        self.gauge('my_metric', randint(1,1000))

