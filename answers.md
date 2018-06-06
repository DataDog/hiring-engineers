The below documentation is a guide to my first steps with Datadog and covers a how to of collecting, visualising & monitoring data. Images and code can be found in directories on this branch for reference.

The below is based on an Ubuntu 16.04 local machine.
The pre-requisite is to install the Datadog agent on the local machine to allow reporting to your Datadog account, the install process is documented at [Datadog Docs - Agent](https://docs.datadoghq.com/agent/) to select your platform of choice. 

For the [Ubuntu installation](https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/) the Datadog Docs provides the single line of code for installation:

` DD_API_KEY=YOUR_API_KEY bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)`

Your API key can either be found at `https://app.datadoghq.com/account/settings#api` or using the "Install an Agent" step of the Datadog GUI "Get Started" wizard.

## Collecting Metrics:
#### 1. Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog

Tags provide the ability to easily query and correlate machines and metrics in Datadog. These can be configured automatically through Integrations, or manually though the Configuration file/GUI.

1.1 To add tags manually in the Agent config file, you first locate the .yaml config file for your platform [Datadog Docs - agent usage](https://docs.datadoghq.com/agent/basic_agent_usage/)

For Ubuntu, it is located at: `/etc/datadog-agent/datadog.yaml`. 
**Note: datadog.yaml requires sudo privileges to edit**

1.2 Follow [Datadog Docs- Assigning Tags](https://docs.datadoghq.com/getting_started/tagging/assigning_tags) to understand how to assign tags using the configuration files. It is recommended to follow [tagging best practices](https://docs.datadoghq.com/getting_started/tagging/#tags-best-practices)

Edit the datadog.yaml file by uncommenting the "tags" line and add your chosen tag; i.e "localhost:alishaw"

![datadog.yaml](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/assiging-tag-datadogyaml.png)

1.3 Save your edits to the configuration file and confirm them in the Datadog GUI by selecting your host in [https://app.datadoghq.com/infrastructure/map](https://app.datadoghq.com/infrastructure/map)

![hostmap](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/assigning-tag-HostMap.png)

#### 2. Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Datadog provides more than 200 built-in integrations for monitoring across systems, apps & services. 

2.1 To enable an Integration, navigate to [https://app.datadoghq.com/account/settings#integrations](https://app.datadoghq.com/account/settings#integrations) to view the available Integrations and select the one to configure. For example, the MongoDB Integration.

Clicking on an Integration will display an Overview description, Configuration steps & Metrics that are tracked.

2.2 Under the Configuration tab you will find the setup required for the MongoDB Integration. 

First, you need to create a read-only user in MongoDB for the Datadog Agent, these commands are run from the Mongo shell

![mongoDB integration step 1](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/MongoDB_Integration_1.png)

Second, you then edit the Integration config file at `/etc/datadog-agent/conf.d/mongo.d/mongo.yaml`

![mongoDB integration step 2](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/MongoDB_Integration_2.png)

Finally, restart the Datadog agent using `sudo service datadog-agent restart` and run a Check to confirm the Integration was successfully created.

The Integration will show as successful in the Datadog portal by marking the Integration as "Installed", as well as creating an event on the main Dashboard:

![mongoDB integrations](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/Integrations_tab_MongoDB.png)

![MongoDB on dashboard](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/MongoDB_installed.png)

![MongoDB yaml](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/MongoYAML.png)

#### 3. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000

Custom Agent checks are a way to collect metrics from custom applications or systems where a Datadog Integration does not already exist. They are run in the main Datadog Agent check run loop which, by default, is set to every 15 seconds.

For more information, follow the guide at [Datadog Docs - Agent Checks](https://docs.datadoghq.com/developers/agent_checks/)

Custom Agent Checks are made up of 2 files:
- A configuration .yaml file that goes in to `/etc/datadog-agent/conf.d`
- A python script .py file that goes in to `/etc/datadog-agent/checks.d`

**Important: the naming convention for both files must match**

3.1 Create the 'mymetric.yaml' configuration file in `/etc/datadog-agent/conf.d` with the simple configuration below. This contains no real information other than the instruction to initialise the configuration and run it for an undefined number of instances:

![mycheck.yaml](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/mycheck_yaml.png)

3.2 Create the 'mymetric.py' python file in `/etc/datadog-agent/checks.d` with the below to execute the code to Import the Random Module in Python, then Import the Datadog AgentCheck to inherit from, then define your check & randomly generate a number between 1 - 1000.

![mycheck.py](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/mycheck_py.png)

3.3 Once both files are created you can restart the Datadog Agent with `sudo service datadog-agent restart` then test your check by running:

`sudo -u dd-agent -- datadog-agent check mymetric` to test it runs without errors.

3.4 The metric can now be visualised in the Datadog portal by navigating to [https://app.datadoghq.com/metric/explorer](https://app.datadoghq.com/metric/explorer) and filtering by "my_metric" under "Graph":

![mycheck in GUI](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/mycheck_GUI.png)

*personal note: in this section, I struggled to understand why my check wasn't executing. Having not written Python extensively before, I based my code on the Datadog Docs example, then modified based on googling of the Python Random Module however didn't have the code in the correct order to execute in the right steps*

#### 4. Change your check's collection interval so that it only submits the metric once every 45 seconds.

To change the collection interval of a Custom Agent Check, you must edit the .yaml configuration file to include `min_collection_interval` as per below:

![collection interval change](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/mymetric_collectioninterval.png)

**Bonus question**: Using the method above, I did not need to edit my Python check file.

## Visualising Data:

The Datadog HTTP API allows a way to easily get data in and out of Datadog. The Datadog API uses resource-oriented URLs as well as status codes to indicate the success or failure of requests. It can be wrapped using multiple client libraries - either Phyton, Ruby or Curl. A reference guide can be found at [Datadog Docs - API Reference Guide](https://docs.datadoghq.com/api/). The below explanations are using Curl as the prefered language.

To visualise data in Datadog, users can create Dashboards to collate multiple metric feeds across systems and applications in to one single pane of glass.

There are 2 types of Dashboard:
1. Timeboard - All graphs visualised share a same time scope and is designed for troubleshooting and correlation of metrics & events.
2. Screenboard - All graphs visualised have individual time scopes and is designed for status boards and sharing data

For a full list of differences and further reading: [Datadog Docs - Dashboards](https://docs.datadoghq.com/graphing/dashboards/)

#### 5. Utilize the Datadog API to create a Timeboard

The Datadog API for interacting with Dashboards (creation, updating, deleting, getting information) is `https://api.datadoghq.com/api/v1/dash`

Before interacting with the Datadog API, you will need to locate 2 keys:

- api_key = unique to your organisation and is required by the Datadog Agent to submit metrics and events to Datadog
- app_key = used in conjunction with your api_key, give you full access to Datadog's programmatic API. They are associated with the user account that created them and are used to log all requests to the API.

You can find and generate these keys at: [https://app.datadoghq.com/account/settings#api](https://app.datadoghq.com/account/settings#api)

Once you have located these keys, follow the instructions at [Datadog Docs - API Reference for Timeboards](https://docs.datadoghq.com/api/?lang=bash#timeboards) to understand the argument structure for making API calls.

5.1 To create a Timeboard using the Datadog API using Bash:
`curl  -X POST -H "Content-type: application/json" \ -d`

Followed by the API call:

The script is made of 2 main components:

- `"graphs" [{}]` : Here you can define a number of graphs by giving them a title, definition and the request using `{"q": "YOUR_PARAMETERS"}
- After the graphs, the Timeboard is given a title & description

```
json
curl  -X POST -H "Content-type: application/json" \
-d '{
  "graphs" : [{
     "title": "My Metric Over Host",
     "definition": {
         "requests": [
			  {"q": "avg:my_metric{host:alishaw}"}
		  ]
     },
     "viz": "timeseries"
 },
 {
     "title": "MongoDB with anomalies",
     "definition": {
         "requests": [
             {"q": "anomalies(avg:mongodb.connections.available{host:alishaw}, 'basic', 2)"}
	     ]
	 },
     "viz": "timeseries"
 },
 {
     "title": "My Metric Rollup Sum",
     "definition": {
         "requests": [
             {"q": "avg:my_metric{host:alishaw}.rollup(sum, 3600)"}
		 ]
	 },
     "viz": "timeseries"
 }      
 ],
 "title" : "Alis Challenge Timeboard v2",
 "description" : "A timeboard to visualise my challenge",
 "template_variables": [{
     "name": "host1",
     "prefix": "host",
     "default": "host:my-host"
 }],
 "read_only": "True"
 }' \
"https://api.datadoghq.com/api/v1/dash?api_key=${api_key}&application_key=${app_key}"
```

*personal note: whilst I picked up the Datadog structure for the JSON file relatively quickly, the first few times I executed it my code failed. After some troubleshooting (Googling) I noticed errors in my code structure (mainly tabs/spacing) that would break my command.*

Note: the JSON configuration can also be found by creating a graph in the UI and selecting the JSON output tab:

![graph JSON](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/timeboardjson.png)

The API will acknowledge the success and the Timeboard will be created in the Datadog GUI at [https://app.datadoghq.com/dashboard/lists](https://app.datadoghq.com/dashboard/lists) :

![Dashboard list](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/dashboard_list.png)

5.2 Once you have created a Timeboard you can interact with is via the GUI:

5.2.1 Set the timeframe to the past 5 minutes:

The default time ranges for a Timeboard are found in the "show" dropdown above your graphs. To set the timeframe to a shorter period than the default Past Hour, hover your cursor over a graph, left click, drag and select a timeframe:

![Dashboard 5mins](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/timeboard_5mins.png)

5.2.2 Take a snapshot of the graph and use the @ notation to send it to yourself:

Datadog has a built in feature to screenshot specific graphs, annotate with comments and share them with individuals or teams. Simply hover over the graph, click the camera icon and write your comment using "@USERNAME" to send it to an individual.

![dashboard screenshot](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/timeboard_screenshot.png)

The user is then notified on their main dashboard:

![event screenshot](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/screenshot_event.png)

## Monitoring Data:

Datadog Monitors allow you to actively check key events/metrics across your infrastructure, systems and applications. Once a monitor is created, it can be configured to alert individuals or teams when conditions are met. It can also be integrated to 3rd party tools such as Slack via Webhooks. [Datadog Docs - Monitors](https://docs.datadoghq.com/monitors/)

To create a new Monitor, go to [https://app.datadoghq.com/monitors#/create](https://app.datadoghq.com/monitors#/create). Here you can chose from different Monitor types depending on what you want to monitor, [Datadog Docs - Monitor Types](https://docs.datadoghq.com/monitors/monitor_types/)

To create a Metric Monitor:
1. Choose the detection method - specify what event you are watching on your metric

2. Define the metric - specify the variables of your metric, host and other factors

3. Set alert conditions - specify the conditions that, if met, create an alert. See below for configuration of my alert

4. Say what's happening - specify individual messages based on which condition has been met. This section supports markdown for customising the message with relevant information about the metric value

5. Notify your team - specify who is alerted when the Monitor is triggered

![alert 1](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/alert_1.png)

![alert 2](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/alert_2.png)

When the Monitor is triggered, the users specified will receive an event notification on their Datadog main dashboard, as well as an email notification:

![alert 3](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/alert_3.png)

![alert 4](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/alert_4.png)

To avoid disruption of a Monitor during certain periods, you can schedule downtime for individual Monitors at [https://app.datadoghq.com/monitors#downtime](https://app.datadoghq.com/monitors#downtime) 

Create a new downtime schedule:
1. Choose which Monitors to silence

2. Define the schedule - either one time or recurring and specify dates/times

3. Add a message to notify team members - markdown is supported for detail

4. Select who to notify

Below are 2 examples of a weekday & weekend downtime schedule:

**Weekday downtime schedule with email notification**

![downtime 1](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/downtime_1.png)

![downtime 2](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/downtime_2.png)

![downtime 3](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/downtime_3.png)

**Weekend downtime schedule with email notification**

![downtime 4](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/downtime_4.png)

![downtime 5](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/downtime_5.png)

![downtime 6](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/downtime_6.png)


## Collecting APM Data:

Application Performance Management (APM) allows Datadog to provide deep insight into your application's performance side by side with your infrastructure monitoring and logs. Datadog will automatically generate dashboards monitoring key metrics, such as volume and latency, to detailed traces of individual requests. For more information, [Datadog Docs - APM](https://docs.datadoghq.com/tracing/)

*ddtrace* is Datadog's tracing client used to trace requests across applications. The ddtrace client is installed depending on your application language, Datadog currently provides official support for Python, Ruby, Go & Java - which can be installed at [https://app.datadoghq.com/apm/install](https://app.datadoghq.com/apm/install). There is also a library of community libraries available at [Datadog Docs - Developer Libraries](https://docs.datadoghq.com/developers/libraries/)

To instrument a Flask app, ensure you are running the latest Python, Flask and Blinker libraries:

`sudo apt-get install python3.6`

`sudo pip install flask`

`sudo pip install blinker`

Then, install the ddtrace python client:

`pip install ddtrace`

Then, instrument your application using the middleware by including the below in your my_app.py app:

```
import blinker as _

from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware
```

The fully instrumented my_app.py should look like this:

```
from flask import Flask
import logging
import sys
import blinker as _

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
    app.run(host='127.0.0.1', port=8080)
```

Next, run the application using:

`ddtrace-run python my_app.py`

*personal note: I encountered a port conflict issue when running the application, which I suspect was a conflict with the Datadog agent. I therefore included a host IP and port number in my my_app.py code*

Datadog will now automatically create an APM Service at [https://app.datadoghq.com/apm/services](https://app.datadoghq.com/apm/services) and automatically configure dashboard visualising Total Requests, Errors, Latency & Latency Distribution:

![APM1](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/APM1.png)

Individual graphs can then be exported to a Timeboard by clicking the export icon in the rop right hand corner:

![APM2](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/APM2.png)

Now - you can visualise infrastructure metrics alongside application data:

![APM3](https://github.com/ali-shaw/hiring-engineers/blob/ali-shaw-se/images/APM3.png)

## Final Question:

From a personal point of view - having completed this challenge & gained a greater understanding of Datadog's capabilities to monitor both infrastructure and application metrics I would like to instrument some of the tooling in my home automation setup. I often suffer broadband drops which interferes with responsiveness of smart appliances - I'd like to see if Datadog can capture anomalies in events triggering in an app and correlate it back to monitoring of network packet loss on my broadband router.

At a bigger scale - I can imagine a use case where Datadog can monitor metrics across traffic lights, CCTV capturing traffic flow and other variables to better understand metropolitan issues such as congestion and pollution.

Thank you for the opportunity & challenge.
Alastair
