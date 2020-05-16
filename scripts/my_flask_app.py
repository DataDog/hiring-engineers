#!/usr/bin/python

from flask import Flask
import logging
import sys
import ddtrace
import random

#Enabing app analytics
ddtrace.config.analytics_enabled = True
ddtrace.config.postgres.analytics_enabled = True

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

#Setting app entry to fail one in ten times
@app.route('/')
def api_entry():
    val = random.randrange(0,10)
    if val == 7:
        sys.exit(1)
    else:
        return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

@app.route('/api/user/<userid>')
def user_endpoint(userid):
    valid_userids = ['1','2','3']
    if userid in valid_userids:
        return 'Profile page for user %s' % userid
    else:
        raise ValueError

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
