## Prerequisites - Setup the environment

On my first attempt, I chose to use Vagrant to configure an Ubuntu 12.04 LTS VM.  While the initial set up was straightforward I ran into issues when attempting to use the Datadog API.  This was before I began tracking issues, therefore I don't have detailed logs.  

Essentially, I had problems when attempting to download the datadogpy library via pip.  The error was that pip could not find any library named datadog, even though I verifed the package at pypi.org.

I wanted to use an an official Datadog library, however after being unable to proceed, I decided to try the third party node-dogapi library.  Unfortunately I was running into issues again, this time with installing node and npm.

Ultimately I suspected the problem might be due to the older version of Ubuntu and decided to try a more recent version.

[I chose Ubuntu 16.04 LTS as my host running on VM Virtual Box](https://p.datadoghq.com/sb/7af5f9814-243e179005f19f7df668a6d7dad75b3c)

I already had Virtual Box with Ubuntu instlled my local machine.  There are many [tutorials online](https://linus.nci.nih.gov/bdge/installUbuntu.html) on how to get this up and running.

![alt text](https://github.com/mjmanney/hiring-engineers/blob/solutions-engineer/images/vbox.PNG "Virtual Box")

Next, I installed CURL by opening a terminal and entering the command:

```sh
sudo apt-get install curl
```
which allowed me to install the Datadog agent with:

```sh
DD_API_KEY=<MY_API_KEY> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

## Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

At the datadog agent root directory edit the config file datadog.yaml.  Note that the Datadog docs recommend to use the yaml list syntax as below:

``` yaml
# Set the host's tags (optional)
tags: mytag:newhost, env:prod, role:database
```

My custom newhost tag appears in the Hostmap, alongside the automatically generated tags.

![alt text](https://raw.githubusercontent.com/mjmanney/hiring-engineers/solutions-engineer/images/hostmap.PNG "Host Map with custom tags")

## Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I chose to integrate MongoDB with my Datadog agent.  [Instructions can be found on mongodb's documentation.](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)

![alt text](https://raw.githubusercontent.com/mjmanney/hiring-engineers/solutions-engineer/images/mongo.png "MongoDB")

After mongodb was installed on the machine I began the integration with datadog.

In terminal run the command `mongo` to access the mongo shell.

Once inside the mongo shell create a read-only user adminstrator for data dog:
```sh
# MongoDB 3.x

# use the admin db
use admin

db.createUser({
  "user":"datadog",
  "pwd": "<CREATE-MY-PASSWORD>",
  "roles" : [
    {role: 'read', db: 'admin' },
    {role: 'clusterMonitor', db: 'admin'},
    {role: 'read', db: 'local' }
  ]
})
```

Verifying the datadog user I just created created with: 

```sh
echo "db.auth('datadog', '<PASSWORD>')" | mongo admin | grep -E "(Authentication failed)|(auth fails)" &&
echo -e "\033[0;31mdatadog user - Missing\033[0m" || echo -e "\033[0;32mdatadog user - OK\033[0m"
```

If the datadog user passes authentication to the mongodb instance, the terminal will echo `datadog user - OK`

Lastly, I configured Datadog Agent to connect to connect to the mongodb instance. 

Edit the config file at datadog-agent/conf.d/mongo.d/mongo.yaml (Agent v6).
I also added some custom tags.

``` yaml
init_config:

  instances:
    - server: mongodb://datadog:<PASSWORD>@localhost:27017/admin
      additional_metrics:
        - collection       # collect metrics for each collection
        - metrics.commands
        - tcmalloc
        - top
      tags:
        - myMongoDB
        - metricsDB
```

Restart the datadog agent with:

```sh
sudo service datadog-agent restart
```

and get the status of the integration with (Agent v6):

```sh
sudo datadog-agent status
```

![alt text](https://raw.githubusercontent.com/mjmanney/hiring-engineers/Michael-Manney_Solutions-Engineer/images/dd_status_mongo-metric.png "Mongo integration status")


## Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Custom checks should be placed in the checks.d directory at the datadog-agent root.

datadog-agent/checks.d/my_metric.py

``` python
#import dd AgentCheck
from checks import AgentCheck

#import randint
from random import randint

class myCheck(AgentCheck):
    def check(self, instance):
        x = randint(0, 1000)
        self.gauge('my_metric', x)
```

## Change your check's collection interval so that it only submits the metric once every 45 seconds.

## Bonus Question Can you change the collection interval without modifying the Python check file you created?
This can be done by altering
datadog-agent/conf.d/my_metric.yaml
``` yaml
init_config:

instances:
    -    host: localhost
         min_collection_interval: 45
         name: my_metric
```

## Visualizing Data

Timeboard does not support anamoly detection.  Therefore I created a timeboard for my custom metric and a monitor for the database anamoly, which I added to my [screenboard](https://p.datadoghq.com/sb/7af5f9814-243e179005f19f7df668a6d7dad75b3c).

I used Datadog's official Python api library, [datadogpy](https://github.com/DataDog/datadogpy).

To install:

```sh
pip install datadog
```

Accessing Datadog's API requires both an api and app key.  Generate an app key and view the existing api key at <https://app.datadoghq.com/account/settings#api>.

For the skeleton of the code I refered to Datadog's [Timeboard API](https://docs.datadoghq.com/api/?lang=python#timeboards) docs.

It took a few back and forth readings between the API docs, Graphing, and Monitor guides before I figured out the query syntax.  In some cases where I was stuck, I found it helpful to create the object via the UI and then examine the JSON structure for comparison.

The code below makes two graphs utilizing the datadogpy package.  The first is a timeseries of `my_metric` tagged by my host.  The second is a query value which uses the rollup function to add together the values of `my_metric` from the last hour.


This code can be found in tboard.py at the root directory of my repository.

```python
from datadog import initialize, api

options = {
    'api_key': '<MY_API_KEY>',
    'app_key': '<MY_APP_KEY>'
}

initialize(**options)

title = "Michael's Timeboard"
description = "Final Timeboard"
graphs = [
{    # Graph of my_metric
    "definition": {
        "events": [],
        "requests": [
            {"q": "my_metric{host:ubuntuyhivi}"},
        ],
        "viz": "timeseries"
    },
    "title": "my_metric"
}, 
{   # Query value of sum of my_metric past 1 hr
    "definition": {
        "events": [],
        "requests": [
            {
                "q": "sum:my_metric{*}.rollup(sum, 3600)",
                "type": None,
                "style": {
                  "palette": "dog_classic",
                  "type": "solid",
                  "width": "normal"
                },
                "conditional_formats": [],
                "aggregator": "sum"
            }
        ],
        "viz": "query_value",
        "autoscale": True
    },
    "title": "Rollup - Sum of my_metric past hr"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     read_only=read_only)

```

Next, to utilize the anamoly monitor I used the API to create a new monitor by reffering to the [create a monitor](https://docs.datadoghq.com/api/?lang=python#create-a-monitor) API and [anamoly monitor](https://docs.datadoghq.com/monitors/monitor_types/anomaly/) documentation.

Creating a monitor is similar to creating a timeboard.

I used the amount of free bytes in the MongoDB thread cache as my metric to monitor.

This code can be found in anomalyMonitor.py at the root directory of my repository.

```python
from datadog import initialize, api

options = {
    'api_key': '<MY_API_KEY>',
    'app_key': '<MY_APP_KEY>'
}

initialize(**options)

# Create a new monitor
options = {
    "notify_no_data": True,
    "no_data_timeframe": 20
}
tags = ["db:mongodb", "myTag:anomaly"]
api.Monitor.create(
    type="metric alert",
    query="avg(last_4h):anomalies(avg:mongodb.tcmalloc.tcmalloc.thread_cache_free_bytes{*}, 'agile', 2, direction='both', alert_window='last_15m', interval=60, count_default_zero='true') >= 1",
    name="Mongo Thread Cache Free Bytes",
    message="Anomaly detected!!!!!",
    tags=tags,
    options=options
)

```

Here is a snapshot of me talking to myself about the metric I created.

![alt text](https://raw.githubusercontent.com/mjmanney/hiring-engineers/Michael-Manney_Solutions-Engineer/images/my_metric_snap.png "my_metric 5min")

Here is a snapshot of the anomaly monitor in my monitor dashboard, and the anamoly graph can be visited on my [public screen board here.](https://p.datadoghq.com/sb/7af5f9814-243e179005f19f7df668a6d7dad75b3c)

![alt text](https://raw.githubusercontent.com/mjmanney/hiring-engineers/Michael-Manney_Solutions-Engineer/images/anomaly_monitor.png "anomaly dash")

### What is the Anomaly graph displaying?
The anomaly graph is the gray area overlaying over the current graph.  This represents the range of "normal" values based the algorithims interpretation of past data and future expectations.  If the graph goes above or below this threshold an alert is created.

## Monitoring Data

To create a new monitor navigate to <https://app.datadoghq.com/monitors/manage> and then click on New Monitor on the top right.

Select the type of monitor to metric since we are monitoring `my_metric`.

Step 1 - set the detection method as `Threshold Alert`.
Step 2 - select `my_metric` as the metric to monitor.  Make sure to select a host or else the host variable markup won't work in step 4.

![alt text](https://raw.githubusercontent.com/mjmanney/hiring-engineers/Michael-Manney_Solutions-Engineer/images/alert_step12.png "Step 1 & 2")

Step 3 - Set the alert to trigger the metric if it is `above` the threshhold `on average` during the last `5 minutes`.  The Alert threshold is set to 800 and the Warning threshold at 500.  Lastly, be sure to send a notification of data is missing for more than 5 minutes.

![alt text](https://raw.githubusercontent.com/mjmanney/hiring-engineers/Michael-Manney_Solutions-Engineer/images/alert_step3.png "Step 3")

Step 4 - configure the alert message based on whether the monitor is an Alert, Warning or is not sending any data using the message template variable syntax.  The following markdown reports whether `my_metric` is nearing or exceed the threshold or if it is not reporting any data.  It also included the host information as well as the value reported and sends a notification to my email.

```
{{#is_alert}}
  ALERT! My_metric avg has exceeded {{threshold}}.  Avg past 5 min is {{value}}.
  HOST: {{host.name}} with IP {{host.ip}}.
{{/is_alert}}

{{#is_warning}}
  WARNING! My_metric avg is nearing {{threshold}}.  Avg past 5 min is {{value}}.
  HOST: {{host.name}} with IP {{host.ip}}.
{{/is_warning}}

{{#is_no_data}}
  ALERT! My_metric has not recieved any data in the past 5 min.
  HOST: {{host.name}} with IP {{host.ip}}.
{{/is_no_data}}

@michaelmanney@yahoo.com 
```

![alt text](https://raw.githubusercontent.com/mjmanney/hiring-engineers/Michael-Manney_Solutions-Engineer/images/alert_step45.png "Step 4")


Here is a screenshot of the alert in action!

![alt text](https://raw.githubusercontent.com/mjmanney/hiring-engineers/Michael-Manney_Solutions-Engineer/images/alert_email.png "alert email")



### Bonus - Monitor Downtime

Naivate to <https://app.datadoghq.com/monitors#/downtime> and click on Schedule Downtime to create a silence period.

The first schedule sets a daily downtime between 7:00p - 9:00a.  It is OK that it runs on the weekends as we are going to create a second schedule that schedules downtime all of Sat & Sun.

![alt text](https://raw.githubusercontent.com/mjmanney/hiring-engineers/Michael-Manney_Solutions-Engineer/images/downtime_MF.png "weekday downtime")

And the weekend down time...

![alt text](https://raw.githubusercontent.com/mjmanney/hiring-engineers/Michael-Manney_Solutions-Engineer/images/downtime_SS.png "weekend downtime")