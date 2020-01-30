
# DataDog Hiring Exercise - William Karges

## Introduction

Today I'm going to give an overview of the various ways to monitor your application data through the DataDog platform.  We'll discuss some high level concepts and dive into the software to start tracking real data.  I'll also provide some context into the various ways you can make use of this data to realize benefits across your organization.

*__Disclaimer__: I will be using Windows 10 OS throughout my tutorial.  For non-windows users some of the setup, configuration, and scripting may be different but at a high level the process should be fairly similar.*

### Getting Started

If you haven't already, install the relevant Datadog agent for your specific OS (see the [README](https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md)).  If you're using Docker or Kubernetes you can simply install and configure the Datadog Agent for that container service rather than the agent specifc to your containers' OS kernel.

## Section 1 - Collecting Metrics

### What are Tags?

As you'll soon see, the Datadog platform can provide a ton of information on your various systems.  In order to make sense of all that data and turn it into actionable information, you'll want to have a good cadence of tagging.

Datadog tags let you assign properties to data so it can be filtered, grouped, and organized in relation to it's relevant components.  For example, on one of your dashboards you might simply see that one of your host machine's physical storage is running low.  Alternatively, with more tagging, you could see that in the AWS us-west-2 Region in one of your Windows Server 2012 EC2 instances, the volume under serial number FAND-B0A8 is nearly full.

You don't necessarily have to get that granular with your tags but as any developer who's had to build a hotfix will know, the more specific information you have on the origin and root cause of your issue(s), the better.

### Defining Tags

Datadog gives you freedom to tag your various application components however you like.  That said, if you need a little direction in your naming conventions, DataDog best practices for tagging can be found [here](https://docs.datadoghq.com/tagging/#why-it-matters).

For this example we're going to tag our host machine based off geographical location (region/availability-zone if you're using AWS), machine name, and environment (production, dev, etc.).

### Configuring Tags

In order to tag your host machine, you'll need to navigate to the `datadog.yaml` configuration file on your relevant OS (see [Agent config file paths](https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6v7)).

Once inside the `datadog.yaml` file navigate to the `tags` key to callout your host machine's tags.  Tags can be labeled in either of two syntaxes (see [Assigning Tags](https://docs.datadoghq.com/tagging/assigning_tags/?tab=agentv6v7)).  The tags and syntax I used are shown below as well as in my [datadog.yaml](configfiles/datadog.yaml) file.

```
tags: 
 - "availability-zone:us-west" 
 - "machine:local" 
 - "env:test"
```

