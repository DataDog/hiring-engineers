My Answers
==========
> First, let me thank you this opportunity. I had fun answering the questions and learning a bit more about Datadog. It also gave me a chance to play Space Invaders again :)
> 
> I used a simple straightforward approach to each challenge and learn that component deep enough to be able to give an educated guess while using some of the tooling I already know *(ex.: docker, python, postman and others).*
>
> Let's dive into it...


Prerequisites - Setup the environment
-------------------------------------
> I used a containerized approach as this is easy to setup and consumes less laptop resources. Nevertheless I tested everything in Vagrant/Puppet. If you want I can provide the scripts and information regarding that.
> I used a docker compose file to generate my container/images and spin up the necessary machines for this test. Mainly I have two machines in docker:
> 
>  + Postgres (Database Machine)
>  + Adminer (Managing Database)
>
> Here is the docker compose file ([stack.yml](../solutions-engineer/docker/stack.yml)):

```
version: '2'

services:
  # Postgres Container
  db:
    image: postgres
    restart: always
    networks:
      - docknet
    environment:
      POSTGRES_PASSWORD: datadog
    
  # Database Adminer Container    
  adminer:
    image: adminer
    restart: always
    ports:
      - 8181:8080
    networks:
      - docknet 
      
networks:
    docknet:
        external: true
```

> Docker compose to the rescue...

