try:
    import random
    from checks import AgentCheck
except ImportError as e:
    pass


class RandomCheck(AgentCheck):

    def check(self, instance):

        rand = random.random()
        self.gauge('test.support.random', rand, tags=['random_check'])
