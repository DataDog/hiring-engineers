## Overview

Welcome to a whirlwind tour of datadog!  

Datadog is the leading cloud based platform for instrumenting, monitoring, visualizing, and managing all levels of cloud and server infrastructure, all layers of the application stack, and hundreds of other integrations that will prove invaluable to developers, cloud and systems engineers, or for that matter anyone else who wants deep insight into how things are running!


This exercise is intended to help you get up and running with datadog and walk through some of the key features and capabilities including:
- Getting started and installing
- Collecting "out of the box" and custom metrics
- Visualizing your data
- Monitoring and alarming
- A closer look at application performance monitoring
- Other ways to use datadog and upcoming features

#### Assumptions and pre-requisites
In an attempt to keep the focus on datadog and its features - the below pre-requisite steps will not be documented as part of this exercise.
- A datadog account has been setup
- Linux based VM's have been provisioned for the purpose of this exercise.  This can be a local VM, your macbook pro, or a cloud instance.


## Getting started
Datadog has the ability to ingest metrics in a few different ways including:
- Installation of an agent on a virtual machine host.  The agent will collect resource utilization metrics and turn-key metrics for many commonly installed components of your stack such as MySQL or IIS.  Additionally an agent can monitor docker containers running on the host.
- Integration with another cloud provider or service, such as AWS or Microsoft Azure.  No agent needed here however datadog will require permissions to pull metrics from a specific account.
- Datadog customers can send metrics directly to datadog from applications or elsewhere using the datadog API.

In order to demonstrate some of datadog's core features, we will be collecting metrics from a datadog agent installed on a linux VM.

Login to your datadog account and follow the steps below to start collecting metrics.

#### Installing the agent
- With datadog's heavy emphasis on devops and automation, installing the datadog agent on a linux vm host is generally nothing more than pasting a simple one liner.  
- For most OS flavors and configuration management tools (i.e. Ansible, Chef) datadog has taken the guess work out and provided scripts and templates that can be run with little or no modification.

From the datadog web console, navigate to "Integrations -> Agent" and we can find instructions for our specific host type.
Choose Ubuntu and the one line command can be found in step 1 under "Use our easy one-step install"
(AgentInstall.png)

From our Ubuntu instance cli paste the command to fetch and run the install script with some expected output shown below:
```bash
$ DD_API_KEY=6c2db0****************** bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"
. . .
* Adding your API key to the Agent configuration: /etc/dd-agent/datadog.conf

* Starting the Agent...


Your Agent has started up for the first time. Were currently verifying that
data is being submitted. You should see your Agent show up in Datadog shortly
at:

    https://app.datadoghq.com/infrastructure

Waiting for metrics.................................

Your Agent is running and functioning properly. It will continue to run in the
background and submit metrics to Datadog.

If you ever want to stop the Agent, run:

    sudo /etc/init.d/datadog-agent stop

And to run it again run:

    sudo /etc/init.d/datadog-agent start
```

Once the agent is installed  - we can return to the Datadog web console and verify that the agent has checked in and is sending metrics.  One way to do this is to check Infrastructure -> Infrastructure List.

You will see that the agent shows a Status of up and is reporting metrics.  Clicking the hostname link will show details on server resource utilization metrics.

(InfrastructureList.png)

(ServerMetrics.png)


### Collecting metrics

Now that we have successfully integrated some of our server infrastructure with DataDog we can tag and customize metrics collection as needed.

#### Tagging

**Why?** Adding tags to datadog metrics, machines, and integrations provides a powerful way to query, organize, and filter data and metrics.

**How?**  
Tags can be applied in the following ways:
- Specifying tags in datadog agent config file
- Adding tags manually (from the web console or datadog API)
- Inheriting tags automatically from a datadog integration (e.g. AWS EC2 AMI name)

