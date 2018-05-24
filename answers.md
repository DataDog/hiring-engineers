# Answers from Ben Sunderland  -  May 18th 2017
====================================

## Part 1: Collecting Metrics

After the agent installs on my Ubuntu VM, I added Tags as follows : 


Set the host's tags (optional) 

```
tags:
  - ben.com
  - env:dev1
  - role:docker_host1
```
Shown here is the host map view showing the custom tags : 

<img width="923" alt="host_map___datadog" src="https://user-images.githubusercontent.com/2524766/40302853-e0d357ce-5d33-11e8-89c0-52d8ef48f8b5.png">


# Install a database on your machine 

<img width="1371" alt="mysql_-_overview___datadog" src="https://user-images.githubusercontent.com/2524766/40284386-d879ea1e-5cd1-11e8-8c0d-eca87724a476.png">

# Create a custom Agent check ....

<img width="1300" alt="my_metric" src="https://user-images.githubusercontent.com/2524766/40341720-0ee59906-5dca-11e8-8253-6d1c0e17999e.png">

(you can change the interval via the check config "min_collection_interval: 45" )

## Part 2: Visualizing Data

Here is my Python script with the 3 graphs in the Timeboard:

(Note: I tried the same graph definitions with the bash script approach and got parsing errors - the same graph definitions worked in Python)

```
from datadog import initialize, api

options = {
    'api_key': 'c18b36aebb7ed23a8fb3c53aad91c38e',
    'app_key': '3de69df6bb0d2662d12d543d8f8eecdf615cd269'
}

initialize(**options)

title = "Bens Timeboard v2"
description = "DD Timeboard."
graphs = [
{
          "title": "Bens check scoped",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{host:osboxes}"}
              ]
          },
          "viz": "timeseries"
      },

      {
          "title": "Bens Check roll up",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "my_metric{host:osboxes}.rollup(sum,3600)"}
              ]
          },
          "viz": "timeseries"
      },

      {
          "title": "mysql anomaly",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "anomalies(avg:mysql.performance.user_time{*}, 'basic', 2)" }
              ]
          },
          "viz": "timeseries"
      }

]

read_only = True 
api.Timeboard.create(title=title,description=description,graphs=graphs,read_only=read_only)


```
Here is the resultant timeboard : 

<img width="1326" alt="timeboard v3" src="https://user-images.githubusercontent.com/2524766/40341495-e73495e8-5dc8-11e8-8da5-80aa5e6407dc.png">

Here is the @message of the MySQL graph with Anomalies :

<img width="522" alt="events___datadog" src="https://user-images.githubusercontent.com/2524766/40302424-66adeac8-5d32-11e8-8627-8392aaa2ef83.png">

Anomaly detection is an algorithmic feature that allows you to identify when a metric is behaving differently than it has in the past, taking into account trends, seasonal day-of-week and time-of-day patterns. It is well-suited for metrics with strong trends and recurring patterns that are hard or impossible to monitor with threshold-based alerting.

In this example we are looking at mysql.performance.user_time metric and the gray envelope shows the range + or - 2 std deviations from a calcualted normal. In this case we are using the 'basic' modifier which:
"... uses a simple lagging rolling quantile computation to determine the range of expected values, but it uses very little data and adjusts quickly to changing conditions but has no knowledge of seasonal behavior or longer trends."

# Part 3 - Monitoring

Here is the configuration for the notification for my monitor: 

<img width="606" alt="monitor config" src="https://user-images.githubusercontent.com/2524766/40344281-6e97b35e-5dd7-11e8-84d4-9f08279ece3f.png">


Email alert received based on the monitor rule violation:

<img width="644" alt="alert" src="https://user-images.githubusercontent.com/2524766/40349547-46c7590c-5dea-11e8-9c8e-51ba33c1a1a0.png">

Here are the configurations for downtime: 

![downtime1](https://user-images.githubusercontent.com/2524766/40345587-24a68daa-5ddd-11e8-8b69-b56973bc0101.png)

![downtime2](https://user-images.githubusercontent.com/2524766/40345589-2958e8ac-5ddd-11e8-81e5-9cf64b21ed89.png)


Email notification received based on the monitor scheduled downtime: 

<img width="1028" alt="_datadog__ben_sunderland_scheduled_downtime_on_my_metric_is_over_the_threshold_-_ben_sunderland22_gmail_com_-_gmail" src="https://user-images.githubusercontent.com/2524766/40345539-eb3c5b94-5ddc-11e8-861a-709500abea87.png">


# Part 4 - Tracing

Bonus Question : 
A service is a set of processes that do the same job. For example an application might have multiple components or services, such as web service and a data layer service. These are automatically discovered with our APM monitoring.

A Resource is a particular action for a service. Its the next level down in granularity from the service. For example, if the service is a web service, the resource is a route or url. For a DB it could be a specific query. 




For the APM tracing I chose the Python App.
Note I tested instrumenting using both approaches. First I used the ddtrace-run command, where I didnt need to change the python code at all to get the service and resources with traces. 

For the second method, I used the middleware objects and ran the python code as usual - also I got the same visibility of service / resources.

Here is my instrumented Python code : 

```

from flask import Flask
import blinker as _

import logging
import sys

#import the datadog tracer
from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware


# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)


app = Flask(__name__)
# create a TraceMiddleware object
traced_app = TraceMiddleware(app, tracer, service="myflaskapp", distributed_tracing=False)


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
          app.run(host='0.0.0.0', port=8080)





```


APM Service Dashboard - Out of the box APM Dashboard showing a summary of the service:

<img width="1300" alt="apm1" src="https://user-images.githubusercontent.com/2524766/40357179-ac9f3bb4-5dfe-11e8-92f5-508a020a8686.png">

APM Resource Dashboard - Out of the box APM Dashboard showing a summary of the resources contained within the service above:

<img width="1319" alt="apm2" src="https://user-images.githubusercontent.com/2524766/40357194-b4299ea6-5dfe-11e8-90dc-c6de7e8edeb3.png">



Dashboard of APM together with server infra metrics:

<img width="1308" alt="apm and infra" src="https://user-images.githubusercontent.com/2524766/40357208-c42f7442-5dfe-11e8-9939-c277884c8e6e.png">


# Part 5 - Final Question


I had two ideas for using DD in interesting ways.

1) DD company business monitoring 
The concept would be to monitor the health of the DD business across a range of metrics and then to understand the correlation to other drivers - for example, you would track total company revenue and then split by geography , by monitored tech , and then correlate with things like marketing spend and headcount and other cost of sale.

e.g. you could then dashboard the current quarter revenue vs target and slice that by all customers using APM vs Log vs Infra , and then by those with cloud hosts (AWS vs Azure etc). 
Then you could look for changes in revenue post marketing initiatives / events.
This would be interesting to correlate business KPIs across regions and to use trend data to make forecasts - e.g. when we increased the field sales headcount in EMEA by x% we saw an increase in average deal size by y% etc etc. 

2) World Cup 2018 insights
On a lighter note, this idea is to pull metrics from the web on world cup data and use to forecast the winner and then take this to the book makers. 
E.g. you could look at correlation and patters between team and individual form (published on world cup sites) and then correlate that with team results in real time. Then based on that you could use our forecasting to predict teams most likley to progress - and use to make bets.
:D







