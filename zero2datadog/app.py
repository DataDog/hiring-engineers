from ddtrace import patch_all
patch_all()

from flask import Flask
from loguru import logger


app = Flask(__name__)


@app.route('/')
def api_entry():
    logger.info("Welcome to Zero2Datadog")
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    logger.info("Starting the APM")
    return 'Getting APM Started'


@app.route('/api/trace')
def trace_endpoint():
    logger.info("Posting a Trace")
    return 'Posting Traces'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
