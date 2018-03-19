from checks import AgentCheck
from random import randint
class my_metric(AgentCheck):
    def check(self, instance):
         self.gauge('My.Metric', randint(0,1000)) #gauge function to push the metrics to DataDog
		 


 