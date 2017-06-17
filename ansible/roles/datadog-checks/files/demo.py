from checks import AgentCheck
import random

class DemoCheck(AgentCheck):
    def check(self, instance):
        totes_random = random.random()
        self.gauge('test.support.random', totes_random, tags=['thematthewgreen', 'tag_set_in_custom_check'])

if __name__ == '__main__':
    check, instances = DemoCheck.from_yaml('/etc/dd-agent/conf.d/demo.yaml')
    for instance in instances:
        print 'Metrics: %s' % (check.get_metrics())
