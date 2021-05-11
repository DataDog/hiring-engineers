from flask import Flask
from flask import request
from ddtrace import tracer
from ddtrace import config
import logging
import sys

config.flask['service_name'] = 'apm-demo'


# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

@app.route('/')
def api_entry():
    with tracer.trace("api_entry") as span:
        span.set_tag("client_ip", request.remote_addr);
        return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    with tracer.trace("APM_Endpoint") as span:
        return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    with tracer.trace("Trace_Endpoint") as span:
        return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')