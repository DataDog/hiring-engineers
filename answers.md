Your answers to the questions go here.
## Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
# Collecting Metrics

`vagrant@ubuntu-xenial:/etc/datadog-agent$ sudo vi datadog.yaml`
Set the host tags to the following: 

```
tags:
   - vagrant_box
   - env:dev
   - aliciatest
   - role:server
```
![Tags Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/host_tags_screenshot.png)

For the tags to take effect, agent is restarted: 
`sudo service datadog-agent restart`


## Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
## Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

`my_metric.py`
```
import random
from checks import AgentCheck

class my_metric(AgentCheck):
    def check(self, instance):
        myrand = random.randint(1, 1000)
        #force NoData for testing
        #myrand = None
        self.gauge('my_metric', myrand)
```


## Change your check's collection interval so that it only submits the metric once every 45 seconds.
## Bonus Question Can you change the collection interval without modifying the Python check file you created?


# Visualizing Data

1. Create an app key
![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/timeboard_createappkey.png)
2. Install datadog python library
`pip install datadog`

3. Write a Python script to create the timeboard using the datadog API: 

```
title = "Alicia Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:ubuntu-xenial}"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric status"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mongodb.network.numrequestsps{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Anomalies in MongoDB Number of requests per second"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:ubuntu-xenial}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric sum of all points for the past hour"
}
]
```

Set the Timeboard's timeframe to the past 5 minutes
![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/timeboard_createappkey.png)

Take a snapshot of this graph and use the @ notation to send it to yourself.

Bonus Question: What is the Anomaly graph displaying?
The anomaly graph shows a distinction between normal and abnormal trends in a series of data points. In this graph we can see that historically there has not been much acitvity in MongoDB requests, however there is an abnormal spike at 1.46 requests per second around the 15:25:36 timestamp.


# Monitoring

## Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes.

Email showing monitor alert triggered when value breached 500: 
![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/monitor_alert_email.png)

Email showing monitor alert triggered when value breached 800: 
![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/monitor_warning_email.png)

Email showing monitor alert triggered when value had No Data: 
![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/monitor_nodata_email.png)


## Bonus Question - Setup scheduled downtimes

Silence from 7pm to 9am daily on M-F:

![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/monitor_downtime_start.png)

And one that silences it all day on Sat-Sun:

![Screenshot](https://github.com/agallav/hiring-engineers/blob/draft/screenshots/monitor_downtime_weekends.png)


# Collecting APM Data