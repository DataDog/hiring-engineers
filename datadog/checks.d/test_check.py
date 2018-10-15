__version__ = "1.0.0"

from checks import AgentCheck
import random
class HelloCheck(AgentCheck):
    def check(self, instance):
        some_num = random.randint(1,1001)
        self.gauge('my_metric', some_num, tags=['test_check'])

