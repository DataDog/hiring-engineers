## Stephen Reveliotty




### Prerequisites: 



I chose to use Virtualbox v5.2.22 and Vagrant (version 2.2.2) running bento/ubuntu-18.04

I signed up for a trial, downloaded and installed the agent:

```
root@vagrant: DD_API_KEY=<MY_API_KEY>  bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

```
root@vagrant:/tmp# datadog-agent version

Agent 6.7.0 - Commit: 2555a01 - Serialization version: 4.7.1
```



### Collecting Metrics:
---


* **Adding tags in the Agent config file:**


`root@vagrant:/etc/datadog-agent# vi /etc/datadog-agent/datadog.yaml`

![Host Tags in agent conf](/images/Host_Tags.png)

then restarted the agent:

`sudo systemctl restart datadog-agent`


screenshot of my host and its tags on the Host Map page in Datadog:

![Host Map with Tags](/images/Host_Map.png)

* **Install a database on your machine and then install the respective Datadog integration for that database:**

I chose to install MySQL :

`sudo apt-get install mysql-server`

Installing the Datadog integration for MySQL:

Reference: https://docs.datadoghq.com/integrations/mysql/

As per the documentation, this check is already included in the agent.  Following the instructions I created a database user ("datadog@localhost") and granted permissions to allow this user to collect metrics:

`mysql> CREATE USER 'datadog'@'localhost' IDENTIFIED BY '<UNIQUEPASSWORD>';`

```
mysql> GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> GRANT PROCESS ON *.* TO 'datadog'@'localhost';
Query OK, 0 rows affected (0.00 sec)
```

`mysql> GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';`


Then edited the mysql.d/conf.yaml file to gather metrics:

 `root@vagrant:/etc/datadog-agent/conf.d/mysql.d# vi /etc/datadog-agent/conf.d/mysql.d/conf.yaml`
 
 ![mysql yaml](/images/mysql_conf_yaml.png)
 
* **Create a custom Agent check:** 

(submit a metric named my_metric with a random value between 0 and 1000)


Reference: https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6#pagetitle

I created a custom check from the example (url) above and added in a random number :

 
`root@vagrant:/etc/datadog-agent/checks.d# vi my_metric.py`

```python

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


class My_MetricCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric.number', randint(0,1000))

```



For the initial check, also need a corresponding conf file.  In /etc/datadog-agent/conf.d/my_metric.yaml,  added:

`instances: [{}]`




![Metric](/images/my_metric_number.png)

* **Change your check's collection interval so that it only submits the metric once every 45 seconds.**

In the conf file /etc/datadog-agent/conf.d/my_metric.yaml changed contents to:

```
instances:
  - min_collection_interval: 45
  
  ```
  
* **Bonus Question Can you change the collection interval without modifying the Python check file you created?**

I may have misunderstood the previous two questions - I debated using time.sleep in my_metric.py before self.gauge, but after reading the docs, believed the way to do this was in the conf file for the instance.


## Visualizing Data



* **Utilize the Datadog API to create a Timeboard that contains:**


Your custom metric scoped over your host.

Any metric from the Integration on your Database with the anomaly function applied.

Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket


Reference:  https://docs.datadoghq.com/api/?lang=python#overview

Reference:  https://docs.datadoghq.com/api/?lang=python#create-a-timeboard


For this section, I installed pip on my host, and pip installed datadog. I also had to create an app key per the documentation referenced above (which was created in the API tab ofr my profile in the Datadog UI)

```python
from datadog import initialize, api

options = {
    'api_key': '10f0a2c69bef1b67ad086092bdc15f63',
    'app_key': '76531123e22758098a5d3a2db6c862cd28e3f5d4'
}

initialize(**options)

title = "Steve's Custom Timeboard"
description = "A custom metric timeboard"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric.number{host:sreveliotty}"}
        ],
        "viz": "timeseries"
    },
    "title": "Custom My_Metric"
},

{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.performance.user_time{*},'basic',3)"}
        ],
        "viz": "timeseries"
    },
    "title": "MySQL Perf User Time"
},

{
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric.number{*}.rollup(sum,3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "Custom My_Metric Sum Rollup One Hour"
}]

template_variables = [{
    "name": "sreveliotty",
    "prefix": "host",
    "default": "host:sreveliotty"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)




```

![Timeboard pic](/images/timeboard.png)



Once this is created, access the Dashboard from your Dashboard List in the UI:


Set the Timeboard's timeframe to the past 5 minutes

![5min Snapshot](/images/5min_snapshot.png)


Take a snapshot of this graph and use the @ notation to send it to yourself.

![at notation email](/images/notation_email.png)

Bonus Question: What is the Anomaly graph displaying?

The Anomaly graph is displaying actual performance versus what is 'predicted' or expected based on trends and statistical models.  In this case I just chose 'Basic', which is doing a lagging, rolling computation where Agile and Robust will account for seasonal day/time trends and watch for according metric shifts.


## Monitoring Data

* **Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:**

Warning threshold of 500

Alerting threshold of 800

And also ensure that it will notify you if there is No Data for this query over the past 10m.


To create, in the Datadog UI I went to 'Monitors' -> 'New Monitor'  chose 'Metric' from the options, then filled out as below:


![Monitor](/images/Metric_monitor.png)

```
{{#is_alert}}

Alert! {{value}} exceeds {{threshold}} on {{host.ip}}


{{/is_alert}} 

{{#is_warning}}

Warning: Custom Metric has crossed {{warn_threshold}} 

{{/is_warning}} 

{{#is_no_data}}

No data received for custom metric 

{{/is_no_data}} 



Notify: @steve.rev@gmail.com
```

![alert](/images/alert.png)


* **Bonus Question** 
set up downtime to silence alerts over the weekend and 7pm-9am Monday - Friday 

![weekday downtime](/images/downtime_m-F)


