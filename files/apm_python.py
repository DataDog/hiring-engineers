from flask import Flask
import ddtrace
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

ddtrace.config.analytics_enabled = True

@app.route('/')
def api_entry():
    return 'Welcome to Springfield'

@app.route('/api/moes')
def apm_endpoint():
    return 'Welcome to Moe\'s'

@app.route('/api/powerplant')
def trace_endpoint():
    return 'Welcome to the Power Plant'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
