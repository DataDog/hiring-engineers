Collecting Metrics:
Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
![alt text](https://raw.githubusercontent.com/maximumsb/hiring-engineers/master/Host%20Tags.PNG)
Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
![alt text](https://raw.githubusercontent.com/maximumsb/hiring-engineers/master/MySQLInstall.PNG)
Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
try:

    from datadog_checks.base import AgentCheck
except ImportError:

    from checks import AgentCheck


__version__ = "1.0.0"

class MyMetricCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my.metric', 25, tags=['metric:check'])


root@ubuntu18:/etc/datadog-agent/conf.d/my_metric.d# cat my_metric.yaml

init_config:

instances:
        - min_collection_interval: 45

![alt text](https://raw.githubusercontent.com/maximumsb/hiring-engineers/master/my_metric_Check.PNG)
Change your check's collection interval so that it only submits the metric once every 45 seconds.
![alt text](https://raw.githubusercontent.com/maximumsb/hiring-engineers/master/my_metric_change_interval.PNG)
Bonus Question Can you change the collection interval without modifying the Python check file you created?
This can be done from the UI in screenshot above

Visualizing Data:
Utilize the Datadog API to create a Timeboard that contains:

Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

from datadog import initialize, api

options = {
    'api_key': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'app_key': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'api_host': 'https://api.datadoghq.com'
}

initialize(**options)

title = "Ben Timeboard"
description = "DDtest timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "sum:my.metric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "my,metric"
}]

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

Once this is created, access the Dashboard from your Dashboard List in the UI:

Set the Timeboard's timeframe to the past 5 minutes
Take a snapshot of this graph and use the @ notation to send it to yourself.
Bonus Question: What is the Anomaly graph displaying?
![alt text](https://raw.githubusercontent.com/maximumsb/hiring-engineers/master/timeboard.PNG)
![alt text](https://raw.githubusercontent.com/maximumsb/hiring-engineers/master/snapshotgraph.PNG)
![alt text](https://raw.githubusercontent.com/maximumsb/hiring-engineers/master/snapshot%20email.PNG)

Monitoring Data
Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

Warning threshold of 500
Alerting threshold of 800
And also ensure that it will notify you if there is No Data for this query over the past 10m.
![alt text](https://raw.githubusercontent.com/maximumsb/hiring-engineers/master/metricmonitor.PNG)

Please configure the monitor’s message so that it will:

Send you an email whenever the monitor triggers.

Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

When this monitor sends you an email notification, take a screenshot of the email that it sends you.
![alt text](https://raw.githubusercontent.com/maximumsb/hiring-engineers/master/monitormessage.PNG)
![alt text](https://raw.githubusercontent.com/maximumsb/hiring-engineers/master/mymetric%20alert.PNG)

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.
Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
![alt text](https://raw.githubusercontent.com/maximumsb/hiring-engineers/master/downtimenightly.PNG)
![alt text](https://raw.githubusercontent.com/maximumsb/hiring-engineers/master/downtimeweekend.PNG)
![alt text](https://raw.githubusercontent.com/maximumsb/hiring-engineers/master/downtimeemail.PNG)

Collecting APM Data:
Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution
Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
![alt text](https://raw.githubusercontent.com/maximumsb/hiring-engineers/master/dashboard%20APMandInfra.PNG)
![alt text](https://raw.githubusercontent.com/maximumsb/hiring-engineers/master/apmflask.PNG)

Final Question:
Is there anything creative you would use Datadog for?
Similar to the restroom availibility hack. Parking spot availibility in parking garages that have sensors, similar to Disney Springs in Orlando. The parking decks have a light over every space red for occupied and green for available. Instead of driving around looking for a green light (available space) we could monitor the stus of each spot red or green and create a dashboard showing available spaces in the garage, from here we could drive straight to the level and parking space available in the garage.  
