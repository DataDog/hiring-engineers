from ddtrace import tracer
import time

#trace = tracer.trace("app.request","myPythonApp").finish()

for x in range(0,100):
  trace = tracer.trace("app.request","myPythonApp").finish()
  time.sleep(7)
  print(x)
