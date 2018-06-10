import atexit
import datetime
#from urllib.request import urlopen
import urllib2
import time

from apscheduler.scheduler import Scheduler
from helpers.helpers import *

cron = Scheduler(daemon=True)
cron.start()

# Wanted to try to ping the /adduser endpoint to continously add users onto the database
def add_random_players():
    time.sleep(10)
    #urllib2.urlopen('https://datadog-app.herokuapp.com/adduser')
    #urlopen('https://datadog-app.herokuapp.com/adduser')
    return True

cron.add_interval_job(add_random_players, seconds=15)

# Shutdown cron thread if web process is stopped
atexit.register(lambda: cron.shutdown(wait=False))
