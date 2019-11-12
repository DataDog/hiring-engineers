# Introduction

## Agent Install
I have deployed the agent on my Intel Nuc running Ubuntu 18.04. Deployment is done easily by running the following command:

`DD_API_KEY=792aad7f4bd921fba0e91560d2382275 DD_SITE="datadoghq.eu" bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"`

For step-by-step instructions, or other architectures, check out: https://app.datadoghq.eu/account/settings#agent/ubuntu

## Tags
Tags are a convenient way of adding dimensions to metrics. They can be filtered, aggregated and compared in visualizations. Tags are a key:value pair with some restrictions for the key. 

In complex cloud and container deployments, it's a good idea to look at service level in a collection of hosts apposed to looking at a single host due to the dynamic nature.

For more information on tags, take a look at: https://docs.datadoghq.com/tagging/. Using tags in visualisations is described in https://docs.datadoghq.com/tagging/using_tags/?tab=assignment

## Applying tags to Ubuntu
To apply tags to an Ubuntu host, edit /etc/datadog-agent/datadog.yaml. Under **&#64;param tags** you can define your tags.

Here is an example:
```yaml
tags:
  - environment:dev
  - data:dog

```
For a full copy of the yaml, check out [datadog.yaml](https://github.com/arnizzle/hiring-engineers/blob/master/agent/datadog.yaml "datadog.yaml")

This is a screenshot of a host configured with tags:

<img src="https://github.com/arnizzle/hiring-engineers/blob/master/screenshots/host%20tags.png">


## MySQL deployment
I have installed MySQL Server version: 5.7.27-0 on my Ubuntu host.

## Monitoring MySQL
It takes a few steps to monitor MySQL databases with Datadog. First we need to configure some configuration files in the Datadog conf directory (/etc/datadog-agent/conf.d/mysql.d on my host). Then, we create a Datadog user for MySQL.

Step-by-step instructions can be found at: https://docs.datadoghq.com/integrations/mysql/

### Generate some load on MySQL and show some pretty graphs

We can use Sysbench to generate some load on the MySQL database.

### Install sysbench:
```shell
sudo apt-get install sysbench
```

###Create database for Sysbench
Then we create a database and assign privileges to user sysbench:
```sql
    mysql> CREATE DATABASE sysbench;
    mysql> CREATE USER 'sysbench'@'localhost' IDENTIFIED BY 'password';
    mysql> GRANT ALL PRIVILEGES ON sysbench. * TO 'sysbench'@'localhost';
    mysql> FLUSH PRIVILEGES;
```

### Setup MySQL integration in Datadog
Now we are going to setup MySQL integration in the Datadog GUI:
* Go to Integrations - Integrations 
* Type mysql in the search bar
* Click Install


### Show the MySQL dashboard
In the Datadog GUI:
* Click Dashboards
* Click Dashboard List
* Click MySQL - Overview

<img src="https://github.com/arnizzle/hiring-engineers/blob/master/screenshots/MySQL%20Sysbench.png">

### Run Sysbench

Now we can go to the directory with Sysbench config files (/usr/share/sysbench) and run the command:

```shell
sysbench oltp_read_only.lua --threads=4 --mysql-host=localhost --mysql-user=sysbench --mysql-password=password --mysql-port=3306 --tables=10 --table-size=1000000 prepare --db-driver=mysql```

Output should be similar to:
    sysbench 1.0.11 (using system LuaJIT 2.1.0-beta3)

    Initializing worker threads...
    Creating table 'sbtest2'...
    Creating table 'sbtest1'...
    Creating table 'sbtest4'...
    Creating table 'sbtest3'...
    Inserting 1000000 records into 'sbtest2'
    Inserting 1000000 records into 'sbtest1'
    Inserting 1000000 records into 'sbtest4'
    Inserting 1000000 records into 'sbtest3'
```
    
### Note
For an extensive guide into Sysbench, take a look at: https://severalnines.com/database-blog/how-benchmark-performance-mysql-mariadb-using-sysbench

## Running and monitoring MySQL on Docker

* In the Datadog GUI Click Integrations, and search for Docker.
* Install the Docker Integration, and click Configuration.
* Follow the steps to add dd-agent to the Docker group and allow the agent to connect to docker
* Restart the agent on your host

### Pull MySQL image
Next we are going to pull the MySQL image.

```shell
arne@nuc:~$ docker pull mysql/mysql-server:5.7
5.7: Pulling from mysql/mysql-server
a316717fc6ee: Pull complete 
b64762744f75: Pull complete 
a1f742e3aa43: Pull complete 
f71a5f0dcc26: Pull complete 
Digest: sha256:5396bc60a6c08abb6b7e8350b255324a91ee9f3ea11f009aea3e4b61ead38bf6
Status: Downloaded newer image for mysql/mysql-server:5.7
docker.io/mysql/mysql-server:5.7
```

### Run container
and run the container, using a different port (optional if there is no MySQL running locally)

```shell
arne@nuc:~$ docker run --name=mysql1 -d mysql/mysql-server:5.7 -p 33060:3306
0ad5b981857a43a828ae60c729257c4a3aa9b9ef0282046fd35c34247d42f330

```

### Get password
We have to find out the auto-generated password:

```shell
arne@nuc:~$ docker logs mysql1 2>&1 | grep GENERATED
[Entrypoint] GENERATED ROOT PASSWORD: 3M2EkVaNiqIK@hYLBIhedYpG3L0N

```

### Login MySQL
and log in to the container using the generated password

```shell
arne@nuc:~$ docker exec -it mysql1 mysql -uroot -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 5
Server version: 5.7.28

```
### Create MySQL database for Sysbench
We are going to generate some load using Sysbench. First we need to create a database and user for Sysbench
**Note: The Commands Used For The Docker Container Are Slighly Different From The Local Mysql Deployment since we are going to connect over TCP versus local socket. With the GRANT PRIVILEGES command we allow access from ANY host. **

```shell
mysql> CREATE DATABASE sysbench;
mysql> CREATE USER 'sysbench'@'localhost' IDENTIFIED BY 'password';
mysql> GRANT ALL PRIVILEGES ON sysbench. * TO 'sysbench'@''%;
mysql> FLUSH PRIVILEGES;
```

### Install sysbench:
```shell
sudo apt-get install sysbench
```
### Run some load
Finally we can run the Sysbench command. Note that the host is NOT localhost since that would connect to a socket. Instead an IP address is used to force a TCP connection. Also, we are using a different port to match that of the container.

```shell
sysbench oltp_read_only.lua --threads=4 --mysql-host=127.0.0.1 --mysql-user=sbtest --mysql-password=password --mysql-port=33060 --tables=10 --table-size=1000000 prepare --db-driver=mysql
```

### Custom Agent Check

In this example we are going to deploy a custom agent check. Custom agent checks run at a regular interval which defaults to every 15 seconds and are recommended to collect metrics for custom applications or unique systems. Alternatively you can write a full fledged integration if you want to share your application (commercially or open soruce).

For more information on customer agent checks check out: https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6 and the full fledged integration can be found here: https://docs.datadoghq.com/developers/integrations/new_check_howto/

### Deploying the custom agent check

First we are going to create a hello.yaml in the *conf.d/ *directory of the agent. This needs to cointain a sequence called *Instances*  that has a mapping, but that can be empty.

     
	 conf.d/hello.yaml
	     instances: [{}]
		 

Next we are going to deploy the code in *checks.d *.

```python
# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from old versions of the Agent...
	from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.1"


class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', 1, tags=['data:dawg'])


```

### Modifying interval and data
To modify the interval of the checks, you can simply modify the conf.d/hello.yaml with the following code:

    init_config:
    
    instances:
      - min_collection_interval: 45
	  

To make the ouput of the check a little more interesting, we modify the code to generate a random number.

    # the following try/except block will make the custom check compatible with any Agent version
    import random
    
    try:
        # first, try to import the base class from old versions of the Agent...
        from checks import AgentCheck
    except ImportError:
        # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck
    
    # content of the special variable __version__ will be shown in the Agent status page
    __version__ = "1.0.2"
    
    
    class HelloCheck(AgentCheck):
        def check(self, instance):
            self.gauge('my_metric', random.randint(1,1000), tags=['data:dawg'])
    
    

## Visualizing Data - 99 problems but a graph aint one

The advantage of using graphs is that they represent complicated sets of data, or a plethora of data points in an easy to understand visual way. Fortunatly Datadog has a lot of ways to integrate graphs and make it easy to point out any anomalies in your environment, thereby reducing potential downtime.

There are multiple ways to create graphs. First we are going to start by creating a Timeboard via the GUI. Click *Dashboards - New Dashboard. *Give it a nice name and click *New Timeboard.*

Now we can add a graph by clicking *Add Graph*.

What we want is a rollup value of My Metric scoped over host Nuc. We can do this by entering My Metric after the Metric dropdown box as seen below.

<img src="https://github.com/arnizzle/hiring-engineers/blob/master/screenshots/Query%20Value.png">

The next step is to add the rollup code. We can do this by selecting the Code editor.

<img src="https://github.com/arnizzle/hiring-engineers/blob/master/screenshots/Enter%20Code.png">

Now we can add the rollup function like so:
<img src="https://github.com/arnizzle/hiring-engineers/blob/master/screenshots/rollup.png">

### Visualizing Data with a script
To make life easier, we can also create script to automate the task of Timeboards. The following script updates an existing timeboard with the following:
* My metric scoped over host NUC.
* The anomalies of MySQL performance queries by host
* My metric with the rollup function applied to sum up all the points for the past hour into one bucket

```python
from datadog import initialize, api
import time
from pprint import pprint

options = {
    'api_key':'8f2c00900af7e1873d6d32de9b335201',
    'app_key':'64fe39f9adb2e2976f047d580af637d4793f87f8',
    'api_host': 'https://api.datadoghq.eu'
}

initialize(**options)

title = 'My Timeboard'
description = 'My Metric and MySQL Anomalies!'
graphs = [ {'definition': 
             {'events': [],
                'viz': 'query_value',
                'requests': [{
                'q': 'avg:my_metric{host: nuc}.rollup(sum,3600)'}
               ],
             },
               'title': 'Cumulative Value of My Metric rolled up',
             },
           {'definition': 

             {'legend_size': '0',
              'events': [],
                'requests': [{
                'q': 'sum:my_metric{host:nuc}'}],
                'type': 'alert_graph'
             },
             'title': 'Average Value of My_Metric scoped over Nuc'
            },

           {'definition': 
             {'events': [],
                'requests': [{
                'q': "anomalies(avg:mysql.performance.queries{*} by {host}, 'basic', '2', 'direction=both' )",
                'display_type': 'line',
             }],
            'precision': '0',
            'autoscale': 'true',
            'viz': 'timeseries'},
            'title': 'Anomalies MySQL Performance queries'
           },
        ]

title = 'Timeboard My Metric and Anomalies'
layout_type = 'ordered'
description = 'A dashboard with My Metric rollup function and MySQL anomalies'
read_only = False
notify_list = ['arne.polman@gmail.com']
template_variables = [{
    'name': 'NUC',
    'prefix': 'host',
    'default': 'NUC'
}]

pprint (api.Timeboard.update(
    9192,
    title=title,
    description=description,
    graphs=graphs,
    template_variables=template_variables,
    read_only=read_only,
))
```

The end result looks like this:
<img src="https://github.com/arnizzle/hiring-engineers/blob/master/screenshots/Timeboard%20from%20Python.png">

We have set the SQL graph for anomaly detection, and as you can see we have found an anomaly within the performance queries (by running a Sysbench on a idle system).

<img src="https://github.com/arnizzle/hiring-engineers/blob/master/screenshots/SQL%20Anomaly%20and%20Snapshot.png">

By clicking the box with the arrow above a graph we can send an image of the graph to our team members.

<img src="https://github.com/arnizzle/hiring-engineers/blob/master/screenshots/Screenshot%20Sent%20to%20Self.png">

In this graph we can see a line showing performance. It is initially flat because the system is idle. After we run a benchmark, we quickly can see the line turning red indicating there is an anomaly detected. The grey area shows the bounderies for anomalies and in this picture is kind of misformed because of the massive difference between idle mode and the benchmark running.

### Monitoring Data

Looking at graphs all day can get tedious despite the beauty of said graphs. So in this example we are going to create a monitor. We have a metric called "My Metric" which can have a value from 0 to 1000. Everything under 500 is nothing to worry about, but we start getting worried when the value is over 500 and total panic mode ensues if the value is over 800 OR if there is no value being reported for the metric.

Go to the GUI and click *Monitor - New Monitor *. We are going to select *Metric*  and search for My Metric after the metric field.

Next, we are going to set the proper values for *Alert * and *Warning* tresholds.

We want to *Notify* if the value is not reported for 10 minutes.

And we want to add the following script to the *Say what is happening * field.

    {{#is_alert}}
    OMG, my metric exceeds 800!
    Currently at {{value}}
    {{/is_alert}} 
    
    {{#is_warning}}
    Watch out now! My Metric is over 500!
    Now at {{value}}
    {{/is_warning}} 
    
    {{#is_no_data}}
    No my metric heartbeat detected! 
    Everything ok?
    {{/is_no_data}}  @arne.polman@gmail.com
    
    {{#is_recovery}}
    Phew, close one! Everything ok now.
    {{/is_recovery}} 

Lastly, we are going to inform a user by selecting the user from the dropdown box in *Notify your team*. This will send out an email if a treshold is reached or when things are back to normal.

<img src="https://github.com/arnizzle/hiring-engineers/blob/master/screenshots/Monitoring%20Screenshot.png">

Now we have deployed all of the alerting, we are going to disable it for non-working hours. Obviously we would like to be notified that we will no longer receive alerts during this window.

We can set this up by clicking *Monitor - Manage downtime*. Then we click *New downtime* and select the timerange we want for the downtime.

In the example below we have downtime scheduled for Monday to Friday from 19:00 until 09:00 and we have downtime in the weekend. We are informing the user that no alerts will be send during this timeframe. 

<img src="https://github.com/arnizzle/hiring-engineers/blob/master/screenshots/No%20Notification.png">




## Tracing a Flask app

Tracing with Datadog is a very easy task. Take a look at the following code.

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

In order to trace this application in Datadog we have to do the following:
* Install Datadog agent
* Integrate Flask with Datadog
* Configure Datadog to collect metrics
* Configure the Datadog agent for logging

#### Install the Datadog Agent
On the server where your Flask app is running, you will need to install the Datadog Agent so you can start monitoring your application. ou can retrieve the Agent installation command for your OS, preconfigured with your API key, [here if you are in the US](https://app.datadoghq.com/account/settings#agent "here if you are in the US") or [here](https://app.datadoghq.eu/account/settings#agent "here") if you are in Europe. (You need to be logged in to your Datadog account to access the customized installation command.

#### Integrate Flask with Datadog
Now we need to install dd-trace, Datadogs Python tracing client library. The Agent uses this library to trace requests to your application and collect detailed performance data about your application:

```bash
pip install ddtrace
```

#### Configure the Datadog agent for logging
First, we need to enable logging on the Datadog agent. We can do this by modifying the Agent configuration file. The path to the log file on your OS can be found [here](https://docs.datadoghq.com/agent/basic_agent_usage/ "here") (US) or [here](https://docs.datadoghq.eu/agent/basic_agent_usage/ "here") (Europe). 

Then, make sure `logs_enabled: true` is enabled and uncommented.

    logs_enabled: true

Next, we are going to create a Python configuration in the [conf.d/ directory](mkdir conf.d/python.d # Create a Python config directory under conf.d vi conf.d/python.d/conf.yaml # Create and open the config file` "conf.d/ directory"). 

    # Create a Python config directory under conf.d
    mkdir conf.d/python.d
    # Create and open the config file`
    vi conf.d/python.d/conf.yaml 

