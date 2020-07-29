#!/usr/bin/env python
from flask import Flask
import logging
import sys
from cowpy import cow
import ddtrace.profiling.auto
ddtrace.config.analytics_enabled = True

main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
c.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

@app.route('/')
def api_entry():
    message = cow.milk_random_cow("Random message for the Entrypoint to the App")
    print(message)
    return message

@app.route('/api/apm')
def apm_endpoint():
    message = cow.Cowacter().milk('Hello from Python from Getting APM Started')
    print(message)
    return message

@app.route('/api/trace')
def trace_endpoint():
    cheese = cow.Moose(thoughts=True)
    message = cheese.milk("My witty mesage, for Posting Traces")
    print(message)
    return message

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')

