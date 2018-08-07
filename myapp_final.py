import logging
import sys
import blinker as _
from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware
from flask import Flask
 # Have flask use stdout as the logger

main_logger = logging.getLogger()

main_logger.setLevel(logging.DEBUG)

c = logging.StreamHandler(sys.stdout)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

c.setFormatter(formatter)

main_logger.addHandler(c)

app = Flask(__name__)

#traced_app = TraceMiddleware(app, tracer, service="my-app", distributed_tracing=False)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

@app.route('/api/trace2')
def trace_2_endpoint():
    return 'Posting Traces 2'
	
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')

