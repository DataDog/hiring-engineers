from checks import AgentCheck
from random import *

class HelloCheck(AgentCheck):
    # Source
    SOURCE_TYPE_NAME = 'my_metric'    
    def check(self, instance):
        self.gauge('my_metric', randint(1, 100))

