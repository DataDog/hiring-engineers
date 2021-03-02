from flask import Flask
from flask_mysqldb import MySQL
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
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ootiquu123456@' #don't do this in real life, kids
app.config['MYSQL_DB'] = 'mysql'
mysql = MySQL(app)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

@app.route('/api/db/getall')
def users():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM mysql.pet''')
    rv = cur.fetchall()
    return str(rv)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
