## Solution Engineering Exercise - Ed Lee

With the speed of digital offerings, modern application development paradigms, multiple languages / technologies, “dev” and “ops”, dynamic infrastructures (VMs and containers), a cloud scale monitoring tool is needed to keep up and close the gaps in applications and infrastructure monitoring.  Datadog is a cloud monitoring solution that is built to support these trends as it monitors dynamic applications and infrastructures in the cloud and many on-premise platforms.  It helps companies gain visibility into the performance of their applications, code and infrastructure; aggregates metrics and events across systems, apps and serves; provides real-time dashboards, analytics and insights that can help businesses improve agility and to help find issues and deal with them before they become bigger problems.

Datadog offers an intuitive, easy to use and reponsive UI to configure, manage and display application and infrastruture monitoring in your enterprise.  In addition, for the programmatic option, Datadog API provides a comprehensive set of capabilities to get data in and out of Datadog and includes the capabilities in the UI.  API Reference:  https://docs.datadoghq.com/api/

The activities and tasks related to the exercise will help illustrate some of the features and capabilities of Datadog.

*Exercise - Environment*

- Vagrant Ubuntu 12.04 VM set up on an Ubuntu 16.04 host

### *Collecting Metrics*

The first step for leveraging the power of Datadog is to collect metrics and events.  Datadog provides agents for numerous platforms to collect events and systems metrics.  The collection of metrics is configurable to a very granular (and frequent) level.

![Agents](/eplee123/agents.png)

