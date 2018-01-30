# DataDog SE Lab Results
## Fork it!

Started by forking an then cloning the repository to my local machine.
![alt text](https://s3-us-west-1.amazonaws.com/redmansimages/let_the_games_begin.png "Cloning Repo")

I decided to run my lab on AWS using a combination of an EC2 instance and S3 to store all my screenshots. I spun up an Ubuntu image installed the Datadog agent, MySQL, Flask and a few other necessities.

Environment Details
![alt text](https://s3-us-west-1.amazonaws.com/redmansimages/aws_env.png "AWS Environment")


## Collecting Metrics
**Ask:** Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

**Answer:** The below image is an illustration of the modified tags in the configuration file and a screenshot of the Hostmap screen.
![alt text](https://s3-us-west-1.amazonaws.com/redmansimages/tags_in_conf.png "Conf file with a couple of tags")

I chose to filter the host by the tag I created in the host file.
![alt text](https://s3-us-west-1.amazonaws.com/redmansimages/hostmap.png "Hostmap")

**Ask:** Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

**Answer:** I ran into an error when initially configuring the MySQL integration. I was able to figure it out pretty quickly by running ```sudo /etc/init.d/datadog-agent info```, this produced the error message in the screenshot. This message had just the right information for me to solve the problem. Turned out to be an extra space in the yaml.
![alt text](https://s3-us-west-1.amazonaws.com/redmansimages/yaml_error.png "yaml error")

Below is a screenshot of the MySQL integration

![alt text](https://s3-us-west-1.amazonaws.com/redmansimages/sql_dashboard.png "SQL Dashboard")

**Ask:** Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

**Answer:** I used the sample I found in the documentation, it's a very simple one but effective. That said I do see it's entirely possible to create robust checks.

Contents of mycheck.py

```python
from checks import AgentCheck
import random

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000))
```

**Ask:** Change your check's collection interval so that it only submits the metric once every 45 seconds.

![alt text](https://s3-us-west-1.amazonaws.com/redmansimages/my_metric.png "Custom agent check")

**Ask:** Bonus Question Can you change the collection interval without modifying the Python check file you created?

**Answer** I was able to change the interval in the yaml

contents of mycheck.yaml
```
init_config:
    min_collection_interval: 45

instances:
    [{}]
```

## Visualizing Data
**Ask:** Utilize the Datadog API to create a Timeboard that contains:

- Your custom metric scoped over your host.
- Any metric from the Integration on your Database with the anomaly function applied.
- Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket.

Result of my timeboard.py script

![alt text](https://s3-us-west-1.amazonaws.com/redmansimages/timeboard.png "Timboard")

Contents of timeboard.py the file is also in the repo.

```Python
from datadog import initialize, api

options = {
    'api_key': '72fdb42db3c939880977b6b32ea31cbd',
    'app_key': '31e8b0547d314e638dd14a4106bd417e420ea39b'
}

initialize(**options)

title = "Redman Timeboard"
description = "An informative timeboard."
graphs = [
  {
   "definition": {
   "events": [],
   "requests": [
              {"q": "avg:my_metric{host:i-02dd61a0045470207}"}
          ],
   "viz": "timeseries"
   },
   "title": "My Metric"
  },
  {
   "definition": {
   "events": [],
   "requests": [
              {"q": "anomalies(avg:mysql.net.max_connections{*}, 'basic', 2)"}
          ],
   "viz": "timeseries"
   },
   "title": "Anomalies SQL Max Connections"
  },
  {
   "definition": {
   "events": [],
   "requests": [
              {"q": "avg:my_metric{*}.rollup(sum, 3600)",
   "aggregator": "sum",
   "style": {
   "width": "normal",
   "palette": "dog_classic",
   "type": "solid"
                }
              }
          ],
   "viz": "query_value"
   },
   "title": "Sum of My Metric - One Hour Buckets"
  }
]

api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs)
```

In order to get the correct JSON I used the JSON tab in each one of the graphs. Maybe not the most efficient way to get the correct structure, but I thought it was a decent approach given I'm still learning the platform.

![alt text](https://s3-us-west-1.amazonaws.com/redmansimages/json_config.png "JSON Config")

Once this is created, access the Dashboard from your Dashboard List in the UI:

- Set the Timeboard's timeframe to the past 5 minutes
![alt text](https://s3-us-west-1.amazonaws.com/redmansimages/5min.png "5 Minutes")
- Take a snapshot of this graph and use the @ notation to send it to yourself.
![alt text](https://s3-us-west-1.amazonaws.com/redmansimages/snapshot.png "Sending a snapshot")

![alt text](https://s3-us-west-1.amazonaws.com/redmansimages/snap_email.png "Email")
- **Bonus Question:** What is the Anomaly graph displaying?

The expected behavior of a series based on past data. Based on reading the following https://docs.datadoghq.com/monitors/monitor_types/anomaly/ I think a good use case for this is on APM response time traces. This particular metric typically vary's greatly based on throughput. I can see customers using this to reduce alerts based on past traffic patterns, as an example every Monday after lunch an increase in throughput and a performance degradation of 1 bound might be "normal" behavior.


## Monitoring Data

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

- Warning threshold of 500
- Alerting threshold of 800
- And also ensure that it will notify you if there is No Data for this query over the past 10m.

![alt text](https://s3-us-west-1.amazonaws.com/redmansimages/monitor_config.png "Monitoring Config")

Please configure the monitor’s message so that it will:

- Send you an email whenever the monitor triggers.

- Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
![alt text](https://s3-us-west-1.amazonaws.com/redmansimages/alert_config.png "Alert")

- Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

When this monitor sends you an email notification, take a screenshot of the email that it sends you.

![alt text](https://s3-us-west-1.amazonaws.com/redmansimages/email.png "Monitoring Config")

- **Bonus Question:** Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

 - One that silences it from 7pm to 9am daily on M-F,
 ![alt text](https://s3-us-west-1.amazonaws.com/redmansimages/maint1.png "Maint1")


 - And one that silences it all day on Sat-Sun.
 ![alt text](https://s3-us-west-1.amazonaws.com/redmansimages/maint2.png "Maint2")

 - Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
 Please find screenshots of both of the email notifications
![alt text](https://s3-us-west-1.amazonaws.com/redmansimages/maint1_email.png "Alert")
![alt text](https://s3-us-west-1.amazonaws.com/redmansimages/maint2_email.png "Alert")


## Collecting APM Data

I reused the Flask app which was provide as part of the Lab. In addition, I created a database called fang with a single table called pet. I wanted to see what level instrumentation the Datadog agent would provide without additional configuration. I started my Flask ample application like so ```ddtrace-run pyton flaskapp.py``` I also wanted to see what the difference was when manually adding the TraceMiddleware, so I installed Blinker and ran the agent with the middleware hook to see what the difference was. I attached screenshots of both approaches.

![alt text](https://s3-us-west-1.amazonaws.com/redmansimages/apm.png "APM Data")

The below is a screenshot of the same application using Blinker and TraceMiddleWare

![alt text](https://s3-us-west-1.amazonaws.com/redmansimages/apm_middleware.png "APM Data")

```Python
from flask import Flask
import logging
import sys
import datetime
import mysql.connector
#from ddtrace import tracer
#from ddtrace.contrib.flask import TraceMiddleware
#import blinker as _

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)
#traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)
@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

@app.route('/api/query')
def run_query():
    for i in range(1000):
        cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='fang')
        cursor = cnx.cursor()
        query = ("select * from pet")
        cursor.execute(query)
        for (name) in cursor:
            print name
    cursor.close()
    cnx.close()
    return 'DB Query'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

```

**Ask:**  What is the difference between a Service and a Resource?

**Answer:** I found a good explanation of the two in the documentation.

![alt text](https://s3-us-west-1.amazonaws.com/redmansimages/terminology.png "Terminology")

## Final Question

Is there anything creative you would use Datadog for?

I think integrating Datadog into performance testing environments would be a fantastic idea. I'm starting to see teams run performance tests as part of the CI pipeline. Build an integration with JMeter, LoadRunner and other testing tools in addition to pulling information from a CI tool would resonate well with performance engineering teams. I have a sample Python wrapper I created for sending events to Datadog upon the start and end of a load test, this script can easily be modified to run as a step in Jenkins and send build information to Datadog

```python
from datadog import initialize, api
import datetime
from subprocess import call


#JMeter Configuration
JMETER_HOME='/Users/michael.redman/Dropbox/AppDynamics/Development/JMeter/apache-jmeter-2.13JP1.3.1WD'
SCRIPT='/Users/michael.redman/Dropbox/AppDynamics/Labs/DataDog/hiring-engineers/load.jmx'
RESULTS='/Users/michael.redman/Dropbox/AppDynamics/Labs/DataDog/hiring-engineers/jmeter-results.jtl'
LOG='/Users/michael.redman/Dropbox/AppDynamics/Labs/DataDog/hiring-engineers/jmeter-log.log'

options = {
    'api_key': '72fdb42db3c939880977b6b32ea31cbd',
    'app_key': '31e8b0547d314e638dd14a4106bd417e420ea39b'
}

def post_event(t,m):
	initialize(**options)

	title = t
	text = m
	tags = ['version:1', 'application:web']

	api.Event.create(title=title, text=text, tags=tags)

def run_automation():
	start_event_name = 'perf_run_start: ' +  str(datetime.datetime.now().strftime("%y-%m-%d-%H-%M"))
	post_event(start_event_name, 'starting load.jmx')
	call([JMETER_HOME + "/bin/jmeter", "-n", "-t", SCRIPT, "-l", RESULTS, "-j", LOG])
	end_event_name = 'perf_run_end: ' +  str(datetime.datetime.now().strftime("%y-%m-%d-%H-%M"))
	post_event(end_event_name, 'end load.jmx')

# If you are programmatically adding a comment to this new event
# you might want to insert a pause of .5 - 1 second to allow the
# event to be available.

run_automation()

```
Sample performance testing dashboard
![alt text](https://s3-us-west-1.amazonaws.com/redmansimages/perf_dash.png "Terminology")
