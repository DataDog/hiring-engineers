# Import packages
from flask import Flask
import logging
import sys

# Create Application Instance
app = Flask(__name__)

# Have Flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)

# Configure logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

# Configure URL Routing
@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

# Configure for External Environment
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')