For more details see [here](https://docs.datadoghq.com/guides/tagging/)

**What about a real world example?**
Lets say we would like to organize our servers by environment (dev, test, prod), layer of the stack (web, db), key component (mysql, activemq), etc.
On a linux or windows machine, we can apply a meaningful tag by updating the datadog agent configuration file and restarting the agent.

We can add tags to the linux agent by adding the following comma separated line in /etc/dd-agent/datadog.conf.

**Note:** It is *highly* recommended that management of this config file be done using tools such as puppet,chef, splunk or any similar automation strategies.

Key:value pairs or a tag name by itself are both supported.
```
tags: <tag1 key>:<tag1 value>, <tag2>
```

*Step 1: backup the dd config file*
```
$ sudo cp /etc/dd-agent/datadog.conf /etc/dd-agent/datadog.conf.original
```

*Step 2: define your tags as an ENV var*
lets apply 3 tags to this server
```
$ export TAGS="env:test, layer:db, exercise"
```
*Step 3: update the config file*
lets avoid manually editing a file, this command will replace existing tags or add the line
```
$ sudo sed -i "s/^tags:.*/tags:${TAGS}/g" /etc/dd-agent/datadog.conf || echo "tags:${TAGS}" | sudo tee -a /etc/dd-agent/datadog.conf
```
verify that the appropriate line has been added
```
$ sudo grep -e '^tags:' /etc/dd-agent/datadog.conf
tags:env:test, layer:db, exercisedd
```

*Step 4: restart the agent*
```
sudo service datadog-agent restart
```

Now we can verify that tags have been applied from the datadog console.

We can also filter or group using tags.
Heres an example to group by the env tag

#### integrations
Datadog has turn-key support to integrate with and monitor dozens of applications and services.
**Why?**
Lets say we need to get application, platform, or vendor specific metrics.
A common example is a database engine such as MongoDB running on one of our server instances.

To illustrate this we will enable the MongoDB integration on the server where the datadog agent is currently running.
To focus on operation and features of datadog we will not include steps to install/configure mongodb itself.

To enable an integration for your MongoDB database we will need to:
- Create a read only user for datadog to use to connect to your mongodb database.
- Create a mongo.yml file under the datadog agent configuration that specifies where to connect and what to monitor
- Restart the datadog agent and verify that the mongo check is running correctly
- Enable the integration from the datadog web console

Datadog has provided concise and easy-to-follow steps here:
https://docs.datadoghq.com/integrations/mongo/

Once the integration has been enabled we can verify that metrics are coming in by using the metrics explorer.
From the datadog web console:
*Metrics -> explorer*

We can view data for a few different mongodb related metrics by searching mongodb in the Graph field.

(MongoMetrics.png)

#### Custom checks
Datadog also allows developers and ops team members to write custom checks.
**Why?**
This can be very useful when we want to monitor something that is not covered by one of the turn-key integrations OR we want to send custom metrics data into datadog.

Plugins are simple python scripts paired with a custom yaml file that defines what and how we are collecting data.

Below steps are based on instructions that can be found here:
https://docs.datadoghq.com/guides/agent_checks/

*Step 1: setup our script to send a custom metric*
A very simple script that generates a random number and sends as a metric to datadog.
This script needs to be deloyed as /etc/dd-agent/checks.d/exercise.py
```
from checks import AgentCheck
from random import *

class RandomValues(AgentCheck):
  def check(self, instance):
	 metric_value = randint(1, 1000)
   self.gauge('my_metric', metric_value)
```

*Step 2: setup our yaml file*
We can setup a dummy yaml file which does nothing more than tell the check how often to run
Deploy as /etc/dd-agent/conf.d/exercise.yaml
```
init_config:
    min_collection_interval: 20
instances:
    [{}]
```

*Step 3: restart datadog agent and verify the check*
Run the command to restart the agent and then run the info command to check the status of all the checks:
```
sudo service datadog-agent restart
sudo service datadog-agent info
...
exercise (custom)
-----------------
  - instance #0 [OK]
  - Collected 1 metric, 0 events & 0 service checks
...
```

We can now check the console - metrics explorer for my_metric to view the metrics being sent:

(CustomCheck.png)

*Updating the collection interval*
If we want to change the minimum collection interval to a different value, such as 45, we can simply change ```min_collection_interval``` param in the /etc/dd-agent/conf.d/exercise.yaml to the desired number of seconds and restart the agent.

(CustomCheck45.png)

*Bonus - do we need to modify the python script to change the interval?*
This should be done from the yaml file - no need to update the python script itself


#### Timeboards and the api

We can setup some example time series Dashboards using the API invoked from a bash script.
The simple bash script will add time boards to our console that will show:
- Our custom metric of random numbers
- Mongodb connections with anomaly detection
- A rollup of my random number metric to show hourly totals

Here is the bash script with the API call that will create this
```
#!/bin/sh
# Make sure you replace the API and/or APP key below
# with the ones for your account

api_key=6c2************
app_key=0b3a**************

curl  -X POST -H "Content-type: application/json" \
-d '{
      "graphs" : [{
          "title": "My Custom Metric of Random Numbers over time 2",
          "definition": {
              "events": [],
              "requests": [
                  {"q": "max:my_metric{host:i-0fb04cbc261bf905c}"}
              ]
          },
          "viz": "timeseries"
      },
	{
          "title": "Mongodb connection count",
          "definition": {
              "events": [],
              "requests": [
                  {
			"q": "anomalies(max:mongodb.connections.current{host:i-0fb04cbc261bf905c}, 'basic', 2)"
		}
              ]
          },
          "viz": "timeseries"
      },
{
          "title": "My metric - random numbers hourly totals rolled up",
          "definition": {
              "events": [],
              "requests": [
                  {
                        "q": "avg:my_metric{host:i-0fb04cbc261bf905c}.rollup(sum, 3600)"
                }
              ]
          },
          "viz": "timeseries"
      }
	],
      "title" : "Exercise Timeboards",
      "description" : "A few graphs for the exercise",
      "template_variables": [{
          "name": "host1",
          "prefix": "host",
          "default": "host:my-host"
      }],
      "read_only": "True"
    }' \
"https://app.datadoghq.com/api/v1/dash/421315?api_key=${api_key}&application_key=${app_key}"
```

Now we have a nice dashboard:

(Dashboard.png)


We can make a few adjustments - zoom into the last 5 minutes and send ourselves a snapshot of the graph:

(Snapshot.png)


#### Monitoring and alerting on our Metrics
For datadog to be useful in a production environment - we can create monitors off of our data.

The following shows a monitor that will:
- Set a warning (lower) and alert threshold (higher) to alert on
- Also alert on missing data (that way we know if the check itself stops reporting metrics)
- Define how the alert text will look and who to notify. Including the hostname and IP if its an alert

(Monitor1.png)

(Monitor2.png)

(AlertEmail.png)


##### Setting downtime for a monitor
Lets say we don't want this monitor to be checking the thresholds due to planned maintenance or just periods of time that the application is not required to be available.

We can schedule a "Downtime for the monitor".
In the console Monitors -> Manage Downtime -> Schedule Downtime
A few examples of scheduling downtime on a recurring basis:
(Downtime1.png)
(Downtime2.png)
Notify appropriate parties when a downtime is scheduled:

(DowntimeEmail.png)

#### Using the APM to instrument your application performance

Using a simple python flask web app - we can show datadogs ability to monitor code traces.

**Why?**
This can be very useful in identifying performance bottle necks and issues within applications, something difficult to gauge with infrastructure sourced metrics.

Instructions to instrument the application can found within the datadog console:
We will follow those instructions to run our application with dd-trace and a simple python flask script - flash.py
https://app.datadoghq.com/apm/docs

Running flash.py web service with dd-trace:
```
$ ddtrace-run python flash.py
DEBUG:ddtrace.writer:resetting queues. pids(old:None new:1049)
2017-12-14 19:43:44,382 - ddtrace.writer - DEBUG - resetting queues. pids(old:None new:1049)
DEBUG:ddtrace.writer:starting flush thread
2017-12-14 19:43:44,383 - ddtrace.writer - DEBUG - starting flush thread
INFO:werkzeug: * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
2017-12-14 19:43:44,385 - werkzeug - INFO -  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
DEBUG:ddtrace.api:reported 1 services
2017-12-14 19:43:44,387 - ddtrace.api - DEBUG - reported 1 services

# make a few sample web requests
$ curl http://127.0.0.1:5000/
$ curl http://127.0.0.1:5000/api/apm

```

See the metrics in the datadog APM console

(APM.png)

##### Putting it all together
We can display performance data for our infrastructure (agent based metrics) and application (apm)
(Combined.png)

##### Services and resources in the APM
*Services:* I like to think of a service as a particular function or process that is servicing a request, such as a web server or a database server.

*Resources:* A resource would be the underlying request thats being past down to the service, for example a web service would have different requests for content etc as different resources that can be queried to provide metric data.


#### Other use cases for datadog

An interesting use case that would apply to the everyday lives of thousands of consumers might be to capture fitness tracker data and metrics into datadog.

Many  of the popular fitness trackers track:
- daily activity minutes
- steps taken
- sleep stats
- heart rate
- calories burned

Many of datadog's features would make for interesting analysis for example:
- look at monthly and yearly activity levels
- combine and correlate activity data with other data sources, ie research study data etc.
- provide custom daily reports to health care professionals
- Monitor and notify when one or a combination of interesting metrics behaves in a certain way

Open source projects exist to capture this data and feeding it into datadog would not be difficult.
