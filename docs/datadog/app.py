from ddtrace import tracer
from flask import Flask
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
    # To generate an error in app operation, uncomment the snippet below.
    # Then restart the app and visit root of the website.

    # tracer.set_tag("generate", "error")
    return 'Entrypoint to the Application'


@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'


@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')