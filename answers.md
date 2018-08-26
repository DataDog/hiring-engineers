# DataDog Solutions Engineer Challenge

## Prerequisites - Setup the environment

* Setup OS/host: I used Vagrant to spin up a Ubuntu VM v. 16.04
* I signed up for Datadog using "Datadog Recruiting Candidate" in the "Company" field
* I installed the Datadog Agent in the VM

![Datadog Agent installation for Ubuntu](https://i.imgur.com/U0kBKo2.jpg)

![Datadog Agent installed](https://i.imgur.com/98pQMR6.jpg)

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

I added the tags in the file /etc/datadog-agent/datadog.yaml

![Datadog Agent config file](https://i.imgur.com/N3MFLTS.png)

Host Map page

![Host Map page](https://i.imgur.com/Dd5DuKv.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I installed MongoDB for the VM, and then I created the user datadog from MongoDB command line

![MongoDB create user](https://i.imgur.com/oW7HrS8.jpg)

I edited the MongoDB configuration file in /etc/datadog-agent/conf.d/mongo.d/conf.yaml

![MongoDB config file](https://i.imgur.com/aMk4j9I.png)

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

I created the file randomcheck.py in /etc/datadog-agent/checks.d/

![randomcheck.py](https://i.imgur.com/K8F394v.png)

and then the file randomcheck.yaml in /etc/datadog-agent/conf.d/

![randomcheck.yaml](https://i.imgur.com/ugTY48F.png)

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

![randomcheck.yaml](https://i.imgur.com/StE3RiP.png)

Please make sure that you restart the agent to be able to collect the metric.

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

I modified the configuration file of randomcheck

## Visualizing Data

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

The script I used to create the timeboard

```
curl -X POST -H "Content-type: application/json"
-d '{
		"graphs": [{
			"title": "Custom metric scoped over host",
			"definition": {
				"viz": "timeseries",
				"requests": [
					{
						"q": "avg:my_metric{*}",
						"type": "line",
						"style": {
							"palette": "dog_classic",
							"type": "solid",
							"width": "normal"
						},
						"conditional_formats": [],
						"aggregator": "avg"
					}]
			}}, {
			"title": "Custom metric with rollup function",
			"definition": {
				"viz": "query_value",
				"requests": [
					{
						"q": "avg:my_metric{*}.rollup(sum, 3600)",
						"type": "line",
						"style": {
							"palette": "dog_classic",
							"type": "solid",
							"width": "normal"
						},
						"conditional_formats": [],
						"aggregator": "avg"
					}
				]
			}}, {
			"title": "MongoDB connection available with anomaly function",
			"definition": {
				"viz": "timeseries",
				"requests": [
					{
						"q": "anomalies(avg:mongodb.connections.available{*}, 'basic', 2)",
						"type": "line",
						"style": {
							"palette": "dog_classic",
							"type": "solid",
							"width": "normal"
						},
						"conditional_formats": [],
						"aggregator": "avg"
					}
				]
			}}],
			"title": "My Timeboard",
			"description": "Timeboard created for Solutions Engineer challenge",
			"template_variables": [],
			"read_only": "True"
	}'
	"https://api.datadoghq.com/api/v1/dash?api_key=67b553698757dea33509fddcd07e62d5&application_key=a541a63cd2a7e233c319308e49ae35ce4411c60a"
```

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.

The Timeboard

![Imgur](https://i.imgur.com/JYKloll.png)

![Imgur](https://i.imgur.com/39isBRd.png)

* **Bonus Question**: What is the Anomaly graph displaying?

The Anomaly graph will identify when the number of connections available for MongoDB change unexpectedly.

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

![Imgur](https://i.imgur.com/jeB9KlX.jpg)

![Imgur](https://i.imgur.com/hNShjZ1.jpg)

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

The alert message
```
The random number has surpassed the predefined threshold and needs to be reconsidered.

{{#is_alert}} The value was over {{threshold}}

- Metric value {{value}}
- The host ip {{host.ip}}

{{/is_alert}}

{{#is_warning}} The value was over {{warn_threshold}}
- Metric value {{value}}
{{/is_warning}}

{{#is_no_data}}
There is no new data during 10 minutes
{{/is_no_data}}

Notify: @nguyenhoainam2k11@gmail.com
```

![Email notification](https://i.imgur.com/6UU6Typ.jpg)

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

The downtime from 7pm to 9am daily on M-F

![Imgur](https://i.imgur.com/lfO9xrM.jpg)

![Imgur](https://i.imgur.com/z5CYwoZ.jpg)

![Imgur](https://i.imgur.com/F1NxXVB.png)

The downtime for all day on Sat-Sun

![Imgur](https://i.imgur.com/liJYjKq.jpg)

![Imgur](https://i.imgur.com/dNZakpi.jpg)

![Imgur](https://i.imgur.com/Oqn43uh.png)

## Collecting APM Data:

The fully instrumented application

```python
from flask import Flask, Response
import blinker as _
import logging
import sys
import time

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)
traced_app = TraceMiddleware(app, tracer, service="simple_flask_app", distributed_tracing=False)

# Add a worker method for APM endpoint
@tracer.wrap(name="apm_work")
def work():
	time.sleep(0.5)
	return 'Getting APM Started'

@app.route('/')
def api_entry():
	return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
	time.sleep(0.3)
	res = work()
	time.sleep(0.3)
	return Response(str(res), mimetype='application/json')

@app.route('/api/trace')
def trace_endpoint():
	return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
```

The APM and Infrastructure Metrics dashboard

![Imgur](https://i.imgur.com/eSvtiRX.png)

[Link to the dashboard](https://app.datadoghq.com/dash/898223/apm-and-infrastructure-metrics?live=true&page=0&is_auto=false&from_ts=1535282434071&to_ts=1535296834071&tile_size=m)

* **Bonus Question**: What is the difference between a Service and a Resource?

A Service is a collection of processes which perform the same job, such as web application, database, and so on. In the other hand, a Resource is a particular action which will be called inside the Service, as a query to a database or a call to a specific API endpoint. In the example Flask application, the whole web application is a service whereas each function provides an API endpoint is a Resource.


## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

- Using Datadog to monitor traffic: anomaly function to detect strange behavior of the traffic (when there is a special event or road accident), reduce traffic jam by detecting bottle neck, etc.

- Connect Datadog to medical support devices or applications: detect unnormal situtation of heart rates, isulin level, etc.

- Integration into smart house: leverage the power of Datadog Dashboard to monitor the temperature, electricity or water usage, unsual movement around the house, etc.
