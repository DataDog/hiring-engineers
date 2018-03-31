from checks import AgentCheck
from random import randint

class MyCheck(AgentCheck):
    def check(self, instance):
        randomNumber = randint(0, 1000)
        self.gauge('my_metric', randomNumber)
