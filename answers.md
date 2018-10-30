# Prerequisites - Setup the environment
* I created a new ec2 instance on my existing AWS account
* After signing up for DataDog with my name and the Company "Datadog Recruiting Canditate" I installed the DD agent for Amazon Linux. Using an agent-based approach has multiple benefits (e.g. agent "phones home"); especially in a cloud environment or in modern app architectures with an increasing number of instances that are provisioned and deprovisioned on a regular basis. Installing and running the agent is super easy - I can imagine that customers benefit from DataDog's ease of use.
* Once the agent is started it shows up in the DataDog UI automatically
# Collecting Metrics
## Host Map Page
* Based on datadog.yaml.example file in /etc/datadog-agent/ and the online documentation https://docs.datadoghq.com/tagging/ I created tags for my sample ec2 instance in the datadog.yaml for the local agent
* After a restart of the agent I checked the Host Map page in DD
![DD Host Map](https://github.com/jg8810/hiring-engineers/blob/master/HostMap.png)

## DataDog integration for a database

* Installation of PostgreSQL (first I tried to use a dockerized database but I ran into issues with getting the datadog pgsql user to work so I switched to a local pgsql installation using yum)
* Followed the Postgres Integration instructions of the DD docs (create a user and grant select on pg_stat_database)
* The Connection Test worked and returned - "Postgres connection - OK"
* Then I configured the DD agent using an additional file "postgres.yaml" (host, port, username, password & tags) in the conf.d in order to collect metrics
* I checked the DD agent status and the postgres section indicated that it has been configured correctly

## Custom Agent Check
* I followed the instructions at https://docs.datadoghq.com/developers/agent_checks/?tab=agentv6 to create a custom agent check using python and a related config yaml
my_check.py:
```
__version__ = "1.0.0"
import random

from checks import AgentCheck
class my_check(AgentCheck):
    def check(self, instance):
        my_number = random.randint(0, 1000)
        self.gauge('my_check', my_number)
```
my_check.yaml:
```
init_config:

instances:
    [{}]

```

* I tested my custom agent check using "datadog-agent check my_check"
<Screenshot of my_check>
  
* The online documentation stated to use the property "min_collection_interval" to overwrite the default check interval of 15 seconds. I changed the my_check.yaml file to 
```
init_config:

instances:
    - name: my_check
      min_collection_interval: 45
```

## Bonus Question
I already handled the custom check interval using the yaml definition without changing the logic of the python check

# Visualizing Data
## Create Timeboard using the DataDog API
* I checked the documentation https://docs.datadoghq.com/graphing/ and the API reference https://docs.datadoghq.com/api/?lang=bash#timeboards
* For interacting with DD via the API I had to create an Application Key first
* To get a better understanding how the Timeboards are created and can be customized I created my very first Timeboard using the DD GUI
* After that I put together the json representation of the Timeboard that I wanted to create using Postman. 
* The REST API provides an easy to use way to provide Dashboards as code, put Dashboards under version control and share common Dashboards with other teams. Furthermore you can work with template variables in order to benefit from reusability and better maintenance.
* After sending the POST request to the REST API endpoint I retrieved a successful response (http status 200 and json payload) so the Dashboard has been created successfully
* json Payload of the POST request:
```
{
    	"graphs" : [{
        	"title": "my_check Average",
        	"definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_check{$host}"}
              ],
              "viz": "timeseries"
        	}
    	},
    	{
          	"title": "PostgreSQL Connection Anomalies",
        	"definition": {
              "events": [],
              "requests": [
                  {"q": "anomalies(avg:postgresql.percent_usage_connections{jg_aws_db}, 'basic', 5)"}
              ],
              "viz": "timeseries"
        	}
    	},
    	{
          	"title": "my_check Rollup per hour",
        	"definition": {
              "events": [],
              "requests": [
                  {"q": "avg:my_check{$host}.rollup(sum, 3600)"}
              ],
              "viz": "timeseries"
        	}
    	}],
      "title" : "Jürgens Dashboard",
      "description" : "A dashboard with my_check and PostgreSQL info.",
      "template_variables": [{
          "name": "host",
          "prefix": "name",
          "default": "name:jgaws"
      }]
}
```
## Access Dashboard
* I opened the Dashboard in the DD GUI and set the timeframe to the past 4 hours in order to see some data in the rollup graph
![Dashboard](https://github.com/jg8810/hiring-engineers/blob/master/dashboard.png)
* It took me a couple of minutes in order to set the timeframe to the past 5 minutes.
  * After checking the keyboard shortcuts, it seems like German keyboards are not supported in order to Zoom out/in time frame using 
```
Alt + [
or
Alt + ]
```
  * So I switched to an English keyboard layout and now it worked :)
![Dashboard 5 minutes timeframe](https://github.com/jg8810/hiring-engineers/blob/master/dashboard5m.png)
* I created a snapshot and sent it to myself using the @-notation
![Snapshot via email](https://github.com/jg8810/hiring-engineers/blob/master/snapshot.png)
## Bonus Question
In my case the anomaly graph for the database metric is not displaying any relevant anomalies, because the database is not used at all. In theory you would see any outliers that deviate from the collected patterns

# Monitoring Data
## Create Metric Monitor
* I created a new Metric Monitor with the properties as requested in the instructions - in order to have some host properties available within the email text I had to define the to be monitored metric "my_check" by host (last parameter)
![Monitor Definition](https://github.com/jg8810/hiring-engineers/blob/master/monitor1.png)
* I used message template variables in order to distinguish alerts, warnings and the case of not receiving data:
![Monitor notification content](https://github.com/jg8810/hiring-engineers/blob/master/monitor2.png)
* After a couple of minutes I received my first warning via email
![Warning notification](https://github.com/jg8810/hiring-engineers/blob/master/warning.png)
* In order to also see the alert emails I changed the custom agent check to generate random numbers between 900 and 1000
* And here is a screenshot of the received alert and the host IP:
![Alert notification](https://github.com/jg8810/hiring-engineers/blob/master/alert.png)

## Bonus Question
* I created two different Scheduled Downtimes for my monitor
* The first downtime is defined as weekly running from Monday-Friday beginning at 7PM and running for 14hrs (so the monitor is active again at 9AM the next day) and has a custom message that is sent to myself once it's activated

![Scheduled Downtime definition](https://github.com/jg8810/hiring-engineers/blob/master/downtime1.png)
* The second downtime is planned for weekends - running from 0:00 for 1 day (duration) and repeated on Saturday and Sunday

![Scheduled Downtime definition](https://github.com/jg8810/hiring-engineers/blob/master/downtime2.png)
* In order to test my scheduled downtimes I changed the start time of the first one to fit into my day :)
* Once it got activated I received an Email notification
![Downtime notification](https://github.com/jg8810/hiring-engineers/blob/master/downtimenotification.png)

# Collecting APM Data
* First I had to install pip in order to install Flask on my ec2 instance
```
easy_install pip
pip install flask
```
* Then I took the sample code and created a new file called sampleapp.py
  * In order to work in my environment I changed the port of the Flask application to 80
* I installed the DD Tracing Library according to https://docs.datadoghq.com/tracing/setup/python/ 
* I enabled apm traces for the DD agent in datadog.yaml
* I decided to use the ddtrace-run option in order not to have to change an existing application code (which could be a scenario for a customer, e.g. because of compliance). 
* I started the sample application using:
```
ddtrace-run python sampleapp.py
```
* I then executed some http requests to the endpoints that have been defined in the application
* The stdout/logs of the application already indicated that traces have been reported to DD already, e.g.
```
DEBUG:ddtrace.api:reported 1 services
2018-10-30 11:15:05,746 - ddtrace.api - DEBUG - reported 1 services
INFO:werkzeug:91.231.22.226 - - [30/Oct/2018 11:15:16] "GET / HTTP/1.1" 200 -
2018-10-30 11:15:16,516 - werkzeug - INFO - 91.231.22.226 - - [30/Oct/2018 11:15:16] "GET / HTTP/1.1" 200 -
DEBUG:ddtrace.api:reported 1 traces in 0.00097s
2018-10-30 11:15:16,757 - ddtrace.api - DEBUG - reported 1 traces in 0.00097s
INFO:werkzeug:91.231.22.226 - - [30/Oct/2018 11:15:20] "GET /api/apm HTTP/1.1" 200 -
2018-10-30 11:15:20,640 - werkzeug - INFO - 91.231.22.226 - - [30/Oct/2018 11:15:20] "GET /api/apm HTTP/1.1" 200 -
DEBUG:ddtrace.api:reported 1 traces in 0.00097s
2018-10-30 11:15:20,762 - ddtrace.api - DEBUG - reported 1 traces in 0.00097s
INFO:werkzeug:91.231.22.226 - - [30/Oct/2018 11:16:52] "GET /api/trace HTTP/1.1" 200 -
2018-10-30 11:16:52,895 - werkzeug - INFO - 91.231.22.226 - - [30/Oct/2018 11:16:52] "GET /api/trace HTTP/1.1" 200 -
DEBUG:ddtrace.api:reported 1 traces in 0.00094s
```
## Create a dashboard with both APM and infrastructure metrics
* I created a dashboard called "Flask Dashboard"
* I added graphs that show APM related data coming from ddtrace
```
trace.flask.request.hits.by_http_status
```
* I also added infrastructure related system load metrics to another graph
![APM and Infrastructure Dashboard](https://github.com/jg8810/hiring-engineers/blob/master/dashboardapm.png)

## My Flask app - almost unchanged since I used ddtrace
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
    app.run(host='0.0.0.0', port='80')
```

## Bonus Question - What is the difference between a Service and a Resource?
If we take the sampleapp from above, I would see it as the Service whereas the individual components or routes of the application would represent individual resources. So a Service can be seen as a logical container for multiple resources.

# Final Question
I see a need to monitor business related data - how to correlate and understand data of different sources to see an impact on the business itself (e.g. producing goods/sales/turnover/transactions). Grabbing up your idea of monitoring availabilities of certain resources: as an avid sports fan I would like to find a way to optimize queues (e.g. entrance into stadium, snack bar, etc.)
