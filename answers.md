Your answers to the questions go here.

Prerequisites - Setup the environment
=================================

I created an ec2 instance in my account, for now I will use a t2.micro, if I find that later steps demand more, I will resize the instance.

I installed the datadog client, and 
![image](images/installed-agent.PNG?raw=true "Installed Agent")

during the startup processs, I saw the filename  "/etc/datadog-agent" so I would assume this is the config file, a quick google search confirmed this.


*Collecting Metrics:*
**Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.**

running a "grep" command, allowed me to find that there was infact a direct mention of "tags" within this file, and as such, I have created 3 tags as follows:


![image](images/tags.PNG?raw=true "Tags")

**one thing to note, I had to stop here for 2 days to move house, I am currently trying to troubleshoot getting the client to publish metrics once again as my instance was stop-started, these steps may give some insight into the troubleshooting steps I have followed**

I checked the outbound SG on my instance, and could see that all outbound traffic was allowed. As SGs are stateful,I do not need to open inbound traffic (unlike ACLs).

I searched online and found the doc:

https://docs.datadoghq.com/agent/troubleshooting/

when first thing to check per the doc was my API-key. When checking the datadog config file, the API key was the same. 

I restarted the datadog client to ensure it was up and sending traffic (should have checked top before hand to confirm if it was running).

this did not work^^ as such, I am trying to find the status of the agent on the instance.

I found the doc here https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/?tab=agentv6v7 outlining how to check the status
running the command :

sudo service datadog-agent status

and see the following information:

![image](images/broken.PNG?raw=true "Broken")

My guess is that there is a small difference in the datadog.yaml vs the default (which I found datadog provides here https://raw.githubusercontent.com/DataDog/datadog-agent/master/pkg/config/config_template.yaml)

as such, I will compare the two files to see that is different

Two files look Identical, in almost all parts

![image](images/diff.PNG?raw=true "Diff")

found the agent logs are contained in "/var/log/datadog/agent.log"

66: did not find expected '-' indicator
2021-04-19 22:21:51 UTC | CORE | INFO | (pkg/logs/logs.go:162 in Stop) | Stopping logs-agent
2021-04-19 22:21:51 UTC | CORE | INFO | (pkg/logs/logs.go:174 in Stop) | logs-agent stopped
2021-04-19 22:21:51 UTC | CORE | INFO | (cmd/agent/app/run.go:466 in StopAgent) | See ya!
2021-04-19 22:21:52 UTC | CORE | INFO | (pkg/util/log/log.go:526 in func1) | runtime: final GOMAXPROCS value is: 1
2021-04-19 22:21:52 UTC | CORE | WARN | (pkg/util/log/log.go:541 in func1) | Error loading config: While parsing config: yaml: line 66: did not find expected '-' indicator
2021-04-19 22:21:52 UTC | CORE | ERROR | (cmd/agent/app/run.go:234 in StartAgent) | Failed to setup config unable to load Datadog config file: While parsing config: yaml: line 

is contained in the logs, checking to see what is on line 66

line 66 contains "tags"

checking compared to the github example, I cannot see a "-" in either, perhaps it is a missing space?

Will test and try again

did not work, I changed 

datadog.yaml.example to contain the same information, and a comparison looks as follows:

![image](images/replacing-config.PNG?raw=true "replacing-config")


based on the error changing from:

66: did not find expected '-' indicator

to

65: did not find expected key

my guess is that it is to do with spacing

changed spacing from


 tags:
   - environment:dev
   - 12456:23456

to 

tags:
 - environment:dev
 - 12456:23456

and it worked! not sure why this change broke my config if it was set up this way previously

I can now see my tags created correctly within the datadog console:

![image](images/tags2.PNG?raw=true "tags2")



**Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.**

installed the database:

![image](images/database.PNG?raw=true "database")

found the steps to integrate mysql here
: https://app.datadoghq.eu/account/settings#integrations/mysql

After following these steps, I ran some basic queries against the database:


![image](images/databaseQueries.PNG?raw=true "databaseQueries")


**Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.**

checked on the datadog docs to find what a custom agent check is, and found that it is the equivalent to a custom cloudwatch metric, and it contains a .yaml file, along with a python script, within the checks.d folder. As such I am creating 2 files

I found the following sample code


```
# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('hello.world', 1, tags=['TAG_KEY:TAG_VALUE'] + self.instance.get('tags', []))
```

I will test this out to see what is performed, my understanding is that I should have a metric named "hello.world" with a value of 1 published each time


checking the console, this was correct, as such, I changed my custom agent to the following:


```
# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck

except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck

import random
# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric',random.randint(1,1000), tags=['environment:testing1234567'] + self.instance.get('tags', []))
```
with the following YAML file

```
init_config:

instances:
 - min_collection_interval: 45
```


![image](images/customMetric.PNG?raw=true "customMetric")

**Bonus Question Can you change the collection interval without modifying the Python check file you created?**]

