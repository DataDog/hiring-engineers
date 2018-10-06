# Author: Abdullah Khan
# Purpose: Writing a custom check following the tutorial:
#   https://docs.datadoghq.com/developers/agent_checks/?tab=agentv6

from checks import AgentCheck

# HelloCheck inherits from AgentCheck
class HelloCheck(AgentCheck):
    def check(self, instance):
        # Every time hello.world is called, it sends a gauge of '1'.
        self.gauge('hello.world', 1)