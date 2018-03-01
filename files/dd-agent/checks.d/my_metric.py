# tsn - tech challenge 2018
from checks import AgentCheck
import random
class my_metric(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric.my_metric', random.randint(0,1000), tags=['test_tag'])
