##################
## Import Items ##
##################
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from helpers import *

############
## Config ##
############
app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('config.py')
db=SQLAlchemy(app)

############
## Routes ##
############
@app.route('/')
def home():
    return render_template('index.html')

# 1. Quotes
@app.route(getURL('quote', 'wisdom'))
def wisdom():
    return render_template('quotes.html', quote=getAPIData('wisdom'))

@app.route(getURL('quote', 'chuck'))
def chuck():
    return render_template('quotes.html', quote=getAPIData('chuck'))

@app.route(getURL('quote', 'cats'))
def cats():
    return render_template('quotes.html', quote=getAPIData('cats'))

# 2. Math game
@app.route(getURL('game', 'math'))
def math():
    return 'Math Game here!'

# 3. Weather App
@app.route('/weather')
def weather():
    return 'Weather application!'

#####################
## Run Application ##
######################
app.run(debug=True, port=8000, host="0.0.0.0")


# Try and Catch
