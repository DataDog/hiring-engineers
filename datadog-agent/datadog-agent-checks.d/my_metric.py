import random
# ...if the above failed, the check is running in Agent version 6 or later
from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"


# Metric returning a random int from 0 to 1000
class MyMetric(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000))
