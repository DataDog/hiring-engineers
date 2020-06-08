# Datadog Set up for first time users

For those ofyou who may be new Datadog, Datadog is a monitoring service for cloud-scale applications, providing monitoring of servers, databases, tools, and services, through a SaaS-based data analytics platform. From infrastructure to apps, Datadog provides observability on any platform.

Below you will find a step - by - step guide for setting up DataDog and taking you through certain excercises for an Ubuntu instances. Enjoy and let me know if you have any questions.

## Prerequisites - Setup the environment

1) Datadog can be installed on an ubuntu instance with the easy one step install command : DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=16cf069063214b66b17d904a7e2e260d bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"

###### Documentation: Resource:https://docs.datadoghq.com/getting_started/agent/?tab=datadogussite

2) Verify that agent is working with the command:
'sudo datadog-agent status’

There are various other agent commands you can use as well to stop and restart the server and they can be found in the documenation below

###### Documentation: https://docs.datadoghq.com/agent/guide/agent-commands/?tab=agentv6v7

# Collecting Metrics:

## How to Add tags to your host

Datadog allows for you to add on your host to allow for further detailed descriptions.Tags are a way of adding dimensions to metrics, so they can be filtered, aggregated, and compared in Datadog visualizations. Essentially

1) Navigate to agent config using command :$ sudo nano /etc/datadog-agent/datadog.yaml

###### Note: depending on what platform you are using determins the location of the .yaml file

2) Add environment, platform, host tags etc. in the designated area the .yaml file

###### Documentation: https://docs.datadoghq.com/tagging/

## How to install a database on your machine and then install the respective Datadog integration for that database.

Datadog Integrations with the  Apache check tracks requests per second, bytes served, number of worker threads, service uptime, and more.

1) In this example I chose to installe Apache with the following command:
$ sudo apt-get update $ sudo apt-get install apache2 $ sudo service apache2 status

Edit the apache.d/conf.yaml file in the conf.d/ folder at the root of the agent conf file

###### Documentation:https://github.com/DataDog/integrations-core/blob/master/apache/datadog_checks/apache/data/conf.yaml.example

## How to create a Custom Agent Check that submits a metric named my_metric with a random value between 0 and 1000.

Custom checks are well suited to collect metrics from custom applications or unique systems

###### If you are trying to collect metrics from an open source project, it is recommended that you create a full fledged Agent Integration rather than a Custom Agent Check

1) Create new example_metric.py and example_metric.yaml using commands:

$ sudo nano /etc/datadog-agent/conf.d/example_metric.yaml 
$ sudo nano /etc/datadog-agent/checks.d/example_metric.py

-- Code in screenshot attached

###### Documentation: https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7

## Change your check's collection interval time 

Sometimes you only want the check to collect information within a certian time period, for this example, we have chosen for the check to be colleted every 45 seconds. To change the collection interval of your check, use min_collection_interval in the configuration file. The default value is 15.

###### Note: This does not mean that the metric is collected every 45 seconds, but rather that it could be collected as often as every 45 seconds. 

1)Cd into the custom metrics .yaml file using command:

$ sudo nano /etc/datadog-agent/conf.d/example_metric.yaml

2) Change min_collection_internal to 45:

-- Code in screenshot attached

###### Documentation: https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7


# Visualizing Data:

Timeboards have automatic layouts, and represent a single point in time—either fixed or real-time—across the entire dashboard. They are commonly used for troubleshooting, correlation, and general data exploration.

In this example we are going to utalize the Datadog API to create a Timeboard to contains the custom metric above scooped over the host. And the custom metric applied with the rollup function applied to sum up all the points for the past hour into one bucket


-- Code in screenshot attached.


Documentation: https://docs.datadoghq.com/dashboards/guide/timeboard-api-doc/?tab=python and https://docs.datadoghq.com/api/v1/dashboards/#create-a-new-dashboard

## Sending monitor triggers

Sending monitor triggers allows you to be alerted when certain requirments are met so that you dont have to continiually watch a certain metric or dashboard.

1) Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

2) Warning threshold of 500 Alerting threshold of 800 And also ensure that it will notify you if there is No Data for this query over the past 10m.

3) Please configure the monitor’s message so that it will:

Send you an email whenever the monitor triggers.

Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state. I have included this in screenshots

If this is done correctly you will be able to get e-mails notifications.

-- screenshots uploaded.



## Collecting APM Data:

Datadog APM & Distributed Tracing gives deep visibility into your applications with out-of-the-box performance dashboards for web services, queues and databases to monitor requests, errors, and latency. 

Datadog APM allows for : Service Map, Service Performance Dashobards, Live Tail, Connect Logs and Distributed Traces, App Analytics, Connect Synthetics and Traces, Continuous Profiling, Integrate with OpenTracing.


1) In order to run the Flask app, make sure to  install pip3 and use it to install the flask dependency.

from flask import Flask import logging import sys

2) Installed ddtrace and configured the trace environment variables as follows:

import os from ddtrace 
import tracer from ddtrace import config config.flask['distributed_tracing_enabled'] = True config.flask['service_name'] = 'custom-service-name' config.flask['extra_error_codes'] = [401, 403]

from ddtrace import patch_all patch_all()

from flask import Flask

app = Flask(name)

@app.route('/') def index(): return 'hello world'

if name == 'main': app.run(host='134.122.123.208')

###### Note: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.


# Frequently asked Questions:

## Can you change the collection interval without modifying the Python check file you created?

Yes, you can just edit the .yaml file. Alternatively you can edit it from the metrics summary page.

## What is the Anomaly graph displaying?

On the graph, the Anomaly will show any deviation o based on previous collected metrics. This could be a good graph for identifying inconsistencies or having a different behavior than expected.

## Can you schedule downtime for alerts if you don’t want to be alerted when you are out of the office?

Yes, you can set alerts that silence at any time. For me, I have one that silences it from 7pm to 9am daily on M-F, And one that silences it all day on Sat-Sun. 

I went into the GUI to make these changes and you can see an example in my my uploads.

## What is the difference between a Service and a Resource?

Services are collections of resources. A resource can be a specific endpoint or job that makes up the service.

## Datadog has been used in a lot of creative ways in the past. Is there anything creative you would use Datadog for?

I'm really interested in the social network surrounding the online dating space. Due to covid-19, traffic to onling dating apps have significantly increased. I wondering if large dating app conglomerations know how much traffic each dating app sees on a day to day basis. If not, this could be useful to the dating app scene to better target their market based on which apps most people are active on based on the common demographic of the area.
