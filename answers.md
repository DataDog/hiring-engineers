# Collecting Metrics:
Added tags hello:world and role:exercise

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

### Set the Timeboard's timeframe to the past 5 minutes

![alt text](https://github.com/josephrivers/hiring-engineers/blob/master/support%20images/unnamed.png)


Link - https://app.datadoghq.com/dash/873292/my-timeboard?live=true&page=0&is_auto=false&from_ts=1532736031198&to_ts=1532739631198&tile_size=m


#### Bonus Question: What is the Anomaly graph displaying?

**Answer:** The Anomaly graph displays current activity along side expected activites based on historical data and shows when those patterns are broken.


# Monitoring Data:

### Send email with custom message and value whenever triggered
![alt text](https://github.com/josephrivers/hiring-engineers/blob/master/support%20images/IMG_3619.PNG)


 

### Bonus Question: Downtime for weeknighs and the weekends.
![alt text](https://github.com/josephrivers/hiring-engineers/blob/master/support%20images/IMG_3624.PNG)


# Collecting APM Data:

```python
from ddtrace import tracer

with tracer.trace("apm.basics", service="apm_services") as span:
  span.set_tag("role", "exercise")
```

![alt text](https://github.com/josephrivers/hiring-engineers/blob/master/support%20images/Screen%20Shot%202018-07-27%20at%208.39.03%20PM.png)

Link - https://app.datadoghq.com/apm/service/apm_tracer/my_metric?start=1532735893790&end=1532739493790&env=none&paused=false

#### Bonus Question: What is the difference between a Service and a Resource?

**Answer:** A service is a set of process that are doing a particular job. Where a resource is an action against a service such as a restful request to a webserver(process).

# Final Question:

#### Is there anything creative you would use Datadog for?

1(practical). A good creative way to use Datadog, would be to monitor and report outages of utilities and services. Growing up in the NY suburbs, there's constantly outages do to hurricane season, heavy snow in the winter and accidents. Utilities and service providers getting information in real time without needing reports of outages from their customers will help them organize a solution faster. Telling the customer this information lets them know of the situation and that the company is on top of it without the customer needed to call having to call.

2(Fun). With E-Sports becoming more popular. Stats will become just as important as they are in other sports. Using Datadog, stats that have never been collected be collected now. This is good information that commentators to use. Example: last time someone got a 20 kills without dying in a round was John Smith September 9th 2017 at the grand tournament. This is good for old historical data. But Datadog’s ability to monitor real time can take it a step further. During tournaments, it can keep track of all stats across all games at once and compare this data to show who’s doing the best in which areas. This data can be display to people watching for a better experience.


