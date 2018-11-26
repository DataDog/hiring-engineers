import time
import json
import urllib2
from checks import AgentCheck

class RandomCheck(AgentCheck):
    def check(self, instance):
	# Retrieve random number from numbersapi
        request = urllib2.Request("http://192.168.0.63:8888/rest/items/Temperature_outside")
        request.add_header('Accept','application/json')
        response = urllib2.urlopen(request)
        content = response.read()
        msg  = json.loads(content)	
        temp="{:.2f}".format(float((msg["state"])))
       	
	# Send metric
	self.gauge('Temp_outside', temp,['#temperature'])
