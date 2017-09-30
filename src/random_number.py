import time
from urllib import urlopen
from checks import AgentCheck

class RandomCheck(AgentCheck):
    def check(self, instance):
	# Retrieve random number from numbersapi
	url = urlopen('http://numbersapi.com/random?min=0&max=1000').read()
	
	# Extract the number
	first_space = url.find(' ')
	random_nr = url[:first_space]

	# Send event if number < 100
	if int(random_nr) < 100:
                self.interesting_event(url, random_nr)
       	
	# Send metric
	self.gauge('my_metric', int(random_nr))
	
    def interesting_event(self, event_text, the_number):
	# Send event
	self.event({
            'timestamp': int(time.time()),
            'event_type': 'random_check',
            'msg_title': 'Interesting fact about the number ' + the_number,
            'msg_text': event_text,
            'aggregation_key': 'Interesting Fact'
      	})
