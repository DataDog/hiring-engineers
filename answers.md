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
2) create the datadog-agent/conf.d/mysql.d/conf.yaml as follow to get metrics collected:

```
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

For that I just changed the datadog-agent/conf.d/custom_check.yaml to the following:

```yaml
init_config:

instances:
  - min_collection_interval: 45
```

**Bonus Question Can you change the collection interval without modifying the Python check file you created?**

Yes, just changing the parameter `min_collection_interval` to the desired value on the custom_check.yaml file without modifying the python check script.

