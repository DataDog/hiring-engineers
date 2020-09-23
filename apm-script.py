from flask import Flask
import logging
import sys
from ddtrace import tracer, config

config.flask['service_name'] = 'flask-app'

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

@tracer.wrap('flask-app.home', service='flask-entry')
@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@tracer.wrap('flask-app.apm', service='flask-apm')
@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@tracer.wrap('flask-app.trace', service='flask-trace')
@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)