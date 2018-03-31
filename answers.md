# Datadog Overview

Datadog is a monitoring and analytics platform for cloud-scale application infrastructure. Combining metrics from servers, databases, and applications, Datadog delivers sophisticated, actionable alerts, and provides real-time visibility of your entire infrastructure.

# Prerequisites - Setup the environment

### Sign up for a free account at https://www.datadoghq.com/
![Get Started Free](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%202.01.34%20PM.png)

### Install the Datadog Agent
###### What is the Agent?
The Datadog Agent is a piece of software that runs on your hosts. Its job is to faithfully collect events and metrics and bring them to Datadog on your behalf so that you can do something useful with your monitoring and performance data. 
![Install the Agent](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%202.09.30%20PM.png)

### Verify the Agent is Reporting Data
To view a list of hosts currently being monitored by Datadog navigate to Infrastructure-->Infrastructure List from the Menu Bar 
![Host Registered and Reporting Data](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%202.20.31%20PM.png)

# Collecting Metrics:
Metrics capture a value pertaining to your systems at a specific point in time.  

### Tags
###### What are Tags?
Tags are a way of adding dimensions to metrics, so they can be sliced, diced, aggregated, and compared on the front end. Using tags enables you to observe aggregate performance across a number of hosts and (optionally) narrow the set further based on specific elements. In a nutshell, tagging is a method to scope aggregated data.

### Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
Edit /etc/datadog-agent/datadog.yaml to set tags on the host
![datadog.yaml](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%2010.18.14%20AM.png)

The view the tags defined on the host navigate to host from the Infrastructure-->Host Map from the Menu Bar
![Host Map](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%2010.19.25%20AM.png)

### Integrations
Datadog has an extensible architecture that allows you to gather information across all your systems, applications, and services.  Quickly enable and configure any of the 200+ out-of-the-box integrations to start the metrics flowing to Datadog’s backend 

### Monitor PostgreSQL
###### Install PostgreSQL if not already present
```
sudo apt-get install postgresql postgresql-contrib
```
To capture PostgreSQL metrics you need to install the Datadog Agent on your PostgreSQL server.

Create a read-only datadog user with proper access to your PostgreSQL Server. Start psql on your PostgreSQL database and run
```
create user datadog with password 'password';
grant SELECT ON pg_stat_database to datadog;
psql -h localhost -U datadog postgres -c "select * from pg_stat_database LIMIT(1);"  
 && echo -e "\e[0;32mPostgres connection - OK\e[0m" || \ ||  
echo -e "\e[0;31mCannot connect to Postgres\e[0m"
```
###### Configure the Agent to connect to the PostgreSQL server 