as per the docs here https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7

sample rate is determined by the config file rather than the python file, therefore my assumption would be that yes, we can modify the sample rate without editing the checks file.


*Visualizing Data:*
**Utilize the Datadog API to create a Timeboard that contains:

Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.**


I searched online for creating a timeboard, and found the doc "https://docs.datadoghq.com/api/latest/dashboards/"

as such, I found some sample code

```
from datadog import initialize, api

options = {
    'api_key': '<DATADOG_API_KEY>',
    'app_key': '<DATADOG_APPLICATION_KEY>'
}

initialize(**options)

title = 'Average Memory Free Shell'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:system.mem.free{*}'}
        ],
        'title': 'Average Memory Free'
    }
}]
layout_type = 'ordered'
description = 'A dashboard with memory info.'
is_read_only = True
notify_list = ['user@domain.com']
template_variables = [{
    'name': 'host1',
    'prefix': 'host',
    'default': 'my-host'
}]

saved_views = [{
    'name': 'Saved views for hostname 2',
    'template_variables': [{'name': 'host', 'value': '<HOSTNAME_2>'}]}
]

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables,
                     template_variable_presets=saved_view)
```

two parameters "api_key" and "app_key" were not documented as to where they can be found, but when checking the "integrations" tab within the user interface, there is section on api keys, and so I copied my API-key from there, likewise, in the user interface, it asked me to go to the "teams" page to find information on application keys, and so I generated a key from here also.

I spent a long time trying to troubleshoot why exactly I was not generating a timeboard.

I printed the response from the API call to datadog and receieved the following:

![image](images/forbidden.PNG?raw=true "forbidden")

I believed it was something to do with my API keys, but when searching this page: https://docs.datadoghq.com/api/latest/authentication/

it states 

``
Note: All Datadog API clients are configured by default to consume Datadog US site APIs. If you are on the Datadog EU site, set the environment variable DATADOG_HOST to https://api.datadoghq.eu or override this value directly when creating your client.
``

for this reason, I ran the command 

export DATADOG_HOST=https://api.datadoghq.eu

and my script started to work.

after creating the three metrics in my timeboard, it looked as follows:


https://p.datadoghq.eu/sb/ad717832-9ec8-11eb-b447-da7ad0900005-b5af1c4d5987a36863b70f068c06ded1

![image](images/3graphs.PNG?raw=true "3graphs")



**Take a snapshot of this graph and use the @ notation to send it to yourself.**

I sent a snapshot to my user within the UI here:

![image](images/snapshot.PNG?raw=true "snapshot")


**Bonus Question: What is the Anomaly graph displaying?**


Anomaly detection is to detect any outlier data or "Anomaly's" within the data, say for instance a CPU is on average at 20-30% load, we can detect if over a certain period, it is now averaging 40-45%, this may not be a cause for alarm, but rather a cause for an investigation rather than outright using an alarm such as cloudwatch alarms.



**Monitoring Data
Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.**

**Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:**

**Warning threshold of 500**
**Alerting threshold of 800**
**And also ensure that it will notify you if there is No Data for this query over the past 10m.**

created threshold alarm as described

![image](images/thresholdAlarms.PNG?raw=true "thresholdAlarms")


*Please configure the monitor’s message so that it will:*

**Send you an email whenever the monitor triggers.**

**Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.**

![image](images/email.PNG?raw=true "Email")


**When this monitor sends you an email notification, take a screenshot of the email that it sends you.**

![image](images/alarm.PNG?raw=true "alarm")

*Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor*

**One that silences it from 7pm to 9am daily on M-F**


![image](images/downtime1.PNG?raw=true "downtime1")
**And one that silences it all day on Sat-Sun.**

![image](images/downtime2.PNG?raw=true "downtime2")

**Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.**

![image](images/downtime3.PNG?raw=true "downtime3")