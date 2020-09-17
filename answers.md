# DataDog Solutions Engineer Assignment

Please find my assignment solution below

## Prerequisites - Setup the environment

I had an Ubuntu 16.04 linux machine installed on an [Intel NUC](https://www.intel.com/content/www/us/en/products/boards-kits/nuc.html) in my lab environemnt, and so I used that machine to host the datadog Agent. I installed the Agent using the easy one-step install instructions documented [here](https://app.datadoghq.com/account/settings#ubuntu). I validated the Agent installation using the following comamnd.

```
$ datadog-agent version
Agent 7.22.0 - Commit: 8db451d - Serialization version: v4.40.0 - Go version: go1.13.11
```
From the installation log `ddagent-install.log`
```
Your Agent is running and functioning properly. It will continue to run in the
background and submit metrics to Datadog.
```

## Collecting Metrics
Once the `datadog-agent` was installed on the linux server, it was time to start collecting metrics from the host

#### Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

The Agent config file `datadog.yaml` is located in the `/etc/datadog-agent` folder. To add tags, I needed to edit the **@param tags** section

```
## @param tags  - list of key:value elements - optional
## List of host tags. Attached in-app to every metric, event, log, trace, and service check emitted by this Agent.
```
Referencing the [Assigning Tags](https://docs.datadoghq.com/getting_started/tagging/assigning_tags/?tab=noncontainerizedenvironments#configuration-files) user guide, I added the following tags.

`tags: ["environment:dev", "env:prod", "service: flask_app", "os:ubuntu", "application:datadog", "location:sanfrancisco"]`. 

I saved the file and restarted the agent `sudo service datadog-agent restart`

The tags should show up under Infrastructure > Host Map

![Agent Host Map](https://github.com/agentAWP/hiring-engineers/blob/master/AgentHostMap.png)

#### Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I installed a MySQL Server on my linux machine. Then, I followed instructions from the [Integrations](https://docs.datadoghq.com/integrations/mysql/?tab=host) document to install the MySQL integration on my host. I prepared MySQL as instructed.
```
$ mysql -u datadog --password=boulder -e "show status" | \
> grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || \
> echo -e "\033[0;31mCannot connect to MySQL\033[0m"
mysql: [Warning] Using a password on the command line interface can be insecure.
Uptime	169459
Uptime_since_flush_status	169459
MySQL user - OK
```

```
$ mysql -u datadog --password=boulder -e "show slave status" && \
> echo -e "\033[0;32mMySQL grant - OK\033[0m" || \
> echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"
mysql: [Warning] Using a password on the command line interface can be insecure.
MySQL grant - OK
```

I also edited the MySQL `conf.yaml` file within `/etc/datadog-agent/conf.d/mysql.d/` folder
```
$ cat /etc/datadog-agent/conf.d/mysql.d/conf.yaml
init_config:

instances:
  - server: 127.0.0.1
    user: datadog
    pass: <PASSWORD>
    port: 3306
    options:
      replication: false
      galera_cluster: true
      extra_status_metrics: true
      extra_innodb_metrics: true
      extra_performance_metrics: true
      schema_size_metrics: false
      disable_innodb_metrics: false
```
I restarted the Agent to apply the changes. MySQL metrics are now available to monitor under the Metrics > Explorer section.
![MySQL metrics](https://github.com/agentAWP/hiring-engineers/blob/master/MySQLMetrics.png)

#### Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

To write my first custom check, I read through the examples in the [Writing a Custom Agent Check](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7) and [Metric Submission](https://docs.datadoghq.com/developers/metrics/agent_metrics_submission/?tab=count) articles

I created a `checks.d` folder under `/etc/datadod-agent` and created `my_metric.py` file.

```
$ cat my_metric.py
#!/usr/bin/python3
import random
from datadog_checks.base import AgentCheck

__version__ = "1.0.0"

class MyMetric(AgentCheck):
	def check(self, instance):
	# Defining the 'gauge' function as we want a random value
	# Adding tag `metric_submission_type:gauge` for future reference
		self.gauge("my_metric.gauge",random.randint(0, 1000),tags=["metric_submission_type:gauge"],)
```
Next, I created a folder `my_metric.d/` within the `/etc/datadog/conf.d/` folder and created the configuration file `my_metric.yaml` for my check. Its important to name the *check* and the *configuration* file same.

```
$ cat my_metric.yaml
init_config:

instances:
  - min_collection_interval: 45
```

#### Change your check's collection interval so that it only submits the metric once every 45 seconds.

The default value for the `min_collection_interval` parameter is 15. Since we had to change the field to 45 seconds, the file shows that updated value. 
I restarted the Agent and validated the check is running properly.

```
$ sudo -u dd-agent -- datadog-agent check my_metric
=== Series ===
{
  "series": [
    {
      "metric": "my_metric.gauge",
      "points": [
        [
          1600232559,
          612
        ]
      ],
      "tags": [
        "metric_submission_type:gauge"
      ],
      "host": "colorado",
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

    my_metric (1.0.0)
    -----------------
      Instance ID: my_metric:5ba864f3937b5bad [OK]
      Configuration Source: file:/etc/datadog-agent/conf.d/my_metric.d/my_metric.yaml
      Total Runs: 1
      Metric Samples: Last Run: 1, Total: 1
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 0, Total: 0
      Average Execution Time : 0s
      Last Execution Date : 2020-09-15 22:02:39.000000 PDT
      Last Successful Execution Date : 2020-09-15 22:02:39.000000 PDT
```
Under the Metrics > Explorer page, I can now plot my custom `my_metric` under Metrics > Explorer.
![My_Metric_Explorer](https://github.com/agentAWP/hiring-engineers/blob/master/My_Metric_Explorer.png)

#### **Bonus Question** Can you change the collection interval without modifying the Python check file you created?
Yes, by editing the *yaml config* file for your check.


#### Visualizing Data

The next task is to create a Dashboard using DataDog API

> Utilize the Datadog API to create a Timeboard that contains:
> * Your custom metric scoped over your host.
> * Any metric from the Integration on your Database with the anomaly function applied.
> * Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

First, I retrieved my [API Key and APPLICATION KEY](https://docs.datadoghq.com/account_management/api-app-keys/#application-keys) available under Integrations > API from within the Datadog portal.

Referencing the [Dashboard API](https://docs.datadoghq.com/api/v1/dashboards/) documentation, I created my [DataDogDashboard.py](https://github.com/agentAWP/hiring-engineers/blob/master/DataDogDashboard.py) file.

> Your custom metric scoped over your host

A dashboard contains widgets, and there are multiple types of [widgets](https://docs.datadoghq.com/dashboards/widgets/). I am working with the [TimeSeries Widget](https://docs.datadoghq.com/dashboards/widgets/timeseries/). As per the requirment, and using the [Requests JSON Schema](https://docs.datadoghq.com/dashboards/graphing_json/request_json/), the relevant snippet of the code is pasted below.

```
{
  "definition":{
      "type":"timeseries",
      "requests": [
          {
	  # 'q' represents query
              "q":"avg:my_metric.gauge{*}"
          }
      ],
      "title":"Average of my_metric"
  }
}
```

> Any metric from the Integration on your Database with the anomaly function applied.

I am now tasked to use the [anomalies](https://docs.datadoghq.com/dashboards/functions/algorithms/) fucnction specifically. In this case, I am choosing a random metric, my `mysql.performance.kernel_time` but plotting it using the *basic* algorithm and *standard deviation of 2*

```
{
    "definition":{
        "type":"timeseries",
        # Using the anomalies function of "my_metric" check using  
        # and "basic" algorithm and standard deviation of 2
        "requests":[
            {
                "q":"anomalies(avg:mysql.performance.kernel_time{*},'basic',2)"
            }
        ],
        "title":"Anomalies function graph"
    }
}
```

> Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Next is the [rollup](https://docs.datadoghq.com/dashboards/functions/rollup/) function for custom `my_metric`. I am aggregating the `sum` over a period of `3600 seconds (1 hour)`

```
{
    "definition":{
        "type":"timeseries",
        # Using the rollup function to sum all values 
        # in the last 1 hour
        "requests":[
            {
                "q":"avg:my_metric.gauge{*}.rollup(sum,3600)"
            }
        ],
        "title":"Rollup function graph"
    }
}
```
The final code is linked [here](https://github.com/agentAWP/hiring-engineers/blob/master/DataDogDashboard.py) 

#### Once this is created, access the Dashboard from your Dashboard List in the UI:
Upon executing my [DataDogDashboard.py](https://github.com/agentAWP/hiring-engineers/blob/master/DataDogDashboard.py) file, I was able to create the "*API Dashboard for Data Visualization*" dashboard ![API Dashboard for Data Visualization](https://github.com/agentAWP/hiring-engineers/blob/master/DataDogDashboard.png)

Here is my [API Dashboard for Data Visualization Snapshot](https://p.datadoghq.com/sb/frevxrj12y7as0m5-9b70b4bdc31e0f0189105ae1de430e34?from_ts=1600221199321&live=true&to_ts=1600235599321&theme=dark)

#### Set the Timeboard's timeframe to the past 5 minutes
I changed the interval to "Past 5 minutes"

#### Take a snapshot of this graph and use the @ notation to send it to yourself.

Snapshot of Anomaly graph.

![Anomaly](https://github.com/agentAWP/hiring-engineers/blob/master/Anomaly_email.png)

#### Bonus Question: What is the Anomaly graph displaying?
The anomaly graph displays the expected behavior of the plotted metric based on past values. The `basic` algorithm uses previous points at regular intervals to determine the range of expected values. The width of the displayed gray band is dicated by the `standard deviation of 2` which means about 95% of values will be within 2 standard deviations of the mean value. Any "unexpected" or "anomaly" in the values will be marked in red.

## Monitoring Data

#### Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

Next task is to setup [Metric Monitors](https://docs.datadoghq.com/monitors/monitor_types/metric/?tab=threshold) that trigger when custom `my_metric` goes above unexpected values. My *Metric Monitor* should consider the followint alerting conditions:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

Here is my configuration for a monitor that respects the above threshold criteria

![Metric_Monitor](https://github.com/agentAWP/hiring-engineers/blob/master/Metric_Monitor_Config.png)

#### Create different messages based on whether the monitor is in an Alert, Warning, or No Data state. Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

Based upon the above requirement, I configured the monitor message to include specific details based upon the monitor state.

```
{{#is_alert}}

MyMetric (my_metric) value is too high! Host {{host.name}} with IP {{host.ip}} recorded {{threshold}} value. 

{{/is_alert}}

{{#is_warning}} 

MyMetric (my_metric) value is OK - but check "API Dashboard for Data Visualization" just in case.

{{/is_warning}}  

{{#is_no_data}}

Looks like {{host.name}} is down. No data was reported since last 10 minutes. Can you check at {{host.ip}}

{{/is_no_data}}  @tmullercity+datadog@gmail.com
```
#### When this monitor sends you an email notification, take a screenshot of the email that it sends you.

***ALERT State***

![AlertNotification](https://github.com/agentAWP/hiring-engineers/blob/master/Alert.png)

***WARNING State***

![WarningNotification](https://github.com/agentAWP/hiring-engineers/blob/master/WARN.png)

***NO Data in last 10 minutes***

![NoDataNotification](https://github.com/agentAWP/hiring-engineers/blob/master/NoData.png)

#### Bonus Question

> Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

I can schedule downtime for my Alerts from the Manage Downtime tab under Monitors > Manage Monitors. Scheduling downtime during a maintentance window is a common use case of this feature.

> * One that silences it from 7pm to 9am daily on M-F. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

I configured "Schedule Downtime" to meet the above criteria as shown below

![WeeklyDowntimeConfiguration](https://github.com/agentAWP/hiring-engineers/blob/master/WeeklyDowntime1.png)

The downtime in an active state is shown below

![WeeklyDowntimeActive](https://github.com/agentAWP/hiring-engineers/blob/master/WeeklyDowntime2.png)

Email notification for scheduled Weekly Downtime

![WeeklyDowntimeEmail](https://github.com/agentAWP/hiring-engineers/blob/master/WeeklyDowntimeEmail.png)

> * And one that silences it all day on Sat-Sun. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

I configured another "Scheduled Downtime" specifically for weekends.
![WeekendDowntimeConfiguration](https://github.com/agentAWP/hiring-engineers/blob/master/WeekendDowntime1.png)

The downtime in a scheduled state.
![WeekendDowntimeScheduled](https://github.com/agentAWP/hiring-engineers/blob/master/WeekendDowntime2.png)

Email notification for Weekend Downtime
![WeekendDowntimeEmail](https://github.com/agentAWP/hiring-engineers/blob/master/WeekendDowntimeEmail.png)

## Collecting APM Data

The final task is to insturment an application using [Datadog APM Solution](https://docs.datadoghq.com/tracing/)

Since the application is written in Python, I referenced the [Tracing Python Applications](https://docs.datadoghq.com/tracing/setup/python/) and installed `dd-trace` librabry on my machine

```
pip install ddtrace
```

I read through the different [Evironment Variable](https://docs.datadoghq.com/tracing/setup/python/) for efficient tracing using `datadog-agent`. I also wanted to implement my application with custom spans, as documented [here](https://docs.datadoghq.com/tracing/guide/add_span_md_and_graph_it/?tab=java#pagetitle). 

```@app.route('/api/apm')
#Service and resource parameters added
@tracer.wrap("flask.request", service='flask_app', resource='APM', span_type="web")
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
#Service and resource parameters added
@tracer.wrap("flask.request", service='flask_app', resource='TRACE', span_type="web")
def trace_endpoint():
	return 'Posting Traces'
```

My fully instrucmented app code is available here -- [Python Flask App](https://github.com/agentAWP/hiring-engineers/blob/master/flask_app.py)

I enabled instrumentation by executing the following code

```
sudo DD_VERSION=1.1 DD_SERVICE="flask_app" DD_ENV="prod" DD_LOGS_INJECTION=true DD_PROFILING_ENABLED=true ddtrace-run python3.8 flask_app.py
```

I executed a sample Python script that issues HTTP GET requests to the different Flask App endpoints (/, /api/apm/,/api/trace). Upon navigating to the APM > Services tab in the Admin portal, I am able to monitor these GET requests under my `flask_app` service.

Screenshots of APM Dashboard available under APM > Services

Screenshot of the **Services** tab
![Services](https://github.com/agentAWP/hiring-engineers/blob/master/flask_app_Services.png)
Screenshot of the **Traces** tab

![Traces](https://github.com/agentAWP/hiring-engineers/blob/master/flask_app_Traces.png)

Screenshot of the **Infrastructure** tab

![Infrastructure](https://github.com/agentAWP/hiring-engineers/blob/master/flask_app_Infrastructure.png)

Screenshot of the **Metrics** tab

![Metrics](https://github.com/agentAWP/hiring-engineers/blob/master/flask_app_Metrics.png)

Screenshot of the **AppAnalytics** tab

![AppAnalytics](https://github.com/agentAWP/hiring-engineers/blob/master/flask_app_AppAnalytics.png)

Screenshot of the **Profiles** tab

![Profiles](https://github.com/agentAWP/hiring-engineers/blob/master/flask_app_Profiles.png)

Screenshot of the **Profiles_Metrics** tab

![ProfileMetrics](https://github.com/agentAWP/hiring-engineers/blob/master/flask_app_ProfilesMetrics.png)

Link to [APM Dashboard](https://p.datadoghq.com/sb/frevxrj12y7as0m5-669c552580a9ec7dc0c70f9c4480daa7?from_ts=1600289802467&live=true&to_ts=1600293402467&theme=dark)

#### Bonus Question: What is the difference between a Service and a Resource?

A Service is a collection of functional resources that combine together to serve a specific purpose. Resources are elements of a service that represent a particular action. In our example, the service flask_app.py contained 3 web endpoints. Individually, each endpoint is considered a resource


## Final Question

> Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!
> Is there anything creative you would use Datadog for?

The start of the **SPORT SEASON**, especially the NFL, [Indian Premier League](https://www.iplt20.com/matches/schedule/men) and English Premier League has got me super excited. There are 14 NFL games being played on Sunday 9/20, along with IPL cricket matches and English Premier League and keeping track on each one of them is impossible. I would like to create a "SPORTS" dashboard that tracks the game scores throught online APIs or web scraping, and sends an alert when there is a touchdown (or a goal is scored). I can integrate the alert to an a lambda function in Alexa that plays the last score loudly. I can also trigger a WARNING alert if the score reads 1st & GOAL, then quickly change to the right channel, and enjoy football. Since all the metrics are now available to me, I can run my own analysis on the game. Every sport update in one single dashboard. **ESPN powered by Datadog!**
