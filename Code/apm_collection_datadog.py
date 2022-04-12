import datadog
from flask import Flask
import logging
import sys
from ddtrace import tracer
from ddtrace import config
from ddtrace.contrib.flask import TraceMiddleware



# Enable distributed tracing
config.flask['distributed_tracing_enabled'] = True

# Override service name
config.flask['service_name'] = 'myFlaskApp'

# Report 401, and 403 responses as errors
config.http_server.error_statuses = '401,403'

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

#Network Sockets
traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)
"""
tracer.configure(
    https=False,
    hostname="daeclan-MacBookPro",
    port="5050",
    
)

"""
"""
tracer.configure(
    dogstatsd_url="http://localhost:5050",
)



tracer.configure(
    dogstatsd_url="unix:///var/run/datadog/dsd.socket",
)
# Unix domain socket configuration

tracer.configure(
    uds_pat="var/run/daadog/apm.socket",
)



"""

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