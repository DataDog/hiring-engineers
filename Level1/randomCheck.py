# Script run by crontab every minute.
import random
from datadog import statsd

# Report random value to test.support.random tag. 
metric = 'test.support.random'
value = random.random()

statsd.gauge(metric=metric,value=value)