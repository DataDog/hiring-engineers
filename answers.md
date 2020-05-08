# Datadog Hiring Exercise
# Tim Cronin
# Submitted: May 8, 2020




## Candidate Background

Tim Cronin is a technology enthusiast, well-versed business consultant, and hopeful future Datadog Sales Engineer. Tim has spent time in the worlds of finance and media technology, having worked at both CBS and Jefferies Group. Most recently, Tim has helped grow a small software development company, Totem Block, which has a core focus on blockchain applications and use cases. Not all work and no play, however, Tim is an avid waterman, having learned to surf the beaches of New Jersey and Long Island at a young age. When not in the icy waters of the Northeast, Tim loves to spend time with friends and family, watching epic 1980’s cult action movies (think anything Patrick Swayze), and traveling the world to see new cultures and meet new people.





## Overview

In this document, we will be walking through how to get started on Datadog’s incredibly comprehensive platform. In this introduction to Datadog, users will be able to set up the appropriate environment to leverage Datadog’s toolkit and features, collect metrics from an integrated database, visualize and monitor the data, as well as collect APM data.

In brief, we will cover:

1. Collecting Metrics

Using Datadog to collect metrics from our specific system

2. Visualizing Data

Once collected, how can we create case-needed visualizations to suit our requirements or inform us further?
3. Monitoring Data

Once appropriately visualized, what tools can we use so that we can be alerted for regularities or anomalies in the data?

4. APM Data

After we have successfully collected, visualized, and monitored our data, how can we evaluate our application’s performance and stability? 

In case any of this is a little foreign to you, or in the event it sounds a bit technical, it might be helpful to watch this quick two minute introductory video explaining Datadog’s capabilities, some of which we will cover in this document: https://www.youtube.com/watch?v=YHmCQ5GVeTk

**Please note: each section of this manual will have additional links to more in depth documentation you can refer to. This Datadog documentation is incredibly useful to understand the “how?” behind the “why?” as we start leveraging the platform. It is encouraged to read the documentation thoroughly in each section to have a complete understanding of what we are accomplishing.





## Setting up the Environment

Now that I’ve detailed all that we’ll cover and you’ve familiarized yourself a bit more with Datadog’s capabilities, I think we’re ready to get started. 

The first step is to set up the proper environment, so that the Datadog Agent runs effectively on your system. The Agent is software that runs on your host and collects metrics, sending them to Datadog, where you can evaluate and monitor the data however you like.

So as to not run into any dependency issues, it’s best to spin up a fresh linux VM via Vagrant. If this is new to you, please refer to this link for documentation on getting set up with Vagrant: https://www.vagrantup.com/intro/getting-started/

Once you’ve successfully set up a Vagrant VM, sign up for Datadog using “Datadog Recruiting Candidate” in the “Company” field. 

After you’ve logged in, it’s time to get the Agent reporting metrics from your local machine. To do this, we have to get to the “Agent 7 Installation Instructions” page for your respective system. Here is the link to the respective pages we need to access: https://app.datadoghq.com/account/settings#agent/overview

In my case, below is an image for the agent installation page for Mac

![Agent Installation Page](/images/api_page.png)

All you have to do is copy and paste the DD_AGENT_MAJOR_VERSION=7 command line into your terminal.

Once the agent finishes loading in terminal, the below message will appear about your agent running properly, and continue to run in the background and submit metrics to Datadog:

![Agent Running Properly](/images/agent_running.png)

To make sure there are no errors at this point, you can also launch the GUI in your terminal, which will provide you with some further Agent, System, and Host Info:

![GUI](/images/gui_metrics.png)

If you have successfully completed the steps above, congratulations! The Datadog Agent is now running and collecting metrics from your local machine. Now that we have successfully run the agent, it’s time to tell the Agent what class of metrics we want to collect.





## Collecting Metrics

Now that the Agent is running on your machine, and collecting metrics, one of the obvious questions that stands out is how can we organize the data that’s running from the host to the Datadog platform? Tags are a way of adding dimensions to metrics, so they can be filtered, aggregated, and compared in Datadog visualizations. Using tags enables you to observe aggregate performance across a number of hosts and (optionally) narrow the set further based on specific elements. In summary, tagging is a method to observe aggregate data points.