Edit etc/datadog-agent/conf.d/[postgres.yaml](https://github.com/bschoppa/hiring-engineers/blob/blake/code/postgres.yaml) to include the PostgreSQL configuration details. 

Restart the Agent

Execute the info command and verify that the integration check has passed. 
```
sudo datadog-agent status
```
![agent info](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%203.39.04%20PM.png)

Complete the Integration installation and view the PostgreSQL database metrics from the Postgres Metrics Dashboard 
![postgres metrics](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%2010.26.41%20AM.png)

### Create a custom Agent Check
###### What is an Agent Check?
An Agent Check collects metrics from custom applications or unique systems.  To create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000 2 files need to be created, a check file and configuration file.

The check file that is placed in the checks.d directory.
/etc/datadog-agent.checks.d/[mycheck.py](https://github.com/bschoppa/hiring-engineers/blob/blake/code/mycheck.py)
```
from checks import AgentCheck
from random import *

class MyAgentCheck(AgentCheck):
    def check(self, instance):
        self.gauge('se-exercise.my_metric', randint(0, 1000))
```
The configuration file  is placed in the conf.d directory.
etc/datadog-agent/conf.d/[mycheck.yaml](https://github.com/bschoppa/hiring-engineers/blob/blake/code/mycheck.yaml)
```
init_config:
instances:
    [{}]
```
To verify the health of the Agent Check navigate to Monitors-->Check Summary from the Menu Bar
![custom my_metric check](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%2010.27.36%20AM.png)

To change the check's collection interval so that it only submits the metric once every 45 seconds.  
etc/datadog-agent/conf.d/[mycheck.yaml](https://github.com/bschoppa/hiring-engineers/blob/blake/code/mycheck.yaml)
```
init_config:
    min_collection_interval: 45
instances:
    [{}]
```
###### Bonus Question Can you change the collection interval without modifying the Python check file you created?
Yes, min_collection_interval can be added to the init_config section to help define how often the check should be run. 

# Visualizing Data:
### What is Graphing?
Graphs are the window onto your monitored systems. Most of the times that you visit Datadog, you look at dashboards made up of graphs. Graphs are at the heart of monitoring and observability

###### What are Screenboards & Timeboards?
Graphs on Timeboards will always appear in a grid-like fashion making them generally better for troubleshooting and correlation whereas Screenboards are flexible, far more customizable and are great for getting a high-level look into a system.

Dashboards can be created from the main User Interface or through the Datadog API.  The following [script](https://github.com/bschoppa/hiring-engineers/blob/blake/code/TimeBoard.sh) uses the Datadog APIs to create a Timeboard with the following graphs: 

 * Custom metric: my_metric scoped over the host.
 * Rows Fetched from the Integration on PostgreSQL with the anomaly function applied.
 * Custom metric: my_metric with the rollup function applied to sum up all the points for the past hour into one bucket

![Timeboard created using Datadog API](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%2010.30.05%20AM.png)

To get more granular information, click & drag on a graph to zoom-in on a particular time-frame.  Here you'll see the Visualizing Data Timeboard's timeframe set to the past 5 minutes. By zooming in to the last 5 minutes you can see that the number of rows fetched from PostgreSQL was abnormal and the anomaly above norm was marked in red. 
![Visualizing Data past 5 minutes](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%2010.31.47%20AM.png)

Timely and effective communication is critical when business-critical metrics shift in your infrastructure.  The ability to capture snapshots of meaningful metrics across your infrastructure and notify team members quickly of the problem is so important in the reduction and avoidance of downtime in today's business climate. 
![Visualizer Snapshot Email](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%2010.33.07%20AM.png)

###### Bonus Question: What is the Anomaly graph displaying?
The gray band represents the region where the metric is expected to be based on past behavior. The blue and red line is the actual observed value of the metric; the line is blue when within the expected range and red when it is outside of the expected range.

# Monitoring Data and Alerting
Monitoring all of your infrastructure in one place wouldn’t be complete without the ability to know when critical changes are occurring. Datadog gives you the ability to create monitors that actively check metrics, integration availability, network endpoints, and more.  Notifications are a key component of any monitor. You want to make sure the right people get notified so the problem can be resolved as soon as possible.

The following example will demonstrate how to create a new Metric Monitor that watches the average of the custom metric: my_metric, will alert if it’s above the following values over the past 5 minutes:

 * Warning threshold of 500
 * Alerting threshold of 800
 * Notify you if there is No Data for this query over the past 10m

![configure alert](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%2010.34.04%20AM.png)
![configure alert](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%2010.34.39%20AM.png)

and use different messages based on whether the monitor is in an Alert, Warning, or No Data state.
![different messages](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%2010.34.52%20AM.png)

When the Monitor triggers an Alert an email containing the value of the custom metric and host ip of affected system is generated.
![alert sent](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%206.00.50%20PM.png)

###### Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

Silence alerts from 7pm to 9am daily on M-F
![silence alert config 7p-9a](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%206.38.24%20PM.png)
![silence email 7p-9a](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%2010.36.17%20AM.png)

Silence alerts all day on Sat-Sun
![silence alert config all day](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%206.38.24%20PM.png)
![silence email all day](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%2010.36.26%20AM.png)


# Collecting APM Data:
Datadog APM provides you with deep insight into your application’s performance—from automatically generated dashboards monitoring key metrics, such as request volume and latency, to detailed traces of individual requests—side by side with your logs and infrastructure monitoring.

Datadog Tracing can automatically instrument many widely used Python libraries and frameworks.  The following application[source code](https://github.com/bschoppa/hiring-engineers/blob/blake/code/__init__.py) is instrumented with Datadog's Trace Client.  

Bringing Application and Infrastructure monitoring together alleviates the blind spots and provides you with a cohesive view into the health of your environment.  a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
![Dashboard](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%207.11.29%20PM.png)


![](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%2010.37.01%20AM.png)

![](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%2010.37.13%20AM.png)

![](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%2010.37.22%20AM.png)

![](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%2010.37.35%20AM.png)

![](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%2010.37.46%20AM.png)

###### Bonus Question: What is the difference between a Service and a Resource?

# Final Question:
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?


