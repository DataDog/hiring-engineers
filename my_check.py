from datadog_checks.base import AgentCheck
from random import randint

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

class MyCheck(AgentCheck):
    def check(self, instance):
        random_val = randint(1, 1000)
        self.gauge('rkiesler.my_metric', random_val)