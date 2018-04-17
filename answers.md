# Welcome to Datadog!
We’re very happy to hear you are considering our product for your monitoring and alerting needs.  To make your evaluation easier, I’ve created a quick guide that will walk you through integrating Datadog with your current infrastructure and applications while also highlighting some of our product’s features.  Here is an overview of what this guide will cover which is broken out into sections:
1. **Collecting Metrics**
    1. Installing the Datadog Agent on Ubuntu Servers
    2. Integrating Datadog with MongoDB
    3. Submitting Custom Metrics with an Agent Check
2. **Visualizing Data**
    1. Creating a Dashboard
    2. Creating a Dashboard with the Datadog API
    3. Snapshots and Annotations
3. **Monitoring Data**
    1. Creating a Monitor
    2. Scheduling Monitor Downtimes
4. **Collecting APM Data**
5. **Conclusion**

If you have any issues or questions during your evaluation, or if you would like help with something not covered in this guide feel free to reach out to me directly at cmcmaho25@gmail.com.


## 1. Collecting Metrics

### 1.1 Installing the Datadog Agent on Ubuntu
Installing the Datadog agent on your servers is easy using our one-step installation.  On each Ubuntu system, run the following command to install the agent and begin sending metrics back to Datadog.  Be sure to include your specific API key which can be found at https://app.datadoghq.com/account/settings#api.
```
DD_API_KEY={Your-API-Key} bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
You can verify the agent is now running with the command ```datadog-agent status```.  You can find other useful commands for the datadog agent here: https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/

Now that your agent is up and running let’s add some tags.  Tags allow you to create sub groups of hosts and integrations which can later be used for monitoring and alerting.  For example you might want to use tags to identify a host’s environment, region, role, type, etc.  To add tags to your Ubuntu systems, locate the datadog.yaml configuration file under /etc/datadog-agent/datadog.yaml.  Open this file and add in the following line, replacing the key value pairs with your desired tags.
```
tags: key1:value1, key2:value2, key3:value3
```
***Example:***
```
tags: name:ubuntu_box_1, env:dev, region:1, type:ubuntu_server
```
Once this has been added and saved you will see your tags are now viewable in the host map page when you click on one of your hosts:

<img src="https://i.imgur.com/3GNew1X.png">

### 1.2 Integrating Datadog with MongoDB
At Datadog we’ve created integrations for the majority of the industry’s leading platforms.  Because your database of choice is MongoDB we’ll start there to introduce you to integrations.  Each integration comes with an installation guide, which can be found under the integrations tab.  Here is the MongodB guide: https://app.datadoghq.com/account/settings#integrations/mongodb

From your Mongo 3.0 server you’ll first need to create a new user for Datadog to use to pull information.  To do this, use the previous link to generate a unique password.  Copy the first block of code and insert your admin authorization credentials before running the command in mongo.  For example:
```
use admin
db.auth("admin", "testing")
db.createUser({"user":"datadog", "pwd": "3FPOoAthqSopinJOgvtXRS7r", "roles" : [ {role: 'read', db: 'admin' }, {role: 'clusterMonitor', db: 'admin'}, {role: 'read', db: 'local' }]})
```
Now that the user is created you need to set up the config file that the Datadog agent will use for mongo.  This file has been created under /datadog-agent/conf.d/mongo.yaml.  Open this file and add the following using the same previously generated password.  This is also where you can add tags to for your various MongoDB instances.
```
init_config:

instances:
      -   server: mongodb://datadog:3FPOoAthqSopinJOgvtXRS7r@localhost:27016
          tags:
              - mytag1
              - mytag2
      -   server: mongodb://datadog:3FPOoAthqSopinJOgvtXRS7r@localhost:27017
          tags:
              - mytag1
              - mytag2
