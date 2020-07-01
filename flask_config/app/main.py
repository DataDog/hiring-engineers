from flask import Flask
from mysql.connector import Error
from flask import request, jsonify
import logging
import sys
import mysql.connector

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


@app.route('/api/city', methods=['GET'])
def api_id():
    # Check if an city name was provided as part of the URL.
    # If city is provided, assign it to a variable.
    # If no city is provided, display an error in the browser.
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."

    try:
    	connection = mysql.connector.connect(user='datadog', password='datadog',
                              host='mysql1', port='3306')


    	sql_select_Query = "SELECT * FROM classicmodels.city_stats where cityname='"+id+"'"
    	cursor = connection.cursor()
    	cursor.execute(sql_select_Query)
    	records = cursor.fetchall()
    	print("Total number of rows in city_stats is: ", cursor.rowcount)

    except Error as e:
     	print("Error reading data from MySQL table", e)
    finally:
    	if (connection.is_connected()):
        	connection.close()
        	cursor.close()
        	print("MySQL connection is closed")


    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(records)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')