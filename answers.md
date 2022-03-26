## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

![Host Tags](/images/host-tags.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

![MySql Integration](/images/mysql-integration.png)

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

I've provided my .yaml and .py files here: [my_metric files](/documents/custom_check)

![My Metric](/images/mymetric.png)

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

![Min Collection Interval](/images/min_collection_interval.png)

**Finished Metric Report**

![My Metrics Graph](/images/mymetric-graph.png)

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

Yes, this can be adjusted on the Metrics Explorer page. Choose your metric and then hit Edit. Under the "Metadata" section, you can input an interval.

![Bonus Question_1](/images/interval-option.png)

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Dashboard Link: https://p.datadoghq.com/sb/a81c4026-aae6-11ec-8eba-da7ad0900002-3df9ebf12895529dad359fec03a4a7bf

![Timeboard](/images/timeboard.png)

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

[Timeboard cURL Command](/documents/timeboard-api-request.txt)

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes

![Timeboard_Last5](/images/timeboard-last5.png)

* Take a snapshot of this graph and use the @ notation to send it to yourself.

![Snapshot](/images/snapshot.png)

![Snapshot Email](/images/snapshot-email.png)

* **Bonus Question**: What is the Anomaly graph displaying?

The way I have this graph set up displays any data that is "2" standard deviations off from the predicted values. This can help determine if current behavior of a metric is different than previous trends and patterns. For my graph specifically, the purple parts of the line graph are all CPU performance values within the predicted values, starting from 6.7e5 n% as a min. The red parts of the lines inidicate all instances in time when the performance was above or below those values.

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

![Monitor](/images/monitor.png)
[Monitor Export JSON](/documents/monitor-export.json)

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

![Monitor Warning Email](/images/warning-email.png)

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

![Downtimes](/images/downtimes.png)

I wanted to test out both options for scheduling. Here are the settings for both in the UI:

![Weekday Settings](/images/mon-fri-downtime.png)
![Weekend Settings](/images/sat-sun-downtime.png)

Emails for setting up both:

![Weekday Downtime Email](/images/downtime-email.png)
![Weekend Downtime Email](/images/weekend-downtime-email.png)

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

A **resource** is a particular action of a **service**. This can be a single endpoint or query that is triggered as a part of said service. A **service** is a set of processes doing the same job. Services group together endpoints, queries, or jobs to help scale instances and build one's application. An example would be a web framework or database.

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

I came across an open-source network automation tool called eNMS (https://www.enms.io/). Using this, I created some trace logs that I was able to record and add to this dashboard here. I have also added the `dd-trace` command I used in my virtual machine to get these logs running.

[ddtrace command](/documents/apm-request.txt)

Dashboard Link: https://p.datadoghq.com/sb/a81c4026-aae6-11ec-8eba-da7ad0900002-ca79ddeec739c80e43d5065126936ae8

![APM Dashboard](/images/apm-infra.png)

SQLite APM Service 

![SQLite APM Service](/images/sqlite-service.png)

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

One big problem users of the popular MMORPG, Final Fantasy 14, have whenever they launch a new patch or expansion are login issues. Not only do these players have to wait until the servers allow them to log in, they have to sit in front of their screen for an undetermined amount of time. This is because while they are queued to log in, there are times where the queue can error out and boot the player out. If they are lucky, they can quickly log back in and get their spot back. If not, it's to the back of the line they go and this whole process can end up taking hours.

![FFXIV Login Queue](/images/ffxiv-login-queue.jpg)

An idea I had would be to create a an application that players can use to get notified when their character has successfully logged in or if an they've encountered an error. An API would probably need to be built to attempt to log in and return status updates on the queue. This dashboard can also include metrics such as the average wait times to login, server statuses, and different uptimes. Users on this shared dashboard would be able to sign up for notifications if a server went down or not and if their attention is required for the login process.
