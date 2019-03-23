This exercise has been a great deal of fun. I've become fully immersed in it over the last two weeks. It's been an incredibly effective way to get me familiar with Datadog's services. It's also helped me to realize that there's so much more to learn about this product, and I'm really psyched about the opportunity to do just that. So take a gander, enjoy the ride, and let me know of any feedback you've got for me.	~ Russel


[Prequisites](/answers.md#prerequisites---setup-the-environment)

[Collecting Metrics](/answers.md#collecting-metrics)

[Visualizing Data](/answers.md#visualizing-data)

[Monitoring Data](/answers.md#monitoring-data)

[Collecting APM Data](/answers.md#collecting-apm-data)

[Final Question](/answers.md#final-question)



Prerequisites - Setup the environment:
======================================
So, a little context on this:


I ended up using vagrant after exploring Docker and just using a standalone VM. I chose vagrant because I had an existing Ubuntu VM environment that I wanted to "vagrantize", if you will. I realize now that this somewhat defeats the purpose of vagrant boxes, as they should be small, and include provisions in the form of a shell script in the vagrant file in order to have the most portable box possible. Doombox has those provisions on the inside so it's a *little* big. If I were to approach this a second time, I would provision the vagrant box by the more standard convention, or use docker.

On the bright side, since Doombox is basically a full fledged Ubuntu machine, you can interact with it's UI by enabling that option in the vagrant file, or by clicking "show" in your VirtualBox dashboard for the machine. If you did that you could always fire up DOOM while you're in there ```/home/vagrant/restful-doom/src/restful-doom -iwad Doom1.WAD -apiport 6666 ...``` and, as you may have noticed, play the game via API calls, but that's another story for another day.

#### With all that said, [Here's Doombox in all its glory on VagrantCloud](https://app.vagrantup.com/russelviola/boxes/doombox/versions/1.0.1) (Spoiler, it's a large file)

#### To get started with this, on a machine with vagrant installed run:

```
vagrant init russelviola/doombox 
vagrant up
```

- I'm working out the kinks with the auto-ssh configuration, so you'll probably see some ```default: Warning: Authentication failure. Retrying...``` errors before the machine gives up. That's a work in progress.

- **_Then_**, when the machine tires and finally gives up all hope of connecting via private key, you can use ```vagrant ssh```, you'll be prompted for a password, which is ```vagrant```


You don't necessarily need to run this to understand my approach to this exercise, as I've documented that below, but I wanted to include access to the environment; 1. because that's what vagrant is for, and 2. in the case that you'd like to explore my environment with all of the following requirements implemented.

___
Collecting Metrics:
===================
To install the agent, We can follow the steps for [Ubuntu Datadog Agent Integration](https://app.datadoghq.com/account/settings#agent/ubuntu) and run 

```
DD_API_KEY=<YOUR_API_KEY> -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

Which starts up the agent after installation. Then we can look to our [Datadog Host Map](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host) and see it's installed, we'll see something like this: 

<img src="/HiringEngineersScreenShots/UbuntuHostShot.png" alt="Ubuntu Host Map Icon" height="500" />

### - Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Since we're using a Linux system, our Agent config file lives at [```etc/datadog-agent/datadog.yaml```](/dataDogVagrant/agent-configuration/datadog-agent-config/datadog.yaml). We can open this with our favorite IDE and take a look inside.
the top of the file will show your API key, so you know you're in the right place.
```yaml
# The Datadog api key to associate your Agent's data with your organization.
# Can be found here:
# https://app.datadoghq.com/account/settings
api_key: ad00c177c779cc3d503ee10c55c302dd

# The site of the Datadog intake to send Agent data to.
# Defaults to 'datadoghq.com', set to 'datadoghq.eu' to send data to the EU site.
# site: datadoghq.com

# The host of the Datadog intake server to send Agent data to, only set this option
# if you need the Agent to send data to a custom URL.
# Overrides the site setting defined in "site".
# dd_url: https://app.datadoghq.com
```
If we look down to around row 48 we'll see the ```tags``` configuration. Un-comment the line and add our tags:
```yaml
# Set the host's tags (optional)
tags:
  - name:doombox
  - env:dev
  - role:virtual_machine
  - test_tag:hello
```
#### It's important to note that when we make changes to the agents configuration files, we need to restart it for them to take effect. In the cli run ```service datadog-agent restart```

Once our agent is up and running again, after a minute or two we'll see the results reflected on our [Host Map Details](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host&host=878227842):

<img src="/HiringEngineersScreenShots/HostDashTags.png" alt="Host Tag View" height="230" />

These tags will help us later on when we're building dashboards to view all of the data coming from the Datadog Agent.

### - Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

#### The first thing we have to do is get PostgreSQL squared away.

First Install PostgreSQL with ```sudo apt-get install postgresql```

Then we can follow the [PostgreSQL Integration Guide](https://docs.datadoghq.com/integrations/postgres/):

We can get into the postres console as root ```sudo -u postgres psql```, then create a new user, datadog.

```
create user datadog with password '<PASSWORD>';
grant pg_monitor to datadog;
```

The second command here, is granting 'datadog' access to all of those sweet, sweet metrics that PostgreSQL collects for itself as it runs. Now, the next part isn't totally necessary, but I thought it would be nice to see an actual database connected to the agent. I brought in [WorldDB](/dataDogVagrant/world-1.0/dbsamples-0.1/world) a simple SQL database for development purposes:

while in the postgres console:
```
CREATE DATABASE worlddb;
```
from [WorldDB directory](/dataDogVagrant/world-1.0/dbsamples-0.1/world):
```
sudo psql -U postgres -d worlddb -f world.sql
```
and just like we did with ```pg_monitor``` in our postgres console, ```grant worlddb to datadog;```

#### The second piece to the integration is configuring the agent itself. We're going to be making changes to [```etc/datadog-agent/conf.d/postgres.d/conf.yaml```](https://github.com/RusselViola/hiring-engineers/blob/master/dataDogVagrant/agent-configuration/datadog-agent-config/conf.d/postgres.d/conf.yaml):
```yaml
init_config:

instances:
  - host: localhost
    port: 5432
    username: datadog
    password: datadog
    dbname: worlddb
    ssl: False
    use_psycopg2: False # Force using psycogp2 instead of pg8000 to connect. WARNING: psycopg2 doesn't support ssl mode.
    tags:
      - db_tag
      - optional_tag2
```
The agent will log into postgres as the ```datadog``` user we created via ```localhost``` and connect to ```worlddb```
```yaml
#    Collect metrics regarding PL/pgSQL functions from pg_stat_user_functions
    collect_function_metrics: True
#

#    Collect count metrics, default value is True for backward compatibility but they might be slow,
#    suggested value is False.
    collect_count_metrics: False
#

#    Collect metrics regarding transactions from pg_stat_activity, default value is False. Please make sure the user
#    has sufficient privileges to read from pg_stat_activity before enabling this option.
    collect_activity_metrics: True
#

#    Collect database size metrics. Default value is True but they might be slow with large databases
    collect_database_size_metrics: True
#

#    Include statistics from the default database 'postgres' in the check metrics, default to false
    collect_default_database:
#

## log Section (Available for Agent >=6.0)
logs:

    # - type : (mandatory) type of log input source (tcp / udp / file)
    #   port / path : (mandatory) Set port if type is tcp or udp. Set path if type is file
    #   service : (mandatory) name of the service owning the log
    #   source : (mandatory) attribute that defines which integration is sending the logs
    #   sourcecategory : (optional) Multiple value attribute. Can be used to refine the source attribute
    #   tags: (optional) add tags to each logs collected

  - type: file
    path: /var/log/pg_log/pg.log
    source: postgresql
    sourcecategory: database
    service: worlddb
```
Here we're enabling some configuration options to collect more metrics, as well as hooking up our agent to the location of PostgreSQL's logs, which can be configured in [```/etc/postgresql/10/main/postgresql.conf```](/dataDogVagrant/agent-configuration/postgres-conf.d/postgresql.conf)
```yaml
# This is used when logging to stderr:
logging_collector = on		# Enable capturing of stderr and csvlog
					# into log files. Required to be on for
					# csvlogs.
					# (change requires restart)

# These are only used if logging_collector is on:
log_directory = '/var/log/pg_log'			# directory where log files are written,
					# can be absolute or relative to PGDATA
log_filename = 'pg.log'	# log file name pattern,
					# can include strftime() escapes
log_file_mode = 0644			# creation mode for log files,
					# begin with 0 to use octal notation
#log_truncate_on_rotation = off		# If on, an existing log file with the
```
Let's restart the datadog-agent with ```service datadog-agent restart``` and then check it's pulse with ```datadog-agent status```. If we've done everything right for postgres, we should see something like this:

<img src="/HiringEngineersScreenShots/psqlIntegrationAgentPickup.png" alt="psql agent check" height="200" /><img src="/HiringEngineersScreenShots/psqlIntegrationLogsConfigured.png" alt="psql agent check" height="200" />

Awesome! To confirm this data is getting pushed up from the agent, we'll check our [Host View](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host&host=878227842)

<img src="/HiringEngineersScreenShots/HostDashPsql.png" alt="postgresHostView" height="230" />

### - Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
### - Change your check's collection interval so that it only submits the metric once every 45 seconds.
To create this custom check, we'll refer to [Writing a Custom Agent Check](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6) in the DataDog documentation.

Within our agent configuration directory: ```/etc/datadog-agent/``` we'll find a directory named [checks.d](https://github.com/RusselViola/hiring-engineers/tree/master/dataDogVagrant/agent-configuration/datadog-agent-config/checks.d). This is where we can create python scripts for our custom checks, with a matching yaml configuration file in the [```etc/datadog-agent/conf.d/```](/dataDogVagrant/agent-configuration/datadog-agent-config/conf.d) directory. 

Here's how the files for my custom check look:

[```/etc/datadog-agent/checks.d/custom_my_metric.py```](/dataDogVagrant/agent-configuration/datadog-agent-config/checks.d/custom_my_metric.py)
```python

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


class MyMetricCheck(AgentCheck):
    def check(self, instance):
        self.gauge('custom_metric.my_metric', random.randint(1, 1000))
``` 
Notice I've used Python's [Random](https://docs.python.org/3/library/random.html) module to generate a random value between 1 and 1000 for the metric.

[```etc/datadog-agent/conf.d/custom_my_metric.yaml```](/dataDogVagrant/agent-configuration/datadog-agent-config/conf.d/custom_my_metric.yaml)
```yaml

init_config:

instances:
  - min_collection_interval: 45
```
I've set an interval here to 45s for the custom metric.
Now we can restart the agent and see if our changes worked. Either check by running ```datadog-agent status``` or viewing the [Host Map](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host&host=878227842)

<img src="/HiringEngineersScreenShots/HostDashCustomMetric.png" alt="custom metric on host map" height="230" />

___
### Bonus Question Can you change the collection interval without modifying the Python check file you created?
Luckily for us, we won't be needing to alter our pyton script to make changes to the collection interval, as it lives in the ```custom_my_metric.yaml``` file we've created. We can alter that and restart the agent to have the changes take effect.

#### An Alternative to accessing the file directly is using the [Agent GUI](https://docs.datadoghq.com/agent/?tab=agentv6#gui). If we're not ssh'd into a VM, this is a great option:

<img src="/HiringEngineersScreenShots/agentGUIEditChecks.png" alt="custom metric on host map" height="350" />

Not only can we manage and edit our checks here without having to navigate the cli, we can also check their status:

<img src="/HiringEngineersScreenShots/agentGUIChecksOverview.png" alt="custom metric on host map" height="350" />

As well as the overall agent status, logs, and more:

<img src="/HiringEngineersScreenShots/agentGUIStatusOverview.png" alt="custom metric on host map" height="350" />

___
Visualizing Data:
=================
### Utilize the Datadog API to create a Timeboard that contains:
#### - Your custom metric scoped over your host.
#### - Any metric from the Integration on your Database with the anomaly function applied.
#### - Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
We'll be looking at the [Curl Implementation From DataDog's API Docs](https://docs.datadoghq.com/api/?lang=bash#create-a-dashboard). I've included a [python script](/dataDogVagrant/agent-configuration/generate-dashboard-python/generateDashboard.py) in this repository that I was trying to implement as well, but for the sake of time, Curl was the way to go.

Essentially, we can build a Bash script that will make a call to the API signature ```POST https://api.datadoghq.com/api/v1/dashboard```, house our API Keys, and reference a seperate Json, where we will house the actual construction of our Dashboard. Then all we have to do is run the Bash script [```./vagrant/generate-dashboard-curl/dashboardGenerator.sh```](/dataDogVagrant/agent-configuration/generate-dashboard-curl/dashboardGenerator.sh) or [```./vagrant/generate-dashboard-curl/dashboardGeneratorSingleWidget.sh```](/dataDogVagrant/agent-configuration/generate-dashboard-curl/dashboardGeneratorSingleWidget.sh) and either check our terminal for the appropriate response or check our [Dashboard List](https://app.datadoghq.com/dashboard/lists)

I noticed that we could either put all the metrics into one widget, or define widgets seperately. So I built one of each with their respective Json bodies. (We'll examine the single widget example here. To check out the multiple widget version, refer to [```dashboardGenerator.sh```](/dataDogVagrant/agent-configuration/generate-dashboard-curl/dashboardGenerator.sh) and [```widgets.json```](/dataDogVagrant/agent-configuration/generate-dashboard-curl/widgets.json))

The compostition of [```./vagrant/generate-dashboard-curl/dashboardGeneratorSingleWidget.sh```](/dataDogVagrant/agent-configuration/generate-dashboard-curl/dashboardGeneratorSingleWidget.sh):

```shell
# !/bin/bash

api_key=ad00c177c779cc3d503ee10c55c302dd
app_key=dfd765459564830537d9cb5f0cce7ccd7b402cff

curl  -X POST -H "Content-type: application/json" \
-d @./singleWidget.json \
"https://api.datadoghq.com/api/v1/dashboard?api_key=${api_key}&application_key=${app_key}"
```

And [```singleWidget.json```](https://github.com/RusselViola/hiring-engineers/blob/master/dataDogVagrant/agent-configuration/generate-dashboard-curl/singleWidget.json) that we're referencing in our script:

```json
{
  "title" : "Custom Dashboard, Single Widget",
  "widgets" : [
    {"definition": {
    "type": "timeseries",
    "requests": [
        {"q": "avg:custom_metric.my_metric{host:ubuntu}"},
        {"q": "anomalies(avg:postgresql.rows_returned{host:ubuntu}, 'basic', 2)"},
        {"q": "avg:custom_metric.my_metric{host:ubuntu}.rollup(sum, 3600)"}
    ],
    "title": "custom_metric.my_metric over ubuntu"
    }}
  ],
  "layout_type": "ordered",
  "description" : "Custom Dashboard for DataDog SE Exercise Showing custom_metric, all requests in one.",
  "is_read_only": true,
  "notify_list": ["russelviola@gmail.com"],
  "template_variables": [{
      "name": "ubuntu",
      "prefix": "ubuntu",
      "default": "ubuntu"
  }]
}
```
We can think of each widget as it's own graph that will show up on our dashboard. We can add multiple metrics to each graph, and have multiple graphs defined in a single API call. We can create, update, delete, and even get dashboards via the REST API. 

Imagine a continuous integration scenario where we might want to change our dashboards dynamically with changes to our application. We could parameterize our API calls and have then kick off updates from a CI tool based on what's happening in our pipeline. This opens up huge possibilities in terms of automation!


### Once this is created, access the Dashboard from your Dashboard List in the UI:
We can see the dashboard in action [here](https://app.datadoghq.com/dashboard/k8t-5pz-umh/custom-dashboard-single-widget?tile_size=m&page=0&is_auto=false&from_ts=1553103414201&to_ts=1553126657406&live=false&fullscreen_widget=6742393085938141) and explore the different monitors we've applied with our API call:

<img src="/HiringEngineersScreenShots/CustomDashSingleWidget.png" alt="singlewidget" height="500" />

### - Set the Timeboard's timeframe to the past 5 minutes
We can click and drag on the timeline of our graph to look at the last 5 minutes,

<img src="https://github.com/RusselViola/hiring-engineers/blob/master/HiringEngineersScreenShots/last5MinutesWithNotation.png" height="300" />

### - Take a snapshot of this graph and use the @ notation to send it to yourself.
Then take a snapshot using the camera icon and leave a notation to our colleagues.

<img src="/HiringEngineersScreenShots/notationSnapshotEmailAlert.png" height="500" />

___
### Bonus Question: What is the Anomaly graph displaying?
The [Anomoly Detection](https://docs.datadoghq.com/monitors/monitor_types/anomaly/#pagetitle) feature is a handy algorythm that observes the trends of a given metric, and adjusts the threshold for unusual behavior based on that. It's a way to keep the expected range of behavior from our systems _dynamic_ as opposed to having to manually adjust our expectations as our application scales.

With the example of my ```postgresql.rows_returned``` metric, as entries to the database continue to expand with the use of my application, so will the amount of information it delivers to users. Maybe this is an ever expanding library or list of products on an eccommerce application. I don't want to have to re-gauge expectations for my monitors for something that can be predicted behavior as we scale. With an anomaly monitor on, we'll see when deviations to this norm happen dynamically, based on trends, rather than static values.

___
Monitoring Data:
==================
### Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.
In this case, I performed all my actions via the Datadog Application following [the Datadog Alerting Documentation](https://docs.datadoghq.com/monitors/). These can be configured via the [Datadog API](https://docs.datadoghq.com/api/?lang=python#create-a-monitor) much like we did earlier with our dashboard.

### Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

### - Warning threshold of 500
### - Alerting threshold of 800
### - And also ensure that it will notify you if there is No Data for this query over the past 10m.

<img src="/HiringEngineersScreenShots/monitorEditor.png" height="500" />

### Please configure the monitor’s message so that it will:

### - Send you an email whenever the monitor triggers.
### - Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
### - Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

There's information in the editor on using this markdown under ```Use message template variables```, but to see the full extent of what we can parameterize, look to the [Notifications Documentation](https://docs.datadoghq.com/monitors/notifications/?tab=is_alertis_warning#message-template-variables)

<img src="/HiringEngineersScreenShots/monitorEditor2.png" height="500" />

So I thought I was being quite clever here in parameterizing the ```Alert Title Field```. It turns out that you can, and it works, but as we'll see later, it looks pretty bad when we're sending Downtime Notifications.

### - When this monitor sends you an email notification, take a screenshot of the email that it sends you.

Here's an example of a warning notification we get from the monitor:

<img src="/HiringEngineersScreenShots/monitorWarningWithNumbers.png" height="500" />

___
### Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
### - One that silences it from 7pm to 9am daily on M-F,
### - And one that silences it all day on Sat-Sun.
### - Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
We can hop on over to the [Manage Downtime](https://app.datadoghq.com/monitors#downtime) section of our Monitor Tab to set custom instances where we won't be alerted by these monitors. We can follow along with the [Downtime Documentation](https://docs.datadoghq.com/monitors/downtimes/) to put these together.

I've configured one for our weekday evenings: 

<img src="/HiringEngineersScreenShots/weekdayDowntime.png" height="500" />

You'll notice how hideous my attempts at creating a parameterized monitor title came out here. Since this downtime is referring to the whole monitor, rather than a particular piece of it, we're getting the full title text.

I've also added one for our weekends, starting Friday evening, and ending Monday morning:

<img src="/HiringEngineersScreenShots/weekendDowntime.png" height="500" />

Here's what we get when the downtime starts:

<img src="/HiringEngineersScreenShots/monitorDowntimeNotification.png" height="500" />

At this point, I've changed this downtime to work for all monitors. Definitely not because it looked better than my dynamic monitor title. ;) 

#### In reality, I imagine, there are going to be certain alerts which _must_ be up at all times. For anything mission critical, it doesn't matter if it's 3 in the morning on Saturday, I want that alert.

___
Collecting APM Data:
===================

### Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:
Note: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

For this excercise I've taken the given flask app and made some alterations, as well as prepared a Bash script to populate data for the APM, since I wanted more data on our dashboard side and didn't feel like hitting 4 endpoints over and over manually. _Additionally_, we'll be using [ddtrace](https://docs.datadoghq.com/tracing/languages/python/) rather than injecting trace middleware into the application itself.

The application lives in [```/vagrant/flaskApp/datadogAPM.py```](/dataDogVagrant/agent-configuration/flaskApp/datadogAPM.py)

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

@app.route('/api/world')
def db_endpoint():
    # Set psql credentials
    hostname = 'localhost'
    username = 'datadog'
    password = 'datadog'
    database = 'worlddb'

    # function to query the database and display 100 entries
    def doQuery( conn ):
        cur = conn.cursor()
        cur.execute( "SELECT * FROM city limit 50")
        cities = cur.fetchall()
        # for city in cities :
        return "{}".format(cities)
    import psycopg2
    #connect to db with credentials
    myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    #perform query function
    return doQuery( myConnection )
    #close connection
    myConnection.close()

if __name__ == '__main__':
	app.run(host='0.0.0.0', port='5050')
```

I've added an additional endpoint that will query our ```worlddb``` database that we set up in the beginning of the exercise. All it does is grab a bunch of rows from the 'cities' table in the databse and returns them. Enough so that we could get a trace on some PostgreSQL information from our application as well. This was implemented using the [psycopg2 - Python-PostgreSQL Database Adapter](https://github.com/psycopg/psycopg2).

#### To configure our agent for the APM we look to [APM Setup](https://docs.datadoghq.com/agent/apm/?tab=agent630) in the Datadog Documentation.

- First we'll need to install ```ddtrace``` as per the [Tracing Python Applications](https://docs.datadoghq.com/tracing/languages/python/) Documentation.

	```pip install ddtrace```

	We'll come back to this in a moment.

- Then we'll need to configure our agent to go back to our [```datadog.yaml```](https://github.com/RusselViola/hiring-engineers/blob/master/dataDogVagrant/agent-configuration/datadog-agent-config/datadog.yaml) and enable ```apm_config``` all the way at the bottom of the file.

```yaml
apm_config:
#   Whether or not the APM Agent should run
 enabled: true
#   The environment tag that Traces should be tagged with
#   Will inherit from "env" tag if "none" is applied here
 env: none
#   The port that the Receiver should listen on
 receiver_port: 8126
#   Whether the Trace Agent should listen for non local traffic
#   Only enable if Traces are being sent to this Agent from another host/container
 apm_non_local_traffic: false
#   Extra global sample rate to apply on all the traces
#   This sample rate is combined to the sample rate from the sampler logic, still promoting interesting traces
#   From 1 (no extra rate) to 0 (don't sample at all)
 extra_sample_rate: 1.0
#   Maximum number of traces per second to sample.
#   The limit is applied over an average over a few minutes ; much bigger spikes are possible.
#   Set to 0 to disable the limit.
 max_traces_per_second: 0
#   A blacklist of regular expressions can be provided to disable certain traces based on their resource name
#   all entries must be surrounded by double quotes and separated by commas
#   Example: ["(GET|POST) /healthcheck", "GET /V1"]
 ignore_resources: []
```

Here we will change ```enabled:``` to ```true```. I've also set ```max_traces-per_second:``` to ```0``` to accomodate my Bash script later on. Everything else is the default value.

From the [```/vagrant/flaskApp/```](/dataDogVagrant/agent-configuration/flaskApp) directory we can run ```./apm_generator.sh``` to boot up the application, then use curl to loop over the endpoints in our application a few times. After that it will shut down the application and close the port ```localhost:5050```.

Here's what the [Bash Script](/dataDogVagrant/agent-configuration/flaskApp/apm_generator.sh) looks like:

```shell
#!/bin/bash
echo "start"
ddtrace-run python datadogAPM.py &
sleep 5

echo "Starting datadogAPM.py"
COUNT=1
for x in $(seq 1 20)
do
  echo "Iteration $x"
  echo "homepage"
  curl "http://localhost:5050"
  echo "apm page"
  curl "http://localhost:5050/api/apm"
  echo "trace page"
  curl "http://localhost:5050/api/trace"
  echo "world page"
  curl "http://localhost:5050/api/world"
  sleep 2
done
kill $(pgrep -f 'datadogAPM.py')
sudo kill $(sudo lsof -t -i:5050)
echo "Shutting Down datadogAPM.py"
echo "finished"
```
Now that we've run the application with ```ddtrace``` and hit enough endpoints for our agent to register, we can look at our [Trace Search & Analytics](https://app.datadoghq.com/apm/search?cols=%5B%22core_service%22%2C%22log_duration%22%2C%22log_http.method%22%2C%22log_http.status_code%22%5D&from_ts=1553190193487&index=trace-search&live=true&query=env%3Adev&stream_sort=desc&to_ts=1553362993487) tab to view what our agent is picking up:

<img src="/HiringEngineersScreenShots/traceSearchAndAnalytics.png" alt="traceSearchAnalytics" height="500" />

Now that we're seeing some data, we can enable [Trace Search](https://docs.datadoghq.com/agent/apm/?tab=agent630#trace-search) in our [```datadog.yaml```](/dataDogVagrant/agent-configuration/datadog-agent-config/datadog.yaml):

```yaml
apm_config:
#   Whether or not the APM Agent should run
 enabled: true
#   The environment tag that Traces should be tagged with
#   Will inherit from "env" tag if "none" is applied here
 env: none
#   The port that the Receiver should listen on
 receiver_port: 8126
#   Whether the Trace Agent should listen for non local traffic
#   Only enable if Traces are being sent to this Agent from another host/container
 apm_non_local_traffic: false
#   Extra global sample rate to apply on all the traces
#   This sample rate is combined to the sample rate from the sampler logic, still promoting interesting traces
#   From 1 (no extra rate) to 0 (don't sample at all)
 extra_sample_rate: 1.0
#   Maximum number of traces per second to sample.
#   The limit is applied over an average over a few minutes ; much bigger spikes are possible.
#   Set to 0 to disable the limit.
 max_traces_per_second: 0
#   A blacklist of regular expressions can be provided to disable certain traces based on their resource name
#   all entries must be surrounded by double quotes and separated by commas
#   Example: ["(GET|POST) /healthcheck", "GET /V1"]
 ignore_resources: []
 analyzed_spans:
   flask|flask.request: 1
   postgres|postgres.query: 1

```

Down at the bottom we've given a name to the services performing the operations that our agent picked up earlier.

Now we can run ```./apm_generator.sh``` to our hearts content and generate some data for our apm.

___
### Bonus Question: What is the difference between a Service and a Resource?

There's a simple and succint explanation in the [Tracing Terminology](https://docs.datadoghq.com/tracing/guide/terminology/) section of the documentation.

A Service is a set of processes that do the same job. A web application can consist of multiple services. So in our case we've got Flask, our web framework, or PostgreSQL, our database. Web framework and database are both examples of what would be defined as a service in Datadog. The neat thing about services in Datadog is that they get their own [out of the box graphs](https://docs.datadoghq.com/tracing/visualization/service/#out-of-the-box-graphs) for things like total amount of requests, error rate, and more.

A Resource is a particular action for a Service. When we look at our [Trace Search & Analytics](https://app.datadoghq.com/apm/search?cols=%5B%22core_service%22%2C%22log_duration%22%2C%22log_http.method%22%2C%22log_http.status_code%22%5D&from_ts=1553190193487&index=trace-search&live=true&query=env%3Adev&stream_sort=desc&to_ts=1553362993487), we can see all of our resources listed out like ```GET /api/world```. This is an example of a resource belonging to the Flask web framework _Service_.

___
### Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Here's a [Dashboard](https://app.datadoghq.com/dashboard/68e-zcq-w5q/infrastructure-and-apm-dash?tile_size=m&page=0&is_auto=false&from_ts=1553362200000&to_ts=1553365800000&live=true) where we're looking at our infastructure metrics an our APM metrics. Now we can really visualize the value of getting all of this information in one place where it's easy to consume. We can start to look for correlations in our data, set alerts, look for anomalies, and so much more in our ever changing dynamic infastructures.

<img src="/HiringEngineersScreenShots/traceAndInfrastructureDash.png" alt="trace and infastructure dash" height="400" />

___
Final Question:
===============
### Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

### Is there anything creative you would use Datadog for?

After gaining a better understanding of the Datadog platform, I can say, it could be used for a whole lot! One thing I thought of immediately was implementing this to monitor IOT infastructures. Imagine hooking it up to every facet of your 'smart' home and setting alerts when the temperature goes down too far, or your energy consumption is going above average. Are these devices communicating with eachother properly? We could look at all their connections and turn something abstract , like communications from device to device, into data that's much more tangible and consumable to a human running the show.


This relates directly to a personal project I've conceptualized with a friend as well. The concept is a smart guitar humidifying case that essentially reads the environment of the case from an arduino board with peripherals (things like humidity, temperature, light, etc.), that relays that information via API to a web server, which would then communicate with individuals' mobile applications to alert them of changes in those variables, and either automatically, or through manual input from the mobile application, make adjustments to them via mechanisms built into the board in the case itself. 

Now, imagine having to make sure all of the data coming from all of those boxes was coming back correctly, and not malfunctioning. We could use Datadog to get a better view of all of the moving parts in our infrastructure. 

___
