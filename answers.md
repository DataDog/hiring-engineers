# DataDog Hiring Challenge
To familiarise myself with the basic features of Datadog, I tried out the following using the free trial period.
    # Setting Up the Environment
    # Collecting Metrics
    # Integrating MySQL
    # Visualizing Data
    # Monitoring Data
    # Collecting APM Data


# Setting Up the Environment
Using Vagrant and VirtualBox, I created a virtual machine (Ubuntu Server 14.04 LTS) and installed Datadog Agent v5.20.0 on it.
The installation instructions for Datadog Agent can be found [here](https://app.datadoghq.com/account/settings#agent/ubuntu). 

I used the pain-free one-step install and my host appeared on the Infrastructure page moments after installation.
[link]https://app.datadoghq.com/infrastructure/map?


# Collecting Metrics

## Adding Host Tags
I added tags to my host so I could easily filter through and piece together information about my infrastructure in meaningful ways later on.

These can be done by editing the config file at '/etc/dd-agent/datadog.conf'.
I added the following tags as I predicted the need to group servers by this information when I have to manage the settings for data monitoring afterwards.
tags: #env:test, #location:tokyo

The tags turned up on the Host Map after I restarted the agent with the '/etc/init.d/datadog-agent restart' command to enable the changes.
[img](/screenshots/01_hostmap_tags.png)

## Integrating MySQL
For systems included in the built-in integrations, you can easily configure Datadog to collect metrics and events from them. For systems not yet available, check out the next step. I followed the instructions [here](https://docs.datadoghq.com/integrations/mysql/) to integrate MySQL but instructions are also available on the Integrations page.

Once configured, I was able to access my MySQL dashboard via the Host Map for an overview of the system.
[img](/screenshots/02_mysql_dashboard.png)

## Creating a Custom Agent Check
For custom applications or unique systems, you can create an agent check in place of integrations. 

You will need to add two files with the exact same name to the following locations for your check.
1. A check file to '/etc/dd-agent/checks.d/'
2. A config file to '/etc/dd-agent/conf.d/'

[The Check File]
I created a sample python script that submits a random value between 0 and 1000 as a metric and named it 'my_metric'.

```python
import random
from checks import AgentCheck

class randomValueCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randrange(0,1001))
```

[The Config File]
I created a simple config file of the same name as my python script and set the agent check frequency to 45 seconds using the min_collection_interval parameter.
If you leave this out of the file, the frequency of the agent checks defaults to 15 seconds (recommended).

```yaml
init_config:
    min_collection_interval: 45

instances:
    [{}]
```

After restarting the Agent, I could see my custom check in the Summary of the Metrics page.
[img](/screenshots/03_my_metric.png)


# Visualizing Data

## Creating a Timeboard Using the Datadog API
A timeboard can be created from either the web console or by using the Datadog API. You will need an API and APP key, which can be found in API Keys on the Integrations page.

With the Python script below, I created a Timeboard containing
- my custom metric scoped over my host.
- MySQL query rate with the anomaly function applied over all available hosts.
- my custom metric with the rollup function applied to sum up all the points for the past hour into one bucket over all available hosts.

(I had to import requests as I was running Python 2.7.3 and faced SNIMissing and InsecurePlatform warnings. Newer versions of Python should not require this.)

```python
from datadog import initialize, api
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

options = {
    'api_key': 'YOUR_API_KEY',
    'app_key': 'YOUR_APP_KEY'
}

initialize(**options)

title = "Random Value & MySQL Timeboard"
description = "A timeboard for my_metric and MYSQL query rate"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:testddagent}", "type": "line"},
            {"q": "anomalies(avg:mysql.performance.queries{*}, 'basic', 2)", "type": "line"},
            {"q": "avg:my_metric{*}.rollup(sum, 3600)", "type": "line"}
        ],
    "viz": "timeseries"
    },
    "title": "Random Value and MySQL Query Rate"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = False

api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)
```

Immediately after running the script, my timeboard appeared under Your Custom Dashboards of the Dashboard page. Check it out!
[img](/screenshots/04_api_timeboard.png)

I customized the Timeboard's timeframe by clicking and dragging the cursor over my desired timeframe (5min).
You can see a red band around the 13:38 mark. This is an anomaly flag raised by Datadog based on analysis of a metric's historical behavour of what is normal and what is not.

To take a snapshot, simply click the camera icon on the top right corner of the graph. I used the @notation to send the snapshot to myself just to see what would happen. Nothing happened. It took me some clicking around before I found the snapshot in the Events page (I wish there'd been a notification...).
[img](/screenshots/05_graph_snapshot.png)


# Monitoring Data

## Creating a Metric Monitor
You can create monitors that will watch your metrics and alert you when they go above the threshold values you've set.

I created one which will alert me when
- the average of my custom metric (my_metric) goes above the warning threshold of 500
- the average of my custom metric (my_metric) goes above the alerting threshold of 800
- there has been no data over the past 10 min.
[img](/screenshots/06_monitor.png)
[img](/screenshots/07_alert_mail.png)

## Scheduling Downtime
You can also schedule downtime to mute any alerts for when you're out of the office. Here, I have scheduled downtimes for 7pm to 9am daily on M-F and all day on Sat-Sun.
[img](/screenshots/08_downtime_1.png)
[img](/screenshots/09_downtime_2.png)
[img](/screenshots/10_downtime_mail.png)


# Collecting APM Data
The Datadog Agent also provides application performance monitoring (tracing). To instrument this I ran the following Flask app with the `ddtrace-run python my_app.py` command. In a separate terminal window, I ran a script accessing the different urls in the app to simulate access.

```Python
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
    app.run()
```

It took a couple of minutes, but my traces started showing up on the APM page in a table with the columns "Type", "Service", and "Resource".

The "Type" refers the nature of the application/framework the Datadog Agent is integrating with.
In this Flask integration example, the "Type" is being set to "Web".  For custom applications, this shows up as "Custom". 

A "Service" refers to a set of processes that come together to provide a feature set, aka the services provided by the application.

A "Resource" is a particular query to a service (think SQL query).

These traces, or APM data, when combined with your infrastructure metrics can give you powerful insights into performance and load.
I can see this coming in handy especially when I need to monitor/reallocate resources for servers running multiple applications.
[link]https://app.datadoghq.com/dash/408062/apm-and-infrastructure-metrics
[img](/screenshots/11_apm_infrastructure_dashboard.png)


Final Thoughts
The Datadog Agent trial was definitely a roller coaster ride. There was what I felt was a steep learning curve at the start which paid itself off when I discovered the sheer amount of things I could do with what little I had time to experiment with.

In other news, there are zero restaurants within a 10 min walk of my office and most people buy their lunches on their way to work. But every Wednesday, a man comes by in a van selling curry rice and it's the best lunch ever! Except sometimes he drops in a line on Facebook the night before announcing his no-show and people come back from his usual spot during lunch the next day with the saddest faces when they realise he's not there. We definitely need alerts for days like this...