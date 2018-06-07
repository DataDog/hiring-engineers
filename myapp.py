from flask import Flask
import blinker as _
import logging
import sys
import werkzeug
# from ddtrace import tracer
# from ddtrace.contrib.flask import TraceMiddleware
# import time
# with tracer.trace("web.request", service="my_service") as span:
# span.set_tag("my_tag", "my_value")
# Have flask use stdout as the logger

main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

# traced_app = TraceMiddleware(app, tracer, service="my_service", distributed_tracing=False)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return 'bad request!', 400
# @tracer.wrap(name='doc_work')
# def work():
#     time.sleep(0.5)
#     return 42

# @app.route('/doc/')
# def doc_resource():
#     time.sleep(0.3)
#     res = work()
#     time.sleep(0.3)
#     return Response(str(res), mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
