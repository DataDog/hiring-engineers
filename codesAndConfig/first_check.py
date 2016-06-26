from checks import AgentCheck
import random
def randomValue():
    return random.random()

class RandomSampleCheck(AgentCheck):
    def check(self, instance):
        self.gauge("test.support.random",randomValue())
