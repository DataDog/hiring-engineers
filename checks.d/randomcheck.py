import random

from checks import AgentCheck
class RandomCheck(AgentCheck):
    def check(self, instance):
    #    print('test.support.random', random.random())
    #     self.service_check('test.support.random', message='test.support.random:', random.random())
    # currentRandom=random.random()
    
     self.gauge('test.support.random', random.random())


