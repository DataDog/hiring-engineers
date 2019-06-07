Answers
=======

## Prerequisites - Setup the environment

Environment setup on an AWS EC2 Amazon Linux 2 instance


## Collecting Metrics:

Qn: Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

1. Add tags in /etc/datadog-agent/datadog.yaml

```yaml
tags:
  - jtag
  - env:test
  - role:mongo
```

2. Restart Agent
```
sudo service datadog-agent restart   # enable any changes to config, v fast!
sudo datadog-agent status            # check agent came up properly
```
![hosttags](images/hosttags1.png)  

<br>

Qn: Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

1. Install and config Mongo on host
```sh
yum install -y mongodb-org
service mongod start
mongo
# mongoCLI
db.createUser({
  user: "admin",
  pwd: "XXXXX",
  roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
})
db.createUser({
  "user":"datadog",
  "pwd": "XXXXX",
  "roles" : [
    {role: 'read', db: 'admin' },
    {role: 'clusterMonitor', db: 'admin'},
    {role: 'read', db: 'local' }
  ]
})
```
2. Insert a couple of documents
```
db.jdb.insertMany([
{ item: "apple", age: 2, size: { h: 14, w: 21, uom: "cm" }, tags: [ "blank", "red" ] },
{ item: "banana", qty: 50, size: { h: 8.5, w: 11, uom: "in" }, tags: [ "red", "blank" ] },
{ item: "carrot", qty: 100, size: { h: 8.5, w: 11, uom: "in" }, tags: [ "red", "blank", "plain" ] },
{ item: "donkey", qty: 75, size: { h: 22.85, w: 30, uom: "cm" }, tags: [ "blank", "red" ] },
{ item: "elderberry", qty: 45, size: { h: 10, w: 15.25, uom: "cm" }, tags: [ "blue" ] }
]);
```
3. edit /etc/datadog-agent/conf.d/mongo.d/conf.yaml
```yaml
- server: mongodb://datadog:XXXXX@localhost:27017/admin
  additional_metrics:
  - collection       # collect metrics for each collection
  - metrics.commands
  - tcmalloc
  - top
```
4. Restart agent
```
sudo service datadog-agent restart
sudo datadog-agent status           # check mongo part is up
```
![MongoDBdash](images/MongoDBoverview.png)

<br>


Qn: Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

1. Create conf.d/my_metric.yaml
```yaml
- init_config:
  instances: [{}]
```

2. Create checks.d/my_metric.py
```python
try:
    from checks import AgentCheck
except ImportError:
    from datadog_checks.checks import AgentCheck

__version__ = "1.0.1"

import random
class MyMetricCheck(AgentCheck):
    def check(self, instance):
       data = random.randint(0,1000)
       self.gauge('jbucket.my_metric', data)
```
<br>

Qn: Change your check's collection interval so that it only submits the metric once every 45 seconds.

1. modify conf.d/my_metric.yaml
```yaml
- instances:
  - min_collection_interval: 45 (means metric could be collected as often as every 45secs)
```
2. Restart agent
3. Verify check is running
```
sudo -u dd-agent -- datadog-agent check my_metric
```
<br>
* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?  <br>
Did not modify py code.

<br>
<br>

## Visualizing Data:

POSTMAN was used to call APIs for the following section

Utilize the Datadog API to create a Timeboard that contains:
Qn: Your custom metric scoped over your host.

```json
https://api.datadoghq.{{datadog_site}}/api/v1/dashboard?api_key={{datadog_api_key}}&application_key={{datadog_application_key}}
{
    "title": "jdasb",
    "widgets": [
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:jbucket.my_metric{host:i-0452ffd2a77f4ebb2}"
                    }
                ],
                "title": "My Metric/host"
            }
        }
    ],
    "layout_type": "ordered",
    "description": "my_metric scoped over host",
    "is_read_only": true
}
```
<br>
Qn: Any metric from the Integration on your Database with the anomaly function applied.  
Qn: Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket  
Use update dashboard API to push out changes  

