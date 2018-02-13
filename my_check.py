from random import *
from checks import AgentCheck

class RandomNum(AgentCheck):
    def check(self, instance):
	random_num = randint(1, 1000)    # Pick a random number between 1 and 1000.
        self.gauge('hvd.my_metric', random_num, tags=['my_metric'])

if __name__ == '__main__':
    check, instances = HTTPCheck.from_yaml('/etc/dd-agent/conf.d/my_check.yaml')
    check.check(instance)
    print 'Metrics: %s' % (check.get_metrics())