![Docker Compose](https://i.imgur.com/GmdSD7s.png)

> I created a container for Postgres Database and I shared the same network with the Database Adminer image. Adminer (formerly phpMinAdmin) is a full-featured database management tool written in PHP. Conversely to phpMyAdmin, it consist of a single file ready to deploy to the target server. 

![Adminer](https://i.imgur.com/U6rA3kM.png)
>
> Adminer is available for [MySQL](https://www.mysql.com/downloads/), [MariaDB](https://mariadb.org/download/), [PostgreSQL](https://www.postgresql.org/download/), [SQLite](https://www.sqlite.org/download.html), [MS SQL](https://www.microsoft.com/en-us/sql-server/sql-server-downloads), [Oracle](https://www.oracle.com/technetwork/database/enterprise-edition/downloads/index.html), [Firebird](https://www.firebirdsql.org/en/server-packages/), [SimpleDB](https://aws.amazon.com/simpledb/), 
[Elasticsearch](https://www.elastic.co/downloads/elasticsearch), [MongoDB](https://www.mongodb.com/download-center).
>
> This way I can quickly spin up other databases for testing and manage it from a central endpoint (localhost:8181 - I mapped a local port to the management port). 

- Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.

![local_machine](https://i.imgur.com/YgSmlRt.png)

> I use the following command to get into the docker container (Postgres):

```
docker exec -it env_db_1 /bin/bash
```
> I also installed the following packages inside the container:

```
apt-get update
apt-get install vim # cannot live without it...
apt-get install python
apt-get install pip
apt-get install curl
pip install flask
```
> Now let's tackle the questions!

Collecting Metrics:
-------------------
- Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

> I installed the datadog agent directly in the postgres machine using the curl command. Could have generated a docker image with the agent and gather the metrics/traces remotely but I figured that this way would be easier and could demonstrate my point.

```
DD_API_KEY=54464b588c296912a22ab3aba82e94f9 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

> vi datadog.yaml

![vidatadog.yaml](https://i.imgur.com/VzUocPv.png)

>Tag Configuration

![Configuration](https://i.imgur.com/vZG7cap.png)

```
tags:
    - region:ireland
    - region:dublin
    - application:database
    - database:postgres
    - role:dummy_test
```
>Host map

![Host with Tags](https://i.imgur.com/ZPalogT.png)

> Modern infrastructure is constantly in flux. Auto-scaling servers die as quickly as they’re spawned, and containers come and go with even greater frequency. With all of these transient changes, the signal-to-noise ratio in monitoring data can be quite low.
> Tagging your metrics enables you to reorient your monitoring along any lines you choose. By adding tags to your metrics you can observe and alert on metrics from different availability zones, instance types, software versions, services, roles—or any other level you may require.
> **Tags** allow you to filter and group your datapoints to generate exactly the view of your data that matters most. They also allow you to aggregate you metrics on the fly, without changing how they are reported and collected.

- Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

> I installed and configured PostgreSQL and the respective integration. Really simple and easy following the instructions.
 
![PostgresIntegration](https://i.imgur.com/4zQUJ2Y.png)

![database configuration - user creation](https://i.imgur.com/YAUCjAa.png)
![database configuration - user grants](https://i.imgur.com/LfVUUVP.png)
![database validation](https://i.imgur.com/zBgwsf1.png)

- Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

> Agent checks are a great way to collect metrics from custom applications or unique systems. However, if you are trying to collect metrics from a generally available application, public service or open source project, it's recommended to write an Integration.
> 
> In this case I created a simple python app (The Datadog Agent installation has its own embedded copy of Python) and a configuration file in yaml following the steps in this [link](https://docs.datadoghq.com/developers/agent_checks/).
>
> **/etc/datadog-agent/checks.d/mycheck.py**

```
__version__ = "1"

from checks import AgentCheck
from random import randint

class my_metricCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(0, 1000))
```

> **/etc/datadog-agent/conf.d/mycheck.yaml**

```
init_config:

instances:
    [{}]
```

> I also found useful information on custom checks (like checking for available licenses) in this [link](https://blog.devopscomplete.com/writing-a-custom-datadog-agent-check-7367c98ffc5a).


**- Change your check's collection interval so that it only submits the metric once every 45 seconds.**

> I changed the *mycheck.yaml* file with the min_connection_interval equal to 45. As I do not have multiple instances of this check, it simply goes like the code below. I could also add the min_collection_interval at the init_config level:

```
init_config:

instances:
    [{
        min_collection_interval: 45
    }]
```
**- Bonus Question: Can you change the collection interval without modifying the Python check file you created?**
> Yes?, You can change the collection interval at the init_config level or at the instance level in the Python check file

Visualizing Data:
-----------------
- Utilize the Datadog API to create a Timeboard that contains:
 
> I used Postman(already use it extensively...) to create the payload below and test the datadog API.
>
> I downloaded the Datadog Postman Collection (pre-configured API call templates, available [here](https://help.datadoghq.com/hc/en-us/article_attachments/360002499303/datadog_collection.json).  

![postman](https://cl.ly/1t39190x0A0p/Screen%252520Recording%2525202018-08-03%252520at%25252008.58%252520AM.gif)

> Example of usage of the API - Get all Active metrics
 
![activemetrics](https://i.imgur.com/sCPKdt2.png)

> For creating the Timeboard I used the "Create a Timeboard" POST method as you see below:

![](https://i.imgur.com/uyE3Aox.png)
 
> And I changed the body of the request with the following code:

![bodychangeAPI](https://i.imgur.com/qqrWnVm.png)

- Your custom metric scoped over your host.

- Any metric from the Integration on your Database with the anomaly function applied.

- Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket. Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

> Below is the body of the JSON payload I used to create the timeboard via API:

```
{
      "graphs" : [
      	{
          "title": "My Metric",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_metric{*}"}
              ]
          },
          "viz": "My Metric timeseries"
    	} , { 
        "title": "My Postgres Metric - Anomaly Function",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "anomalies(avg:postgresql.bgwriter.checkpoints_timed{*},'basic',2)"}
              ]
          },
          "viz": "Postgres BGWriter timeseries"
      } , {
      "title": "My Metric - Rollup Function",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "my_metric{*}.rollup(sum,100)"}
              ]
          },
          "viz": "My Metric Rollup timeseries"
      }],
      "title" : "My Awesome Metric Timeboard",
      "description" : "Timeboard that contains: - My custom metric scoped over my host. - Any metric from the Integration on your Database with the anomaly function applied. - My custom metric with the rollup function applied to sum up all the points for the past hour into one bucket",
      "template_variables": [{
          "name": "postgres",
          "prefix": "host",
          "default": "host:postgres"
      }],
      "read_only": "True"
    }
