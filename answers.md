# Datadog Sales Engineer Technical Exercise

Larry Mahoney\
larrymahoney98@gmail.com\
Email address for Datadog Trial Instance:  z98alpha@gmail.com (because I had already done a free trial with larrymahoney98@gmail.com)

## This document is meant to be Customer Facing

I have formatted the remainder of this document to be a customer facing piece that you can leave with a prospect to help close a deal.  This is a guide for prospects that want to learn more about about **Datadog** by taking it for a test drive.  It will walk them through 3 easy steps where they will learn about Metrics (collecting, visualizing and monitoring) and get a taste of APM (instrumenting code and viewing performance).

This was a really fun project!  And you have an awesome product that just works!

#############################################################################################


![logo](datadog-logo.png)


# Let's take a tour of Datadog in three Easy Steps!

Congratulations!  You have found the most powerful platform for monitoring metrics, traces and logs on the planet.  Buckle in and lets take it for a test drive.  In the following 3 steps, we will walk you through:

* Step 1 -- Setting up your Datadog laboratory
* Step 2 -- Metrics - Collecting, Visualizing and Monitoring  
* Step 3 -- APM - Trace that Call!


## Step 1 -- Setting up your Datadog laboratory

![Frank](Frankenstein.png)

### Spin up a Linux VM  

You will need a test host for the following trial of **Datadog**.  It can be any OS or host.  You can use Hashicorp's Vagrant to spin a dev environment. Or you can use IaaS.  The example that follows uses and Ubuntu 18 VM on AWS.  We recommend that you use a fresh Linux install (Ubuntu `v. 16.04` or later is recommended).  

VM Specs - the following minimum specs will work fine for this trial:
* 1 vcpu
* 1 GB memory
* 8 GB storage

On AWS, the t2.micro instance is sufficient.  Here is what our test VM looks like on the Instances dashboard:

![Linux VM](linux_vm.png)

### Sign up for a Datadog Free Trial

