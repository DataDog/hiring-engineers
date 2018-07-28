# Collecting Metrics:
Added tags hello:world, role:exercise

![alt text](https://github.com/josephrivers/hiring-engineers/blob/master/support%20images/Screen%20Shot%202018-07-27%20at%206.29.37%20PM.png)

### Custom Agent Check
```python
from datadog_checks.checks import AgentCheck
from random import randrange

class RandomCheck(AgentCheck):
  def check(self, instance):
		self.gauge('my_metric', randrange(0, 1000))
```

#### Bonus Question: Can you change the collection interval without modifying the Python check file you created?

**Answer:** The interval can be changed in the UI in the matadata of the metric.


# Visualizing Data:
```python
from datadog import initialize, api

options = {'api_key': '###', 'app_key': '###'}

initialize(**options)

# Timeboard
title = "My Timeboard"
description = "my metric data board"
graphs = [{
    "title": "Metric data",
    "definition": {
		"events": [],
		"requests": [
		    {"q": "anomalies(avg:my_metric{host:vagrant}, 'basic', 2)"},
		    {"q": "avg:my_metric{host:vagrant}.rollup(sum, 3600)"}
		],
    }
}]
read_only = False

api.Timeboard.create(title=title, description=description,graphs=graphs, read_only=read_only)
```
Link - https://app.datadoghq.com/dash/873292/my-timeboard?live=true&page=0&is_auto=false&from_ts=1532736031198&to_ts=1532739631198&tile_size=m

Set the Timeboard's timeframe to the past 5 minutes

![alt text](https://github.com/josephrivers/hiring-engineers/blob/master/support%20images/unnamed.png)


#### Bonus Question: What is the Anomaly graph displaying?

**Answer:** 


# Monitoring Data:

Send email with custom message and value whenever triggered
![alt text](https://github.com/josephrivers/hiring-engineers/blob/master/support%20images/IMG_3619.PNG)



#### Bonus Question: Downtime
![alt text](https://github.com/josephrivers/hiring-engineers/blob/master/support%20images/IMG_3624.PNG)


# Collecting APM Data:

```python
from ddtrace import tracer

with tracer.trace("apm.basics", service="apm_services") as span:
  span.set_tag("role", "exercise")
```

![alt text](https://github.com/josephrivers/hiring-engineers/blob/master/support%20images/Screen%20Shot%202018-07-27%20at%208.39.03%20PM.png)

Link - https://app.datadoghq.com/apm/service/apm_tracer/my_metric?start=1532735893790&end=1532739493790&env=none&paused=false

