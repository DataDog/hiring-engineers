<img src="images/datadog_logo_share_tt.png" width="300" >

# Introduction to Datadog - Ryan Donat

## Topics:
* Collecting Metrics
  * How can we use Datadog to collect metrics from our system? 
* Visulizing Data
  * Once we have collected Metrics, how can we use Datadog to visulize them?
* Monitoring Data
  * When your data is visulized exactly how you want it, how do you set up Monitors so that someone does not need to be watching the dashboard indefinitely for anomolies?
* Collecting APM Data
  * Now that we are collecting,visulizing, and monitoring our data and metrics, what else is there? Application Performance Monitoring lets you deep dive into your application's performance.
  
**NOTE:** As always, documentation is our friend, throughout this Introduction there will be many references and quotes to and from documentation that explains these topics in greater depth.

## Collecting Metrics:

### Datadog provides three main types of integrations that allow us to collect metrics:

* Agent-based integrations are installed with the Datadog Agent and use a Python class called check to define the metrics to collect.
* Authentication (crawler) based integrations are set up in the Datadog App where you provide credentials for obtaining metrics with the
* API. These include popular integrations like Slack,AWS,Azure, and PagerDuty.
Library integrations use the Datadog API to allow you to monitor applications based on the language they are written in, like Node.js, or Python.

### Example of Authentication based integration:
* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
* SCREENSHOT OF Datadog and DynamoDb

### Agent based integrations with custom Checks:
* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
  * Custom checks are well suited to collect metrics from custom applications or unique systems. However, if you are trying to collect metrics from a generally available application, public service, or open source project, it is recommended that you create a full fledged Agent Integration.
  * https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6
  * https://docs.datadoghq.com/agent/
* Change your check's collection interval so that it only submits the metric once every 45 seconds.
  * https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6#collection-interval
* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

### How do we keep all of the data comming into Datadog many different host organized?
* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
  * Tags are a way of adding dimensions to metrics, so they can be filtered, aggregated, and compared in Datadog visualizations. Using tags enables you to observe aggregate performance across a number of hosts and (optionally) narrow the set further based on specific elements. In summary, tagging is a method to observe aggregate data points.
  * Typically, it’s helpful to look at containers, VMs, and cloud infrastructure at the “service” level in aggregate. For example, it’s more helpful to look at CPU usage across a collection of hosts that represents a service, rather than CPU usage for server A or server B separately. Containers and cloud environments regularly churn through hosts, so it is critical to tag these to allow for aggregation of the metrics you’re getting.
  * https://docs.datadoghq.com/tagging/

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Once this is created, access the Dashboard from your Dashboard List in the UI:

* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.
* **Bonus Question**: What is the Anomaly graph displaying?

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

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

* **Bonus Question**: What is the difference between a Service and a Resource?

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?
