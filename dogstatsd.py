from datadog import statsd, initialize, api
import time

def latency(page_tag):
	""" Creates histogram showing latency """
	start = time.time()
	duration = time.time() - start
	statsd.histogram('web.page_latency', duration, tags = ["support", page_tag])
	increase_counter(page_tag)
	return "It's done!"

def increase_counter(page_tag):
    """ Increments page view count """
    statsd.increment('web.page_views', tags = ["support", page_tag])
    return "cool"