Your answers to the questions go here.
Your answers to the questions go here. Prerequisites - Setup the environment

I used an ubuntu instance and the easy one step install command : DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=16cf069063214b66b17d904a7e2e260d bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
Resource:https://docs.datadoghq.com/getting_started/agent/?tab=datadogussite

Verify that agent is working with the command:
'sudo datadog-agent status’

Documentation: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6v7

Collecting Metrics:

Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

I navigated to agent config using command :
$ sudo nano /etc/datadog-agent/datadog.yaml

Adding environment, platform, and host tag Documentation: https://docs.datadoghq.com/tagging/
Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

I installed Apache
$ sudo apt-get update $ sudo apt-get install apache2 $ sudo service apache2 status

Edit the apache.d/conf.yaml file in the conf.d/ folder at the root of the agent conf file
Documentation:https://github.com/DataDog/integrations-core/blob/master/apache/datadog_checks/apache/data/conf.yaml.example

Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Create new example_metric.py and example_metric.yaml using commands:
$ sudo nano /etc/datadog-agent/conf.d/example_metric.yaml $ sudo nano /etc/datadog-agent/checks.d/example_metric.py

-- Code in my_metric.py file

the following try/except block will make the custom check compatible with any$

try: # first, try to import the base class from new versions of the Agent... from datadog_checks.base import AgentCheck except ImportError: # ...if the above failed, the check is running in Agent version < 6.6.0 from checks import AgentCheck

content of the special variable version will be shown in the Agent status$

version = "1.0.0"

class MyCheck(AgentCheck): def check(self, instance): from random import randrange random_val = randrange(1000) self.gauge('my_metric', random_val)

Documentation: https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7

Change your check's collection interval so that it only submits the metric once every 45 seconds.

1)Cd into the custom metrics .yaml file using command:

$ sudo nano /etc/datadog-agent/conf.d/example_metric.yaml

2)Change min_collection_internal to 45:

init_config:

instances:

min_collection_interval: 45
Documentation:https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7

Bonus Question Can you change the collection interval without modifying the Python check file you created?

Yes, you can just edit the .yaml file. Alternatively you can edit it from the metrics summary page

Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

Your custom metric scoped over your host. Any metric from the Integration on your Database with the anomaly function applied. Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

from datadog import initialize, api

options = { 'api_key': 'xxxxx', 'app_key': 'xxxxx' }

initialize(**options)

title = 'My Timeboard 2' widgets = [{ 'definition': { 'type': 'timeseries', 'requests': [ {'q': 'avg:example_metric.count{*}'} ], 'title': 'Average Mem over my metric' } }] layout_type = 'ordered' description = 'A dashboard with memory info.' is_read_only = True notify_list = ['kristinatubera@gmail.com'] template_variables = [{ 'name': 'Kristina', 'prefix': 'host', 'default': 'my-host' }]

saved_views = [{ 'name': 'Saved views for hostname 2', 'template_variables': [{'name': 'host', 'value': '<HOSTNAME_2>'}]} ]

api.Dashboard.create(title=title, widgets=widgets, layout_type=layout_type, description=description, is_read_only=is_read_only, notify_list=notify_list, template_variables=template_variables, template_variable_presets=saved_views)

Documentation: https://docs.datadoghq.com/dashboards/guide/timeboard-api-doc/?tab=python and https://docs.datadoghq.com/api/v1/dashboards/#create-a-new-dashboard

Once this is created, access the Dashboard from your Dashboard List in the UI:

Set the Timeboard's timeframe to the past 5 minutes Take a snapshot of this graph and use the @ notation to send it to yourself.

Bonus Question: What is the Anomaly graph displaying? Monitoring Data

On the graph, the Anomaly will show any deviation o based on previous collected metrics. This could be a good graph for identifying inconsistencies or having a different behavior than expected.

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

Warning threshold of 500 Alerting threshold of 800 And also ensure that it will notify you if there is No Data for this query over the past 10m. Please configure the monitor’s message so that it will:

Send you an email whenever the monitor triggers.

Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state. I have included this in screenshots

When this monitor sends you an email notification, take a screenshot of the email that it sends you.

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

One that silences it from 7pm to 9am daily on M-F, And one that silences it all day on Sat-Sun. Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

I went into the GUI to make these changes and then sent in a screen shot.

Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

from flask import Flask import logging import sys

1)In order to run the Flask app, I first had to install pip3 and use it to install the flask dependency.

Next, I installed ddtrace and configured the trace environment variables as follows:

import os from ddtrace import tracer from ddtrace import config config.flask['distributed_tracing_enabled'] = True config.flask['service_name'] = 'custom-service-name' config.flask['extra_error_codes'] = [401, 403]

from ddtrace import patch_all patch_all()

from flask import Flask

app = Flask(name)

@app.route('/') def index(): return 'hello world'

if name == 'main': app.run(host='134.122.123.208')

Note: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

Bonus Question: What is the difference between a Service and a Resource?

Services are collections of resources. A resource can be a specific endpoint or job that makes up the service.

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

I'm really interested in the social network surrounding the online dating space. Due to covid-19, traffic to onling dating apps have significantly increased. I wondering if large dating app conglomerations know how much traffic each dating app sees on a day to day basis. If not, this could be useful to the dating app scene to better target their market based on which apps most people are active on based on the common demographic of the area.
