import blinker as _
import logging
import sys

from flask import Flask

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware
# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

#Tracer configuration
tracer.configure(hostname='datadog')
app = Flask('API')
traced_app = TraceMiddleware(app, tracer, service='my_service')

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'