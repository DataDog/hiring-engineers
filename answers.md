## Prerequisites - Setup the environment

You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

* You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. [Here are instructions](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#vagrant) for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum `v. 16.04` to avoid dependency issues.
```bash
# set up playground
$ mkdir Datadog_Hiring_Exercise
$ cd Datadog_Hiring_Exercise

# spin up an Ubuntu box
$ vagrant box add ubuntu/xenial64
$ vagrant init ubuntu/xenial64
$ vagrant up
```
* ~~You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.~~

Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.
```bash
# enter box
$ vagrant ssh
Welcome to Ubuntu 16.04.5 LTS (GNU/Linux 4.4.0-139-generic x86_64)

# install agent
$ DD_API_KEY=************************************ bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/data
dog-agent/master/cmd/agent/install_script.sh)"
```

##### Expected Outcome: Events Page
###### [https://app.datadoghq.com/event/stream](https://app.datadoghq.com/event/stream)
&NewLine;
![Events Page](/screenshots/1_events_page_outcome.png)

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
```bash
# in Ubuntu
$ sudo nano /etc/datadog-agent/datadog.yaml

# add tags to datadog.yaml
tags:
- env:local
- role:database
```
##### Expected Outcome: Host Map Page
###### [https://app.datadoghq.com/infrastructure/map](https://app.datadoghq.com/infrastructure/map)
&NewLine;
![Host Map Page](/screenshots/5_host_map_page.png)
* Install a database on your machine (~~MongoDB~~, MySQL, ~~or PostgreSQL~~) and then install the respective Datadog integration for that database.
```bash
# install mysql-server
$ sudo apt-get update
$ sudo apt-get install mysql-server

# log in as root
$ mysql -u root -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 31
Server version: 5.7.24-0ubuntu0.16.04.1 (Ubuntu)

# create user with replication rights
mysql> CREATE USER 'datadog'@'localhost' IDENTIFIED BY '************************';
Query OK, 0 rows affected (0.00 sec)
mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.00 sec)
mysql> GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
Query OK, 0 rows affected, 1 warning (0.00 sec)

# get full metrics catalog
mysql> GRANT PROCESS ON *.* TO 'datadog'@'localhost';
Query OK, 0 rows affected (0.00 sec)
mysql> GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';
Query OK, 0 rows affected (0.00 sec)

# create and open mysql.yaml
$ sudo nano /etc/datadog-agent/conf.d/mysql.yaml

# edit mysql.yaml
init_config:

instances:
  - server: localhost
    user: datadog
    pass: ************************
    options:
      replication: 0
      galera_cluster: 1
      extra_status_metrics: true
      extra_innodb_metrics: true
      extra_performance_metrics: true
      schema_size_metrics: false
      disable_innodb_metrics: false

# restart agent
$ sudo service datadog-agent restart

# check mysql
$ sudo -u dd-agent -- datadog-agent check mysql

# expected outcome
=========
Collector
=========

  Running Checks
  ==============

    mysql (1.4.0)
    -------------
        Instance ID: mysql:183e873ec04d0018 [OK]
        Total Runs: 1
        Metric Samples: 60, Total: 60
        Events: 0, Total: 0
        Service Checks: 1, Total: 1
        Average Execution Time : 27ms
```

##### Expected Outcome: MySQL Integrations Page
###### [https://app.datadoghq.com/account/settings#integrations/mysql](https://app.datadoghq.com/account/settings#integrations/mysql)
![MySQL Integrations Page](/screenshots/2_mysql_integrations_page.png)

##### Expected Outcome: MySQL Overview Page
###### [https://app.datadoghq.com/dash/integration/12/mysql---overview](https://app.datadoghq.com/dash/integration/12/mysql---overview)
![MySQL Overview Page](/screenshots/3_mysql_overview_page.png)

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
```bash
# create my_metric.yaml file
$ cd /etc/datadog-agent/conf.d
$ sudo nano my_metric.yaml

# edit my_metric.yaml file
init_config:

instances: [{}]

# create my_metric.py file
$ cd /etc/datadog-agent/checks.d
$ sudo nano my_metric.py

# edit my_metric.py file
try:
    from checks import AgentCheck
except ImportError:
    from datadog_checks.checks import AgentCheck

from random import randint

__version__ = "1.0.0"

class MyMetric(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(0, 1000))
```
* Change your check's collection interval so that it only submits the metric once every 45 seconds.
```bash
# edit my_metric.yaml file
init_config:

instances:
    - min_collection_interval: 45
```

##### Expected Outcome: Metrics Explorer Page
###### [https://app.datadoghq.com/metric/explorer](https://app.datadoghq.com/metric/explorer)
&NewLine;
![Metrics Explorer Page](/screenshots/4_metrics_explorer_page.png)
* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?
```
Yes. You can edit the yaml file associated with the Python check file.
```

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

##### Postman JSON Script:
&NewLine;
```json
{
    "graphs": [
        {
            "title": "My Metric",
            "definition": {
                "viz": "timeseries",
                "requests": [
                    {
                        "q": "my_metric{host:ubuntu-xenial}"
                    }
                ],
                "events": []
            }
        },
        {
            "title": "Anomalized MySQL Queries",
            "definition": {
                "viz": "timeseries",
                "requests": [
                    {
                        "q": "anomalies(avg:mysql.performance.queries{*}, 'basic', 2)"
                    }
                ],
                "events": []
            }
        },
        {
            "title": "Custom Metric with Rollup Function",
            "definition": {
                "viz": "timeseries",
                "requests": [
                    {
                        "q": "my_metric{*}.rollup(sum, 3600)"
                    }
                ],
                "events": []
            }
        }
    ],
    "title": "My Timeboard",
    "description": "An informative timeboard.",
    "template_variables": [
        {
            "name": "scope",
            "prefix": "host",
            "default": "*"
        }
    ],
    "read_only": "True"
}
```
&NewLine;
##### Postman Setup:
![Postman Setup](/screenshots/6a_my_timeboard_postman_setup.png)

#### Postman Screenshot:
![Postman Screenshot](/screenshots/6b_my_timeboard_postman.png)

##### Expected Outcome: Dashboard List Page
###### [https://app.datadoghq.com/dashboard/lists](https://app.datadoghq.com/dashboard/lists)
&NewLine;
![Dashboard List Page](/screenshots/6_dahsboard_list_page.png)

##### Expected Outcome: My Timeboard Page (Show: The Past Hour)
###### [https://app.datadoghq.com/dash/1006369/my-timeboard](https://app.datadoghq.com/dash/1006369/my-timeboard)
&NewLine;
![My Timeboard Page](/screenshots/7a_my_timeboard_page_past_hour.png)

##### Expected Outcome: My Timeboard Page (Show: The Past 2 Days)
###### [https://app.datadoghq.com/dash/1006369/my-timeboard](https://app.datadoghq.com/dash/1006369/my-timeboard)
&NewLine;
![My Timeboard Page](/screenshots/7_my_timeboard_page.png)

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
&NewLine;
![My Timeboard - Past 5 Minutes](/screenshots/8_my_timeboard_5_mins.png)
* Take a snapshot of this graph and use the @ notation to send it to yourself.
##### My Timeboard: My Metric Graph Snapshot with Recipient and Corresponding Email Notification:
&NewLine;
![My Metric Graph Snapshot with Recipient](/screenshots/9_snapshot_my_metric.png)
&NewLine;
![My Metric Graph Snapshot Email Notification](/screenshots/9a_email_snapshot_my_metric.png)
&NewLine;
##### My Timeboard: Anomalized MySQL Queries Graph Snapshot with Recipient and Corresponding Email Notification:
&NewLine;
![Anomalized MySQL Queries Graph Snapshot with Recipient](/screenshots/10_snapshot_anomalized_mysql_queries.png)
&NewLine;
![Anomalized MySQL Queries Graph Snapshot Email Notification](/screenshots/10a_email_snapshot_anomalized_mysql_queries.png)
&NewLine;
##### My Timeboard: Custom Metric with Rollup Function Graph Snapshot with Recipient and Corresponding Email Notification:
&NewLine;
![Custom Metric with Rollup Function Graph Snapshot with Recipient](/screenshots/11_snapshot_custom_metric_with_rollup_function.png)
&NewLine;
![Custom Metric with Rollup Function Graph Snapshot Email Notification](/screenshots/11a_email_snapshot_custom_metric_with_rollup_function.png)
* **Bonus Question**: What is the Anomaly graph displaying?
```
The anomaly graph displays grayed-out boundaries and renders an anomaly in red when it is detected by the algorithm.
```

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.
&NewLine;
![New Metric Monitor](/screenshots/12_my_metric_monitor_threshold.png)
Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
&NewLine;
##### Code Snippet for Metric Monitor Messages
&NewLine;
```
{{#is_alert}}
Your metric is equal to or above the alert threshold!
Host IP: {{host.ip}}
Value: {{value}}
{{/is_alert}}

{{#is_warning}}
Your metric is equal to or above the warning threshold!
{{/is_warning}}

{{#is_no_data}}
There has been no data for my_metric over the past 10 minutes.
{{/is_no_data}}  @g.a.salamat@gmail.com
```
##### My Metric Monitor Messages and Notification
![My Metric Monitor Messages and Notification](/screenshots/14_my_metric_monitor_email_messages.png)
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.
&NewLine;
![My Metric Monitor Email Notification](/screenshots/13_my_metric_monitor_warn_email.png)

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  ![Downtime M-F Part1](/screenshots/20_downtime_mf.png)
  ![Downtime M-F Part2](/screenshots/20a_downtime_mf.png)
  * And one that silences it all day on Sat-Sun.
  ![Downtime Sat-Sun Part1](/screenshots/21_downtime_ss.png)
  ![Downtime Sat-Sun Part2](/screenshots/21a_downtime_ss.png)
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
  ![Email Notification for Downtime M-F](/screenshots/20b_downtime_mf.png)
  ![Email Notification for Downtime Sat-Sun](/screenshots/21b_downtime_ss.png)

## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

```python
from flask import Flask
import logging
import sys

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

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

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

```bash
# edit datadog.yaml file
$ sudo nano /etc/datadog-agent/datadog.yaml

# edit apm_config in datadog.yaml file
apm_config:
  enabled: true
```

```bash
# VAGRANT SESSION 1
# install ddtrace and flask
$ pip install ddtrace
$ pip install flask

# create my_app.py and paste Flask app code
$ sudo nano my_app.py

# run my_app.py
$ ddtrace-run python my_app.py
```

```bash
# VAGRANT SESSION 2
# create and run flask_requests.py to hit endpoints
$ sudo nano flask_requests.py
$ python flask_requests.py
```

##### Script for flask_requests.py:
&NewLine;
```python
import requests
import time

url = 'http://0.0.0.0:5050/'

def get_main():
  r = requests.get(url)
  print(r.content)
  return r.content

def get_api_apm():
  r = requests.get(url + 'api/apm')
  print(r.content)
  return r.content

def get_api_trace():
  r = requests.get(url + 'api/trace')
  print(r.content)
  return r.content

if __name__ == '__main__':
  get_main()
  time.sleep(5)
  get_api_apm()
  time.sleep(5)
  get_api_trace()
```

##### Screenshot of 2 Vagrant Sessions:
![Screenshot of 2 Vagrant Sessions](/screenshots/19_terminal_vagrant_sessions.png)

##### Expected Outcome: APM Services Page
###### [https://app.datadoghq.com/apm/services](https://app.datadoghq.com/apm/services)
&NewLine;
![APM Services Page](/screenshots/15_apm_services_page.png)

##### Expected Outcome: APM Services: Flask Page
###### [https://app.datadoghq.com/apm/service/flask/flask.request](https://app.datadoghq.com/apm/service/flask/flask.request)
&NewLine;
![APM Services: Flask Page](/screenshots/16_apm_services_flask_page.png)

##### Expected Outcome: APM Trace List Page
###### [https://app.datadoghq.com/apm/traces](https://app.datadoghq.com/apm/traces)
&NewLine;
![APM Trace List Page](/screenshots/17_apm_trace_list.png)

* **Bonus Question**: What is the difference between a Service and a Resource?
```
A service is a group of processes that have the same function. Resources are associated with services and are
specific actions for a service.
```

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
##### Dashboard with APM and Infrastructure Metrics
&NewLine;
![Dashboard with APM and Infrastructure Metrics](/screenshots/18_dashboard_apm_infrastructure_metrics.png)

Please include your fully instrumented app in your submission, as well.

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

```
As a former band member whose band released an album on Spotify, I would use Datadog on Spotify to gain more
exposure. The way I would do this is to monitor users who listen to the genre of music my band's album belongs
to and monitor the podcasts they listen to, then find correlations between the two.

I would then contact the creators of those podcasts and ask them to make one of our album's songs their feature
song for a certain episode. This way, my band will gain more exposure by reaching the right audience.
```
