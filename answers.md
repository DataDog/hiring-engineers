# Datadog Self-Guided Tour - Solutions Engineer Technical Exercise

This tutorial will go through Datadog main features in order for you to discover and test the software various features in a structured way. Don’t be scared, it will be fun and as documented as possible! We will also provide you with some extra links throughout the tutorial in case you are interested in knowing more about a particular topic.

Summary
* [Getting Started](https://github.com/MargotLepizzera/hiring-engineers/blob/solutions-engineer/answers.md#prerequisites---setup-the-environment)
* [Collecting Metrics](https://github.com/MargotLepizzera/hiring-engineers/blob/solutions-engineer/answers.md#collecting-metrics)
* [Visualizing Data](https://github.com/MargotLepizzera/hiring-engineers/blob/solutions-engineer/answers.md#visualizing-data)
* [Monitoring Data](https://github.com/MargotLepizzera/hiring-engineers/blob/solutions-engineer/answers.md#monitoring-data)
* [Collecting APM Data](https://github.com/MargotLepizzera/hiring-engineers/blob/solutions-engineer/answers.md#collecting-apm-data)
* [Getting Creative](https://github.com/MargotLepizzera/hiring-engineers/blob/solutions-engineer/answers.md#getting-creative)

More information about Datadog overview: https://docs.datadoghq.com/guides/overview/

 GIF 
Let’s go or similar

## Prerequisites - Setup the environment

__You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:__

* __You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. Here are instructions for setting up a Vagrant Ubuntu 12.04 VM. You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.__

For the environment, we decided to use Mac OS X. However, the best way to setup your environment and to avoid any OS and/or dependency issues, is to go with a combination of VirtualBox and Vagrant Ubuntu 12.04VM. 

To do so:
-	Download VirtualBox from here: https://www.virtualbox.org/wiki/Downloads
-	Download Vagrant from here: https://www.vagrantup.com/downloads.html
-	Get started with Vagrant here: https://www.vagrantup.com/intro/getting-started/

* __Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.__

Once your environment is all done, you can move on to Datadog setup!

1.	First, go to Datadog website, and hit the sign-up button.
2.	Enter a few information about yourself, and most importantly, about your stack.
3.	Then, pick the right OS (in this example: Mac OS X) and start following the different steps.

![Installation Instructions for Mac OS X](/screenshots/install_instructions.jpg)

In the case of a Mac OS X…

1.	First download the DMG package and install it by adding your API key to `/opt/datadog-agent/etc/datadog.conf`. 

```
[Main]

# The host of the Datadog intake server to send Agent data to
dd_url: https://app.datadoghq.com

# If you need a proxy to connect to the Internet, provide the settings here (default: disabled)
# proxy_host: my-proxy.com
# proxy_port: 3128
# proxy_user: user
# proxy_password: password
# To be used with some proxys that return a 302 which make curl switch from POST to GET
# See http://stackoverflow.com/questions/8156073/curl-violate-rfc-2616-10-3-2-and-switch-from-post-to-get
# proxy_forbid_method_switch: no

# If you run the agent behind haproxy, you might want to enable this
# skip_ssl_validation: no

# The Datadog api key to associate your Agent's data with your organization.
# Can be found here:
# https://app.datadoghq.com/account/settings
# This can be a comma-separated list of api keys.
# (default: None, the agent doesn't start without it)
api_key: <YOUR_API_KEY>

```

You could also copy paste this command line on your terminal:	

```
DD_API_KEY=<YOUR_API_KEY> bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/dd-agent/master/packaging/osx/install.sh)"
```

2.	You should then be able to use the command line datadog-agent in your terminal. Here is a list of some basic command lines that can be used to manage the agent on OS X: https://docs.datadoghq.com/guides/basic_agent_usage/osx/. 
You can also use the Datadog Agent app using your system tray.

3.	If you want to, you can set up the agent so it automatically runs at login. To do so, you just need to execute these two command lines displayed on the configuration tab:

```
sudo cp '/opt/datadog-agent/etc/com.datadoghq.agent.plist' /Library/LaunchDaemons
sudo launchctl load -w /Library/LaunchDaemons/com.datadoghq.agent.plist
```

More information about how to get started with the agent depending on your platform: https://docs.datadoghq.com/guides/basic_agent_usage/.

## Collecting Metrics: 

* __Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.__

>Tags are a good way for you to add an extra dimension to your metrics in order to conduct in-depth analysis by filtering and grouping them.

Tags can be created by adding them to the datadog.conf file below the `# Set the host's tags (optional)` section. We advise you to follow the structure key: value syntax. Also make sure that you don’t use “device”, ”host”, and “source” as they are reserved tag keys.

```
[Main]

# The host of the Datadog intake server to send Agent data to
dd_url: https://app.datadoghq.com

# If you need a proxy to connect to the Internet, provide the settings here (default: disabled)
# proxy_host: my-proxy.com
# proxy_port: 3128
# proxy_user: user
# proxy_password: password
# To be used with some proxys that return a 302 which make curl switch from POST to GET
# See http://stackoverflow.com/questions/8156073/curl-violate-rfc-2616-10-3-2-and-switch-from-post-to-get
# proxy_forbid_method_switch: no

# If you run the agent behind haproxy, you might want to enable this
# skip_ssl_validation: no

# The Datadog api key to associate your Agent's data with your organization.
# Can be found here:
# https://app.datadoghq.com/account/settings
# This can be a comma-separated list of api keys.
# (default: None, the agent doesn't start without it)
api_key: f7adb89b942119d34edbb691009cec0d

# Force the hostname to whatever you want. (default: auto-detected)
# hostname: mymachine.mydomain

# Set the host's tags (optional)
tags: laptop:margot,project:test,env:dev,platform:macosx
```

In the following example, 4 tags were implemented:
* A first tag related to our development environment.
* A second tag related to the owner of the device, here it is Margot’s laptop.
* A third tag related to the platform type, here it is Mac OS X.
* A fourth tag related to the project’s type, here: test.

![Host Tagging Through Agent Config File](/screenshots/host.png)

You can also easily assign tags to hosts using the API or the UI. This, however, is not an available feature for integrations.

 GIF 
Moi en train d’ajouter un tag via UI
Host Tagging Through UI

More information on the tagging topic: 
https://docs.datadoghq.com/guides/tagging/
https://help.datadoghq.com/hc/en-us/articles/204312749-Getting-started-with-tags

* __Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.__

> Our next step is about database integration. Integration is one of the main ways Datadog connects to your stack to collect metrics for you to monitor. Datadog has over 200 built-in integrations that allow you to see pretty much across all your systems, apps and services.

To integrate a database, first pick the one you’re the most comfortable working with, install it, and visit the corresponding Datadog integration page to learn how to integrate/proceed to the integration:
* PostgreSQL: https://docs.datadoghq.com/integrations/postgres/
* MongoDB: https://docs.datadoghq.com/integrations/mongo/
* MySQL: https://docs.datadoghq.com/integrations/mysql/

Detailed information about your integration is also to be found when you hit the Integration button on Datadog Application sidebar and click the integration of interest. The Configuration tab indeed helps you go through the whole integration process.

![Postgres Integration](/screenshots/postgres_inte_1.png)
![Postgres Integration](/screenshots/postgres_inte_2.png)

In our case, we decided to go with PostgreSQL (that can be downloaded from here - https://postgresapp.com/). We consequently …

1.	Created a read-only Datadog user using the following command line:

```
create user datadog with password '<PASSWORD>';
grant SELECT ON pg_stat_database to datadog;
```

2.	Checked the correct permissions running the following command line:

```
psql -h localhost -U datadog postgres -c \
    "select * from pg_stat_database LIMIT(1);"
    && echo -e "\e[0;32mPostgres connection - OK\e[0m" || \
    || echo -e "\e[0;31mCannot connect to Postgres\e[0m"
And entered our ‘<PASSWORD>’.
```

3.	Then, we edited the conf.d/postgres.yaml file (using this https://github.com/DataDog/integrations-core/blob/master/postgres/conf.yaml.example) and added a few tags to configure the agent and to connect it to our PostgreSQL server. 

```yaml
init_config:

instances:
   -   host: localhost
       port: 5432
       username: datadog
       password: <YOUR_PASSWORD>
       tags:
            - laptop:margot
            - project:postgres
```

4.	We restarted the agent.

```
datadog-agent stop
datadog-agent start
```

5.	We ran the `datadog-agent info` command line to make sure the PostgreSQL integration has been successfully completed.

![Postgres Integration Validation](/screenshots/postgres_working.png)

* __Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.__

> Datadog custom agent checks are a way for you to get the Agent to collect metrics from your custom applications or unique systems.

Different types of check can be sent (metric, event, service), however we will here focus on implementing a gauge metric.

To get our Agent check to submit a brand-new metric, we need to create two distinct files: 

* mymetric.yaml that needs to go in `datadog-agent/conf.d`:

```yaml
init_config:

instances:
    [{}]
```

* mymetric.py that has to go in `datadog-agent/checks.d`: 

```python
from random import random
from checks import AgentCheck
class HelloCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', 1000 * random())
```

Make absolutely sure that the name of your two files match, otherwise your custom check will not work.

 GIF
Sad, careful

After that, we restarted the Datadog Agent and executed the `datadog-agent info` command line to make sure the check had successfully been implemented.

![Custom Agent Check Validation (Terminal)](/screenshots/mymetric_working.png)

To make sure your custom agent check was implemented, you can also go to “Dashboard” on Datadog Application sidebar, pick the corresponding custom metric, and you should be able to see your metric evolution: yay you!

![Custom Agent Check Validation (UI)](/screenshots/mymetric_workingui.png)

More information about custom agent check: https://docs.datadoghq.com/guides/agent_checks/

* __Change your check's collection interval so that it only submits the metric once every 45 seconds.__

> As you can tell by its name, the check’s collection interval corresponds to which the frequency the check is run.
By default, the collection interval is set to 0 seconds. This means that the check will be collected at the same frequency as the other agent integrations, ie every 15-20 seconds (depending on the number of integrations).
This can be changed by modifying the check’s yaml file: you simply need to add the `min_collection_interval: nb_of_seconds` parameter at the init_config or at the instance level.

To change our check’s collection interval, we therefore slightly modified our `datadog-agent/conf.d/mymetric.yaml` file, and simply added the parameter `min_collection_interval: 45` to the configuration file.

```yaml
init_config:
  min_collection_interval: 45

instances:
    [{}]
```

After that, we restarted again our Datadog agent, and went back to our graph to make sure that the collection interval had, indeed, gone from 15-20 to 45 seconds.

![Change of Collection Interval](/screenshots/collection_interval_change.png)

More information about the frequency of agent checks: 
https://docs.datadoghq.com/guides/agent_checks/#configuration
https://help.datadoghq.com/hc/en-us/articles/203557899-How-do-I-change-the-frequency-of-an-agent-check-

* __Bonus Question: Can you change the collection interval without modifying the Python check file you created?__

The collection interval was therefore changed in the yaml file (and not the Python one).

## Visualizing Data:

__Utilize the Datadog API to create a Timeboard that contains:__
* __Your custom metric scoped over your host.__
* __Any metric from the Integration on your Database with the anomaly function applied.__
* __Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket.__

> Datadog allows you to create dashboards so you can quickly visualize the data you’re interested in. The application features two different types of dashboards: timeboards and screenboards. Timeboards are always scoped to the same time and have a predefined grid-like layout whereas screenboards are more flexible and customizable.

We will here focus on creating a timeboard through Datadog API.

To start using Datadog API, you first need to install Datadog. Therefore, go to your python environment and run the `pip install datadog` command line as indicated here: https://github.com/DataDog/datadogpy. 

![Datadog Installation](/screenshots/pipinstalldd.png)

You then need to look for your API key and to create your application key. To do so, just go to Datadog application, go to the “Integrations” section in the side bar menu, and pick the APIs tab. Just hit the button “Create Application Key” and there you go, your brand-new application key!

![Application Key Creation](/screenshots/appkeycreation.jpg)

You then need to adapt a code snippet from here: https://docs.datadoghq.com/api/#timeboards. 
Here is what ours looked like :

```python
from datadog import initialize, api

options = {
    'api_key': <YOUR_API_KEY>,
    'app_key': <YOUR_APP_KEY>
}

initialize(**options)

title = "Datadog Project Timeboard V2"
description = "This timeboard displays the custom metric scoped over host, the max connections over PostGres, and the sum of the custom metric for the past hour"
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {
            "q": "avg:my_metric{host:Margots-MacBook-Pro.local}",
             "type": "line"
            },
            {
             "q": "anomalies(avg:postgresql.max_connections{*}, 'basic', 2)",
             "type": "line"
            },
            {
             "q": "avg:my_metric{*}.rollup(sum, 3600)",
             "type": "line"
            }
        ],
    "viz": "timeseries"
    },
    "title": "Custom Metric & PostGres"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:my-host"
}]

read_only = True

res = api.Timeboard.create(title=title, description=description, graphs=graphs, template_variables=template_variables, read_only=read_only)

print(res)
```

Then, save and run the python script you just created on your terminal. It should output something like this:

![Output](/screenshots/ddapi.png)

In a few moments you should be able to see your timeboard over the Datadog Application. 

![Timeboard Created Through Datadog API](/screenshots/timeboard.png)

If you solely need to do small modifications on your timeboard, you can simply change the method from `api.Timeboard.create` to `api.Timeboard.update` on your timeboard python file.

It is also worth noting that you can very easily create dashboards using drag and drop in the UI and immediately get the corresponding JSON file.

 GIF 
![](http://g.recordit.co/55jadBYi6q.gif)
 SCREENSHOT
![Creating Timeboard Through UI & Getting the Corresponding JSON File](/screenshots/timeboard_UI.png)
![Creating Timeboard Through UI & Getting the Corresponding JSON File](/screenshots/timeboard_JSON.png)


More information about dashboards:
https://help.datadoghq.com/hc/en-us/articles/204580349-What-is-the-difference-between-a-ScreenBoard-and-a-TimeBoard-

More information about Datadog API:
https://docs.datadoghq.com/api/

More information about anomalies:
https://docs.datadoghq.com/guides/anomalies/

More information about graphing and advanced functions (including rollup functions):
https://docs.datadoghq.com/graphing/
https://help.datadoghq.com/hc/en-us/articles/204820019-Graphing-with-Datadog-from-the-query-to-the-graph
https://help.datadoghq.com/hc/en-us/articles/204526615-What-is-the-rollup-function-

__Once this is created, access the Dashboard from your Dashboard List in the UI:__
* __Set the Timeboard's timeframe to the past 5 minutes.__

> For some reasons, you might be willing to select a specific timeframe on your dashboard.

Setting a timeboard’s timeframe to 5 minutes for instance can be done easily with the UI by directly selecting the timeframe of interest on the graph.

![Timeframe Change](/screenshots/timeframe_change.png)

* __Take a snapshot of this graph and use the @ notation to send it to yourself.__

> Datadog enables you to be notified automatically or by your team in case of performance problems. It also quickly lets you know where they are happening in your infrastructure so you can immediately react if you need to.

You can for instance take a snapshot of a graph and comment it with a @ notation to send it to yourself or someone of your team.

![Notify Someone About a Specific Graph](/screenshots/graph_notif.png)

The notified person will consequently be able to see the graph in her/his events section and receive an email.

![Notification About a Graph in Events Section](/screenshots/graph_events.png)

![Notification About a Graph in Mailbox](/screenshots/graph_mail.png)

More information about notifications: https://help.datadoghq.com/hc/en-us/articles/203038119-What-do-notifications-do-in-Datadog-

* __Bonus Question: What is the Anomaly graph displaying?__

Anomaly detection is a feature allowing you to identify metrics behaving differently than they have in the past. The anomaly graph should therefore highlight unusual data so you can quickly react if you need to.

It is not obvious in the previous graph as it displayed a constant figure (maximum number of connections to PostgreSQL), however when applied to a metric such as my_metric, we can see that the graph (see below) features a grey area with a blue curve, which is made up of the normal data; and a white area with red values, which is the unexpected data. 

![Anomaly Function Applied to my_metric](/screenshots/anomaly_graph.png)

## Monitoring Data

__Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.__
__Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:__
* __Warning threshold of 500__
* __Alerting threshold of 800__
* __And also ensure that it will notify you if there is No Data for this query over the past 10m.__

__Please configure the monitor’s message so that it will:__
* __Send you an email whenever the monitor triggers.__
* __Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.__
* __Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.__

> Datadog not only allows you to visualize your data, it also enables you to monitor it, and to be alerted when critical changes happen. There are different types of monitor that can be implemented within Datadog: host, metric, integration, process, network, event-based, and custom. 

Here we will focus on metric monitor. To create a monitor, first click “Monitors” on Datadog Application’s side bar, then hit the “+ New monitor” button, and start editing your monitor visually.

You can create different types of metric monitors (threshold, forecast or change alert, anomaly or outlier detection), you then need to define conditions, to setup notifications and you’re good to go!

In this example we decided to define a threshold alert on my_metric from our host:
-	We first set a warning in case the average of our custom metric went over the 500 threshold in the past 5 minutes.
-	We then set an alert in case the average of our custom metric went over the 800 threshold in the past 5 minutes.
-	Thirdly, we asked for a notification in case data was missing for more than 10 minutes.

We also designed a monitor’s message adapted to the type of issue: alert, warning or missing data. In the alert message, we included the host name, ip, the threshold and the value that caused the monitor to trigger. Finally, we added our email address to check the email notifications worked.

![Creating a Metric Monitor](/screenshots/alert_creation_1.png)
![Creating a Metric Monitor](/screenshots/alert_creation_2.png)

More information about monitoring:
https://docs.datadoghq.com/guides/monitors/
https://docs.datadoghq.com/monitoring/

* __When this monitor sends you an email notification, take a screenshot of the email that it sends you.__

> Datadog allows you to setup alerts to automatically notify individuals or teams using their favorite communication tools. This involves emails, third party services such as Slack, Hipchat or Pagerduty, or other custom endpoints through webhooks.

Following the setup of our monitor, we received a first warning email: 

![Warning Email](/screenshots/warn_mail.png)

Other emails should follow such as alert, no data, and recovery emails.

* __Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:__
	* __One that silences it from 7pm to 9am daily on M-F,__
	* __And one that silences it all day on Sat-Sun.__
	* __Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.__

> For various reasons (upgrades, maintenance, etc.), you might be willing to schedule downtimes. This Datadog feature allows you to take off systems without triggering the related monitors.

To schedule a downtime, you need to remain in the “Monitors” section of Datadog Application side bar, to click on “Manage Downtime” and to hit the “Schedule Downtime” button.

You then need to follow Datadog Application UI and…
1.	Choose what to silence
2.	Schedule the downtime
3.	Add a message for the downtime
4.	Choose who should consequently be notified

Two downtimes were scheduled and two emails informing us from a downtime scheduling were received.

-	The first one to silence our my_metric monitor from 7pm to 9am daily from Monday to Friday.

![M-F Downtime](/screenshots/downtime1.png)

![M-F Downtime Email](/screenshots/downtime1_email.png)

-	The second one to silence our my_metric monitor on Saturday and Sunday.

![Weekend Downtime](/screenshots/downtime2.png)

![Weekend Downtime Email](/screenshots/downtime2_email.png)

People notified in downtime messages should also receive an email notification when the downtime begins.

![Downtime Beginning Email](/screenshots/downtime_begin.png)

More information about downtime scheduling:
https://docs.datadoghq.com/guides/monitors/#scheduling-downtime

## Collecting APM Data:

__Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:__

```python
from flask import Flask
import logging
import sys

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

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
    app.run()
```

__Note: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.__

> Datadog’s APM tool allows you to monitor, troubleshoot and optimize application performance. It provides greater visibility as it enables you to get information about the relationship between your application code and infrastructure.

To get started with Datadog’s APM, first hit “APM” in the side bar. In this example, we went for Python as the application we want to implement is a Flask application.

Begin with the installation of ddtrace `pip install ddtrace` to install the Python client. You might also need to install flask, logging and sys (depending on your previous python installation).

We decided to go with ddtrace-run but you could also have gone for the Middleware. If you  you do, you will have to install additional libraries (blinker, ddtrace) and create a TraceMiddleware object.
No matter what, just make sure not to use ddtrace-run with a manually inserted Middleware as it might cause issues.

If you’re on Mac OS X, remember to install the APM agent or you might run into a connection error such as…

![APM Agent Error](/screenshots/apmagent_error.png)

1.	Download the latest OSX Trace Agent release from here: https://github.com/DataDog/datadog-trace-agent/releases/tag/5.20.0
2.	Add the `apm_enabled: yes` parameter at the end of your datadog.conf file in order to enable the Agent.
3.	Enter the command line: `chmod +x trace-agent-osx` to transform the downloaded file in an executable one.
4.	Run the Trace Agent using the Datadog Agent configuration `./trace-agent-osx -ddconfig /opt/datadog-agent/etc/datadog.conf`
5.	You should then have your Trace Agent running in foreground looking like this:

![Trace Agent Running](/screenshots/trace_agent_running.png)

We then created our Flask application file, `flaskapp.py` that we ran using ddtrace-run python2 flaskapp.py command line in a new terminal.

```python
from flask import Flask
import logging
import sys

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

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
    app.run()
```

![Flask Application Running](/screenshots/flaskapp_run.png)

Once all of this is done, you just need to navigate between the different pages of the localhost to manually generate data:
-	http://localhost:5000/
-	http://localhost:5000/api/apm
-	http://localhost:5000/api/trace

Going back to Datadog UI, we can see that a new service appeared:

![Flask Application on UI](/screenshots/flaskapp.png)

More information about how to get started with Datadog APM tracing:
https://docs.datadoghq.com/tracing/
https://github.com/DataDog/datadog-trace-agent

More information about the Flask trace middleware:
http://pypi.datadoghq.com/trace/docs/#module-ddtrace.contrib.flask

More information about Flask:
http://flask.pocoo.org/docs/0.12/quickstart/

__Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.__

Once your APM is all set up and sends metrics, you can create a dashboard mixing both APM and Infrastructure metrics. 

In our example, we decided to try the Screenboard feature and to implement four graphs: two infrastructure ones (“PostgreSQL max connections” & “CPU idle”), and two APM ones (“Flask App Request Duration By Host” & “Flask App Requests Hits By HTTP Status”).

Link to dashboard:
https://p.datadoghq.com/sb/64875c795-e24793fe15

![Dashboard Combining Infrastructure and APM Metrics](/screenshots/infra_apm_dash.png)

More information about dashboards:
https://docs.datadoghq.com/graphing/dashboards/
https://docs.datadoghq.com/videos/datadog101-1-overview/
https://help.datadoghq.com/hc/en-us/articles/204580349-What-is-the-difference-between-a-ScreenBoard-and-a-TimeBoard-

__Bonus Question: What is the difference between a Service and a Resource?__

> If you look at Datadog APM into more details, you might bump into a specific terminology (trace, span, service, resource, type, name, app, etc.) that is worth investigating if you want to get the most of tracing. We will here focus on the difference between a service and a resource.

A service is defined as a “set of processes that work together to provide a feature set”. A service can therefore for instance be a web application, a database or a cache. Datadog monitors each service and then provide you with performance metrics such as requests duration, average latency, maximum latency, etc.

As for resources, they are defined as “particular queries to a service“. Resources are therefore the calls and traces making up a specific service. For a web application service, the resources are the entry points into the application (such as an URL visited by users). For a database, a resource is a SQL query like `select * from users where id = 1234`.

In our previous example, the service is therefore our Flask web application, which is made of three different resources that are the three different URLs we defined: api_entry, apm_endpoint & trace_endpoint.

![Difference Between Service and Resources](/screenshots/service_resources.png)

More information about Datadog tracing terminology:
https://docs.datadoghq.com/tracing/terminology/
https://help.datadoghq.com/hc/en-us/articles/115000702546-What-is-the-Difference-Between-Type-Service-Resource-and-Name-

## Getting Creative: 

__Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!__

__Is there anything creative you would use Datadog for?__

From the moment on you manage to collect the data, you can barely monitor whatever you want to monitor and there’s a ton of possible use cases.

If you are one of these animal nerds (no offense, I’m part of this team) for instance, you could totally decide to track your pet using a bit of electronics and Datadog. By adding some kind of Raspberry Pi to its collar and using sound analysis you could monitor if it is barking or not when you are away: here goes your brand-new home alarm system!

With the adapted sensors implementation, you could also help shops, public organizations, etc. monitor their waiting lines and why not have them send you an alert when one of the counter or cash desk is available.

There are as many Datadog use cases as you can think of it, so let’s get creative! 
