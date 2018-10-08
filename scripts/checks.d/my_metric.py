from checks import AgentCheck
import random

class my_metric(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', str(random.randint(1,1001)))

