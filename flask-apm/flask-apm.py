from flask import Flask
import logging
import sys
import blinker as _

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

# setting the datadog agent location
tracer.configure(hostname="datadog", port=8126)

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

# Trace middleware object
traced_app = TraceMiddleware(app, tracer, service="flask-apm", distributed_tracing=False)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run()
