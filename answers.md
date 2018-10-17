My Answers
==========

[![Language](https://img.shields.io/badge/language-python-blue.svg?style=flat
)](https://www.python.org)
[![Module](https://img.shields.io/badge/module-pygame-brightgreen.svg?style=flat
)](http://www.pygame.org/news.html)
[![Release](https://img.shields.io/badge/release-v1.0-orange.svg?style=flat
)](http://www.leejamesrobinson.com/space-invaders.html)

About Me
--------
Add information about me here.... Love for gaming, running, reading, technology :D

<img src="http://i.imgur.com/u2mss8o.png" width="360" height="300" />


What I build
------------
 - I used a containerized approach as it is easy to setup and consumes less laptop resources
 - I used the following dockerfile for spining up the necessary machines for this test:
    + Postgres (Database Machine)
    + Adminer (Managing Database)
 
 If you don't have [Python](https://www.python.org/downloads/) or [Pygame](http://www.pygame.org/download.shtml) installed, you can simply double click the .exe file to play the game.
   **Note:** *The .exe file needs to stay in the same directory as the sounds, images, and font folders.*
   
 - If you have the correct version of Python and Pygame installed, you can run the program in the command prompt / terminal.
 ``` bash
cd SpaceInvaders
python spaceinvaders.py
 ```
 **Note:** If you're using Python 3, replace the command "python" with "python3"


Prerequisites - Setup the environment
-------------------------------------
I used the Containerized approach with Docker for Linux. It is the simplest in terms of infrastructure. Nevertheless I tested everything in a vagrant

Here is the docker compose file (stack.yml):

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

I created a container for Postgres Database sharing the same network with the Database Adminer image. Adminer (formerly phpMinAdmin) is a full-featured database management tool written in PHP. Conversely to phpMyAdmin, it consist of a single file ready to deploy to the target server. 

<img src="https://i.imgur.com/U6rA3kM.png" align="middle"/>

**(CHANGE THIS LINKS)**Adminer is available for [MySQL](https://www.mysql.com/downloads/), [MariaDB](https://www.mysql.com/downloads/), [PostgreSQL](https://www.mysql.com/downloads/), [SQLite](https://www.mysql.com/downloads/), [MS SQL](https://www.mysql.com/downloads/), [Oracle](https://www.mysql.com/downloads/), [Firebird](https://www.mysql.com/downloads/), [SimpleDB](https://www.mysql.com/downloads/), 
[Elasticsearch](https://www.mysql.com/downloads/), [MongoDB](https://www.mysql.com/downloads/).

This way I can quickly spin up other databases and manage it from a central endpoint (http://localhost:8181 - I mapped a local port to the management port). Check the enablement commands necessary for the side of the Postgres Integration:

<img src="https://i.imgur.com/DmrDiyt.png" width="350" height="300" />
<img src="https://i.imgur.com/RUeR4oK.png" width="350" height="300" />



I signup for a free trial account at datadoghq.com 




 and our dockerized Datadog Agent image.
Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.




Demo
----
[![Space Invaders](http://img.youtube.com/vi/_2yUP3WMDRc/0.jpg)](http://www.youtube.com/watch?v=_2yUP3WMDRc)



Collecting Metrics:
-------------------
- Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
I added several tags in the datadog.yaml file (located in /etc/datadog-agent/ folder)

```
tags:
    - region:ireland
    - region:dublin
    - application:database
    - database:postgres
    - role:dummy_test
```
**explain tags here from ebook**

**[Screenshot here]**

- Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
I installed PostgreSQL. Check the screenshots below. I also added to the container vim and curl.

- Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

**Agent checks are a great way to collect metrics from custom applications or unique systems. However, if you are trying to collect metrics from a generally available application, public service or open source project, we recommend that you write an Integration.**

Add information about the check and the gauge...(different ways besides gauge)

**/etc/datadog-agent/checks.d/mycheck.py**

```
from checks import AgentCheck
from random import randint

class my_metricCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(0, 1000))
```

**/etc/datadog-agent/conf.d/mycheck.yaml**

```
init_config:

instances:
    [{}]
```

A custom Agent check

examples of others checks - https://blog.devopscomplete.com/writing-a-custom-datadog-agent-check-7367c98ffc5a (useful)


**- Change your check's collection interval so that it only submits the metric once every 45 seconds.**

I changed the *mycheck.yaml* file with the min_connection_interval equal to 45. Has I do not have multiple instances of this check, it simply goes like the code below. I could also add the min_collection_interval at the init_config level:

```
init_config:

instances:
    [{
        min_collection_interval: 45
    }]
```
**- Bonus Question: Can you change the collection interval without modifying the Python check file you created?**

[check better this response] ?Yes?, You can change the collection interval at the init_config level or at the instance level in the Python check file

Visualizing Data:
-----------------
Utilize the Datadog API to create a Timeboard that contains:

- Your custom metric scoped over your host.
 
- Any metric from the Integration on your Database with the anomaly function applied.

All of the seasonal algorithms may use up to a couple of months of historical data when calculating a metric’s expected normal range of behavior. By using a significant amount of past data, the algorithms are able to avoid giving too much weight to abnormal behavior that might have occurred in the recent past. I used the basic one due to that...


- Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket. Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

I used Postman(use it extensively...) to create the payload below and test the datadog API.
I downloaded the Datadog Postman Collection (pre-configured API call templates, available for [download here](https://help.datadoghq.com/hc/en-us/article_attachments/360002499303/datadog_collection.json).  

<img  src="https://cl.ly/1t39190x0A0p/Screen%252520Recording%2525202018-08-03%252520at%25252008.58%252520AM.gif" align="middle"/>


Just changed the body of the [Screenshot 2018-10-17 at 00.33.32]


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

- Once this is created, access the Dashboard from your Dashboard List in the UI:

- Set the Timeboard's timeframe to the past 5 minutes
Take a snapshot of this graph and use the @ notation to send it to yourself.

DONE :D

**Bonus Question: What is the Anomaly graph displaying?**

Anomaly detection is an algorithmic feature that allows you to identify when a metric is behaving differently than it has in the past, taking into account trends, seasonal day-of-week and time-of-day patterns. It is well-suited for metrics with strong trends and recurring patterns that are hard or impossible to monitor with threshold-based alerting.

For example, anomaly detection can help you discover when your web traffic is unusually low on a weekday afternoon—even though that same level of traffic would be perfectly normal later in the evening. Or consider a metric measuring the number of logins to your steadily-growing site. As the number is increasing every day, any threshold would be quickly outdated, whereas anomaly detection can quickly alert you if there is an unexpected drop—potentially indicating an issue with the login system.

There is an anomalies function in the Datadog query language. When you apply this function to a series, it returns the usual results along with an expected “normal” range.

Anomaly detection monitors provide both “Historical Context” so that you can see how the metric behaved in the past, as well as a separate “Evaluation Window” that is longer than the alerting window to provide you some immediate context. This should provide some insight into what the anomalies algorithm takes into account when calculating the bounds.

Keep in mind that anomalies uses the past to predict what is expected in the future, so using anomalies on a new metric, for which you have just started collecting data, may yield poor results.



Monitoring Data
---------------
Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

- Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

- Warning threshold of 500
- Alerting threshold of 800
- And also ensure that it will notify you if there is No Data for this query over the past 10m.

Please configure the monitor’s message so that it will:

Send you an email whenever the monitor triggers.

Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

When this monitor sends you an email notification, take a screenshot of the email that it sends you.

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.
Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

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

Bonus Question: What is the difference between a Service and a Resource?
check this link: https://help.datadoghq.com/hc/en-us/articles/115000702546-What-is-the-Difference-Between-Type-Service-Resource-and-Name-


Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

Final Question:
---------------
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

- Check the status of the coffee machine each morning before getting there
- Dashboard for Music Concert management, number of people, status of all the systems, alerts if something fails
- Check the online status of your team and the physical status (if they are at the office or working from home)
- Monitoring home automation System with Alexa and cameras
- Monitor the automatic feeding machine for my daughters fish
- Monitor the presence of boss in the headqarters.
- Monitor the backup/restore process of different machines
- Check hazard areas, delayed flights, affected areas, police reports and social media reports (ex.: Hurricane Michael)

Contact
-------
Thanks for checking out my responses. Hope you have as much fun as did answering them.

- Rui Lamy
- rui.lamy@gmail.com




