from flask import Flask
import logging
import sys
from ddtrace import tracer

with tracer.trace("web.request", service="my_app") as span:
  span.set_tag("my_app", "tag_1")

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
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    with tracer.trace("web.request", service="m_app") as span:
     span.set_tag("trace", "end_point")
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(port=9000)
