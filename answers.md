## Collecting Metrics

### Tags
![Tags](/imgs/tags.png)
Added the tags:
- #mytag,
- #env:prod,
- #role:database

### Database Integration
![PostgreSQL Database Integration](/imgs/postgres.png)

### Custom Agent Check
![Custom Agent Check](/imgs/my_metric.png)

~/.datadog-agent/conf.d/my_metric.yaml
```
init_config:
  # submits metric once at most, every 45 seconds
  min_collection_interval: 45

instances:
    [{}]
```

~/.datadog-agent/checks.d/my_metric.py
```
import random
from checks import AgentCheck

class myMetric(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0, 1001))
```

This custom metric that returns a random value between 0 and 1000.

**Bonus** -- How to change collection interval without modifying the Python check file:

In the Agent Config file, configure the `collector_profile_interval` setting.
~/.datadog-agent/datadog.conf
```
collector_profile_interval: 45
```
## Visualizing Data

### Custom Metric Scoped Over Host
Using the Datadog API guides, Postman, and the Postman API Collection, I made a POST request to `https://app.datadoghq.com/api/v1/dash?api_key={MY_API_KEY}&application_key={MY_APP_KEY}` with the following payload:
```
{
    "graphs" : [{
        "title": "Custom Metric (Random Number from 1 - 1000)",
        "definition": {
        "events": [],
        "requests": [
            {
                "q": "avg:my_metric{host:Fannys-MacBook-Air.local}.rollup(sum, 3600)",
                "type": "line",
                "conditional_formats": []
            }
        ]},
        "viz": "timeseries",
        "autoscale": true
    }, {
        "title": "PostgreSQL Requests",
        "definition": {
        "events": [],
        "requests": [
            {
                "q": "anomalies(avg:postgresql.rows_inserted{host:Fannys-MacBook-Air.local}, 'basic', 2)",
                "type": "line"
            }, {
                "q": "anomalies(avg:postgresql.rows_deleted{host:Fannys-MacBook-Air.local}, 'basic', 2)",
                "type": "line"
            }, {
                "q": "anomalies(avg:postgresql.rows_fetched{host:Fannys-MacBook-Air.local}, 'basic', 2)",
                "type": "line"
            }, {
                "q": "anomalies(avg:postgresql.rows_updated{host:Fannys-MacBook-Air.local}, 'basic', 2)",
                "type": "line"
            }, {
                "q": "anomalies(avg:postgresql.rows_returned{host:Fannys-MacBook-Air.local}, 'basic', 2)",
                "type": "line"
            }]
        },
        "viz": "timeseries",
        "autoscale": true
    }],
    "title" : "Solutions Engineer",
    "description" : "Dashboard monitoring custom metrics and PostgreSQL requests",
    "read_only": "True"
}
```
In the payload of the Timeboard POST request, I made two graphs.
1. My Custom Metric, with the rollup function, `.rollup(sum, 3600)`, applied to sum up all the points for the past hour. To scope the metric over my host, I added a template variable from the UI. The Timeseries graph charts the sum at each over hour, over time.
2. The Postgres Database with the anomaly function, `anomalies(avg:postgresql.rows_inserted{host:Fannys-MacBook-Air.local}, 'basic', 2)`, applied.

![5 Minute Snapshot of Timeboard](/imgs/5min_snapshot.png)

**Bonus** What is the Anomaly graph displaying?

The Anomaly algorithm and graph identifies when a metric is behaving differently than it has in the past and takes into account seasonal day-of-week and time-of-day trends. For example, if a metric is unusually high or low during a given time period. The data points that are unusually high or low are shaded a different color from the rest of data points. I used the "Basic" anomaly function, which has a simple computation to determine the expected ranges. I also set a bound of 2, which is like the standard deviation to determine the extent of the normal points.

![PostgreSQL Database with Anomalies Function Applied](/imgs/postgres_anomalies.png)
* The top line is measuring the `rows_returned` metric, the yellow shaded portions represent the anomaly points and the purple portions represent the normal points.
* The bottom line is measuring the `rows_fetched` metric, the pink portions represent the anomaly points, and the yellow portions represent the normal points.


## Monitoring Data

Made POST request to the Create Monitor Datadog API, `https://app.datadoghq.com/api/v1/monitor?api_key={MY_API_KEY}&application_key={MY_APP_KEY}` with the following payload:
```
{
      "type": "metric alert",
      "query": "avg(last_5m):my_metric{host:Fannys-MacBook-Air.local} > 800",
      "name": "My Metric",
      "message": "{{#is_alert}} My metric is too high! Average over 800. @hello@fanny-jiang.com {{/is_alert}} {{#is_warning}} My metric is OK but getting high. Average over 500. @hello@fanny-jiang.com {{/is_warning}} {{#is_no_data}} My metric is not sending any data. Run status check. @hello@fanny-jiang.com {{/is_no_data}} ",
      "tags": [],
      "options": {
      	"notify_no_data": true,
      	"no_data_timeframe": 10,
      	"thresholds": {"critical": 800, "warning": 500}
      }
}
```
* `"query"`, sets the alert on "my_metric" and a threshold value of greater than 800
* `"message"`, uses sets a custom message for alerts and warnings and also emails me
* `"thresholds"`, sets the threshold values for critical to > 800 and warning alerts > 500