```
Now all you need to do is restart the agent by running ```sudo service datadog-agent restart```.  And that’s it!  You’re now receiving metrics from your MongoDB instances which you can confirm through the prebuilt MongoDB dashboard that has been added to your dashboards list at https://app.datadoghq.com/screen/integration/13/mongodb.

### 1.3 Submitting Custom Metrics with an Agent Check
You’ve seen that Datadog can pull in metrics from hosts and platforms through the agent and integrations, but what if you want to submit a metric from a custom application or unique system?  This is where custom Agent Checks come in.  With an Agent Check you are able to send custom metrics to the agent which will be reported every time the agent passes metrics to Datadog.

Let’s look at adding a custom check with a simple Python application.  First, you’ll want to create your check Python script under etc/datadog-agent/checks.d/mycheck.py.  You’ll also need to create a matching config file under etc/datadog-agent/config.d/mycheck.yaml.  Here is an example check.py and check.yaml that will submit a random number between 0 and 1000 as ‘my_metric’.  
**metric_check.py**
```
metric_check.py
from checks import AgentCheck
from random import *
class MetricCheck(AgentCheck):
     def check(self, instance):
       x = randint(0,1000)
       self.gauge('my_metric', x)
```
**metric_check.yaml**
```
metric_check.yaml
init_config:
    min_collection_interval: 45

instances:
    [{}]
```
The check is inherited from AgentCheck and by default runs once every time the agent checks in to Datadog.  For this example, it has been modified to only report in once every 45 seconds by setting ```min_collection_interval:45``` in the config file.
Once you’ve created both the .py and .yaml files your check will get kicked off by the agent automatically and will continue to send data for 'my_metric' which can be leveraged in dashboards and monitors.


## 2. Visualizing Data
You’re now receiving metrics from your Ubuntu hosts, MongoDB instances, and the custom Agent Check.  It’s time to create a custom dashboard to visualize all of this data!  This can be done through the Datadog website or via the Datadog API.  For now, let’s focus on creating a new timeboard through the website.

### 2.1 Creating a Dashboard
First, navigate to Dashboards->New Dashboard and select TimeBoard.  From this editing page you can edit the TimeBoard’s title, time range, and widgets.  Try adding some widgets by dragging them into the dashboard and configuring them to pull from the new metrics you have added.  Here are some example widgets:
* Bar graph of my_metric from the host running our custom check: 
  <img src="https://i.imgur.com/Gs4UzvT.png">
* Line graph of MongoDB inserts with anomalies highlighted.  The anomaly function highlights any data points outside of the expected bounds. These bounds are relative to the actual data observed and can be manipulated with the defined multiplier (in this case 2).
  <img src="https://i.imgur.com/1n2n0kv.png">
* Sum of my_metric from the past hour.  The rollup function allows you to combine data over a defined period (in seconds), so for an hour you’d use a period of 3600. 
  <img src="https://i.imgur.com/TxpiEmJ.png">

### 2.2 Creating a Dashboard with the Datadog API
Now that you have a grasp on creating dashboards through the Datadog website, let’s accomplish the same thing by calling the Datadog API through a Python script.  For reference you can use the documentation at https://docs.datadoghq.com/api/?lang=python#overview.
The first thing you’ll need to do is go to https://app.datadoghq.com/account/settings#api and create a new APP key for this python script.  You’ll also want to pull your API key from the same page as both will be used for authorization.  Next, create a new Python application named makeTimeboard.py and add the following using your specific API and APP keys:
```
#makeTimeboard.py
from datadog import initialize, api

api_key = '6a44adbdf2d661542100723e1b79b58a'
app_key = '5cd019b15629768501a9d58146fe26e3bdea72d7'
options = {
    'api_key': api_key,
    'app_key': app_key
}

initialize(**options)

