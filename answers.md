Your answers to the questions go here.

## How to install Datadog Agent: 


Datadog Agent is a software that will gather and provide information and metrics about a host machine.
Datadog Agent has to be installed on the machine that will be monitored.
Here, the monitored machine will run with **Linux Ubuntu 16.04.3**.

To install the Datadog Agent, the following command has to be run : 
```bash
DD_API_KEY=586e6a2a113d9c586e4b72fcb6f738d6 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"
```

Once the command has finished, the following command has to be run to know whether or not Datadog Agent is running : 
```bash
sudo /etc/init.d/datadog-agent status
```
The result should be displayed as follows : 
![DatadogAgentStatus](/Screens/DatadogAgentStatus.png)

The following command provides information about metrics, checks, paths:
```bash
sudo /etc/init.d/datadog-agent info -v
```
The result should be displayed as follows :
![DatadogStatusInfo1](/Screens/DatadogStatusInfo1.png)
![DatadogStatusInfo2](/Screens/DatadogStatusInfo2.png)

Once, Datadog Agent is running and delivering metrics. The next chapter will describe how to create a custom check and how to make it communicate with the Datadog Host.

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog. 

The Agent config file is located in ```/etc/dd-agent/datadog.conf```
The following line needs to be add at the end of ```datadog.conf``` file.
```yaml
tags: personal_tag_by_marcquero, env:prod, role:database
```
![Datadog Host installation ](/Screens/Answer1.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

For this installation, the database used will be **PostgreSQL**. 
In this documentation, it will be assumed that PostgreSQL has been installed and a database called datadog has been installed. Otherwise, please follow this [procedure](https://doc.ubuntu-fr.org/postgresql).
In order, to intergrate PostgreSQL to Datadog, please refer to the following [procedure](https://app.datadoghq.com/account/settings#integrations/postgres).

Validation of the PostgreSQL installation :
![Datadog PostgreSQL integration](/Screens/Answer2.png) 
![Datadog PostgreSQL integration_2](/Screens/Answer3.png)
 
* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Datadog Agent will scan two directories in order to summarize all custom checks : 
* ```/etc/dd-agent/checks.d/``` : containing the code that will run the application, only python files.
* ```/etc/dd-agent/conf.d/``` : containing the configuration of the application, only yaml files.

To create a custom Agent check, two files have been created : 
* A Python file: ```personal_check.py```, located in ```/etc/dd-agent/checks.d/```
* A Yaml file: ```personal_check.yaml```, located in ```/etc/dd-agent/conf.d/```

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

To check if personal_check has been installed and run correctly, the following command needs to be perform : 
```bash
sudo -u dd-agent dd-agent check personal_check
```
The result should be displayed as follows:
![Validate_check_metrics](/Screens/Validate_personal_check_metric.png)

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

For each custom check, there is a field called ```min_collection_interval```. This field defines the submitting interval for metrics. The value is defined in seconds. 
Here is the code for ```personal_check.py```, submitting metrics every 45 seconds: 
```python
from random import randint
from checks import AgentCheck

class PersonalCheck(AgentCheck):
	def check(self, instance):
		self.init_config['min_collection_interval'] = 45 #Set the check's collection interval to 45 seconds
		self.gauge('my_metric', randint(0,1000))
```
* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

It is possible by adding the line ```min_collection_interval: 45``` to ```personal_check.yaml``` file.

As follows:
```yaml
init_config:
    min_collection_interval: 45
instances:
    [{}]
```
A custom check and a custom metric have been set, the next step is to visualize them in real-time.

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Datadog interface provides some features to visualize data. These are called Dashboard. They can be found [here](https://app.datadoghq.com/dash/list).
There is two ways to create dashboard : 
* A graphical interface
* By using Datadog API

The following procedure will focus on the Datadog API's using.

First of all, to use Datadog API. It is necessary to understand HTTP methods (GET, POST, etc..). Here is [an introduction](http://www.geeksforgeeks.org/get-post-requests-using-python/) to that matter. 

To use Datadog API, it is important to use Datadog API key and Datadog App key.
They are located in the following page : [Datadog Settings API](https://app.datadoghq.com/account/settings#api)
![DatadogAPI](/Screens/DatadogAPI.png)

The following [template](https://docs.datadoghq.com/api/?lang=python#dashboards-post) can be used as a base to create a timeboard.

Here is the code which create a Timeboard using Datadog API :
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

To see whether or not the timeboard has been created, a check in the [Dashboard list](https://app.datadoghq.com/dash/list) has to be done.
![Timeboard manually created](/Screens/Answer4.png)

* Set the Timeboard's timeframe to the past 5 minutes

To set the Timeboard's timeframe to the last 5 minutes, a focus need to be done with the mouse. By selecting the timeframe desired.
As follows :
![Timeframe_To_5_Miutes](/Screens/Answer5.png)
* Take a snapshot of this graph and use the @ notation to send it to yourself.

Once, the timeframe is selected, beyond the timeboard, there is a field. Just start write with the character `@`.
![Use of @ notation](/Screens/Answer6.png)
* **Bonus Question**: What is the Anomaly graph displaying?

Anamoly graph is based on an algorithm that used usual data. When the data seem to be odd compared the usual value, a alert is raised. It has to be used for metrics that can not be monitored with threshold. For more [information](https://docs.datadoghq.com/guides/anomalies/).

The metrics have been created and vizualized. 
One of the benefit of Datadog is that data can be monitored and some user can be notify e-mails. The next chapter will describe how to deal with that.

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

All monitors are displayed and described in that [dedicated page](https://app.datadoghq.com/monitors/manage).
To create, a metric monitor. 
Go the [New monitor creation page](https://app.datadoghq.com/monitors#/create)
![Warning, Alert threshold](/Screens/Answer7.png)

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

In the following screenshot, there is the way to define a template for  notification mails. 
How to use metric's variables and host.
![Mail send by alert monitor](/Screens/Answer8.png)

* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

Below, a mail received after noification.
![Mail_send_part1](/Screens/Answer9.png) 
![Mail_send_part2](/Screens/Answer10.png)

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

Datadog allows to configure Downtime which represents slot times during when no notification mails are send.
They can be configured through this [panel](https://app.datadoghq.com/monitors#/downtime).


    * One that silences it from 7pm to 9am daily on M-F
    
The following screenshot describes how to set it as requested : from 7pm to 9am daily on M-F
![Downtime1](/Screens/Answer11.png)

    * And one that silences it all day on Sat-Sun.
    
The following screenshot describes how to set it as requested : all day on Sat-Sun
![Downtime2](/Screens/Answer12.png)
 
    * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
    
Since, downtimes have been configured. The following screeshot displays the downtime notification.
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
