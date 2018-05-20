import time
import random
from checks import AgentCheck
class MyMetric(AgentCheck):
    def check(self, instance):
            value = random.randint(0, 1000)
            self.gauge('my_metric', value)
            time.sleep(45)