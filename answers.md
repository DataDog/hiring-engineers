

#Single Sign On to Datadog Home Dashboard

You can login to my Datadog trial instance by doing SAML IdP initiation request via:

Okta IdP page: https://dev-998003.oktapreview.com/

![SSO_Datadog_login](AWS%20instance/Collecting%20Metrics/login.png)

Kindly enter the username,

Username: datadog_eval@okta.com

then the password,

Password: SEChallenge123!

Once successful, you should be redirected to the Okta Dashboard page and inside the said page will have a Datadog icon. 
![SSO_Datadog](AWS%20instance/Collecting%20Metrics/SSO.png)

Please click the Datadog icon or chiclet and you should be Single Sign On to Datadog.

![SSO_Datadog_Home](AWS%20instance/Collecting%20Metrics/DatadogHome.png)

## Collecting Metrics:
* Download the Datadog Agent
    * After logging in the Datadog dashboard, Look at the left hand navigator and hover Integrations.
    * Click Agent
    * You should be taken to a page: [install agent] https://app.datadoghq.com/account/settings#agent
    * Select the server you want to install the agent. For this exercise, we will use Ubuntu hence click Ubntu.
    * You should see the page below and execute the steps provided as instructed within your server.
        ![install_datadog_agent](AWS%20instance/Collecting%20Metrics/installDatadogAgent.png)

