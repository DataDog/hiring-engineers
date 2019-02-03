# Collecting Metrics:

## Requirements
- Vagrant

## Installing datadog agent

``` bash
DD_API_KEY=my_keyXXXXXX bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
# Collecting Metrics

* We need to a tag as follows

``` bash
# vi /etc/datadog-agent/datadog.yaml
```
``` bash
# add tags
tags:
  - env:ubuntu:local
```
``` bash
# service datadog-agent restart
```
![tag-snapshot](https://github.com/cmcornejocrespo/hiring-engineers/blob/solutions-engineer/images/01-tags.jpg)

We use MySQL as an example of integration and follow installation instructions provided
* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
``` bash

# Configure the Agent to connect to MySQL
vi /etc/datadog-agent/conf.d/mysql.yaml

init_config:

instances:
  - server: localhost
    user: datadog
    pass: mypass
    tags:
        - optional_tag1
        - optional_tag2
    options:
      replication: 0
      galera_cluster: 1
      
# restart the agent
service datadog-agent restart

# check agent status (mysql)
datadog-agent status
...

 mysql (1.5.0)
    -------------
      Instance ID: mysql:4fblah49a9ad6c6f1 [OK]   
...

```

Create the custom check

```bash
#add custom metrics
vi /etc/datadog-agent/conf.d/my_metric.yaml

instances: [{}]
```
```bash
#create check

vi /etc/datadog-agent/checks.d/my_metric.py

from random import randint
# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from old versions of the Agent...
    from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"


class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(0,1000))

# restart agent
service datadog-agent restart

# check the check is ok
datadog-agent check my_metric

```

Change your check's collection interval so that it only submits the metric once every 45 seconds

```bash
#add min_collection_interval
vi /etc/datadog-agent/conf.d/my_metric.yaml

init_config:

instances:
  - min_collection_interval: 45
  
# restart agent
service datadog-agent restart

```

- Bonus Question Can you change the collection interval without modifying the Python check file you created?

  By changing the interval at the instance level in the yaml file.

# Visualizing Data

We need to get the API authorization sorted by requesting API Keys and Application key.
We create a new application key in the in the account’s API [view](https://app.datadoghq.com/account/settings#api).

The script used to create the timeboard can be found [here](https://github.com/cmcornejocrespo/hiring-engineers/blob/solutions-engineer/visualizing-task/create-timeboard.sh).

![snapshot](https://github.com/cmcornejocrespo/hiring-engineers/blob/images/02-graph.png) 

- Bonus Question: What is the Anomaly graph displaying? 
It allows you to identify when a metric threshold based on basic algorithm is behaving differently than it was over the past.

# Monitoring Data

Create a new Metric Monitor

![snapshot](https://github.com/cmcornejocrespo/hiring-engineers/blob/images/03-monitoring-data.png)

Configure the monitor’s message accordingly

``` markdown
{{#is_alert}} 

Alert threshold ({{threshold}}) exceeded with value :: {{value}}!! 
Please check on {{host.name}} :: {{host.ip}}  

{{/is_alert}}
{{#is_warning}}

Warning threshold exceeded!!

{{/is_warning}} 
{{#is_no_data}}

There is no data from my metric for the last 10 minutes!!

{{/is_no_data}}
@carlos.cornejo.crespo@gmail.com
```

![email-snapshot](https://github.com/cmcornejocrespo/hiring-engineers/blob/images/04-email-snapshot.png)

- Bonus Question

![downtime-weekend](https://github.com/cmcornejocrespo/hiring-engineers/blob/images/05-downtime-weekend.png)
![downtime-working-days](https://github.com/cmcornejocrespo/hiring-engineers/blob/images/06-downtime-working-days.png)


# Collecting APM Data:

We need to [install](https://docs.datadoghq.com/tracing/languages/python/) the Datadog Tracing library so we can instrument the provided python app.

We run the agent, curl the endpoints and check APM is working in the UI.

![apm-01-snapshot](https://github.com/cmcornejocrespo/hiring-engineers/blob/images/apm-01.png)
![apm-02-snapshot](https://github.com/cmcornejocrespo/hiring-engineers/blob/images/apm-02.png)
![apm-03-snapshot](https://github.com/cmcornejocrespo/hiring-engineers/blob/images/apm-03.png)

![public accesible dashboard](https://p.datadoghq.com/sb/xc8xyqjicrfqidw7-bf1a6ec613ef25b6be8b8d166327d2db)
![public dashboard snapshot](https://github.com/cmcornejocrespo/hiring-engineers/blob/images/apm-04.png)


![public dashboard snapshot](https://github.com/cmcornejocrespo/hiring-engineers/blob/images/07-weekend-notification.png)

- Bonus Question: What is the difference between a Service and a Resource?

A Service is a set of processes that do the same job, and a Resource is a particular action for a service.

Using our flask app as an example, the service is the app itself that have a number of resources ("/", "/api/apm", "/api/trace").