Register for a free **Datadog** 14-day trial here [here](https://www.datadoghq.com/free-datadog-trial/). And let your account team know if you need more time.  We can extend your trial!

![Free Trial](FreeTrial.png)

### Add Tags in the Datadog Agent config file

Edit the `datadog.yaml` file in the `\etc\datadog-agent` directory.  Add your own custom tags using this syntax:

```YAML
tags:
   - custom_OS:Ubuntu18
   - custom_aws_host:Datadog-MondoDB
   - custom_location:Denver
```

Then in Datadog, navigate to `Infrastructure > Host Map` and click on your host. You will see something like this with your custom tags shown in the `Tags` block:

![My Host and Tags](my_host_tags.png)

### Database

It's time to install a database. Any database will do ... MongoDB, PostgreSQL, MySQL, etc.  In this example, we are using `MongoDB v. 4.2.8`.

![database issues](database-issues.jpg)

You can find instructions for installing MongoDB [here](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/).

### Integrations !!!

Datadog has more than 400 integrations.  What is an integration?  See an introduction [here](https://docs.datadoghq.com/getting_started/integrations/).



![integrations](integrations.png)


Datadog integrations span numerous categories.  You will find what you need.  Or let your account team know.  We're likely working on it.

![int-cats](int-cats.png)

Install the integration for the database that you installed on your test bench.  After you do, navigate to `Integrations` in **Datadog** and you will see confirmation of your installed integrations:

![MongoDB](mongodb.png)

## Step 2 -- Metrics - Collecting, Visualizing and Monitoring

![Girl](Girl.png)

### Let's create a Custom Agent Check

We are going to create a **Custom Agent Check** named 'my_metric' that generates random values between 0 and 1000.  And we will set the collection interval to 45 seconds.  Here is the python code to create the **Custom Agent Check**.  Put this code in `/etc/datadog-agent/checks.d/my_metric.py`.

```Python
from random import random

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
        self.gauge('my_metric', value=random()*1000, tags=['TAG_KEY:TAG_VALUE'])
```

Then, to set the collection interval to 45 seconds, put the text below into `/etc/datadog-agent/conf.d/my_metric.yaml`.  Then be sure to restart the agent to start your custom check.  See below for a table of **Agent Commands**.

```YAML
# instances: [{}]

init_config:

instances:
  - min_collection_interval: 45
```

See this article for more details on [Writing a Custom Agent Check](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7).

* **Bonus Question:** Can you change the collection interval without modifying the Python check file you created?

Yes, you can set the collection interval in the YAML config file as shown above.  Here is a screenshot showing the 45 second collection interval.  

![interval](my_metric_interval.png)

**Note:** Setting the collection interval to 45 seconds does mean that **Datadog** will collect a metric every 45 seconds.  Rather, the agent will make a best effort to collect every 45 seconds (it will be collected as often as every 45 seconds).  The actual interval will be dependent on Agent loading (driven by, among other factors, the number of integrations enabled on that agent).

### Datadog Agent Commands

Action | Linux Command
------ | -------------
**Start** the Agent | `	sudo service datadog-agent start`
**Stop** the Agent | `sudo service datadog-agent stop`
**Restart** the Agent | `sudo service datadog-agent restart`
Agent **Status** | `sudo service datadog-agent status`

See this page for more [Agent Command details](https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6v7).

### Visualizing Data

Now let's use the [**Datadog** API](https://docs.datadoghq.com/api/) to create a Timeboard that contains:

* 'my_metric' scoped over your host
* MongoDB Writes/Sec metric with the anomaly function applied
* 'my_metric' with the rollup function applied with a 1 hour range.

See the file `make_dashboard.py` for the detailed code to do this.  Here is the core of that code:

```Python
title = 'Mahoney Dashboard-7'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{host:i-0b2438f9031697d3c}'}
        ],
        'title': 'My Metric'
    }
    },
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{host:i-0b2438f9031697d3c}.rollup(sum, 3600)'}
        ],
       'title': 'My Metric - Rollup 1 Hour'
    }
    }
    ,
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'anomalies(mongodb.opcounters.updateps{*}, "basic", 2)'}
        ],
        'title': 'MongoDB Writes/Sec - Anomalies Function'
    }
    }
    ]
```

And here is the resulting Timeboard, shown with 4h and 8h spans:

![dashboard 4h](my_dashboard_4h.png)

![dashboard 8h](my_dashboard_8h.png)

Link to dashboard:
https://p.datadoghq.com/sb/wtoiabphsohwb8fi-c902bc17dca7f4b703f79280584690c8

### Snapshot of Graph

Now set the timeframe to the past 5 minutes and send a snapshot to myself using the @'your user id' notation.

![snapshot](snapshot.png)

* **Bonus Question**: What is the Anomaly graph displaying?

The Anomaly graph is showing the actual measured metric with an overlay in gray that shows the 'normal' range of values. This allows the operator to very easily see when a metric is abnormal even if it experiences cyclical perturbations.

### Monitoring Data

Now navigate in **Datadog** to 'Monitors > Manage Monitors'.  Using the instructions [here](https://docs.datadoghq.com/monitors/monitor_types/), create a monitor called "My_Metric Monitor" that triggers in these conditions:

* Warning if average above 500 over last 5 minutes
* Alert if average above 800 over last 5 minutes

And also set up the monitor to notify if you if there is no data for this query over the past 10m.  Set it up to email you with notification type, host IP and actual metric value.  Here is a sample email:

![monitor alert email](monitor_alert_email.png)

### Scheduled Downtimes

Let's assume that you don't want to be alerted except during office hours Monday to Friday. Using the instructions [here](https://docs.datadoghq.com/monitors/downtimes/?tab=bymonitorname), set up two scheduled downtimes for this monitor as follows:

  * From 7pm to 9am daily on Monday-Friday
  * All day on Saturday-Sunday

Set it up to email you want the downtime is scheduled.  Here is a sample:

![downtime](downtime.png)

# Step 3 -- APM - Trace that Call() !

![operator](operator.png)

Now let's learn about **Datadog's powerful APM** capabilities.  There are two ways to instrument code for APM:
* Use ddtrace-run at the command line
* Insert APM middleware in your code

You can see a sample by inspecting `flaskapp.py` where you will see that we added code to enable analytics.  We then used ddtrace-run to capture APM data.

### Bonus Question
What is the difference between a Service and a Resource?

A Resource is typically an instrumented endpoint.  But it can also be a database query or a background job.
A Service is a collection of endpoints, queries or jobs.
In this example, the app `flaskapp.py` embodies the service, whereas the endpoints /api/apm and /api/trace are resources.

Here is screenshot and link to an example Dashboard with both APM and Infrastructure Metrics:

![dash apm](dash_apm.png)

https://p.datadoghq.com/sb/wtoiabphsohwb8fi-45cb1ab404e3e28e6792a2286b03646a


# Thank you for evaluating Datadog!

You did it!  You finished your quick evaluation of Datadog with a tour of **Metrics** and **APM**.  Keep in mind that Datadog also monitors **Logs** rounding out the the [Three Pillars of Observability](https://www.datadoghq.com/blog/apm-watchdog-service-map-trace-search/). 

## Let your account team how it went!


![logo](datadog-logo.png)


#############################################################################################

## Final Question:

Is there anything creative you would use **Datadog** for?

COVID-19 Park Alert!
I would get public access to municipal cameras at the city's parks and feed them into a crowd-counting service like Amazon Rekognition.  And then pull that data into Datadog and do analytics on the crowd size data as well as weather data to send alerts when the crowd size is low on days that are sunny!  The alerts would let you know when you can throw your frisbee to your dog at the park with extra social distancing!

## Thanks!

Thank you for reviewing my work!  This was a blast!

Larry Mahoney\
larrymahoney98@gmail.com\
970.214.3685
