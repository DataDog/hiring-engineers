from ddtrace import patch_all
from ddtrace import tracer
patch_all(logging=True)
from flask import Flask
from pymongo import MongoClient
import logging
import sys
import requests
from random import randint

FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
          '[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
          '- %(message)s')
logging.basicConfig(level=logging.DEBUG, filename='app.log', format=FORMAT)

app = Flask(__name__)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

@app.route('/api/magic')
def magic_endpoint():
    print('in')
    if randint(0, 100) <=5:
      main_logger.error('counterspelled')
    else:
      r = requests.get('https://api.magicthegathering.io/v1/cards?pageSize=1&random=true')
      response = r.json()
      cards = response['cards']
      card = cards[0]
      client = MongoClient("mongodb://127.0.0.1:27017")
      db = client.mdb
      result=db.magic.insert_one({'name': card['name']})
      current_span = tracer.current_span()
      if current_span:
        current_span.set_tag('card.id', card['multiverseid'])
        current_span.set_tag('card.set', card['setName'])
      return 'Added ' + card['name']  + ' to collection'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
