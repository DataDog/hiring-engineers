Your answers to the questions go here.

# Datadog Overview
Datadog is a monitoring service for cloud-scale applications, providing monitoring of servers, databases, tools, and services, through a SaaS-based data analytics platform. [Wiki](https://en.wikipedia.org/wiki/Datadog)

### Features
* Observability - From infrastructure to apps, in any environment
* Dashboards - Use instant, real-time boards or build your own
* Infrastructure - From overview to deep details, fast
* Analytics - Custom app metrics or business KPIs
* Collaboration - Share data, discuss in context, solve issues quickly
* Alerts - Avoid alert fatigue with smart, actionable alerts
* API - Love infrastructure as code? You'll love Datadog's API
* Machine Learning - Automatically detect outliers and temporal anomalies
* APM - Monitor, optimize, and troubleshoot app performance

I am here to apply for the support engineer at [Datadog](https://www.datadoghq.com/careers/detail/?gh_jid=1160573) Sydney.

# The Challenge

## 1. Prerequisites - Setup the environment
* What is my environment setting?

>Answer: I am using macOS Sierra Version 10.12.6, data dog agent version 6.2.0 for this challenge.

* Sign up for Datadog, get the Agent reporting metrics from your local machine.

>Answer: [Sign up here](https://www.datadoghq.com/#), get a datadog account for free for 14 days.

>login, click on [_integration-Agent_](https://app.datadoghq.com/account/settings#agent/mac) in DataDog on the left column and follow the installation instructions for Mac OS X to install the Agent.

> The datadog can be installed on OS X as easily as:
```
DD_API_KEY=<you_api_key> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/osx/install.sh)"
```

![Datadog agent on my macOS](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/1_host_agent.png)

## 2. Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

> Open ~/.datadog-agent/datadog.yaml, uncomment tag block and add your own tags to the host.  
[Reference: Applying Tags](https://docs.datadoghq.com/tagging/#applying-tags)

![config_tags](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/2_host_tags_config_file.png)

![Apply tags on infrastructure](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/2_host_tags.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

> I used PostgreSQL to complete this section, for how to install Postgresql on your host, you can check its official docs.
> [Reference: Postgre integrations](https://docs.datadoghq.com/integrations/postgres/)

![psql intergration instrcution](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/2_postgresql_integration_instruction.png)

```sql
-- Step1
-- Create a read-only datadog user with proper access to your PostgreSQL Server. Start psql on your PostgreSQL database and run
create user datadog with password 'password_for_datadog';
grant SELECT ON pg_stat_database to datadog;

-- Step 2
-- Configure the Agent to connect to the PostgreSQL server
-- Edit conf.d/postgres.yaml
init_config:

instances:
   -   host: localhost
       port: 5432
       username: datadog
       password: z3aBCOlb0pSmLKErITgCxfQj
       tags:
            - optional_tag1
            - optional_tag2

-- Step 3
-- Restart Agent

-- Step 4
-- check the integration
$ datadog-agent status
$ ...
  postgres
  --------
    Total Runs: 1
    Metrics: 142, Total Metrics: 142
    Events: 0, Total Events: 0
    Service Checks: 1, Total Service Checks: 1
    Average Execution Time : 800ms
 ...
```

![psql metrics](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/2_postgresql_integration_metrics.png)


* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
> Each check has a YAML configuration file that is placed in the conf.d directory. The file name should match the name of the check module (e.g.: haproxy.py and haproxy.yaml).
> [Reference - Sending metrics](https://docs.datadoghq.com/developers/agent_checks/#sending-metrics)

```python
# python script goes into ~/.datadog-agent/checks.d/my_metric.py
from random import randrange
from checks import AgentCheck

class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randrange(0, 1001))
```
```yaml
# configuration file goes into ~/.datadog-agent/conf.d/my_metric.yaml
init_config:

instances:
    [{}]
```

![cli-check](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/3_my_metric_check.png)

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

```yaml
# we modify config file to set up collection interval
init_config:

instances:
    - min_collection_interval: 45
```


* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

```yaml
# we can use the same approach shown in the last question
init_config:

instances:
     - min_collection_interval: INTERVAL_VALUE
```

## 3. Visualizing Data:
### 3.1 Using API to create timeboard
Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
> By referring to API doc: Timeboards - [Create a Timeboard](https://docs.datadoghq.com/api/?lang=python#create-a-timeboard), the code is shown in `create_dashboard.py`([link](https://github.com/southpolemonkey/hiring-engineers/blob/AlexRong-solution-engineer/code_snippet/create_timeboard.py)). In addition, `api_key` and `app_key` can be created in [APIs management sector](https://app.datadoghq.com/account/settings#api) in the web portal.

![api_key](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/3_api_key.png)

After successfully put the code at the right place, you should be able to find 'my_metric' appearing in metrics summary.

![my_metrics](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/3_my_metric.png)

* Any metric from the Integration on your Database with the anomaly function applied.

```python
    # graph2: database with anomaly function
    {"definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:postgresql.buffer_hit{*}, 'basic', 3)"}
        ],
        "viz": "timeseries"
    },
    "title": "PostgreSQL buffer hit"}
    ]
```
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
```python
    # graph1: my_metric
    {"definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{*}"}, # my custom metric
            {"q": "my_metric{*}.rollup(sum, 3600)"} # rollup sum
           ],
        "viz": "timeseries"
    },
    "title": "Average Memory Free"
    },
```

### 3.2 Change timeframe
Once this is created, access the Dashboard from your Dashboard List in the UI:
The red line in the first graph is my_metric rollup sum while the line in blue shows the trend of my\_metric.
![enter image description here](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/3_dashboard.png)

* Set the Timeboard's timeframe to the past 5 minutes
> Let mouse hover over your graph, click and drag crusor to the desired time duration.

![5_min_timeframe](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/3_dashboard_5mins_update.png)

* Take a snapshot of this graph and use the @ notation to send it to yourself.

![snapshot_send_notification](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/3_snapshot_notification_update.png)

![snapshot_received](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/3_snapshot_notification_email_update.png)

* **Bonus Question**: What is the Anomaly graph displaying?
> The grey area in the graph shows the normal area predicted by the anomaly algorithm based on historical data. The data stay within the grey area is in blue while the anomaly data is in red.

![anomaly_graph](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/3_anomaly_graph_3.png)

## 4. Monitoring Data
### 4.1 Create monitor for my_metric
Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

![create_new_monitor](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/4_create_monitor.png)

![enter image description here](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/4_monitor_set_threshold_value.png)

### 4.2 Create Notification message
* Send you an email whenever the monitor triggers.

* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

![enter image description here](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/4_monitor_message.png)

> During the test, I found it a bit tricky to trigger ALERT condition, so I add host.ip and triggered_value in WARNING notification message, the details can be found in the screenshot below.

![warning_trigger](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/4_monitor_warning_email.png)

![no_data](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/4_monitor_no_data.png)


### 4.3 Set up downtime
- **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
	- One that silences it from 7pm to 9am daily on M-F,
	- And one that silences it all day on Sat-Sun.
	- Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

#### 4.3.1 Weekday Schedule
![new_downtime_schedule](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/4_create_downtime_schedule.png)

![weekday_schedule](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/4_downtime_weekday_schedule.png)

![weekday_schedule_email](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/4_downtime_weekday_email.png)


#### 4.3.2 Weekend schedule
![enter image description here](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/4_downtime_weekend_schedule.png)

![enter image description here](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/4_downtime_weekend_email.png)


## 5. Collecting APM Data
### 5.1 APM setup
> [Setup process](https://docs.datadoghq.com/tracing/setup/)
#### 5.1.1 Install the Datadog Agent
> "The APM agent (aka Trace Agent) isn't part of the OSX Datadog Agent yet, it needs to be run manually on the side."

I need to manually install trace-agent according to the instruction [here](https://github.com/DataDog/datadog-trace-agent). Otherwise, you might see ERROR information like `ddtrace.writer - ERROR - cannot send services to localhost:8126: [Errno 61] Connection refused` when you run the flask application.

#### 5.1.2 Enable trace collection for the Datadog Agent
> To enable trace collection for your Agent, update the apm_config key in your Agent datadog.yaml main configuration file

```yaml
# modify configuration file: ~/.datadog-agent/datadog.yaml

# Trace Agent Specific Settings
apm_config:
  enabled: true
```

#### 5.1.3 Configure your environment
> **Note**: if you do not configure your own environments, all data will default to env:none

#### 5.1.4 Instrument your application
> For python applications, the installation instruction can be found [here.](https://docs.datadoghq.com/tracing/setup/python/)

```python
# install the Datadog Tracing library using pip
$ pip install ddtrace

# instrument Python application
$ ddtrace-run python flask_app.py
```



After implementing the above procedures successfully, you should be able the web app running without showing ERROR info.

![trace_agent_installation](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/5_install_trace_agent.png)






### 5.2 Trace on flask application
- Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
> You should be able to view my dashboard [here](https://app.datadoghq.com/dash/907821/alexs-apm-dashboard?live=true&page=0&is_auto=false&from_ts=1536242499935&to_ts=1536246099935&tile_size=m&tpl_var_var=*).
> The instrumented app code can be found [here](https://github.com/southpolemonkey/hiring-engineers/blob/AlexRong-solution-engineer/code_snippet/flask_app.py)

![enter image description here](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/5_apm_service_3.png)

![apm_dashboard](https://raw.githubusercontent.com/southpolemonkey/hiring-engineers/AlexRong-solution-engineer/datadog_screenshot/5_apm_timeboard_1.png)

- **Bonus Question**: What is the difference between a Service and a Resource?
> A service is a set of processes that do the same job  while a resource is a particular action for a service.
> **Reference**: [Getting started with APM](https://docs.datadoghq.com/tracing/visualization/)

## 6. Final Question
hmm...after going through the backbone of datadog, it now turns out to be more like a data-driven initiative tool for my life. Well, I'm a food and beer lover, can't even bear a warm beer (taste so weird). So what I'm thinking is a tool which can help me to monitor my beer quantity and temperature. For the beer quantity, a digitial weight scale connected with Raspberry Pi which sends data to datadog should do the job. For the temperature, I would use a thermometer to ensure the beer stays at an optimal temperature.  Once the weight goes below 2 bottles' weight, or the temperature gets too warm, the monitor triggers the alert and send me the notification. Ha, sounds like a solid system, I can even monitor my icecream, chocolate and all the tasty stuff! Happy monitoring!!
