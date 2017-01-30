import random
from checks import AgentCheck


class random_number_check(AgentCheck):

    def check(self, instance={}):
        self.gauge('test.support.random', random.random(), tags=['random_num'])


if __name__ == '__main__':
    check, instances = random_number_check.from_yaml('/Users/janak/.datadog-agent/agent/conf.d/random_number_check.yaml')
    check.check()
