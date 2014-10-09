import random
from checks import AgentCheck
class RandomCheck(AgentCheck):
    def __init__(self, name, init_config, agentConfig):
        AgentCheck.__init__(self, name, init_config, agentConfig)
        self.log.info("Initializing custom check %s" % self.__class__)
        self.key='test.support.random'

    def check(self, instance):
    	self.log.info("Custom check %s called" % self.__class__)
    	rVal = random.random()
    	tagList=['support']
        self.log.info("%s %s %s", self.key, rVal, tagList)
        self.gauge(self.key, rVal, tagList)