# a flask app to showcase Datadog APM
#
# the logging in the demo app seems to be irrelevant
# for the task at hand - left it out for now

from ddtrace import tracer

from flask import Flask
app = Flask(__name__)

@app.route('/')
@tracer.wrap('api_entry')
def api_entry():
    with tracer.trace('api_entry'):
        return 'Entrypoint to the application!'

@app.route('/api/apm')
@tracer.wrap('api_apm')
def api_apm():
    with tracer.trace('api_apm'):
        return 'Getting APM started'

@app.route('/api/trace')
@tracer.wrap('api_trace')
def api_trace():
    with tracer.trace('api_trace'):
        return 'Posting traces'


# the port is configured by means of a command line argument
# (DD_SERVICE=custom_flask_app  ddtrace-run flask run --port=5533)
if __name__ == '__main__':
    app.run()
