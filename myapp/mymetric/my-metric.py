from datadog import initialize, statsd
import time
import random
import os

options = {
    'statsd_host':os.environ['DD_AGENT_HOST'],
    'statsd_port':8125
}

initialize(**options)

i = 0

while(1):
  i += 1
  r = random.randint(0, 1000)
  statsd.gauge('mymetric',r , tags=["environment:dev"])
  time.sleep(int(os.environ['interval']))