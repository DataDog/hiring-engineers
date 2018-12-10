from ddtrace import patch_all
patch_all()

from ddtrace import config

# Override service name
config.flask['service_name'] = 'The Dummy App'

# Report 401, and 403 responses as errors
config.flask['extra_error_codes'] = [401, 403, 404]

from flask import Flask
import logging
import sys

# Configure the module according to your needs
from datadog import initialize

options = {
    'api_key':'1e4bc1602c9a7eeac37718d0b4fcd482',
    'app_key':'02e9c8a50a650907e979279ba2dd227deef90094'
}

initialize(**options)

# Use Datadog REST API client
from datadog import api

# Use Statsd, a Python client for DogStatsd
from datadog import statsd



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
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
    