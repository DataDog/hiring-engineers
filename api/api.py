import os
import traceback
import random
import time
import requests
import json
import copy
import pprint
import psycopg2

from datadog import initialize, api
from flask import Flask, send_file, redirect
from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

options = {'api_key': 'e1dbdaceaf7516f90ef9e2ad5546072e',
            'app_key': '25b8d433ca6e9ca99c1ee791e8ece8c67e6a0ec3'}

initialize(**options)

app = Flask(__name__)

the_spans = []

tracer.configure(hostname="127.0.0.1")
traced_app = TraceMiddleware(app, tracer, service="api", distributed_tracing=False)

@app.route(u'/ce')
def cause_exception():
    assert(1==3)
    return 'x'

@app.route(u'/tfs')
def trace_full_stack():
    try:
        connect_str = "dbname=ddhee user='datadog' host='localhost' " + \
                      "password='CG4W1mPaET70QWl2TrjYeAlN'"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        # create a new table with a single column called "name"
        cursor.execute("""CREATE TABLE tutorials (name char(40));""")
        # run a SELECT statement - no data in there, but we can try it
        cursor.execute("""SELECT * from tutorials""")
        rows = cursor.fetchall()
        return json.dumps(rows)
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
    return 'x'
 
@app.route(u'/ks')
def kill_server():
    quit()
    return 'x'

@app.route(u'/pc')
def post_comment():
    api.Comment.create(
        handle='robot@ddhee.com',
        message='Datadog should use Clojure!'
    )
    return 'x'

@app.route(u'/event')
def post_event():
    title = "Something big happened!"
    text = 'You discovered Tony Mayse!'
    tags = ['version:1', 'application:web']
    api.Event.create(title=title, text=text, tags=tags)
    return 'x'

@app.route(u'/pt')
def post_trace():
    pp = pprint.PrettyPrinter(indent=4)
    # Create IDs.
    TRACE_ID = random.randint(1,1000000)
    SPAN_ID = random.randint(1,1000000)
    START = int(time.time() * 1000000000)
    DURATION = 2.5e+10 #2.5e+10 nanoseconds = 25 seconds
    parent_span = {
            u'trace_id': TRACE_ID,
            u'span_id': SPAN_ID,
            u'name': u'app level',
            u'resource': u'post_trace',
            u'service': u'api',
            u'type': u'web',
            u'start': int(START),
            u'duration': int(DURATION)
    }
    the_spans.append(parent_span)
    add_to_span(parent_span) #this is the meat
    pp.pprint(the_spans)
    the_spans.append(parent_span)
    pp.pprint(the_spans)
    # Send the traces.
    the_trace = [].append(the_spans)
    data = json.dumps(the_trace)
    headers = {"Content-Type": "application/json"}
    response = requests.put("http://localhost:8126/v0.3/traces", data=data , headers=headers)
    print(response.text)
    return response.text

# Everything not declared before (not an API endpoint)...
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def not_found(path):
    #302 = keep trying
    return redirect("https://docs.datadoghq.com/integrations/postgres/", code=302)

def add_to_span(span):
    pp = pprint.PrettyPrinter(indent=4)
    max_time = span[u'duration']
    start_delay = int(random.triangular(0.0, max_time, max_time / 3))
    start_time = int(span[u'start'] + start_delay)
    max_time -= start_delay
    SPAN_ID = random.randint(1,1000000)

    choice = random.randint(1,10)
    if (choice <3 or max_time < 900000000.0): #stop adding spans < 0.9s left
	pass
    else:
	print('choice add new span')
        new_span = {
            u'trace_id': span[u'trace_id'],
            u'span_id': SPAN_ID,
            u'parent_id': span[u'span_id'],
            u'name': u'app level',
            u'resource': u'/pt',
            u'service': u'api',
            u'type': u'web',
            u'start': start_time,
            u'duration': int(max_time)
        }
	the_spans.append(new_span)
	print(the_spans)
        add_to_span(new_span)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8081)
