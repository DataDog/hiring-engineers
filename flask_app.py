from flask import Flask
import logging
import sys

import time

import blinker as _
from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

tracer.configure(hostname='localhost')
app = Flask(__name__)
traced_app = TraceMiddleware(app, tracer, service="hiring-flask-app", distributed_tracing=False)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    # Let's wait a few ms to show some "action" in the graphs
    time.sleep(0.2)
    apm_worker()
    time.sleep(0.3)
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

# Let's add a worker method that sleeps for a while and returns something.
# Just to have an example of tracing for submethods.
@tracer.wrap(name='apm_worker')
def apm_worker():
    time.sleep(0.5)
    return 'asdf'
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')

