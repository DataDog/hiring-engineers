## Answering all the technical exercise by Kazutoshi Shimazu ###

### 0. Prerequisites - Setup the environment ###

#### Installing Ubuntu/xenial64 OS with MySQL on My MAC laptop with Vagrant (Oracle VM VirtualBox) ####

#### Installing mysql on ubuntu VM ####
```vb
sudo apt install mysql-server
```
#### Installing flask and mysql-connector-python-rf on ubuntu VM as part of APM demo ####

```vb
sudo python3 -m pip install -U flask
pip3 install mysql-connector-python-rf
```

#### Creating the MySQL DB user for datadog agent instead of using root user as per datadog's document ####
```vb

mysql> create user datadog@localhost identified by 'datadog';
Query OK, 0 rows affected (0.00 sec)

mysql> grant replication client on *.* to 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> grant process on *.* to 'datadog'@'localhost';
Query OK, 0 rows affected (0.00 sec)

mysql> grant select on performance_schema.* to 'datadog'@'localhost';
Query OK, 0 rows affected (0.00 sec)

```

#### Creating the `conf.yaml` under the `/etc/datadog-agent/conf.d/mysql.d/` as per the instruction below ####

[MySQL Metrics] (https://docs.datadoghq.com/ja/integrations/mysql/?tab=host)

```vb
cp conf.yaml.example conf.yaml
vi conf.yaml
diff -u conf.yaml.example conf.yaml 

root@main:/etc/datadog-agent/conf.d/mysql.d# diff -u conf.yaml.example conf.yaml 
--- conf.yaml.example   2020-10-21 07:42:49.000000000 +0900
+++ conf.yaml   2020-11-07 18:59:26.638507112 +0900
@@ -40,7 +40,7 @@
     ## @param pass - string - optional
     ## Password associated to the MySQL user.
     #
-    pass: <PASS>
+    pass: datadog
 
     ## @param port - number - optional - default: 3306
     ## Port to use when connecting to MySQL.
@@ -153,7 +153,7 @@
         ## @param replication - boolean - optional - default: false
         ## Set to `true` to collect replication metrics.
         #
-        # replication: false
+          replication: false
 
         ## @param replication_channel - string - optional
         ## If using multiple sources, set the channel name to monitor.
@@ -168,21 +168,21 @@
         ## @param galera_cluster - boolean - optional - default: false
         ## Set to `true` to collect Galera cluster metrics.
         #
-        # galera_cluster: false
+          galera_cluster: true
 
         ## @param extra_status_metrics - boolean - optional - default: true
         ## Set to `false` to disable extra status metrics.
         ##
         ## See also the MySQL metrics listing: https://docs.datadoghq.com/integrations/mysql/#metrics
         #
-        # extra_status_metrics: true
+          extra_status_metrics: true
 
         ## @param extra_innodb_metrics - boolean - optional - default: true
         ## Set to `false` to disable extra InnoDB metrics.
         ##
         ## See also the MySQL metrics listing: https://docs.datadoghq.com/integrations/mysql/#metrics
         #
-        # extra_innodb_metrics: true
+          extra_innodb_metrics: true
 
         ## @param disable_innodb_metrics - boolean - optional - default: false
         ## Set to `true` only if experiencing issues with older (unsupported) versions of MySQL
@@ -192,7 +192,7 @@
         ##
         ## see also the MySQL metrics listing: https://docs.datadoghq.com/integrations/mysql/#metrics
         #
-        # disable_innodb_metrics: false
+          disable_innodb_metrics: false
 
         ## @param schema_size_metrics - boolean - optional - default: false
         ## Set to `true` to collect schema size metrics.
@@ -203,7 +203,7 @@
         ##
         ## See also the MySQL metrics listing: https://docs.datadoghq.com/integrations/mysql/#metrics
         #
-        # schema_size_metrics: false
+          schema_size_metrics: false
 
         ## @param extra_performance_metrics - boolean - optional - default: true
         ## These metrics are reported if `performance_schema` is enabled in the MySQL instance
@@ -222,7 +222,7 @@
         ## to have PROCESS and SELECT privileges. Take a look at the
         ## MySQL integration tile in the Datadog Web UI for further instructions.
         #
-        # extra_performance_metrics: true
+          extra_performance_metrics: true
 
     ## @param tags - list of strings - optional
     ## A list of tags to attach to every metric and service check emitted by this instance.
```

#### Restarting the datadog-agent ####

```vb
 sudo service datadog-agent restart
 datadog-agent status
 ```

### 1. The requirements for Collecting Metrics ###

#### 1.1 Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog ####

##### 1.1.1 Modifying the `datadog.yaml` under the `/etc/datadog-agent/` as per the instruction below #####

[How to enable tagging] (https://docs.datadoghq.com/ja/getting_started/tagging/)

```vb
cp datadog.yaml datadog.yaml.backup
vi datadog.yaml
diff -u datadog.yaml.backup datadog.yaml

root@main:/etc/datadog-agent# diff -u datadog.yaml.backup datadog.yaml
--- datadog.yaml.backup 2020-11-07 19:27:13.197969195 +0900
+++ datadog.yaml        2020-11-07 20:32:38.870388214 +0900
@@ -48,8 +48,7 @@
 
 ## @param hostname - string - optional - default: auto-detected
 ## Force the hostname name.
-#
-# hostname: <HOSTNAME_NAME>
+hostname: ubuntu-vm01
 
 ## @param hostname_fqdn - boolean - optional - default: false
 ## When the Agent relies on the OS to determine the hostname, make it use the
@@ -63,15 +62,17 @@
 ##
 ## Learn more about tagging: https://docs.datadoghq.com/tagging/
 #
-# tags:
-#   - environment:dev
-#   - <TAG_KEY>:<TAG_VALUE>
+tags:
+  - location:Tokyo
+  - host_os:Ubuntu_xenial64
+  - mysql_version:5.7.32
+  - flask_version:1.1.2 
 
 ## @param env - string - optional
 ## The environment name where the agent is running. Attached in-app to every
 ## metric, event, log, trace, and service check emitted by this Agent.
 #
-# env: <environment name>
+env: dev
 
 ## @param tag_value_split_separator - list of key:value elements - optional
 ## Split tag values according to a given separator. Only applies to host tags,
@@ -1102,7 +1103,7 @@
 ## Valid log levels are: trace, debug, info, warn, error, critical, and off.
 ## Note: When using the 'off' log level, quotes are mandatory.
 #
-# log_level: 'info'
+log_level: 'info'
 
 ## @param log_file - string - optional
 ## Path of the log file for the Datadog Agent.



```

 ##### 1.1.2 Restarting the datadog-agent #####
 
```vb
 sudo service datadog-agent restart
 datadog-agent status
```

 ##### 1.1.3 Verifying all the tags are assigned to the host #####
 ```vb
datadog-agent status

root@main:/etc/datadog-agent# datadog-agent status 
<snip>
   Hostnames
  =========
    hostname: ubuntu-vm01
    socket-fqdn: main
    socket-hostname: main
    host tags:
      location:Tokyo
      host_os:Ubuntu_xenial64
      mysql_version:5.7.32
      flask_version:1.1.2
      env:dev
    hostname provider: configuration

```
 ![The screenshot taken from the hostmap](https://user-images.githubusercontent.com/47805074/98442036-98814200-2145-11eb-8c4f-0439f57b056e.png)
 
#### 1.2 Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database ####

`MySQL` was already installed on ubuntu-vm as part of `0.Prerequisites` and DD integration for MySQL DB also done.

![DD Integration for MySQL DB#1](https://user-images.githubusercontent.com/47805074/98442378-915b3380-2147-11eb-800d-dfdf39ae8eed.png)
![DD integration for MySQL DB#2](https://user-images.githubusercontent.com/47805074/98442560-a97f8280-2148-11eb-9ace-933de667d8d1.png)

#### 1.3 Create a custom Agent check that submits a metric named `my_metric` with a random value between `0` and `1000` ####

[How to enable a custom agent check] (https://docs.datadoghq.com/ja/developers/write_agent_check/?tab=agentv6v7)

##### 1.3.1 Creating the python file named `custom-agent-check.py` under`/etc/datadog-agent/checks.d` in my setup #####

 ```vb
root@main:/etc/datadog-agent/checks.d# pwd
/etc/datadog-agent/checks.d

root@main:/etc/datadog-agent/checks.d# cat custom-agent-check.py 
from datadog_checks.checks import AgentCheck
import random

__version__ = "1.0.0"

class HelloCheck(AgentCheck):
  def check(self, instance):
    random_value = random.randint(1, 1000)
    self.gauge('my_metric', random_value)
```

##### 1.3.2 Creating the YAML file named `custom-agent-check.yaml` under`/etc/datadog-agent/conf.d` in my setup #####

 ```vb
root@main:/etc/datadog-agent/conf.d# pwd
/etc/datadog-agent/conf.d

root@main:/etc/datadog-agent/conf.d# cat custom-agent-check.yaml 
instances: [{}]
```

##### 1.3.3 Verifying the custom check from the Datadog-agnet CLI #####

 ```vb
sudo service datadog-agent restart
sudo -u dd-agent -- datadog-agent check custom-agent-check --check-rate

root@main:/etc/datadog-agent/conf.d# sudo -u dd-agent -- datadog-agent check custom-agent-check --check-rate
=== Series ===
{
  "series": [
    {
      "metric": "my_metric",
      "points": [
        [
          1604758910,
          494
        ]
      ],
      "tags": [],
      "host": "ubuntu-vm01",
      "type": "gauge",
      "interval": 0,
      "source_type_name": "System"
    },
    {
      "metric": "my_metric",
      "points": [
        [
          1604758911,
          26
        ]
      ],
      "tags": [],
      "host": "ubuntu-vm01",
      "type": "gauge",
      "interval": 0,
      "source_type_name": "System"
    }
  ]
}
=========
Collector
=========

  Running Checks
  ==============
    
    custom-agent-check (1.0.0)
    --------------------------
      Instance ID: custom-agent-check:d884b5186b651429 [OK]
      Configuration Source: file:/etc/datadog-agent/conf.d/custom-agent-check.yaml
      Total Runs: 2
      Metric Samples: Last Run: 1, Total: 2
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 0, Total: 0
      Average Execution Time : 0s
      Last Execution Date : 2020-11-07 23:21:51.000000 JST
      Last Successful Execution Date : 2020-11-07 23:21:51.000000 JST

root@main:/etc/datadog-agent/conf.d# datadog-agent status 
Getting the status from the agent.
<snip>

===============
Agent (v7.23.1)
===============

  Status date: 2020-11-07 23:23:40.514383 JST
  Agent start: 2020-11-07 23:00:20.509259 JST
  Pid: 31494
  Go Version: go1.14.7
  Python Version: 3.8.5
  Build arch: amd64
  Agent flavor: agent
  Check Runners: 4
  Log Level: info

  Paths
  =====
    Config File: /etc/datadog-agent/datadog.yaml
    conf.d: /etc/datadog-agent/conf.d
    checks.d: /etc/datadog-agent/checks.d

```

##### 1.3.4 Verifying the custom check from the Datadog-agnet dashboard created manually #####

![Custom Agent Check#1](https://user-images.githubusercontent.com/47805074/98443791-11d26200-2151-11eb-9539-2de0a63d2eda.png)

![Custom Agent Check#2](https://user-images.githubusercontent.com/47805074/98443848-7ee5f780-2151-11eb-832d-880ae9742b6f.png)

#### 1.4 Change your check's collection interval so that it only submits the metric once every 45 seconds. ####

##### 1.4.1 Modifying the YAML file named `custom-agent-check.yaml` under`/etc/datadog-agent/conf.d` in my setup #####

 ```vb
cd /etc/datadog-agent/conf.d
vi custom-agent-check.yaml 

#instances: [{}]
init_config:
instances:
  - min_collection_interval: 45

```
##### 1.4.2 Restarting Datadog-Agent and then verifying the custom check #####
 
 ```vb
sudo service datadog-agent restart
sudo -u dd-agent -- datadog-agent check custom-agent-check --check-rate
 ```

#### 1.5 Bonus Question Can you change the collection interval without modifying the Python check file you created? ####

That is doable by modifying the `YAML file` under instance configuration as per the URL below.
The default check interval is `15 sec`, but we can change it with `min_collection_interval` in the YAML file.

[How to enable a custom agent check] (https://docs.datadoghq.com/ja/developers/write_agent_check/?tab=agentv6v7)


### 2. The requirements for Visualizing Data: Utilize the Datadog API to create a Timeboard ###

#### 2.1 `Your custom metric` scoped over your host ####
#### 2.1 Any metric from the Integration on your Database with `the anomaly function applied` ####
#### 2.1 Your custom metric with the rollup function applied to sum up all the points for `the past hour` into one bucket ####

##### 2.1.1 Creating Datadog-dog Application Key via Datadog GUI #####

DD-APPLICATION-KEY needs to be created first as per the url below.

[How to create a dashboard via REST API] (https://docs.datadoghq.com/ja/api/v1/dashboards/)

![Creating DD-APPLICATION-KEY](https://user-images.githubusercontent.com/47805074/98455688-5abd0180-21b7-11eb-8191-12365a67b197.png)

I used the python script to create a dashboard with 3 graphs in line with the requirements above.

 ```vb
#!/usr/bin/python3
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Ignore SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

"""
Nov, 8 2020
This script is for creating a dashboard through REST API
Author: Kazutoshi Shimazu
"""

PROTOCOL = 'https'
ADDRESS = 'api.datadoghq.com'
URL = '%s://%s/api/v1/dashboard' % (PROTOCOL, ADDRESS)
API_KEY = 'ea5e05c10b35b658cf07123746f5815b'
APP_KEY = '1de7f2d3abdbc8dce688fc3461bb8a42f8a713e1'

JSON_DATA_PAYLOAD = json.dumps({
    "title": "Visualizing Data through Datadog API",
    "widgets": [
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "anomalies(max:mysql.performance.queries{host:ubuntu-vm01}, 'basic', 2)",
                        "display_type": "line",
                        "style": {
                            "palette": "dog_classic",
                            "line_type": "solid",
                            "line_width": "normal"
                        }
                    }
                ],
                "yaxis": {
                    "max": "auto",
                    "scale": "linear",
                    "min": "auto",
                    "label": "",
                },
                "title": "Max of MySQL Performance Queries with the anomaly function applied"
            }
        },

        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "my_metric{host:ubuntu-vm01}"
                    }
                ],
                "yaxis": {
                    "max": "auto",
                    "scale": "linear",
                    "min": "auto",
                    "label": "",
                },
                "title": "my_metric with the default  setting"
            }
        },

        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "sum:my_metric{host:ubuntu-vm01}.rollup(sum,3600)"
                    }
                ],
                "yaxis": {
                    "max": "auto",
                    "scale": "linear",
                    "min": "auto",
                    "label": "",
                },
                "title": "my_metric summed up for the past hour"
            }
        },
    ],

    "layout_type": "ordered",
    "description": "A dashboard created via REST API",
    # "is_read_only": true,
    "notify_list": ["shimadyu9999@gmail.com"],
    "template_variables": [
        {
            "name": "host",
            "prefix": "host",
            "default": "ubuntu-vm01"
        }
    ],

})

if __name__ == '__main__':
    response = requests.post(url=URL, data=JSON_DATA_PAYLOAD,
                             headers={'Content-Type': 'application/json', 'DD-API-KEY': API_KEY,
                                      'DD-APPLICATION-KEY': APP_KEY, }, verify=False)
    print(json.dumps(response.json(), indent=4))

 ```

Here is the JSON response from datadoghq.com after performing the python script above.

 ```vb
{
    "notify_list": [
        "shimadyu9999@gmail.com"
    ],
    "description": "A dashboard created via REST API",
    "author_name": "Kazutoshi Shimazu",
    "template_variables": [
        {
            "default": "ubuntu-vm01",
            "prefix": "host",
            "name": "host"
        }
    ],
    "is_read_only": false,
    "id": "td5-qm9-vsn",
    "title": "Visualizing Data through Datadog API",
    "url": "/dashboard/td5-qm9-vsn/visualizing-data-through-datadog-api",
    "created_at": "2020-11-08T11:43:56.571363+00:00",
    "modified_at": "2020-11-08T11:43:56.571363+00:00",
    "author_handle": "shimadyu9999@gmail.com",
    "widgets": [
        {
            "definition": {
                "requests": [
                    {
                        "q": "anomalies(max:mysql.performance.queries{host:ubuntu-vm01}, 'basic', 2)",
                        "style": {
                            "line_width": "normal",
                            "palette": "dog_classic",
                            "line_type": "solid"
                        },
                        "display_type": "line"
                    }
                ],
                "title": "Max of MySQL Performance Queries with the anomaly function applied",
                "type": "timeseries",
                "yaxis": {
                    "max": "auto",
                    "scale": "linear",
                    "label": "",
                    "min": "auto"
                }
            },
            "id": 7753171838786262
        },
        {
            "definition": {
                "requests": [
                    {
                        "q": "my_metric{host:ubuntu-vm01}"
                    }
                ],
                "title": "my_metric with the default  setting",
                "type": "timeseries",
                "yaxis": {
                    "max": "auto",
                    "scale": "linear",
                    "label": "",
                    "min": "auto"
                }
            },
            "id": 8291163223111479
        },
        {
            "definition": {
                "requests": [
                    {
                        "q": "sum:my_metric{host:ubuntu-vm01}.rollup(sum,3600)"
                    }
                ],
                "title": "my_metric summed up for the past hour",
                "type": "timeseries",
                "yaxis": {
                    "max": "auto",
                    "scale": "linear",
                    "label": "",
                    "min": "auto"
                }
            },
            "id": 632619508899250
        }
    ],
    "layout_type": "ordered"
}

Process finished with exit code 0
 ```

![Verifying all the graphs](https://user-images.githubusercontent.com/47805074/98464288-2708c880-2205-11eb-8930-830510e69424.png)


#### 2.2 Set the Timeboard's timeframe to `the past 5 minutes` ####
#### 2.2 Take a snapshot of this graph and use `the @ notation` to send it to yourself ####


![How to send an email with attached screenshot](https://user-images.githubusercontent.com/47805074/98464879-24a86d80-2209-11eb-8289-341c6a270e3c.png)
![E-mail notification to myself using @notation](https://user-images.githubusercontent.com/47805074/98464944-7e109c80-2209-11eb-90be-02a7962a7331.png)


#### 2.3 Bonus Question: What is the Anomaly graph displaying? ####

[The anomaly detection] (https://docs.datadoghq.com/ja/monitors/monitor_types/anomaly/)

The anomaly graph that I was showing helps us understand `how much metrics you want to monitor can vary in a give period of time and how you can handle these deviations from the reference value and potential risks based on the historical data`.
I used `Basic` algorithm to determine the range of expected values as desceibed in the url above. 
You can also use other alogorihms like `Agile` and `Robust` (e.g. seasonal trends) as per your requirements.

### 3. The requirements for Monitoring Data ###

#### 3.1 Create a new Metric Monitor that watches the average of your custom metric (`my_metric`) and will alert if it’s above the following values over `the past 5 minutes` ####
#### 3.1 `Warning threshold of 500` ####
#### 3.1 `Alerting threshold of 800` ####
#### 3.1 It will notify you if there is `No Data` for this query over `the past 10m` ####

##### 3.1.1 The JSON configuration from Export Monitor #####

 ```vb
{
	"id": 25447132,
	"name": "Notification on my_metrics value changes  from {{host.name}}",
	"type": "metric alert",
	"query": "avg(last_5m):avg:my_metric{host:ubuntu-vm01} > 800",
	"message": "{{#is_alert}} The observed value {{value}} has crossed the current alert threshold {{threshold}} over the past 5 minutes. {{/is_alert}}\n{{#is_alert}} The affected host is {{host.name}}  with IP {{host.ip}}. {{/is_alert}}\n{{#is_alert}} Please take an appropriate corrective action if this is something that you're not expecting.  {{/is_alert}} \n\n{{#is_recovery}} The alert raised on {{host.name}}  with {{host.ip}} was cleared.  {{/is_recovery}} \n\n{{#is_warning}} The observed value {{value}} has crossed  the current warning threshold {{warn_threshold}} over the past 5 minutes  {{/is_warning}} \n{{#is_warning}} The affected hostname is {{host.name}}. {{/is_warning}} \n{{#is_warning}}Please take remedial actions if needed to make sure that the system named {{host.name}} is still working as intended. {{/is_warning}} \n\n{{#is_warning_recovery}} The warning raised on {{host.name}} was cleared. {{/is_warning_recovery}} \n\n{{#is_no_data}} No data is received. The issue could be either {{host.name}} brought down for some reason or network connectivity issue in between that you can't manage. {{/is_no_data}} \n{{#is_no_data}} Please take an remediate action if this is something that you're not expecting. {{/is_no_data}} \n\n{{#is_no_data_recovery}} The metrics on {{host.name}} has been received at datadog end. {{/is_no_data_recovery}} \n\n\n @shimadyu9999@gmail.com",
	"tags": [],
	"options": {
		"notify_audit": true,
		"locked": false,
		"timeout_h": 0,
		"new_host_delay": 300,
		"require_full_window": false,
		"notify_no_data": true,
		"renotify_interval": "0",
		"escalation_message": "",
		"no_data_timeframe": 10,
		"include_tags": true,
		"thresholds": {
			"critical": 800,
			"warning": 500
		}
	}
}
 ```
#### 3.2 Send you an email `whenever the monitor triggers` ####
#### 3.2 Create `different messages` based on whether the monitor is in an `Alert`, `Warning`, or `No Data` state ####
#### 3.2 Include `the metric value` that caused the monitor to trigger and `host ip` when the Monitor triggers an `Alert state` ####
#### 3.2 When this monitor sends you an email notification, take a `screenshot of the email` that it sends you ####

##### 3.2.1 The screenshot of the email taken when the monitor triggers or clears an Warning state #####

[How to set up alerting for your metrics] (https://docs.datadoghq.com/ja/monitors/notifications/?tab=is_alert)

The tag variables of `{{host.name}}` showing the hostname, `{{host.ip}}` showing the IP and `{{value}}` showing the value observed on average during the past 5 minutes are available to populate actual values in the message field.

Conditional variables of `#is_alert`, `#is_warning` and `is_no_data` also availble to notify a different message depending on the state (Alert/Warning/No Data).

Here is the screenshot of the email.

![E-mail notification about a warning state](https://user-images.githubusercontent.com/47805074/98498450-22d2be80-228a-11eb-96db-0115ffb7a7c0.png)
![Recovered](https://user-images.githubusercontent.com/47805074/98499180-236c5480-228c-11eb-9971-629a854b5472.png)

#### 3.3 Bonus Question: Set up `two scheduled downtimes` for this monitor ####
#### 3.3 One that `silences` it from `7pm` to `9am` `daily` on `M-F` ####
#### 3.3 And one that `silences` it `all day` on `Sat-Sun` ####
#### 3.3 Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification ####

##### 3.3.1 The configuration of manage Downtime###

![from 7pm to 9am daily on M-F](https://user-images.githubusercontent.com/47805074/98496712-9de5a600-2285-11eb-9103-d939efd68f1a.png)

![all day on Sat-Sun](https://user-images.githubusercontent.com/47805074/98498852-45190c00-228b-11eb-8015-0a7352f4af04.png)

##### 3.3.2 The screenshot of e-mail after scheduling the downtime #####

![email-1](https://user-images.githubusercontent.com/47805074/98497562-ad65ee80-2287-11eb-9837-5d183700f4f8.png)

![e-mail-2](https://user-images.githubusercontent.com/47805074/98497839-9c69ad00-2288-11eb-9454-59837368e8d8.png)

### 4. Collecting APM Data ###

#### 4.1 Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution ####

##### 4.1.1 Lab Diagram #####

My simple web applicaition showcases a CRUD (Create, Read, Update and Delete) to create/read/modify/delete a user account with Python Flask and MySQL DB on ubuntu VM.

![Diagram](https://user-images.githubusercontent.com/47805074/98524484-9db3cd80-22ba-11eb-91f7-44db6b87bffd.png)

1. The Rest Client trying to register a user (e.g. kazu in my setup) into the MySQL DB through the commonly-used HTTP methods (GET/POST/PUT/DELETE operations) using the python/shell script.
2. On receipt of HTTP requests from the Rest Client, Flask Web app will connect to MySQL DB and then the perform the SQL commands (SELECT/INSERT/UPDATE/DELETE) based on the HTTP methods.
3. Flask Web app will return the HTTP response with the username, HTTP status code and user's DB ID to the Rest Client as long as the required transactions are successfully committed to MySQL DB.

```vb
├── apm_demo
       ├── flask-mysql-demo.py
       ├── rest_client.py
       ├── test_flask.sh
```

Please see all the scripts above used for APM demo.

```vb

root@main:~/apm_demo# cat flask-mysql-demo.py
#!/usr/bin/python3
import mysql.connector
import sys
import logging
from flask import Flask
from flask import g
from flask import render_template
from flask import request
from flask import Response

"""
Nov, 9 2020
This script is created to showcase APM with flask and MySQL.
Author: Kazutoshi Shimazu
"""
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        conn = mysql.connector.connect(user='root',password='root',host='127.0.0.1')
        cursor = conn.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS mysql_db_demo')
        cursor.close()
        conn.close()
        db = g._database = mysql.connector.connect(user='root',password='root',host='127.0.0.1',database='mysql_db_demo')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/accounts', methods=['POST', 'PUT', 'DELETE'])
@app.route('/accounts/<name>', methods=['GET'])

def accounts(name=None):
    db = get_db()
    curs = db.cursor()
    curs.execute(
        'CREATE TABLE IF NOT EXISTS USER_CRUD ('
              'id integer not null AUTO_INCREMENT,'
               'name varchar(14) NOT NULL,'
               'PRIMARY KEY (id))')
    db.commit()
    name = request.values.get('name', name)

    if request.method == 'GET':
        curs.execute('SELECT * FROM USER_CRUD WHERE name = "{}"'.format(name))
        person = curs.fetchone()
        if not person:
            return '### [Read] Notice The user named {} is not yet registered in the MySQL DB ###'.format(name), 404
        user_id, name = person
        return '### [Read] The user namaed {} is already registered into the MySQL DB with the User-ID {} ###'.format(name, user_id), 200

    if request.method == 'POST':
        curs.execute('INSERT INTO USER_CRUD(name) values("{}")'.format(name))
        db.commit()
        return '### [Create] The user named {} is successfully created and then registered into the MySQL DB ###'.format(name), 201

    if request.method == 'PUT':
        new_name = request.values['new_name']
        curs.execute('UPDATE USER_CRUD set name = "{}" WHERE name = "{}"'.format(new_name, name))
        db.commit()
        return '### [Update] The existing user named {} is changed to user {} in the MySQL DB ###'.format(name, new_name), 200

    if request.method == 'DELETE':
        curs.execute('DELETE from USER_CRUD WHERE name = "{}"'.format(name))
        db.commit()
        return '### [Delete] The existing user named {} is successfully deleted from the MySQL DB ###'.format(name), 200

    curs.close()

def main():
    app.debug = True
    app.run(host='127.0.0.1', port=10005)

if __name__ == '__main__':
    main()


```

```vb
root@main:~/apm_demo# cat rest_client.py
#!/usr/bin/python3
import requests

"""
Nov, 9 2020
This script was created to perform the commonly-used HTTP methods (GET/POST/PUT/DELETE operations) to register a user into MySQL DB through flask web app
Author: Kazutoshi Shimazu
"""
PROTOCOL = 'http'
ADDRESS ='127.0.0.1'
PORT ='10005'
TEST_USER1 ='kazu'
TEST_USER2 ='kazutoshi'

GET_URL1 ='%s://%s:%s/accounts/%s'% (PROTOCOL,ADDRESS,PORT,TEST_USER1)
GET_URL2 ='%s://%s:%s/accounts/%s'% (PROTOCOL,ADDRESS,PORT,TEST_USER2)
POST_PUT_DELETE_URL ='%s://%s:%s/accounts'% (PROTOCOL,ADDRESS,PORT)

PAYLOAD_POST = {'name':'kazu'}
PAYLOAD_PUT = {'name': 'kazu', 'new_name': 'kazutoshi' }
PAYLOAD_DELETE =  {'name':'kazutoshi'}

response = requests.get(url=GET_URL1)
print("Response {}: Status code {}".format(response.text,response.status_code))

response = requests.post(url=POST_PUT_DELETE_URL, data=PAYLOAD_POST)
print("Response {}: Status code {}".format(response.text,response.status_code))

response = requests.get(url=GET_URL1)
print("Response {}: Status code {}".format(response.text,response.status_code))

response = requests.put(url=POST_PUT_DELETE_URL, data=PAYLOAD_PUT)
print("Response {}: Status code {}".format(response.text,response.status_code))

response = requests.get(url=GET_URL2)
print("Response {}: Status code {}".format(response.text,response.status_code))

response = requests.delete(url=POST_PUT_DELETE_URL, data=PAYLOAD_DELETE)
print("Response {}: Status code {}".format(response.text,response.status_code))

```

```vb
root@main:~/apm_demo# cat test_flask.sh 
#!/bin/bash

#
#Nov, 9 2020
#This script was created to perform the commonly-used HTTP methods (GET/POST/PUT/DELETE operations) to register a user into MySQL DB through flask web app
#Author: Kazutoshi Shimazu

set -e
Count=1
Total_num=11

func1() {
 while [ $Count -lt $Total_num ]
  do 
  echo "### $Count.Performing REST API calls (CRUD operations) towards Flask Web App with MySQL DB ###"
  func2
  python3 rest_client.py
  Count=$((Count + 1))
 done
}

func2() {
  if [ "$Count" = "5" ]; then
   echo "MySQL intentionally stopped to mimic the MySQL error"
   systemctl stop mysql
  elif [ "$Count" = "7" ]; then
   echo "MySQL started"
   systemctl start mysql
  fi
}

func1 &
func2 &
wait
```

Here are the outputs collected from my setup when the python/shell script performed.

```vb
root@main:~/apm_demo# sh test_flask.sh 
<snip>
Response ### [Read] Notice The user named kazu is not yet registered in the MySQL DB ###: Status code 404
Response ### [Create] The user named kazu is successfully created and then registered into the MySQL DB ###: Status code 201
Response ### [Read] The user namaed kazu is already registered into the MySQL DB with the User-ID 227 ###: Status code 200
Response ### [Update] The existing user named kazu is changed to user kazutoshi in the MySQL DB ###: Status code 200
Response ### [Read] The user namaed kazutoshi is already registered into the MySQL DB with the User-ID 227 ###: Status code 200
Response ### [Delete] The existing user named kazutoshi is successfully deleted from the MySQL DB ###: Status code 200
```
##### 4.1.2 Installing Cython and ddtrace on ubuntu VM #####

```vb
pip3 install Cython
pip3 install ddtrace
```
##### 4.1.3 Adding the service tag named `wep-app-flask` to `the datadog.yaml` under the `/etc/datadog-agent` #####

[Unified Service Tagging] (https://docs.datadoghq.com/getting_started/tagging/unified_service_tagging/?tab=kubernetes#non-containerized-environment)

```vb
cd /etc/datadog-agent
vi datadog.yaml
<snip>
tags:
  - location:Tokyo
  - host_os:Ubuntu_xenial64
  - mysql_version:5.7.32
  - flask_version:1.1.2
  - service:web-app-flask <<< HERE!

sudo service datadog-agent restart
```
##### 4.1.4 Adding the `DD_XXX` arguments to my application `ddtrace-run` command #####

[The trace for python application] (https://docs.datadoghq.com/ja/tracing/setup/python/)

```vb
DD_SERVICE="web-app-flask" 
DD_ENV="dev" 
DD_LOGS_INJECTION=true  
DD_HOST="ubuntu-vm01" 
DD_TRACE_SAMPLE_RATE="1" 
DD_PROFILING_ENABLED=true 
ddtrace-run python3 flask-mysql-demo.py

root@main:~/apm_demo# DD_SERVICE="web-app-flask" DD_ENV="dev" DD_LOGS_INJECTION=true DD_HOST="ubuntu-vm01" DD_TRACE_SAMPLE_RATE="1" DD_PROFILING_ENABLED=true ddtrace-run python3 flask-mysql-demo.py
 * Serving Flask app "flask-mysql-demo" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
2020-11-09 18:40:22,203 INFO [werkzeug] [_internal.py:113] [dd.service=web-app-flask dd.env=dev dd.version= dd.trace_id=0 dd.span_id=0] -  * Running on http://127.0.0.1:10005/ (Press CTRL+C to quit)
2020-11-09 18:40:22,203 - werkzeug - INFO -  * Running on http://127.0.0.1:10005/ (Press CTRL+C to quit)
2020-11-09 18:40:22,203 INFO [werkzeug] [_internal.py:113] [dd.service=web-app-flask dd.env=dev dd.version= dd.trace_id=0 dd.span_id=0] -  * Restarting with stat
2020-11-09 18:40:22,203 - werkzeug - INFO -  * Restarting with stat
2020-11-09 18:40:24,802 WARNING [werkzeug] [_internal.py:113] [dd.service=web-app-flask dd.env=dev dd.version= dd.trace_id=0 dd.span_id=0] -  * Debugger is active!
2020-11-09 18:40:24,802 - werkzeug - WARNING -  * Debugger is active!
2020-11-09 18:40:24,803 INFO [werkzeug] [_internal.py:113] [dd.service=web-app-flask dd.env=dev dd.version= dd.trace_id=0 dd.span_id=0] -  * Debugger PIN: 949-885-547
2020-11-09 18:40:24,803 - werkzeug - INFO -  * Debugger PIN: 949-885-547
```

##### 4.1.5 Checking whether both of wep-app-flask and mysql are displayed #####


![APM#1](https://user-images.githubusercontent.com/47805074/98531836-3f8be800-22c4-11eb-9af3-b236265f56e9.png)

![APM#2](https://user-images.githubusercontent.com/47805074/98532127-9f828e80-22c4-11eb-9464-53e6cc87a8b8.png)

![APM#3](https://user-images.githubusercontent.com/47805074/98532229-c5a82e80-22c4-11eb-9a6f-5416e15a13ed.png)

![APM#4](https://user-images.githubusercontent.com/47805074/98532665-5979fa80-22c5-11eb-9c14-49f5c819ed57.png)

![APM#5](https://user-images.githubusercontent.com/47805074/98533006-c3929f80-22c5-11eb-85ea-aab8f5767029.png)

![APM#6](https://user-images.githubusercontent.com/47805074/98533253-11a7a300-22c6-11eb-916c-5980cb545382.png)

![APM#7](https://user-images.githubusercontent.com/47805074/98533436-53384e00-22c6-11eb-87e1-b4c9339709d3.png)


#### 4.2 Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics ####

The dashboard below has `system.cpu.idle (max)`, `system.io.await` and `system.load.1` as part of `infra metrics` and `trace.flask.requests.error/hits` and `mysql.query.hits` as part of `APM`.

Constanly correlating between Web `App/DB` and `infra resource utilization (CPU/Disk IO etc)` with the same dashboard is really helpful to figure out both  of doing user impact and root cause analysis

![APM#8](https://user-images.githubusercontent.com/47805074/98535036-c5aa2d80-22c8-11eb-8390-b7dd4e958398.png)

https://app.datadoghq.com/dashboard/46d-vf4-7if/dashboard-created-manually-to-check-the-json-payload?from_ts=1604916251654&live=true&to_ts=1604919851654
https://app.datadoghq.com/dashboard/46d-vf4-7if/dashboard-created-manually-to-check-the-json-payload?from_ts=1604916251654&fullscreen_section=overview&fullscreen_widget=6668561559221867&live=true&to_ts=1604919851654&fullscreen_start_ts=1604917283925&fullscreen_end_ts=1604920883925&fullscreen_paused=false

#### 4.3 Bonus Question: What is the difference between `a Service` and a `Resource?` ####

[Resource] (https://docs.datadoghq.com/tracing/visualization/resource/)

`Resource` means a particualr action for a given endpoint. In my setup lab with flask and MySQL DB, The exact `Resource` should be below.

```vb

The Resouce of Flask:

1. GET /account/<name>
2. POST /accounts
3. PUT /accounts
4. DELETE /accounts
	
The Resource of MySQL:

1. CREATE TABLE IF NOT EXISTS USER_CRUD ('id integer not null AUTO_INCREMENT,'name varchar(14) NOT NULL,'PRIMARY KEY (id)')
2. CREATE DATABASE IF NOT EXISTS mysql_db_demo
3. SELECT * FROM USER_CRUD WHERE name = ?
4. UPDATE USER_CRUD set name = "{}" WHERE name = ?
5. INSERT INTO USER_CRUD(name) values(kazu)
6. DELETE from USER_CRUD WHERE name = ?

```
[Service] (https://docs.datadoghq.com/tracing/visualization/#services)

`Service` means a given endpoint (e.g. App and DB, etc). In my setup lab, `flask` and `MySQL` are the exact `services`.
`Services` are also the building blocks of modernized infra like micro-service architectrure.

### 5. Final Question ###

#### 5.1 Is there anything creative you would use Datadog for? ####

For mission critical use cases like connected and autonomous vehicles, V2X (vehicle to Everything), The vehicle will be changed to internet-connected endpoint.
According to the url below, The global connected car market was valued at $63.03 billion in 2019, and is projected to reach $225.16 billion by 2027.
[Connected Car Market Statistics – 2027] https://www.alliedmarketresearch.com/connected-car-market

The generic connected vehicle use case would be to push Vehicle data to the public clouds (also MEC) to let them process an enormous amount of data (e.g. environment information to drivers, road conditionsetc) to get the necessasry information in real time for safe driving.
However, the mobile network stability from vehicle to Cloud is also challenging due to handover interruption between 4G/5G base stations (RU/CU/DU) or external depedencies in between.

Another concern is a huge amount of data that single car generates. 
It's thought that one autonomous car generates 5TB and 20TB of data per day that could be exorbitant costs of cloud storage subscriptios.

[Connected Vehicle Platform using Cloud IoT core on Google Cloud] https://cloud.google.com/solutions/designing-connected-vehicle-platform
[storage estimates for intelligent vehicles vary widely] [https://blocksandfiles.com/2020/01/17/connected-car-data-storage-estimates-vary-widely/

Hence, the connected vehicle needs to analyze the data by the vehicle itself.
I'm hoping vehicles will have more compute resources as part of an edge device in the future and containerized vehicle applications could be deployed on a connected Vehicle acting as K8s worker nodes which are managed by K8s master node on public clouds.

For instance, DENSO is one of the global automobile manufactures and developing Kubernetes based connected vehicle platform named Misaki. 
That still seems to be under development, but it will change the way how connected vehicles build their applications.

[DENSO: Kubernetes based connected vehicle platform] https://www.youtube.com/watch?v=2x7jQTBUT5w&feature=emb_logo

In such context, The use case with Datadog would be to monitor vehicle as an edge device or trace Vehicle application amongst vehicles and multi-public clouds environments.

Datadog can display service map representing how V2V (vehicle to vehicle) or V2C (vehicle to cloud or everything) applications communicate between them behind the scenes and they can find any problematic Vehicle in service map topology that are relevant to the poorest resources and infrastructure (vehicle itself hosting vehicle app) metrics.

