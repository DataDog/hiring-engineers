# DataDog Solutions Engineer Excercise

# Intro
Thank you for granting me the opportunity to complete this challenge! Most of it was straightforward and the datadog documentation made completing virtually every task quite simple. Without further ado, let's begin!


## Prerequisites (setting up the environment)

The very first thing I did as per the instructions, was skim through the references that were provided at the bottom of the assignment. Once I felt that I had a general understanding of Datadog and how it works, I was ready to proceed forward.


For setting up the environment, I opted to use Vagrant and Virtualbox because I already had Virtualbox installed. Although I've never used Vagrant to setup an Ubuntu VM before, it was quite simple and the steps outlined here were easy to follow:
https://www.vagrantup.com/intro/getting-started/

The version of Ubuntu that was setup in the VM was 12.04

I then created a new Datadog account and connected the agent to my new VM using the steps outlined here: https://app.datadoghq.com/account/settings#agent/ubuntu

The only issue I ran into was that the Datadog agent failed to install the first time around, but after trying again it succeeded. Here is the error that was displayed:

![Error](https://i.imgur.com/BrrmeTd.png)

I then checked the status of Datadog by running "sudo datadog-agent status" and by logging onto the Datadog portal online. At this point the testing environment is ready.
![Status](https://i.imgur.com/xDpn6bj.png)

## Collecting Metrics
1. "Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog."

In order to do this, I simply edited the datadog.yaml file located in /etc/datadog-agent/datadog.yaml and add the following line with whatever tags I'd wanted:
tags: great:success, datadogisthebest

I can then see our host from the Datadog hostmap, along with the tags I just assigned.
![Tags](https://i.imgur.com/tBn9cjG.png)

2. "Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database."

I opted to install MySQL since that is what I'm most familiar with. 
First, I installed MySQL on the VM. To do this I ran the following command:
sudo apt-get install mysql-server -y

Now I was ready to connect Datadog to my new MySQL server, so I followed the steps outlined here: https://app.datadoghq.com/account/settings#integrations/mysql

Following the above steps a new user is created called datadog and the appropriate permissions are granted to the user in order to obtain certain metrics from Datadog.

I checked that the user was sucessfully created and that the appropriate permissions are granted by running:

mysql -u datadog --password='REPLACE_WITH_YOUR_PASSWORD' -e "show status" | grep Uptime && echo -e "\033[0;32mMySQL user - OK\033[0m" || echo -e "\033[0;31mCannot connect to MySQL\033[0m"

and

mysql -u datadog --password='REPLACE_WITH_YOUR_PASSWORD' -e "show slave status" && echo -e "\033[0;32mMySQL grant - OK\033[0m" || echo -e "\033[0;31mMissing REPLICATION CLIENT grant\033[0m"

I then saw that the user was created with the appropriate permissions.

![MySQL](https://i.imgur.com/hsQvKLi.png)

Finally, I checked that Datadog was succesfully reporting MySQL server metrics by going to the metrics explorer and selecting a MySQL metric. I ran a bunch of select queries and then plotted the resultant graph of the "mysql.performance.com_select" metric. I saw the spike from me running the select queries.

![MySQL2](https://i.imgur.com/PVtbt9C.png)


3. "Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000."

To accomplish this, I followed the steps outlined here:  https://docs.datadoghq.com/developers/agent_checks/

I was particularly interested in the part of the article that talks about "Your First Check." After completing the steps outlined in the article, I saw that the metric "hello.world" was sucessfully reporting to Datadog by monitoring it from the metric explorer. 

![HelloWorld](https://i.imgur.com/sFKBuMU.png)

Now that I was able to create a check, I was ready to create the new metric that reports a random number from 0-1000. I used the exact same yaml file as from the hello.world check but I renamed it to "my_metric.yaml".

The python code is also very similar to the hello.world code but I added/modified a few things. First, I wanted to change the name of the metric from "hello.world" to "my_metric".

```python
self.gauge('my_metric', 1)
```

Then, instead of reporting a constant 1, I wanted to generate a random number from 0-1000. To do that, I needed to important the "random" library into python by adding the line "import random" to the top of our code. I can generate a random number between 0-1000 with the randint member of the random class "random.randint(0,1000))" My final code looks like the following:


```python
import random

from checks import AgentCheck
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0,1000))
```

Then, I restarted the Datadog agent by running the command:

sudo service datadog-agent restart

Finally, by checking my new metric "my_metric" in the metrics explorer, I saw that our check is successfully generating random numbers between 0-1000.

![my_metric](https://i.imgur.com/oshMTBs.png)

4/5. "Change your check's collection interval so that it only submits the metric once every 45 seconds.
Bonus Question Can you change the collection interval without modifying the Python check file you created?"

Here, I can kill two birds with one stone.

I will first answer the bonus question for which I refered to this article: https://docs.datadoghq.com/developers/agent_checks/#configuration

Yes, I can modify the collection interval without modifying my python code. I simply needed to modify our .yaml file for our my_metric to include the following line of code:

   -  min_collection_interval: 45

The my_metric.yaml file then looks like this:

```
init_config:

instances:
   -  min_collection_interval: 45
```

I have now successfully changed the collection interval, and all that is left to do is restart the Datadog service by running the command:

sudo service datadog-agent restart

As per the documentation, it is important to note that this does not guarantee a collection every 45 seconds. Instead, it means that this particular check *may be collected* as often as every 45 seconds. 

![NewInterval](https://i.imgur.com/c6W1vHL.png)

I saw that Datadog is now reporting less often than before as the data points were more spreadout. 


*It is important to note that the time scale on the metric explorer is always in increments of 20 seconds, so I will not see a metric exactly every 45 seconds.*


## Visualizing Data

Utilize the Datadog API to create a Timeboard that contains:

Your custom metric scoped over your host.
Any metric from the Integration on your Database with the anomaly function applied.
Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

In order to accomplish this task, I first installed the Datadog python library by following the instructions on the Datadog python github: https://github.com/DataDog/datadogpy

I ran the command:
pip install datadog

At this point I was ready to begin writing the timeboard code in python. To do this, I referenced the following article:
https://docs.datadoghq.com/api/?lang=python#timeboards

I then wanted to compile this code but I needed to get the API keys from Datadog. To obtain them, I went to the API tab on the integrations menu and generated a new key by selecting "Create Application Key":

The code I compiled was taken from the datadog doc and is seen below:

```python

from datadog import initialize, api

options = {
    'api_key': '<YOUR_API_KEY>',
    'app_key': '<YOUR_APP_KEY>'
}

initialize(**options)

title = "My Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:system.mem.free{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "Average Memory Free"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)                     
```

I executed this code and verified that it successfully created a timeboard by looking on the Datadog page and seeing "My timeboard" under Dashboards. I was then ready to add the metrics specified for this excercise to the timeboard. Namely,

-my_metric scoped over host
-any other metric with the anomaly function applied to it
-my metric with a rollup function applied to it

To accomplish this, I again referenced the timeboard article above and followed the format that is specified under graphs to modify my code to include those 3 graphs. 

Since I also needed to use the rollup and anomalies function I needed the documentation on those. I recalled seeing a functions section from the graphing documentation, so I opened that up as well and found them there.
https://docs.datadoghq.com/graphing/miscellaneous/functions/

For the anomalies detection method, I opted for basic because none of the data monitored on my Datadog is seasonal. I selected the mysql.performance.com_select to monitor for anomalies since it is really easy to generate an anomaly. That's because my select queries are constant (I'm not actively using the SQL server). Lastly, I opted to use 1 as my deviation number.

My code then looked like the following:

```python

from datadog import initialize, api

options = {
    'api_key': '**dont put your api keys on the internet!**',
    'app_key': '**nor your app keys!'
}

initialize(**options)

title = "Datadog Assignment Timeboard"
description = "Datadog rocks!"

graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.performance.com_select{*}, 'basic', 1)"}
        ],
        "viz": "timeseries"
    },
    "title": "SQL Select Anomalies"
    

},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{*}.rollup(sum, 3600)"}
        ],
        "viz": "timeseries"
    },
    "title": "my_metric rollup"
    

}
]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)

```

I executed the above python script and my new timeboard was created in Datadog!

Then, I was supposed to change the timeboard scale to 5 minutes. There was no way to do this normally through the ui, but I noticed that the time board's time range is specified in the URL through a difference of milliseconds!

## So I was able to change the time scale to 5 minutes by simply adding 300000ms to the "from_ts" parameter in the url and pasting it into the "to_ts" parameter.

![5 Minute TB](https://i.imgur.com/oIHtT8Z.png)

![Anomaly](https://i.imgur.com/hp6LqYw.png)

Bonus Question: What is the Anomaly graph displaying?
The anomaly graph is comparing past data trends to present ones. If something seems out of the ordinary, Datadog flags it as an anomaly. The SQL select query metric was a great example. Since I'm not using the SQL server for anything other than this assignment, the select queries are always at a constant level. Thus, by logging into my SQL server and spamming select queries, Datadog immediately flags this as an anomaly because all of a sudden, the amount of select queries is looking different than how it usually looks based on the past. That is why the SQL select query spike portion is highlighted red.


## Monitoring data

Creating a monitor in Datadog is straightforward. I first went to the monitors section on the Datadog page and selected "New Monitor"
https://app.datadoghq.com/monitors#/create

I left the default threshold alert there because we want the threshold at 800. I input my_metric as the metric to monitor. input the warning and alert thersholds, and also specified for Datadog to send out an alert if data is not reported for more than 10 minutes. I followed the rest of the procedure, having Datadog send an email with the monitor triggers, modifying the message based on the type of alert and including the metric that caused the alert.

I included {{host.ip}} in the message but it did not replace it with the host ip in the email for some reason (bug?)

![Config1](https://i.imgur.com/3dEPdh4.png)
![Config2](https://i.imgur.com/dc5tVGf.png)
![Config3](https://i.imgur.com/VjzmQrY.png)



Here is the alert email I received:
![Alert](https://i.imgur.com/rKlXpNs.png)


I then scheduled the downtime from 7pm to 9am daily on M-F and one that silences it all day on Sat-Sun by clicking the schedule downtime button near the top.

Here were the emails I received after doing so:

![Down1](https://i.imgur.com/a5DQ5bq.png)
![Down2](https://i.imgur.com/a5DQ5bq.png)

*Note the UTC timezone.*


## Collecting APM Data
This was by far the most challenging part of this excercise for me, I had a lot of trouble getting it up and running. As mentioned, I used Vagrant to setup my enviroment and when I tried to install ddtrace onto my machine, the version of pip that was running was too old. After a lot of struggling I managed to update pip to a proper version and installed ddtrace. I should also mention that I had never encountered something like "middleware" before, and so when I first read the instructions that had stated "Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other." I, at first, did not really understand what that meant. As I dove deeper into this part of the challenge, I began to understand what middleware was exactly, and what ddtrace was doing. However, unfortunately, I forgot about that line that I read. Combined with my frustrations with the outdated version of pip, by the time I got to trying to collect the APM data, I had done exactly what was stated to be avoided and I ran both the middleware and ddtrace. When I realized what I did I immediatley corrected it, but still had some issues. I then discovered that the final issue was due to port forwarding being disabled on the VM. After correcting everything I finally got the APM data to start collecting.


In order to collect APM data, I used this Datadog article:  https://docs.datadoghq.com/tracing/setup/python/




Then, I integrated the middleware into the provided code by adding the following code snippets:

```python
import blinker as _

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)
```

I also changed port 5050 to 8080 because initially I could not get the traces to send to Datadog. Tweaking that and also forwading port 8080 from my VM to my host machine fixed the issue.

Here is the full code I used:

```python
from flask import Flask

import time
import blinker as _
import logging
import sys

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware




# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)
app = Flask(__name__)
traced_app = TraceMiddleware(app, tracer, service="my-flask-app", distributed_tracing=False)

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
    app.run(host='0.0.0.0', port='8080')
```


Here are the traces as recieved in Datadog:
![Traces](https://i.imgur.com/CJdUlI2.png)


Here is the timeboard that was created showing both APM and Infrastructure metrics:
![Timeboard](https://i.imgur.com/nRxfLFc.png)

Finally, here is the link to the dashboard:
https://app.datadoghq.com/dash/858307/apm-and-infrastructure?live=true&page=0&is_auto=false&from_ts=1531342584083&to_ts=1531346184083&tile_size=m

Bonus question:
From the datadog knowledge base, "A service is a set of processes that do the same job." Some examples include webapp, admin, and query. Also from the knowledge base, "A Resource is a particular action for a service." Some examples include, for a web application a URL like "/etc/datadog" or some SQL query like "SELECT * FROM table1234"



## Creative use for Datadog

A great fit that I can see for Datadog is in the manufacturing industry. My current employer maintains a manufacturing facility with many different CNC machines. It would be a great help to have insights on the analytics of the machines such as uptime, production speed and perhaps even more specific things like the vibration of the CNC machines. We may then tie in the different programs that are being run on the machines and be able to find some really useful information. For instance, one particular program may vibrate the CNC machine a lot more than usual, and shortly after the large vibrations occur, we can see that the machine malfunctions, receives an error, and goes down. This would save manfacturing environments a lot of money if they could quickly figure out the source of various problems in their machinery.


# Conclusion
Thank you for taking the time to review my submission. 

I learned a lot from completing this excercise. I had never used many of the tools that were required such as flask and vagrant, but by carefully reading the incredible Datadog documentation and googling a few things along the way I was able to successfully complete every task.

I think the toughest part of this excercise was getting the APM setup properly, but after some resiliance, the flask server was setup with the middleware and datadog was tracing away.


