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



