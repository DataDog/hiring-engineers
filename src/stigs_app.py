from flask import Flask
import blinker as _

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

app = Flask(__name__)

traced_app = TraceMiddleware(app, tracer, service="stigs-app")

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
    app.run()
