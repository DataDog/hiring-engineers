from checks import AgentCheck
class HelloCheck(AgentCheck):
    def check(self,instance):
        self.gauge('my_metric', 777)
