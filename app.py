from flask import Flask
import logging
import sys

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

# tracer.configure(hostname="127.0.1.1", port=8126)

# Traces web requests and sends spans that set tags on each trace
# with tracer.trace("web.request", service="my_service") as span:
#   span.set_tag("my_tag", "my_value")

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

# Tracing middleware
traced_app = TraceMiddleware(app, tracer, service="my_service", distributed_tracing=False)

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