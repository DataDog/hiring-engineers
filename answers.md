# Answers

I am presenting this technical exercise as if presenting Datadog to a client or student. As such, please use the table of contents to find specific answers. 

## Table of Contents: 
- [Datadog Overview](#datadog-overview)
- [Set Up the Environment](#set-up-the-environment)
- [Collecting Metrics](#collecting-metrics)
  - [Add tags to Agent Config](#add-tags-to-agent-config)
  - [Install a database](#first-we-install-mysql)
  - [Create a custom Agent check](#create-a-custom-agent-check)
  - [Change check's collection interval](#adjust-collection-interval-and-bonus)
  - [Bonus Question - Collection Interval](#adjust-collection-interval-and-bonus)
 - [Visualizing Data](#visualizing-data)
  - [Create Timeboard via API](#create-timeboard-via-api)
  - [API payload for Timeboard](#payload)
  - [Adjust Timeboard View and Snapshot](#adjust-timeboard-and-snapshot)
  - [Bonus - Anomaly](#bonus-anomaly)
- [Monitoring Data](#monitoring-data)
  - [Create Metric Monitor](#create-metric-monitor)
  - [Customize Monitor's Notification Messages](#customize-alert-messages)
  - [Bonus - Downtimes](#bonus-downtimes)
- [Application Performance Monitoring](#application-performance-monitoring)
  -[Trace an Application](#trace-an-application)
  -[Bonus - Service vs Resource](#bonus-services-and-resources)
  -[Dashboard with APM and Infrastructure Metrics](#dashboard-with-apm-and-infrastructure-metrics)
- [Final Question](#final-question)


### Datadog Overview
In today’s modern application world, customer experience is what makes or breaks businesses. Application Performance can be the most critical factor to progressing or impeding customer experience. As such, your DevOps teams will do everything in their power to build highly performant apps. But, with their scope being bounded (rightfully so, per modern architecture practices), these teams will be unable to view and control all factors of overall performance. Datadog focuses on enabling your organization to: collect the wealth of data that’s already available from servers, VMs, container hosts, and the applications running on them, then visualize that data through customizable graphs to discover problems, and then set up alerts and monitors to be made aware of ongoing problems. 
  
Or to put it simply.. if your applications are like Infinity Stones, then Datadog enables you to become Thanos for monitoring. 

![alt text](/images/infinityGauntlet.gif "the first thing we all would do with powers")

Let’s discover just how Datadog helps you collect, visualize, and monitor your systems with an example together.

Through this process, we will be introduces to the key areas of Datadog, from Agents that collect data, to dashboards that visualize the data, and alerts that monitor the data. 

To start, we request a trial instance of Data dog and set up a fresh Ubuntu server with Vagrant then install the Datadog Agent:

>Note: You can request a [free trial instance here](https://www.datadoghq.com/lpg6/) and much of our set up is covered nicely in the introductory wizard

#### Set Up the Environment
```
vagrant init ubuntu/xenial64

vagrant up 

vagrant ssh

DD_API_KEY=<APIKey> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

Immediately, you can see this host alongside any other hosts in your Datadog instance. Additionally, system-resource metrics have already begun to track. To help isolate and organize all of your metrics and scenarios, datadog supports tagging in many areas. Here we add tags in key:value format to the new agent so we can easily reference it later: 
###### Add tags to Agent config
![alt text](/images/hosts_gif.gif "")
![alt text](/images/ubuntu_host_tag.png "filter by tag for sinlge host")

#### Collecting Metrics
Now, this is fun, but we want more data! 

Let’s set up a MySQL db to show how easy it is to integrate with common applications, and some agent checks to show what it’s like to gather data from custom applications. 

![alt text](/images/collect_all_the_datas.jpg)

##### First we install MySQL:
sudo apt-get install mysql-server
To capture metrics from MySQL we: 
1. set up a MySQL user for Datadog (mainly as a security precaution to limit what is accessible) with permissions from https://app.datadoghq.com/account/settings#integrations/mysql
2. make a config file at /etc/datadog-agent/conf.d/mysql.yaml with contents from: https://app.datadoghq.com/account/settings#integrations/mysql

###### Create a custom Agent check
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
###### Adjust collection interval and bonus
Now, as soon as we restart the Datadog agent, the new configs will be picked up and metrics will start to be collected every 15-20 seconds by default. However, we adjusted our custom check to slow that specific collection down to every 45 seconds. This was done by adding a modifier line to the instance definition in the .yaml configuration. This simple agent check is self-contained, but it outlines where you could easily make calls out to your custom applications. This, coupled with all the available methods, shows that you have complete control over what metrics to collect and when. 

note: Regarding Bonus - The configuration for collection interval was done through the .yaml file rather than directly in the Python check. Also I assume there must be a way to configure global collection interval as well, but I did not see this in agent config file. 

A quick agent restart and `datadog-agent status` shows that our configuration is successful and our metrics are being captured. 
![alt-text](images/ddagent_status_metrics_terminal.gif)

### Visualizing Data
Collecting data is nice, but the real value is provided by effectively visualizing the data. This is what enables organizations to make intelligent business decisions. 
![alt-text](images/drucker_quote.png)

To visualize our data, we could of course go into the UI and create dashboards, but that’s too easy! Let’s instead see what your DevOps teams will grow accustomed to - creating dashboards made up of multiple graphs via the Datadog API. 

###### Create Timeboard via API
I’ve pulled and manipulated one of the code snippets from our API documentation. And if we include our API key and App key, we can then POST this payload to instantly create the customized dashboard. Post to: https://api.datadoghq.com/api/v1/dash?api_key=api_key&application_key=app_key
###### Payload
```
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
```

![alt-text](/images/api_to_dashboard.gif)
![alt-text](/images/create_dashboard.png)

Voila, we have a dashboard with three unique graphs: 
1. CPU performance of our MySQL Server, tracked within bounds created by an intelligent anomaly algorithm
2. A broad of datapoints from our previously created custom metric “my_metric"
3. A full summation of all the “my_metric” entries over the last hour

###### Adjust Timeboard and Snapshot
It’s important to note that although this dashboard was created via API, we can still interact with it as normal. For example, say a big spike just occurred and we want to isolate it, we can quickly adjust the time window to show only the last five minutes. 
![alit-text](/images/last_five_mins.gif)

If the anomaly is in fact something that requires action, you’ll want to let the appropriate groups know immediately. For this reason, you can annotate graphs and have snapshots sent directly to engineers. 

![alt-text](/images/alert_snapshot_email.png)

###### Bonus-Anomaly
Now we can see that from the “last hour” window down to the “last five minutes” window, the anomaly threshold has changed and updated. This is because the anomaly feature is actually an algorithm that continuously updates according to that specific metrics behavior. This intelligent detection algorithm is based on established statistical trends like 
“Seasonal Autoregressive Integrated Moving Average”. The feature will notice and pick up varying patterns like: service request lulls on the weekends or seasonal spikes. 

### Monitoring Data
Now that we have our data captured and visualized, we are able to *watch* for outstanding scenarios and find issues faster. However, what is even faster and much more efficient than us watching these screens is to create monitors that will alert us when certain thresholds are hit (way less annoying too :thumbsup:).

To show this, let's stick with the same theme and our custom metric to monitor for a certain threshold, and then alert us as soon as it is triggered. 

###### Create a Metric Monitor
###### Customize Alert Messages
This is done via the “Monitors” section of the UI. We will set a Metric Monitor to watch the average of our metric, *warn if over 500* and *alert if over 800* and *send us custom messages based on the scenario*. This is accomplished by leveraging the message template variable that are available within the “Say what’s happening” field. Also, to be notified almost immediately after a spike, we will set the *threshold to watch over the last five minutes*. 
![alt-text](/images/my_metric_monitor_alert.gif)

And pretty soon.. we start getting the glorious automatic alert emails!
![alt-text](/images/alert_snapshot_email.png)

aaand pretty soon after you realize you have them alerting way too often.. like in the middle of actually solving the problem or.. the middle of the night.  we really don’t need this many emails telling us: 

![alt-text](/images/thatdbegreat.jpg)

##### Bonus-Downtimes
Fortunately, we can schedule downtimes that make sense per each monitor. 
![alt-text](/images/downtime_wizard_screenshot.png) 
![alt-text](/images/downtime_summary_screenshot.png)
![alt-text](/images/downtime_email.png)

### Application Performance Monitoring
Infrastructure monitoring is a great start down the path of improving your overall performance. Application performance monitoring is the other half of the picture. Datadog completes your full monitoring solution with it’s final key piece: APM. 
###### Trace an Application
To fully realize these values, we need to instrument Datadog’s APM solution on an application. 
We will use a simple Python app to post data to our MySQL server. find this app's code at: https://github.com/samirgandhi19/hiring-engineers/blob/samir-test/code/flaskapp.py

Setting up a trace on this app is as easy as any of the other steps so far, we simple start our app with:
```
ddtrace-run python app.py
```

Because this app interacts with our MySQL db, you will see two services in the APM GUI and can even follow traces to see just how long every part of each request takes.
![alt-text](/images/apm_trace_list.png)

###### Bonus Services and Resources
Additionally, in the "Trace Search" view you can see the services (a set of processes that work toward the same goal) that are being traced, and the resources (specific actions/endpoints that are part of the service) that are being requested from those services.

![alt-text](/images/apim_trace_search.png)

##### Dashboard with APM and Infrastructure Metrics
And the best part.. we can add metrics from our service into our previously created timeboard as if it was any of our other agents or integrations.

![alt-text](/images/final_dashboard.png)

And now, after showing how to collect metrics, then visualize them, and finally, how to monitor those metric, whether from your infrastructure or applications.. we are able to acheive the ultimate goal.. restore balance by eliminating half the population with a snap!.. no no, the real ultimate goal: seeing all of our data, from all of our systems in one holistic view so that we can truly see bottlenecks, understand trends, and make performance enhancing decisions. 

### Final Question
This whole process helps us realize how powerful it is to have all this data at our fingertips. Going back to customer experience being critical to our business and performance making or breaking that experience.. Datadog's solution for overall monitoring and analysis gives your organization a fighting chance! This makes me think back to customer's I have worked with in the past that I *know* could have benefitted tremendously. One in particular is a state lottery. They came to us with a challenge: their systems could not handle tremendous spikes in traffic. When the lottery jackpot valuation would reach a certain amount, it would generate so much public attention and traffic as a result that it would crash their systems. Regardless of the fact they prepared with tests and  additional infrastructure. So, think about it, not only did their systems crash, but it would only happen at the *worst* possible point. At the time, I showed them how caching responses intelligently would dramatically reduce backend load. However, after learning more about Datadog, I see this challenge in a new light. How cool would it be to go back to that system, and put in agents, integrations, and traces.. we could get so much insight into that increased load. Insights like: 1. how does additional load impact the performance of the systems, 2. what is the critical threshold that is a sign for crash 3. what is the exact piece of the system that may be a bottleneck 4. and then, going above and beyond into actual business cases, how does the size of a jackpot correllate to additional traffic they see. With this type of information, the Lottery group could be so much more efficient in their infrastructure costs! Perhaps they move to an auto-scale/scalable infrastructure. If not that, then at least they would have so much more insight to just how much infrastructure they need, and when! 

This use case is extremely relevant to that organization, but I believe these same questions and insights could be applied to *any* organization that deals with varying traffic, seasonal peaks, or spikes in load. Retail stores of course (Black Friday), Government groups during elections, first responders during emergencies, marketing organizations and TV stations playing ads.. the list goes on and on. NICE!
