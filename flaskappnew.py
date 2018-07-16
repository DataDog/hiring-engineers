from flask import Flask
import logging
import sys
import time

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

#tracer.configure(hostname='vagrant')
app = Flask(__name__)
traced_app = TraceMiddleware(app, tracer, service='simple_service')

@tracer.wrap(name='api_entry')
@app.route('/')
def api_entry():
    time.sleep(0.2)
    slow_function()
    time.sleep(0.2)
    return 'Entrypoint to the Application'

@tracer.wrap(name='slow_function')
def slow_function():
    time.sleep(0.5)
    return 'Slow function in Application'


@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
