from checks import AgentCheck

class SampleCheck(AgentCheck):
    def random_sample(self):
        import random
        return random.random()

    def check(self, instance):
        self.gauge('test.support.random', self.random_sample())
