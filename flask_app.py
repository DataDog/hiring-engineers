from flask import Flask
import logging
import sys
import os

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
    print('Entrypoint to the Application')
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    print('Getting APM Started')
    # add something to do 
    os.system("dpkg --get-selections|grep mysql")
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    print('Posting Traces')
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
