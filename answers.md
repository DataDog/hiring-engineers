If you want to apply as a Solutions or Sales Engineer at [Datadog](http://datadog.com) you are in the right spot. Read on, it's fun, I promise.


<a href="https://www.datadoghq.com/careers/" title="Careers at Datadog">
<img src="https://imgix.datadoghq.com/img/careers/careers_photos_overview.jpg" width="1000" height="332"></a>

## The Exercise

Don’t forget to read the [References](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#references)

## Questions

Please provide screenshots and code snippets for all steps.

## Prerequisites - Setup the environment

You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

* You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. [Here are instructions](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#vagrant) for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum `v. 16.04` to avoid dependency issues.
* You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.

Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.

***Ans:  I utilized the dockerized Datadog Agent as well as a Windows Datadog Agent upon which I did my PostgreSQL integration***

##

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

***Ans:***

***Screenshot of Windows Agent***

<img src="Tags Screenshot 1.png">

##

***Screenshot of Dockerized Agent***

<img src="Tags Screenshot 2.png">

##

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

***Ans:  I installaed PostgreSQL --- screenshot of PostgreSQL integration***

<img src="PostgreSQL integration.png">

##

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

***Ans:  --- c:\ProgramData\Datadog\checks.d\my_check.py***

```python

# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"


import random

class my_check_metric(AgentCheck):
    def check(self, instance):
        self.gauge('my_check_metric_value', random.randint(0, 1000))
``` 

##

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

***Ans:  --- c:\ProgramData\Datadog\conf.d\my_check.yaml***

```
instances:
  - min_collection_interval: 45
```
##

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

***Ans:  Yes, you can by modifying the "\<check>.yaml" configuration file for the instance***

##


## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

***Ans:  Script to create the Timeboard***

```
from datadog import initialize, api
import socket

options = {
    'api_key': 'feb8891bd26d35ab3ab3c088a6563710',
    'app_key': 'df4f8e86af7bcce78007f04f8d53d33b5c8e4aa5'
}

initialize(**options)

title = 'VIMAL KANERIA - DatadogNew Hire Dashboard Solution'
widgets = [

{   'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_check_metric_value{host:DESKTOP-0S76KLQ}'}
        ],
        'title': 'My Random Check Metric'
}},

{   'definition': {
        'type': 'timeseries',
        'requests': [
            {"q": "anomalies(avg:postgresql.buffer_hit{host:DESKTOP-0S76KLQ}, 'basic', 1)"}
        ],
        'title': 'Postgres Anomaly Metric'
}},

{
	'definition': {
        'type': 'timeseries',
        'requests': [
            {"q": "my_check_metric_value{host:DESKTOP-0S76KLQ}.rollup(sum, 3600)"}
        ],
        'title': 'My Random Check Metric Rollup'
}}

]

layout_type = 'ordered'
description = 'A dashboard of my custom check metric value'
is_read_only = True
notify_list = ['vimal@kaneria.com']
template_variables = [{
    'name': 'scope',
    'prefix': 'host',
    'default': socket.gethostname()
}]



api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables)
```

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes

***Ans:  Screenshot of Timeboard - "Past 5 Minutes" interval***

<img src="Timeboard 5 mins.png">

##

* Take a snapshot of this graph and use the @ notation to send it to yourself.

<img src="PostgreSQL Anomaly Metric.png">

##

<img src="My Random Check Metric.png">

##

<img src="My Random Check Metric Rollup.png">

##

* **Bonus Question**: What is the Anomaly graph displaying?

***Ans:    The anomaly graph is displaying when data is out of normal ranges based on historical predictable patterns, without historical data ther graph is not meaningful***

##

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

***Ans:***

<img src="Monitor Screenshot.png">

##

* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

<img src="email notification screenshot.png">

##

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
  
***Ans:***

<img src="scheduled downtime email.png">

##

## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

```python
from flask import Flask
import logging
import sys

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

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
    app.run(host='0.0.0.0', port='5050')
```

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

***Ans:  used "ddtrace-run" for this***
##

* **Bonus Question**: What is the difference between a Service and a Resource?

***Ans:  A service is a set of processes that do the same job \[i.e. database].  A resource is a particular action within a given service \[i.e query]***
##

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

***Ans:*** [https://p.datadoghq.com/sb/jz1ihhw7w5m1qtc4-3d4ffce1148d890c733dacea56865e66]

<img src="apm and infrastructure.png">

Please include your fully instrumented app in your submission, as well.

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

***Ans:***
***1. Monitor solar panel production efficiency, enable anomaly detection to predict abnormal patterns***
***2. Monitor using IoT of things in combination with Big Data and ML to potentially predict next pandemic*** 
