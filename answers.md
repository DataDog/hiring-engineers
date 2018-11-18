1. Tag Assignment
![alt text](https://github.com/cconerby/hiring-engineers/blob/master/1_Assigning_Tags.JPG)

2. MongoDB Instrumented:
![alt text](https://github.com/cconerby/hiring-engineers/blob/master/2_MongoDB_Instrumented.JPG)

3. Custom_Agent_Random_Code.py

import random
from checks import AgentCheck
class HelloCheck(AgentCheck):
  def check(self, instance):

        x = random.randint(1, 1000)

        self.gauge('random.number', x)
