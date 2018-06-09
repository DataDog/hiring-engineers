##################
## Import Items ##
##################
from flask import Flask, render_template
from helpers import *
from flask_sqlalchemy import SQLAlchemy

############
## Config ##
############
app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('config.py')
db=SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<E-mail %r>' % self.email

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

# Save e-mail to database and send to success page
@app.route('/prereg')
def prereg():
    email = 'ben@gmail.com'
    # Check that email does not already exist (not a great query, but works)
    if not db.session.query(User).filter(User.email == email).count():
        reg = User(email)
        db.session.add(reg)
        db.session.commit()
        return 'check database'
    return render_template('index.html')

#####################
## Run Application ##
######################
if __name__ == '__main__':
    app.run(debug=True, port=8000, host="0.0.0.0")
    #app.run()


# Try and Catch
