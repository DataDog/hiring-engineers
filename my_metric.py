from checks import AgentCheck
import random

class MyMetricCheck(AgentCheck):
    def check(self, instance):
        min = 0
        max = 1000
        metric = random.randint( min, max)

        self.gauge('my_random_check', metric)
