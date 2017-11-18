from flask import Flask
import blinker as _
import logging
import sys

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

tracer.configure(hostname="127.0.1.1", port=8126)

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)

@app.route("/")
def home():
    return "hello world"