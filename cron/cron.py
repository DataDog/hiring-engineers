import atexit
import datetime
import names
import random
import requests
from urllib.request import urlopen

from apscheduler.scheduler import Scheduler
from helpers.helpers import *

cron = Scheduler(daemon=True)
cron.start()

def add_random_players():
    #urlopen('https://datadog-app.herokuapp.com/adduser')
    return True

cron.add_interval_job(add_random_players, seconds=5)

# Shutdown cron thread if web process is stopped
atexit.register(lambda: cron.shutdown(wait=False))
