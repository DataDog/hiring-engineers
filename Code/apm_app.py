from flask import Flask
import logging
import sys
from random import randint
import datetime


main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

@app.route('/')
def api_entry():
    return 'Welcome to the Application\nFor date got to navigate to /date\nTo find your lucky number navigate to /lucky :P \n'

@app.route('/date')
def date():
    return "The time now is {}\n".format(datetime.datetime.now())

@app.route('/lucky')
def lucky():
    return "Your lucky number is {} :-)\n".format(randint(1,9))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8500')
