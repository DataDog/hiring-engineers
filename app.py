#imports
from flask import Flask, render_template, redirect, url_for, request

from datadog import initialize, api, statsd
import time

options = {
    'api_key': '5ed187caa3871e87c086c7a6e83717c6',
    'app_key': '1b39da63c63b5c308be0a86bc90f0c6cc5c036c7'
}

initialize(**options)


#create project
app = Flask(__name__)

def page_view_count(page_name):
	statsd.increment('web.page_views', tags = ["support", page_name])
	return

def page_view_latency(page_name):
	start_time = time.time()
	page_view_count(page_name);
	duration = time.time() - start_time
	statsd.histogram('page_view_latency', duration, tags = ["support", page_name])
	return

#decorators to link fuctions to url
@app.route('/')
def home():
	page_view_latency("home_page");
	return render_template('home.html')


@app.route('/addition', methods=['GET', 'POST'])
def addition():
	page_view_latency("addition_page");
	return render_template('addition.html')

#starts server
if __name__== '__main__':
	app.run(debug=True)