Once you've added your tags, save your `datadog.yaml` file and restart the agent.  To do so, Windows users will run `"%PROGRAMFILES%\Datadog\Datadog Agent\bin\agent.exe" restart-service` from a command prompt.  For non-Windows users you'll need to search for the agent commands relevant to your OS in [Datadog Docs](https://docs.datadoghq.com/).

With that done your host machine should now be visible in from the Datadog browser client.  Log into DatadogHQ, navigate to Infrastructure->Host Map, and you should see your host machine with it's relevant tags.

[Sample HostMap](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host)

![HostMap_Tags.png](https://ddhiringexercise.s3-us-west-2.amazonaws.com/assetsv2/hostmaptags_v2.png)

...And it's that easy!  By just installing the Datadog agent and adding the relevant tags, you can track all kinds of performance metrics on any number of host machines through the Datadog platform!  In the next module we'll configure our first data integration and you'll start to see the different types of application data we can track beyond just machine performance.

### Configuring your first Integration

For our first data integration exercise I'm going to be using the Datadog MySQL integration but you're welcome to choose from any of the over 350 built-in integrations available in the [Datadog platform](https://app.datadoghq.com/account/settings#integrations/activemq).

Once again if you haven't already installed MySQL on your host machine go ahead and do so now.  If by some small chance you're also running Windows and, like me, prefer to manage relational databases with a UI, I'd also recommend you install [HeidiSQL](https://www.heidisql.com/download.php).

Once MySQL is installed you can navigate to the [MySQL Integration documentation](https://app.datadoghq.com/account/settings#integrations/mysql) and follow the configuration instructions.  You'll likely notice that the integration process is nearly identical to most a typical ODBC/OLE DB integration; you just add the Datadog agent as a user and grant that user permissions to the databases you want to track.  Then navigate to the conf.d folder in your [Agent's configuration directory](https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6v7#agent-configuration-directory) and inside the MySQL `conf.yaml` file, re-enter the credentials for your datadog user as well as your server's IP/Hostname and port.

Unlike most standard relational database integrations; once you grant the Datadog user access to the `perfromance_schema` table, you'll have full insight of the performance metrics of you're MySQL client, as opposed to the simple SELECT queries most other integrations are limited to.

With the [`conf.yaml`](configfiles/conf.yaml) file updated, go ahead and restart your agent.  Once that's done you'll see MySQL listed as Installed in your integrations tab.

[MySQL_Installed.png](https://ddhiringexercise.s3-us-west-2.amazonaws.com/assetsv2/MySQL_Installed.png)

Navigate back to your Hostmap where the MySQL integration should now display on your host machine.  Click on mysql then *mysql dashboard* to pull up your [MySQL Overview dashboard](https://app.datadoghq.com/dash/integration/12/MySQL%20-%20Overview?tpl_var_scope=host%3AWKARGES-10P.fourwindsinteractive.com&from_ts=1580339619368&to_ts=1580343219368&live=true&tile_size=m).

![MySQL_overview.png](https://ddhiringexercise.s3-us-west-2.amazonaws.com/assetsv2/MySQL_overview.png)

### Custom Metric collection

Next we're going to take a look at how you can collect metrics from some of the programs/services that your application uses but don't have an existing DataDog integration.  It's important to note this is more for smaller programs and/or prioprietary systems.  If you're trying to collect metrics from recognized/open source applications, it's recommended you create a [full Agent Integration](https://docs.datadoghq.com/developers/integrations/new_check_howto/).

For this example we're going to write a simple Agent check that submits a metric with a random value between 0 and 1000.  To get started you'll need to navigate to the `checks.d` in your Agent's configuration directory and create a new python file called `<YOUR_CUSTOM_AGENT_NAME>.py` (I'm using [`custom_ac1.py`](configfiles/custom_ac1.py) in my example.  Within your python file it's always best practice to make sure your check is compatible with any Agent version.  To do so simply copy/paste the following try/except block into your python file (I've included the comments from Datadog's [custom agent documentation](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7) so you can better understand what the script is doing).

```
try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck
```

Next we'll just need to create the AgentCheck class to submit our metric.  To do so we'll use the DataDog [`gauge()`](https://docs.datadoghq.com/developers/metrics/agent_metrics_submission/?tab=gauge) function that submits the value of a metric with a timestamp (so we can better track historical data).  Using this `gauge()` function we can give our metric the name `my_metric`, we can give the metric a random value using the python [random](https://docs.python.org/3/library/random.html) library (specifcally the `randint` function), and finally assign the relevant tags to give context to the metric.

#### Example Agent Check python class

```
class myCheck(AgentCheck):
	def check(self, instance):
		self.gauge('my_metric', random.randint(0, 1000), tags=['env:test','ac:mycheck','checktype:guage'])
```

Now all you have to do is navigate back to the `conf.d` directory and create a yaml file called `<YOUR_CUSTOM_AGENT_NAME>.yaml`.  *__Important:__ your .yaml file name must __exactly match__ the name of your custom agent .py file to work.*  If you just want to get your Agent working all you have to do is put in an empty instance script `instances: [{}]`.  For our example we're also going to add the `min_collection_interval` function to set the agent check to run every 45 seconds.  For better reference, you can see my whole example .yaml file [here](configfiles/custom_ac1.yaml).

Make sure and save both your .py and .yaml files then once again restart your agent using the relevant OS command.  You should now be able to see your custom metric, as well as your MySQL integration, attached to your host machine in the Datadog Hostmap.

![my_metric_andHostMap.png](https://ddhiringexercise.s3-us-west-2.amazonaws.com/assetsv2/my_metric_andHostMap.png)

## Section 2 - Visualizing Data



Imported the DataDog API collection into Postman.  Customized the create dashboard POST requet to track my_metric averages and sum over the past hour as well as MySQL CPU usage anomalies.  See [WK_CustomTimeBoard JSON file](configfiles/WK_CustomTimeBoard.json)

### Create Dashboard API

[WK Timeboard](https://app.datadoghq.com/dashboard/ysn-u6q-tmg/williams-timeboard-20-jan-2020-1735?from_ts=1579721318547&to_ts=1579722218547&live=true&tile_size=m)

![PostmanAPI_Success.png](assets/PostmanAPI_Success.png)

![TimeTable_1-21-2020.png](assets/TimeTable_1-21-2020.png)

Unfortunately I wasn't able to, "Set the Timeboard's timeframe to the past 5 minutes" (see screenshot below).  While I can adjust individual graphs to 5 minutes, the timeboard itself seems to be restricted to 15 minute intervals.  Not sure if this is just a limitation of the trial version or if I'm doing something wrong or maybe this was just a trick question?

### 5 Minute Snapshot

[TimeBoard Notification e-mail](assets/TimeBoard_Notification.eml)

##### Error
![Error_5min.png](assets/Error_5min.png)

##### 5 Minute Graph
![5mGraph.png](assets/5mGraph.png)

##### Notifications
![Notifications.png](assets/Notifications.png)

### Bonus Question - What is the Anomaly graph displaying?

The Anomaly graph compiles historical performance of a specific metric to flag truly "abnormal" activity.  

For example a game developer may have an alert set for when their autoscaling server/instance count eclipses a specified threshold.  If the alert gets triggered on a Friday night it's likely redundant as the majority of their users are active weekend nights and there's probably an existing process to provision more servers if needed.  

The more relevant information might actually be the opposite, if the server count stays unchanged or low through the Friday night.  The alert wouldn't go off since the threshold wasn't eclipsed but the anomaly graph would call out the unusually low server usage.  This in turn may motivate the game company to boost their marketing efforts and/or run an in-game promotion the next weekend to recooperate that user base or, at the very least, scale down server usage to save costs.

## Section 3 - Monitoring Data

Used the DataDog monitoring tool to create a monitor that tracked my_metric on my host machine and sent notifications to my e-mail if specific criteria was met:

	* Warning if my_metric eclipsed the threshold of 500
	* Alert if my_metric eclipsed the threshold of 800
	* Notification if my_metric has missing data over 10 minutes

Tested the threshold both on average and at least once during the last five minutes.  Used conditional statements to adjust the body of the e-mail notification based on the relevant alert type.  Then immediately turned off the monitor to prevent my phone from vibrating off my desk.

* [Monitor JSON](configfiles/Monitor.json)

* [Monitor E-mails](assets/Monitors/)

![Warn.png](assets/Monitors/Warn.png)

### Bonus Question - Deactivate Out of Office notifications

Monitor notifications can be turned off on the fly via the mute button in the monitor dashboard or you can scheduled deactivation using the scheduled downtime feature.

* [Scheduled Downtime](https://app.datadoghq.com/monitors#downtime?)

#### Mute
![mute.png](assets/Monitors/mute.png)

#### Scheduled Downtime configuration
![SilenceScope.png](assets/Monitors/SilenceScope.png)

#### Scheduled Downtime test e-mail
![scheduled_downtime_email.png](assets/Monitors/scheduled_downtime_email.png)

## Section 4 - Collecting APM Data

I was unable to get the provided Flask app to run (I believe due to compatibility issues with my Win10 OS).  I instead modified the code to form a native python application that simply prints a string.  

Once the program could run on my machine all I had to do was use the tracer.wrap function to tag the relevant operation name, service, and resource.  Being an increadibly simple application, the trace recorded a processing-time of near 0.

* [APM & Infra Dashboard](https://app.datadoghq.com/dashboard/4nn-f4a-m48/williams-apm--metrics-dashboard?from_ts=1579795766356&to_ts=1579882166356&live=true&tile_size=m)

* [APM Python code](configfiles/APM-test.py)

![APM1.png](assets/APM1.png)

### Bonus Question - What is the difference between a Service and a Resource?

Services are groups of related functions, URLs, etc. within an application.  Resources are the specifc endpoints (URL IP, DB Query, etc.) within that service.

The benefit of Datadog is tracking the performance of these services and make sure they're loosely coupled and new changes aren't negatively affecting each other and the application as a whole as is best practice with modern development.

## Final Question - Creative use of DataDog

Outside of cloud applicaiton monitoring DataDog's agent could be used to push the envelope in IT device management.  An organization's IT group could image all employee devices (laptops, cell phones, etc.) with the DataDog Agent installed.

From there they could track machine performance to determine how effectively individuals/department are using their devices.  Specifically they could tag each device to the relevant individual, team, department, etc. and make better determinations on the appropriate device OS/specs for each department.

For example the IT group might see the project managers barely tax their machines and then start issuing lower powered devices to that department to shave costs.  Conversely the creative teams may be constantly overclocking their machines so IT could source upgraded devices to reduce render times and improve effeciency.  For purely selfish reasons this use case would help me make the argument to upgrade my wildly under-spec'd PC.  You could also track anomalies in performance that may relate to misusage/malware or other IT concerns.

## Resource Folders

* [Assets/Screenshots](assets/)
* [Code Commits](configfiles)