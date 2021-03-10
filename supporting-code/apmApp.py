from flask import Flask
from flask_mysqldb import MySQL
import logging, logging.handlers
from decouple import config
import sys

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)
#set up tcp logger
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = config('password')  #don't expose passwords in real life, kids
app.config['MYSQL_DB'] = 'mysql'
mysql = MySQL(app)

#set up logger
log = logging.getLogger(__name__)
log.level = logging.INFO
socketHandler = logging.handlers.SocketHandler('localhost', 10518)
log.addHandler(socketHandler)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    log.info('Hit APM Endpoint /api/apm')    
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    log.info('Hit Trace Endpoint /api/trace')    
    return 'Posting Traces'

@app.route('/api/db/getall')
def users():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM mysql.pet''')
    rv = cur.fetchall()
    return str(rv)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
