from flask import Flask, g, request, jsonify
from ddtrace import tracer
import logging
import sys
import random
import sqlite3


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

@app.route('/api/rsvp', methods=["POST",])
@tracer.wrap("flask.request", service='flask', resource='POST /api/rsvp', span_type='web')
def rsvp():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    name = request.json['name']
    print "name= " + str(name)

    with tracer.trace("database.post.rsvp") as span:
        cur.execute('INSERT INTO GUESTS (name) VALUES (?);', (name,))
        span.set_tag("name", name)

    conn.commit()
    conn.close()

    return "You've successully RSVP'd! \n"
    

@app.route('/api/guests', methods=["GET",])
@tracer.wrap("flask.request", service='flask', resource='GET /api/guests', span_type='web')
def apm_endpoint():
    query_result = []
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    with tracer.trace("database.get.guests") as span:
        query_result = cur.execute("SELECT * FROM GUESTS").fetchall()
        span.set_tag("num_guests", len(query_result))
    

    conn.commit()
    conn.close()

    current_span = tracer.current_span()

    return jsonify(query_result) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')