from flask import Flask, Response, jsonify
import logging
import sys

from datadog import initialize, api

options = {
    'api_host': 'https://app.datadoghq.com/',
    'api_key': '22089f47d7c7cd9285ad8cd7b94b9663',
    'app_key': 'd3a238f120fc730ddf663a58eb72dac600bafc71'}

initialize(**options)

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

@app.route('/api/dashboards')
def get_dash():
#    res = str(api.DashboardList.get_items(5819))
   res = api.DashboardList.get_items(5819) 
   return jsonify(res)

@app.route('/api/timeboards')
def get_timeboards():
#    res = str(api.Timeboard.get_all())
    res = api.Timeboard.get_all()
    return jsonify(res)

if __name__ == '__main__':
    app.run(host= '0.0.0.0' , port=10000)
