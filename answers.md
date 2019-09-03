# Introduction

Hello there! My name is Alex Gabrielian and I am applying for the Technical Account Manager role at Datadog.
As a part of my application, I was asked to complete the Solutions Engineer technical exercise which you will find below with both my code and the screenshots supporting my work.

# Setting up the environment

I decided to utilize the containerized approach with Docker for Linux.

First, I obtained my unique Datadog API key from the online user interface under Integrations > APIs > API Keys. Then, I ran the installation command to install a Datadog container on my local host which pulled a Docker image from Docker Hub and executed it to create the container. 

![Docker container](https://i.imgur.com/HBXYq9y.png)

Then, I set up my Datadog account through the [Datadog online portal](https://www.datadoghq.com/).

# Collecting metrics

First, I needed to get inside my Docker container to install basic components. All commands inside the dd-agent container were executed as `root` unless otherwise noted.

```
 docker exec -it dd-agent /bin/bash
 apt-get update 
apt-get install -y vim 
```

Then, I edited my Datadog agent configuration by adding my unique API key and a few custom tags to uniquely identify various systems in my infrastructure for easier troubleshooting and analyzing.

```
 vi /etc/datadog-agent/datadog.yaml 
```

![Adding API key to Datadog agent](https://i.imgur.com/yWlaDCE.png)

![Adding tags to Datadog agent](https://i.imgur.com/UewE9Nm.png)

Here is a screenshot of my Host Map page showing infrastructure and tags:

![Host Map](https://i.imgur.com/3cwR3Si.png)

## PostgreSQL

Next, I installed a PostgreSQL database to my host, gave Datadog read-only access to it, and configured my PostgreSQL configuration file to collect logs. 

### Installing and starting PostgreSQL

```
apt-get install -y postgresql
 service posgresql start
 su – postgres 
psql
```

### Preparing and making sure connection check is working

![Preparing PostgreSQL](https://i.imgur.com/0Y6CopP.png)

To start collecting logs, I needed to update database password from above, add tags, and update the logging path in the PostgreSQL configuration file.

```
vi /etc/datadog-agent/conf.d/postgres.d/conf.yaml
```

![PostgreSQL collecting logs](https://i.imgur.com/r2YXxuv.png)

Next, I needed to configure `/etc/postgresql/11/main/postgresql.conf` to enable log collection by adding the following parameters:

```
logging_collector = on
log_directory = 'pg_log'
log_filename = 'pg.log'
log_statement = 'all'
log_line_prefix= '%m [%p] %d %a %u %h %c '
log_file_mode = 0644
```

Additionally, collecting logs was disabled by default in the Datadog agent, so I needed to enable it in my `datadog.yaml` file by adding the following:

```
logs_enabled: true
```

Lastly, a restart of Datadog Docker agent to engage changes and check status.

```
docker exec -it dd-agent agent stop
docker start dd-agent
docker exec -it dd-agent /bin/bash
service postgresql start
exit
docker exec -it dd-agent agent status
```

![Postgres status](https://i.imgur.com/YerSBhm.png)

Here are the PostgreSQL metrics showing a healthy state:

![Postgres metrics shown](https://i.imgur.com/VU8gnxk.png)

## Create custom metric

First, I installed the Datadog API.

```
pip install datadog
```

Here are the steps to create a custom agent check that submits a metric named my_metric with a random value between 0 and 1000 and change your check's collection interval so that it only submits the metric once every 45 seconds.

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

Add the following code to change the check's collection interval so that it only submits the metric once every 45 seconds.

```
init_config:

instances:
  - min_collection_interval: 45
```

**Bonus question:** Can you change the collection interval without modifying the Python check file you created?

The collection interval can be modified in the configuration `.yaml` file, as I have done above.

# Visualizing data

Utilizing the Datadog API, I created a Timeboard which contains:

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

**Bonus question:** What is the Anomaly graph displaying?

The anomaly graph is displaying anomalies in your metric. You can apply the anomaly algorithm to your metrics to enable yourself to identify patterns which may be behaving outside of their normal behaviors, which are difficult to monitor with traditional threshold-based alerting. For example, building a service in your CI/CD platform will consume far more computing power during weekday business hours whereas in the evenings and weekends it will not be as high. Both are normal behaviors which normal threshold alerting will not be able to capture.

# Monitoring data

I created a metric monitor which watches the average of my_metric and sends out an alert email if it is above the following values over the past 5 minutes:
* Warning threshold of 500
* Alerting threshold of 800
* No data for the query over the past 10 minutes

Configure the monitor’s message so that it will:
* Send an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

![Metric monitor](https://i.imgur.com/X0p2RKB.png)

**Bonus question:** Downtimes

* One that silences it from 7pm to 9am daily on M-F.

![Weekday downtimes](https://i.imgur.com/5N9NHhL.png)

* And one that silences it all day on Sat-Sun.

![Weekend downtimes](https://i.imgur.com/LdyLNT5.png)

All email notifications:

![Email notifications](https://i.imgur.com/L8xORkj.png)

# Collecting APM data

In order to collect APM data, the first thing I needed to do is enable APM logging in the `datadog.yaml` file.

```
vi /etc/datadog-agent/datadog.yaml
```

![Enable APM logging](https://i.imgur.com/Jc1V4bC.png)

I installed the Agent:

![Installing APM agent](https://i.imgur.com/GkRevx1.png)

I installed the Pyton clients from inside the new container:

```
docker exec -it charming_sammet /bin/bash
pip install ddtrace
pip install flask
```

I executed the following `my_app.py` file with command `DD_TRACE_ANALYTICS_ENABLED=true ddtrace-run python my_app.py` to instrument:

```
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

From another terminal window, I stimulated the trace with a `curl` command:
```
curl localhost:5050/api/apm
curl localhost:5050/api/trace
```

Screenshot of APM:

![APM](https://i.imgur.com/QrsW0vi.png)

Screenshot of infrastructure metrics:

![Infrastructure metrics](https://i.imgur.com/Drei8gl.png)

**Bonus question:** What is the difference between a Service and a Resource?

Services are the building blocks of modern microservice architectures - broadly a service groups together endpoints, queries, or jobs for the purposes of scaling instances. For instance, a single webapp service and its backend database service.
Resources represent a particular domain of a customer application - they are typically an instrumented web endpoint, database query, or background job. For instance, in a database service, these would be database queries with the span name `db.query`.

# Final question

Is there anything creative you would use Datadog for?

After playing around with Datadog for the last week, I began to see how useful it can become when applied creatively. There seems to be an unlimited number of ways it can be used, it just takes a creative mind to use it in a way that refines our day-to-day choices and allows us to see data from a legible perspective. One example which comes to mind is the headache of finding parking in a busy city.

I have lived in the Los Angeles area for most of my life and one of the problems I face both during the weekdays and the weekends is finding street parking. The restriction signs are extremely difficult to comprehend. It is not uncommon to find yourself reading layers and layers of parking restrictions for time allowance, duration allowance, and the restrictions applied to certain types of vehicles.

Imagine if we created an application which took your GPS location, created an interactive map, and showed you where there is parking near you and, based on your search criteria, if you could park there with your type of car. Implementing this would require hardware installed on designated parking meters but with the right funding this could be done using Datadog’s monitoring capabilities. Furthermore, we could create anomaly tables which may even refine traffic monitoring used by services like Google Maps and Waze. For example, if there is a concert at the Hollywood Bowl one Saturday evening and all street parking spots within a 2 mile radius are taken, this can notify map users that traffic congestion will be higher than normal for that weekend.

The example I mentioned may be a little farfetched since it will require a collaboration with both the municipal bodies and the private companies willing to invest in something like this but it only takes a wild idea to start a snowball effect of betterment in the future.

# Thank you for your time

I hope you have made it this far in my exercise for the Technical Account Manager role and I look forward to presenting this material to you in person.