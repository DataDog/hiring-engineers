from checks import AgentCheck
import random
class HelloCheck(AgentCheck):
    def check(self, instance):
        randInt = random.randint(0, 1000)
        self.count('my_metric', randInt)