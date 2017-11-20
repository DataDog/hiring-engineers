from checks import AgentCheck 
from random import randint
import os
import time

class mymetric(AgentCheck):
        def check(self, instance):
                timestampFile = '/tmp/mymetric-timestamp'

                currentTime = time.time()
                lastTimeRan = 0
                
                if os.path.isfile(timestampFile):
                    lastTimeRan = os.path.getmtime(timestampFile)
                else:
                    openFile = open(timestampFile, 'w')
                    openFile.write('updated')
                    openFile.close()

                if lastTimeRan < currentTime - 45:
                        os.utime(timestampFile, (currentTime, currentTime))
                        random1000 = randint(0,1000)
                        self.gauge('my_metric', random1000)
                else:
                        return