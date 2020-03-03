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
def api_entry():
    main_logger.info('api_entry function call')
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    main_logger.info('apm_endpoint function call')
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    main_logger.info('trace_endpoint function call')
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')