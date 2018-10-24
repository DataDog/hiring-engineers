# Answers

I am presenting this technical exercise as if presenting Datadog to a client or student. As such, please use the table of contents to find specific answers. 

## Table of Contents: 
- [Datadog Overview](#datadog-overview)
- [Set Up the Environment](#set-up-the-environment)
- Collecting Metrics
  - Add tags to Agent config
  - Install a database
  - Create a custom Agent check
  - Change check's collection interval
  - Bonus Question


### Datadog Overview
In today’s modern application world, customer experience is what makes or breaks businesses. Application Performance can be the most critical factor to progressing or impeding customer experience. As such, your DevOps teams will do everything in their power to build highly performant apps. But, with their scope being bounded (rightfully so, per modern architecture practices), these teams will be unable to view and control all factors of overall performance. Datadog focuses on enabling your organization to: collect the wealth of data that’s already available from servers, VMs, container hosts, and the applications running on them, then visualize that data through customizable graphs to discover problems, and then set up alerts and monitors to be made aware of ongoing problems. Or to put it simply.. if your applications are like Infinity Stones, then Datadog enables you to become Thanos. 

![alt text](https://github.com/samirgandhi19/hiring-engineers/blob/samir-test/images/infinityGauntlet.gif)

Let’s discover just how Datadog helps you collect, visualize, and monitor your systems with an example together.
>Note: You can request a [free trial instance here](https://www.datadoghq.com/lpg6/) and much of our set up is covered nicely in the introductory wizard

Through this process, we will experience an introduction to the key areas of Datadog, from Agents that collect data, to dashboards to visualize the data, and alerts to monitor the data. 

##### Set Up the Environment
To start, we set up a fresh Ubuntu server with Vagrant and install the Datadog Agent:

```
vagrant init ubuntu/xenial64

vagrant up 

vagrant ssh
```

DD_API_KEY=<APIKey> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"

Immediately, you can see this host, alongside any other hosts, in your Datadog instance. Additionally, system-resource metrics have already begun to track: 
[insert hosts gif]
[insert host dashboard]


Now, this is fun, but we want more data! 


Let’s set up a MySQL db to show how easy it is to integrate with common applications, and some agent checks to show what it’s like to gather data from custom applications. 

First we install MySQL:
sudo apt-get install mysql-server
To capture metrics from MySQL we: 
1. set up a MySQL user for Datadog (mainly as a security precaution to limit what is accessible) with permissions from https://app.datadoghq.com/account/settings#integrations/mysql
2. make a config file at /etc/datadog-agent/conf.d/mysql.yaml with contents from: https://app.datadoghq.com/account/settings#integrations/mysql

Then, let’s create a simple Agent check. Ours will consist of two files: 
my_agent.py:
from checks import AgentCheck
from random import randint
class MyCheck(AgentCheck):
    def check(self, instance):
        self.gauge(instance['name'],randint(1,1000))
my_agent.yaml
init_config:
instances:
  - name: my_metric
    min_collection_interval: 45

Now, as soon as we restart the Datadog agent, the new configs will be picked up and metrics will start to be collected every 15-20 seconds by default. However, we adjusted our custom check to slow that specific collection down to every 45 seconds. This was done by adding a modifier line to the instance definition in the .yaml configuration. This simple agent check is self-contained, but it outlines where you could easily make calls out to your custom applications. This, coupled with all the available methods, shows that you have complete control over what metrics to collect and when. 

note: Regarding Bonus - The configuration for collection interval was done through the .yaml file rather than directly in the Python check. Also I assume there must be a way to configure global collection interval as well, but I did not see this in agent config file. 

A quick agent restart and "datadog-agent status” shows that our metrics are being captured. 
[insert ddagent gif]

Collecting data is nice, but the real value is provided by effectively visualizing the data. This is what enables organizations to make intelligent business decisions. 
[insert drucker quote]

To visualize our data, we could of course go into the UI and create dashboards, but that’s too easy! Let’s instead see what your DevOps teams will grow accustomed to - creating dashboards made up of multiple graphs via the Datadog API. 

I’ve pulled and manipulated one of the code snippets from our API documentation. And if we include our API key and App key, we can then POST this payload to instantly create the customized dashboard. Post to: https://api.datadoghq.com/api/v1/dash?api_key=ffc569bfd80d03e7c81eff56223e49bc&application_key=4cb2bc3be5a304ab9e2a32d9ee0e08f9d6b195af
{
      "graphs" : [{
      "title": "MySQL Performance Timeline",
      "definition": {
        "events": [],
        "requests": [
        {
          "q": "anomalies(avg:mysql.performance.cpu_time{tech-exercise,host:ubuntu-xenial}, 'basic', 2)",
          "type": "line",
          "conditional_formats": [],
          "aggregator": "avg"
        }
        ],
        "viz": "timeseries"
      }
},{    
      "title": "My Metric - Agent Check",
      "definition": {
        "events": [],
        "requests": [
            {
                "q": "avg:samir{host:ubuntu-xenial}",
                "type": "bars",
                "style": {
                  "palette": "cool",
                  "type": "solid",
                  "width": "normal"
                },
                "conditional_formats": [],
                "aggregator": "avg"
            }
        ],
        "viz": "timeseries",
        "autoscale": "True",
        "xaxis": {}
      }
},{
      "title": "My_Metric Rollup Over Last Hour",
      "definition": {
        "events": [],
        "viz": "timeseries",
        "requests": [{
            "q": "my_metric{host:ubuntu-xenial}.rollup(sum,3600)",
            "type": "bars",
            "style": {
                "palette": "grey",
                "type": "solid",
                "width": "normal"
            }
        }],
        "autoscale": "True"
      }  
}],
      "title" : "Tech Exercise Timeboard",
      "description" : "Showing off some great monitoring!",
      "read_only": "True"
}

[insert api_to_dashboard.gif]
[insert created dasboard image]

Voila, we have a dashboard with three unique graphs: 
1. CPU performance of our MySQL Server, tracked within bounds created by an intelligent anomaly algorithm
2. A broad of datapoints from our previously created custom metric “my_metric"
3. A full summation of all the “my_metric” entries over the last hour

It’s important to note that, although this dashboard was created via API, we can still interact with it as normal. For example, say a big spike just occurred and we want to isolate it, we can easily adjust the time window to show only the last five minutes. 
[]insert last_five gif]

If the anomaly is in fact something that requires action, you’ll want to let the appropriate groups know immediately. For this reason, you can easily annotate a graph and have a snapshot sent directly to the engineer’s email. 

[insert snapshot email]

Now we can see that from the “last hour” window down to the “last five minutes” window, the anomaly threshold has changed and updated. This is because the anomaly feature is actually an algorithm that continuously updates according to that specific metrics behavior. This intelligent detection algorithm is based on established statistical trends like 
“Seasonal Autoregressive Integrated Moving Average”. The feature will notice and pick up varying patterns like: service request lulls on the weekends or seasonal spikes. 

So, now that we have our data captured, and visualized, we were able to watch for outstanding scenarios and find issues faster. However, what’s even faster and much more accurate than us watching these screens (not to mention, way less annoying) is to create monitors that will alert us when certain thresholds are hit.

We will stick with the same theme and our custom metric to watch for a certain threshold, and then alert us as soon as that is hit. 
This is done via the “Monitors” section of the UI. We will set a Metric Monitor to watch the average of our metric, warn if over 500 and alert if over 800 and send us custom messages based on the scenario. This is accomplished by leveraging the message template variable that are available within the “Say what’s happening” field. Also, to be notified almost immediately after a spike, we will set the threshold to watch over the last five minutes. 
[insert my_metric alert gif]

And pretty soon.. we start getting the glorious automatic alert emails!
[insert alert email]

aaand pretty soon after you realize you have them alerting way too often.. like in the middle of actually solving the problem or.. the middle of the night.  we really don’t need this many emails telling us: 
[insert thatdbegreat]

Fortunately, we can schedule downtimes that make sense per each monitor. 
[insert monitor wizard]
[insert downtime summary]
[insert downtime email]

Infrastructure monitoring is a great start down the path of improving your overall performance. Application performance monitoring is the other half of the picture. Datadog provides a complete monitoring solutions with it’s final key piece: APM. 

To fully realize these values, we need to instrument Datadog’s APM solution on an application. 
in bon infrastructure that you don’t have to main realize Aristotle’s “the whole is greater than the sum of it’s parts”. 


*basically this exercise is an  

and one of the most critical factors to impact your customer’s experience today is the performance of your application. 

