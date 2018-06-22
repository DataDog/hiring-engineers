

import random 

from checks import AgentCheck
class MyRandNum(AgentCheck):
  def check(self, instance):
	rand_num = random.randint(1,1000)
	self.gauge('My_Rand_Num', rand_num)
