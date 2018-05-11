import logging
import sys
import requests

from flask import Flask, Response
from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware
from time import sleep

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)
traced_app = TraceMiddleware(
    app, tracer, service="my-flask-app", distributed_tracing=False)


@app.route('/')
def api_entry():
    return 'Home'


@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'


@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'


@app.route('/traffic')
def traffic():
    with tracer.trace("/traffic", service="test") as span:
            span.set_tag("traffic", 3)
            sleep(3)
            r = "Congrats! You've got 3 seconds of lag"
    return r


@app.route('/fail')
def failure():
    with tracer.trace('/fail', service="test") as span:
        span.set_tag("fail", 0)
        r = Response(response="Service Unavailable - You Lose :(",
                     status=503, mimetype='application/json')
    return r


if __name__ == '__main__':
    app.run()
