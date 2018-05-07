import random
import time

from ddtrace import tracer
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello World!"

@app.route("/quick")
def test():
	return "this is a very quick response."

@app.route("/short")
def short():
	with tracer.trace("/short", service="tomscoolAPI") as span:
		r = random.randint(1,3)

		span.set_tag("my_tag", r)
		time.sleep(r)
		response = "this response takes approx 1 - 3 seconds (" + str(r) + ")"
		return response

@app.route("/long")
def long():
	with tracer.trace("/long", service="tomscoolAPI") as span:
		r = random.randint(2,5)

		span.set_tag("my_tag", r)
		time.sleep(r)
		response = "this response takes approx 2 - 5 seconds (" + str(r) + ")"
		return response