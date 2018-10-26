from flask import Flask
import blinker as _
import logging
import sys

# Add some dBase fun, make the agent work a little
import pymysql

# From guides, this is needed to function as middleware
# for tracking request timings
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
traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)

# Connect to the mysql server installed for the exercise
def connectdBase():
	server = 'localhost'
	user = 'datadog'
	pwd = 'BG/ALNNK3KCWdbR1mkTSUMlP'
	db = 'performance_schema'
	conn = pymysql.connect(server, user, pwd, db)
	return conn

@app.route('/')
def api_entry():
	conn = connectdBase()	
	cursor = conn.cursor()
	cursor.execute('select thread_id, name, type from threads')
	row = cursor.fetchone()
	while row:
		print row
		row = cursor.fetchone()
	conn.close()
	return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
	conn = connectdBase()	
	cursor = conn.cursor()
	cursor.execute('select thread_id, variable_name from status_by_thread')
	row = cursor.fetchone()
	while row:
		print row
		row = cursor.fetchone()
	conn.close()
	return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
	conn = connectdBase()	
	cursor = conn.cursor()
	cursor.execute('select thread_id, variable_name from variables_by_thread')
	row = cursor.fetchone()
	while row:
		print row
		row = cursor.fetchone()
	conn.close()
	return 'Posting Traces'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port='5050')
