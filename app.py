from flask import Flask
from ddtrace import tracer, patch_all, config
patch_all(flask=True, requests=True)
import blinker as _
import logging
import sys
import os
import requests
from ddtrace.contrib.flask import TraceMiddleware

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

tracer.configure(hostname='localhost')

app = Flask(__name__)
traced_app = TraceMiddleware(app, tracer, service="flask_app")

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    print('In app.py __main__')
    app.run(host='127.0.0.1', port='8126')
