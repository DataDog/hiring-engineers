
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

*__Additional Disclaimer__: If you're using Datadog in Europe you'll also need to be sure to change the `dd_url` node value from `intake.logs.datadoghq.com` to `tcp-intake.logs.datadoghq.eu`*

Once you've added your tags, save your `datadog.yaml` file and restart the agent.  To do so, Windows users will run `"%PROGRAMFILES%\Datadog\Datadog Agent\bin\agent.exe" restart-service` from a command prompt.  For non-Windows users you'll need to search for the agent commands relevant to your OS in [Datadog Docs](https://docs.datadoghq.com/).

With that done your host machine should now be visible in from the Datadog browser client.  Log into DatadogHQ, navigate to Infrastructure->Host Map, and you should see your host machine with it's relevant tags.

[Sample HostMap](https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host)

![HostMap_Tags.png](https://ddhiringexercise.s3-us-west-2.amazonaws.com/assetsv2/hostmaptags_v2.png)

...And it's that easy!  By just installing the Datadog agent and adding the relevant tags, you can track all kinds of performance metrics on any number of host machines through the Datadog platform!  In the next module we'll configure our first data integration and you'll start to see the different types of application data we can track beyond just machine performance.

### Configuring your first Integration

For our first data integration exercise I'm going to be using the Datadog MySQL integration but you're welcome to choose from any of the over 350 built-in integrations available in the [Datadog platform](https://app.datadoghq.com/account/settings#integrations/activemq).

Once again if you haven't already installed MySQL on your host machine go ahead and do so now.  If by some small chance you're also running Windows and, like me, prefer to manage relational databases with a UI, I'd also recommend you install [HeidiSQL](https://www.heidisql.com/download.php).

Once MySQL is installed you can navigate to the [MySQL Integration documentation](https://app.datadoghq.com/account/settings#integrations/mysql) and follow the configuration instructions.  You'll likely notice that the integration process is nearly identical to most a typical ODBC/OLE DB integration; you just add the Datadog agent as a user and grant that user permissions to the databases you want to track.  Then navigate to the conf.d folder in your [Agent's configuration directory](https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6v7#agent-configuration-directory) and inside the `MySQL\conf.yaml` file, re-enter the credentials for your datadog user as well as your server's IP/Hostname and port.

Unlike most standard relational database integrations; once you grant the Datadog user access to the `perfromance_schema` table, you'll have full insight of the performance metrics of you're MySQL client, as opposed to the simple SELECT queries most other integrations are limited to.

With the [`conf.yaml`](configfiles/conf.yaml) file updated, go ahead and restart your agent.  Once that's done you'll see MySQL listed as Installed in your integrations tab.

![MySQL_Installed2.png](https://ddhiringexercise.s3-us-west-2.amazonaws.com/assetsv2/MySQL_Installed2.png)

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

Now all you have to do is navigate back to the `conf.d` directory and create a yaml file called `<YOUR_CUSTOM_AGENT_NAME>.yaml`.  *__Important:__ your .yaml file name must __exactly match__ the name of your custom agent .py file to work.*  If you just want to get your Agent working all you have to do is put in an empty instance script `instances: [{}]`.  For our example we're also going to add the `min_collection_interval` function to set the agent check to run every 45 seconds.  For reference, you can see my whole example .yaml file [here](configfiles/custom_ac1.yaml).

Make sure and save both your .py and .yaml files then once again restart your agent using the relevant OS command.  You should now be able to see your custom metric, as well as your MySQL integration, attached to your host machine in the Datadog Hostmap.

![my_metric_andHostMap.png](https://ddhiringexercise.s3-us-west-2.amazonaws.com/assetsv2/my_metric_andHostMap.png)

## Section 2 - Visualizing Data

Now that we've got a variety of data integrated with Datadog, let's make it look pretty!

In this example we're going to create a custom timeboard so we can view all our different metrics in any specified timeframe.  Since manual creation of dashboards is fairly self-explanitory (see the [dashboard docs](https://docs.datadoghq.com/dashboards/) for reference), we're going to create our timeboard using the DataDog API.

To get started you'll need to:

* If you haven't already, download [Postman](https://www.getpostman.com/downloads/)
* Download the [Datadog Postman collection](https://docs.datadoghq.com/resources/json/datadog_collection.json)
* Follow the [instructions](https://docs.datadoghq.com/getting_started/api/) for getting the Datadog Postman collection imported.
* Navigate to the API tab in DatadogHQ to retrieve your API and application keys.  Then once again follow the [instructions](https://docs.datadoghq.com/getting_started/api/) to set those variables in Postman.

![APIKeys.png](https://ddhiringexercise.s3-us-west-2.amazonaws.com/assetsv2/APIKeys.png)

With Postman configured we can now use the Create Dashboard `POST` request to build our first timeboard.  The request should be available in your collections dropdown, you'll notice it's already inherited your API/APP key headers.  Navigate to the body where we'll use the JSON script to design how your timeboard will look and function.

A full description of each of the JSON arguments can be found in the [API Documentation](https://docs.datadoghq.com/api/?lang=bash#dashboards), for now I'll just callout some of the more important fields:

* `title` is required to help you identify your Timeboard and the graph(s) within it.
* `q` refers to the metric(s) you want to view and any manipulation you want to perform on them.  For this example we're going to map three different metrics:
	* Average of my_metric on my host machine -> `avg:my_metric{host:WKARGES-10P.fourwindsinteractive.com}`
	* Rollup sum of my_metric over the past hour -> `avg:my_metric{*}.rollup(sum, 1)`
	* Anomalies in MySQL's CPU usage -> `anomalies(avg:mysql.performance.cpu_time{*}, 'basic', 2)`
* `type` refers to how you want your data to display.  The type of graph you use directly correlates with the function you're applying to your data.  
	* For example we'll be using the `timeseries` visualization for average and anomalies graphs so we can see how those metrics perform over time.
	* Conversely we'll use `query_value` for our rollup as it's designed to show a single value and we're wanting to see only the sum of our metric.
	* A full list of the different widgets can be found [here](https://docs.datadoghq.com/dashboards/widgets/).

Once you've filled out the necessary arguments in your JSON body (see my [completed example](configfiles/WK_CustomTimeBoard.json)), you can submit the `POST` request.  You should see a response similar to [this](configfiles/POST_response.json).

![POST_Success.png](https://ddhiringexercise.s3-us-west-2.amazonaws.com/assetsv2/POST_Success.png)

After submitting the request, navigate the Dashboard List where you should see your [newly created timeboard](https://app.datadoghq.com/dashboard/tt5-dey-zu6/wkarges-datadog-hiring-exercise-timeboard?from_ts=1580423907246&to_ts=1580424807246&live=true&tile_size=m).  Open it up to ensure all your graphs were created and appearing as you specified.

![TimeTable_1-21-2020.png](https://ddhiringexercise.s3-us-west-2.amazonaws.com/assetsv2/TimeTable_1-21-2020.png)

Now open up one of your graphs and set the timeframe to the past five minutes.

![past5minutes.png](https://ddhiringexercise.s3-us-west-2.amazonaws.com/assetsv2/past5minutes.png)

Once again, it's that easy.  Through just a simple post request you can create as many Timeboards as you like each of which containing graphs that can display your data in endless ways.

When referencing the API documentation you may have also noticed each call can be written in Python and Ruby as well.  This means you could write any of the Datadog APIs directly into your code.

For example you could tie the `Create a Dashboard` API into your autoscaling instances.  Everytime your server count increased due to demand you would automatically have dashboards created with them tracking all their metrics.  As the instance count scaled back in, you could use the `Delete a Dashboard` API to ensure all your no-longer needed dashboards were automatically deleted.

### Anomalies

Before we move on I wanted to make sure and callout the Anomaly graph that we created earlier, as it's one of Datadog's biggest differentiators.  

In the next section you'll see how you can monitor your data and create alerts when the data you're monitoring meets specified criteria.  While almost any monitoring software can trigger an alert when a certain threshold is eclipsed, the Datadog anomaly graph is unique in how it compiles historical performance of a specific metric to flag truly "abnormal" activity.

Building off the example of autoscaling instances, a game developer may have an alert set for when their autoscaling server/instance count eclipses a specified threshold.  If the alert gets triggered on a Friday night it's likely redundant as the majority of their users are active weekend nights and there's probably an existing process to provision more servers if needed.  

The more relevant information might actually be the opposite, if the server count stays unchanged or low through the Friday night.  The normal alert wouldn't go off since the threshold wasn't eclipsed but the anomaly graph would flag the unusually low server usage.  This in turn may motivate the game company to boost their marketing efforts and/or run an in-game promotion the next weekend to recooperate that user base or, at the very least, scale down server usage to save costs.

## Section 3 - Monitoring Data

We've successfully built some functional graphs but no matter how nice they look you probably don't want to sit and stare and them 24 hours a day waiting for something to happen.  Luckily Datadog provides a comprehensive monitoring tool where you can configure automated alerts to notify yourself and your relevant team members when your data meets specified criteria.

For this example we're going to monitor the custom metric, `my_metric`, that we created earlier.  To get started, navigate to the [manage monitors](https://app.datadoghq.com/monitors/manage) tab, select 'New Monitor', and then select 'Metric'.

![CreateMonitor.gif](https://ddhiringexercise.s3-us-west-2.amazonaws.com/assetsv2/CreateMonitor.gif)

Once inside of the monitor editor you'll need to do a few things:

1. Set the detection method: for this example we'll be using the default `Threshold Alert`
1. Define the metric: choose `my_metric` from the dropdown and set your hostmachine as the source.
1. Set the alert conditions: Datadog gives you the ability to both define the threshold and the severity of the issue.  For this example we're going to set a few different alert conditions:
	* Warning if my_metric eclipses a threshold of 500.
	* Alert if my_metric eclipses a threshold of 800.
	* Notification if my_metric returns no data for more than 10 minutes.
![monitormethod.png](https://ddhiringexercise.s3-us-west-2.amazonaws.com/assetsv2/monitormethod.png)
1. Define the message you wanted to send.  You can use markdown to conditionally format the message to pair with the relevant criteria.
	* Use `{{#is_alert}}<YOUR_MESSAGE>{{/is_alert}}` to define your alert message.
	* Use `{{#is_warning}}<YOUR_MESSAGE>{{/is_warning}}` to define your warning message.
	* Use `{{#is_no_data}}<YOUR_MESSAGE>{{/is_no_data}}`to define your missing data message.
1. Finally define the team members you want to notify.  You can individually add users or simply select `all` to send it to all the users in your Datadog company account.
![monitorrecipients.png](https://ddhiringexercise.s3-us-west-2.amazonaws.com/assetsv2/monitorrecipients.png)

You can reference my complete [monitor JSON here](configfiles/Monitor.json).  Shortly after you save your monitor you should start recieving warning and alert e-mails like [these](assets/Monitors/E-mails/).  You can also use the 'Test Notifications' feature in the monitor editing tool to make sure they're sending correctly.

As you'll soon realize, these monitor e-mails can quickly fill up your inbox.  Fortunately Datadog also provides the ability to mute e-mails for set durations or scheduled periods of time (such as off work hours).

### Muting Notifications

If you want to hault your notifications immediately for a specific duration, you can simply use the mute botton in the top right of your monitor's dashboard.

![MuteMonitor](https://ddhiringexercise.s3-us-west-2.amazonaws.com/assetsv2/MuteMonitor.gif)

If you instead want to schedule your notifications to turn off after work hours, you can do so using the [Scheduled Downtime feature](https://www.datadoghq.com/blog/mute-datadog-alerts-planned-downtime/).  

Navigate to the [Manage Downtime](https://app.datadoghq.com/monitors#downtime) tab, select 'Schedule Downtime', and define the duration for which you want monitor(s) muted.  You can schedule as many downtimes as needed, in this case you'll need one for nights and one for weekends.

![ScheduleMute.gif](https://ddhiringexercise.s3-us-west-2.amazonaws.com/assetsv2/ScheduleMute.gif)

## Section 4 - Collecting APM Data

Earlier I mentioned the importance of granular information for monitoring, troubleshooting, and working to improve the overall performance of your application.  Arguably the greatest tool for accomplishing this is Datadog's Application Performance Monitoring (APM).

With APM you can integrate Datadog directly into your code to create [traces](https://docs.datadoghq.com/tracing/visualization/#trace) which track the amount of time your applications spend processing requests.  For mission critical applications where data needs to be served up to users in near-real time, this kind of functionality is invaluable.

For this exercise you'll need an application to track.  You can use any application you like within the [officially supported languages](https://docs.datadoghq.com/tracing/setup/), or this [sample Flask app](configfiles/SampleFlaskApp.py).  For my example I'm going to use a simple python app that just prints a string.

Before we get into the code, you'll want to make sure you have all the necessary libraries installed.  Open a command prompt (or the equivelant tool for your relevant OS) and run a `pip install` command to import the `ddtrace` library.

You'll need to reference that same library in your python file.  We'll also use the native Python logging API.  You can reference both with the following commands:

```
from ddtrace import patch_all; patch_all(logging=True)
import logging
from ddtrace import tracer
```

Next you'll need to format the python logger messages to match the Datadog APM required sytax.

```
FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
          '[dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
          '- %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger(__name__)
log.level = logging.INFO
```

Finally you'll need to use the 	`@tracer.wrap()` function to define your `object name`, `service`, and `resource`.  
* `Object name` refers to the python function you've written, for this example I've identified named my object in relation to it's use, `printstring`.
* `Service` refers to the group of endpoints/queries that your microservice is composed of.  An example would be an API that retrieves data from a variety of SQL tables that collectively equate to your service.
* `Resource` essentially refers to the network location of your application.  A resource could be a web address, database query, or task running in the background.
The `@tracer.wrap()` function includes arguments for you to appropriately identify these fields.  You can see mine below:

```
@tracer.wrap('testApp.printstring', service='hiring_exercise-service', resource='testApp-response')
```

Once you've [finished writting your application](configfiles/APM-test.py), use the [`ddtrace-run`](https://docs.datadoghq.com/tracing/setup/python/) command to run your application and log your trace.  

`ddtrace-run python APM-test.py`

Then once again restart your Datadog agent and navigate to the APM module to view your newly recorded APM Service and all it's properties.

![APM.gif](https://ddhiringexercise.s3-us-west-2.amazonaws.com/assetsv2/APM.gif)

You can also view APM metrics through a [standard dashboard](https://app.datadoghq.com/dashboard/4nn-f4a-m48/williams-apm--metrics-dashboard?from_ts=1579795766356&to_ts=1579882166356&live=true&tile_size=m).

![APM1](https://ddhiringexercise.s3-us-west-2.amazonaws.com/assetsv2/APM1.png)

//---------------------------------------------------------------------------------

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