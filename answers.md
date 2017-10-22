### Daniel Farrington

## Environment 

I opted to run the Datadog agent on my Windows 10 64-bit home machine, just for the sake of personal simplicity. However, for the last part of the challenge, I decided to run the agent off of the recommended [Vagrant](https://www.vagrantup.com/downloads.html) Ubuntu VM, using [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1).

*Note: Vagrant wouldn't detect my installation of VirtualBox 5.2. I had to install version 5.1.14 instead to complete the Vagrant installation.*

With the Vagrant VM set aside for now, I signed up for a DataDog trial, and installed the [DataDog Agent for Windows](https://s3.amazonaws.com/ddagent-windows-stable/ddagent-cli-latest.msi).

## Collecting Metrics

### Tags

To begin, I was able to add a couple of descriptive tags and change the name of my host by editing the datadog.conf file inside of the very convenient Datadog Agent Manager editor. The changes were as follows:

`hostname: dfarrington.home`

`tags: office:home, os:win10`

And the result:
![alt text](https://imgur.com/oVjl0iY.jpg "Host map(s) with tags")

Duplicate hosts! 

This was slightly worrying, though I was reassured [here](https://docs.datadoghq.com/faq/#i-just-set-up-my-aws-integration-why-am-i-seeing-duplicate-hosts) that the duplicate would disappear within 10-20 minutes. And that it did. 

### PostgreSQL Database Integration

I downloaded and installed [PostgreSQL 10 for x86-64 Windows](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads#windows), and then followed the PostgreSQL integration instructions found [here](https://app.datadoghq.com/account/settings#integrations/postgres). This was very straightforward: I started psql and executed the following command: 

```
create user datadog with password '*****************';
grant SELECT ON pg_stat_database to datadog;
```

The Verification:
```
psql -h localhost -U datadog postgres -c "select * from pg_stat_database LIMIT(1);"  
 && echo -e "\e[0;32mPostgres connection - OK\e[0m" || \ ||  
echo -e "\e[0;31mCannot connect to Postgres\e[0m"
```

Next I had to edit and enable the PostgreSQL.yaml file as such: 

![alt text](https://imgur.com/w44wwP6.jpg "PostgreSQL.yaml config")

Following an agent restart:

![alt text](https://imgur.com/QDHy2Bf.jpg "Status")

A successful integration! All that was left to do was ![alt text](https://i.imgur.com/AFLLG3K.png "Install") the integration on the DataDog website. 

### A Custom Agent Check

A custom agent check is a user-created check made for collecting metrics from applications and systems that DataDog hasn't yet had the opportunity to cover. This grants the user nearly unlimited freedom to collect whatever metrics they need.

In order to create a custom agent check, I had to read through and follow the information given [here](https://docs.datadoghq.com/guides/agent_checks). From that, I learned that I had to create two files with the same name: 

**mycheck.py** *C:\Program Files\Datadog\Datadog Agent\agent\checks.d* 

```python
import random
from checks import AgentCheck

class testCheck(AgentCheck):

	def check(self, instance):
		self.gauge('my_metric', random.uniform(0,1000))
```

This code was built off of the hello.world check provided in references. I imported the random library, which gave me access to the random.uniform() function. This function takes two integer arguments as a range and produces a random integer within that range. Lastly, I changed the name of the metric from *'hello.world'* to *'my_metric'*.

*Note: The checks.d directory wasn't where the [Agent Check reference document](https://docs.datadoghq.com/guides/agent_checks/#directory-structure) led me to believe it would be, though it wasn't at all hard to find.*


**mycheck.yaml** *C:\ProgramData\Datadog\conf.d*

```
init_config:
    min_collection_interval: 45
instances:
    [{}]
```

This is simply the skeleton of the configuration file for the agent check. The line 'min_collection_interval: 45' will be discussed in the next section. With the files in place and complete, I restarted the agent, and datadog began collecting my_metric!

![alt text](https://i.imgur.com/Pfua6MI.png "no-namespace is my_metric.")

### Modifying the Check Collection Interval

A check's collection interval governs how often the check can run. It is determined by the presence of `min_collection_interval` in the init_config section of the check's .yaml file, as can be seen above. In my example I use a `min_collection_interval` value of 45. This means that the check will not run until at least 45 seconds have passed. 

The Datadog agent inherently checks to see if any metrics are ready to be collected every 15-20 seconds. This cannot be changed, and thus it is not possible to collect a metric at an interval less than 15 seconds.

### Visualizing Data with a Timeboard

In order to visualize the metrics I've collected, I needed to create a Dashboard. You can do this easily using Datadog's web interface, though it's also possible to use the Datadog API. The API method involved describing the Timeboard in a JSON format, and then passing it through the Datadog API using Python. I used the example request from the [Datadog API Reference page](https://docs.datadoghq.com/api/?lang=python#timeboards) to help get started and build off of. Here's what the complete Python request looks like:

```python
from datadog import initialize, api

options = {
    'api_key': '********',
    'app_key': '********'
}

initialize(**options)

title = "API Timeboard"
description = "The lengthy way."
graphs = [{
    "definition": {
        "requests": [
            {"q": "avg:my_metric{host:dfarrington.home}",
			"type": "line"},
			{"q": "avg:my_metric{host:dfarrington.home}.rollup(sum, 60)",
			"type": "line"},
			{"q": "anomalies(avg:postgresql.rows_returned{host:dfarrington.home}, 'basic', 2)",
			"type": "line"}
        ],
    "viz": "timeseries"
    },
    "title": "my_metric, my_metric, postgresql.rows_returned"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = False

api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)
```

Once I ran the python request, I was able to see my dashboard on the website almost immediately. With that, I set the timetable's timeframe to show only the past five minutes using the keyboard shortcut ALT-\[ , and then took a snapshot of it using the camera button ![alt text](https://i.imgur.com/b09NPLo.png "Camera!") in the top-right corner of the graph. This allowed me to send the snapshot to myself with an @ mention, and view the snapshot in the events stream! ![alt text](https://imgur.com/RbP8xwC.jpg "Notifications")

##### An explanation of the anomaly graph:

The anomaly function applied to a metric uses historical data to predict a range where that metric will most likely fall in, assuming normal operation. On a graph with the anomaly function, the grey band represents that predicted range. If the metric falls within it, it will be colored blue by default. If it falls outside of the range, it is considered anomalous and will be colored red. This behavior can be seen in my graphs above (orange and purple lines instead of blue and red), though a much better example can be seen in the datadog anomalies guide [here](https://docs.datadoghq.com/guides/anomalies/).

### Monitoring Data

A monitor is a tool which can alert us automatically if a metric is displaying alarming behavior, such as abnormally high values, or a loss of data altogether. 

I created a monitor for my_metric, which would send me an alert email whenever my_metric was on average above 800 for five minutes, or a warning email if it was above 500. It would also send an email if there was loss of data for more than 10 minutes. 

![alt text](https://i.imgur.com/wl9mJj5.png "Threshold config")

Next I set up the email notification. This was straightforward, except for the use of the conditional statements, which I used to send the correct message for the given situation. Here's how I set up my notification:

`my_metric Monitor: High my_metric values detected on {{host.name}} [{{host.ip}}]`

```
##{{#is_alert}}my_metric has passed the alert threshold ( {{threshold}} ) on host {{host.ip}}! Value: {{value}}  {{/is_alert}} 

###{{#is_no_data}}my_metric missing data for on host {{host.ip}}!{{/is_no_data}} 

####{{#is_warning}}my_metric has passed the warning threshold ( {{warn_threshold}} ) on {{host.ip}}! Value: {{value}}  {{/is_warning}} 

@farrington512@gmail.com
```

With the monitor configured, all I had to do next was wait for my_metric to trigger the monitor. Instead of waiting patiently though, I modified the random number range in mycheck.py to 500-1000, which net the following alert email (among many):

![alt text](https://imgur.com/P1sITxh.jpg "Uh oh!")

This monitor is great, but it has sent me many emails already in a short time.

![alt text](https://i.imgur.com/26iCMKl.png "Better set my_metric's range back to normal!")

In order to catch a break, I can schedule downtime for the monitor. During downtime, the monitor will be muted and thus will not send out any alerts. Scheduling downtime is a very simple process: You first decide which monitor will be muted. Next, decide whether it's a one-time or recurring downtime, set the repeat interval if applicable (daily, weekly, etc.), determine which days to carry out the downtime, and the amount of downtime. 

As an example, here's my weekday downtime schedule:


![alt text](https://i.imgur.com/W9kctDI.png "Downtime")

And here's the message that lets me know that downtime has begun:
![alt text](https://imgur.com/QMSwvBZ.jpg "Downtime Email")

### Instrumenting a Flask app using Datadog's APM

For this last portion of the challenge, I switched over to the Vagrant VM that I set up at the beginning, and installed the agent using the easy one-step install: 

`DD_API_KEY=***** bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/datadog-agent/source/install_agent.sh)"`

That line also installs the datadog APM component. Couldn't be easier. With the agent up and running, I had to edit datadog.conf to set `apm_enabled` to true. 

Next, using pip, I installed virtualenv, ddtrace, Flask, and blinker, and modified the given Flask app to look like this:

![alt text](https://imgur.com/1sCJiLa.jpg "Flask app")

Finally, I ran the following commmand inside of venv: `ddtrace-run python my_app.py`.
Here's a screenshot of a Timeboard with both APM and Infrastructure metrics:

![alt text](https://imgur.com/Y9EeG1u.jpg "Timeboard")

#### The difference between a Service and a Resource

In regards to Datadog, a service encompasses the processes required to provide a function or a ..service. A resource is a query to a service.

### Creative uses for Datadog

With some new integrations, I can see Datadog being incredibly useful in a hospital, monitering patient biometrics! Each individual patient's monitoring systems would be a host. Then, the vitals of all the patients in the hospital can be reviewed at a glance using the host map! Further, maybe the host map can color the hosts depending on reported heart-rate or blood pressure, instead of CPU utilization. The host-patients could then be grouped and filtered by age, symptoms, disease, hospital wing, anything, really. Doctors could use the dashboard visualizations to monitor a patient's changing health, discuss with others whether or not a particular treatment was successful, next steps to take, and more. With monitors, doctors can be notified immediately when a patient's condition changes and needs attention. I'm sure doctors would appreciate the sanity that comes with Datadog. 

## Conclusion

This ends my answers to the Datadog Solutions Engineer hiring challenge. If you have any questions or concerns about anything here, please feel free to contact me at farrington512@gmail.com. Thanks for reading!
