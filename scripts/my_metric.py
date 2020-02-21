try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck
import random
__version__ = "1.0.0"


class MyMetric(AgentCheck):
    def check(self, instance):
        timing = random.randint(0, 1000)
        self.gauge('heroku.my_metric', timing, tags=['service:heroku'])
