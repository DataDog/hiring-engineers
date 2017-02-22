from checks import AgentCheck 
import random
class RandCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())