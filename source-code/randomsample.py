from checks import AgentCheck
import random
class RandomSampleCheck(AgentCheck):
    def check(self, instance):
        self.gauge('random.sample', random.random())

