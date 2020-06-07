from flask import Flask
import logging
import sys

from ddtrace import tracer

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

@app.route('/')
@tracer.wrap(name='my_entry')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
@tracer.wrap(name='my_apm_endpoint')
def apm_endpoint():
    with tracer.trace('my_apm_span') as span:
        #designate this span as a separate service:
        span.service='my_apm_service'
        #add metadate
        span.set_tag('service_type','my_apm_service_type')
    return 'Getting APM Started'

@app.route('/api/trace')
@tracer.wrap(name='my_apm_trace',service='my_apm_trace_service')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
