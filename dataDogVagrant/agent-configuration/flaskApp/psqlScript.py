
# Set psql credentials
hostname = 'localhost'
username = 'datadog'
password = 'datadog'
database = 'worlddb'

# function to query the database and display 100 entries \
def doQuery( conn ):
    cur = conn.cursor()
    cur.execute( "SELECT * FROM city limit 100")
    for city in cur.fetchall() :
        print city
import psycopg2
#connect to db with credentials \
myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
#perform query function \
doQuery( myConnection )
#close connection \
myConnection.close()
