# Introduction to Datadog with a quick and easy setup

To better undertsand and visualize Datadog's utility, I'm going to walk through a brief implementation of how to collect a variety of host metrics, integrate a database, monitor metrics with alerts and notifications, and collect Application Performance Monitoring (APM) Data from a simple application.

First we need to utilize any OS/host. This can be done quickly by using a containerized approach such as Docker or by spinning up a Virtual Machine (VM). Due to recommended best practices I used a Vagrant Ubuntu VM. Below are the steps and resources needed to download, install, and initialize the Vagrant Ubuntu VM with VirtualBox on macOS. (Mojave Version 10.14.6.)

For instructions on how to download and install Vagrant see [here](https://learn.hashicorp.com/collections/vagrant/getting-started).

After downloading and installing Vagrant, ```vagrant``` is automatically added to your system path so that it is available to use in your terminal. Below are the following commands to intialize the Vagrant VM.

Initialize Vagrant:
```vagrant init hashicorp/bionic64```

Start the Vagrant VM:
```vagrant up```

Verify the installation worked by checking that the VM is available:
```vagrant status```


Next, we want to install and configure our VM as a Datadog Agent. Before we do this we must sign up for Datadog at https://www.datadoghq.com/. Once we are signed up, Datadog provides us with our API key to use for integrations. We can now install and configure our VM as a Datadog Agent using a one-step install command. Head to the Datadog Integrations tab and use the one-step install for Ubuntu, make sure to run the command inside Vagrant.

To access inside your Vagrant VM:
```vagrant ssh```

One-step Datadog install command for Ubuntu (make sure to use your API key):
```DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=<removed> DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)```

Wait about 5 minutes and then check you Datadog host Dashboard for [Agent metrics](https://github.com/LLabonte94/datadog_screenshots/blob/main/Agent-metrics.png).

And just like that your Vagrant VM is now a Datadog Agent!

![Alt text](https://media.giphy.com/media/111ebonMs90YLu/giphy.gif)


# Tags, Integrating Databases, and Collecting Metrics

Now that our Agent is connected lets start having a little fun with our Agent by adding Tags. Tags are a useful way of adding dimensions to Datadog telemetries so they can be filtered, aggregated, and compared in Datadog visualizations. Tags can be added by updating the Agent configuration file **/datadog-agent/datadog.yaml**.

Add the following code to **datadog.yaml**:

```
tags:
  - environment:dev
  - env:ubuntu
  - version:lukes-vm
```


After updating any code file inside the Vagrant Agent, logout of the Vagrant and restart the Agent:
```logout```
```vagrant reload``` 


Wait a few minutes and then refresh your Host Map in Datadog and then click on your Vagrant Agent hexagon in the Host Map. The [Tags](https://github.com/LLabonte94/datadog_screenshots/blob/main/Tags.png) you just added to the **datadog.yaml** can be seen on the right-hand side. 


> **Note:**
I initially used Docker since I have prior experience using it to spin up instances in the past. However, I switched to Vagrant because I ran into issues when adding Tags. I created a configuration file, **datadog.yaml**, from the **datadog.yaml.example** file in my Docker Agent, but didn’t see the Tags on the Host Map. I also added Tags as environment variables at container creation, but I didn’t see those Tags added to the Host Map either. I then saw some, but not all, of the Tags on the Host Map after waiting about 5-10 minutes. I tried to figure out where they were coming from by adding new, different Tags to the configuration file and as environment variables at container creation, but I did not see these new Tags after copying in the updated configuration file into Agent from my local machine and restarting the Agent. 
>![Alt text](https://media.giphy.com/media/UX08QMbe9BECjRoq3E/giphy.gif)
However, I did not run into any issues when using Vagrant. 

---

Next, let's integrate a database in Datadog and see some metrics. For this part I chose to use Postgres because I have prior experience using it. For instructions on how to download and install Postgres refer to the following [link](https://postgresapp.com/). Go to the Integrations tab and click on Postgres icon and go through each step under "Configuration". 


Below is the code I added to **/datadog-agent/conf.d/postgres.d/conf.yaml** and used to point to my host, port, and database using a username and password. (I forgot to change the password when configuring the database to datadog so that's why the default '<PASSWORD>' from the Postgres configuration steps is in the code below lol).

```
init_config:

instances:
  - host: localhost
    port: 5432
    username: datadog
    password: '<PASSWORD>'
    dbname: postgres
```

After adding this code I again logged out of Vagrant and restarted the Agent. 

To check if Postgres is configured in your Agent you can run the follow code to check the Agent status:
```sudo datadog-agent status```

If you happen to have accidentally left the admin password blank when installing Postgres, you will find out at this point by seeing an error under the Postgres section in the output from the status check above (which I did). I found in the Postgres documentation that doing this will make the admin password **always** fail. However, I resolved the issue by running the following code that runs Postgres as a super user, which overrides the default password.

```sudo su - postgres```
```psql postgres```

![Alt text](https://media.giphy.com/media/JWF7fOo3XyLgA/giphy.gif)

After doing so I was able to see that the issue was cleared up in the status check and in the Host Map, which displayed [intial postgres metrics](https://github.com/LLabonte94/datadog_screenshots/blob/main/Postgres-Integration.png).

---

So far we've added some tags and integrated a Database to our Agent. Now let's create a custom Agent check that submits a metric with a random value between 0 and 1000. A custom check is similar to a regular check, but the custom check can be scheduled to run at a fixed interval. The default is every 15 seconds. If needed, see the [checks documentation](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7) for more information.

We create the following files for our custom Agent check:

**/datadog-agent/checks.d/custom_check.py**
**/datadog-agent/conf.d/custom_check.yaml**

I added the following code to **custom_check.py** to make the custom check compatible with any Agent version:

```
try:
    from datadog_checks.base import AgentCheck
except ImportError:
    from checks import AgentCheck
    from random import randint

__version__ = "7.23.1"

class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(1,1000), tags=['check:check-randint'])
```

Logout and restart the Agent. Wait a few minutes and go to the Metrics tab and create a graph of your metric ('my_metric' from the code above) to check the collection intervals. Change your check's collection interval in the **custom_check.yaml** so that it only submits the metric once every 45 seconds. You do not need to modify **custom_check.py** to see this collection interval change.

```
init_config:

instances:
    - min_collection_interval: 45
```

Again, restart Vagrant and look at the graph of your metric to check to see if the collection interval changed. To get a clear view of the collection interval, click and drag over a section of the grpah to scale the timeframe. The following are screenshots of the updated graph:

https://github.com/LLabonte94/datadog_screenshots/blob/main/check-45-start.png
https://github.com/LLabonte94/datadog_screenshots/blob/main/check-45-end.png


# Visualizing Data using Datadog API

With Datadog we can vizualize data using different types of Dashboards: Screenboards and Timesboards. These Dashboards can be constructed through the Datadog UI or through the Datadog API. We're going to create a Timeboard utilizing the Datadog API to display our custom metric in a couple of different ways and a Postgres metric. To get started using Datadog APIs refer to the documentation [here](https://docs.datadoghq.com/getting_started/api/). We will be using Postman to send a POST request with our Timeboard information in JSON format. The instructions in the link above also include Postman download and setup. 

> **Note:**
We will need our Datadog API Key and an App Key. We can create an App Key by going to API subsection under the Integrations tab. For more information refer to information [here](https://docs.datadoghq.com/account_management/api-app-keys/).

Our Timeboard will have three graphs. The first is using the metric we created in the previous step scoped over our host. The second is a Postgres metric with the [anomaly function](https://docs.datadoghq.com/dashboards/functions/algorithms/) applied. The third is our metric with the [rollup function](https://docs.datadoghq.com/dashboards/functions/rollup/) applied to sum up all points for the past hour into one bucket.

I used the following JSON code in a Postman POST request to create my Timeboard containing the three timeseries graphs:

```
{
    "title": "Luke's Timeboard",
    "widgets": [
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:my_metric{*}"
                    }
                ],
                "title": "Average of My Metric Over Time"
            }
        },
        {
                "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "anomalies(avg:postgresql.postgresql.percent_usage_connections{*}, 'basic', '2')"
                    }
                ],
                "title": "Postgres Percent Usage Anomalies"
            }
        },
        {
                "definition": {
                "type": "timeseries",
                "requests": [
                    {
                        "q": "avg:my_metric{*}.rollup(sum, 3600)",
                        "display_type": "bars",
                        "style": {
                            "palette": "dog_classic",
                            "line_type": "solid",
                            "line_width": "normal"
                        }
                    }
                ],
                "title": "Hourly Rollup Sum of My Metric"
            }
        }
    ],
    "layout_type": "ordered",
    "description": "This is my dashboard",
    "is_read_only": true,
    "notify_list": [
        "luke7@vt.edu"
    ],
    "template_variables": [
        {
            "name": "host",
            "prefix": "host",
            "default": "Luke's Host"
        }
    ],
    "template_variable_presets": [
        {
            "name": "Saved views for hostname 2",
            "template_variables": [
                {
                    "name": "host",
                    "value": "Luke's second host"
                }
            ]
        }
    ]
}
```



> **Note:**
I tried running the code in a Python script using the Datadog library and the ```initialize``` and ```api``` modules, as shown in the [documentation](https://docs.datadoghq.com/api/v1/dashboards/); however, after installing the necessary packages in the Vagrant and running the script, I did not see my Timeboard created in the Dashboard List. I couldn't find any other documentation to resolve the issue, so I sent the request from Postman.


Once the Timeboard is created, we can access the Dashboard from our Dashboard List on Datadog. We can also change the timeframe of our Timeboard to whatever range we want in order to get a better visualization. [Here](https://github.com/LLabonte94/datadog_screenshots/blob/main/Timeboard_5-minute.png) is our Timeboard with a 5-minute interval.

> **Note:**
I was not able to see the Hourly Rollup Sum of **my_metric** in the 5-minute, so I adjusted the timeframe to a [1-hour interval](https://github.com/LLabonte94/datadog_screenshots/blob/main/Timeboard_1-hour.png).


The anomaly graph doesn't seem to have the gray band as show in the documentation. Strange. Lets notify a person of contact who can help us resolve this issue. To do this click the graph and a message box will appear which allows you to create a comment and send a notification to the person(s) of interest by using the "@" notation. [Here](https://github.com/LLabonte94/datadog_screenshots/blob/main/Notification-email.png) is a screenshot to help.


The Anomaly graph is displaying ```postgresql.percent_usage_connections``` metric, which oscillates in such a way that the anomaly gray band around the metric didn't show up in the latest 5-minute interval. By using a 7-day timeframe we are able to see the Anomaly graph displaying the gray band around the metric showing the expected behavior of a series based on the past. Below is the [Anomaly screenshot](https://github.com/LLabonte94/datadog_screenshots/blob/main/Timeboard_7-day_anomaly.png). 

> **Note:**
I could't find a Postgres metric that oscillated over a range that would be seen in the 5-minute interval timeframe. Majority of the Postgres metrics were in steady state after connecting the database since I was not running any database queries, etc.


# Monitoring Data and Alerts

It's great that we can monitor custom metrics, but what about when metrics get to certain critical levels? We don’t want to have to continually watch our Dashboards to be alerted when metrics exceed certain thresholds. So let’s make life easier by creating a monitor for 'my_metric'. We can do this by going to the Monitor tab and create a new Metric Monitor that watches the average of 'my_metric' and will send a warning if it’s above 500 or send an alert if it's above 800 over the past 5 minutes. We will also want to be notified if there is no data for this query over the past 10 minutes. 

Once we've completed making the Metric Monitor in Datadog we can export it into JSON format, as seen below.

```
{
	"id": 25507064,
	"name": "My Metric Threshold Levels",
	"type": "metric alert",
	"query": "avg(last_5m):avg:my_metric{host:vagrant} > 800",
	"message": "{{#is_alert}} my_metric reached a critical level of {{value}} at IP Address: {{host.ip}}, which is unusually high. Check it out ASAP!  @luke7@vt.edu {{/is_alert}}\n{{#is_warning}} my_metric reached {{value}} at IP Address: {{host.ip}}. Keep an eye on it.  @luke7@vt.edu {{/is_warning}}\n{{#is_no_data}} No data coming from my_metric in the past 10 minutes.\n1. Check if {{host.name}} is running\n2. Check my_metric code in configuration file to see if anything has been changed\n @luke7@vt.edu \n{{/is_no_data}}",
	"tags": [],
	"options": {
		"notify_audit": true,
		"locked": false,
		"timeout_h": 0,
		"new_host_delay": 300,
		"require_full_window": true,
		"notify_no_data": true,
		"renotify_interval": "0",
		"escalation_message": "",
		"no_data_timeframe": 10,
		"include_tags": true,
		"thresholds": {
			"critical": 800,
			"warning": 500
		}
	}
}
```


This will send us an email whenever any three of the thresholds from our monitor are triggered. [Here](https://github.com/LLabonte94/datadog_screenshots/blob/main/Monitor-email.png) is an email notification of 'my_metric' exceeding the 500 warning threshold.


Since this monitor is going to alert pretty often, we don’t want to be alerted when we are out of the office. So we'll want to set up two scheduled downtimes for this monitor. One that silences it from 7pm to 9am daily on Monday-Friday and one that silences it all day on Saturday-Sunday. 

Below are the email notifications for the scheduled downtimes:
[Evening Downtime](https://github.com/LLabonte94/datadog_screenshots/blob/main/Evening-downtime.png)
[Weekend Downtime](https://github.com/LLabonte94/datadog_screenshots/blob/main/Weekend-downtime.png)


> **Note:**
When creating the two scheduled downtimes, each the initial notifications showed the correct amount of time, but the start and end times were shifted and I'm not sure why. Screenshots of each downtime setup can be seen below:
[Evening Downtime Mon-Fri](https://github.com/LLabonte94/datadog_screenshots/blob/main/Monitor_M-F.png)
[Weekend Downtime Sat-Sun](https://github.com/LLabonte94/datadog_screenshots/blob/main/Monitor_Sat-Sun.png)


# Collecting APM Data

So far we've been able to collect metrics from our host Agent, Postgres database, and custom metrics as well as create custom monitors and email notifications. But what about monitoring application performance, infrastructure, logs, and traces? Datadog APM allows us to do just that for troubleshooting and optimization. 

We'll instrument the following Flask application with Python using Datadog’s APM solution. Create a Pytho file called ```my-app.py``` and insert the following code:

```
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

Using both ddtrace-run and manually inserting the Middleware has been known to cause issues, so I chose to instrument the application using the ddtrace-run method. Below are the steps to collect APM data for ```my-app.py```.

First, install the ```flask``` and ```ddtrace``` libraries:
```pip3 install flask```
```pip3 install ddtrace```

Add the following code in the ```datadog.yaml```:

```
apm_config:
	enabled: true
```
```
tags:
  - service:myapp-metrics
```

Logout of Vagrant, restart the Agent, and then run the following command to instrument the application:
```DD_SERVICE="myapp-metrics" DD_ENV="ubuntu" DD_VERSION="lukes-vm" DD_LOGS_INJECTION=true DD_TRACE_SAMPLE_RATE="1" DD_PROFILING_ENABLED=true DD_RUNTIME_METRICS_ENABLED=true ddtrace-run python3 my-app.py```

Once the code is running, switch to a new terminal and ping the flask application endpoint using the following commands:
```curl http://0.0.0.0:5050/```
```curl http://0.0.0.0:5050/api/apm```
```curl http://0.0.0.0:5050/api/trace```


Wait about 5-10 minutes and then refresh the Datadog APM Services page to see the Flask application. Below is the link and screenshots of the application's APM data on Datadog:

Link:
[APM and Infrastructure Metrics Dashboard](https://p.datadoghq.com/sb/95557gac4g6agrso-2020678a12480ea825d0308892b21506)

Screenshots:
[APM and Infrastructure Metrics Dashboard](https://github.com/LLabonte94/datadog_screenshots/blob/main/APM-dashboard.png)
[Services List](https://github.com/LLabonte94/datadog_screenshots/blob/main/services-list.png)
[Service - Endpoint Hits](https://github.com/LLabonte94/datadog_screenshots/blob/main/services-1.png)
[Service - Infrastructure Metrics](https://github.com/LLabonte94/datadog_screenshots/blob/main/services-infrastructure.png)
[Service - CPU Performance](https://github.com/LLabonte94/datadog_screenshots/blob/main/service-performance.png)
[Service - Metrics](https://github.com/LLabonte94/datadog_screenshots/blob/main/service-metrics.png)
[Traces](https://github.com/LLabonte94/datadog_screenshots/blob/main/traces.png)
[Continuous Profiler](https://github.com/LLabonte94/datadog_screenshots/blob/main/continuous-profiler.png)


---

Datadog has been used in a lot of creative ways in the past. I think it would be really interesting if Datadog could monitor the wait time at airports, from the time you walk into the airport to the time you board. As opposed to showing up unnecessarily early and having to wait and hour or more at the gate - which I hate - I think it would be efficient if Datadog could give a break down visualization of each step of the process - from checking in, waiting in line to get to security, getting through security, the time it takes to get from security to your gate, etc. Every airport is different in terms of capacity, the amount of foot traffic, speed of checking in, speed of security from the time you put your items on the belt to the time you get through and reclaim your items, distance to gates, etc. and I think a real-time monitoring application for the consumer would make the airport experience more efficient and less stressful. 

![Alt text](https://media.giphy.com/media/l0MYtRMfHX97W7T3y/giphy.gif)
