import random
from ddtrace import tracer

tracer.configure(
    hostname=os.environ['DD_AGENT_HOST'],
    port=os.environ['DD_TRACE_AGENT_PORT'],
)


class Myrandom:

    self.gauge(
        "my_metric.gauge",
        random.randint(0, 1000),
        tags=["env:dev", "metric_submission_type:gauge"],
    )

def myfunc(n):
  return lambda a : a * n



i = 1
while i < 100000:
  print(i)
  i += 1