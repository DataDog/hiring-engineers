from flask import Flask
from ddtrace import tracer
import logging
import sys

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

@app.route('/')
@tracer.wrap('my.wrapped.function', service='myFlaskEntry')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
@tracer.wrap('my.wrapped.function', service='myFlaskInto')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
@tracer.wrap('my.wrapped.function', service='myFlaskTraces')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')