```


> All of the seasonal algorithms (robust and agile) may use up to a couple of months of historical data when calculating a metric’s expected normal range of behavior. By using a significant amount of past data, the algorithms are able to avoid giving too much weight to abnormal behavior that might have occurred in the recent past. As I did not have such amount of data I used the basic. Basic uses very little data and adjusts quickly to changing conditions but has no knowledge of seasonal behavior or longer trends.
>
> anomalies(avg:postgresql.bgwriter.checkpoints_timed{*}, 'basic', 2)"

![](https://i.imgur.com/MlN6gmV.png)
![](https://i.imgur.com/vDl1vJL.png)
> 
> Rollup custom metric 

![rollup custom metric](https://i.imgur.com/Izx1vWi.png)
![my_metric](https://i.imgur.com/NhJZD7S.png)

- Once this is created, access the Dashboard from your Dashboard List in the UI:

![Dashboard List](https://i.imgur.com/9trlWGH.png)

- Set the Timeboard's timeframe to the past 5 minutes
Take a snapshot of this graph and use the @ notation to send it to yourself.

![@notation for sharing](https://i.imgur.com/YCCCFB5.png)
![email received](https://i.imgur.com/iHYjpRV.png)

- Bonus Question: What is the Anomaly graph displaying?

> Anomaly detection is an algorithmic feature that allows you to identify when a metric is behaving differently than it has in the past, taking into account trends, seasonal day-of-week and time-of-day patterns. It is well-suited for metrics with strong trends and recurring patterns that are hard or impossible to monitor with threshold-based alerting.
>
> For example, anomaly detection can help you discover when your web traffic is unusually low on a weekday afternoon—even though that same level of traffic would be perfectly normal later in the evening. Or consider a metric measuring the number of logins to your steadily-growing site. As the number is increasing every day, any threshold would be quickly outdated, whereas anomaly detection can quickly alert you if there is an unexpected drop—potentially indicating an issue with the login system.
>
> There is an anomalies function in the Datadog query language. When you apply this function to a series, it returns the usual results along with an expected “normal” range.
>
> Anomaly detection monitors provide both “Historical Context” so that you can see how the metric behaved in the past, as well as a separate “Evaluation Window” that is longer than the alerting window to provide you some immediate context. This should provide some insight into what the anomalies algorithm takes into account when calculating the bounds.
>
> Keep in mind that anomalies uses the past to predict what is expected in the future, so using anomalies on a new metric, for which you have just started collecting data, may yield poor results.


Monitoring Data
-------------------------------
Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

- Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

- Warning threshold of 500
- Alerting threshold of 800
- And also ensure that it will notify you if there is No Data for this query over the past 10m.

> I just created a metric monitor from the UI with the following parameters:
 
![MetricMonitor](https://i.imgur.com/KM6vzfs.png)

Please configure the monitor’s message so that it will:

- Send you an email whenever the monitor triggers.

- Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.


- Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

![Messages notification](https://i.imgur.com/YBVTxlI.png)

When this monitor sends you an email notification, take a screenshot of the email that it sends you.

![email](https://i.imgur.com/iKkKBcR.png)

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

- One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.

> Evening Weekdays

![Weekdays](https://i.imgur.com/jO2vWX5.png)
>Weekend

![Weekend](https://i.imgur.com/9eNHux1.png)

>Manage Downtime

![Downtime](https://i.imgur.com/WQlfTGi.png)

- Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

![Adminer](https://i.imgur.com/lbUzPnD.png)
![Adminer](https://i.imgur.com/FQeb2Rx.png)

Collecting APM Data:
--------------------
Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

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
    
Note: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

> ddtrace provides tracing support for many Python web frameworks. For each framework ddtrace supports:
>
> - tracing of requests: trace requests through middleware and back
> - distributed tracing: trace requests across application boundaries
> - automatic error tagging: spans will be marked with any errors that occur
>
> I created two simple apps based on Flask. One will use the ddtrace-run and the other will use the middleware.
> 
> | App Name    | method        | port  |
> | ------------- |:-------------:| -----:|
> | hello.py      | ddtrace-run   |   5050|
> | hey.py        | middleware    |   6060|
> 
> For the sake of having some traffic in these 2 apps I used the following commands:

```
> (one app) 
> → ab -n 10000 -c 100 'http://127.0.0.1:5050/api/trace'

