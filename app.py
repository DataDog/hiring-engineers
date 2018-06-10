################
## Variables ##
###############
ENVIRONMENT='dev'
team_page='team.html'

##################
## Import Items ##
##################
from flask import Flask, render_template, Response, session
from flask_heroku import Heroku
import blinker as _
import names
import random

from ddtrace import tracer

from helpers.helpers import *
from database.models import *
from cron.cron import *

############
## Config ##
############
app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('config/config.py')
#heroku = Heroku(app)

with app.app_context():
    db.init_app(app)
    if (ENVIRONMENT == 'dev'):
        db.create_all()
        db.session.commit()

add_random_players()
#############
## Tracers ##
#############
@tracer.wrap(name="compilation_of_quotes", service="quotes", resource="valor")
def valor_tracer():
    words=insertQuoteIntoDB('chuck')
    players=selectNumOfTeamMembers('valor')
    return render_template(team_page, quote=words, team='Valor', quote_type="Chuck Norris", players=players)

@tracer.wrap(name="compilation_of_quotes", service="quotes", resource="mystic")
def mystic_tracer():
    words=insertQuoteIntoDB('wisdom')
    players=selectNumOfTeamMembers('mystic')
    return render_template(team_page, quote=words, team='Mystic', quote_type="Wisdom", players=players)

@tracer.wrap(name="compilation_of_quotes", service="quotes", resource="instinct")
def instinct_tracer():
    words=insertQuoteIntoDB('cats')
    players=selectNumOfTeamMembers('instinct')
    return render_template(team_page, quote=words, team='Instinct', quote_type="Cat", players=players)

@tracer.wrap(name="total_players", service="players", resource="players")
def register_tracer():
    if request.method == 'POST':
        name = request.form['username']
        team = request.form['team']
        insertUserIntoDB(name, team)
        return render_template('index.html')
    elif request.method == 'GET':
        name = names.get_first_name()
        team = random.choice(['mystic', 'instinct', 'valor'])
        insertUserIntoDB(name, team)
        return None
    return render_template('register.html')

############
## Routes ##
############
@app.route('/')
def home():
    return render_template('index.html')

# 1. Quotes
@app.route(getURL('team', 'valor'))
def valor():
    return Response(str(valor_tracer()))

@app.route(getURL('team', 'mystic'))
def mystic():
    return Response(str(mystic_tracer()))

@app.route(getURL('team', 'instinct'))
def instinct():
    return Response(str(instinct_tracer()))

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    return Response(str(register_tracer()))

@app.route('/adduser')
def adduser():
    name = names.get_first_name()
    team = random.choice(['mystic', 'valor', 'instinct'])
    return 'hello'

# Charts
@app.route('/charts')
def charts():
    return render_template('charts.html')

#####################
## Run Application ##
######################
if __name__ == '__main__':
    if (ENVIRONMENT == 'dev'):
        app.run(debug=True, port=8000, host="0.0.0.0")
    else:
        app.run()

