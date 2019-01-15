# how the  check file looks inside the checks directory

from checks import AgentCheck
import random

class MetricCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric',random.randint(0,1000))
