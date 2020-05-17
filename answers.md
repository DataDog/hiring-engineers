Dashboard link: https://app.datadoghq.com/dashboard/lists
Datadog agent installed to host running on Vagrant VM
MySQL DB installed to same host

Collecting Metrics:
Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
- The following tags were added to the /etc/datadog-agent/datadog.yaml file 
tags:
        - testtag1:test1
        - testtag2:test2
        - testtag3:test3

The uploaded screenshot (Datadog_Dashboard.PNG) shows these tags on the Host Map page of Datadog.

Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
- MySQL database is installed on the same host as where the Datadog Agent is installed
- Datadog integration with the MySQL was done by following the documentation: https://docs.datadoghq.com/integrations/mysql/

Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
- my_metric.py was created at /etc/datadog-agent/checks.d with following content:
try:
    from datadog_checks.base import AgentCheck
except ImportError:
    from checks import AgentCheck

__version__ = "1.0.0"

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric.gauge', random.randint(0, 1000))

- my_metric.yaml was created at /etc/datadog-agent/conf.d with following content:
instances: [{}]

Change your check's collection interval so that it only submits the metric once every 45 seconds.
- The my_metric.yaml was updated so the collection interval would be 45 seconds:
init_config:
instances:
        - min_collection_interval: 45
        
Utilize the Datadog API to create a Timeboard that contains:

Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Script used below (createtimeboard.py), executed from:
/opt/datadog-agent/embedded/bin$ python3 createtimeboard.py

from datadog import initialize, api

options = {
    'api_key': '77be3ef7547da187cd332cfc691bb304',
    'app_key': '3637663eeefed92bca57ad351d4da62b358f3162'
}

initialize(**options)

title = "MT1"
description = "Marc Test Timeboard2"
graphs = [
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:system.mem.free{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:system.mem.free{*} by {host}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "My Metric Rollup"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(mysql.innodb.buffer_pool_total{*}, 'basic' ,3)"}
        ],
        "viz": "timeseries"
    },
    "title": "MySQL Buffer Pool Total Anomaly"
}
]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
                     
Set the Timeboard's timeframe to the past 5 minutes
Take a snapshot of this graph and use the @ notation to send it to yourself.
- Screenshot attached of timeboard dashboard set to past 5 minutes (timeboard5min.png)

Bonus Question: What is the Anomaly graph displaying?
- Anomaly detection checks to see when a metric is behaving differently than it has in the past through consideration of trends, seasonal day-of-week, and time-of-day patterns.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
Warning threshold of 500
Alerting threshold of 800
And also ensure that it will notify you if there is No Data for this query over the past 10m.
Please configure the monitor’s message so that it will:
Send you an email whenever the monitor triggers.
Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
When this monitor sends you an email notification, take a screenshot of the email that it sends you.
- Please find screenshot uploaded (metricmonitor.png)

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.
Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
- Please find screenshot uploaded (scheduleddowntime.png)

Collecting APM Data:
Bonus Question: What is the difference between a Service and a Resource?
- Resource: a particular action for a given service (typically an individual endpoints or query)
- Service: building blocks of modern microservice architecutres-- a service groups together endpoints, queries, or jobs for the purposes of scaling instances

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
- Please find screenshot uploaded (apmdashboard.png)

Final Question:
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?
- I worked in corporate real estate for many years so the initial thought would to use Datadog for space utilization.  Sensors that detect seat occupancy could be placed at every seat in a building.  These sensors would update a central server that has a Datadog agent installed.  The agent would use a custom agent check to query the occupancy data stored on the server that gets stored to custom metrics.  Monitors would then be set up to alert when capacity thresholds are met for proper capacity planning. Additionally, dashboard graphics could be use to analyze trends, anomalies, and much more.
