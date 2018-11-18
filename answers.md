1. Tag Assignment

![alt text](https://github.com/cconerby/hiring-engineers/blob/master/1_Assigning_Tags.JPG)

2. MongoDB Integration:

![alt text]https://github.com/cconerby/hiring-engineers/blob/master/2_MongoDB_Instrumented_2.JPG

![alt text](https://github.com/cconerby/hiring-engineers/blob/master/2_MongoDB_Instrumented.JPG)

3. Custom_Agent_Random_Code.py
```
import random
from checks import AgentCheck
class HelloCheck(AgentCheck):
  def check(self, instance):

        x = random.randint(1, 1000)

        self.gauge('random.number', x)
```
4. Custom Agent Metrics with 45 Second Interval:

![alt text](https://github.com/cconerby/hiring-engineers/blob/master/3_4_Custom_Agent_My_Metric_45_Seconds.JPG

5. Bonus Question:
  You can change the check collection interval with the agent manager within Windows.(GUI)
