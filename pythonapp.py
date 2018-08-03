from ddtrace import tracer
import time

#trace = tracer.trace("app.request","pythonapp").finish()

for x in range(0,1000):
  trace = tracer.trace("app.asking.for.stuff","pythonapp").finish()
  time.sleep(10)
  print(x)
