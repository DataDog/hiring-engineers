from checks import AgentCheck 
from random import randint

class mymetric(AgentCheck):
        def check(self, instance):
                random1000 = randint(0,1000)
                self.gauge('my_metric', random1000)