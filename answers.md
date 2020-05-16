Your answers to the questions go here.
Below are the solutions for Michael Ahearn, yes I watched hackers way to many times as a kid and even though its terrible, but the handle stuck.
<h2>PART - 1 (Collecting metrics)</h2>
- Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog:


![](https://github.com/LordNykon/hiring-engineers/blob/solutions-engineer/Datadoghostmaptagging.jpg)


- Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Postgres was used for this exercise: (instructions for setup :https://www.datadoghq.com/blog/collect-postgresql-data-with-datadog/)

Log into postgres

```
sudo su - postgres
psql
```

User Creation: ##password removed for security
```
create user datadog with password '<PASSWORD>';
grant SELECT ON pg_stat_database to datadog;
grant pg_monitor to datadog
```


Verification Code:
```
psql -h localhost -U datadog postgres -c \ "select * from pg_stat_database LIMIT(1);" && echo -e "\e[0;32mPostgres connection - OK\e[0m" || \ || echo -e "\e[0;31mCannot connect to Postgres\e[0m"
```


Verification Output:
```
datid | datname  | numbackends | xact_commit | xact_rollback | blks_read | blks_hit | tup_returned | tup_fetched | tup_inserted | tup_updated | tup_deleted | conflicts | temp_files | temp_bytes | deadlocks | blk_read_time | blk_write_time |          stats_reset           datid | datname  | numbackends | xact_commit | xact_rollback | blks_read | blks_hit 
| tup_returned | tup_fetched | tup_inserted | tup_updated | tup_deleted | conflicts | temp_files | temp_bytes | deadlocks | blk_read_time | blk_write_time |          stats_reset
-------+----------+-------------+-------------+---------------+-----------+----------+--------------+-------------+--------------+-------------+-------------+-----------+------------+------------+-----------+---------------+----------------+-------------------------------
 13053 | postgres |           2 |        3020 |             1 |       206 |   149812 |      1262794 |       40560 |    
        0 |           0 |           0 |         0 |          0 |          0 |         0 |             0 |
0 | 2020-05-15 14:49:21.242781+00
(1 row)
```


- Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

my_metric.py
```
import random
try:
    from checks import AgentCheck
except ImportError:
    from datadog_checks.base import AgentCheck
__version__="1.0.0"
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge(
        "my_metric.gauge",
        random.randint(0, 1000))
```


my_metric.yaml
```
init_config:
instances:
        - min_collection_interval: 45
```


Bonus Question Can you change the collection interval without modifying the Python check file you created?
Yes you can update the collection interval by inside of the yaml file for the check in /etc/datadog-agent/conf.d/{checkname} in this cas e/etc/datadog-agent/conf.d/my_check.yaml

<h2>PART - 2 (Visualizing Data)</h2>

-Utilize the Datadog API to create a Timeboard that contains:

--Your custom metric scoped over your host.
--Any metric from the Integration on your Database with the anomaly function applied.
--Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Python script used to create the timeboard.

```
## I removed the API and APP keys from the documentation for security

from datadog import initialize, api
options = dict(api_key='<DD_API_KEY>', app_key='<DD_APP_KEY') 
initialize(**options)
title = "Michael Ahearn Dashboards"
description = "Dash/timeboard creation via api"
#my_metric
graphs = [
{
  "title": "My_Metrics Scoped over Host",
  "definition": {
  "requests": [
    {
      "q": "avg:my_metric.gauge{host:vagrant}",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "autoscale": "true",
  "viz": "timeseries"  }
},
#Postgres Anomoly
{
  "title": "Anomalies in Postgres: Average number of disk blocks read ",
  "definition": {
  "requests": [
    {
      "q": "anomalies(avg:postgresql.percent_usage_connections{*}, 'basic', 2)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "autoscale": "true",  "viz": "timeseries"
  }
},
#my_metic with rollup
{
  "title": "my_metric with rollup function",
  "definition": {
  "viz": "timeseries",
  "requests": [
    {
    "q": "avg:my_metric.gauge{*} by {host}.rollup(sum, 3600)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],      "aggregator": "sum"
    }
  ],
  "autoscale": "true"
  }
}]

api.Timeboard.create(title=title, description=description, graphs=graphs)
```
-Set the Timeboard's timeframe to the past 5 minutes
-Take a snapshot of this graph and use the @ notation to send it to yourself.

Drag To select custom time frame on dashboard:

![Optional Text](https://github.com/LordNykon/hiring-engineers/blob/solutions-engineer/images/dragtoselectcustomtime.jpg)

Select Send Snap shot

![Optional Text](https://github.com/LordNykon/hiring-engineers/blob/solutions-engineer/images/SendSnapShot.jpg)

@ The users you would like to notify

![Optional Text](https://github.com/LordNykon/hiring-engineers/blob/solutions-engineer/images/snapshotat5minterval.jpg)

Example of the Notification email:

![Optional Text](https://github.com/LordNykon/hiring-engineers/blob/solutions-engineer/images/Snapshotemail.jpg)


-Bonus Question: What is the Anomaly graph displaying?
As coded in my script with the Basic Option: The Algorithm uses a simple lagging rolling quantile computation to determine the range of expected values. It uses very little data and adjusts quickly to changing conditions but has no knowledge of seasonal behavior or longer trends.

Which in limited terms will flag any values that deviate from the normal operation of in this case the percent of connection usage in postgres ie if in a normally 10 percent of the connections are used and the algorithm determines that the acceptable range is 8-12 any number of percentage connections out side of that range will be flagged as an anomaly.


<h2>PART - 3 (Monitoring Data)</h2>

-Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

-Warning threshold of 500
-Alerting threshold of 800
-And also ensure that it will notify you if there is No Data for this query over the past 10m.

Parameters Used to create the Checks:


![Optional Text](https://github.com/LordNykon/hiring-engineers/blob/solutions-engineer/images/monitorcreation.jpg)


Warning Example:


![Optional Text](https://github.com/LordNykon/hiring-engineers/blob/solutions-engineer/Monitoring%20Alert%20wit%20value%20and%20IP.jpg)


-Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

Daily:


![Optional Text](https://github.com/LordNykon/hiring-engineers/blob/solutions-engineer/7pmdowntimealert.jpg)


Weekend:


![Optional Text](https://github.com/LordNykon/hiring-engineers/blob/solutions-engineer/Weekend%20Down%20time.jpg)


<h2>PART - 4 (Collecting APM Data:)</h2>

In the datadog.yaml I updated the following under Trace Collection Configuration

```
## Trace Collection Configuration ##
####################################

## @param apm_config - custom object - optional
## Enter specific configurations for your trace collection.
## Uncomment this parameter and the one below to enable them.
## See https://docs.datadoghq.com/agent/apm/
#
apm_config:

  ## @param enabled - boolean - optional - default: true
  ## Set to true to enable the APM Agent.
  #
  enabled: true

  ## @param env - string - optional - default: none
  ## The environment tag that Traces should be tagged with.
  ## If not set the value will be inherited, in order, from the top level
  ## "env" config option if set and then from the 'env:' tag if present in the
  ## 'tags' top level config option.
  #
  env: none

  ## @param receiver_port - integer - optional - default: 8126
  ## The port that the trace receiver should listen on.
  #
  receiver_port: 8126
```

Flask application used for generating APM data:

```
from flask import Flask
import logging
import sys
from ddtrace import tracer


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

The application was started using the following command

```
ddtrace-run python flask_app.py
```

A second terminal window was brought up and several request were run against that endpoint:

```
curl http://0.0.0.0:5050/
curl http://0.0.0.0:5050/api/apm
curl http://0.0.0.0:5050/api/trace
curl http://0.0.0.0:5050/api/apm
curl http://0.0.0.0:5050/api/
```
Dashboard Link:
https://app.datadoghq.com/dashboard/6tx-7nh-fpy/michael-ahearn-dashboards?from_ts=1589511126741&to_ts=1589597526741&live=true

Dashboard Screenshot:


![Optional Text](https://github.com/LordNykon/hiring-engineers/blob/solutions-engineer/Dashboard%20with%20APM%20.jpg)

-Bonus Question: What is the difference between a Service and a Resource?
While the formal definitions are below and even more verbose explanations can be found here (https://docs.datadoghq.com/tracing/visualization/) Services are made of a group of resources and the resources are the individual endpoint or query with in a service.

Services are the building blocks of modern microservice architectures - broadly a service groups together endpoints, queries, or jobs for the purposes of scaling instances.

Resources represent a particular domain of a customer application - they are typically an instrumented web endpoint, database query, or background job.


<h2>PART - 5 (Final Question:)</h2>

Is there anything creative you would use Datadog for?

I feel my answer is selfish given the global pandemic but, I have a passion for anything with an engine and wheels. I have been fortunate enough to endurance race a car at a major track and we did well.  The opportunity to add more sensors to the car and  to be able to aggregate, alert on, and monitor the health of the car in near real time on the track, would allow us to make much better decisions about what we are doing with the car. We could predict failure and prevent it and save time in the pits and be safer racers. I know professional teams have similar technology but to be able to bring it to an amateur level would be great and I would really like to try and find creative ways to solve these challenges with Datadog. 
