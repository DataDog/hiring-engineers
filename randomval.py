import random
from time import sleep
from checks import AgentCheck

class RandomValue(AgentCheck): #class definition
    def check(self, instance):
	while True:
	    self.gauge('test.support.random', random.random()) #this sends a random value for the metric 'test.support.random'
	    time.sleep(20)   #send the random value every 20 seconds
