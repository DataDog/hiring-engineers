from ddtrace import tracer
import time
import random

while True:
    span = tracer.trace("My_Interval",service="Fake_Serv")
    time.sleep(random.randint(15,25))
    span.finish()
