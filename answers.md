## Environment

* **Laptop:** macOS High Sierra
* **VM:** Vagrant Ubuntu 12.04

## Collecting Metrics

~~Screenshot of your host and its tags on the Host Map page in Datadog~~
~~Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.~~

<a href="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%201%20-%20host.png" title="Datadog Host Map page">
<img src="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%201%20-%20host.png" width="500" alt="datadog_host_map_page"></a>

~~Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.~~

*dd-agent/checks.d/my_first_metrics.py*

```
import random

from checks import AgentCheck
class MyFirstMetricsCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_first_metrics.my_metric', random.randint(0, 1000))
```

~~Change your check's collection interval so that it only submits the metric once every 45 seconds.
Bonus Question - Can you change the collection interval without modifying the Python check file you created?~~

*dd-agent/conf.d/my_first_metrics.yaml*

```
init_config:
    min_collection_interval: 45

instances:
    [{}]
```

- [ ] TODO: fix check interval - metric is submitting every 60 seconds as default check interval is 20 seconds

## Visualizing Data

~~Utilize the Datadog API to create a Timeboard that contains:
Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket~~

<a href="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%202%20-%20timeboard.png" title="Datadog Timeboard">
<img src="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%202%20-%20timeboard.png" width="500" alt="datadog_timeboard"></a>

~~Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timemboard.~~

```
require 'rubygems'
require 'dogapi'

dog = Dogapi::Client.new(ENV['DATADOG_API_KEY'], ENV['DATADOG_APP_KEY'])

title = 'My First Timeboard (Ruby API)'
description = 'Woop woop.'
graphs = [
{
    "definition" => {
        "events" => [],
        "requests" => [{
            "q" => "sum:my_first_metrics.my_metric{host:karnoult.datadog}"
        }],
        "viz" => "timeseries"
    },
    "title" => "Graph - my first metric"
},
{
    "definition" => {
        "events" => [],
        "requests" => [{
            "q" => "anomalies(sum:postgresql.rows_returned{host:karnoult.datadog}, 'basic', 2)"
        }],
        "viz" => "timeseries"
    },
    "title" => "Graph - postgres connections"
},
{
    "definition" => {
        "events" => [],
        "requests" => [{
            "q" => "sum:my_first_metrics.my_metric{host:karnoult.datadog}.rollup(sum,3600)"
        }],
        "viz" => "timeseries"
    },
    "title" => "Graph - my first metric (rollup)"
}
]

dog.create_dashboard(title, description, graphs)
```

~~Once this is created, access the Dashboard from your Dashboard List in the UI:
Set the Timeboard's timeframe to the past 5 minutes
Take a snapshot of this graph and use the @ notation to send it to yourself.~~

<a href="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%203%20-%20snapshot.png" title="Datadog Snapshot">
<img src="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%203%20-%20snapshot.png" width="500" alt="datadog_snapshot"></a>

Link to the dashboard: [here](https://app.datadoghq.com/dash/589005/my-first-timeboard-ruby-api)

~~Bonus Question: What is the Anomaly graph displaying?~~

Anomaly detection shows behaviors that the datadog agent doesn't feel like they're right.
In my case, there's not enough data (no real trend) for the anomaly detection to work:

<a href="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%2010%20-%20anomaly.png" title="Datadog Anomaly">
<img src="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%2010%20-%20anomaly.png" width="500" alt="datadog_anomaly"></a>

## Monitoring Data

~~Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.
Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
Warning threshold of 500
Alerting threshold of 800
And also ensure that it will notify you if there is No Data for this query over the past 10m.~~

<a href="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%204%20-%20monitoring.png" title="Datadog Monitoring">
<img src="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%204%20-%20monitoring.png" width="500" alt="datadog_monitoring"></a>

```
{
	"name": "My Metric is acting a little weird",
	"type": "metric alert",
	"query": "avg(last_5m):avg:my_first_metrics.my_metric{host:karnoult.datadog} > 800",
	"message": "{{#is_alert}}\nAlert, I repeat, this is an alert: {{value}} {{comparator}} {{threshold}}\nThis alert is related to the following host: Host {{host.name}} with IP {{host.ip}}\n{{/is_alert}}\n\n{{#is_warning}}\nWarning warning\n{{/is_warning}}\n\n{{#is_no_data}}\nThere is No Data over the past 10m.\n{{/is_no_data}}\n\n@kevin.arnoult@gmail.com",
	"tags": [],
	"options": {
		"timeout_h": 0,
		"notify_no_data": true,
		"no_data_timeframe": 10,
		"notify_audit": false,
		"require_full_window": true,
		"new_host_delay": 300,
		"include_tags": false,
		"escalation_message": "",
		"locked": true,
		"renotify_interval": "0",
		"evaluation_delay": "",
		"thresholds": {
			"critical": 800,
			"warning": 500
		}
	}
}
```

~~Please configure the monitor’s message so that it will:
Send you an email whenever the monitor triggers.
Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
When this monitor sends you an email notification, take a screenshot of the email that it sends you.~~

<a href="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%205%20-%20emails.png" title="Datadog Monitoring - emails">
<img src="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%205%20-%20emails.png" width="500" alt="datadog_monitoring_emails"></a>

<a href="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%206%20-%20alert.png" title="Datadog Monitoring - alert">
<img src="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%206%20-%20alert.png" width="500" alt="datadog_monitoring_alert"></a>

~~Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.
Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.~~

<a href="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%207%20-%20downtime.png" title="Datadog Downtime">
<img src="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%207%20-%20downtime.png" width="500" alt="datadog_downtime"></a>

<a href="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%207%20-%20downtime_1.png" title="Datadog Downtime 1">
<img src="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%207%20-%20downtime_1.png" width="500" alt="datadog_downtime_1"></a>

*(I've moved it sooner in order to test it)*

<a href="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%207%20-%20downtime_2.png" title="Datadog Downtime 2">
<img src="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%207%20-%20downtime_2.png" width="500" alt="datadog_downtime_2"></a>

---

## Collecting APM Data:

~~Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:~~
~~Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.~~

https://app.datadoghq.com/screen/291623/apm-and-infrastructure-screenboard

<a href="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%208%20-%20screenboard.png" title="Datadog Screenboard">
<img src="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%208%20-%20screenboard.png" width="500" alt="datadog_screenboard"></a>

~~Please include your fully instrumented app in your submission, as well.~~

```
#/vagrant/bilobaba/config/initializers/datadog-tracer.rb

Rails.configuration.datadog_trace = {
  auto_instrument: true,
  auto_instrument_redis: true,
  default_service: 'my-rails-app'
}
```

```
#/vagrant/bilobaba/Gemfile

gem 'ddtrace
```

~~Bonus Question: What is the difference between a Service and a Resource?~~

Services are the components of the app (ex: the postgres db in my bilobaba app)
Resources are the use of these services  (ex: the queries to that bilobaba db)

<a href="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%209%20-%20apm.png" title="Datadog APM">
<img src="https://github.com/karnoult/hiring-engineers/blob/master/Datadog%20-%209%20-%20apm.png" width="500" alt="datadog_apm"></a>

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?
