Your answers to the questions go here.


Note: I spun up a vagrant ubuntu 16.04 distribution and installed MongoDB. 

## Collecting Metrics:

*Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.*

Here is just the hostmap with custom hostname :
https://github.com/shimran/hiring-engineers/blob/master/Screen%20Shot%202018-07-04%20at%2011.21.55%20PM.png

Another screenshot with tag: 
https://github.com/shimran/hiring-engineers/blob/master/Screen%20Shot%202018-07-04%20at%2011.22.06%20PM.png


*Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.*

Screenshot:
https://github.com/shimran/hiring-engineers/blob/master/Screen%20Shot%202018-07-05%20at%205.27.29%20PM.png

Code:

In `/etc/datadog-agent/checks.d`:

```
from checks import AgentCheck
import random
class CheckIncrement(AgentCheck):
  def check(self, instance):
    My_metric=random.randint(0,1000)
    self.gauge('My_metric', My_metric)
```
In `/etc/datadog-agent/checks.d`:
```
init_config:
    default_timeout: 5
instances:
    - min_collection_interval: 45

```

*Can you change the collection interval without modifying the Python check file you created?*

Yes, you can modify the configuration file yaml and add a 'min_collection_interval' to change the collection interval to desired amount of seconds under instances in the conf.d directory 

e.g.

min_collection_interval: 45


## Visualizing Data:


*Utilize the Datadog API to create a Timeboard that contains:

Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket*

I was unable to do an anomaly function...I believe this is a monitor alert, rather than a metric (but if I am wrong, please point this out...I have searched everywhere for it).


See below for Timeboard created via DD-API. 

I did not wipe out the api/app keys. I am cognizant of security, I felt for this excercise there is little to exposure in keeping it in here.

```
from datadog import initialize, api

options = {
    'api_key': '1df6fa95b4e30580f7b85a846520967f',
    'app_key': 'ca541d2fa22c8dce58d9ba70e3f4341642c6a865'
}

initialize(**options)

title = "Shimran's Hiring Excercise Timeboard"
description = "Hiring Excercise"
graphs = [{
    "definition": {
        "events": [],
        "viz": "timeseries",
        "requests": [
            {"q": "My_metric{host:mymachine.shimrangeorge}", "type": "line"
            },
            {"q": "sum:My_metric{host:mymachine.shimrangeorge}.rollup(sum, 3600)",
            "type": "line",
                "style":{
                "palette": "red"
                }
            },
            {"q": "mongodb.mem.bits{host:mymachine.shimrangeorge}",
            "type": "line",
                "style":{
                "palette": "green"
                }
            }
      ],
    },

        "title": "Hiring Excercise: Timeboard-Shimran George"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]
read_only = True
api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)


```

I took screenshots of the timeboard to show metric, rollup sum, and integration metric on same timeboard:

https://github.com/shimran/hiring-engineers/blob/master/Screen%20Shot%202018-07-05%20at%2010.54.05%20PM.png
https://github.com/shimran/hiring-engineers/blob/master/Screen%20Shot%202018-07-06%20at%2012.23.31%20AM.png

@mention snapshot:
https://github.com/shimran/hiring-engineers/blob/master/Screen%20Shot%202018-07-05%20at%2010.56.31%20PM.png

Anomaly monitor:
https://github.com/shimran/hiring-engineers/blob/master/Screen%20Shot%202018-07-06%20at%2012.23.08%20AM.png


*What is the Anomaly graph displaying?*

The Anomaly graph displays abberrant behavior within a metric as compared to historical data the agent has tracked throughout the certain variables such as time-of-day trends.i

## Monitoring Data

*Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:*

*Warning threshold of 500*
*Alerting threshold of 800*
*And also ensure that it will notify you if there is No Data for this query over the past 10m.*

Monitor Screenshot:
https://github.com/shimran/hiring-engineers/blob/master/Screen%20Shot%202018-07-06%20at%2012.29.10%20AM.png

Alert Email Screenshot:
https://github.com/shimran/hiring-engineers/blob/master/Screen%20Shot%202018-07-05%20at%209.09.46%20PM.png

*Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:*

Screenshots of Downtime setup:

https://github.com/shimran/hiring-engineers/blob/master/Screen%20Shot%202018-07-05%20at%209.20.28%20PM.png
https://github.com/shimran/hiring-engineers/blob/master/Screen%20Shot%202018-07-05%20at%209.20.44%20PM.png

Screenshot for Notification Email of Downtime:

https://github.com/shimran/hiring-engineers/blob/master/Screen%20Shot%202018-07-05%20at%209.21.00%20PM.png
I should note, the Datadog email puts the time in UTC despite scheduling in PST. I took a picture of the actual UI downtime rule to show this was scheduled as per specification. 
I probably would put a feature request to have the email put the time in the proper time zone that is configured in the UI.





## Collecting APM Data:

*Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.*
https://github.com/shimran/hiring-engineers/blob/master/Screen%20Shot%202018-07-06%20at%2012.43.20%20AM.png

*Please include your fully instrumented app in your submission, as well.*

I used the python app provided, but I did play around with both dd-trace and Trace Middleware.
```
from flask import Flask
#import blinker as _
import logging
import sys
from ddtrace import tracer
#from ddtrace.contrib.flask import TraceMiddleware


#http://pypi.datadoghq.com/trace/docs/#flask
# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)
#traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)


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
~

```



*What is the difference between a Service and a Resource?*

To be fair, it is explained here: https://help.datadoghq.com/hc/en-us/articles/115000702546-What-is-the-Difference-Between-Type-Service-Resource-and-Name-

They are fundamentally different concepts. Services can be distinct components of a feature set that create a webapplication. For example, the web application has a database service, as ervice that provides core functionality, and other services like search that may be distinct but compromise 

A resource, on the other hand, is "a particular query to a service," but if probably best thought of as a transaction that engages with the service. URLs that map to parts of an application, the SQL transaction itself, are all transactions that occur that interface with the respective webapp and db service. 


## Final Question:
*Is there anything creative you would use Datadog for?*

I have many interests that fascinate me, especially infrastrcture. Since NYC subway was taken and I work in computer infrastructure, I think I want to focus on food perishability. The whole idea of food lifetimes and food management interests me...especially considering how much food inevitably ends up wasted.

I would like to develop an app that parses a grocery receipt (Ideally, this would work mainly for emailed grocery receipts...but lets assume we have image processing software in this app, and it can parse a receipt for a grocery item). Essentially, this app would be a large database. Imagine, one day you buy 10 apples. This data gets processed and assigned the date of purchase. It also will set up a countdown on the shelf life of the apple based on an industry standard. This works on the assumption that if a grocery store is still selling the apple, it is still in good condition. I could use Datadog to set Threshold alerts to determine the supposed expiration of the apples. If the apples have a shelf life of 10 days, for example, I could set alerts 5 days before expiration, and 2 days before expiration. I additionally can do a monitor inventory of the apples to determine how many are left. This could lead to two scenarios: 1) Not only could I send an alert if the apples drop below 3 in inventory, and send an alert to restock 2) I could make a more complex rule that if number of apples are greater than 5, and the days_until_expiration < 2 days, I could trigger an alert that also sends recipes that require apples to encourage people to use all the apples before they go bad.

One can gather data about consumption patterns, time of purchase etc...as Datadog metrics as well.

I'd be happy to elaborate on this and other ideas I have for metrics!

Other Idea:

1) Use datadog for BBQ smokers. Integrate and send an alert when temperature drops below or rises above specified temperature. You can probably set up a Raspbery PI and put a thermometer probe to send the data.
  
 
 
