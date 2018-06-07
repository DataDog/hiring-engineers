from flask import Flask, Response
import blinker as _
import logging
import sys
from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware
import time

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

# turn on debugging
tracer.debug_logging = True

# initializes app
app = Flask(__name__)

traced_app = TraceMiddleware(app, tracer, service="myapp_service", distributed_tracing=False)

# dummy function to immitate the time to start apm
@tracer.wrap(name='start_api')
def start_api():
    time.sleep(0.5)
    return 'Getting APM Started'

# dummy function to immitate the time to post traces
@tracer.wrap(name='post_trace')
def post_trace():
    time.sleep(0.3)
    return 'Posting Traces'

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    time.sleep(0.2)
    res = start_api()
    time.sleep(0.2)
    return Response(res, mimetype='application/json')

@app.route('/api/trace')
def trace_endpoint():
    time.sleep(0.3)
    res = post_trace()
    time.sleep(0.3)
    return Response(res, mimetype='application/json')

# dummy error
@app.route('/error')
def error():
    return Response('Oh no! Something is wrong with our server!', status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
