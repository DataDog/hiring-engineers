from random import randint

try:
    from checks import AgentCheck
except ImportError:
    from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"


class MyMetric(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(0,1000))