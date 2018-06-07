import time
import blinker as _
import logging
import sys
from flask import Flask, Response

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware
from ddtrace import patch_all


main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

# Tracer configuration
tracer.configure(hostname='datadog')
app = Flask('API')
traced_app = TraceMiddleware(app, tracer, service='doc_service')
with tracer.trace("web.request", service="my_service") as span:
  span.set_tag("my_tag", "my_value")

@tracer.wrap(name='doc_work')
def work():
    time.sleep(0.5)
    return 42

@app.route('/doc/')
def doc_resource():
    time.sleep(0.3)
    res = work()
    time.sleep(0.3)
    return Response(str(res), mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
