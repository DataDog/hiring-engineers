# Setup the environment

I started off by setting up a virtual environment using Vagrant on my laptop. I used bento/ubuntu-16.04 to install Ubuntu 16.04. Following this, I created a datadog trial account. Using the key information from the newly created account, I setup my environment by installing the Datadog Agent and a tool I like to use called midnight commander(mc).


# Collecting Metrics:

I started with adding tags to the datadog yaml file. The tags that I added were hello:world and role:exercise. I used the basic “hello world” placeholder but also decided to add the “role:exercise” to tag this as an exercise and not production. 

![alt text](https://github.com/josephrivers/hiring-engineers/blob/master/support%20files/images/Host%20map%20and%20tags.png)

## Postgres Intergration

I followed that up with installing Postgres in the virtual environment. I setup and confirmed the permissions for the datadog user in Postgres. Then changed the postgres yaml configuration for the agent. After doing all of this I installed the Postgres integration in the Datadog UI.

![alt text](https://github.com/josephrivers/hiring-engineers/blob/master/support%20files/images/Postgres%20dashboard.PNG)

## Custom Agent Check

I created a new file under the folder “checks.d” with the name “customchecks.py.” In there I created a custom agent check for “my_metric” to receive a value between 0-1000 using a random number generator. This was written in python and I used the agents gauge function to receive these values over time. I created a new yaml file with the same name as my python file, under “conf.d” for configuring the check.

```python
from checks import AgentCheck
from random import randrange

class RandomCheck(AgentCheck):
  def check(self, instance):
		self.gauge('my_metric', randrange(0, 1000))
```

#### Bonus Question: Can you change the collection interval without modifying the Python check file you created?

**Answer:** The interval can be changed in the UI in the matadata of the metric.


# Visualizing Data:

## Timeboard

Next using the Datadog API, I created a timeboard called “My Timeboard” for the metric “my_metric.” Included in the timeboard are both the anomaly function and the rollup function for “my_metric.” 

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
I followed this up with going to the timeboards UI and setting the graph to the past 5 minutes. Using the timeboards “snapshot” feature, I sent a report of this data to myself.

### Set the Timeboard's timeframe to the past 5 minutes and send notification

![alt text](https://github.com/josephrivers/hiring-engineers/blob/master/support%20files/images/5%20min%20metric.png)

#### Bonus Question: What is the Anomaly graph displaying?

**Answer:** The Anomaly graph displays current activity along side expected activites based on historical data and shows when those patterns are broken.


# Monitoring Data:

In the UI under monitors, I created a new threshold monitor called “high metric alert” to monitor the metric “my_metric.” The alert threshold was set up for average values over 800 and “warning” for average values over 500 over a 5 minute time period. I set a notification for missing data over a 10 minute time span. All three of these would send custom messages with alert and warning showing the value of the metric.

```
{{#is_alert}}Alert! Your metric is too high with a value of {{value}}.  {{/is_alert}}

{{#is_warning}}Warning! Your metric is growing fast - {{value}}.  {{/is_warning}}
 
{{#is_no_data}}No Data! This metric is lacking data. {{/is_no_data}}
 
@joseph.thomas.rivers@gmail.com
```

![alt text](https://github.com/josephrivers/hiring-engineers/blob/master/support%20files/images/Custom%20warning.PNG)


 

## Bonus Question: Downtime for weeknights and the weekends.
At this point I created some downtime schedules in the UI under “manage downtime.” I started off by created downtime for Monday-Friday 7pm-9am. I did this by setting the start time to 7pm and having it go for 14 hours on the weekdays. Next I created one for all day Saturday and all day Sunday. This was done by selecting Saturday and Sunday and setting downtime to a day. These were both done for the virtual environment host and later added the tag “role:exercise.”

I realized a gap and some overlap after setting this up. The gap is there's no downtime for Monday 12am-9am. Simple solution would be to create a downtime for this time period. Another solution would be to include Sunday in the weekday downtime but this causes overlapping downtime Sunday night. The third solution leads into the overlap in the current solution. The overlap is Saturday 12am-9am do to fridays downtime going for 14 hours because it's apart of the weekday downtime. The solution would be to shift the weekends start time to 9am and leaving it to a day(24 hours) of downtime or 2 days from saturday. This is will cause the weekend downtime to end 9am Monday.

A notification for each was setup of with custom messages to notify when the downtime has started.

![alt text](https://github.com/josephrivers/hiring-engineers/blob/master/support%20files/images/Scheduled%20down%20time.PNG)



# Collecting APM Data:

I took the Flask app provided and instrumented it using the APM.

```python
from flask import Flask
import blinker as _
import logging
import sys

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware
from ddtrace import patch_all

main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

traced_app = TraceMiddleware(app, tracer, service="tracer-flask", distributed_tracing=False)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5051')
```

Next I created a new dashboard showing both APM data and system metric data.

![alt text](https://github.com/josephrivers/hiring-engineers/blob/master/support%20files/images/APM%20Dashboard.png)

**Link to APM** - https://p.datadoghq.com/sb/9a994d2a2-de255325f8ff6c461f307736a3b1a7f0


### Bonus Question: What is the difference between a Service and a Resource?

**Answer:** A service is a set of processes that are doing a particular job. Where a resource is an action against a service such as a restful request to a webserver(process).

# Final Question:

**Is there anything creative you would use Datadog for?**

1(practical). A good creative way to use Datadog, would be to monitor and report outages of utilities and services. Growing up in the NY suburbs, there's constantly outages do to hurricane season, heavy snow in the winter and accidents. Utilities and service providers getting information in real time without needing reports of outages from their customers will help them organize a solution faster. Telling the customer this information lets them know of the situation and that the company is on top of it without the customer needed to call having to call.

2(Fun). With E-Sports becoming more popular. Stats will become just as important as they are in other sports. Using Datadog, stats that have never been collected be collected now. This is good information that commentators to use. Example: last time someone got a 20 kills without dying in a round was John Smith September 9th 2017 at the grand tournament. This is good for old historical data. But Datadog’s ability to monitor real time can take it a step further. During tournaments, it can keep track of all stats across all games at once and compare this data to show who’s doing the best in which areas. This data can be display to people watching for a better experience.


