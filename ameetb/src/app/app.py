from flask import Flask
from datadog import initialize, api
#from ddtrace import tracer
import logging
import sys

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)
    
# Don't mix the streams
# tracer.configure(
#    hostname="ameet.docker",
#)

app = Flask(__name__)

@app.route('/')
def api_entry():
    main_logger.debug('Addressing root route request');
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    main_logger.debug('Addressing apm route request');
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    main_logger.debug('Addressing trace route request');
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
