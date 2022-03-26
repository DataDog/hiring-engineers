from checks import AgentCheck
import random
class myMetric(AgentCheck):
    def check(self, instance):
        random_num = random.randint(0,1000)
        self.gauge('my_metric', random_num)
