Your answers to the questions go here.

## Prerequisites - Setup the environment:
For the exercise I decided to explore a few different scenarios where Datadog would typically be utilised so I could experience the process and integrations - on prem (Datadog docker container, standalone linux host) and Cloud (Azure container instance).


## Collecting Metrics:
### Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
![Host Map](https://i.imgur.com/DUHFXTo.png)

### Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
![MySQL](https://i.imgur.com/3DbGMBt.png)

### Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
Created /etc/datadog-agent/checks.d/custom_random.py
```
import random
from checks import AgentCheck

__version__ = "0.0.1"

class RandomValue(AgentCheck):
      def check(self, instance):
          data = random.randint(1,1000)
          self.gauge('my_metric', data,tags=['metric:custom'])
```

### Change your check's collection interval so that it only submits the metric once every 45 seconds.
### Bonus Question Can you change the collection interval without modifying the Python check file you created?
Both of the above are achieved by leveraging the associated /etc/datadog-agent/conf.d/custom_random.yaml
```
init_config:
instances:
    [{
        min_collection_interval: 45
     }]
```

## Visualizing Data:
I used the below python script to create the dasbhoard:
```
from datadog import initialize, api

options = {
    'api_key': '190f120effc6772ee2bbebecb4d856b3',
    'app_key': '934daad7e6e4f631209e6a22da64c211dea85f19'
}

initialize(**options)

title = 'Super Test Dashboard'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{host:ubuntu_dd}'}
        ],
        'title': 'My random metric'
        }
},{
    'definition': {
        'type': 'timeseries',
        'requests': [
                {'q': 'sum:my_metric{host:ubuntu_dd}.rollup(sum, 3600)'}
        ],
        'title': 'My random metric rollup'
        }
},{
    'definition': {
        'type': 'timeseries',
        'requests': [
                {"q": "anomalies(avg:mysql.performance.cpu_time{host:ubuntu_dd}, 'basic', 2)"}
        ],
        'title': 'MySQL anomalies'
        }
}]

layout_type = 'ordered'
description = 'Test dashbaord from API'
is_read_only = True
notify_list = ['dean.moreton@gmail.com']
template_variables = [{
    'name': 'ubuntu_dd',
    'prefix': 'host',
    'default': 'ubuntu_dd'
}]
api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables)
```


Dashboard of last 5 mins w/ notation:
![Dasbhoard](https://i.imgur.com/uVqNIaA.png[/img)

### Bonus Question: What is the Anomaly graph displaying?
In short, detecting activity that has deviated from normal behaviour within the metric.  This can be useful for when wanting to be alerted that something is not behaving how it typically does in a certain timeframe, as opposed to a static threshold.


## Monitoring Data:
Metric monitor:
![Metric Monitor](https://i.imgur.com/A2L0KiW.png)

Metric notification email:
![Metric notification](https://i.imgur.com/eksJpMl.png)

### Bonus question:
Weekday scheduled downtime:  
![Weekday downtime](https://i.imgur.com/Tt19Wb1.png)

Weekday scheduled downtime notification:  
![Weekday notification](https://i.imgur.com/4F1Utgx.png)

Weekend scheduled downtime:  
![Weekend downtime](https://i.imgur.com/0bmqe4k.png)

Weekend scheduled downtime notification:  
![Weekend notification](https://i.imgur.com/l2gHWAe.png)


## Collecting APM Data:
I used the below provided Flask app which was auto-instrumented by using ddtruce-run python flaskapp.py

```
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

Dashboard with APM and Infrastructure metrics:

![Weekend notification](https://i.imgur.com/fthubul.png)

Not sure if this was a trick question, but regarding sharing a link to the dashboard, I noticed that only screenboards are publicly shareable so created one here:
https://p.datadoghq.com/sb/tsafe0h9vu9fy68w-42cddf7df201e437a0f7f9932c04d530

### Bonus Question
Per Datadog's documentation, a service is a set of processes that do the same job - for example a web framework or database, whereas a resource is a particular action for a given service (typically an individual endpoint or query). 

## Final Question:
There are a lot of great use cases for Datadog in a commercial/enterprise sense, but it's often the home projects that can get the creativity flowing.  For me personally, I have a Superannuantion fund that has terrible reporting functionality.  

I am currently using a community version of the RPA tool UIPath to regularly log in and extract out investment balances. Rather than looking at these in excel, I think I could get some very interesting dashboards in Datadog, either by leveraging the Datadog API within the UIPath recording or alternatively using log file ingestion.

Thanks for reading!  I enjoyed it and learnt a lot going through these exercises, regardless of the outcome of this process.
