### Candidate: Murat Goncu 
### Contact: muratlutfigoncu@gmail.com

# Collecting Metrics:

#### - Added tags: hello:world, machine:ubuntu/xenial and env:test
#### - Please see image: 

![alt text](https://raw.githubusercontent.com/muratlutfigoncu/hiring-engineers/master/images/question1.png)


## Database Integration:


From DataDog dashboard: Click Integrations and select PostgreSQL
To collect database metrics, we need to create a user on PostgreSQL and grant access


```bash
create user datadog with password 'pass';
grant SELECT ON pg_stat_database to datadog;
```

Then let's edit the configuration file at /etc/datadog-agent/conf.d/mongo.d:

```yaml
init_config:

instances:
   -   host: localhost
       port: 5432
       username: datadog
       password: pass
    
       tags:
            - machine:ubuntu-xenial
            - env:exercice
            - app:postgres
```

The configuration file should be active after datadog agent restart.

```bash
sudo systemctl restart datadog-agent  ### restart service
sudo systemctl status datadog-agent	  ### check status of service
sudo datadog-agent status ### check status of agent
```

The result should be like the image below.
![alt text](https://raw.githubusercontent.com/muratlutfigoncu/hiring-engineers/master/images/postgres1.png)

Let's check our dashboard: click Dashboards on the menu and select Postgres - Metrics.
The result should be like the image bellow
![alt text](https://raw.githubusercontent.com/muratlutfigoncu/hiring-engineers/master/images/postgres2.png)

##  Creating a Custom Check:
To create a custom check we need to create two things: hello.py and a configuration file for that check hello.yaml. (Names should be the same).
hello.py should be placed in a folder called 'checks' 

in conf.d/hello.yaml

```yaml
init_config:

instances:
    [{}]
```


in hello.py  

```python
from checks import AgentCheck
import random

class hello(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1001))

```


##  Editing custom check's collection interval:

In order to edit the collection interval, we need to edit hello.yaml file. 
```yaml
min_collection_interval: 45  ##seconds
```


##  Bonus question:

To change the collection interval, we can use the datadog user interface. For this click Metrics -> Summary then search for your metric, in our case my_metric, click on it. Now edit the metadata, custom change the interval.

![alt text](https://raw.githubusercontent.com/muratlutfigoncu/hiring-engineers/master/images/customcheck.png)


# Visualizing Data:

## Timeboard
In order to create a timeboard using the DataDog API, we need to create a pair of credentials (api key and app key). Navigate to Integrations -> API's and click create application key and create API key. Copy those keys, we will need them in our timeboard creator python  file.

To create timeboard using DataDog API, created a python file like below. Which created three graphs: my_metric, postgresql.bgwriter.checkpoints_timed anomalies graph and my_metric 1 hour rollup graph, all from the host:ubuntu-xenial. 

In order to run the python file below (timeboardCreator.py), we have to install python datadog module in our system, we will be using pip to install packages. If your system doesn't have pip you can install with the following commands:

```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

```bash
pip install datadog
```
We can confirm python datadog installation by using python shell:

```bash
$ python
>>> import datadog
>>> print datadog.__version__
```


```python
### timeboardCreator.py

from datadog import initialize, api

options = {
    'api_key': '****',  # Enter the api key
    'app_key': '****'   # Enter the app key 
}

initialize(**options)

title = "My Timeboard"                          # Give your timeboard a title
description = "An informative timeboard."       # Description of your timeboard
graphs = [                                      # Make a list of the graphs that you want to create in the timeboard

    ### Json used to create my_metric graph
    {
        "definition": {
            "events": [],
            "requests": [
                {   "q": "avg:my_metric{host:ubuntu-xenial}", 
                }
            ],
        },
        "title": "my_metric" ## Title of the graph
    },

    ### Json used to create graph from postgresql metric
    {
        "definition": {
            "events": [],
            "requests": [
                {   
                    "q": "anomalies(avg:postgresql.bgwriter.checkpoints_timed{host:ubuntu-xenial}, 'basic', 2)"
                }
            ],
        },
        "title": "bgwriter.checkpoints_timed anomalies" ## Title of the graph
    }, 

    ### Json used to create graph from my_metric (rollup of 1 hour)
    {
        "definition": {
            "events": [],
            "requests": [
                {   
                    "q": "avg:my_metric{host:ubuntu-xenial}.rollup(sum,3600)"
                }
            ],
        },
        "title": "my_metric rollup" ## Title of the graph
    },
]
read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)

```

Created timeboard can be seen below:

![alt text](https://raw.githubusercontent.com/muratlutfigoncu/hiring-engineers/master/images/timeboard.png)


Created an annotation from my_metric graph. Clicked the camera icon at the right-corner of the my_metric graph and entered the user email to annotate. Result can be seen below:

![alt text](https://raw.githubusercontent.com/muratlutfigoncu/hiring-engineers/master/images/annotation.png)


## Bonus question:

The anomaly graph is showing us where a metric is behaving differently than it has in the past. This type of graph will display in red color, when the anomaly happens.


# Monitoring Data:

Created a new metric monitor for my_metric on host ubuntu-xenial. Selected my_metric then defined alert conditions:
Alert if my_metric is above 800 over last 5 minutes
Warning if my_metric is above 500 over last 5 minutes
No Data if cannot receive values from my_metric for more than 10 minutes

Then created different messages for every condition and added the current value of my_metric to the message. The monitor will also send a notification to user. The message template can be found below:

```bash

{{#is_alert}}  Alert: my_metric is above 800! Current value is {{value}} {{/is_alert}}
{{#is_warning}} Warning: my_metric is above 500! Current value is {{value}}  {{/is_warning}}
{{#is_no_data}} No Data from my_metric over the last 10 minutes {{/is_no_data}}

@muratlutfigoncu@gmail.com
```

On the image below we can see the screenshot of the mail notification.

![alt text](https://raw.githubusercontent.com/muratlutfigoncu/hiring-engineers/master/images/mailnotif.png)


## Bonus:

Let's start with weekdays. On the monitor page, navigate to Manage Downtime. From here selected the host that we want to silence (i.e. host:ubuntu-xenial). Created a silencer:  start date today, repeating everyday, beginning hour 19:00 and lasting 14 hours and no end date. This silencer will schedule downtime for weekdays but also weekends. But we want to schedule downtime for every weekend. To accomplish this we will need to create another scheduler. For example: start date would the next weekend (in my case 04/08/2018), repeating every 5 days, beginning hour 00:00 and lasting 24 hours.
![alt text](https://raw.githubusercontent.com/muratlutfigoncu/hiring-engineers/master/images/downtimeschedule.png)

# Collecting APM Data:


Used the Flask application provided and insert the middleware. 

```python
from flask import Flask
import logging
import sys
from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware
from ddtrace import patch_all
import blinker as _

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

traced_app = TraceMiddleware(app, tracer, service="flask-trace", distributed_tracing=False)

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

Intalled necesasary packages to run this python flask application:

```bash
pip install flask ddtrace blinker
```

To make APM trace work, first we need to enabled APM config in datadog.yaml located in /etc/datadog-agent. The APM part in yaml file can be commented out:

```yaml
apm_config:
#   Whether or not the APM Agent should run
    enabled: true
```

Then restart datadog agent using terminal commands and check status of agent.

```bash
sudo systemctl restart datadog-agent
sudo systemctl status datadog-agent
```

Finally run Flask application:

```bash
python test.py
```

In a couple of minutes, DataDog APM will start to display metrics obtained from our Flask application.
Created a dashboard with values obtain from Flask application and also system metrics. 

![alt text](https://raw.githubusercontent.com/muratlutfigoncu/hiring-engineers/master/images/dashboard.png)

Also we can create a public url to share our dashboard with others, on the Dashboard page click the settings icon and click generate public URL. Here's the public url of the dashboard:

https://p.datadoghq.com/sb/18ff9e83c-91b55934d75d1498487fd686be5dc6c1


## Bonus question (What is the difference between a Service and a Resource?):

A service is the name given to a set of processes that work together. For example a web application can consist of two services: webapp and database. Whereas a resource is specific action for a service. In a web application an examples of a resource might be a canonical URL like /user/home.



# Final question:

In Istanbul we have three bridges that connects two sides of the city (Europe and Asia). Generally people live in the asian side and travel through the european side for work. Everyday millions of people travels from Asia to Europe and vice versa and while passing pay tolls. In the rush hour, traffic jams are massive, as you can see in the image below :). DataDog can be used to monitor the devices embedded in tollhouses used for automatic tolling.


![alt text](https://raw.githubusercontent.com/muratlutfigoncu/hiring-engineers/master/images/traffic.jpg)


