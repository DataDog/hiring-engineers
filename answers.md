## Questions

Please provide screenshots and code snippets for all steps.

## Prerequisites - Setup the environment

You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

* You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. [Here are instructions](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#vagrant) for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum `v. 16.04` to avoid dependency issues.

```
OS Info:
Distributor ID:	Ubuntu
Description:	Ubuntu 18.04.3 LTS
Release:	18.04
Codename:	bionic
```

* You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.

Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog. 

![IMG 1](/images/001-tags-config.png)

![IMG 2](/images/002-tags.png)


* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

![IMG 3](/images/003-mysql_int_installed.png)
![IMG 3-1](/images/003-1-mysql-dashboard.png)

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

```
root@enterprise:/etc/datadog-agent/checks.d# cat custom_mymetric.py
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
        from random import randint
        self.gauge('mymetric', (randint(0,1000)), tags=['host:enterprise'])
```

```
root@enterprise:/etc/datadog-agent/checks.d# sudo -u dd-agent -- datadog-agent check custom_mymetric
=== Series ===
{
  "series": [
    {
      "metric": "mymetric",
      "points": [
        [
          1590976235,
          833
        ]
      ],
      "tags": [
        "host:enterprise"
      ],
      "host": "enterprise",
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

    custom_mymetric (1.0.0)
    -----------------------
      Instance ID: custom_mymetric:5ba864f3937b5bad [OK]
      Configuration Source: file:/etc/datadog-agent/conf.d/custom_mymetric.yaml
      Total Runs: 1
      Metric Samples: Last Run: 1, Total: 1
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 0, Total: 0
      Average Execution Time : 0s
      Last Execution Date : 2020-06-01 01:50:35.000000 UTC
      Last Successful Execution Date : 2020-06-01 01:50:35.000000 UTC


Check has run only once, if some metrics are missing you can try again with --check-rate to see any other metric if available.
```
* Change your check's collection interval so that it only submits the metric once every 45 seconds.

```
root@enterprise:/etc/datadog-agent/conf.d# cat custom_mymetric.yaml
init_config:

instances:
  - min_collection_interval: 45
  ```

![IMG 6](/images/006-metric_00.png)

![IMG 7](/images/007-metric_45.png)

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

`Yes you can!!!`

![IMG 8](/images/008-metric-interval-update.png)

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

**https://p.datadoghq.com/sb/dpsd42bam3zstxxy-1bbf5a8ae97bfe274edf84f8df2b6453**

`[note: that notify email was hiden in the code below for security reasons, dashboard has full user email address]`
```
{
    "title": "My Timeseries Demo Dash",
    "widgets": [
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:mymetric{host:enterprise}"
                    }
                ],
                "title": "My Metric (avg) scoped for host enterprise"
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "anomalies(avg:mysql.net.max_connections{*}, 'basic', 2)"
                    }
                ],
                "title": "Avg mysql net max connections"
            }
        },
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:mymetric{*}.rollup(sum, 60)"
                    }
                ],
                "title": "My Metric rollup(sum) period(60)"
            }
        }       
    ],
    "layout_type": "ordered",
    "description": "A cool homemade dash",
    "is_read_only": true,
    "notify_list": [
        "m*****z@yahoo.com"
    ],
    "template_variables": [
        {
            "name": "host",
            "prefix": "host",
            "default": "enterprise"
        }
    ]
}
```

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.

`[Note: I was unable to figure out how to use @ notation in the snapshot request, tried key "notifications"]`
`[Note: request below has personal email hidden for security reasons but used full address in actual request]`


`https://api.datadoghq.{{datadog_site}}/api/v1/graph/snapshot?metric_query=anomalies(avg:mysql.net.max_connections{*}, 'basic', 2)&start=1591044560&end=1591044860&title=anomalies avg mysql net max connectoins&notification=m******z@yahoo.com`

```
{
    "graph_def": "{\"requests\": [{\"q\": \"anomalies(avg:mysql.net.max_connections{*}, 'basic', 2)\"}]}",
    "snapshot_url": "https://p.datadoghq.com/snapshot/view/dd-snapshots-prod/org_421262/2020-06-01/8d26c55db4977b169280e8dea8945190055243a6.png",
    "metric_query": "anomalies(avg:mysql.net.max_connections{*}, 'basic', 2)"
}
```

![anomaly](https://p.datadoghq.com/snapshot/view/dd-snapshots-prod/org_421262/2020-06-01/8d26c55db4977b169280e8dea8945190055243a6.png)

**Bonus Question**: What is the Anomaly graph displaying?

`The anomaly graph is displaying a noticed change for the measured "normal" max connections. The metric had been stable at one connection but then jumped to three.  As configured, after two minutes three becomes the new "normal" for measuring anomalies.`

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

![IMG 10](/images/010-my-metric-alert.png)

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

![IMG 11](/images/011-my-metric-alert-notify.png)

* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

![IMG 12](/images/012-my-metric-notify-email.png)

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  
![IMG 13](/images/013-monitor-silence-7pm-9am.png)

  * And one that silences it all day on Sat-Sun.
  
![IMG 14](/images/014-monitor-silence-weekends.png)

  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

`Silence 7pm-9am monday, tuesday, wednesday, thursday, friday`
![IMG 15](/images/015-setup-email-monitor-silence-7pm-9am.png)

`Silence weekends saturday, sunday`
![IMG 16](/images/016-setup-email-monitor-silence-weekends.png)

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

**service:**
Services are the building blocks of modern microservice architectures - 
broadly a service groups together endpoints, queries, or jobs for the purposes 
of scaling instances.

**resource:**
Resources represent a particular domain of a customer application - they are 
typically an instrumented web endpoint, database query, or background job.

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

**https://p.datadoghq.com/sb/dpsd42bam3zstxxy-b79f6c876e569417a432e34b28995934**

![IMG 17-1](/images/017-flask-infra-dash-15min.png)

![IMG 17-2](/images/017-flask-infra-dash-1hr.png)

Please include your fully instrumented app in your submission, as well.

![IMG 18](/images/018-flask-app-run_ddtrace.png)

ddtrace debug from cli
```
2020-05-31 23:54:01,012 - ddtrace.tracer - DEBUG -
      name flask.request
        id 4408242162714064626
  trace_id 17919790669043516262
 parent_id None
   service flask
  resource GET /
      type web
     start 1590969241.0111501
       end 1590969241.011831
  duration 0.000681s
     error 0
      tags
           flask.endpoint:api_entry
           flask.url_rule:/
           flask.version:1.1.2
           http.method:GET
           http.status_code:200
           http.url:http://127.0.0.1:5050/
           runtime-id:235a36ba79614058a8cb863a136e338d, 471 additional messages skipped
```
Used example python.app provided in insructions:
flaskappdd.py
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


## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

`With the launch of the Space X Dragon in the news, the quest for space is back. Datadog could help in so many ways.  From ground control to rocket/capsule metrics are key.  These metrics drive saftey and success simultaneously. It is key that anomalies are detected and managed effectively. The deep configuration options and scalability within the datadog platform would allow teams to levarge large datasets and display the data needed at the right time.`

## Instructions

If you have a question, create an issue in this repository.

To submit your answers:

* Fork this repo.
* Answer the questions in answers.md
* Commit as much code as you need to support your answers.
* Submit a pull request.
* Don't forget to include links to your dashboard(s), even better links and screenshots. We recommend that you include your screenshots inline with your answers.
