import schedule
import time
import os

def job():
  os.system('python custom_metric.py')

schedule.every(45).seconds.do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)