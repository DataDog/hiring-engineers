##################
## Import Items ##
##################
from flask import Flask, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku
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
heroku = Heroku(app)

with app.app_context():
    db.init_app(app)
    db.create_all()
    db.session.commit()

################
## Variables ##
###############
teamPage='team.html'

#############
## Tracers ##
#############
@tracer.wrap(name="compilation_of_quotes", service="quotes", resource="valor")
def valor_tracer():
    words=insertIntoDB('chuck')
    return render_template(teamPage, quote=words, team='Valor', quote_type="Chuck Norris")

@tracer.wrap(name="compilation_of_quotes", service="quotes", resource="mystic")
def mystic_tracer():
    words=insertIntoDB('wisdom')
    return render_template(teamPage, quote=words, team='Mystic', quote_type="Wisdom")

@tracer.wrap(name="compilation_of_quotes", service="quotes", resource="instinct")
def instinct_tracer():
    words=insertIntoDB('cats')
    return render_template(teamPage, quote=words, team='Instinct', quote_type="Cat")

############
## Routes ##
############
@app.route('/')
def home():
    return render_template('index.html')

# 1. Quotes
@app.route(getURL('team', 'valor'))
def chuck():
    return Response(str(valor_tracer()))

@app.route(getURL('team', 'mystic'))
def wisdom():
    return Response(str(mystic_tracer()))

@app.route(getURL('team', 'instinct'))
def cats():
    return Response(str(instinct_tracer()))

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
    #app.run(debug=True, port=8000, host="0.0.0.0")
    app.run()

