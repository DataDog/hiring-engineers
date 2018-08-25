from checks import AgentCheck
import random

# Custom Checks are inherit AgentCheck
class MyCheck(AgentCheck):
    
    # Automatically send a metric
    def check(self, instance):
     
        # We've chosen my_metric with a random value between 0 and 1000
        self.gauge('hiring.my_metric', random.randint(0, 1000))

