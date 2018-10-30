#!/usr/bin/env python
from flask import Flask
from flask import request
from time import sleep

#import the necessarry modules for tracing our app
import blinker as _
from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

import logging
import sys
import random
import requests

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

# Instrument our app
traced_app = TraceMiddleware(app, tracer, service="sample-flask-app", distributed_tracing=False)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

# Create a new method that does something interesting that we can measure
@app.route('/url_lookup')
def url_lookup():
    url_name= request.args.get("url-name")
    full_url= "http://" + url_name

    # Trace how much time this portion of the method takes
    with tracer.trace("setup_overhead", service = "url-lookup"):
        # Artificially insert some random overhead time to make things interesting
        random_nbr = float(random.randint(250,750))
        sleep (float(random_nbr/1000))

    # Trace how much time the actual URL call takes
    with tracer.trace("call_url") as span:
        # By setting a tag in the span, we can see which URL was being called when we look at our metrics
        span.set_tag("url-name", url_name)
        return requests.get(full_url).content

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
