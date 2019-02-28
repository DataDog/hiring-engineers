

## Collecting Metrics:

_* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.*_

First I included this configuration

```bash
[root@centos7 ~]# grep -A 5 ^tags /etc/datadog-agent/datadog.yaml 
tags: 
 - recruiting 
 - env:test 
 - role:database
```

Then I restarted the agent
 
```bash
[root@centos7 ~]# systemctl restart datadog-agent
```

![alt text](https://github.com/luisarizmendi/hiring-engineers/raw/master/images/tag.png "Tags")





_* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database._


After installing mysql server on my centos7, I added datadog user and grant access:

```bash
[larizmen@centos7 ~]$ sudo mysql -e "CREATE USER 'datadog'@'localhost' IDENTIFIED BY 'D5I-LEIiWP1pdFxWE7wlj068';" 
[larizmen@centos7 ~]$ sudo mysql -e "GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;" 
[larizmen@centos7 ~]$ sudo mysql -e "GRANT PROCESS ON *.* TO 'datadog'@'localhost';" 
[larizmen@centos7 ~]$ sudo mysql -e "GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';"
```

Then changed the configuration:

```bash
[root@centos7 ~]# cat /etc/datadog-agent/conf.d/mysql.d/conf.yaml    
init_config: 

instances: 
 - server: localhost 
   user: datadog 
   pass: D5I-LEIiWP1pdFxWE7wlj068 
   tags: 
       - optional_tag1 
       - optional_tag2 
   options: 
     replication: 0 
     galera_cluster: 1
```

And finally restarted the agent:

```bash
[larizmen@centos7 ~]$ sudo systemctl restart datadog-agent
```

This is the dashboard:

![alt text](https://github.com/luisarizmendi/hiring-engineers/raw/master/images/database.png "database")






_* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000._

First I created the config yaml file with this contents:

```bash
[larizmen@centos7 ~]$ cat /etc/datadog-agent/conf.d/my_metric.yaml        
instances: [{}] 
```

and the python script:


```bash
[larizmen@centos7 ~]$ cat /etc/datadog-agent/checks.d/my_metric.py     
from datadog_checks.checks import AgentCheck 
from random import randint 
__version__ = "1.0.0" 


class MyCheck(AgentCheck): 
   def check(self, instance): 
       randval = randint(1, 1000) 
       self.gauge('my_metric', randval)
```

Then, restarted the agent:

```bash
[larizmen@centos7 ~]$ sudo systemctl restart datadog-agent
```


I checked that script does not have any issue:

```bash
[larizmen@centos7 ~]$ sudo -u dd-agent -- datadog-agent check my_metric --check-rate 
=== Series === 
{ 
 "series": [ 
   { 
     "metric": "datadog.agent.check_ready", 
     "points": [ 
       [ 
         1551355210, 
         0 
       ] 
     ], 
     "tags": [ 
       "agent_version_major:6", 
       "agent_version_minor:9", 
       "check_name:my_metric", 
       "status:unknown" 
     ], 
     "host": "centos7.localdomain", 
     "type": "gauge", 
     "interval": 0, 
     "source_type_name": "System" 
   }, 
   { 
     "metric": "my_metric", 
     "points": [ 
       [ 
         1551355210, 
         200 
       ] 
     ], 
     "tags": null, 
     "host": "centos7.localdomain", 
     "type": "gauge", 
     "interval": 0, 
     "source_type_name": "System" 
   }, 
   { 
     "metric": "my_metric", 
     "points": [ 
       [ 
         1551355211, 
         854 
       ] 
     ], 
     "tags": null, 
     "host": "centos7.localdomain", 
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
     Total Runs: 2 
     Metric Samples: Last Run: 1, Total: 2 
     Events: Last Run: 0, Total: 0 
     Service Checks: Last Run: 0, Total: 0 
     Average Execution Time : 0s
```



_* Change your check's collection interval so that it only submits the metric once every 45 seconds._

Taking a look to the graph we can see that the default interval is 15 seconds:

![alt text](https://github.com/luisarizmendi/hiring-engineers/raw/master/images/collection-default.png "15s")


This can be changed including the following configuration:

```bash
[larizmen@centos7 ~]$ cat /etc/datadog-agent/conf.d/my_metric.yaml     
init_config: 

instances: 
 - min_collection_interval: 45
```

A restart of the datadog agent is needed:

```bash
[larizmen@centos7 ~]$ sudo systemctl restart datadog-agent
```

After those changes, we can see how the new interval is the configured (45 seconds):

![alt text](https://github.com/luisarizmendi/hiring-engineers/raw/master/images/collection-45.png "15s")




_* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?_

Yes, it is possible, actually it's what I did changing the configuration in my_metric.yaml, not my_metric.py


## Visualizing Data:

_Utilize the Datadog API to create a Timeboard that contains:_

_* Your custom metric scoped over your host._
_* Any metric from the Integration on your Database with the anomaly function applied._
_* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket_

_Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard_


First step is to create a new application key:

![alt text](https://github.com/luisarizmendi/hiring-engineers/raw/master/images/app-key.png "key")

Then I installed datadog python libs with pip:

```bash
[root@centos7 ~]# pip install datadog
```

Following the documentation [1] below, I created a python script to create the new Dashboard 

[1] https://docs.datadoghq.com/api/?lang=bash#create-a-dashboard

![alt text](https://github.com/luisarizmendi/hiring-engineers/raw/master/images/api-docs.png "apidocs")

But when I tried to run it, I found the following issue:

```bash
[larizmen@centos7 ~]$ python create_timeboard.py  
Traceback (most recent call last): 
 File "create_timeboard.py", line 47, in <module> 
   api.dashboard.create(title=title, 
AttributeError: 'module' object has no attribute 'dashboard'
```

So I decided to review the datadog.api:

```bash
[larizmen@centos7 ~]$ pydoc datadog.api



Help on package datadog.api in datadog: 

NAME 
   datadog.api - # flake8: noqa 

FILE 
   /usr/lib/python2.7/site-packages/datadog/api/__init__.py 

PACKAGE CONTENTS 
   api_client 
   comments 
   constants 
   dashboard_lists 
   distributions 
   downtimes 
   events 
   exceptions 
   format 
   graphs 
   hosts 
   http_client 
   infrastructure 
   metadata 
   metrics 
   monitors 
   resources 
   screenboards 
   service_checks 
   tags 
   timeboards 
   users 

(END)
```

Taking a deeper look we can see that there is no method api.Dashboard (the one mentioned in the documentation). My first idea was that pip installed an old version of the libraries, so I searched how to write the python script with the modules installed by pip. Finally I ended up with this script:

```python
from datadog import initialize, api

options = {
    'api_key': '968ff88314a015a7efbf4ca54f3a55af',
    'app_key': 'fb3b1e7b4fac1de6c27b0715d21ec7b53c592d9f'
}

initialize(**options)

title = 'larizmen Timeboard'
description = "This is my Timeboard" 

graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}"},
        ],
        "viz": "timeseries"
    },
    "title": "My_Metric"
    },
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "anomalies(avg:mysql.performance.user_time{*}, 'basic', 2)"}
            ],
            "viz": "timeseries"
        },
        "title": "MySQL CPU Time (per sec)"
    },
    {
        "definition": {
            "events": [],
            "requests": [
                {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
            ],
            "viz": "timeseries"
        },
        "title": "My_Metric - Hourly"
    }
]


is_read_only = True
template_variables = [{
    'name': 'testvar',
    'prefix': 'host',
    'default': 'centos7.localdomain'
}]

api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=is_read_only,
                     template_variables=template_variables)
```

I ran this script and the dashboard was created:

![alt text](https://github.com/luisarizmendi/hiring-engineers/raw/master/images/created-timeboard.png "created-timeboard")

In order to check that I was right wbout the libraries installed by pip, I followed the other installation method metioned in [2] in a diferent server.

[2] https://datadogpy.readthedocs.io/en/latest/

```bash
[root@director-13 datadogpy]# git clone https://github.com/DataDog/datadogpy


[root@director-13 datadogpy]# python setup.py install


[root@director-13 datadog]# vi create_new_dashboard.py 
[root@director-13 datadog]# python create_new_dashboard.py  
```

and it worked with the coded showed in the datadog documentation [1]. This is the generated code:

```python
from datadog import initialize, api

options = {
    'api_key': '968ff88314a015a7efbf4ca54f3a55af',
    'app_key': 'fb3b1e7b4fac1de6c27b0715d21ec7b53c592d9f'
}

initialize(**options)

  title = 'NEW larizmen Timeboard'

widgets = [
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_newmetric{*}'}
        ],
        'title': 'My_NewMetric'
    }
},
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {"q": "anomalies(avg:mysql.performance.user_time{*}, 'basic', 2)"}
        ],
        'title': 'MySQL CPU Time (per sec)'
    }
},
{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_newmetric{*}.rollup(sum, 3600)'}
        ],
        'title': 'My_Metric - Hourly'
    }
}
]
layout_type = 'ordered'
description = 'New test'
is_read_only = True
notify_list = ['luis.ariz@gmail.com']
template_variables = [{
    'name': 'newtest',
    'prefix': 'host',
    'default': 'director'
}]
api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables)
```

Once this is created, access the Dashboard from your Dashboard List in the UI:

_* Set the Timeboard's timeframe to the past 5 minutes_

Already showed screenshot:

![alt text](https://github.com/luisarizmendi/hiring-engineers/raw/master/images/created-timeboard.png "created-timeboard")

_* Take a snapshot of this graph and use the @ notation to send it to yourself._

![alt text](https://github.com/luisarizmendi/hiring-engineers/raw/master/images/snapshot.png "snapshot")


_* **Bonus Question**: What is the Anomaly graph displaying?_

Anomaly graphs identify if the metrics collected behaves in a "non-usual" way taking into account the past values and patterns, for example:

![alt text](https://github.com/luisarizmendi/hiring-engineers/raw/master/images/ano-5sec.png "ano-5sec.png")

![alt text](https://github.com/luisarizmendi/hiring-engineers/raw/master/images/ano-15sec.png "ano-15sec.png")




## Monitoring Data

_Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:_

_* Warning threshold of 500_
_* Alerting threshold of 800_
_* And also ensure that it will notify you if there is No Data for this query over the past 10m._

_Please configure the monitor’s message so that it will:_

_* Send you an email whenever the monitor triggers._
_* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state._
_* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state._
_* When this monitor sends you an email notification, take a screenshot of the email that it sends you._

This is the config:

![alt text](https://github.com/luisarizmendi/hiring-engineers/raw/master/images/create-mon.png "create-mon.png")

The full monitor message is:

```bash
My monitor says:

{{#is_alert}} ALERT!
alert threshold reached

My_metric has a value of {{value}} in {{host.ip}}

{{/is_alert}} 

{{#is_warning}} WARNING!
warning threshold reached
{{/is_warning}} 

{{#is_no_data}} There is no DATA{{/is_no_data}} 
```

This one example of the emails received:

![alt text](https://github.com/luisarizmendi/hiring-engineers/raw/master/images/mon-email.png "mon-email.png")


_* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:_

  _* One that silences it from 7pm to 9am daily on M-F,_
  _* And one that silences it all day on Sat-Sun._
  _* Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification._
  
I configured two downtime schedulers, one in a daily basis and another one that last for 2 days and that repits every 7 days:

![alt text](https://github.com/luisarizmendi/hiring-engineers/raw/master/images/shutdown-daily.png "shutdown-daily.png")

![alt text](https://github.com/luisarizmendi/hiring-engineers/raw/master/images/shutdown-weekend.png "shutdown-weekend.png")
  
 This is an example of email:
 
 ![alt text](https://github.com/luisarizmendi/hiring-engineers/raw/master/images/shutdown-email.png "shutdown-email.png")
  

## Collecting APM Data:

First I included this configuration:

```bash
[root@centos7 ~]# grep -A 50 apm_config /etc/datadog-agent/datadog.yaml | grep -v ^# 
apm_config: 
 enabled: true 
 env: test 
 receiver_port: 8126
```

and restarted the agent:

```bash
[larizmen@centos7 ~]$ sudo systemctl restart datadog-agent
```

Then added the flask libraries with pip:

```bash
[larizmen@centos7 ~]$ sudo pip install flask
```

I used the given python code:

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
I ran that python script:

```bash
[root@centos7 myflask]# ddtrace-run python myflask.py  
* Serving Flask app "myflask" (lazy loading) 
* Environment: production 
  WARNING: Do not use the development server in a production environment. 
  Use a production WSGI server instead. 
* Debug mode: off 
2019-02-28 20:07:48,903 - werkzeug - INFO -  * Running on http://0.0.0.0:5050/ (Press CTRL+C to quit)
```

Then did some requests:

```bash
izmen@centos7 ~]$ curl http://localhost:5050 
Entrypoint to the Application

[larizmen@centos7 ~]$ curl http://localhost:5050/api/apm 
Getting APM Started

[larizmen@centos7 ~]$ curl http://localhost:5050/api/trace 
Posting Traces[larizmen@centos7 ~]$
```

Se can see the log outputs in the console:

```bash
[root@centos7 myflask]# ddtrace-run python myflask.py                                                                                                                                                              
* Serving Flask app "myflask" (lazy loading) 
* Environment: production 
  WARNING: Do not use the development server in a production environment. 
  Use a production WSGI server instead. 
* Debug mode: off 
2019-02-28 20:14:46,760 INFO [werkzeug] [_internal.py:88] -  * Running on http://0.0.0.0:5050/ (Press CTRL+C to quit) 
2019-02-28 20:14:46,760 - werkzeug - INFO -  * Running on http://0.0.0.0:5050/ (Press CTRL+C to quit) 
2019-02-28 20:14:52,934 DEBUG [ddtrace.writer] [writer.py:43] - resetting queues. pids(old:None new:31617) 
2019-02-28 20:14:52,934 - ddtrace.writer - DEBUG - resetting queues. pids(old:None new:31617) 
2019-02-28 20:14:52,934 DEBUG [ddtrace.writer] [writer.py:78] - starting flush thread 
2019-02-28 20:14:52,934 - ddtrace.writer - DEBUG - starting flush thread 
2019-02-28 20:14:52,938 INFO [werkzeug] [_internal.py:88] - 127.0.0.1 - - [28/Feb/2019 20:14:52] "GET / HTTP/1.1" 200 - 
2019-02-28 20:14:52,938 - werkzeug - INFO - 127.0.0.1 - - [28/Feb/2019 20:14:52] "GET / HTTP/1.1" 200 - 
2019-02-28 20:14:53,943 DEBUG [ddtrace.api] [api.py:160] - reported 1 traces in 0.00296s 
2019-02-28 20:14:53,943 - ddtrace.api - DEBUG - reported 1 traces in 0.00296s 
2019-02-28 20:14:56,027 INFO [werkzeug] [_internal.py:88] - 127.0.0.1 - - [28/Feb/2019 20:14:56] "GET /api/apm HTTP/1.1" 200 - 
2019-02-28 20:14:56,027 - werkzeug - INFO - 127.0.0.1 - - [28/Feb/2019 20:14:56] "GET /api/apm HTTP/1.1" 200 - 
2019-02-28 20:14:56,948 DEBUG [ddtrace.api] [api.py:160] - reported 1 traces in 0.00154s 
2019-02-28 20:14:56,948 - ddtrace.api - DEBUG - reported 1 traces in 0.00154s 
2019-02-28 20:14:56,948 INFO [ddtrace.sampler] [sampler.py:42] - initialized RateSampler, sample 100% of traces 
2019-02-28 20:14:56,948 - ddtrace.sampler - INFO - initialized RateSampler, sample 100% of traces 
2019-02-28 20:14:56,948 INFO [ddtrace.sampler] [sampler.py:42] - initialized RateSampler, sample 100% of traces 
2019-02-28 20:14:56,948 - ddtrace.sampler - INFO - initialized RateSampler, sample 100% of traces 
2019-02-28 20:14:57,957 INFO [werkzeug] [_internal.py:88] - 127.0.0.1 - - [28/Feb/2019 20:14:57] "GET /api/trace HTTP/1.1" 200 - 
2019-02-28 20:14:57,957 - werkzeug - INFO - 127.0.0.1 - - [28/Feb/2019 20:14:57] "GET /api/trace HTTP/1.1" 200 - 
2019-02-28 20:14:58,954 DEBUG [ddtrace.api] [api.py:160] - reported 1 traces in 0.00204s 
2019-02-28 20:14:58,954 - ddtrace.api - DEBUG - reported 1 traces in 0.00204s
```

Then I created a Dashboard with both infra and APM information and make it public in this link [3]

[3] https://p.datadoghq.com/sb/pv03bghqc10h75mt-1d51df6c15d5517a88b2d8186d68f4c0

![alt text](https://github.com/luisarizmendi/hiring-engineers/raw/master/images/apm_plus_infra.png "apm_plus_infra.png")



_* **Bonus Question**: What is the difference between a Service and a Resource?_

If the question is regarding metrics collected by APM, the main difference is that the Service refers to a group of processes that are intended to perform the same job, whereas a resource is restricted to a particular task for a service.
For example, in our test environment a service could be the database and a resource the would be the SQL query.


_Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics._
Already done: https://p.datadoghq.com/sb/pv03bghqc10h75mt-1d51df6c15d5517a88b2d8186d68f4c0

_Please include your fully instrumented app in your submission, as well._
Done above


## Final Question:

_Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!_

_Is there anything creative you would use Datadog for?_

One thing that I’m worried about during this past years is the quality of air. There are tons of info resources that could be used to create nice and useful dashboards, for example you could present pollution index at same time than current weather and public/private transport information per location and time.

