import random
from checks import AgentCheck


class RandomCheck(AgentCheck):
    def check(self, instance):
        rand_num = random.randint(1, 1000)
        self.gauge('my_metric', rand_num)
