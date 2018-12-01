# Introduction
Companies are changing the way they access and run application using modern architectures, moving to cloud environments, public, priveate or hybrid. These architectures provide great capabilities in term of scalability and flexibility, but it creates a big challenge to monitor such complex architectures with multiples layers and dependencies. 

Here is when Datadog comes to help, providing a flexible monitoring and analytics cloud platform, able to monitor and analyze traditional and modern application architectures, including cloud environments, containrers, servers, databases, etc. If something is not ready you can create it...

# Prerequisites - Setup the environment

To avoid any compatibility or dependency issues I used an Ubuntu 16.04 VM running on Virtual Box using a Vagrant image. I already had a datadog trial account that was expired, and I requested to extend it in order to run the Challenge.

## Installing the VM environment

First step is to add the box from vagrant catalog to the local vagrant app
```
$ vagrant box add hashicorp-vagrant/ubuntu-16.04
```
Then we have to modify the configuration fiile **Vagrantfile**
```
Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp-vagrant/ubuntu-16.04"
end
```
To start the environment we run the following command:
```
vagrant up
```
Now we have the environment up and running.

<img src="https://github.com/vlorente68/hiring-engineers/blob/master/screenshots/Virtualbox.png?raw=true">

## Installing the agent

Now we have to install the datadog agent into our VM to start monitoring it. It is really easy to do it, just need run the specific command for your OS:

<img src="https://github.com/vlorente68/hiring-engineers/blob/master/screenshots/Agent platform.png?raw=true">


To install the Datadog agent into the Ubuntu server, is as easy as running from a shell the following command:

```
DD_API_KEY=c7c0572c87dc9c1295865e5fb4246307 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```
This is the answer to the command that confirm that the agent is running

<img src="https://github.com/vlorente68/hiring-engineers/blob/master/screenshots/Agent Installed.png?raw=true">

We can see in the [Datadog Host Map](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host) that we are already monitoring it.

<img src="https://github.com/vlorente68/hiring-engineers/blob/master/screenshots/Host Map Initial.png?raw=true">

# Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Datadog uses tags as a mechanism to filter, aggregate and compare metrics and infrastructure elements. Tagging is a very good mechanism to provide flexibility and multi-dimensioning to data.

It is possible to add tags to the datadog agent in the **datadog.yaml** file:

```
tags:
  - owner:vicente
  - project:technical_test
  - region:spain
```
We can see in the [Host Map](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host) the new added tags to the agent:

<img src="https://github.com/vlorente68/hiring-engineers/blob/master/screenshots/Host Map with Tags.png?raw=true">


* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

We are goint to install into our VM the database server MongoDB version 3.6.9 Community Edition by using the following commands:
```
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
$ echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list
$ sudo apt-get update
$ sudo apt-get install -y mongodb-org=3.6.9 mongodb-org-server=3.6.9 mongodb-org-shell=3.6.9 mongodb-org-mongos=3.6.9 mongodb-org-tools=3.6.9
$ echo "mongodb-org hold" | sudo dpkg --set-selections
$ echo "mongodb-org-server hold" | sudo dpkg --set-selections
$ echo "mongodb-org-shell hold" | sudo dpkg --set-selections
$ echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
$ echo "mongodb-org-tools hold" | sudo dpkg --set-selections
```
Now we are going to install the datadog integration for MongoDB following the instruction at the datadog portal:

<img src="https://github.com/vlorente68/hiring-engineers/blob/master/screenshots/MongoDB Integration.png?raw=true">

We run the commands at the MongoDB shell to create a user for datadog:
```
> use admin
switched to db admin
> db.createUser({"user":"datadog", "pwd": "er1RKRdSi10Xoq0Mac64xhAu", "roles" : [ {role: 'read', db: 'admin' }, {role: 'clusterMonitor', db: 'admin'}, {role: 'read', db: 'local' }]})
Successfully added user: {
	"user" : "datadog",
	"roles" : [
		{
			"role" : "read",
			"db" : "admin"
		},
		{
			"role" : "clusterMonitor",
			"db" : "admin"
		},
		{
			"role" : "read",
			"db" : "local"
		}
	]
}
```
To confirm that the user has been correctly created, we run the following:
```
$ echo "db.auth('datadog', 'LJjrd2A9Sdf5LVodMIUmabHe')" | mongo admin | grep -E "(Authentication failed)|(auth fails)" &&
> echo -e "\033[0;31mdatadog user - Missing\033[0m" || echo -e "\033[0;32mdatadog user - OK\033[0m"
datadog user - OK
```
Now we edit the **mongodb.yaml** file to instruct the agent to integrate with MongoDB:

