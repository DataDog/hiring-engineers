from flask import Flask
import logging
import sys
from pymongo import MongoClient
import json_log_formatter

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
f = logging.FileHandler(filename='flask-app.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
json_formatter = json_log_formatter.JSONFormatter()
c.setFormatter(formatter)
f.setFormatter(json_formatter)
main_logger.addHandler(c)
main_logger.addHandler(f)



app = Flask(__name__)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application. <a href="/api/inventory">View inventory item.</a>'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

@app.route('/api/inventory')
def api_inventory():
    client = MongoClient()
    db = client.admin
    inventory = db.inventory
    item = inventory.find_one()
    return str(item)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
