# Prerequisites: environment setup

For this exercise's environmnet, I decided to go wtih an AWS EC2 instance because why not, right? I launched a t3.micro instance with their latest Ubuntu AMI (18.04.) You can find the instructions how to launch a EC2 instance [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/LaunchingAndUsingInstances.html).

After the instnace became running, I logged into it via ssh and did `sudo apt upgrade` to upgrade and make sure that everything installed is up-to-date. I also installed the datadog-agent by using the bash script for Ubuntu that are available on the Datadog integrations page.

Here's how it looks like when the installation is complete:

<img src="dd_exercise-assets/01_afterSetupTerminal.png">

That should do for this exercise. 

# Collecting Metrics:

## Adding tags

To modify config file of the agent, the first thing you should know is, of course, the default location of config file. It was relatively easy to guess the config file is located at `/etc/datadog-agent/datadog.yaml` from the output of agent installation, but I was also able to find the official documentation [here](https://docs.datadoghq.com/agent/faq/agent-configuration-files/?tab=agentv6).

After fiding the location of config file, I modified the following part of config file to add some tags: `DatadogTechExcersie`, `foo01`, `bar01` and then restart the agent by `sudo service datadog-agent restart`.

```
42 # Set the host's tags (optional)
43  tags:
44    - DatadogTechExcersie
45    - foo01
46    - bar01
```

Here's the screenshot of Host Map page:

<img src="dd_exercise-assets/02_hostmapWithTags.png">

## Database integration

First, I decided to go with MySQL for this and simply did `sudo apt install mysql-server` to install it on my Ubuntu instance. The Ubuntu's official documentaion on MySQL is available [here](https://help.ubuntu.com/lts/serverguide/mysql.html.en).

After that, from the left menu of Datadog conosle, I went to [Integrations] and searched for "MySQL." I simply followed the instruction there and it's installed.

Below is the screenshot of MySQL dashboard after installing the integration:

<img src="dd_exercise-assets/03_MySQLIntegrationInstalled.png">

## Custom agnet check

After taking a look at [Writing an Agnet check](https://docs.datadoghq.com/developers/agent_checks/?tab=agentv6), I created `my_metric.yaml` in /etc/datadog-agent/conf.d/ and `my_metric.py` in /etc/datadog-agent/checks.d/.

my_metric.yaml
```
init_config:

instances:
    [{}]
```

my_metric.py
```
import random
from checks import AgentCheck

class randomNumCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0, 1000))
```

The screenshot of my_metric metrics page:

<img src="dd_exercise-assets/04_mymetric.png">

## Changing check's collection interval to once every 45 sec.

Looking at the `my_metric` metrics on the dashboard created above, it looks like, in my case, it's collecting once every 20 sec. by default. Thus as per the [document](https://docs.datadoghq.com/developers/agent_checks/?tab=agentv6), if I set `min_collection_interval` in `my_metric.yaml` to 45, this metric could be collected as often as every 45 sec. Since I'm using agent v6 for this exercise, adding it to instance level.

Now, my `my_metric.yaml` looks like:

```
init_config:

instances:
    - min_collection_interval: 45
```

## Bonus Question:

Technically, configuring `min_collection_interval` did not modifyied the .py check file, rather it's defined in the .yaml config file.

However to change the interval without modifying niether of those files, I think this cloud be done by changing the main check loop interval of datadog-agent, if there's a way to do so. However, I unfortunately was not able to figure out the way of doing so.

# Visualizing Data:

## Creating a Timeboard utilizing the API

First, for this section I had to get familiar with how to utilize Datadog API. By taking a look at the [API reference](https://docs.datadoghq.com/api/), I figured that all requests to the API must be authenticated. This can be done with an API key, and also an application key if the request requires reading data. 

I've noticed, by now, that API key is stated in datadog-agent's main configuration file. So I used that for the API key. Next thing I needed to do was to obtain an application key. I was able to do it by going to `APIs` page from the left menu on Datadog console and clicking `Create Appliction key`.

After obtaining those keys, I first went ahead to find out how to create a Timeboard with the API. For that, I was able to find the documentaion [here](https://docs.datadoghq.com/api/?lang=python#timeboards).

Now, I know how to create a Timeboard that has a basic graph in it. For this exercise, I also needed to figure out how to inculude a graph with anomaly function applied and a custom metric with the rollup function applied summing up all the point for the past hour. Fortunately, I was able to find documentations for those: [anomaly](https://docs.datadoghq.com/graphing/functions/algorithms/), and [rollup function](https://docs.datadoghq.com/graphing/functions/rollup/) by looking around the documentations. Since the exercise did not specify the algorithm and rounds for anomaly, I went with `basic` for algorith and `2` for rounds.

Please look for `createTimeboard.py` in `dd_exercise-assets` folder for the script that I wrote.

Here's what the Timeboard looks like created by the script utilizing the API.

<img src="dd_exercise-assets/05_timeboardCreatedWithAPI.png">

### Setting timeframe to the past 5 min.

I found that I can zoom in/out the timeframe by using keyboard shortcut `alt + [ or ]` on the dashbaord page. So I first paused the graphs, and then hit `alt + ]` couple of times to zoom in timeframe, and as you can see it on the screenshot below, it's now showing the past 5 min.

<img src="dd_exercise-assets/06_timboardWithZoomedTimeframe.png">

### Taking a snapshot and sending it to myself

To take a snapshot of a graph, I simply clicked the camera icon on the top right corner of the graph. And then I typed `@[my name]` into the notation which automatically pulled up with my registerd email address. After that simply hit enter and it's sent!

<img src="dd_exercise-assets/07_takingSnapshot.png">
<img src="dd_exercise-assets/08_snapshotRecievedEmail.png">

### Bonus Question:

The Anomaly graph is displaying the range of what-it-looks-to-be-normal graph based on history and trends of the metric of the past. I was able to find the official blog post of Anomaly detection [here](https://www.datadoghq.com/blog/introducing-anomaly-detection-datadog/).

# Monitoring Data

To create a new monitor, I clicked `Create Monitor` from graph's top-right geer icon. On the new monitor creation page, I configured as below. 

<img src="dd_exercise-assets/09_createNewMonitor.png">
<img src="dd_exercise-assets/10_createNewMonitor.png">

This should do for request monitor configuration.

For the monitor's message, I found that this could be done with `Say what's happening` section as some variables and conditional statements are available to use such as `{{host.name}}` or `{{#is_alert}}` in it.

Here's how my message looks like:

```
Hey, it's datadog.

{{#is_alert}}
Host {{host.name}} ( {{host.ip}} ) is in ALERT state. 
Recorded value: {{value}} 
{{/is_alert}} 

{{#is_warning}}
This is a friendly WARNING from datadog.

We've detected that your {{host.name}} went above of warning threshold. 
You might wanna take a look at it.
{{/is_warning}} 

{{#is_no_data}}
We don't see any data being recorded from your {{host.name}}.
Maybe configuration error on the host?
{{/is_no_data}}  

Please contact @tacoinf9015@gmail.com for any questions.
```

Screenshots of emails that I recieved. 

<img src="dd_exercise-assets/11_monitorWarning.png">

For the alert state, unfortunately somehow my `my_metric` did not record average above 800 so I modified my `my_metric.py` from 0 ~ 1000 to 700 ~ 1000. By doing so, `my_metric` was successfuly averaged above 800. I also had to cancel the downtime that I configured for the following bonus question to take a screenshot of the notification since I worked on the bonus question first rather than wating for this monitor to be alerm state.

<img src="dd_exercise-assets/12_monitorAlert.png">

For this missing metric state, I simply stopped datadog-agent on my host by running `sudo service datadog-agent stop`.

<img src="dd_exercise-assets/13_monitorNoData.png">

For the Bonus Qestion, I was able to find the documentaion of monitor downtime [here](https://docs.datadoghq.com/monitors/downtimes/).

I've configured some downtimes for the monitor as below.

* One that silinces it from 7pm to 9am daily on M-F

<img src="dd_exercise-assets/14_downtimeMF.png">

The notification mail of downtime configuration:

<img src="dd_exercise-assets/15_downtimeMFNotification.png">

* One that silences it all day on Sat-Sun.

<img src="dd_exercise-assets/16_downtimeSS.png">

The notification mail of downtime configuration:

<img src="dd_exercise-assets/17_downtimeSSNotification.png">

# Collecting APM Data:

First thing I did after taking a look on [APM documentation](https://docs.datadoghq.com/tracing/) and [flask's quick start](http://flask.pocoo.org/docs/0.12/quickstart/), I installed `ddtrace` and `flask` on my host.

```
pip install ddtrace
pip install flask
```

After succesfull installation of those, I went ahead and un-commented out below section on the agent's main config file, `datadog.yaml`.

```
580 apm_config:
581 #   Whether or not the APM Agent should run
582   enabled: true
```

Now, I decided to use the provided flask app for this and I ran the following command to instrument it. (I've named it `givenFlaskApp.py`, which is included in `dd_exercise-assets` folder just in case.)

```
ddtrace-run python givenFlaskApp.py
```

After that I gave couple of requests by using `curl` to givenFlaskApp, I was able to see this flask app on the APM dashboard page.

<img src="dd_exercise-assets/18_APMDashboard.png">

To simulate some loads on the app, I also wrote a small shell script that randomly throws a request to `/` or `/api/apm` or `/api/trace` which looks like:

```
#!/bin/bash

randaomNum=$(( $RANDOM % 3 ))

if [ $randaomNum = 0 ]; then
    curl localhost:5050/
elif [ $randaomNum = 1 ]; then
    curl localhost:5050/api/apm
else
    curl localhost:5050/api/trace
fi
```
(Also included in `dd_exercise-assets` folder as `randomReq.sh`)

And I ran it like:

```
for i in `seq 1 100000`; do ./randomReq.sh; done
```

As a result, I was successfully simulate some loads on the app. (I stopped around 67k requests because I thought that was fairly enough to visualize the data on the dashboard for this exercise.)

Here's the [link](https://app.datadoghq.com/dash/940066/apm-and-infrastructure-metrics) and screenshot of my dashboard that has both APM and Infrastructure metrics. 

<img src="dd_exercise-assets/19_APMAndInfrastructure.png">

### Bonus Question:

I was able to find the [documentation](https://docs.datadoghq.com/tracing/visualization/service/) on a Service and a Resource. According to the documentation, the difference between a Service and a Resource is:

* A service is a set of processes that do the same job like a web framework or database. 
* A resource is one of particular actions for the servic (typically individual endpoints or queries.)

# Final Question:

I remembered reading the article about [monitoring office bathroom availability](https://www.datadoghq.com/blog/engineering/restroom-hacks/) in the past and I touguht that was amazing idea since at that time the company I worked for had a huge problem not having enough bathroom for the amount of people worked there; the bathroom was always being full.

That being said, with the techniques that I've learned so far I think I would write some custom checks that checks the price of products on the EC sites like Amazon, and configure a monitor that notifies me when the price becomes low enough to buy!