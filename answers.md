<img src="" alt="U" height="500" />


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


You don't necessarily need to run this to understand my approach to this exercise, as I've documented that below, but I wanted to include access to the environment 1. because that's what vagrant is for, and 2. in the case that you'd like to explore my environment with all of the following requirements implemented.

___
Collecting Metrics:
===================
To install the agent, We can follow the steps for [Ubuntu Datadog Agent Integration](https://app.datadoghq.com/account/settings#agent/ubuntu) and run ```DD_API_KEY=<YOUR_API_KEY> -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"```, which starts up the agent after installation. Then we can look to our [Datadog Host Map](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host) and see it's installed, we'll see something like this: 

<img src="https://github.com/RusselViola/hiring-engineers/blob/master/HiringEngineersScreenShots/UbuntuHostShot.png" alt="Ubuntu Host Map Icon" height="500" />

### - Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

Since we're using a Linux system, our Agent config file lives at [```etc/datadog-agent/datadog.yaml```](https://github.com/RusselViola/hiring-engineers/blob/master/dataDogVagrant/agent-configuration/datadog-agent-config/datadog.yaml). We can open this with our favorite IDE and take a look inside.
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

<img src="https://github.com/RusselViola/hiring-engineers/blob/master/HiringEngineersScreenShots/HostDashTags.png" alt="Host Tag View" height="230" />

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
The second command here, is granting 'datadog' access to all of those sweet, sweet metrics that PostgreSQL collects for itself as it runs. Now, the next part isn't totally necessary, but I thought it would be nice to see an actual database connected to the agent. I brought in [WorldDB](https://github.com/RusselViola/hiring-engineers/tree/master/dataDogVagrant/world-1.0/dbsamples-0.1/world) a simple SQL database for development purposes:

while in the postgres console:
```
CREATE DATABASE worlddb;
```
from [WorldDB directory](https://github.com/RusselViola/hiring-engineers/tree/master/dataDogVagrant/world-1.0/dbsamples-0.1/world):
```
sudo psql -U postgres -d worlddb -f world.sql
```
and just like we did with ```pg_monitor``` in our postgres console, ```grant worlddb to datadog;```

#### The second piece to the integration is configuring the agent itself. We're going to be making changes to [etc/datadog-agent/conf.d/postgres.d/conf.yaml](https://github.com/RusselViola/hiring-engineers/blob/master/dataDogVagrant/agent-configuration/datadog-agent-config/conf.d/postgres.d/conf.yaml):
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
Here we're enabling some configuration options to collect more metrics, as well as hooking up our agent to the location of PostgreSQL's logs, which can be configured in [/etc/postgresql/10/main/postgresql.conf](https://github.com/RusselViola/hiring-engineers/blob/master/dataDogVagrant/agent-configuration/postgres-conf.d/postgresql.conf)
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

<img src="https://github.com/RusselViola/hiring-engineers/blob/master/HiringEngineersScreenShots/psqlIntegrationAgentPickup.png" alt="psql agent check" height="200" /><img src="https://github.com/RusselViola/hiring-engineers/blob/master/HiringEngineersScreenShots/psqlIntegrationLogsConfigured.png" alt="psql agent check" height="200" />

Awesome! To confirm this data is getting pushed up from the agent, we'll check our [Host View](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host&host=878227842)

<img src="https://github.com/RusselViola/hiring-engineers/blob/master/HiringEngineersScreenShots/HostDashPsql.png" alt="postgresHostView" height="230" />

### - Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
### - Change your check's collection interval so that it only submits the metric once every 45 seconds.
To create this custom check, we'll refer to [Writing a Custom Agent Check](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6) in the DataDog documentation.

Within our agent configuration directory: ```/etc/datadog-agent/``` we'll find a directory named [checks.d](https://github.com/RusselViola/hiring-engineers/tree/master/dataDogVagrant/agent-configuration/datadog-agent-config/checks.d). This is where we can create python scripts for our custom checks, with a matching yaml configuration file in the [etc/datadog-agent/conf.d/](https://github.com/RusselViola/hiring-engineers/tree/master/dataDogVagrant/agent-configuration/datadog-agent-config/conf.d) directory. 

Here's how the files for my custom check look:

[/etc/datadog-agent/checks.d/custom_my_metric.py](https://github.com/RusselViola/hiring-engineers/blob/master/dataDogVagrant/agent-configuration/datadog-agent-config/checks.d/custom_my_metric.py)
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

[etc/datadog-agent/conf.d/custom_my_metric.yaml](https://github.com/RusselViola/hiring-engineers/blob/master/dataDogVagrant/agent-configuration/datadog-agent-config/conf.d/custom_my_metric.yaml)
```yaml

init_config:

instances:
  - min_collection_interval: 45
```
I've set an interval here to 45s for the custom metric.
Now we can restart the agent and see if our changes worked. Either check by running ```datadog-agent status``` or viewing the [Host Map](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host&host=878227842)

<img src="https://github.com/RusselViola/hiring-engineers/blob/master/HiringEngineersScreenShots/HostDashCustomMetric.png" alt="custom metric on host map" height="230" />

___
### Bonus Question Can you change the collection interval without modifying the Python check file you created?
Luckily for us, we won't be needing to alter our pyton script to make changes to the collection interval, as it lives in the ```custom_my_metric.yaml``` file we've created. We can alter that and restart the agent to have the changes take effect.

#### An Alternative to accessing the file directly is using the [Agent GUI](https://docs.datadoghq.com/agent/?tab=agentv6#gui). If we're not ssh'd into a VM, this is a great option:

<img src="https://github.com/RusselViola/hiring-engineers/blob/master/HiringEngineersScreenShots/agentGUIEditChecks.png" alt="custom metric on host map" height="350" />

Not only can we manage and edit our checks here without having to navigate the cli, we can also check their status:

<img src="https://github.com/RusselViola/hiring-engineers/blob/master/HiringEngineersScreenShots/agentGUIChecksOverview.png" alt="custom metric on host map" height="350" />

As well as the overall agent status, logs, and more:

<img src="https://github.com/RusselViola/hiring-engineers/blob/master/HiringEngineersScreenShots/agentGUIStatusOverview.png" alt="custom metric on host map" height="350" />

___
Visualizing Data:
=================
### Utilize the Datadog API to create a Timeboard that contains:
#### - Your custom metric scoped over your host.
#### - Any metric from the Integration on your Database with the anomaly function applied.
#### - Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
We'll be looking at the [Curl Implementation From DataDog's API Docs](https://docs.datadoghq.com/api/?lang=bash#create-a-dashboard). I've included a [python script](https://github.com/RusselViola/hiring-engineers/blob/master/dataDogVagrant/agent-configuration/generate-dashboard-python/generateDashboard.py) in this repository that I was trying to implement as well, but for the sake of time, Curl was the way to go.

Essentially, we can build a Bash script that will make a call to the API signature ```POST https://api.datadoghq.com/api/v1/dashboard```, house our API Keys, and reference a seperate Json, where we will house the actual construction of our Dashboard. Then all we have to do is run the Bash script [```./vagrant/generate-dashboard-curl/dashboardGenerator.sh```](https://github.com/RusselViola/hiring-engineers/blob/master/dataDogVagrant/agent-configuration/generate-dashboard-curl/dashboardGenerator.sh) or [```./vagrant/generate-dashboard-curl/dashboardGeneratorSingleWidget.sh```](https://github.com/RusselViola/hiring-engineers/blob/master/dataDogVagrant/agent-configuration/generate-dashboard-curl/dashboardGeneratorSingleWidget.sh) and either check our terminal for the appropriate response or check our [Dashboard List](https://app.datadoghq.com/dashboard/lists)

I noticed that we could either put all the metrics into one widget, or define widgets seperately. So I built one of each with their respective Json bodies. (We'll examine the single widget example here. To check out the multiple widget version, refer to [dashboardGenerator.sh](https://github.com/RusselViola/hiring-engineers/blob/master/dataDogVagrant/agent-configuration/generate-dashboard-curl/dashboardGenerator.sh) and [widgets.json](https://github.com/RusselViola/hiring-engineers/blob/master/dataDogVagrant/agent-configuration/generate-dashboard-curl/widgets.json))

The compostition of [```./vagrant/generate-dashboard-curl/dashboardGeneratorSingleWidget.sh```](https://github.com/RusselViola/hiring-engineers/blob/master/dataDogVagrant/agent-configuration/generate-dashboard-curl/dashboardGeneratorSingleWidget.sh):

```shell
# !/bin/bash

api_key=ad00c177c779cc3d503ee10c55c302dd
app_key=dfd765459564830537d9cb5f0cce7ccd7b402cff

curl  -X POST -H "Content-type: application/json" \
-d @./singleWidget.json \
"https://api.datadoghq.com/api/v1/dashboard?api_key=${api_key}&application_key=${app_key}"
```

And [singleWidget.json](https://github.com/RusselViola/hiring-engineers/blob/master/dataDogVagrant/agent-configuration/generate-dashboard-curl/singleWidget.json) that we're referencing in our script:

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

<img src="https://github.com/RusselViola/hiring-engineers/blob/master/HiringEngineersScreenShots/CustomDashSingleWidget.png" alt="singlewidget" height="500" />

### - Set the Timeboard's timeframe to the past 5 minutes
We can click and drag on the timeline of our graph to look at the last 5 minutes,

<img src="https://github.com/RusselViola/hiring-engineers/blob/master/HiringEngineersScreenShots/last5MinutesWithNotation.png" height="300" />

### - Take a snapshot of this graph and use the @ notation to send it to yourself.
Then take a snapshot using the camera icon and leave a notation to our colleagues.

<img src="https://github.com/RusselViola/hiring-engineers/blob/master/HiringEngineersScreenShots/notationSnapshotEmailAlert.png" height="500" />

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

<img src="https://github.com/RusselViola/hiring-engineers/blob/master/HiringEngineersScreenShots/monitorEditor.png" height="500" />

### Please configure the monitor’s message so that it will:

### - Send you an email whenever the monitor triggers.
### - Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
### - Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

There's information in the editor on using this markdown under ```Use message template variables```, but to see the full extent of what we can parameterize, look to the [Notifications Documentation](https://docs.datadoghq.com/monitors/notifications/?tab=is_alertis_warning#message-template-variables)

<img src="https://github.com/RusselViola/hiring-engineers/blob/master/HiringEngineersScreenShots/monitorEditor2.png" height="500" />

So I thought I was being quite clever here in parameterizing the ```Alert Title Field```. It turns out that you can, and it works, but as we'll see later, it looks pretty bad when we're sending Downtime Notifications.

### - When this monitor sends you an email notification, take a screenshot of the email that it sends you.

Here's an example of a warning notification we get from the monitor:

<img src="https://github.com/RusselViola/hiring-engineers/blob/master/HiringEngineersScreenShots/monitorWarningWithNumbers.png" height="500" />

___
### Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
### - One that silences it from 7pm to 9am daily on M-F,
### - And one that silences it all day on Sat-Sun.
### - Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
We can hop on over to the [Manage Downtime](https://app.datadoghq.com/monitors#downtime) section of our Monitor Tab to set custom instances where we won't be alerted by these monitors. We can follow along with the [Downtime Documentation](https://docs.datadoghq.com/monitors/downtimes/) to put these together.

I've configured one for our weekday evenings: 

<img src="https://github.com/RusselViola/hiring-engineers/blob/master/HiringEngineersScreenShots/weekdayDowntime.png" height="500" />

You'll notice how hideous my attempts at creating a parameterized monitor title came out here. Since this downtime is referring to the whole monitor, rather than a particular piece of it, we're getting the full title text.

I've also added one for our weekends, starting Friday evening, and ending Monday morning:

<img src="https://github.com/RusselViola/hiring-engineers/blob/master/HiringEngineersScreenShots/weekendDowntime.png" height="500" />

Here's what we get when the downtime starts:

<img src="https://github.com/RusselViola/hiring-engineers/blob/master/HiringEngineersScreenShots/monitorDowntimeNotification.png" height="500" />

At this point, I've changed this downtime to work for all monitors. Definitely not because it looked better than my dynamic monitor title. 

#### In reality, I imagine, there are going to be certain alerts which _must_ be up at all times. For anything mission critical, it doesn't matter if it's 3 in the morning on Saturday, I want that alert.

___
Collecting APM Data:
===================

### Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:
Note: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

___
### Bonus Question: What is the difference between a Service and a Resource?
___
### Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
### Please include your fully instrumented app in your submission, as well.-

___
Final Question:
===============
### Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

### Is there anything creative you would use Datadog for?

___
