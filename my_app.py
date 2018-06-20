import time
from flask import Flask
import blinker as _
import logging
import sys

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

# Have flask use stout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(level)s - % (message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__) \
 \
      @ tracer.wrap(name='trace_work')


def work():
    time.sleep(0.5)
    return 42


# dummy trace
# with tracer.trace("Hello, Jerry. Hello."):
#    pass


# tracer.debug_logging = True

# set Tracer tags
# tracer.set_tags('env', 'prod')

# tracer middleware for flask apps
traced_app = TraceMiddleware(app, tracer, service="my_app", distributed_tracing=False)


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
    app.run(host='0.0.0.0', port='5050')
