from flask import Flask
import logging
import sys
import datetime
import mysql.connector
import blinker as _
#from ddtrace import tracer
#from ddtrace.contrib.flask import TraceMiddleware

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)
#traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)
@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

@app.route('/api/query')
def run_query():
    for i in range(100):
        cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='fang')
        cursor = cnx.cursor()
        query = ("select * from pet")
        cursor.execute(query)
        cursor.close()
        cnx.close()

    return 'DB Query'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
~