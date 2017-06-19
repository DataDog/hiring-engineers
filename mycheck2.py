from checks import AgentCheck

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('test.support.max', 0.9)		