from flask import Flask
import logging
import sys
from ddtrace import tracer

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

# from source endpoint
@app.route('/')
def api_entry():
    with tracer.trace('endpoint.source') as span:
        span.set_tag('from_entry_method', 'true')
        return 'Entrypoint to the Application'

# from apm endpoint
@app.route('/api/apm')
def apm_endpoint():
    with tracer.trace('endpoint.source') as span:
        span.set_tag('from_apm_method', 'true')
        return 'Getting APM Started'

# from trace endpoint
@app.route('/api/trace')
def trace_endpoint():
    with tracer.trace('endpoint.source') as span:
        span.set_tag('from_tracer_method', 'true')
        return 'Posting Traces'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
