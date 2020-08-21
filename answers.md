## Prerequisites - Setup the environment

> **_For this challenge I'm using a Linux CentOS 7 server hosted on the Rackspace public cloud. This election was because its was the fastest and easiest way to deploy a server from which I can take snapshots of it and recreate it in case that run into any issue. And the main reason for the Linux distro is due I have a lot of experience working with it and felt more confortable._**

```
[root@server-01 ~]# cat /etc/redhat-release
CentOS Linux release 7.8.2003 (Core)
```

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

> **_On the screenshot you can find the tags on the lower-right corner._**

<img src="https://github.com/erikhvc/hiring-engineers/blob/solutions-engineer/images/Tags.JPG">

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

<img src="https://github.com/erikhvc/hiring-engineers/blob/solutions-engineer/images/mysql.JPG">

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

```
import random
# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge("my_metric",random.randint(0, 1000),tags=["metric_submission_type:gauge"],)
```

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

```
[root@server-01 ~]# cat /etc/datadog-agent/conf.d/my_metric.d/my_metric.yaml
init_config:

instances:
  - min_collection_interval: 45
```

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

> **_This can be modify at instance level as do it in the past question_**

<img src="https://github.com/erikhvc/hiring-engineers/blob/solutions-engineer/images/my_metric.JPG">

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

<img src="https://github.com/erikhvc/hiring-engineers/blob/solutions-engineer/images/Timeboard.JPG">

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

```
{
    "title":"Timeboard",
    "description":"",
    "widgets":
    [
        {
            "id":4277638947435944,
            "definition":
            {
                "type":"timeseries",
                "requests":
                [
                    {
                        "q":"avg:my_metric{*}"
                    }
                ],
                "title":"My Metric",
                "show_legend":false,
                "legend_size":"0"
            }
        },
        {
            "id":4275078505207606,
            "definition":
            {
                "type":"timeseries",
                "requests":
                [
                    {
                        "q":"anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 2)",
                        "display_type":"line",
                        "style":
                        {
                            "palette":"dog_classic",
                            "line_type":"solid",
                            "line_width":"normal"
                        }
                    }
                ],
                "yaxis":
                {
                    "label":"",
                    "scale":"linear",
                    "min":"auto",
                    "max":"auto",
                    "include_zero":true
                },
                "title":"Avg of mysql.performance.cpu_time over *",
                "time":{},
                "show_legend":false
            }
        },
        {
            "id":110550056585550,
            "definition":
            {
                "type":"query_value",
                "requests":
                [
                    {
                        "q":"avg:my_metric{*}.rollup(sum)",
                        "aggregator":"sum"
                    }
                ],
                "title":"Sum Last Hour My Metric",
                "time":{},
                "precision":2
            }
        }
    ],
    "template_variables":
    [
        {
            "name":"server-01",
            "default":"my-host",
            "prefix":"host"
        }
    ],
    "layout_type":"ordered",
    "is_read_only":true,
    "notify_list":[],
    "id":"fi2-yt2-4cr"
}
```

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes

> **_This can be changed clicking on the top-right corner and selecting the requiered timeframe of the drop-down menu._**

<img src="https://github.com/erikhvc/hiring-engineers/blob/solutions-engineer/images/timeborad_5_mins.JPG">

* Take a snapshot of this graph and use the @ notation to send it to yourself.

<img src="https://github.com/erikhvc/hiring-engineers/blob/solutions-engineer/images/graph_snapshot.JPG">

* **Bonus Question**: What is the Anomaly graph displaying?

> **_This graph is displaying when the metric selected start having an unspected behavior, in this case the cpu performance of the mysql database_**

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

<img src="https://github.com/erikhvc/hiring-engineers/blob/solutions-engineer/images/monitor.JPG">

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

```
{
	"id": 0,
	"name": "Metric Monitoring",
	"type": "metric alert",
	"query": "avg(last_5m):avg:my_metric{*} > 800",
	"message": "{{#is_alert}} Metric is above the threshold {{value}} for the host with IP {{host.ip}}!! {{/is_alert}}\n\n{{#is_warning}} Metric is in warning state {{value}} for the host with IP {{host.ip}}!! {{/is_warning}}\n\n{{#is_no_data}} Metric is currently not reporting any data for the host with IP {{host.ip}}!! {{/is_no_data}}\n\n @yoyis_erik@hotmail.com",
	"tags": [],
	"options": {
		"notify_audit": true,
		"locked": false,
		"timeout_h": 0,
		"new_host_delay": 300,
		"require_full_window": true,
		"notify_no_data": true,
		"renotify_interval": "0",
		"escalation_message": "",
		"no_data_timeframe": 10,
		"include_tags": true,
		"thresholds": {
			"critical": 800,
			"warning": 500
		}
	}
}
```

<img src="https://github.com/erikhvc/hiring-engineers/blob/solutions-engineer/images/monitor_alerting.JPG">

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
  
 <img src="https://github.com/erikhvc/hiring-engineers/blob/solutions-engineer/images/monitor_downtime.JPG"> 

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

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

* **Bonus Question**: What is the difference between a Service and a Resource?

> **_A service is the app running on the host using the resources available for it, this resources can be cpu, memory, disk space, iops_**

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

https://p.datadoghq.com/sb/ipxpic8ey7wlh788-ac113c5271312b02504a2ff36636e955

<img src="https://github.com/erikhvc/hiring-engineers/blob/solutions-engineer/images/apm_dashboard.JPG">

Please include your fully instrumented app in your submission, as well.

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

> **_I'll probably try to use it for my smart home devices, trying to check and monitor how often my kids use them and how they do it, like how many calls to alexa they made as well the average time the light switches are on._**

<img src="https://github.com/erikhvc/hiring-engineers/blob/solutions-engineer/images/Alexa.jpeg">