```
instances:
  - server: mongodb://datadog:er1RKRdSi10Xoq0Mac64xhAu@localhost:27017

  tags:
    - database:mongodb
    - project:technical_test
```
And restart the agent

```
sudo systemctl stop datadog-agent
sudo systemctl start datadog-agent
```

Now we can check that the integration is running correctly

```
sudo datadog-agent status
```
<img src="https://github.com/vlorente68/hiring-engineers/blob/master/screenshots/Mongo Check.png?raw=true">

Datadog will provide out of the box [dashboard for MongoDB](https://app.datadoghq.com/screen/integration/13/MongoDB%20-%20Overview?tpl_var_scope=host%3Avagrant&page=0&is_auto=false&from_ts=1543681380000&to_ts=1543684980000&live=true)

<img src="https://github.com/vlorente68/hiring-engineers/blob/master/screenshots/Mongo Dashboard.png?raw=true">

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Datadog has integrations for most of the commercial software platforms in the market, but sometimes it is needed to monitor something that is so unique or home grown that needs to build a custom monitoring. Datadog provides the flexibility to be extended with custom checks to create new metrics.

We need to create a configuration file for the custom check, in this case we will call it **myrandom.yaml**  

```
init_config:

instances: [{}]
```

We need also to create the script that will run to provide the custom metric **myrandom.py**
```
import random

from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"


class CustomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('custom.mycheck', random.randint(0,1000))

```

Now, let's confirm that the custom metric is correctly running at the agent

<img src="https://github.com/vlorente68/hiring-engineers/blob/master/screenshots/Custom Check Agent.png?raw=true">

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

It is possible to adjust the collection interval for checks, just by changing the configuration file, in this case **myrandom.yaml**
```
init_config:

instances:
  - min_collection_interval: 45
```

Automatically we will have the custom check available for the agent, as we can se at the [Host Map](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host)

<img src="https://github.com/vlorente68/hiring-engineers/blob/master/screenshots/Host Map with Custom.png?raw=true">

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

To change the collection interval there is no need to modify the script created, just need to modify the configuration file.

# Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Datadog is an extremely flexible and open monitoring platform, it provides an API to easily integrate with any other external system and control programmaticaly all functionality included into the platform.

We are going to use that API to create a new Timeboard, we will use a python script that call the API **timeseries.py**
```
from datadog import initialize, api

options = {
    'api_key': 'c7c0572c87dc9c1295865e5fb4246307',
    'app_key': 'b0ce75a211360b93300465f78abfc8ce82443c5d'
}

initialize(**options)

title = "Vicente's Dashboard"
description = "Dashboard created through the API"
graphs = [
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:custom.mycheck{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "Random Number"
},
{ 
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mongodb.uptime{*}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Anomalies for MongoDB"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:custom.mycheck{*}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "Random number 1 hour rollup"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)

```
Now we can access our [Dashboard](https://app.datadoghq.com/dash/1006937/vicentes-dashboard?live=true&page=0&is_auto=false&from_ts=1543678463245&to_ts=1543692863245&tile_size=m&tpl_var_host1=vagrant) from the Dashboard list:

<img src="https://github.com/vlorente68/hiring-engineers/blob/master/screenshots/Custom Dashboard.png?raw=true">










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

## Instructions

If you have a question, create an issue in this repository.

To submit your answers:

* Fork this repo.
* Answer the questions in answers.md
* Commit as much code as you need to support your answers.
* Submit a pull request.
* Don't forget to include links to your dashboard(s), even better links and screenshots. We recommend that you include your screenshots inline with your answers.

## References

### How to get started with Datadog

* [Datadog overview](https://docs.datadoghq.com/)
* [Guide to graphing in Datadog](https://docs.datadoghq.com/graphing/)
* [Guide to monitoring in Datadog](https://docs.datadoghq.com/monitors/)

### The Datadog Agent and Metrics

* [Guide to the Agent](https://docs.datadoghq.com/agent/)
* [Datadog Docker-image repo](https://hub.docker.com/r/datadog/docker-dd-agent/)
* [Writing an Agent check](https://docs.datadoghq.com/developers/write_agent_check/)
* [Datadog API](https://docs.datadoghq.com/api/)

### APM

* [Datadog Tracing Docs](https://docs.datadoghq.com/tracing)
* [Flask Introduction](http://flask.pocoo.org/docs/0.12/quickstart/)

### Vagrant

* [Setting Up Vagrant](https://www.vagrantup.com/intro/getting-started/)

### Other questions:

* [Datadog Help Center](https://help.datadoghq.com/hc/en-us)
