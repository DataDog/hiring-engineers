
import time
import requests
import random

from checks import AgentCheck

class SampleRandomValue(AgentCheck):
            def check(self,instance):
              self.gauge('test.support.random',random.random())
if __name__ == '__main__':    
    check, instances = SampleRandomValue.from_yaml('/path/to/conf.d/randomcheck.yaml')
    for instance in instances:
        if check.has_events():
            print 'Events: %s' % (check.get_events())
        print 'Metrics: %s' % (check.get_metrics())


