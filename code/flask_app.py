from flask import Flask
import logging
import sys
from datadog import initialize, api
import time




# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)


"""Get Datadog API key from file"""
with open('/Users/joshuabrown/Documents/keys/datadog_api_key.txt') as file:
	key = file.read().strip()

now = time.time()
future_10s = now + 10

options = {
    'api_key': key,
 }

initialize(**options)

@app.route('/')
def api_entry():
	api.Metric.send(metric='page.views', points=(now, 15))
	return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')