import settings
import tweepy
import dataset
from datafreeze import freeze
from textblob import TextBlob

db = dataset.connect(settings.CONNECTION_STRING)

result = db[settings.TABLE_NAME].all()
freeze(result, format='csv', filename='test.csv')