```json
https://api.datadoghq.{{datadog_site}}/api/v1/dashboard/:DASHBOARD_ID?api_key={{datadog_api_key}}&application_key={{datadog_application_key}}
{
    "title": "jdasb",
    "widgets": [
        {
            "definition": {
                "type": "timeseries",
                "requests": [{ "q": "avg:jbucket.my_metric{host:i-0452ffd2a77f4ebb2}" }],
                "title": "My Metric/host"
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "requests": [{ "q": "anomalies(avg:mongodb.connections.totalcreated{*}, 'basic', 2)" }],
                "title": "Mongo Total Conns (Anomalized)"
            }
        },
        {
            "definition": {
                "type": "query_value",
                "requests": [{ "q": "avg:jbucket.my_metric{*}.rollup(sum, 3600)" }],
                "title": "Sum of My Metric over last hour",
                "precision": 0
            }
        }
    ],
    "layout_type": "ordered",
    "description": "cool datadog vizualizations",
    "is_read_only": true
}
```
![dashboard](images/jdasb.png)

Qn: Once this is created, access the Dashboard from your Dashboard List in the UI:
    Set the Timeboard's timeframe to the past 5 minutes
![dashboard](images/jdasb2_5min.png)

Qn: Take a snapshot of this graph and use the @ notation to send it to yourself.
![dashboard](images/jdasb3.png)

* **Bonus Question**: What is the Anomaly graph displaying? <br>
The grey area shows the boundary of 2 standard deviations from the metric of total mongoDB connections


## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Qn: Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

Setup monitor
![monitor](images/monitor1.png)

Qn: Please configure the monitor’s message so that it will:
* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

![monitor](images/monitor2.png)

Monitor message template below.
```
{{#is_alert}}
Value of my_metric hit {{value}} on {{host.ip}}.
Please do something about it. Maybe seed the random generator? 
{{/is_alert}}

{{#is_warning}}
Value of my_metric hit {{value}}. Relax, just a heads up :)
{{/is_warning}}

{{#is_no_data}}
No data has been seen for the past 10mins. Please check.
{{/is_no_data}}
```


Qn: When this monitor sends you an email notification, take a screenshot of the email that it sends you.

![monitor alert](images/monitoralert.png)

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor: <br>
  Qn: One that silences it from 7pm to 9am daily on M-F,

![downtime](images/downtime1.png)

  Qn: And one that silences it all day on Sat-Sun.

![downtime](images/downtime2.png)

  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

![downtime](images/downtime3.png)



## Collecting APM Data:

Used the provided Flask app without change to simulate the scenario where the dev team is unwilling to make direct changes to their code

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

Config Datadog agent to collect traces
1. Edit datadog.yaml (apm sect is right at bott)
```yaml
   apm_config:
      enabled: true
```

2. Restart agent

3. Use pip to install ddtrace and run app
```
./pip install ddtrace
sudo ./pip install flask
./python flash.py                # test run flask app
./ddtrace-run ./python flash.py  # run flash app instrumented by ddtrace
```
4. Generate some traffic
```
for i in {1..30}; do curl localhost:5050/api/apm; curl localhost:5050/api/trace; done
```

![apm services](images/apm1.png)
Main Services screen
![apm services detailed](images/apm2.png)
Detailed Services Page
![apm traces](images/apm3.png)
APM Trace

* **Bonus Question**: What is the difference between a Service and a Resource? <br>
A Service is a set of processes that perform the same job, something like a microservice. <br>
A Resource is a subset of a service that does a particular action (eg. endpoint or query).

Qn: Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

![apm dashboard](images/APMdasb.png)
http://app.datadoghq.com/screen/722324 <br>
Public links only can be generated for Screenboards.


## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

Using Datadog Python library and public realtime APIs (eg. data.gov.sg) custom metrics can be easily graphed and  anomalities in carpark and taxi availability highlighted for better travel optimization.
Monitoring Smart Home electricity meters and IoT devices would also reveal very cool trends and help save electricity usage.
