#!/usr/bin/env python3

from flask import Flask
from ddtrace import config, patch_all,tracer
import logging
import sys
import time
import requests
import json

# Override service name
config.flask['service_name'] = "my_datadog_instrumented_flask_app"

# Report 404 responses as error
config.flask['extra_error_codes'] = [404]

patch_all()

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

# sleep for 10 msec
@tracer.wrap(name='sleep_function')
def sleep_function():
    time.sleep(0.01)
    return True

# get random text from randomtext.me
@tracer.wrap(name='get_random_text',service='randomtext.me')
def get_random_text():
    r = requests.get('http://www.randomtext.me/api/')
    j = json.loads(r.text)
    return j['text_out']

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

#adding an additional endpoint calling another function to be traced and an external resource
@app.route('/api/random')
def random_endpoint():
    sleep_function()
    return get_random_text()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
                