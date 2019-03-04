# Answers

## Prerequisites - Environment

	OS: Ubuntu 16.04
	VM: Vagrant w/ VirtualBox

## Collecting Metrics:

*Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.*
	![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/agent-tags-file.png)	
	![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/agent-tags-hostmap.png)

*Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.*
	![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/integration-database.png)
	![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/integration-mysql.png)

*Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.*
![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/agent_check-custom_djcheck.png)	
![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/agent_check-my_metric_status.png)

*Change your check's collection interval so that it only submits the metric once every 45 seconds.*
> Updated the `min_collection_interval` to `45` in the `/etc/datadog-agent/checks.d/custom_djcheck.yaml` file. Default is `15`

*Bonus Question Can you change the collection interval without modifying the Python check file you created?*
![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/agent_check-bonus.png)

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

- Your custom metric scoped over your host.
- Any metric from the Integration on your Database with the anomaly function applied.
- Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket.

<b>Timeboard</b>
![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/Vagrant_API_Timeboard.png)

<b>Script: Timeboard.py</b>
```python
# DogAPI
from dogapi import dog_http_api as api

# API & App Keys
api.api_key = 'XXXXXXXXXX'
api.application_key = 'XXXXXXXXXX'

title = "Vagrant API Timeboard"
description = "Custom Metrics Visualized on a Timeboard using Datadog API's"
template_variables = [{
    'name': 'vagrant',
    'prefix': 'host',
    'default': 'host-vagrant'
}]

graphs = []

my_metric_over_host = {
    "title": "My Metric over Host - Vagrant",
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:vagrant}"}
        ],
        "viz": "timeseries"
    }
}

mysql_integration_with_anomaly_func = {
    "title": "MySQL Performance CPU Time over Host - Vagrant",
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.performance.cpu_time{*},'basic',2)"}
        ],
        "viz": "timeseries"
    }
}

my_metric_with_rollup_sum_for_hour = {
    "title": "My Metric Rolled up Sum for past one hour",
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}.rollup(sum,3600)"}
        ],
        "viz": "timeseries"
    }
}

graphs.append(my_metric_over_host)
graphs.append(mysql_integration_with_anomaly_func)
graphs.append(my_metric_with_rollup_sum_for_hour)
api.create_dashboard(title, description, graphs, template_variables=template_variables)
```
Once this is created, access the Dashboard from your Dashboard List in the UI:

*Set the Timeboard's timeframe to the past 5 minutes*
![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/my_metric_5_min_snapshot.png)

*Take a snapshot of this graph and use the @ notation to send it to yourself.*
![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/snapshot-notation-1.png)
![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/snapshot-notation-2.png)
![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/snapshot-notation-3.png)

*Bonus Question: What is the Anomaly graph displaying?*
> The Anomaly Graph for the MySQL CPU Time shows an average pattern and highlights the various spikes/drops that deviate from a normal (average) behavior.

## Monitoring Data:

*Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.*

*Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:*

- Warning threshold of 500
- Alerting threshold of 800
- And also ensure that it will notify you if there is No Data for this query over the past 10m.

*Please configure the monitor’s message so that it will:*

- Send you an email whenever the monitor triggers.
- Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
- Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

<b>Monitor.json</b>
```json
{
	"name": "Average of my_metric is above threshold on {{host.name}} @ IP: {{host.ip}}",
	"type": "metric alert",
	"query": "avg(last_5m):avg:my_metric{host:vagrant} > 800",
	"message": "{{#is_alert}} <b>ALERT</b>: Average of my_metric is above threshold limit: 800 in the past 5 mins! {{/is_alert}}\n{{#is_warning}} <b>WARNING</b>: Average of my_metric is above: 500 in the past 5 mins! {{/is_warning}}\n{{#is_no_data}} <b>NO_DATA_ALERT</b>: No data has been recorded for my_metric in the past 10 mins! {{/is_no_data}}\n{{#is_warning_recovery}}<b>RECOVERY</b>: Average of my_metric is below: 500 in the past 5 mins! {{/is_warning_recovery}}\n{{#is_recovery}}<b>RECOVERY</b>: Average of my_metric is below: 800 in the past 5 mins! {{/is_recovery}}\nNotify: @joshidheeraj1992@gmail.com",
	"tags": [],
	"options": {
		"notify_audit": false,
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

<b>Monitor Setup Screens:</b>

![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/monitor-screen-1.png)
![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/monitor-screen-2.png)

*When this monitor sends you an email notification, take a screenshot of the email that it sends you.*
<b>Warning Notification:</b>
![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/monitor-warning.png)

<b>Warning Recovery:</b>
![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/monitor-recovery.png)

*Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:*

- One that silences it from 7pm to 9am daily on M-F,
- And one that silences it all day on Sat-Sun.
- Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

<b>Scheduled Downtime: Weekdays Mon-Fri / 7 PM - 9 AM ET:</b>
![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/scheduled_downtime_weekdays.png)

<b>Scheduled Downtime: Weekends Sat-Sun / 24 Hrs:</b>
![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/scheduled_downtime_weekends.png)

## Collecting APM Data:

<b>Flask app instrumented using ddtrace for Datadog’s APM solution:</b>

```python
from flask import Flask
# from ddtrace import patch_all
# patch_all()
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
    print('In app.py __main__')
    app.run(host='0.0.0.0', port='5050')
```

Bonus Question: What is the difference between a Service and a Resource?
> Service is a function that performs a task. Services can be Database, API Endpoints etc. 
> Resource actually describes the action/implementation of a defined service.  
> Services are more like a web application with databases and other integrations whereas Resources are like the actual Queries/Commands used to perform actions.

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

<b>Dashboard:</b>
[APM & Infrastructure Metrics](https://p.datadoghq.com/sb/yqtap2bnkp6at8cv-7e2f6910a444b6349ff92af405689811)

<b>Host Metrics:</b>
![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/infra-1.png)
![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/infra-2.png)

<b>APM Services</b>
![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/apm-3.png)
![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/apm-2.png)
![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/apm-1.png)

<b>APM and Infrastructure Metrics:</b>
![alt text](https://raw.githubusercontent.com/DJ92/hiring-engineers/DheerajJoshi_SolutionsEngineer/screenshots/apm_and_infra_metrics.png)


## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

*Is there anything creative you would use Datadog for?*

<b>As someone who's worked in the payments space for a while, I can definitely anticipate applications of Datadog across the board for payment processing & accepting platforms. Each feature could be used in the following ways:</b>

- An Agent can be setup at a Data Center Group (DCG) level with custom checks for each service running. 
- Payment Switches can have their own monitors in terms of CPU Usage, Load, DB Reads & Writes, etc. to ensure zero downtime.
- Declines/Unauthorized erros can be aggregated with set thresholds for alerting monitors in order to keep track of alerts & downtime.
- Custom Metrics for Authentication, Invoicing, Authorization, Settlement & Disbursement can help track performance as well as risk scores.
- Visualizing support & uptime data can help technical support and evaluation processes as well as help determine escalation policies.

[Braintree Payments Tool](https://github.com/DJ92/braintree-spring-shop)