title = "My API Generated Timeboard"
description = "A super awesome timeboard!"
graphs = [{
    "definition": {
        "events": [],
        "requests": [{}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)
```
In its current state this script will create an empty TimeBoard named ‘My API Generated Timeboard’, but you'll want to add in the graphs previously created vie the web app.  To add these, all you’ll need to do is go to the graph’s editing page and select the JSON tab.  This will give you the graph’s definition which can be inserted into the graphs.definition.requests block in the Python script.  For example here is the definition for the previously shown anomaly graph:
```
{
  "viz": "timeseries",
  "status": "done",
  "requests": [
    {
      "q": "anomalies(avg:mongodb.metrics.document.insertedps{server:mongodb://datadog:_localhost:27017}, 'basic', 2)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "autoscale": true
}
```
Once you have added your graph definitions (make sure to separate definitions with commas)  your makeTimeboard.py script should look something like this:
```
#makeTimeboard.py
from datadog import initialize, api

api_key = '6a44adbdf2d661542100723e1b79b58a'
app_key = '5cd019b15629768501a9d58146fe26e3bdea72d7'
options = {
    'api_key': api_key,
    'app_key': app_key
}

initialize(**options)

title = "My API Created Timeboard"
description = "A super awesome timeboard!"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {
        "q": "avg:my_metric{host:precise64}",
        "type": "bars",
        "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
        },
        "conditional_formats": [],
        "aggregator": "avg"
      }
        ],
        "viz": "timeseries",
    "status": "done"
    },
    "title": "Value of my_metric from host:precise64"
},
{
    "definition": {
        "events": [],
        "requests": [
            {
        "q": "anomalies(avg:mongodb.metrics.document.insertedps{server:mongodb://datadog:_localhost:27017}, 'basic', 2)",
        "type": "line",
        "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
        },
        "conditional_formats": [],
        "aggregator": "avg"
      }
        ],
        "viz": "timeseries",
    "status": "done"
    },
    "title": "MongoDB inserts with anomalies highlighted"
},
{
    "definition": {
        "events": [],
        "requests": [
            {
        "q": "avg:my_metric{*}.rollup(sum, 3600)",
        "type": "line",
        "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
        },
        "conditional_formats": [],
        "aggregator": "last"
      }
        ],
        "viz": "query_value",
    "precision": "0"
    },
    "title": "Sum of my_metric from the past hour"
}]


