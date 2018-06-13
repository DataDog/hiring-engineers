## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

#### Agent Config File

![Agent Config File](images/agentconfig.png)

#### Host Map Visualization

![Host Map Visualization](images/hostmap.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

#### MongoDB Integration

![MongoDB Integration](images/mongodbintegration.png)

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

⋅⋅⋅The following script creates a metric called 'my_metric' for the app 'first'. Its check generates a random value between 0 and 1000.

**my_metric.py:**

```python
from checks import AgentCheck
from random import randint
class MetricCheck(AgentCheck):
	def check(self, instance):
		self.gauge('first.my_metric', randint(0, 1000))
```

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

**my_metric.yaml:**

```
init_config:

instances:
  - min_collection_interval: 45
```

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

⋅⋅⋅The collection interval can be changed by configuring min_collection_interval of each check instance to a positive numerical value.

#### Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

**timeboard.py:**

```python
from datadog import initialize, api

options = {
    'api_key': '5077ea49d30f7c6e2b1e47a2eb9e701d',
    'app_key': '07d17cb9388be688455f1e13b8f3067e7a659ca0'
}

initialize(**options)

title = "My Metric Data + MongoDB Collections"
description = "Values generated every 45 sec + MongoDB collections."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:first.my_metric{*}"},
            {"q": "anomalies(avg:mongodb.stats.collections{*}, 'basic', 2)"},
            {"q": "avg:first.my_metric{*}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "Random Values Over Time"
}]

template_variables = [{
    "name": "timeboard",
    "prefix": "my_metric",
    "default": "host:Ralph-PC"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)


```

#### MongoDB Configuration (located in /conf.d/mongo.d/conf.yaml)

```
init_config:
instances:
  - server: mongodb://datadog:NMexkkPoWYv7p4hy86kRyaOG@localhost:27017/admin
    additional_metrics:
      - collection       # collect metrics for each collection
      - metrics.commands
      - tcmalloc
      - top
```

Once the Timeboard is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.

#### Generated Timeboard (last 5 minutes)

![Generated Timeboard](images/last5min.png)

#### Timeboard Emailed to Self

![Emailed Timeboard](images/senttimeboard.png)

* **Bonus Question**: What is the Anomaly graph displaying?

The anomaly graph displays the metric visualization plus any areas that deviate from the expected flow of data (in the case of my graph, deviations are colored red). Since my timeboard was visualizing Mongo collection data for my admin db, an anomaly occurred as I was generating more collections for that db since initially, there were little to none within the time frame.

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

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

* **Bonus Question**: What is the difference between a Service and a Resource?

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?
