from datadog import initialize, api
from flask import Flask
import logging
import sys

# Have flask use stdout as the logger
logger = logging.getLogger()  # Root logger
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
# handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.DEBUG,
#     handlers=[logging.StreamHandler(sys.stdout)]
# )
# logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route('/')
def api_entry():
    logger.debug('Handling root route request')
    return 'Entrypoint to the Application\n'


@app.route('/api/apm')
def apm_endpoint():
    logger.debug('Handling apm route request')
    return 'Getting APM Started\n'


@app.route('/api/trace')
def trace_endpoint():
    logger.debug('Handling trace route request')
    return 'Posting Traces\n'


if __name__ == '__main__':
    # args = parser.parse_args()
    # initialize(api_key=args.api_key, app_key=args.app_key)
    app.run(host='0.0.0.0', port=5050)
