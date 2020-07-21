# 1:Setup the environment:
*  #### The first step of this exercise was to setup the environment. I followed the recommendation and decided to use a Vagrant VM running Ubuntu. I had a lot of experience deploying VM using VMware product, but it was a first for me with Vagrant. I used *VirtualBox 6.1.12 for Linux* as a virtualizer, pre-packaged with *Ubuntu 19.10 / 20.04*. Then I downloaded and launched *Vagrant 2.2.9_x86_64*
  ```
  > vagrant init hashicorp/bionic64
  > vagrant up
   ```
  
  Here is the result:
  ![](./Vagrant_VM.png)

* #### I then went ahead and installed the Datadog Agent for Ubuntu by running the one-step install command:
```
DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=3163017dc099bcab6c9860e05f3a7ade DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
```
```
vagrant@vagrant:/etc/datadog-agent$ ls -ltr
total 148
-r--r-----   1 dd-agent dd-agent   918 Jun 17 10:28 system-probe.yaml.example
-rw-r--r--   1 dd-agent dd-agent 55687 Jun 17 10:28 datadog.yaml.example
drwxr-xr-x   2 dd-agent dd-agent  4096 Jul  7 02:45 selinux
-rw-r--r--   1 dd-agent dd-agent   117 Jul  7 02:45 install_info
-rw-------   1 dd-agent dd-agent    64 Jul  7 02:45 auth_token
-rw-r-----   1 dd-agent dd-agent 55700 Jul  7 03:33 datadog.yaml
drwxr-xr-x 144 dd-agent dd-agent  4096 Jul  7 03:41 conf.d
drwxr-xr-x   3 dd-agent dd-agent  4096 Jul  7 03:51 checks.d
-rw-r--r--   1 root     root      1195 Jul  7 16:43 my_dashboard.py
drwxr-xr-x   2 root     root      4096 Jul  8 15:45 DD_test
-rw-r--r--   1 root     root       685 Jul  8 18:13 trial_app.py
```
# 2:Collecting Metrics:
*  #### The next step was to setup tags in the agent config file. I decided to change the hostname, add a tag for the specific geolocalized area, and define the environment into which the host will be running. Those tags were changed in the datadog.yaml file ![Tags](./tags_datadog_yaml.png)
  
  Here is the resulting Host Map Screenshot take from the Datadog WebUI: ![hostmap_screenshot](./1-hostmap_screenshot.png)

*  #### I went on and installed a local MySQL server and created the datadog user with the suggested grants
  ```
  sudo apt install mysql-server
  sudo mysql
  mysql>CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'datadog';
  mysql> GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
  mysql> GRANT PROCESS ON *.* TO 'datadog'@'localhost';
  mysql> GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';
  mysql>
  mysql> show databases like 'performance_schema';
  +-------------------------------+
  | Database (performance_schema) |
  +-------------------------------+
  | performance_schema            |
  +-------------------------------+
  1 row in set (0.00 sec)
  ```
  MYSQL installation: ![MYSQL](./mysql.png)
  
  * I then edited the MYSQL config file to add the metric collection configuration block. I also added a tag for dbtype because I thought in a multi-DB system it would be easier to track some metrics:
  ```
  instances:
  - server: 127.0.0.1
    user: datadog
    pass: datadog
    port: 3306
    tags:
       - dbtype:mysql
    options:
      replication: false
      galera_cluster: true
      extra_status_metrics: true
      extra_innodb_metrics: true
      extra_performance_metrics: true
      schema_size_metrics: false
      disable_innodb_metrics: false
   ```
  You can find the complete yaml file here: [MYSQL conf.yaml](./mysql_conf.yaml)
  
* #### Then I had to setup a custom check agent that submits a metric named my_metric with a random value between 0 and 1000: Here is the Custom Check Agent python script */etc/datadog-agent/checks.d/my_metric.py*:
```python
import random

from datadog_checks.base import AgentCheck

__version__ = "1.0.0"

class MyClass(AgentCheck):
 def check(self, instance):
  self.gauge(
   "my_metric.gauge",
   random.randint(0, 1000),
   tags=["env:sandbox","metric_submission_type:gauge"])
```
  
* #### Next, I was asked to change the collection interval so that it only submits the metric once every 45 seconds. To do so I added a parameter *min_collection_interval: 45* to the */etc/datadog-agent/conf.d/my_metric.d/my_metric.yaml*
```yaml
init_config:

instances:
 - min_collection_interval: 45
```

### Bonus Question Can you change the collection interval without modifying the Python check file you created ?
DD: Yes through the metric’s config file …/conf.d/my_metric.d/my_metric.yaml

# 3:Visualizing Data:
  Dashboard creation API Script: [my_dashboard.py](./my_dashboard.py)
  
  Resulting dashboard Screenshot: ![My_dashboard_screenshot](./4-My_dashboard_screenshot.png)

  Dashboard with a 5 min timeframe: ![my_dashboard_5min_screenshot](./5-my_dashboard_5min_screenshot.png)

  Dashboard Snapshot and @notation email: ![snapshot_notation_email](./6-snapshot_notation_email.png)

  ### Bonus Question: What is the Anomaly graph displaying? 
  DD: The anomaly graph is highlighting abnormal variations in data value as compared to the majority of values in the given interval. In my case it highlights spikes in cpu   utilization for the given timeframe.

# 4:Monitoring Data:
  Create a metric monitor : ![metric_monitor](./7-metric_monitor.png)

  Triggered alert email notification: ![Triggered_alert_email](./8-Triggered_alert_email.png)

  ### Bonus Question: 
  Downtime email notif : ![Downtime_schedule_emails](./9-Downtime_schedule_emails.png)
  
  Downtime schedules: ![Downtime_schedule_screenshot](./10-Downtime_schedule_screenshot.png)

 # 5:Collecting APM data
  Instrumented app: [trial_app](./trial_app.py)
  
  Dashboard Screenshot with Infrastructure and APM metrics: ![Dasboard_with_APM_screenshot](./11-Dasboard_with_APM_screenshot.png)
  
  Dashboard link: https://p.datadoghq.com/sb/pplgzjts4v4gyxk3-4a2301f4a537fdf031350b2b0cb55419
  
  ### Bonus Question: What is the difference between a Service and a Resource?
  DD: 
  -A *service* is a group of processes \(queries, jobs, endpoints) that allow the creation of an application. \(i.e: The flask service in our examples)
  -A *resource* is a specific domain of an application \(single endpoint, single query) \(i.e: The specific request http://127.0.0.1:5050/api/trace from the example)

# Final Question:
  ### Is there anything creative you would use Datadog for? 
  DD: I could see a very practical use of collecting metrics from kid’s sceen time. There are applications that can calculate the amount of time spent on each app/device per   kids. A custom Agent check could aggregate all this data and show it on a single pane of glass, while highlighting anomalies and keeping track of the SLO the family has       agreed on.


