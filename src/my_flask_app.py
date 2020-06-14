import logging
import sys
import time
import random
from flask import Flask
from ddtrace import patch_all
patch_all()


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
    return 'Entrypoint to the Application'


@app.route('/api/apm')
def apm_endpoint():
    time.sleep(random.randint(0,15))
    return 'Getting APM Started'


@app.route('/api/trace')
def trace_endpoint():
    time.sleep(random.randint(0,10))
    return 'Posting Traces'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5050')
