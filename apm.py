from flask import Flask
from ddtrace import tracer
from datetime import date
import logging
import sys

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

tracer.set_tags({ 'env': 'gui-datadog-env' })

@app.route('/')
def api_entry():
    main_logger.info('Hello, this is Gui playing with Datadog features')
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    main_logger.info('This is the APM entrypoint!')
    return 'Getting APM Started'

@tracer.wrap()
@app.route('/api/trace')
def trace_endpoint():
    with tracer.trace('some.random.things'):
      whatIsTheDifference = 10 - 5
      currentDateTime = date.today()
      print(currentDateTime)
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')