Typically, it’s helpful to look at containers, VMs, and cloud infrastructure at the “service” level in aggregate. For example, it’s more helpful to look at PU usage across a collection of hosts that represents a service, rather than CPU usage for server A or server B separately. Containers and cloud environments regularly churn through hosts, so it is critical to tag these to allow for aggregation of the metrics you’re getting.




### Tagging exercise:

To demonstrate what we just learned about the utility behind tagging, we will now add tags in the Agent config file on your machine so that we can see updated tags on the Host Map page in Datadog.

Using a source-code editor of your choice, access the “Agent config” file within the Datadog-Agent folder. In that file, you can adjust the “tags” that are listed in the script. As illustrated in my screenshot below, I adjusted the tags to read in name, env, and role for simple organization:

![Tags Config File](/images/tags_config.png)

NOTE: Once saved, you must restart the agent for these tags to appear on your Host Map in Datadog. This is a common error. Please restart the agent now. Further, it might take a few minutes to load on the Host Map. (Here is a list of agent commands that will prove useful as well: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6v7)

Once the agent is restarted, you can reload your Host Map and see the new tags you’ve created:

![Tags Host Map](/images/tags_host.png)


For further documentation on tagging, please refer to his link: https://docs.datadoghq.com/tagging/






### Postgres Integration:

One of the incredible features of Datadog is that there are a number of integrations that allow us to collect certain metrics on the platform. For this demonstration, we are using what are called agent-based integrations, which we can install using the Datadog Agent itself, with the simple need to adjust the “class,” so that we can stipulate which metrics we want to collect. In this instance, we can manipulate the “class” titled “checks” (written in Python) to define our metrics.

Before we can create custom Agent checks, however, we must first successfully install a database, and the respective Datadog integration for that database. Suggested integrations for this step are MongoDB, MySQL, and PostgreSQL. For the purposes of this demonstration, let’s download PostgreSQL to your machine: https://www.postgresql.org/download/

