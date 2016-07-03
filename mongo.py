from checks import AgentCheck
import random


class TestCheck(AgentCheck):

	SOURCE_TYPE_NAME = 'mongodb'

	SERVICE_CHECK_NAME = 'test.support.random'

	def check(self,instance):
		self.gauge('test.support.random', random.random(), tags=['kevin3'])
		self.increment('test.support.random', random.random())
		sel.log.info('mongo')
