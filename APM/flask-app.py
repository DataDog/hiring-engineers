from flask import Flask
import logging
import sys
import os
import ddtrace.profile.auto
from ddtrace import tracer

tracer.configure(
        hostname=os.environ['DD_AGENT_HOST'],
        )

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

@tracer.wrap()
@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@tracer.wrap()
@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@tracer.wrap()
@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080')
