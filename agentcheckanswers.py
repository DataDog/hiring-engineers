#3 #I used stackoverflow.com for help with this 
from checks import AgentCheck
import random

class HTTPCheck(AgentCheck):
    def check(self, instance):
        if 'url' not in instance:
            return
        self.count("my_metric", random.randint(0,1000))

#4 #I used stackoverflow.com for help with this 

from checks import AgentCheck
import random
import sched, time
s = sched.scheduler(time.time, time.sleep)

class HTTPCheck(AgentCheck):
    def check(self, instance):
        if 'url' not in instance:
            return
        self.count("my_metric", random.randint(0,1000))
        s.enter(45, 1, AgentCheck, (sc,))

s.enter(45, 1, AgentCheck, (s,))
s.run()


