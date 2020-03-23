import random

try:
    from datadog_checks.base import AgentCheck
except ImportError:
    from checks import AgentCheck

__version__ = "1.0.0"


# When everything started
random.seed( 2010 )

class CustomMetricCheck(AgentCheck):
    def check(self, instance):
        random_number = random.randint(0, 1000)
        self.gauge('my_metric', random_number, tags=['owner:abruneau', 'role:the_next_datadog_se'])