The python-based agent is open source (https://github.com/DataDog/dd-agent/) and is the foundation software for collecting metrics.  The agent is lightweight and made up of 4 components:
-	Collector:  collects systems metrics such as memory and CPU usage, network traffic, etc
-	Dogstatsd:  extension of statsd daemon to aggregate and summarize metrics instrumented in code.  Dogstatsd also accepts all three major data types: metrics, events and service checks.
-	Forwarder:  sends data from the collector and dogstatsd to Datadog
-	Supervisord:  responsible for keeping the subprocesses running

The metrics collected from the agent helps provide a full picture of what is happening by correlating the metrics of the applications and systems.  More information about Agents in this guide:  https://docs.datadoghq.com/guides/basic_agent_usage/.

*Exercise: Agent installation*

- Ubuntu agent installed on Vagrant Ubuntu 12.04 VM guest host

![Agent Installed](/eplee123/agent-installed.png "Datadog Agents")

Tagging metrics makes it easier to subset and query in the dashboards and graphs.  Tags add dimensions to the metrics or, in other words, help categorize to slice the data, such that filters can be applied across a collection.  This helps in providing relevant views or provide the right visualization into the applications and infrastructure within your enterprise.  Tags can be added in the agent configuration file and would be reflected in the Datadog UI.  More information about Tags in this guide:  https://docs.datadoghq.com/guides/tagging/.

*Exercise: Add Tags*

- Tags are added to the agent configuration file, by editing the datadog.conf file

![Configuring Tags](/eplee123/tags-conf.png)

- Host map view shows the tags

![Hostmap with Tags](/eplee123/hostmap-tags.png)

Integrations allow for extension beyond the native metrics from the agent to more easily monitor application health, process utilization and more.  Datadog has over 200 built-in integrations across many systems, applications and services.

![Integrations](/eplee123/integrations.png)

*Exercise: Install database and install respective Datadog integration for that database*

- Installed MySQL on the Vagrant Ubuntu 12.04 VM.

![MySQL Installation](/eplee123/mysql-install.png)

- The MySQL integration for Datadog was installed / configured

![MySQL Integration](/eplee123/mysql-integration1.png)

 

![MySQL Integration](/eplee123/mysql-integration2.png)

- The Datadog dashboard for MySQL shows the metrics collected from the MySQL database

![MySQL Metrics](/eplee123/mysql-metrics-dash.png)

Custom agent checks are a great way to collect metrics from custom applications or unique systems.  This concept is very similar to integrations.  The general guideline is that if metrics are to be collected from a generally available application, public service or open source project, an integration would be recommended.
Writing a custom agent check involves:
-	Check module (python) in the agent’s check.d directory.  The custom check inherits from the AgentCheck class with a check method that defines the metrics collected, events or status checks to be sent
-	Corresponding check configuration file (yaml) in the agent’s conf.d directory

https://docs.datadoghq.com/guides/agent_checks/

*Exercise: Custom Agent Check*

- This custom metric generates a random integer value between 0 and 1000.  Sample a gauge metric with the metric name (my_metric) as first argument and value (randInt function) for the second argument.

- /etc/dd-agent/checks.d/checkrandom.py:

```
import random
from checks import AgentCheck

class my_metric(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(1,999))
```

- /etc/dd-agent/conf.d/checkrandom.yaml:

```
init_config:

instances:
[{}]
```

![my_metrics dashboard](/eplee123/my_metric-dash.png)

- A check’s collection interval specifies the frequency that the agent’s check is run.  The default is 15 seconds.  The frequency can be adjusted by adding the min_collection_interval parameter at the init_config level or at the instance level of the configuration yaml file.

- /etc/dd-agent/conf.d/checkrandom.yaml:

```
init_config:
  min_collection_interval: 45

instances:
[{}]
```
        
- Bonus question:  The collection interval can be applied in the check configuration yaml file.  Therefore the Python check file that was created remains untouched.

### *Visualizing Data*

Datadog offers real-time interactive dashboards of high-resolution metrics and events that had been collected for manipulation and graphing.
-	See graphs across sources in real-time
-	Slice data by host, device or any other tag
-	Apply arithmetic and  calculations functions (rates, ratios, averages, integrals, etc)
-	Easily customize views, interactively or in code

There are two types of dashboards:
-	Timeboard: Time-synchronized metrics and event graphs.  Usage is more for troubleshotting and correlation
-	Screenboard: Mixing widgets and timeframes for status boards and sharing data
The dashboards can be created using the Datadog UI.

![Create Dashboard UI](/eplee123/dashboard-create.png)

In addition, for those who prefer to script or code the creation and management of Timeboards and Screenboards can use the Datadog API.  This allows for the ability to automate through scripts.  As a note, there are features from the API that are not yet available in the UI.  So there are instances that use of API would be needed over UI.

*Exercise: Create Timeboard using Datadog API*

- Coded python request in JSON format according to Datadog’s HTTP API.  All requests to Datadog’s API must be authenticated through the API and application keys.  These keys were generated based on my Datadog account.

-	Your custom metric scoped over your host; Average of custom metric scoped to the host with line type

```
{“q”: “avg:my_metric{host:precise64}”,”type”: “line”}
```

- Any metric from the Integration on your Database with the anomaly function applied; Average of a MySQL performance metric with anomaly function applied, using basic algorithm and a bounds (standard deviation) of 2; with line type.  Note:  There are four different anomaly detection algorithms.  For more information, see the guide for anomoly detection:  https://docs.datadoghq.com/guides/anomalies/
  - Basic: Used when there is no repeating pattern; uses a lagging rolling computation to determine the range of expected values
  - Agile: Used for seasonal metrics patterns and need to adjust to level shifts in the metric
  - Robust: Used for seasonal metrics patterns and when the metric is fairly stable; catch the slow level shifts
  - Adaptive: Used for seasonal metrics patterns and can adjust more readily than agile or robust algorithms

```
{“q”: “anomalies(avg:mysql.performance.bytes_sent{host:precise64},’basic’,2)”,”type”:”line”}
```

- Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

```
{“q”: “avg:my_metric{host:precise64}.rollup(sum, 3600)”,”type”: “line”}
```

- Edlee_Timeboard.py

```

from datadog import initialize, api

# All requests to Datadog's API must be authenticated
options = {
    'api_key': '2b7508d.......031428ae62095',
    'app_key': '0c8c11e.......af00fff23a2d6b19f281d07f9d'
}

initialize(**options)

# Title and description of the custom dashboard
title = "Ed Lee - Timeboard: Datadog API1"
description = "Timeboard Utilizing Datadog API"
# Define Timeboard with custom metric (my_metric), metric from database integration (bytes sent) with anomaly function, my_metric rollup 
graphs = [{
    "definition": {
        "requests": [
            {"q": "avg:my_metric{host:precise64}","type": "line"},
            {"q": "anomalies(avg:mysql.performance.bytes_sent{host:precise64},'basic', 2)","type": "line"},
            {"q": "avg:my_metric{host:precise64}.rollup(sum, 3600)","type": "line"}
         ],
    "viz": "timeseries"
    },
    "title": "my_metric, mysql.performance.bytes_sent,my_metric_rollup"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = False

api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)

```

![Timeboard](/eplee123/edlee-timeboard.png)

Within the dashboard, there are some additional formatting that can be done to highlight and show the right visualization of data.  Within the Keyboard and Mouse Shortcuts, there are options to change the graph sizes, zoom in/out, adding graphs to Timeboards, etc.

- Used the keyboard shortcut to change the size / timeframe to be for the past 5 minutes

![Timeboard with 5 minute timeframe](/eplee123/edlee-timeboard-5min.png)

Datadog’s collaboration features allow the sharing of dashboards and graphs by annotating specific points on a graph to alert others.

- Clicked on snapshot icon to add message and use @notation.  Sent to Events

![Snapshot of Timeboard](/eplee123/edlee-timeboard-snapshot.png)

- Bonus Question: What is the Anomoly graph displaying

- The anomaly graph shows the MySQL performance metric for bytes sent; with a gray band that represents the region where the metric is expected to be based on past behavior.  The blue line and red lines are the actual values.  The blue line is within the expected range while the red line showing a dip is outside of the expected range.  Anomaly detection is useful for identifying potential problems or issues.

![Anomaly Graph](/eplee123/anomaly.png)

### *Monitoring Data*

Monitors are automated notifications that can alert when a metric or check reach a specified level.  There are different types of monitors, such as host (if host is sending data to Datadog), metric (watching the metric), integration (status of integration or watch some metrics that are available from integration),  custom check, event monitor (watch event stream), among others.  To set up monitors, four basic steps are needed to get started:
-	Pick the metric
-	Set the conditions
-	Enter the message
-	Define the recipients

Monitors can be managed either from the UI or programatically throught the Datadog API.  More information about Monitors can be found in the guide:  https://docs.datadoghq.com/guides/monitors and the Monitoring Reference page:  https://docs.datadoghq.com/monitoring/

Within Monitor type of Metric

Metric Monitor Type

Detection Method
-	Threshold Alert: triggers alert whenever a metric crosses a threshold
-	Change Alert: triggers alert when the change in values is higher than the threshold
-	Anomaly Detection: triggers alert whenever a metric deviates from an expected pattern
-	Outlier Detection: triggers alert whenever one member in a group behaves differently from its peers

Alert Conditions: set the thresholds for alert, warning, alert recovery, warning recovery and conditions

Define the message body; specify the problem.  Within message template variables can be entered to define some conditional statements for the different messages

*Exercise: Create Metric Monitor*

![Monitor Created](/eplee123/my_monitor.png)

- Note: Changed the random number generation to be in range of 500-1000 to increase the likelihood of triggering the monitor

- Alert Triggered:

![Alert Triggered](/eplee123/monitor-alert.png)

- Warning Triggered:

![Warning Triggered](/eplee123/monitor-warn.png)

- No Data Triggered

![No Data Triggered](/eplee123/monitor-nodata.png)

- Bonus Question:  Managed downtime: schedule downtime to silence alerts according to a schedule

![Downtime - Weekday](/eplee123/monitor-downtime-weekday.png)



![Downtime - Weekend](/eplee123/monitor-downtime-weekend.png)



![Downtime Triggered](/eplee123/monitor-downtime-triggered.png)

When monitors are triggered and notification are issued, then some action can be taken to resolve the triggered monitors.

### *Collecting APM Data*

The Datadog APM tool collects performance metrics by tracing code to troubleshoot parts of the application that may be running slow or running inefficiently.  The performance metrics are sent to the Datadog agent and can help in understanding the components and the execution within the context of the underlying infrastructure.  APM helps bridge the gap between the infrastructure and application performance monitoring, by providing full stack observability.

Datadog APM includes:
-	Distributed tracing of requests from end to end, across every service and host involved
-	Detailed performance overviews for each monitored service
-	Latency distributions and percentiles, plus full decompositions of how much each service contributes to aggregate latency

*Exercise: Collecting APM Data*

- Used dd-trace-run

![Flask Trace](/eplee123/APM1.png)



![Flask Trace](/eplee123/APM2.png)



![Flask Trace Metrics](/eplee123/APM3.png)

- Bonus Question: A service in Datadog APM is a set of processes that work together that provide some functionality.  An application can be looked at as comprised of multiple services.  For example, an application can have a web app service, database service and cache service.  Datadog monitors each service for metrics such as requests, latency (average, max, p75, p95, p99), error rate, etc.  A resource is a particular query / request to a *service*.  For a web application service, a resource can be /api/apm or /api/trace.  Using a SQL database service as an example, a query (select * from users) is a resource.

### *Final Question*
The world is becoming connected and becoming "smart".  And so, there are many creative ways to monitoring.  IOT and smart devices are becoming mainstream and continuing to advance.  Examples: the connected home and connected car.  Potentially Datadog can be used to collect metrics, events and data in order to aggregate, correlate and analyze.  For example, a set of smart home devices, that may be independent on its own; can be related (high temperature, power usage) can lead to potential power outage.  So some warnings or alerts can be triggered to take some action, such as turning off appliances and/or electronics.  Another example is wine production where the fermentation and production processes are automated and controlled.  Aggregating and correlating metrics, events and data can provide some insightful analytics such that high quality of the wine produced is maintained.
