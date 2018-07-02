# from datadog-agent/checks.d

from checks import AgentCheck
from random import randint
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('hello.world', randint(0,1000))