* Setting up the Datadog Agent
    * Check whether your Datadog agent is running by invoking the following command: <br />
            __sudo service datadog-agent status__ <br />
      if the agent is not running, then you can invoke the following command:<br />
            __sudo service datadog-agent start__ <br />
    * Proceed to the configuration filepath of the Datadog Agent. Normally in Ubuntu, it should be located at, 
        The configuration files and folders for the Agent are located in:<br />
            __/etc/datadog-agent/datadog.yaml__ <br />
    * Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

        Refer to sample datadog yaml file: [Datadog_YAML](https://github.com/hawjefferson/hiring-engineers/blob/master/AWS%20instance/Collecting%20APM%20Data/datadog.yaml)

        Set the host's tags (optional)
        tags:
        - env_se_os:ubuntu
        - env_se_owner:jeffhaw
        - env_se_function:se_tech_challenge
        - env_provider:aws
![SSO_Datadog_Home](AWS%20instance/Collecting%20Metrics/host-tags.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
    * installing MySQL via terminal by invoking the following command: __sudo apt-get install mysql-server__
        All done! 
        ```SQL service
        ubuntu@ip-172-31-13-132:/etc/datadog-agent$ systemctl status mysql.service
        ● mysql.service - MySQL Community Server
        Loaded: loaded (/lib/systemd/system/mysql.service; enabled; vendor preset: en
        Active: active (running) since Sun 2019-02-03 11:39:15 UTC; 1min 27s ago
        Main PID: 11406 (mysqld)
        CGroup: /system.slice/mysql.service
                └─11406 /usr/sbin/mysqld

        mysqladmin  Ver 8.42 Distrib 5.7.25, for Linux on x86_64
        Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

        Oracle is a registered trademark of Oracle Corporation and/or its
        affiliates. Other names may be trademarks of their respective
        owners.

        Server version		5.7.25-0ubuntu0.16.04.2
        Protocol version	10
        Connection		Localhost via UNIX socket
        UNIX socket		/var/run/mysqld/mysqld.sock
        Uptime:			2 min 13 sec

        Threads: 1  Questions: 5  Slow queries: 0  Opens: 115  Flush tables: 1  Open tables: 34  Queries per second avg: 0.037
         ```
![SQL_Datadog_InfraView](AWS%20instance/Collecting%20Metrics/mysql_infrastructure_list.png)
![SQL_Datadog_DashboardView](AWS%20instance/Collecting%20Metrics/mysql_dashboard_overview.png)
* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
    Refer to [Datadog_Custom_Metric] https://github.com/hawjefferson/hiring-engineers/blob/master/AWS%20instance/Collecting%20Metrics/myMetric.py
```Python
#import random modules to generate number between 0 to 1000
import random
# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from old versions of the Agent...
    from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"


class myMetricCheck(AgentCheck):
    def check(self, instance):
       self.gauge('custom_myMetric',random.uniform(0, 1000))
```
![Metric_view](AWS%20instance/Collecting%20Metrics/custom_myMetric.png)
* Change your check's collection interval so that it only submits the metric once every 45 seconds.

Jefferson Haw: Please refer to  [Datadog_Custom_Metric_YAML] https://github.com/hawjefferson/hiring-engineers/blob/master/AWS%20instance/Collecting%20Metrics/myMetric.yaml 

```Python
        init_config:

        instances:
            - min_collection_interval: 45

```

* Bonus Question Can you change the collection interval without modifying the Python check file you created?

Jefferson Haw: create a myMetric.yaml file wherein you can set the interval collection frequency of the custom check. This is better rather than programmatically implementing this within the python code.

Jefferson Haw: Please refer to  [Datadog_Custom_Metric_YAML] https://github.com/hawjefferson/hiring-engineers/blob/master/AWS%20instance/Collecting%20Metrics/myMetric.yaml 

```Python
        init_config:

        instances:
            - min_collection_interval: 45

```

# Visualizing Data:
Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Jefferson Haw: Please see https://github.com/hawjefferson/hiring-engineers/blob/master/AWS%20instance/Visualizing%20Data/TimeboardRequestJSON.json <br />
and https://github.com/hawjefferson/hiring-engineers/blob/master/AWS%20instance/Visualizing%20Data/TimeboardResponseJSON.json <br />
for API script. I've used curl command via postman using JSON objects.

* Once this is created, access the Dashboard from your Dashboard List in the UI:
Jefferson Haw: Please see the screenshow below

![Timeboard](AWS%20instance/Visualizing%20Data/Timeboard.png)

* Set the Timeboard's timeframe to the past 5 minutes
Jeffeson Haw: Please see the modified Timeboard using 5 minutes interval
![Timeboard_5mins](AWS%20instance/Visualizing%20Data/Timeboard_5mins.png)

* Take a snapshot of this graph and use the @ notation to send it to yourself.
Jefferson Haw: Please see Graph
![Timeboard_5mins](AWS%20instance/Visualizing%20Data/GraphNotification.png)

* Bonus Question: What is the Anomaly graph displaying?
Jefferson Haw: It tries to dentify when a metric is behaving differently than it has in the past, taking into account trends, seasonal day-of-week, and time-of-day patterns. It is well-suited for metrics with strong trends and recurring patterns that are hard or impossible to monitor with threshold-based alerting.

Here is a sample JSON script that allows you to create a Anomaly within Datadog.

```JSON
{
	"name": "MySQL Performance CPU Time High",
	"type": "query alert",
	"query": "avg(last_4h):anomalies(avg:mysql.performance.cpu_time{sql_server_function:sechallenge_database}, 'basic', 2, direction='both', alert_window='last_15m', interval=60, count_default_zero='true') >= 0.9",
	"message": "MySQL CPU Performance is high\n\n{{#is_alert}} CPU performance usage is too high! {{/is_alert}}\n\nCheck with MySQL Admin for any questions.\n@jeff.haw.23@gmail.com",
	"tags": [],
	"options": {
		"notify_audit": false,
		"locked": false,
		"timeout_h": 0,
		"silenced": {},
		"include_tags": true,
		"no_data_timeframe": 10,
		"require_full_window": true,
		"new_host_delay": 300,
		"notify_no_data": true,
		"renotify_interval": 0,
		"escalation_message": "",
		"threshold_windows": {
			"recovery_window": "last_15m",
			"trigger_window": "last_15m"
		},
		"thresholds": {
			"critical": 0.9,
			"warning": 0.75,
			"critical_recovery": 0
		}
	}
}
```

# Monitoring Data
Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

* Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

Warning threshold of 500
Alerting threshold of 800
And also ensure that it will notify you if there is No Data for this query over the past 10m.
Please configure the monitor’s message so that it will:

Jefferson Haw: Please refer here https://github.com/hawjefferson/hiring-engineers/blob/master/AWS%20instance/Monitoring%20Data/customMetricMonitor.json

```JSON
{
	"name": "MyMetric threshhold reach",
	"type": "metric alert",
	"query": "avg(last_5m):avg:custom_myMetric{env_se_function:se_tech_challenge} > 800",
	"message": "{{#is_alert}} [ALERT]Alert Threshold reach. Metric value of: {{value}}  , Host from {{host.ip}} {{/is_alert}} \n\n{{#is_warning}} [WARNING]Warning Threshold reach.{{/is_warning}} \n\n{{#is_no_data}} [NO DATA] No data has been collected for more than last 10 minutes{{/is_no_data}}  @jeff.haw.23@gmail.com",
	"tags": [],
	"options": {
		"notify_audit": true,
		"locked": false,
		"timeout_h": 0,
		"new_host_delay": 300,
		"require_full_window": false,
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

* Send you an email whenever the monitor triggers.

Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
* ALERT:

    Given that the customMetric.py generated random numbers, it was hard to show the ALERT outcome hence I’ve lowered the threshold from 800 to 500 such that I can have Datadog issue an alert notification.

    ![Alert](AWS%20instance/Monitoring%20Data/Alert_Threshold_Email.png)
* WARNING:
    ![Warning](AWS%20instance/Monitoring%20Data/Warning_Threshold_Email.png)
When this monitor sends you an email notification, take a screenshot of the email that it sends you.

* Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
Jefferson Haw: Please see Downtime.png
![Downtime](AWS%20instance/Monitoring%20Data/Downtime.png)

One that silences it from 7pm to 9am daily on M-F,
Jefferson Haw: Please see WeekdayDowntimeConfig.png.png

        
![WeekendDowntime](AWS%20instance/Monitoring%20Data/WeekdayDowntimeConfig.png)

And one that silences it all day on Sat-Sun.
Jefferson Haw: Please see WeekendDowntimeConfig.png.png

![WeekendDowntime](AWS%20instance/Monitoring%20Data/WeekendDowntimeConfig.png)

Jefferson Haw: Please see SnoozeNotificationSample.png. Instead of waiting for the weekend/time for the weekday. I’ve just created a third one-time off downtime configuration to show how the notification should work.
![Snoozetime](AWS%20instance/Monitoring%20Data/SnoozeNotificationSample.png)


# Collecting APM Data:
Note: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

Note: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

* In order to enable APM, one would need to modify the Datadog.yaml file and set the following values:
```YAML

# Trace Agent Specific Settings
#
apm_config:
#   Whether or not the APM Agent should run
enabled: true
#   The environment tag that Traces should be tagged with
#   Will inherit from "env" tag if none is applied here
env: dev
#   The port that the Receiver should listen on
receiver_port: 8126
#   Whether the Trace Agent should listen for non local traffic
#   Only enable if Traces are being sent to this Agent from another host/container
#   apm_non_local_traffic: false
#   Extra global sample rate to apply on all the traces
#   This sample rate is combined to the sample rate from the sampler logic, still promoting interesting traces
#   From 1 (no extra rate) to 0 (don't sample at all)
extra_sample_rate: 1.0
```

Once done, please restart the Datadog agent using the command: __sudo service datadog-agent restart__ <br />

Datadog Host Infrastucture view should be updated with a new tag called trace

![APM](AWS%20instance/Collecting%20APM%20Data/HostInfrastructure.png)

This will also enable the APM module within Datadaog specific to the resource you are monitoring
![APM_View](AWS%20instance/Collecting%20APM%20Data/APM.png)

To create a holistic view, you can append the APM reports into your existing or new dashboard.
![APM_Dashboard](AWS%20instance/Collecting%20APM%20Data/Dashboard_APM_Infrastructure.png)

* Bonus Question: What is the difference between a Service and a Resource?
Jefferson Haw: Service is the application or component itself. e.g. Web App, SQL Database
Resource is the operations managed within the Service. e.g. GET/POST/Servlet method on the Web App Service. SELECT SQL or INSERT SQL on the Database service.

Here is an example of the service within my sample APM which is a web-app  called hello-sqlite

![APM_Application](AWS%20instance/Collecting%20APM%20Data/ServiceNodeJSApp.png?raw=true)

While here is an example of the Resource which is going to certain NodeJS express request route that is using a HTTP GET command

![APM_Resource](AWS%20instance/Collecting%20APM%20Data/Resource.png)
* Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.
Jefferson Haw: I've re-used a nodejs web application that allows you to submit information or data to the web application. By submitting the data/information you provided, the data gets stored on a SQLite backend.
You can access the web application via: http://18.221.245.80:34936/

You can also deploy the nodejs application locally by getting the source code here: https://github.com/hawjefferson/hiring-engineers/tree/master/AWS%20instance/Collecting%20APM%20Data/nodejs_datadog


# Final Question:
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?
* Jefferson Haw: Rather than answering this question in a traditional Monitoring way, I would attempt to use Datadog's engine to provide unique customer experience by allowing datadog to sift through http server, web appliation session logs that can monitor and analyze customer behavior or activity. Once a customer or end user fits on a certain metric or behavior defined within Datadog, Datadog can call or initiate webhooks that can provide a tailorized experience to the customer/end user. This could be as simple as sending a One Time offer in the form of SMS or email. This can also be triggering the current web/mobile application the customer is using for promotional offers or even as simple as providing relevant information base on what he/she has browse through during his activity period over time.

* Another additional idea would be allow Datadog to do SECOPS like capability wherein Datadog monitors infrastructure, applications. Base on certain events, Datadog can be configured to manage certain metrics which will eventually trigger security based APIs (e.g: Challenging MFA, killing sessions, suspending a compromised account,etc.) This is the trend for most APM based vendors wherein they would partner with Security based providers to create a secured and integrated eco-system.