Once you’ve successfully installed PostgreSQL, it’s time to install the corresponding Datadog integration. Fortunately, as is probably clear from our previous installation instructions, Datadog has made it incredibly easy and user friendly. Simply access the Integrations page in Datadog (https://app.datadoghq.com/account/settings#integrations), and click the “+Available” button below its title. 

Now that the integration is installed, we can now look to create a custom Agent check.




### Custom Agent Check Exercise:

To get started with the PostgreSQL integration, create a read-only datadog user with proper access to your PostgreSQL server. Start psql on your PostgreSQL database. Next, run:


![Postgres 1](/images/postgres_integration1.png)



To verify the permissions are correct, run the following command:



![Postgres 2](/images/postgres_integration2.png)



Now, for the purposes of this demonstration, let’s create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

To do this, we must first create the custom Agent check configuration file (my_metric.yaml) and define or add the needed parameters:



![Custom Agent Check Parameters](/images/collection_interval.png)



If you notice, by adjusting the min_collection_interval instance, you can now change your check’s collection interval so that it only submits the metric once every 45 seconds (the default is every 15 seconds).

Now, we must create a python script called my_metric.py that submits a metric with a random value between 0 and 1000. You can use the script below to do this:



![Custom Agent Check my_metric](/images/my_metric.png)



Once this is executed, saved, and the agent is restarted, you can now access the “Metrics” tab in Datadog to make sure it is properly reporting with the parameters you defined.

Custom checks are well suited to collect metrics from custom applications or unique systems. However, if you are trying to collect metrics from a generally available application, public service, or open source project, it is recommended that you create a full-fledged Agent Integration.  

For further documentation on writing custom Agent checks, please refer to these links: https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7
https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7#overview

Also, here is a great blog to help understand key metrics for PostgreSQL monitoring: https://www.datadoghq.com/blog/postgresql-monitoring/






## Visualizing Data

Now that we have collected our metrics, we can tackle how to visualize them accordingly. In my opinion, this is the most incredible element of the Datadog platform. There are endless possibilities in how you want to specifically visualize your metrics, and for the purposes of our walkthrough, we will simplify it to creating a fairly straightforward Timeboard. 

Timeboards have automatic layouts, and represent a single point in time – either fixed or real-time – across the entire dashboard. They are commonly used for troubleshooting, correlation, and general data exploration. 


Our next activity will be to leverage the Datadog API to create a Timeboard that contains:

	Our custom metric scoped over our host
	Any metric from the Integration on our Database with the anomaly function applied
	Our custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Scoping a metric over a host is a simple and sound way to see what’s happening on a specific host. Further, you can apply anomaly detection to your metrics, which will allow you to see (or be alerted to) anomalies appearing in the data collection. This can be an extremely useful tool for troubleshooting and real-time monitoring. Finally, you can generate custom functions to assist in illustrating the most fundamental visualizations to inspect. In this example, the rollup is for one hour of my_metric.py collection, which could be useful if you have less of an interest in real-time monitoring and more in overall system health and functionality. The rollup, essentially, details the generalist trends of the collection. 

To accomplish the tasks listed above, we must create a new script file titled timeboard.py in the “scripts” folder within Datadog-Agent. The following three images are the script that you can use to get to the next section:

![Timeboard 1](/images/timeboard_script1.png)


![Timeboard 2](/images/timeboard_script2.png)


![Timeboard 3](/images/timeboard_script3.png)


Once you have successfully saved and executed the script, you must restart the agent. In doing so, you will now have created the custom Timeboard and its corresponding graphs, accessible in the “Dashboards” tab in Datadog.

Here’s how the graphs should look:



![Timeboard Visualizations](/images/se_dashboard.png)



As another fun experiment, let’s now set the Timeboard’s timeframe to the past 5 minutes, and use the @ notation to send it to yourself! Take a look at the below screen grab to see how to do this:



![Timeboard Visualizations Last 5 Mins](/images/Last_5_mins.png)



The final highlight I want to make is with the anomaly graph. As I alluded to before we executed the script, the anomaly graph is unique because it is analyzing new behavior as it compares to past behavior, thus providing an anomaly monitor alert when something changes from its previous pattern or trend. We will touch on this in the next section, but this can be an incredibly valuable tool for time sensitive issues.

As you can see, the utilization of Dashboards on the Datadog platform can prove to be an endless, and seamless tool. It's super fun to explore, so I encourage you to play around with different features on offer to create some custom and informative visualizations. For further reading on Timeboards and other types of Dashboards please refer to the official documentation: https://docs.datadoghq.com/dashboards/timeboards/







## Monitoring Data

Before we deep dive into our monitoring capabilities with Datadog, here is a great blog post detailing the importance of automated alerts: https://www.datadoghq.com/blog/monitoring-101-alerting/

This is actually part of a three-blog series that I highly suggest reading to ensure you get the most out of your monitoring comprehension. 

As detailed in the Datadog blogs, automated alerts are crucial to monitoring. The alerts allow you to spot problems from anywhere in your infrastructure, so you can identify their causes and minimize service degradation and disruption. To quote the blog, “if metrics and other measurements facilitate observability, then alerts draw human attention to the particular systems that require observation, inspection, and intervention.” 

To put this importance into practice, let’s play around with the “Manage Monitors” tool in Datadog.

As an example, since we’ve already caught our test metric going above 800 once, we don’t want to have to continually watch the dashboard to be alerted when it goes above 800 again. We, naturally, need to tackle other issues or projects. So, to make life easier, let’s create a monitor that watches the average of your custom metric that will alert if it’s above the following values over the past 5 minutes:

	Warning threshold of 500
	Alerting threshold of 800
	Also ensure that it will notify you if there is No Data for this query over the past 10m

We can configure the monitor’s message so that it will:

	Send an email whenever the monitor triggers
	Create different messages based on whether the monitor is in an Alert, Warning, or No Data state 
	Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert State
	For comparison: screenshot the email notification the monitor sends you

To help get started, read through the alerting documentation here: https://docs.datadoghq.com/monitors/notifications/?tab=is_alert https://www.datadoghq.com/blog/monitoring-101-alerting/ https://docs.datadoghq.com/monitors/downtimes/
 
The great part of this tool is its aggregated simplicity. All of the above can be accomplished using the “New Monitors” tab in Datadog. Take a look at the below screen grabs to see how you can set up these monitor alerts:



![Monitor Alert](/images/monitor_alert.png)



![Monitor Alert Message](/images/monitor_alert2.png)



Once you’ve put these parameters in place, you can run the alert, and screenshot the alert email, that should look like this:



![Monitor Alert Email](/images/alert_email.png)

I cannot stress the value of these alerts enough, as it is an incredibly useful, and time sensitive tool that makes sure the individuals who need core information, are alerted immediately to address any issues that may need to be resolved quickly.

To take it a step further, mainly because no one wants to get blitzed with emails from this alert every few minutes, we can schedule downtimes for this monitor. As an example, here’s a sample scheduled downtime for my alert that silences the alert over the weekend:



 ![Monitor Alert Email](/images/downtime.png)
 
 

Feel free to play around with this option, as it might be useful to silence the alert during the evenings on weekdays as well.

 





## Collecting APM Data

Thus far, we have tackled a great deal of what Datadog has to offer. But a unique tool that we will conclude this guidebook with is APM. So, what is Datadog APM?

Datadog Application Performance Monitoring (APM or tracing) provides you with deep insight into your application’s performance, from automatically generated dashboards for monitoring key metrics, like request volume and latency, to detailed traces of individual requests – side by side with your logs and infrastructure monitoring. When a request is made to an application, Datadog can see traces across a distributed system, and can show you systematic data about precisely what is happening to this request. To use APM, you start by sending your traces to Datadog, and then configure your environment. 

Our final exercise in this Datadog platform manual will be to instrument this provided Flask app using Datadog’s APM Solution:




![Flask Code](/images/flask_code.png)





### Getting Started: APM

The first step is to enable APM logging settings within the datadog.yaml file so that the system allows the APM Agent to run.

Next, you have to install flask and ddtrace (among other modules needed, should they not already be installed). You can do this in terminal with:

	pip install flask
	pip install ddtrace

After these are installed successfully, you must create a new script called my_app.py, in which you copy and paste the above script. Once properly saved, the next step will be to run the python application using the following in terminal:
 
	ddtrace-run python my_app.py 

Note: the path name must be exactly as it is in the Datadog agent folder. Be sure that you have the correct path name. This can be a common obstacle, which can lead to endless permissions errors.

Once this command has run, the Datadog platform will allow you access to the APM Services tab. The below screen grabs are examples of what the APM dashboard and services pages should look like:



![Flask APM](/images/flask3.png)



![Flask APM Services](/images/flask4.png)



![Flask APM Endpoints](/images/APM_endpoints.png)



It’s important to recognize that in normal use cases, it’s valuable to have some data to thoroughly analyze in APM. You can do this by using a recurring trace request at a given frequency. From this point, you can inspect the trends over the course of some time, wherein Datadog will then recommend some APM monitors to help illustrate a narrative. Further, if you play around in the APM platform, you’ll see that you can use APM outputs in Timeboards you’ve already created to further build on what has essentially become a metric collection storyboard.

For continued reading on APM and Distributed Tracing please see this additional documentation: https://docs.datadoghq.com/tracing/

After gathering all of this information, it’s also important to delineate the difference between a Service and a Resource. Leveraging APM, it’s important to define such terms in highly distributed systems. As the APM documentation will tell you, services are the foundation of modern microservice architectures – grouping together endpoints, queries, or jobs for the purposes of scaling instances. Resources, however, represent a particular domain of a customer application. They are typically an instrumented web endpoint, database query, or background job.  

These insightful differentiations live in the APM Glossary and Walkthrough documentation here: https://docs.datadoghq.com/tracing/visualization/

I highly encourage everyone to peruse it as you become more technically sound using the platform.





## Final Question & Thoughts

Datadog has been used in a lot of creative ways in the past. They’ve written blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

From a generalist vantage point, it’s clear that there are an endless number of effective use cases to leverage Datadog’s platform. However, from a personal perspective, I’d love to see Datadog be used in the world of ocean swell forecasting models. While I know an integration for weather already exists, there are a couple of platforms that have predictive ocean swell models as far out as two weeks in advance. Over time, through collecting data from open-ocean buoys as well as satellite forecasting technology, creating a historical narrative, we would be able to fine tune swell and wind predictions using a much more distinct and accurate methodology. Further, as a surfer, you could get alerted every time the wind, tide, swell size and direction all line up for optimal conditions in real-time. It’s literally a surfer’s dream to know where, when, and for how long the waves will be perfect! On a more serious note, we might be able to monitor, and prepare for natural oceanic disasters much more efficiently as well. 

So I conclude our session with this: is there anything creative you would use Datadog for? Let me know by shooting me an email at tcronin10@gmail.com.

Here are some sources of inspiration as food for thought: https://www.datadoghq.com/blog/datadog-in-the-wild-5-fun-projects/


Thanks very much for your time, and I hope this was as productive for you as it has been for me!










