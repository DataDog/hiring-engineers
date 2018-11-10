from flask import Flask
import logging
import sys
import json_log_formatter
import blinker as _

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

import threading
formatter = json_log_formatter.JSONFormatter()
json_handler = logging.FileHandler(filename='/var/log/my-log.json')
json_handler.setFormatter(formatter)
logger = logging.getLogger('my_json')
logger.addHandler(json_handler)
logger.setLevel(logging.INFO)

app = Flask(__name__)
traced_app = TraceMiddleware(app, tracer, service="osowskit-middleware-flask", distributed_tracing=False)

@app.route('/')
def api_entry():
    # logger.info('function1 has executed', extra={ 'job_category': 'test_function', 'logger.name': 'my_json', 'logger.thread_name' : my_thread } )
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
