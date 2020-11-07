## Answering all the technical exercise by Kazutoshi Shimazu ###

### 0. Prerequisites - Setup the environment ###

Installing Ubuntu/xenial64 OS with MySQL on My MAC laptop with Vagrant file

#### Installing mysql on ubuntu VM ####
```vb
sudo apt install mysql-server
```

#### Creating the MySQL DB user for datadog agent instead of using root user ####
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

### 1. Collecting Metrics: ###

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

##### 1.3.1 Creating the python file named `custom-agent-check.py` under`/etc/datadog-agent/checks.d` #####

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

##### 1.3.2 Creating the YAML file named `custom-agent-check.yaml` under`/etc/datadog-agent/conf.d` #####

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

##### 1.3.4 Verifying the custom check from the Datadog-agnet GUI #####

![Custom Agent Check#1](https://user-images.githubusercontent.com/47805074/98443791-11d26200-2151-11eb-9539-2de0a63d2eda.png)

![Custom Agent Check#2](https://user-images.githubusercontent.com/47805074/98443848-7ee5f780-2151-11eb-832d-880ae9742b6f.png)

#### 1.4 Change your check's collection interval so that it only submits the metric once every 45 seconds. ####

##### 1.4.1 Modifying the YAML file named `custom-agent-check.yaml` under`/etc/datadog-agent/conf.d` #####

 ```vb
cd /etc/datadog-agent/conf.d
vi custom-agent-check.yaml 

#instances: [{}]
init_config:
instances:
  - min_collection_interval: 45

```
##### 1.4.2 Restarting Datadog-Agent and then verify the custom check #####
 ```vb
sudo service datadog-agent restart
sudo -u dd-agent -- datadog-agent check custom-agent-check --check-rate
 
 ```

#### 1.5 Bonus Question Can you change the collection interval without modifying the Python check file you created? ####

That is doable by modifying the `YAML file` under instance configuration as per the URL below.
The default check interval is `15 sec`, but we can change it with `min_collection_interval` in the YAML file.

[How to enable a custom agent check] (https://docs.datadoghq.com/ja/developers/write_agent_check/?tab=agentv6v7)




