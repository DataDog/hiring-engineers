from flask import Flask
import logging
import sys

# import opentracing
# from ddtrace.opentracer import Tracer, set_global_tracer

# def init_tracer(service_name):
#     config = {
#       'agent_hostname': 'localhost',
#       'agent_port': 8126,
#     }
#     tracer = Tracer(service_name, config=config)
#     set_global_tracer(tracer)
#     return tracer


# tracer.set_tags({ 'env': 'prod' })

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
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