> (both apps) 
> → ab -n 10000 -c 100 'http://127.0.0.1:5050/' | ab -n 10000 -c 100 'http://127.0.0.1:6060/'

> (execute 10 times both apps) 
> → repeat 10 {ab -n 10000 -c 100 'http://127.0.0.1:5050/' | ab -n 10000 -c 100 'http://127.0.0.1:6060/'; sleep 5}

```
![](https://i.imgur.com/1GpKK4N.png)

> **hello.py -> ddtrace-run** 

```
from flask import Flask
import logging
import sys
from ddtrace import *

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

@app.route('/')
@tracer.wrap()
def api_entry_hello():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
@tracer.wrap()
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
@tracer.wrap()
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
```
> **hey.py -> Insert Middleware**

```
from flask import Flask
import logging
import sys

from flask import Flask
import blinker as _

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

traced_app = TraceMiddleware(app, tracer, service="my-hey-app", distributed_tracing=False)

@app.route('/')
def api_entry_hey():
    return "hello world"

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='6060')
```
> In terms of execution I run the following commands:

```
→ ddtrace-run python hello.py
→ python hey.py
```

Bonus Question: What is the difference between a Service and a Resource?
> **Service**

> A "Service" is the name of a set of processes that work together to provide a feature set. For instance, a simple web application may consist of two services: a single webapp service and a single database service, while a more complex environment may break it out into 6 services: 3 separate webapp, admin, and query services, along with a master-db, a replica-db, and a yelp-api external service.
>
> These services are defined by the user when instrumenting their application with Datadog. This field is helpful to quickly distinguish between your different processes.
>
> **Resource**
>
> Most of the components of your infrastructure can be thought of as resources. At the highest levels, each of your systems that produces useful work likely relies on other systems. For instance, the Apache server in a LAMP stack relies on a MySQL database as a resource to support its work of serving requests. One level down, MySQL has unique resources that the database uses to do its work, such as the finite pool of client connections. At a lower level still are the physical resources of the server running MySQL, such as CPU, memory, and disks.
Thinking about which systems produce useful work, and which resources support that work, can help you to efficiently get to the root of any issues that surface. When an alert notifies you of a possible problem, the following process will help you to approach your investigation systematically.
>
> A particular query to a service. For a web application, some examples might be a canonical URL like /user/home or a handler function like web.user.home (often referred to as "routes" in MVC frameworks). For a SQL database, a resource would be the SQL of the query itself like select * from users where id = ?
>
> The Tracing backend can track thousands (not millions or billions) of unique resources per service, so resources should be grouped together under a canonical name, like /user/home rather than have /user/home?id=100 and /user/home?id=200 as separate resources.
>
> These resources can be found after clicking on a particular service.
>
> check this link: https://help.datadoghq.com/hc/en-us/articles/115000702546-What-is-the-Difference-Between-Type-Service-Resource-and-Name-
> check more info on the ebook I'm reading!

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

> [Dashboard](https://p.datadoghq.com/sb/271985619-b37dd043701a21f66b0975d7ee572694)
> 
> My dashboard - I had to create a screenboard in order to generate the public url for sharing. I could not use the Timeboard I had previously created. Check table below.
> 
> |     | Timeboards        | Screenboards  |
| ------------- |:-------------:| -----:|
| Time Scope      | All graphs share same time scope	   |   All graphs can have individual time scope|
| Layout        | Graphs appear in a fixed grid	    |   Graphs are placed anywhere you like on the canvas|
| Can Share Graphs Individually	        | Yes    |   No|
| Can Share the Entire Dashboard	        | **No**    |   Yes|
| Sharing can be Read-Only	        | Yes    |   Yes|
> Screenboard
>
![Screeboard](https://i.imgur.com/7fTooqb.png)
> 
> Timeboard 

![Timeboard](https://i.imgur.com/S9j6Col.png)

Please include your fully instrumented app in your submission, as well.

> [hello.py](../solutions-engineer/python/hello.py)
> 
> [hey.py](../solutions-engineer/python/hey.py)

Final Question:
---------------
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!
Is there anything creative you would use Datadog for?

>
1. Monitor the status of the office coffee machine each morning before getting in or the vending machine for a Coke...
- Monitor my wife's plants in the house and suggest water them
- Monitor the automatic feeding machine for my daughters aquarium (this one will be awesome to decrease the mortality rate...) :) **[TAKE PICTURE]**
- Dashboard for Music Concert management, number of people, status of all the systems, alerts if something fails and rock on
- Check the online/physical status of your team (if they are at the office or working from home), overlay in a map
- Monitoring home automation System with Alexa for example and live feed video, fire and intrusion alarms or others - **IoT feeds**
- Smart City 
- Monitor the backup/restore process of different cloud/on-prem machines
- Monitor hazard areas, delayed flights, affected areas, police reports and social media reports (ex.: Hurricane Michael) - **Social feeds**

Links and important stuff:
--------------------------
- [Docker useful commands](../solutions-engineer/aux/docker_commands.txt)

- [Tracing and testing commands](../solutions-engineer/aux/tracing_commands.txt)

- [My Dashboard](https://p.datadoghq.com/sb/271985619-b37dd043701a21f66b0975d7ee572694)

- [Datadog APM agent - macosx additional steps](https://github.com/DataDog/datadog-trace-agent#run-on-osx)

- [Agent checks](https://docs.datadoghq.com/developers/agent_checks/)

- [Tracing Python Apps - APM](https://docs.datadoghq.com/tracing/setup/python/)

- [Integrations](https://docs.datadoghq.com/integrations/)

- [Tagging](https://docs.datadoghq.com/tagging/)

- [API](https://docs.datadoghq.com/api/?lang=python#overview)

Suggestions & Feedback:
-----------------------
![BugsShirt](https://i.imgur.com/JCEHo2Dm.png)

> I had a strange occurence when I was scheduling the downtime. Even if I scheduled a recurring downtime with no end date there is a date that my two scheduled downtimes were disable. Are this limitations on the trial or a random feature?

![Bug](https://i.imgur.com/hnA4KOU.png)

![Bug](https://i.imgur.com/Ip6Y66a.png)

> I missed some features like:
>
> - Responsive design on the website so I could check on a mobile device
> - Mobile native app for on the go monitoring
> - Mobile monitoring: BYOD as part of the infrastructure, Datadog agent in the mobile
> - Easier way to delete the dashboard created using the API, I should be able to delete the dashboard inside of "himself" instead of jumping to the dashboard list

About Me
--------

<a href="mailto:rui.lamy@gmail.com">rui.lamy@gmail.com</a>


I Love gaming, running, reading, technology :D

<p align="center">
<img src="https://i.imgur.com/nUqjr07.jpg" width="200" height="300" align="middle"/>
  <img />
</p>

> **APM Invaders Video**

- Example of ddtrace trace.wrap() code instrumentation in a cool game. 

[![APM Invaders](https://i.ytimg.com/vi/Wj-zdkiwo2Q/hqdefault.jpg)](https://www.youtube.com/watch?v=Wj-zdkiwo2Q&t=2s)

Hope to be part of the team!
![Team](https://datadog-prod.imgix.net/img/blog/engineering/being-a-solutions-engineer-at-datadog/se_group.jpg?auto=format&fit=max&w=847&dpr=2)


Thanks for checking out my responses. Hope you have as much fun as I did answering them ;)