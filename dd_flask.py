from flask import Flask
import logging
import sys

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

import os

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

# Tracer configuration
tracer.configure(hostname='127.0.0.1')
app = Flask("RL_service")
traced_app = TraceMiddleware(app, tracer, service='RL_service')

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

@tracer.wrap(name='RL_work')
@app.route("/rhys/")
def hello():
    return "Hello World From Rhys!"
	
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT',
            18080))) #Code to overcome address in use issue