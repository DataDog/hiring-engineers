from flask import Flask, abort
import logging
import sys
import time
import json_log_formatter

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

formatter = json_log_formatter.JSONFormatter()
json_handler = logging.FileHandler(filename='/var/log/my-log.json')
json_handler.setFormatter(formatter)
logger = logging.getLogger('my_json')
logger.addHandler(json_handler)
logger.setLevel(logging.INFO)

@app.route('/')
def api_entry():
    time.sleep(5)
    logger.info('Entrypoint accessed.')
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    logger.info('Getting APM Started.')
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    logger.info('Posting traces.')
    return 'Posting Traces'

@app.route('/api/database')
def database_endpoint():
    logger.info('Database was accessed.')
    raise Exception("Can't connect to database")

@app.route('/api/protected')
def auth_endpoint():
    logger.info('Protected resource was accessed.')
    abort(401)

@app.errorhandler(401)
def custom_401(error):
    return 'Authentication required.', 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')