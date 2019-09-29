# Prerequisites - Setup the environment

My approach was to spin up a Debian 10 Linux Server running on a Public Cloud Provider

The DataDog Agent installed with the following command:

```
$ DD_API_KEY=<MY_API_KEY> DD_SITE="datadoghq.eu" bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

# Collecting Metrics:

**Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.**

I added the following tags on the /etc/datadog-agent/datadog.yaml file:

```
tags:
   - env_test:testing_datadog_tags
   - test:succeeded
```

![screenshot][screenshots/debian-dd-box_extra_tags.png]


**Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.**

I installed Mysql Database and took the following steps for datadog integration collects metrics:

1) Added datadog user on Mysql Database with right privileges;

```sql
CREATE USER 'datadog'@'localhost' IDENTIFIED BY '<DATADOG_MYSQL_PASS>';
GRANT PROCESS ON *.* TO 'datadog'@'localhost';
ALTER USER 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';
```

2) create the datadog-agent/conf.d/mysql.d/conf.yaml as follow to get metrics collected:

```yaml
init_config:

instances:
  - server: 127.0.0.1
    user: datadog
    pass: '<DATADOG_MYSQL_PASS>' 
    port: 3306 
    options:
        replication: 0
        galera_cluster: true
        extra_status_metrics: true
        extra_innodb_metrics: true
        extra_performance_metrics: true
        schema_size_metrics: false
        disable_innodb_metrics: false
```

3) Restart the datadog Agent;
4) Install datadog mysql integration on the datadog dashboard.

![screenshot][screenshots/debian-dd-box_mysql_integration.png] 
![screenshot][screenshots/debian-dd-box_mysql_metrics.png]

**Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.**

For that I wrote the datadog-agent/check.d/custom_check.py script with the following code:

```python
from datadog_checks.checks import AgentCheck
from random import randint

class Check(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(0,1000))
```

And the following datadog-agent/conf.d/custom_check.yaml file:

```yaml
init_config:

instances:
  - min_collection_interval: 30
```

![screenshots/debian-dd-box_custom_my_metric.png]


**Change your check's collection interval so that it only submits the metric once every 45 seconds.**

For that I just changed the `min_collection_interval` on datadog-agent/conf.d/custom_check.yaml to the following:

```yaml
init_config:

instances:
  - min_collection_interval: 45
```


**Bonus Question Can you change the collection interval without modifying the Python check file you created?**

Yes, just changing the parameter `min_collection_interval` to the desired value on the custom_check.yaml file without modifying the python check script.


# Visualizing Data:

**Utilize the Datadog API to create a Timeboard that contains:

Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.**

Below, the python script I wrote for using the Datadog API for creating the requested Timeboard:

```python
from datadog import initialize, api

options = {
    'api_key': '566d9fdc17db68dbf7fe45c583e87ab0',
    'app_key': '210918174a206a326464ab8a04a620e387e21d41',
    'api_host': 'https://api.datadoghq.eu'
}

initialize(**options)

title = 'my_metric dashboard'
description = 'Testing adding a new dashboard for my_metric using datadog API.'
layout_type = 'ordered'

widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{host:datadog-debian-box}'}
        ],
        'title': 'my_metric on datadog-debian-box'
    }
},
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "anomalies(avg:mysql.performance.user_time{host:datadog-debian-box}, 'basic', 3)"}
        ],
        'title': 'Mysql CPU time per user'
    }
},
    {
    'definition': {
        'type': 'query_value',
        'requests': [
            {'q': 'my_metric{host:datadog-debian-box}.rollup(sum, 3600)'}
        ],
        'title': 'my_metric rollup function'
    }
}]

api.Dashboard.create(title=title,widgets=widgets,description=description,layout_type=layout_type)
```

![screenshots/datadog-debian-box_dashboard_api_creation.png]
![screenshots/datadog-debian-box_my_metric_rollup_function.png]


**Once this is created, access the Dashboard from your Dashboard List in the UI:

Set the Timeboard's timeframe to the past 5 minutes
Take a snapshot of this graph and use the @ notation to send it to yourself.**

Please check the screenshot below which shows I'm sending the 5 minutes graph to myself using the datadog dashboard

![screenshots/datadog-debian-box_my_metric_sending_snapshot.png]

**Bonus Question: What is the Anomaly graph displaying?**

On the graph I've created the Anomaly will show any deviation on Mysql CPU usage per user, based on previous collected metrics. This could be a good graph for identify possible sql queries using too much resource or having a different behaviour than expected.

The blue line shows the regular cpu time per user and the red line possible anomalies.


# Monitoring Data


