__version__="1.0.0"
import time
import random

from checks import AgentCheck

class CheckDemo(AgentCheck):
   def check(self, instance):
      #Open our delay file and read in the current collection interval
      delay_file = open ('/etc/datadog-agent/checks.d/CheckDemo.delay', 'r') 
      collect_interval = int(delay_file.read())

      #The first time we run the check, we need to create the last_collection attribute
      #By creating it as current time - the collection interval, we guaruntee we run
      #the check the first time
      if not hasattr(self, 'last_collection'):
         self.last_collection = time.time() - collect_interval

      #Check to see if we've already submitted the check within the collection interval
      if time.time() - self.last_collection <= collect_interval:
        #If we're not going to submit the check, send a log message
        self.log.info('Not submitting check because custom collection interval not met. Current collection interval is set to: %d' % collect_interval)
        delay_file.close()
        return

      delay_file.close()
      #Since we're going to submit the metric, update the last collection time
      self.last_collection=time.time()
      
      #Get our random number and call the gauge method to send in our metric
      random_nbr = random.randint(1,1001)
      self.gauge('my_metric', random_nbr)
