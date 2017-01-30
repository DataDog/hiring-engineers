from flask import Flask, render_template
from dogapi import dog_http_api as api
from statsd import statsd
import time, random

app = Flask(__name__)

# API params.
api.api_key = 'cd5682f38e477d011c8c788064869b07'
api.application_key = '718b5ffa208043f4c4f2f90198a7a55844c2e61b'

#level 1 event generation.
title = "Basic level-1 event"
text = 'Event with custom tag.'
tags = ['version:1', 'application:web', 'type:support', 'basic:event']
api.event_with_response(title, text, tags=tags)


#Landing page handler.
@app.route("/")
@statsd.timed('page.load.time', tags=['type:support', 'page:home'])
def home_page():
    statsd.increment('web.page_count', tags=['page:home'])
    return "App Home Page"


#Main page handler
@app.route("/main")
def main_page():
    statsd.increment('web.page_count', tags=['page:main'])
    #time diff for histograms
    start_time = time.time()
    #putting randomly to sleep to generate delays.
    time.sleep(random.randint(1, 10))
    duration = time.time() - start_time
    #paging data for histogram
    statsd.histogram('page.load.hist_timer', duration, tags=['type:support', 'page:main'])
    return "App Main Page"


#About page handler
@app.route('/about')
@statsd.timed('page.load.time', tags=['type:support', 'page:about'])
def about():
    statsd.increment('web.page_count', tags=['page:about'])
    return "App About Page"



if __name__ == "__main__":
    app.debug = True
    app.run()

