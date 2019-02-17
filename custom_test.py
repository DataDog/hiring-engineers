from datadog_checks.checks import AgentCheck
from random import randint 
class CustomCheck(AgentCheck):
    def check(self,instance):
       # data = randint(0,1000)        
        self.gauge('my_metric', randint(0,1000))

