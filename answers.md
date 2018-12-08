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


[!Custom Metric](/images/my_metric_number.png)


* **Change your check's collection interval so that it only submits the metric once every 45 seconds.**

In the conf file /etc/datadog-agent/conf.d/my_metric.yaml changed contents to:

```
instances:
  - min_collection_interval: 45
  
  ```
  
* **Bonus Question Can you change the collection interval without modifying the Python check file you created?**