read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)
```
Now, just run the script to kick off the API and your new TimeBoard will appear in your dashboards list.  Here is the resulting dashboard from the above script which includes the three graphs shown in the web app section.
<img src="https://i.imgur.com/Z21ZJEa.png">
https://app.datadoghq.com/dash/755892/my-api-created-timeboard?live=false&page=0&is_auto=false&from_ts=1522713358275&to_ts=1522716958275&tile_size=m

### 2.3 Snapshots and Annotations
Before moving to the next section, take a snapshot of one of your new graphs and send it out to a team member with a comment attached.  In Datadog, this is as easy as hovering over the desired graph and clicking the camera icon that appears in the top right of the graph.  From here you can annotate the snapshot and add emails for the team members you’d like to notify.

<img src="https://i.imgur.com/Gjx0UNB.png">
Here is an example email received for a 5 minute window on the anomaly graph:

<img src="https://i.imgur.com/otu73pK.png">


## 3. Monitoring Data
### 3.1 Creating a Monitor
When problems arise in your infrastructure you want to be quickly notified so you can troubleshoot the issue.  Luckily, with Datadog you can be proactive and create monitors to alert you the second issues arise.  To create a new monitor, navigate to the monitor manager at https://app.datadoghq.com/monitors/manage and select to add a new monitor.  You’ll see there are several different types of monitors to choose from.  For now, create a new Metric Monitor to alert you when the new metric ‘my_metric’ exceeds a set threshold.  Set up this monitor as a threshold alert on my_metric which triggers an alert when the 5 minute average is above 800.  Also add warnings for when the average is above 500 and when the monitor is missing data.  Here’s what the setup should look like:
<img src="https://i.imgur.com/vSCwGgj.png">

You’ll also want this alert to send an email out when it is triggered, so you’ll need to create a message for the alert.  You can customize the message based on the trigger type using the tags ```{{#is_alert}}```, ```{{is_warning}}```, and ```{{is_no_data}}```.  You can also add the value that triggered the monitor using ```{{value}}```.  Example message for the monitor:
```
#{{#is_alert}} **ALERT** 
my_metric averaged {{value}} for the past 5 minutes which exceeds the alert threshold of 800.{{/is_alert}}
{{#is_warning}} **Warning** 
my_metric averaged {{value}} for the past 5 minutes which exceeds the warning threshold of 500.{{/is_warning}}
{{#is_no_data}} **No Data** 
No data has been received for my_metric in the last 10 minutes.{{/is_no_data}}
```
Once you have your message created make sure to add emails to be notified when the monitor is triggered.  You’ll notice these emails appear in the message body when added.  Once you’re happy with your monitor, hit save and you will begin receiving notifications when the monitor is triggered.  Here’s are some sample emails received from this monitor:
* Warning: 
  <img src="https://i.imgur.com/D9W0irq.png">
* No Data Alert: 
  <img src="https://i.imgur.com/czax96V.png">
  
Monitor link: https://app.datadoghq.com/monitors#4549553?group=all&live=4h

### 3.2 Scheduling Monitor Downtimes
Because you don’t want the new monitor sending alerts when you are out of office, let’s set up some scheduled downtimes to mute the monitor outside of business hours.  You can create a new downtime under Monitors -> Manage Downtime -> Schedule Downtime.  The new monitor should be muted during the weekend and from 7PM to 9AM on weekdays.  To accomplish this, set up two scheduled downtimes as follows:
* Weekend Downtime: 
  <img src="https://i.imgur.com/GsJu5Ne.png">
* Weekday Downtime: 
  <img src="https://i.imgur.com/pkpIbhQ.png">

Schedule Downtime Link: https://app.datadoghq.com/monitors#downtime?id=309567430

Now that the downtimes are configured, you’ll begin receiving emails like the following when the monitor enters a scheduled downtime.
<img src="https://i.imgur.com/aNrk6Iy.png">


## 4. Collecting APM Data

Up to this point the focus has been on collecting and monitoring metrics from your infrastructure, but not on collecting information from your applications.  With APM (Application Performance Monitoring) Datadog enables you to collect metrics and add tracing to your applications.  With tracing you can monitor your various services (Python/Flask apps, MongoDB instances, etc.) as well as the resources called by those services (functions, queries, reads/writes, etc.).  You mentioned you use Python and Flask to power your web apps, so let’s take a look at setting up APM for those.
The first thing you’ll need to do is install Datadog’s python tracing client **ddtrace**.  You can install this quickly with pip using ```pip install ddtrace```.  With ddtrace you can easily add tracing to your Python applications without making code changes by running them through the ddtrace client like so:
```ddtrace-run python my_app.py```
	For Flask, you’ll need to add a few lines of code in your Flask applications and you’ll also need to download the Blinker python library.  This can be done with ```pip install blinker```.
Let’s take the following simple Flask application and add tracing to it:
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
    app.run()
```
To begin you’ll need to import the blinker library as well as the necessary middleware from ddtrace.  Here are the lines you need to add for these imports:
```
import blinker as _

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware
```
Next, add the following line after your app definition and change the service name to reflect your application:
```
traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)
```
Here’s the sample Flask app which has been configured for tracing:
```
from flask import Flask
import logging
import sys
import blinker as _

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

traced_app = TraceMiddleware(app, tracer, service="flask-apm-intro-app", distributed_tracing=False)

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
Now run the flask app ```using ddtrace-run python flaskApp.py``` and your application will start reporting APM data back to Datadog.  To hit the Flask application’s endpoints locally you can use the following curls:
* ```curl 127.0.0.1:5000/```
* ```curl 127.0.0.1:5000/api/apm```
* ```curl 127.0.0.1:5000/api/trace```

You’ll find your trace data available in the APM section and as metrics for dashboards under the datadog.tracer fields.  If you’d like to explore setting up APM for other web frameworks and entrypoints, reference our full documentation on the Datadog Python trace client: http://pypi.datadoghq.com/trace/docs/#

You’re now set up to create rich, insightful dashboards to monitor both your applications and infrastructure.  Here’s a sample dashboard which pulls together metrics from each component configured in this guide (Ubuntu systems, MongoDB instances, and a Flask application):
<img src="https://i.imgur.com/IRkcXrC.png">

## 5. Conclusion
I hope that by completing this guide you are feeling much more comfortable with the Datadog product.  We’ve only just scratched the surface of Datadog’s offerings, so please continue to explore the vast amount of integrations available and reach out if you have any questions or issues.  I look forward to speaking with you soon.


## Final Question: Is there anything creative you would use Datadog for?
As a passionate NHL fan, I would love to integrate professional sports data into Datadog to create unique visuals and power advanced analytics.  You could build out dashboards to view team and individual performance, use algorithms to predict future performance, and even create monitors to warn fantasy fanatics when their players are injured or underperforming.