**Bonus** Scheduled Downtime
I made a POST request to the Datadog API with the following query:
```
https://app.datadoghq.com/api/v1/downtime?api_key=3f28739dc9067d3da8817cf5efd5859e&application_key=2e01db942359226940704dc5ec70d3676af6a669&start=1510704000&end=1510754400&type=weeks&period=1&week_days=Mon,Tue,Wed,Thu,Fri&scope=host:Fannys-MacBook-Air.local&message=Scheduled%20weekdayß%20downtime%20@hello@fanny-jiang.com
```

This sets a downtime between 7pm and 9am on weekdays, repeating weekly.

For a downtime all day Saturday and Sunday, I made a POST request with the following:
```
https://app.datadoghq.com/api/v1/downtime?api_key=3f28739dc9067d3da8817cf5efd5859e&application_key=2e01db942359226940704dc5ec70d3676af6a669&start=1510981200&end=1511067600&type=weeks&period=1&week_days=Sat,Sun&scope=host:Fannys-MacBook-Air.local&message=Scheduled%20weekend%20downtime%20@hello@fanny-jiang.com
```

For each Downtime request, I set a `start` and `end` time in UNIX timestamp notation, recurrence type, which days, the monitors' scopes, and a message containing a tag to notify me by email of the scheduled downtime.

![Scheduled Downtime](/imgs/downtime.png)

## Collecting APM Data:

While I haven't been able to successfully set up APM tracing, here are the steps that I took to instrument the Flask app to send trace data to Datadog APM:

* Create a new file, `app.py` with the small Flask app
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
    app.run()
```

* Next, I followed the Flask installation instructions to get the app running:
```
$ sudo pip install virtualenv  // virtual environment to run python app
$ . venv/bin/activate  // activate virtual env
$ pip install Flask
$ pip install ddtrace
```

* Since I run Mac OS X and the Datadog APM Tracing Agent doesn't come packaged in the Datadog agent, I downloaded Virtualbox and a Vagrant Ubuntu 12.04 Virtual Machine to run the Datadog agent and the built in tracing agent.

* In the `/etc/dd-agent/datadog.conf` config file, I set `apm_enabled: yes` to enable APM tracing. (I also noticed the syntax within the Datadog docs varied between `apm_enabled: yes` and `apm_enabled: true`, so I tried restarting the DD agent with both configs).

* I confirmed in the Datadog app that it was receiving data from the VM agent.
![VM Dashboard](/imgs/vm_dash.png)

* Here was when I ran into some trouble. I first tried to run the Flask app inside the VM. I decided to go this route first because I thought I needed to run both the app and the Datadog Tracing agent in the same environment. I tried to install Flask and ddtrace in the VM environment, however I got the following errors:

![VM pip install errors](/imgs/pip_install_errors.png)

* To troubleshoot:
1. Update the pip version. Currently on version 1.2.1
2. Update Python version. Currently on version 2.7.6

I was still getting the same errors and since getting the Flask app to run in the VM wasn't working, I decided to keep the DD agent running on the VM and to run the app from my local environment.

To run the app, I ran the following commands:
```
$ . venv/bin/activate
$ ddtrace-run python app.py
```

I also instrumented the app to trace web requests:

hiring-challenge/app.py
```
from ddtrace import tracer

with tracer.trace("web.request", service="my_service") as span:
  span.set_tag("mytag", "my_value")
```

The app was able to run and I was able to navigate to it in the browser and reach the different routes, however I received the following error:

![Connection Refused Error](/imgs/connection_refused.png)

After Googling what a "connection refused" error could mean, I found a resource that suggested that the tracer needs to be configured to the Trace Agent's hostname and port number. I added the following line to my code:

/app.py
```
tracer.configure(hostname=8126)
```
I got a NEW error (which was great!)
![Encode_Error](/imgs/encode/error.png)

After reviewing the API docs more closely, I realized my mistake in configuring the tracer. The hostname takes an argument for the *hostname*. After figuring out the hostname for the VM where the Datadog agent was running from, I corrected the line:
/hiring-challenge/app.py
```
tracer.configure(hostname="127.0.1.1", port=8126)
```

Now that the tracer was pointing to the Datadog tracing agent, I was no longer getting any immediate errors, and GET requests to the different routes logged to the console. After a few seconds, I did end up getting a time out error:

[!Connection Timeout Error](/imgs/connection_timeout.png)

I checked the Datadog Agent state information and the APM log, by running the following commands:
```
$ sudo /etc/init.d/datadog-agent info
$ tail -f /var/log/datadog/trace-agent.log
```

The Agent Status check looked normal, but it wasn't receiving any traces. The Trace Agent log was also showing that data was not being received.

![Agent Status and Trace Logs](/imgs/trace_logs.png)

I've also tried instrumenting the app with tracing middleware and running it with the `flask run` command and get the same errors as above

*Running Flask app with Tracing Middleware*

/app.py
```
from ddtrace.contrib.flask import TraceMiddleware

app = Flask(__name__)
traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)
  ...
```
VM Terminal
```
$ export FLASK_APP=app.py
$ flask run
```
