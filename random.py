import random
from checks import AgentCheck

class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.random', random.random())
#built using hello.world example on http://docs.datadoghq.com/guides/agent_checks/
