
# Acme Corporation Datadog Prof of Concept

This POC will illustrate Datadog’s ability to tie infrastructure and application monitoring together.

At the end of the POC we will have:
	1. Set up a Vagrant Ubuntu Environment
	2. Collect Metrics (memory and processor utilization, database uptime, ect) on our environment
	3. Visualize these metrics to gain insights
	4. Set up alerting conditions
	5. Instrument our Flask application
	6. Use the Datadog API to send custom information such as page views





## Setting up Vagrant Ubuntu Environment

The first step in the POC is to replicate Acme's current technology stack. 

Acme has developed a Flask web application that leverages MongoDB. It is deployed via on premise Ubuntu servers. We will use Vagrant and Virtual Box to create a test environment for the POC. 

The first step is downloading and installing [Virtual Box](https://www.virtualbox.org/wiki/Downloads). 

Tip: If installing Virtual Box on a Mac and your installation fails with the following:

![alt text](https://cl.ly/0S380f2x1W3A/Image%2525202018-07-30%252520at%2525208.52.17%252520AM.png)

You need to allow Oracle to be install in your [Security & Privacy settings[(https://apple.stackexchange.com/questions/301303/virtualbox-5-1-28-fails-to-install-on-macos-10-13-due-to-kext-security)

You will now need to [download Vagrant](https://www.vagrantup.com/downloads.html). Once Vagrant is downloaded you can use the following to get your vagrant environment up and running:

```
$ vagrant init hashicorp/precise64
$ vagrant up
```

If this step is successful should see the following: 

![alt text](https://cl.ly/242O2G113h0J/Image%2525202018-07-28%252520at%25252011.42.52%252520AM.png)


Now that you have your Ubuntu Environment, we need to get the [Datadog agent installed in your environment](https://docs.datadoghq.com/agent/). The Datadog agent is responsible for collecting data from your infrastructure and application. 

But, before installing the agent, you need a Datadog account! Please sign up [here](https://app.datadoghq.com/signup) My account is under jeb2162@gmail.com

After getting your account, you can install the Datadog agent via the following command on your Ubuntu machine:

```
DD_API_KEY=YOUR_API_KEY bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

[This page](https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/) has additional info on installing and using the agent in Ubuntu. Once completed you will see the following in your Ubuntu command line:

![alt text](https://cl.ly/310a0s0U3m2X/Image%2525202018-07-28%252520at%25252012.08.20%252520PM.png)

If you log into your Datadog account online and go to the events section you will see that your Agent has started.

![alt text](https://cl.ly/1p1k1i0a292i/Image%2525202018-07-28%252520at%25252012.09.16%252520PM.png)

Congrats! You are now collecting data on your Ubuntu test environment.




## Collecting Metrics

The previous steps will enable you to collect System metrics such as CPU usage, Network Traffic, and System memory. 

But Acme's use case requires more customization of these metrics. Acme needs to tag incoming metrics, so it can quickly filter data to identify and resolve issues. Acme also needs the ability to capture custom metrics that describe the health of Acmes underlying infrastructure.

To do this we will create tags and a [custom Data check](https://docs.datadoghq.com/developers/agent_checks/) in Datadog.

[Tags](https://docs.datadoghq.com/getting_started/tagging/) are values descriptive value attached to data. This descriptive value help to filter and understand data. Tags will enable us to determine if a CPU usage value is coming from a server in New York or in Boston. 

To [add tags to our application](https://help.datadoghq.com/hc/en-us/articles/203037169-Where-is-the-configuration-file-for-the-Agent-), we will need to open the datadog.yaml file which is located at "/etc/datadog-agent/datadog.yaml" on our Ubuntu machine.

To edit the file, we will use [nano in the command line](https://www.howtogeek.com/howto/42980/the-beginners-guide-to-nano-the-linux-command-line-text-editor/).

To add a tag, insert the following into the datadog.yaml file:

```
tags:
 - location:somerville_ma
 - env_type:test_instance
```

After modifying the datadog.yaml file, restart the Agent and return to your Datadog event dashboard. You should notice your tags are no included in the start event as the following image shows.

![alt text](https://cl.ly/3Z1N1T1g2h1O/Image%202018-07-28%20at%201.34.33%20PM.png)

You will also be able to see the tags in the Host Map section of your Datadog account.

![alt text](https://cl.ly/0Q3l203t123N)


Now we need to show how Datadog integrates with mongoDB. First, lets get a mongoDB instance up. [This article](http://www.mkyong.com/mongodb/how-to-install-mongodb-on-ubuntu/) illustrates how to get mongoDB on Ubuntu. After going through the steps in the article we will want to check that our database is operational. 

If we type mongo into the Ubuntu machines command line, we will enter the mongo shell. We can then type "show dbs" to verify we are connected to our database as shown below:

![alt text](https://cl.ly/47401v3k212j/Image%202018-07-28%20at%201.52.53%20PM.png)


We now need to add the mongoDB integration for Datadog. [This article](https://www.datadoghq.com/blog/monitor-mongodb-performance-with-datadog/) will be a helpful reference. In the integrations section of Datadog search for mongoDB. Selecting the mongoDB integration will lead you to a configuration window as shown below:

![alt text](https://cl.ly/2s0v2D1y2r46)

Here, Datadog will generate commands for you to run in the mongo shell. It will also provide the text of a mongo.yaml file. Follow the instructions to install the mongoDB Datadog Agent. 

Once this is complete you will need to confirm the mongodb service is running via the "sudo -u dd-agent -- datadog-agent check mongo" in the Ubuntu command line. This should yield the following:

![alt text](https://cl.ly/3X2h1w0V093l/Image%202018-07-28%20at%202.29.58%20PM.png)

Now you can go into your Datadog account, the dashboard list, and selecting mongoDB and find the following:

![alt text](https://cl.ly/132q451x1c1w/Image%202018-07-28%20at%202.34.29%20PM.png)

The last component of collecting metrics from our infrastructure is extending the Datadog collection software to acquire custom metrics. We do this via a [custom Agent Check](https://docs.datadoghq.com/developers/agent_checks/). 

To do this we will need to write a custom check in python and configure the Agent to run the check via a .yaml file. To illustrate a custom check, our code will generate a random number between 0-1000 and record that every 45 seconds. We will call this metric 'my_metric'

Let’s call our check joshCheck. We will create a python file "checks.d/joshCheck.py" that contains the following:

```python
from checks import AgentCheck
from random import randint

class joshBrownAgengCheck(AgentCheck):
 
	def check(self, instance):
		self.gauge('my_metric', randint(0, 1000))
```

Next, we need to create the .yaml file 'conf.d/joshCheck.yaml'. Please note, the .yaml file and .py file should have the same name. We will create the following joshCheck.yaml file:

```
init_config:

instances:
    - min_collection_interval: 45
 ```

 Please note, we are setting min_collection_interval to 45 seconds. This does not guarantee joshCheck will run every 45 seconds. It ensures that it will not be collected faster than every 45 seconds.

 Now you can restart the Agent and use 'sudo -u dd-agent --datadog-agent check joshCheck' to confirm the custom Agent check is working. You should see:

 ![alt text](https://cl.ly/1W432S000f2U/Image%202018-07-28%20at%206.50.01%20PM.png)

 Tip: if you see the following:

 ![alt text](https://cl.ly/260i470R101p/Image%202018-07-28%20at%204.46.47%20PM.png)

You have a tab in your .yaml file. Replace the tab with spaces per [this article](https://github.com/moraes/config/issues/1).

Nice, we now have a custom Agent check running! But wait... How can we combine the system, mongoDB, and custom metrics we are collecting to better understand our application’s performance.

That is for the next section.

### Appendix to Collecting Metrics

Looking at a graph of the my_check metric created by joshCheck, I noted the sample interval to be 40 seconds to 1 min. 40 seconds appears to violate the 45 second minimum specified in the joshCheck.yaml file. 

As a test, I removed the min_collection_interval from the .yaml file. Returning to the graph of my_check, the sample rate would be every 20 to 40 seconds. Clearly, the min_colleciton_interval had an effect on the sampling interval. 

I spoke to Mike Moore about this and he indicated that using min_collection_interval is an appropriate approach. I am not sure if the 40 second interval is an artifact of the way data is graphed in the dashboard, an error on my end, or a bug with the agent itself.

I am using Agent 6.




## Visualizing Data

Data Acme's systems, database, and applications in isolation is useless. To reduce downtime and proactively identify weak spots in Acme's infrastructure, we need tie the data we are collecting in the previous section together.

To do this, we will use Datadog's [graphing and dashboard tools](https://docs.datadoghq.com/graphing/).

First, in the Datadog web application, go to Dashboard>New Dash Board. You will see a series of widgets. Drag the Timeseries widget into the finish editing area. This will open a modal that will look like this:

![alt text](https://cl.ly/3c162B3P0b3p/Image%202018-07-30%20at%2011.31.56%20AM.png)

Before we dive into the modal, lets define what we want to see. 

Let’s say the goal of this graph is to help debug an issue with one specific on premiss server. Pretend the issue involves my_metric and our mongoDB database on our server. It would be helpful to see the mongodb database's uptime overlaid on my_metric for this troublesome server.

To do this we will search for and select my_metric from the metric filter from our troubled host (precise64).

![alt text](https://cl.ly/2P3x3Q0l0Z0v/Image%202018-07-29%20at%207.58.08%20AM.png)

Next we will get the mongodb.uptime metric:

![alt text](https://cl.ly/1L3a2z1o1w2x/Image%202018-07-29%20at%207.58.40%20AM.png).

This will yield the following result:

![alt text](https://cl.ly/3t2W1Q1h0R3r)

We can see the blue line representing my_metric varying between 0-1000. 

The mongodb.uptime increases until there is a start event at which point it returns to zero. If my_metric represented a non-random value, we could gain insight into this server’s behavior by looking for a trend with my_metric at the start events.

Of course, once you solve the case of precise64 you will need to share your insights with the team. 

Datadog makes this easy via the share button in the top write of the graph. You can @mention a team might with a screen shoot and notes as shown below.

![alt text](https://cl.ly/0u2M2a2b3x2n/Image%202018-07-29%20at%208.04.31%20AM.png)

What makes Datadog so powerful is how we can layer analysis on top of the data we tie together in graphs. Let’s say as a next step we wanted to troubleshoot the metric mongodb.network.bytesinps. We can use Datadog's anomaly detection (https://www.datadoghq.com/blog/introducing-anomaly-detection-datadog/) to identify trends in data that are abnormal. 

See the graph below:

![alt text](https://cl.ly/1f0V3L0w1o14)

More traditional analysis is also available. Below is an example of taking a one hour rolling average of the my_metric value.

![alt text](https://cl.ly/2u0h0r2i2w2K)

For reference, here are the scripts used to create these graphs:

### my_metric with mongodb overlay scoped to Ubunto Server
```json
{
  "viz": "timeseries",
  "status": "done",
  "requests": [
    {
      "q": "avg:my_metric{host:precise64}, anomalies(avg:mongodb.uptime{host:precise64}, 'basic', 2)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "autoscale": true,
  "events": [
    {
      "q": "start ",
      "tags_execution": "and"
    }
  ]
}
```
### mongodb.network.bytesinps with anomoly analysis
```json
{
  "viz": "timeseries",
  "status": "done",
  "requests": [
    {
      "q": "anomalies(avg:mongodb.network.bytesinps{*}, 'basic', 2)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "autoscale": true
}
```
### my_metric with 1 hour average
```json
{
  "requests": [
    {
      "q": "sum:my_metric{host:precise64}.rollup(avg, 3600)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    }
  ],
  "viz": "timeseries",
  "autoscale": true,
  "status": "done"
}
```

### Additional Info (Bonus) What is the Anomaly graph displaying?

Folks often ask what the anomaly graph is actually displaying. To understand this let’s start with what the mongodb.network.bytesinps represents.

From the Datadog mongoDB integration documentation, mongodb.network.bytesinps represents "The number of bytes that reflects the amount of network traffic received by this database."

So, the blue and red line in the [provided graph](https://cl.ly/1f0V3L0w1o14)) corresponds to the amount of network traffic the database received.

Ok, so why does the line change colors and what is the grey area?

The anomaly tool in Datadog looks at historic values and identifies when a value deviates from an expected range. The expected range is the grey area. A blue line means the value is in the expected range. The red means it falls outside of that range. 

Our data set is small since we just started this server. Thus, you can see the expected value change (get wider in the y axis) as the model adds additional data points. 

Even as the model is being trained on this small dataset, it is smart enough to know that the network traffic from ~18:00 to ~07:00 is abnormal. This makes sense as we are looking at a period where the server was down and thus there was no network traffic. 

Zero traffic is definitely abnormal for a functioning database!




## Monitoring Data

Being able to gain insights from data is useful. But proactively addressing problem to prevent major outages is the ultimate goal of Acme. This is where Datadog's monitoring tools come into play.


Let’s use my_metric to demonstrate Datadog's monitoring capabilities.

Recall, my_metric is a randomly generated value between 0 and 1000. Pretend that values of 500 and above are import to know about. Values of 800 and above require immediate response. 

Setting up alerting in Datadog is straight forward as [this document outlines](https://docs.datadoghq.com/monitors/). If you open the New Monitor section under Monitors, you can configure you monitor to look like the following:

![alt text](https://cl.ly/473e3M1O1Y2l)


Please remember to add your team member to the monitor via the @mention in the Notify your team section. Note that I have created a custom message with template variables. This is helpful as context is critical to generating the proper response from team members.

Given the warning and alert thresholds we have set, you should get an email similar to the following shortly after the monitor is saved.

![alt text](https://cl.ly/022v1S451t1s/Image%202018-07-29%20at%209.00.07%20AM.png)

Nice! Now team members can be notified when something is amok. They will have the proper context and even custom messages with instructions on how to respond. 

The customization of Datadog's monitoring is critical to avoiding the "boy who cried wolf situation." Monitoring that lacks customization can result in to many alerts with no context. This desensitizes team members to the emails and notifications they receive. 

This results in costly inaction when alerts are received. 

### Bonus Question 

Speaking of which, let’s look at how we can put a Monitor to sleep during periods where we do not need to be alerted. A good example might be planned server downtime on a weekend. 

We can schedule one off or recurring downtime using the [Manage Downtime tool](https://www.datadoghq.com/blog/mute-datadog-alerts-planned-downtime/). 

I set up downtime at night as well as on the weekend for the my_metric monitor. Below are the email notifications I received after setting up the downtime.

![alt text](https://cl.ly/1v3N3T2j2a21/Image%202018-07-30%20at%203.19.47%20PM.png)

![alt text](https://cl.ly/2c190a3l3A2A/Image%202018-07-30%20at%203.20.58%20PM.png)



## Collecting APM Data

To truly get a handle on Acme's tech stack, we need to tie the infrastructure monitoring in with application monitoring. 

Let’s use the following Flask App as an example.

```
from flask import Flask
import logging
import sys

import time

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)


now = time.time()
future_10s = now + 10

@app.route('/')
def api_entry():
    print 'In the api entry index'
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    print 'in apm enpoint'
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    print 'in trace endpoint'
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')

```

To instrument this app with Datadog's APM monitoring tools we need to configure our Ubuntu machine to run flask. 

First, we need to install python and pip on the machine. With Ubuntu 16 you may run into a few issues with the installation. [This Stackoverflow post](https://stackoverflow.com/questions/44296498/unable-to-install-pip-in-ubuntu) was extremely helpful for me.

Ensure that python is installed correctly by using "python -v" in the Ubuntu command line. 

Now you can use pip to install Flask, datadog, and ddtrace using "pip install [package]" 

Before you run the app we need to modify the datadog.yaml file. We need to add the following:

```
apm_config:
  enabled: true
```

Restart the Datadog agent and then start the flask app with 'ddtrace-run python flask_app.py' in the Ubuntu command line. If your flask app has a different name than flask_app.py, replace flask_app.py with the appropriate name.

Now if you go to the APM section Datadog, select python, you will see:

![alt text](https://cl.ly/0H0b2v2J012z)

Wait! We already did everything listed on that page. What is going on?

To trouble shoot this we can open '/var/log/datadog/trace-agent.log' on our Ubuntu machine. You will likely see a log that looks like this:

```
018-07-28 16:06:05 INFO (main.go:85) - pid '2099' written to pid file '/opt/datadog-agent/run/trace-agent.pid'
2018-07-28 16:06:05 INFO (main.go:98) - Loaded configuration: /etc/datadog-agent/datadog.yaml
2018-07-28 16:06:06 INFO (trace_writer.go:49) - Trace writer initializing with config: {MaxSpansPerPayload:1000 FlushPeriod:5s UpdateInfoPeriod:1m0s SenderConfig:{MaxAge:20m0s MaxQueuedBytes:67108864 Max$
2018-07-28 16:06:06 INFO (stats_writer.go:42) - Stats writer initializing with config: {MaxEntriesPerPayload:12000 UpdateInfoPeriod:1m0s SenderConfig:{MaxAge:20m0s MaxQueuedBytes:67108864 MaxQueuedPayloa$
2018-07-28 16:06:06 INFO (service_writer.go:31) - Service writer initializing with config: {FlushPeriod:5s UpdateInfoPeriod:1m0s SenderConfig:{MaxAge:20m0s MaxQueuedBytes:67108864 MaxQueuedPayloads:-1 Ex$
2018-07-28 16:06:06 INFO (main.go:161) - trace-agent running on host precise64
2018-07-28 16:06:06 INFO (receiver.go:140) - listening for traces at http://localhost:8126
2018-07-28 16:06:16 INFO (receiver.go:324) - no data received
2018-07-28 16:07:06 INFO (service_mapper.go:59) - total number of tracked services: 0
2018-07-28 16:07:26 INFO (receiver.go:324) - no data received
2018-07-28 16:08:06 INFO (service_mapper.go:59) - total number of tracked services: 0
2018-07-28 16:08:36 INFO (receiver.go:324) - no data received
2018-07-28 16:09:06 INFO (service_mapper.go:59) - total number of tracked services: 0
2018-07-28 16:09:36 INFO (receiver.go:324) - no data received
2018-07-28 16:10:06 INFO (service_mapper.go:59) - total number of tracked services: 0
2018-07-28 16:10:46 INFO (receiver.go:324) - no data received
2018-07-28 16:11:06 INFO (service_mapper.go:59) - total number of tracked services: 0
2018-07-28 16:11:46 INFO (receiver.go:324) - no data received
2018-07-28 16:12:06 INFO (service_mapper.go:59) - total number of tracked services: 0
2018-07-28 16:12:46 INFO (receiver.go:324) - no data received
2018-07-28 16:13:06 INFO (service_mapper.go:59) - total number of tracked services: 0
2018-07-28 16:13:56 INFO (receiver.go:324) - no data received
2018-07-28 16:14:06 INFO (service_mapper.go:59) - total number of tracked services: 0
2018-07-28 16:14:56 INFO (receiver.go:324) - no data received
2018-07-28 16:15:06 INFO (service_mapper.go:59) - total number of tracked services: 0
2018-07-28 16:16:06 INFO (service_mapper.go:59) - total number of tracked services: 0
2018-07-28 16:16:06 INFO (receiver.go:324) - no data received
2018-07-28 16:17:06 INFO (service_mapper.go:59) - total number of tracked services: 0
2018-07-28 16:17:06 INFO (receiver.go:324) - no data received
2018-07-28 16:18:06 INFO (service_mapper.go:59) - total number of tracked services: 0
2018-07-28 16:18:16 INFO (receiver.go:324) - no data received
2018-07-28 16:19:06 INFO (service_mapper.go:59) - total number of tracked services: 0
2018-07-28 16:19:26 INFO (receiver.go:324) - no data received
2018-07-28 16:20:06 INFO (service_mapper.go:59) - total number of tracked services: 0
2018-07-28 16:20:36 INFO (receiver.go:324) - no data received
```

Our service is up and running but no data is being sent. 

The reason is that we have not hit one of the routes in our Flask app. If we use telnet to [send a GET request](http://blog.tonycode.com/tech-stuff/http-notes/making-http-requests-via-telnet/) and return to the APM section of Datadog we will now see:

![alt text](https://cl.ly/3J270b1n1z2S)

Now you can use the export function - top right hand corner of the graphs in the above image - to add these graphs to our previously created dashboard.

[Dashboard with APM and Infrastructure](https://app.datadoghq.com/dash/873979/joshuas-timeboard-28-jul-2018-1851?live=true&page=0&is_auto=false&from_ts=1532807383334&to_ts=1532980183334&tile_size=m)
![alt text](https://cl.ly/0J0T372m3Q3F)


Datadog is now providing insights across Acmes application and infrastructure.

### Bonus Question: What is the difference between a Service and a Resource?

A service refers to functionality delivered by a group of processes. A resource is a query to a service.

To illustrate, consider the application I developed for New Model Investing. 

Part of the app I developed enables the user to search the database of trades made by the portfolio manager. This is the "trades_search" service. All of the background code - mongodb interface, real time calculations, ect - are a part of this service.

The resource is a specific query made to the service. Looking at the url below you, everything after '/trades_serach/' is a part of the resource. The resource provides the service with the information to understand which trades the user is searching for.

```
/trades_search/?&trade_type=Long-Call-Spread,&option_type=SLD,&trade_date=01/01/2018%20-%2005/04/2050,&expiry_date=01/01/2018%20-%2005/04/2050,&max_moneyness_at_initiation=,&min_moneyness_at_initiation=,&max_duration_at_initiation=,&min_duration_at_initiation=,&min_tp_added_at_initiation=,&max_tp_added_at_initiation=,&min_total_tp_added_at_initiation=,&max_total_tp_added_at_initiation=,&max_current_moneyness=,&min_current_moneyness=,&min_duration_current=,&max_duration_current=,&min_mtm_per_contract_profit=,&max_mtm_per_contract_profit=,&min_mtm_total_profit=,&max_mtm_total_profit=,&primary_sort=Symbol,&secondary_sort=Symbol,&third_sort=Symbol,&fourth_sort=Symbol,&reverse_sort=True,&max_number_of_results=,
```

## Final Question

I would use Datadog to monitor the application I have developed for New Model Investing. 

I have a Django app deployed on Heroku, mongoDB Atlas hosted database, and several python scripts running on AWS that interface with our Brokers API to collect and push data to the mongoDB database.

Currently, I get alerted to system outages by my boss giving me a phone call saying something is not working. Debugging the situation is difficult as the issue may lie in Djanog, MongoDB, AWS, Heroku, or a python script. 

Datadog would help reduce response time to outages by giving me a heads up when something went wrong as well as clues as to where to look.

Further, the data would help me understand where the pain points are in my tech stack.

This could help me justify investing development time to improve existing technology.















