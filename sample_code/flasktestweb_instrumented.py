from flask import Flask
import logging
import sys
from flaskext.mysql import MySQL
from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)


app = Flask(__name__)

TraceMiddleware(app, tracer, service="flasktestweb")

def api_entry():
    return 'Entrypoint to the Application'

def apm_endpoint():
    return 'Getting APM Started'

def trace_endpoint():
    return 'Posting Traces'

def db_endpoint():
    with tracer.trace('db_queries', service='flasktestdb'):
    # Add configuration details for database
        mysql = MySQL()
        app.config['MYSQL_DATABASE_USER']='datadog'
        app.config['MYSQL_DATABASE_PASSWORD']='datadogtest12345'
        app.config['MYSQL_DATABASE_HOST']='localhost'
        app.config['MYSQL_DATABASE_DB']='datadogtestdb'
        mysql.init_app(app)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT silly FROM testtable LIMIT 1")
        return 'Got the DB to Connect'

@app.route('/')
def my_root():
    root_answer = api_entry()
    return root_answer

@app.route('/api/testdb')
def my_db():
    db_answer = db_endpoint()
    return db_answer

@app.route('/api/apm')
def my_apm():
    apm_answer = apm_endpoint()
    return apm_answer

@app.route('/api/trace')
def my_trace():
    trace_answer = trace_endpoint()
    return trace_answer

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
