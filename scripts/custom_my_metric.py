from checks import AgentCheck
from random import randint

class MyMetricCheck(AgentCheck):
    def check(self, instance):
        random_number = randint(0, 1000)
        self.gauge('my_metric', random_number, tags=['metric:my_metric'])