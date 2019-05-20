Introduction
------------
As part of the hiring process for a role with DataDog - as a Technical Account Manager - I was asked to complete this Solutions Engineer technical exercise.
Hopefully what follows will give you a quick glimpse into my approach to technical problems - as well as my presentation and documentation style.


Prerequisites - Setup the environment
-------------------------------------

The technical exercise instructions recommend starting with a blank canvas - and using a fresh host and OS - which is a sensible approach and provides a level playing field for comparison between candidate submissions.

I chose to fire up a new Vagrant VM on my development Macbook Pro - and use the bento box image to start an Ubuntu 16.04 OS - via the command:    

```
vagrant init bento/ubuntu-16.04

```

![Vagrant initiation](https://i.imgur.com/ORNli1f.png) 


The next step is to sign up for a new DataDog account - https://www.datadoghq.com/ - specifying the "DataDog Recruiting Candidate" organisation - so I could start collecting the metrics needed for this exercise.

Thankfully the agent installation is super simple - and when opening a new account - the first screens presented are those to guide you through the process for your specific situation and even provide the exact commands you need to run including the required API Key.

![Agent install screens](https://i.imgur.com/7IwQxAa.png) 

Collecting Metrics
-------------------------------------
 
Here we have the Host Map screen within my new DataDog account - showing the details of my vagrant box - as well as some custom tags set within the datadog.yaml file - using the syntax:

```
tags:
    - env:macbook_pro_15
    - role:mysql_database
```

The ability to add custom tags and identify different elements being monitored in a way that is meaningful to you and your team / organisation - opens up a whole world of additional options over more traditional monitoring tools.

It means you are the master of how your infrastructure is identified - rather than being dictated to from a small set of auto-assigned names.   This in turn means that when there is a problem - the returned information and alerts about it - can be sorted, filtered and grouped in ways that demonstrate much more context for those trying to understand the situation.

![Host map details](https://i.imgur.com/ne1ISxO.png) 

Next the exercise requests an installation of a database - in my case I chose MySql - and the corresponding DataDog integration.

![mySql installation](https://i.imgur.com/CXuV7hq.png) 

Once again - DataDog makes the installation of the MySQL integration very straightforward - providing detailed instructions and specific commands to be run in order to setup each potential option and metric.

![mySql installation](https://i.imgur.com/xEfMdBn.png) 

After creating a new database (datadogdb) and a new user to be given access to it (datadog) - one needs to set the required permissions on the main db - as well as on the performance_schema - in order to extract metrics from it and pull them into DataDog.

![mySql permissions](https://i.imgur.com/lhKVDBj.png)

Once completed - these steps enable the included out of the box MySQL reports and dashboards within DataDog.  The huge advantage with these views and reports being included by DataDog - is the amount of time saved by not having to create your own.   Anyone who has run some of the other traditional monitoring tools will know the amount of time that used to need investing in even the basic views.  Thankfully the below required no manual time to produce or configure.

![mySql overview](https://i.imgur.com/B6TQsms.png)

#### Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000

Despite the extensive number of out of the box integrations - there may well be metrics that need to be collected from unique systems and require a custom check to be built.  This is catered for via Custom Agent Checks - https://docs.datadoghq.com/developers/write_agent_check/ - via the creation of a check file and a configuration file - which the DataDog agent can use together to gather the required data from the system.

I created a check within /etc/datadog-agent/checks.d/ - called mycheck.py

```
from checks import AgentCheck
from random import randint

class my_metricCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(0, 1000))
```

and a corresponding configuration file in /etc/datadog-agent/conf.d/ - called (a matching) mycheck.yaml

```
init_config:

instances:
    [{}]
```

These two files working together - after restarting the datadog-agent service - began collecting a metric named my_metric with a random integer value - as shown below in the datadog metric explorer:

![my_metric check](https://i.imgur.com/GoSPhYL.png)

#### Change your check's collection interval so that it only submits the metric once every 45 seconds.

With the configuration file empty - the check just created - is using the default min_collection_interval of 15 seconds.

By altering the mycheck.yaml file and adding the following - we can change the collection interval to 45 seconds:

```
init_config:

instances:
    [{
        min_collection_interval: 45
     }]
```


#### Bonus Question Can you change the collection interval without modifying the Python check file you created?

It is possible to alter the value for min_collection_interval within the configuration file of any check, whether created by DD or by yourself as a custom check - from within the *.yaml* as we did for the mycheck.yaml file above.  The benefit of always keeping configuration like this within a configuration file - rather than in the check file - is that when time comes to verify or change configuration values - they are all in one place rather than scattered amongst the check code itself.

Visualising Data:
-------------------------------------

Utilize the Datadog API to create a Timeboard that contains:

- Your custom metric scoped over your host.
- Any metric from the Integration on your Database with the anomaly function applied.
- Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Since DataDog provide a set of very helpful templates for API interaction if using Postman - that is what I used here.  Adding the templates to a DataDog collection was as simple as downloading them, importing them to Postman and then adding the right variables for this current environment (DataDog API Key, App key and region). * *see my note re: these values in Notes/AOB at the end of this document*.

![Postman setup](https://i.imgur.com/ec7wSiZ.png) 


In order to create the required dashboard - I used the following JSON body:

```
{
    "title": "Now Thats What I call a Dashboard",
    "widgets": [
        {
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                     "q": "avg:my_metric{*}"
                    }
                ],
                "title": "My Metric timeseries"
            }
        }
         , 
          {
            "definition": {
                "type": "timeseries",
                "requests": [ 
                	{
                		"q": "anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 2)"
                	}
                	],
              "title": "My MySQL Anomaly Graph" 
    		}
          }
    	,
		{
            "definition": {
                "type": "timeseries",
                "requests": [
                    {
                  "q": "my_metric{*}.rollup(sum,100)"
                    }
                ],
                "title": "My Metric Rollup Function"
            }
		}
    ],
    "layout_type": "ordered",
    "description": "Now Thats What I call a Dashboard - Vol 1 - this is a set of visualisations for some the key metrics related to my DataDog technical exericse.  This includes a timeseries for the randomly generated values of My Metric, an anomoly function laid over values from the MySQL installation I am using and rollup function applied to My Metric.",
    "is_read_only": true,
    "template_variables": [
        {
            "name": "host1",
            "prefix": "host",
            "default": "myhost"
        }
    ]
}

```

Which gave a response as shown below:

![Postman response to Dashboard create](https://i.imgur.com/2XzxoZO.png)


Which in turn - created the below Dashboard within the DD portal:

![My API created Dashboard](https://i.imgur.com/z8lCnOm.png)

Setting the timeframe for the past 5 minutes - and then taking a snapshot to send to myself - but it could easily have been a colleague / team member who I needed to look at a metric I had spotted:

![My Dashboard over 5 mins](https://i.imgur.com/AkTgXnz.png)

![My dashboard snapshot](https://i.imgur.com/NnKPwUg.png)

#### Bonus Question: What is the Anomaly graph displaying

![My MySQL Anomaly graph](https://i.imgur.com/DTx15M3.png)

Anomaly detection is intended to highlight when a measured metric has reached a value which is outside of expectation - not just for a defined range - but also taking into consideration detectable repeating patterns in the data - such as daily, weekly and seasonal trends.

This is incredibly useful for a support function that is trying to be alerted to issues that need attention - and don't want to be alerted to "expected" behaviour which happens on a schedule not usually catered for by traditonal monitoring tools and basic threshold alerting.

For example - peaks in traffic associated with online video viewing - where the regular patterns of usage can see values 1000's of times higher in an evening than a daytime - but are still valid and ok.

Here I have measured the cumulative CPU time elapsed for the MySQL processes running - and then asked DataDog to analyse the data and provide an "expected range" - then highlight values which are "anomalies" to that expectation.  In a real situation with a much larger body of historical data, the anomaly monitoring would be able to overlay a much more informed set of expected ranges.


Monitoring Data
-------------------------------------

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

- Warning threshold of 500
- Alerting threshold of 800
- And also ensure that it will notify you if there is No Data for this query over the past 10m.

Using the DataDog UI - and chosing to create a new Monitor from the menu on the left - I configured the required thresholds as shown below:

![My Metric Monitor config](https://i.imgur.com/L7Ek84P.png)

Which - when tested - produced the following email notification:

![Monitor Alert Email](https://i.imgur.com/dl4JemH.png)

The configuration requested included thresholds for Alerting, Warning and for a lack of data over the last 10mins - each of which has a different notification message written - and which DataDog will pick when triggered.

#### Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

- One that silences it from 7pm to 9am daily on M-F

![My_Metric Alerts silenced](https://i.imgur.com/pBrRca1.png)

- And one that silences it all day on Sat-Sun.

![My Metric Alerts silenced - weekends](https://i.imgur.com/levJUBE.png)

- email notifications for both new schedules:

![Weekday silencing](https://i.imgur.com/zLfgHfJ.png)

![Weekend silencing](https://i.imgur.com/BH10bvY.png)


Collecting APM Data
-------------------------------------

Given the provided Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution.

The first step - was to enable the APM logging settings within the *datadog.yaml* file - found in */etc/datadog-agent*.  Thanks to the extensive comments in the file - finding the section related to APM was simple - and with some removed comments - should give:

```
# Trace Agent  Specific Settings
#
apm_config:
# Whether or not the APM Agent should run
  enable: true
```

Next up was installing PIP, Flask, Python (and other pre-requisites as needed) - plus reading up on the deeper usage of the Middleware and the DDTRace Python client - within the main DataDog docs as well as here -> pypi.datadoghq.com/trace/docs 

Building on the back of the provided Flask app - and adding the required entries to use DataDog's APM tracing - gave a result like the one below (and included as a file at the bottom of this section):

```
vagrant@vagrant:/home$ diff -urN original.py new.py
--- original.py	2019-05-20 13:25:10.349203003 +0000
+++ new.py	2019-05-20 13:30:04.852381002 +0000
@@ -1,7 +1,12 @@
+
 from flask import Flask
 import logging
 import sys
 
+from ddtrace import tracer
+from ddtrace.contrib.flask import TraceMiddleware
+
+
 # Have flask use stdout as the logger
 main_logger = logging.getLogger()
 main_logger.setLevel(logging.DEBUG)
@@ -12,6 +17,10 @@
 
 app = Flask(__name__)
 
+# Register the flask app with the ddtrace flask middleware and provide a name for the service within APM
+
+traced_app = TraceMiddleware(app, tracer, service="new-py-app", distributed_tracing=False)
+
 @app.route('/')
 def api_entry():
     return 'Entrypoint to the Application'
``` 
 
![new.py APM trace](https://i.imgur.com/gbTKJT0.png)

Instrumented app *new.py* can be found here

https://pastebin.com/FJuefiPg


This new Flask app - when run via command - *ddtrace-run python new.py* - began the application running on port 5050 ready to respond.

In order to have some data to analyse in APM - it was necessary to target this app with some traffic - using a recurring trace request once a second.

After being allowed to build up some history - DataDog APM was able to begin providing Application Performance Monitoring stats and recommended monitors - as shown below for latency and error count in particular:

![new.py APM widgets](https://i.imgur.com/9QSuM14.png)

These graph outputs can then be incorporated in Dashboards and Timeboards - alongside other metrics and information about the estate being monitored - as seen here:

![Now Thats What I call a Dashboard](https://i.imgur.com/iDbv7jR.png)

After some investigation - it became clear that the Timeboard that I had created above - was not publicly shareable.  Instead I had to create a Screenboard in order to share - and in turn - I also had to summarise the APM queries and metrics - rather than simply adding single graphs.

Public URL for Board with Infrastructure and APM information - can be found here - https://p.datadoghq.com/sb/8efr12g1plm39skj-21940aae301129828f1aff2e4a77e0f3

Screenshot of my DataDog Exercise Screenboard

![Public Shareable Screenboard](https://i.imgur.com/IqqsalF.png)



#### Bonus Question: What is the difference between a Service and a Resource?

DataDog Docs confirms that, in the context of APM Tracing and Visualisation, there are four levels of granularity: services, resources, traces, and spans level.

A service is a set of processes that do the same job. For instance, a simple web application may consist of two services - A single webapp service and a single database service.  APM automatically assigns names to services.

Whereas - a resource is a particular action for a service - for example a canonical URL, such as /user/home or a handler function like web.user.home (often referred to as “routes” in MVC frameworks).  Resources should be grouped together under a canonical name - and again APM will automatically assign names to resources.


Final Question
-------------------------------------
Datadog has been used in a lot of creative ways in the past.  Is there anything creative you would use DataDog for?

There are lots of different aspects of DataDog that could be put to use in weird and wonderful ways - but the one that jumps out at me immediately - is the ability to gather information from lots of remote sources, store it centrally and offer lots of different ways to view that information, on many different endpoints.

I am the Chairman of a Village Hall Charity here in Yorkshire, UK - and one of our main responsibilities is the upkeep, maintenance and organisation around the Village Hall building itself.

![Kilnwick Village Hall](https://i.imgur.com/pB646Wm.jpg)

The building's main purpose is as a community hub - and can be rented for the day at a very subsidised rate to allow those who live in and around the village - to organise and host events.  We have weekly clubs and gatherings for the local youth club, the old-folks club, exercise classes, yoga classes and monthly pub gatherings.

As there is no one permanently on site at the hall - there is always a worry that the variety of electrically powered items we have - can be left powered on and cause problems.  These include: 

- heating system - which uses lightbulbs to indicate status (On / Off) - and pose a serious danger if left on unattended

- storage areas - with lights than can easily be left on - and cost significant amounts for a non-profit charity

- kitchen area - with boilers, cookers and appliances which can be left on and present a fire hazard

![Inside Hall](https://i.imgur.com/p0lGCBw.jpg)
![Heating](https://i.imgur.com/4pnzQTa.jpg) 
![Inside kitchen](https://i.imgur.com/wVwvsAC.jpg)

In addition - there is an emergency defibrillator (yellow box on wall in first picture) - which is powered from a socket inside the hall - and needs to be powered at all times in order to stay usable, should the emergency services require it.

Those of us on the Village Hall committee are responsible for ensuring all of the above is maintained - however our availability differs greatly across the time of day and days of the week.  In addition - there are varied preferences for contact via lots of different mediums (text, email, whatsapp) - and so keeping track of who has been notified is an issue.

Step up DataDog :)

I think that the first step would be replacing the heating and general lightbulbs - with IoT connected ones - plus adding IoT connections to the plug sockets for the appliances and the defibrillator - with all of them reporting back into Home Assistant.

Then - thanks to DataDog's pre-existing integration with Home Assistant - I would be able to begin reporting on the status of each appliance and lightbulb and heating component - with the DataDog portal.

Being able to then configure alerts on the values detected - around configurable schedules - and know what alert had been sent when - would be hugely helpful to the committee.

Once that was in place - and showing its value to the Village Hall - I think that the next step of a IoT connected smart electricty meter would become an obvious and useful addition.


Final Summary
-------------------------------------

I hope that the above document proves as interesting to those reviewing it as it has been for me to create.  I have learned about a number of additional capabilities within DataDog that I wasn't aware of before - and which I will actively use in future - as they seem so useful for people with the regular struggles that Technology Operations teams tend to have.

I wish to thank you for reading this far - and hope to have the opportunity to present to more of the Technical Account Management team in person - some time in the near future.

Many Thanks

Lee Beddows




Notes / AOB
-------------------------------------

While working with the documentation around APIs - found here - https://docs.datadoghq.com/developers/guide/using-postman-with-datadog-apis/ - there is an instruction within the environment setup, which I found did not match with the downloaded Postman templates.
The instruction advises:
```
In the table, add the variables datadog_api_key and datadog_application_key.
```

However - the available Postman templates actually expect: 
```
{{dd_api_key}} and {{dd_app_key}}
```
Once changed - all worked as required - but it would be useful for those starting out - to have the docs updated to match expected values. 
