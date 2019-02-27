## Candidate: Masahiro Hattori

## Collecting Metrics:

* Adding tags in the Agent config file:

[Tags in Host Map page](images/sc001_tags.png)

at /etc/datadog-agent/datadog.yaml
```yaml
# Set the host's tags (optional)
tags:
  - env:trial
  - role:api
  - team:sre
```

* Installing MySQL and MySQL integration

Installing MySQL on the Host

```bash
sudo apt install mysql-server mysql-client
```

Installing MySQL integration

```bash
mysql> CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'Passw0rd';
Query OK, 0 rows affected (0.00 sec)

mysql> GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> GRANT PROCESS ON *.* TO 'datadog'@'localhost';
Query OK, 0 rows affected (0.00 sec)

mysql> show databases like 'performance_schema'
    -> ;
+-------------------------------+
| Database (performance_schema) |
+-------------------------------+
| performance_schema            |
+-------------------------------+
1 row in set (0.00 sec)

mysql> GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';
Query OK, 0 rows affected (0.01 sec)
```
/etc/datadog-agent/conf.d/mysql.d/conf.yaml
```bash
instances:
  - server: localhost
    user: datadog
    pass: Passw0rd
    port: 3306             # Optional
    # sock: /path/to/sock    # Connect via Unix Socket
    # defaults_file: my.cnf  # Alternate configuration mechanism
    # connect_timeout: None  # Optional integer seconds
    tags:                  # Optional
      - placement:local
    options:               # Optional
    replication: 0
    #   replication_channel: channel_1  # If using multiple sources, the channel
 name to monitor
    #   replication_non_blocking_status: false  # grab slave count in non-blocki
ng manner (req. performance_schema)
    galera_cluster: 1
    extra_status_metrics: true
    extra_innodb_metrics: true
    extra_performance_metrics: true
    schema_size_metrics: false
    disable_innodb_metrics: false
```
sudo datadog-agent status
```bash

 mysql (1.5.0)
 -------------
   Instance ID: mysql:667066b4239d96b6 [OK]
   Total Runs: 1
   Metric Samples: Last Run: 60, Total: 60
   Events: Last Run: 0, Total: 0
   Service Checks: Last Run: 1, Total: 1
   Average Execution Time : 58ms
```

[MySQL Dashboard](images/sc002_mysql-dash.png)

* Creating a custom Agent check

/etc/datadog-agent/conf.d/my_metric.yaml
```bash
init_config:

instances: [{}]
````

/etc/datadog-agent/checks.d/my_metric.py
```bash
try:
    from checks import AgentCheck
    import random
except ImportError:
    from datadog_checks.checks import AgentCheck

__version__ = "1.0.0"

class MyMetric(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.uniform(0, 1000))
```

```bash
vagrant@ubuntu:~$ sudo -u dd-agent -- datadog-agent check my_metric
=== Series ===
{
  "series": [
    {
      "metric": "datadog.agent.check_ready",
      "points": [
        [
          1551214201,
          1
        ]
      ],
      "tags": [
        "agent_version_major:6",
        "agent_version_minor:9",
        "check_name:my_metric",
        "status:ready"
      ],
      "host": "ubuntu",
      "type": "gauge",
      "interval": 0,
      "source_type_name": "System"
    },
    {
      "metric": "my_metric",
      "points": [
        [
          1551214201,
          827.7088623046875
        ]
      ],
      "tags": null,
      "host": "ubuntu",
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

    my_metric (1.0.0)
    -----------------
      Instance ID: my_metric:d884b5186b651429 [OK]
      Total Runs: 1
      Metric Samples: Last Run: 1, Total: 1
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 0, Total: 0
      Average Execution Time : 0s
```

[Metrics Explorer](images/sc003_my_metric.png)

* Changing my_metric interval as 45 sec.

/etc/datadog-agent/conf.d/my_metric.yaml
```bash
init_config:

instances:
  - min_collection_interval: 45
```
[Metrics Explorer](images/sc004_my_metric_45s.png)

* **Bonus Question** "Can you change the collection interval without modifying the Python check file you created?"

Definitely, YES. You can modify the collection interval at the configuration file named my_metric.yaml, not need to modify your python check file itself.

## Visualizing Data:

* Utilizing the Datadog API to create a Timeboard

[My Timeboard](images/sc005_my_timeboard.png)

```bash
#!/bin/bash

api_key=$DD_API_KEY
app_key=$DD_APP_KEY

curl  -X POST -H "Content-type: application/json" \
-d '{
      "title" : "My Timeboard",
      "widgets" : [
      {
          "definition": {
              "type": "timeseries",
              "requests": [
                  {"q": "avg:my_metric{host:ubuntu}"}
              ],
              "title": "my_metric over a host"
          }
      },
      {
          "definition": {
              "type": "timeseries",
              "requests": [
                  {"q": "anomalies(avg:mysql.net.connections{*}, '\''basic'\'', 5)"}
              ],
              "title": "Anomaly Detection on MySQL connections"
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
                ],
                "title": "Rolled up my_metrics"
            }
        }
        ],
        "layout_type": "ordered",
        "description" : "A dashboard with memory info.",
        "is_read_only": true,
        "notify_list": ["user@domain.com"],
        "template_variables": [{
            "name": "host1",
            "prefix": "host",
            "default": "my-host"
        }]
  }' \
  "https://api.datadoghq.com/api/v1/dashboard?api_key=${api_key}&application_key=${app_key}"
```

* Accessing the Dashboard

[My Timeboard set timeframe as 5min.](images/sc006_my_timeboard_5min.png)

[Snapshot and @mention in Datadog](images/sc007_snapshot_in_timeboard.png)

[E-mail notification sent via @mention](images/sc008_e-mail_notification.png)

* **Bonus Question** "What is the Anomaly graph displaying?"

Although Anomaly Detection can help to find seasonal behavior in metrics and see what is normal and/or not, \
Anomaly detection for mysql.net.connections in the dashboard above shows no pattern has been found in the metrics.

## Monitoring Data:

* Creating a new Metric Monitor for **my_metric**

[Setting up Metric Monitor -1](images/sc009_threshold.png)

[Setting up Metric Monitor -2](images/sc010_message-body.png)

[Triggered Alert E-mail](images/sc011_triggered-alert.png)

* **Bonus Question** "How to set scheduled downtimes for the Metric Monitor above?"

[Setting up two scheduled downtimes -Out of Office in weekdays](images/sc012_downtime-outofoffice.png)

[Setting up two scheduled downtimes -Weekend](images/sc013_downtime-weekend.png)

## Collecting APM Data:

* my_flaskapp.py ( Nothing changed though )

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

* [Shared Dashboard](https://p.datadoghq.com/sb/7k6umrascfdhy0wn-3c2249d1226d1590b27d4bf09a753b0a)

[My Screenboard](images/sc014_MyScreenboard.png)

* **Bonus Question**: "What is the difference between a Service and a Resource?"

While a Service represents a role that set of process are grouped on, a Resource represents specific action in the Service.

## Final Question:

* Is there anything creative you would use Datadog for?

To achieve my ideal bed room environment, not hot/cold, good humidity, less CO2 and dust, with those metrics dynamically optimized.
Now my bed room has been equipped with air purifier, humidifier, air-conditioner　and additional heating appliance working fully separately.
Those metrics in bed room is really dynamically changing. It would be fun to monitor and manage those. 
