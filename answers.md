# Introduction

Hello there! My name is Alex Gabrielian and I am applying for the Technical Account Manager role at Datadog.
As a part of my application, I was asked to complete the Solutions Engineer technical exercise which you will find below with both my code and the screenshots supporting my work.

# Setting up the environment

I decided to utilize the containerized approach with Docker for Linux.
After creating a Datadog account, I obtained my unique Datadog API key from the online User Interface (UI). Then, I ran the installation command to install a Datadog container on my local host which pulled a Docker image from Docker hub and ran it to create the container. 

![Docker container](https://i.imgur.com/HBXYq9y.png)

# Collecting metrics

First, I need to execute my docker container to install basic components. All commands inside the dd-agent container will be executed as root unless otherwise noted.

```
 docker exec -it dd-agent /bin/bash
 apt-get update 
apt-get install -y vim 
```

Now I edit my Datadog agent configuration by adding my unique API key and a few custom tags to uniquely identify various systems in my infrastructure for easier troubleshooting and analyzing.

```
 vi /etc/datadog-agent/datadog.yaml 
```

![Adding API key to Datadog agent](https://i.imgur.com/yWlaDCE.png)

![Adding tags to Datadog agent](https://i.imgur.com/UewE9Nm.png)

## PostgreSQL

Next, I will install a PostgreSQL database to my host, give Datadog read-only access to it, and configure my PostgreSQL configuration file to collect logs. 

### Installing and starting PostgreSQL

```
apt-get install -y postgresql
 service posgresql start
 su – postgres psql
```

### Preparing and making sure connection check is working

![Preparing PostgreSQL](https://i.imgur.com/0Y6CopP.png)

To start collecting logs, update database password from above, add tags, and update logging path.

```
vi /etc/datadog-agent/conf.d/postgres.d/conf.yaml
```

![PostgreSQL collecting logs](https://i.imgur.com/r2YXxuv.png)

Edit your PostgreSQL configuration file /etc/postgresql/<version>/main/postgresql.conf and add the following parameters.

```
logging_collector = on
log_directory = 'pg_log'
log_filename = 'pg.log'
log_statement = 'all'
log_line_prefix= '%m [%p] %d %a %u %h %c '
log_file_mode = 0644
```

Collecting logs is disabled by default in the Datadog agent, enable it in your datadog.yaml file by adding the following.

```
logs_enabled: true
```

Restart Datadog Docker agent to engage changes and check status.

```
docker exec -it dd-agent agent stop
docker start dd-agent
docker exec -it dd-agent /bin/bash
service postgresql start
exit
docker exec -it dd-agent agent status
```

![Postgres status](https://i.imgur.com/YerSBhm.png)

Postgres metrics shown

![Postgres metrics shown](https://i.imgur.com/VU8gnxk.png)

## Create custom metric

First install the Datadog API

```
pip install datadog
```

Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000 and change your check's collection interval so that it only submits the metric once every 45 seconds.

```
vi /etc/datadog-agent/checks.d/custom_my_metric.py
```

Add the following code:

```
from checks import AgentCheck
from random import randint


class MyMetricCheck(AgentCheck):
    def check(self, instance):
        random_number = randint(0, 1000)
        self.gauge('my_metric', random_number, tags=['metric:my_metric'])
```

Create the corresponding configuration file.

```
vi /etc/datadog-agent/conf.d/custom_my_metric.yaml
```

Add the following code to change your check's collection interval so that it only submits the metric once every 45 seconds.

```
init_config:

instances:
  - min_collection_interval: 45
```

Bonus question: Can you change the collection interval without modifying the Python check file you created?
The collection interval can be modified in the configuration .yaml file, as I have done above.

# Visualizing data

Utilizing the Datadog API, I have created a Dashboard which contains:

* my_metric scoped over my host.
* Max connections metric from the integration on PostgreSQL with the anomaly function applied.
* my_metric with the rollup function applied to sum up all the points for the past hour into one bucket.

```
from datadog import initialize, api

options = {
    'api_key': 'xxxxxxxxxxxxxxxxxx',
    'app_key': 'xxxxxxxxxxxxxxxxxx'
}

initialize(**options)

title = 'My timeboard'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{*}'}
        ],
        'title': 'my_metric values'
    }
},
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': "anomalies(avg:postgresql.max_connections{*}, 'basic', 3, direction='above', alert_window='last_5m', interval=20, count_default_zero='true')"}
        ],
        'title': 'PostgreSQL maximum number of client connections allowed'
    }
},
    {
    'definition': {
        'type': 'query_value',
        'requests': [
            {'q': "avg:my_metric{*}.rollup(sum, 3600)"}
        ],
        'title': 'my_metric sum of all points in the past hour'
    }
}]

layout_type = 'ordered'
description = 'My timeboard for the Technical Account Manager exercise'
is_read_only = True
notify_list = ['user@domain.com']
template_variables = [{
    'name': 'host1',
    'prefix': 'host',
    'default': 'docker-desktop'
}]

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables)

```

Screen capture after executing the Python code above.

![The Ultimate Dashboard](https://i.imgur.com/yChUZH9.png)

Setting the Timeboard's timeframe to the past 5 minutes and sending a snapshot to myself.

![Check out this killer metric!!](https://i.imgur.com/byVN7Iw.png)
![Email received](https://i.imgur.com/IpFfD6O.png)

Bonus Question: What is the Anomaly graph displaying?

The anomaly graph is displaying anomalies in your metric. You can apply the anomaly algorithm to your metrics to enable yourself to identify patters that may be behaving outside of its normal behavior, which are difficult to monitor with traditional threshold-based alerting. For example, building a service in your CI/CD platform will consume far more computing power during weekday business hours whereas in the evenings and weekends it will not be as high. Both are normal behaviors which normal threshold alerting will not be able to capture.

# Monitoring data

Next, I will create a metric monitor which watches the average of my_metric and send out an alert email if it is above the following values over the past 5 minutes:
* Warning threshold of 500
* Alerting threshold of 800
* No data for the query over the past 10 minutes

![Metric monitor](https://i.imgur.com/X0p2RKB.png)

Configuring the monitor’s message so that it will:
* Send me an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

Downtimes:
* One that silences it from 7pm to 9am daily on M-F.

![Weekday downtimes](https://i.imgur.com/5N9NHhL.png)

* And one that silences it all day on Sat-Sun.

![Weekend downtimes](https://i.imgur.com/LdyLNT5.png)

All email notifications:

![Email notifications](https://i.imgur.com/L8xORkj.png)

# Collecting APM data

In order to collect APM data, the first thing I need to do is enable apm_logging in the datadog.yaml file.

```
vi /etc/datadog-agent/datadog.yaml
```

![Enable APM logging](https://i.imgur.com/Jc1V4bC.png)