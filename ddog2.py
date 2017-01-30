import argparse
import random
import time
from dogapi import dog_http_api as api

########
# SETUP
########
api.api_key = '3a79a29a47c7fed3e1ad3bf0fb824218'
api.application_key = '74c64ae146e2bb0600ce4606c342829092a01f3d'
tag1="support"

# initiaalize CLI parser 
parser = argparse.ArgumentParser(description='send variety of data to datadog', add_help=True)
parser.add_argument('--event', action="store_true", dest="do_event", default=False)
parser.add_argument('--metric', action="store_true", dest="do_metric", default=False)
ns = parser.parse_args()

# randomly generate value to be sent as metric + add tag
def send_metric(t):
	while 1:
		# Submit a single point with a timestamp of `now`
		# for each page
		for p in ['home', 'signin', 'signup', 'create', 'update', 'delete']:
			# setup page meta date
			pg='page:'+p
			page_counter=0
			# do page view for page pg (e.g page.home)
			rval=random.randint(1000, 1000000)
			api.metric('page.views', rval, tags=[t, pg])
			print(pg, "page.views ", rval)
			# do page count for pg
			page_counter+=rval
			print('page_counter', page_counter, pg, "page.views ", rval)
			api.metric('page.counter', page_counter, tags=[t,pg], metric_type='counter')
			# do latentcy for pg
			rval=random.randint(10000, 100000)
			api.metric('page.latency', rval, tags=[t, pg])
			print(pg, "page.latency", rval)
		#
		time.sleep(5)

if ns.do_event:
	# do event
	title = "Eva appears in ze Garden. from Py !"
	text = 'Dude, Eva just popped in, from Py!'
	# tags = ['version:1', 'application:web']
	# All optional parameters are specified as keyword arguments.
	api.event_with_response(title, text)
elif ns.do_metric:
	# do all metrics at once
	send_metric(tag1)
else:
	print("invalid usage.")
	parser.print_help()