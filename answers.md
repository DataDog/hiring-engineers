## Prerequisites
#### Agent installed on centos linux / AWS using command listed below

```DD_API_KEY=[KEY] bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"}```

## Collecting Metrics
#### Arbitrary tags added to /etc/datadog-agent/datadog.yaml file

![tags](https://github.com/DanCardno/edbinstall/blob/master/images/tags.png)

#### Postgres (deliberate older version) installed and user added / permisisons granted and connection added in /etc/datadog-agent/conf.d/postgres.d/conf.yaml

![postgrestest](https://github.com/DanCardno/edbinstall/blob/master/images/postgres%20connection.png)

#### Created custom agent check

Custom agent check comes in two sections

| File | Location | Description |
| ------ | ----------- | ----- |
| my_metric.yaml   | /etc/datadog-agent/conf.d | configuration parameters for custom check |
| my_metric.py | /etc/datadog-agent/checks.d | script for execution |

**.yaml example (default)**

    init_config:
    
    instances:
    [{}]


**.py example**

``` python
import random
# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from old versions of the Agent...
    from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

class my_metric(AgentCheck):
    def check(self, instance):
        value = random.randint(0,1000)
        self.gauge('my_metric', value)

};
```
**.yaml example (with collection interval adjusted)**

    init_config:

    instances:
      - min_collection_interval: 45

## Visualizing Data
**API Script used to**
+ Create dashboard
+ Track Anomolies
+ Roll up data

**note** python libraries added using **pip install datadog** python command

```python

from datadog import initialize, api

options = {
    'api_key': 'e0b9616712c333cd8454e05d72ceb162',
    'app_key': '8eba3e0bb155f09517acc5a0fbead774dbf6b63e'
}

initialize(**options)

title = 'Cardno Dashboard'
widgets = [
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{*}'}
        ],
        'title': 'Random Numbers'
                      }
},
{
    'definition': {
        'type': 'timeseries',
        'requests': [
        { "q": "anomalies(avg:system.cpu.user{*}, 'basic', 5)"}
        ],
        'title': 'CPU Anomalies'
                      }
},
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {"q": "sum:my_metric{*}.rollup(sum, 3600)"}
        ],
        'title': 'MyMetric Rollup'
                      }
}
]
layout_type = 'ordered'
description = 'A dashboard with random info.'
is_read_only = True
notify_list = ['dancardno@hotmail.com']
template_variables = [{
    'name': 'host1',
    'prefix': 'host',
    'default': 'CardnoDemoMachineAWS'
}]
api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables)


```
#### Timeboard set to the last 5 minutes

![5minInterval](https://github.com/DanCardno/edbinstall/blob/master/images/5mins.png)

#### Metric snapshot sent directly to user

![Tagged Snapshot](https://github.com/DanCardno/edbinstall/blob/master/images/TaggedSnapshot.png)

#### What are anomolies

In the area of performance monitoring, identifying anomolies can be incrediby useful. 

For example, it helps to identify any deviation from standard patterns of usage, especially over longer periods of time, which may indicate an issue with the system rather than standard 'seasonal' consumption. It's often the case that workload is expected to be higher at certain times and we wouldn't want to trigger alerts and raise alarms over the hard coded alert values; by monitoring the deviation we can assess if the metric is above the the normal patterns of usage.


## Monitoring Data
#### Metric Monitor
Used to identify where metric exceeds thresholds for the purpose of alerting

![MetricMonitor](https://github.com/DanCardno/edbinstall/blob/master/images/metric_monitor.png)

#### Individual responses for different alerts

![Alerts](https://github.com/DanCardno/edbinstall/blob/master/images/alert_messages.png)

![email alert](https://github.com/DanCardno/edbinstall/blob/master/images/emailed_alert.png)

#### Bonus Data - Downtime

Evening Exeptions: prevents alerts being sent between the hours of 7PM and 9AM

![DailyDowntime](https://github.com/DanCardno/edbinstall/blob/master/images/daily_downtime.png)

Weekends: Silences alerts for weekends

![Weekend Downtime](https://github.com/DanCardno/edbinstall/blob/master/images/weekend_downtime.png)


Downtime Notification

![UTC Notification](https://github.com/DanCardno/edbinstall/blob/master/images/downtime_email_received.png)



## Collecting APM Data

#### Resource Started
![ddtracerunning](https://github.com/DanCardno/edbinstall/blob/master/images/ddtrace_running.png)

#### APM Metric Charts

![APM Overview](https://github.com/DanCardno/edbinstall/blob/master/images/apm%20home.png)

#### Public URL to APM and KPI Data
https://p.datadoghq.com/sb/9dr2wubjyonk8d48-c1a733e80456a35ae9b248c6cb0ac9a2

![APM Combined](https://github.com/DanCardno/edbinstall/blob/master/images/apm_combined.png)


#### Bonus Info Conundrum

q: What is the difference between a service and resource?

a: Generally speaking, a service is a set of processes that do the same job, such as a web server, whereas a resource is a specific action for a service for example, a URL in a webservice or a query from a DB Server.


## Final Question

Creative uses of datadog could extend to 

* Security
   - By monitoring for suspiciously high connections to a secure database
   - Ensuring MSSQL servers don't run out of disk space
* Efficiency
  - With the rise of automation, sensors for temperature / environmental changes can be monitored in the office / home / transportation
  - Identifying which servers via load balancers are utilized
* Performace 
  - Track performance telemetry for motorsport
* Health
  - Log and monitor patient metrics in cardiac cases
  


