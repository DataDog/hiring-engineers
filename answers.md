Your answers to the questions go here.

This file needs to be read along with the folder Screens containing screenshots of the Datadog web application.

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog. 

The Agent config file is located in ```/etc/dd-agent/datadog.conf```
The following line needs to be add at the end of ```datadog.conf``` file.
```yaml
tags: personal_tag_by_marcquero, env:prod, role:database
```
![Datadog Host installation ](/Screens/Answer1.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
Validation of the PostgreSQL installation :
![Datadog PostgreSQL integration](/Screens/Answer2.png) 
![Datadog PostgreSQL integration_2](/Screens/Answer3.png)
 
* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
To create a custom Agent check, two files have been created. Both have the same name but two different extension py (application code) and yaml (configuration of the application) : 
-A Python file: ```personal_check.py```, containing the code that will run the application, located in ```/etc/dd-agent/checks.d/```
-A Yaml file: ```personal_check.yaml```, containing the configuration of the application, located in ```/etc/dd-agent/conf.d/```

Here is the code for ```personal_check.py```: 
```python
from random import randint
from checks import AgentCheck

class PersonalCheck(AgentCheck):
	def check(self, instance):
		self.gauge('my_metric', randint(0,1000))
```
Here is the code for ```personal_check.yaml```:
```yaml
init_config:

instances:
    [{}]
```

* Change your check's collection interval so that it only submits the metric once every 45 seconds.
Here is the code for personal_check.py, submitting metrics every 45 seconds: 
```python
from random import randint
from checks import AgentCheck

class PersonalCheck(AgentCheck):
	def check(self, instance):
		self.init_config['min_collection_interval'] = 45 #Set the check's collection interval to 45 seconds
		self.gauge('my_metric', randint(0,1000))
```
* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?
It is possible by adding the field 'min_collection_interval' to personal_check.yaml file.
Here is the code :
```yaml
init_config:
    min_collection_interval: 45
instances:
    [{}]
```
## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Here is the code which create a Timeboard using Datadog API:
```python
from datadog import initialize, api

options = {
    'api_key': '586e6a2a113d9c586e4b72fcb6f738d6',
    'app_key': 'c5ce4f35eb2ff20b4b73eea2db0c62c01615164f'
}

initialize(**options)

title = "My Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
          {
      	    "q": "avg:my_metric{*} by {host}",
      	    "type": "area",
            "style": {
              "palette": "dog_classic",
              "type": "solid",
              "width": "normal"
      	    },
      	    "conditional_formats": [],
            "aggregator": "avg"
    	 },
    	 {
      	   "q": "avg:datadog.agent.emitter.emit.time{*}",
           "type": "line",
           "style": {
             "palette": "dog_classic",
             "type": "solid",
             "width": "normal"
           }
         },
         {
           "q": "hour_before(sum:my_metric{*} by {host}.rollup(sum))",
           "type": "area",
           "style": {
             "palette": "dog_classic",
             "type": "solid",
             "width": "normal"
           }
         }
        ],
    "viz": "timeseries"
    },
    "title": "Handcrafted Metrics timeboard"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True

api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)
```
![Timeboard manually created](/Screens/Answer4.png)

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
![Timeframe_To_5_Miutes](/Screens/Answer5.png)
* Take a snapshot of this graph and use the @ notation to send it to yourself.
![Use of @ notation](/Screens/Answer6.png)
* **Bonus Question**: What is the Anomaly graph displaying?
Anamoly graph is based on an algorithm that used usual data. When the data seem to be odd compared the usual value, a alert is raised. It has to be used for metrics that can not be monitored with threshold.

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.
![Warning, Alert threshold](/Screens/Answer7.png)

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
![Mail send by alert monitor](/Screens/Answer8.png)

* When this monitor sends you an email notification, take a screenshot of the email that it sends you.
![Mail_send_part1](/Screens/Answer9.png) 
![Mail_send_part2](/Screens/Answer10.png)

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

    * One that silences it from 7pm to 9am daily on M-F,
![Downtime1](/Screens/Answer11.png)

    * And one that silences it all day on Sat-Sun.
![Downtime2](/Screens/Answer12.png)
 
    * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
![Downtime3](/Screens/Answer13.png)


## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

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

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other. 
    
* **Bonus Question**: What is the difference between a Service and a Resource?
* A service : A service reprensents a set of processes which performing the same tasks.
* A ressource : A ressource is a particular query belonging to a service.

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
![APM and Infrasture Metrics](/Screens/Answer14.png)

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

Datadog has been created to monitor IT Infrastructures. Datadog has the potential to diversify monitored field. There is an opportunity in top performance sport field.
Datadog can also be used to monitor data from connected objects in order to help athletes to monitor and imporve their performances. The dedicated metrics can be created with the help of specialists of this field.
