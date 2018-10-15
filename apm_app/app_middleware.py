#!/usr/bin/env python

# This version of the app has the middleware hard-coded.

from flask import Flask
import logging
import sys
from ddtrace import tracer

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

@app.route('/')
@tracer.wrap()
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
@tracer.wrap()
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
@tracer.wrap()
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')