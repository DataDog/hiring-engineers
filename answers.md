# Datadog Overview



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
### Describe what Metrics are and the importance of monitoring

### Tags
###### What are Tags?
Tags are a way of adding dimensions to metrics, so they can be sliced, diced, aggregated, and compared on the front end. Using tags enables you to observe aggregate performance across a number of hosts and (optionally) narrow the set further based on specific elements. In a nutshell, tagging is a method to scope aggregated data.

### Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
Edit /etc/datadog-agent/datadog.yaml to set tags on the host
![datadog.yaml](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%2010.18.14%20AM.png)

The view the tags defined on the host navigate to host from the Infrastructure-->Host Map from the Menu Bar
![Host Map](https://github.com/bschoppa/hiring-engineers/blob/blake/images/Screen%20Shot%202018-03-30%20at%2010.19.25%20AM.png)

### Integrations
Describe Integrations

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

Utilize the Datadog API to create a Timeboard that contains:

Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timemboard.

Once this is created, access the Dashboard from your Dashboard List in the UI:

Set the Timeboard's timeframe to the past 5 minutes
Take a snapshot of this graph and use the @ notation to send it to yourself.
Bonus Question: What is the Anomaly graph displaying?

# Monitoring Data
Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

Warning threshold of 500
Alerting threshold of 800
And also ensure that it will notify you if there is No Data for this query over the past 10m.
Please configure the monitor’s message so that it will:

Send you an email whenever the monitor triggers.

Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

When this monitor sends you an email notification, take a screenshot of the email that it sends you.

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.
Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

# Collecting APM Data:
Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

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
Note: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

Bonus Question: What is the difference between a Service and a Resource?

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

# Final Question:
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?


