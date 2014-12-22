from flask import Flask
from statsd import statsd
import datetime as dt

datetime=dt.datetime
app =  Flask(__name__)

@app.route("/")
@statsd.timed('page.view.time',tags=["support"])
@statsd.timed('page.view.time',tags=["page:page0"])
def gen():
   #statsd.event('Flask app is running!', 'Our python app (app.py) has run')
   title = 'This is the index page<br/>'
   return title

@app.route("/hello")
@statsd.timed('page.view.time',tags=["support"])
@statsd.timed('page.view.time',tags=["page:page1"])
def hello_World():
    title =  "Hello World<br/>"
    return title

@app.route("/time")
@statsd.timed('page.view.time',tags=["support"])
@statsd.timed('page.view.time',tags=["page:page2"])
def time_is():
    now = datetime.now()
    title =  "The time is: %s<br/>" % now
    return title

if __name__ == "__main__":
    app.run()