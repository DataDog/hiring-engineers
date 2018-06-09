##################
## Import Items ##
##################
from flask import Flask, render_template, Response
from flask_sqlalchemy import SQLAlchemy
import blinker as _

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

from helpers.helpers import *
from database.models import *

############
## Config ##
############
app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('config/config.py')

with app.app_context():
    db.init_app(app)
    db.create_all()
    db.session.commit()

#############
## Tracers ##
#############
@tracer.wrap(name="compilation_of_quotes", service="quotes", resource="wisdom")
def wisdom_tracer():
    words=insertIntoDB('wisdom')
    return render_template('quotes.html', quote=words)

@tracer.wrap(name="compilation_of_quotes", service="quotes", resource="chuck")
def chuck_tracer():
    words=insertIntoDB('chuck')
    return render_template('quotes.html', quote=words)

@tracer.wrap(name="compilation_of_quotes", service="quotes", resource="cats")
def cat_tracer():
    words=insertIntoDB('cats')
    return render_template('quotes.html', quote=words)

############
## Routes ##
############
@app.route('/')
def home():
    return render_template('index.html')

# 1. Quotes
@app.route(getURL('quote', 'wisdom'))
def wisdom():
    return Response(str(wisdom_tracer()))

@app.route(getURL('quote', 'chuck'))
def chuck():
    return Response(str(chuck_tracer()))

@app.route(getURL('quote', 'cats'))
def cats():
    return Response(str(cat_tracer()))

"""
# 2. Math game
@app.route(getURL('game', 'math'))
def math():
    return 'Math Game here!'

# 3. Weather App
@app.route('/weather')
def weather():
    return 'Weather application!'
"""

#####################
## Run Application ##
######################
if __name__ == '__main__':
    app.run(debug=True, port=8000, host="0.0.0.0")
    #app.run()

