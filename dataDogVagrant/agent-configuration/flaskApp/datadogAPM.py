from flask import Flask
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

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

@app.route('/api/world')
def db_endpoint():
    # Set psql credentials
    hostname = 'localhost'
    username = 'datadog'
    password = 'datadog'
    database = 'worlddb'

    # function to query the database and display 100 entries
    def doQuery( conn ):
        cur = conn.cursor()
        cur.execute( "SELECT * FROM city limit 50")
        cities = cur.fetchall()
        # for city in cities :
        return "{}".format(cities)
    import psycopg2
    #connect to db with credentials
    myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    #perform query function
    return doQuery( myConnection )
    #close connection
    myConnection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
