from flask import Flask
import MySQLdb
from ddtrace import Pin, patch
import logging
import sys
from random import randint
from time import sleep
from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware
from ddtrace import patch_all

patch(mysqldb=True) #is redundat as patch_all is active
patch_all()

# Have flask use stdout as the logger

main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

# instrumentation
#trace_app = TraceMiddleware(app, tracer, service="flask", distributed_tracing=False)


db = MySQLdb.connect("localhost","mysql-user","mysql-user", "FLASKDB")
Pin.override(db, service='mysql-users')

#@tracer.wrap(name='mysql_db_access')
def writetodb(database, name):
	cursor = db.cursor()
	sleep(randint(0,3))
	sql_query = "INSERT INTO example ( id, name ) VALUES ( null, '" + name + "');"
	cursor.execute(sql_query)
	db.commit()

#@tracer.wrap(name='mysql_db_close')
def closedb(database):
	database.close()

#@tracer.wrap(name='default_message')
def respond_default():
	sleep(randint(1,3))
	return "Hello Y'all"

@app.route('/')
def hello_default():
	message = respond_default()
	return message


@app.route('/api/apm')
def apm_endpoint():
    main_logger.info('APM started')
    return 'Getting APM Started'

 
@app.route('/api/trace')
def trace_endpoint():
    main_logger.info('Posting traces')
    return 'Posting Traces'



@app.route('/<name>')
def hello_name(name):
	if name != 'favicon.ico':
		writetodb(db, name)	
    	return "Hello {}!".format(name)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port='9999')
	closedb(db)