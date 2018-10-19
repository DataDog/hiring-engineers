__version__ = "1"

from checks import AgentCheck
from random import randint

class my_metricCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(0, 1000))


        def check(self, instance):
    if time.time() - self.last_collection < 5 * 60: # 5 minutes 
        self.log.debug("Check ran less than 5 min ago, not running it")
        return

    self.last_collection = time.time()
    self.actually_process_check(instance)