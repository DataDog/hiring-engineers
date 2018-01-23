## Questions

## Prerequisites - Setup the environment

I set up a Vagrant Ubuntu 12.04 VM, I signed up for Datadog as Guillaume Raimbault and I installed the Datadog Agent.
<img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/Vagrant_ubuntu_with_datadog.jpg" width="500">

<img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/datadogAgentReporting.jpg" width="500">

## Collecting Metrics:

* I added tags #region:europe, #town:sannois, #special_tag in etc/dd-agent/datadog.conf
<img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/tagInDatadogConf.jpg" width="500">
<img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/tagsInDatadogMap.jpg" width="500">

* I installed MySQL and the respective integration.
<img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/mysqlInstalled.jpg" width="500">
<img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/mysqlIntegrationWorking.jpg" width="500">
<img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/mysqlIntegration.png" width="200">
<img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/mysqlDashboard.jpg" width="500">

* I created a custom Agent check by creating /etc/dd-agent/checks.d/my_metric.py and /etc/dd-agent/conf.d/my_metric.yaml. The corresponding files are in folder <a href="https://github.com/gRaimbault/hiring-engineers/tree/solutions-engineer/code">code</a>.
* I changed the collection interval in my_metric.yaml .

* **Bonus Question** The only solution I found to modify the collection interval is by modifying the yaml files.

## Visualizing Data:

* I created the script timeboardCreation.py (in folder <a href="https://github.com/gRaimbault/hiring-engineers/tree/solutions-engineer/code">code</a>) to create the corresponding Timeboard.

Once this is created, access the Dashboard from your Dashboard List in the UI:

* The minimum Timeboard's timeframe in the UI seems to be the past hour.
* Snapshot of the graph with the @ notation to sent it to myself:
<img src="https://github.com/gRaimbault/hiring-engineers/blob/solutions-engineer/images/graphSnapshot.jpg" width="500">

* **Bonus Question**: The anomaly graph compare expected values to observed values in order to highlight anomalies.

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

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

* **Bonus Question**: What is the difference between a Service and a Resource?

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well. 

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?


