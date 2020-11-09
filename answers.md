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

##### 3.2.1 The screenshot of the email taken when the monitor triggers an alert state #####

[How to set up alerting for your metrics] (https://docs.datadoghq.com/ja/monitors/notifications/?tab=is_alert)

The tag variables of `{{host.name}}` showing the hostname, `{{host.ip}}` showing the IP and `{{value}}` showing the value observed on average during the past 5 minutes are available to populate actual values in the message field.

Conditional variables of `#is_alert`, `#is_warning` and `is_no_data` also availble to notify a different message depending on the state (Alert/Warning/No Data).

Here is the screenshot of the email.

#### 3.3 Bonus Question: Set up `two scheduled downtimes` for this monitor ####
#### 3.3 One that `silences` it from `7pm` to `9am` `daily` on `M-F` ####
#### 3.3 And one that `silences` it `all day` on `Sat-Sun` ####
#### 3.3 Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification ####

##### 3.3.1 The configuration of mmanage Downtime###

![from 7pm to 9am daily on M-F](https://user-images.githubusercontent.com/47805074/98496712-9de5a600-2285-11eb-9103-d939efd68f1a.png)

![all day on Sat-Sun](https://user-images.githubusercontent.com/47805074/98496808-cf5e7180-2285-11eb-94a2-4db8c72a9c65.png)

##### 3.3.2 The screenshot of e-mail after scheduling the downtime #####







