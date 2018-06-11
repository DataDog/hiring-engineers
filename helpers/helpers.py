from flask import request
import requests
from database.models import *

WISDOM_API_ENDPOINT='https://talaikis.com/api/quotes/random/'
CHUCK_API_ENDPOINT='https://api.chucknorris.io/jokes/random'
CATS_API_ENDPOINT='https://catfact.ninja/fact'

VERSION='v1'

# General Helper Methods
def getURL(category, pathway=''):
    return '/{}/{}/{}'.format(VERSION, category, pathway)

def getAPIData(endpoint):
    if endpoint == 'wisdom':
        return requests.get(WISDOM_API_ENDPOINT).json()['quote']
    elif endpoint == 'chuck':
        return requests.get(CHUCK_API_ENDPOINT).json()['value']
    elif endpoint == 'cats':
        return requests.get(CATS_API_ENDPOINT).json()['fact']

# Database Helper Methods
def insertQuoteIntoDB(category):
    words = getAPIData(category)
    words_to_insert_db = Quote(words=words, category=category)
    if not db.session.query(Quote).filter(Quote.words == words).count():
        db.session.add(words_to_insert_db)
        db.session.commit()
    return words

def insertUserIntoDB(name, clan):
    user_to_insert_db = User(username=name, team=clan)
    if not db.session.query(User).filter(User.username == name).count():
        db.session.add(user_to_insert_db)
        db.session.commit()
    return name

def selectNumOfTeamMembers(clan):
    return User.query.filter_by(team=clan).count()

def userIsValid(username):
    if User.query.filter_by(username=username).count():
        return True
    return False