and add the following lines:
    init_config:
    
    instances:
    
    logs:
    
      - type: file
        path: /var/log/my-log.json
        service: flask
        source: python
        sourcecategory: sourcecode

**Note: make sure the agent has read/write access on /var/log/my-log.json **

<img src="https://github.com/arnizzle/hiring-engineers/blob/master/screenshots/flask.png">

#### Configure Datadog to collect metrics
The beauty about dd-trace is that it can collect data about your application without making any changes to your code. You do need to run your code using the ddtrace-run wrapper:

    FLASK_APP=sample_app.py DATADOG_ENV=flask_test ddtrace-run flask run --port=4999


**Note: By default Flask runs on port 5000, but this is the port of the Datadog agent as well.
**

### Troubleshooting

#### datadoghq .com or .eu
Should the Flask app not report traces, the first thing to do is figure out if the agent is configured to run in your correct zone (.com or .eu). You can do this by editing datadog.yaml in your datadog-agent/ directory. The second parameter (site:) defaults to datadoghq.com and should be replaced by datadoghq.eu if you are in Europe.

    ## @param site - string - optional - default: datadoghq.com
    ## The site of the Datadog intake to send Agent data to.
    ## Set to 'datadoghq.eu' to send data to the EU site.
    #
    site: datadoghq.eu
    
    

#### API key
Then figure out if your API key is valid by running the following command: 
`sudo  datadog-agent status | grep -i -A 3 'API Keys status'`

This should show the following:
    arne@nuc:/etc/datadog-agent$ sudo  datadog-agent status | grep -i -A 3 'API Keys status'
    [sudo] password for arne: 
      API Keys status
      ===============
        API key ending with 82275: API Key valid

You can also check if the agent is reporting via the GUI, by checking Infrastructure - Host Map.

#### Trace the traces
To check if traces are being accepted you can check the contents of /var/log/datadog/trace-agent.log If the following is shown, please recheck all the steps.

    2019-11-12 11:34:16 CET | TRACE | INFO | (pkg/trace/info/stats.go:101 in LogStats) | No data received
    2019-11-12 11:35:16 CET | TRACE | INFO | (pkg/trace/info/stats.go:101 in LogStats) | No data received
    2019-11-12 11:36:26 CET | TRACE | INFO | (pkg/trace/info/stats.go:101 in LogStats) | No data received
    2019-11-12 11:37:36 CET | TRACE | INFO | (pkg/trace/info/stats.go:101 in LogStats) | No data received
    2
	


