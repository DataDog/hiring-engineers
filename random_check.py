from checks import AgentCheck
import random
class RandomCheck(AgentCheck):
    def check(self, instance):
        self.count('test.support.random', random.random())