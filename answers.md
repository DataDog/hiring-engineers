Your answers to the questions go here.

## Table of contents

- Setup the environment
- Collecting Metrics
- Visualizing Data
- Monitoring Data
- Collecting APM Data
- Final Question

## Setup the environment

In this readme file we will be going through a number of different Datadog features which will help you familiarize with the product and its offering. 

To start with you will need to download and install Vagrant [https://www.vagrantup.com/downloads]. You can choose your OS version and proceed with the setup instructions [https://learn.hashicorp.com/tutorials/vagrant/getting-started-index]. Once completed you will have a fully running virtual machine in VirtualBox running Ubuntu. 

_% brew upgrade

_% brew install vagrant
==> Downloading https://releases.hashicorp.com/vagrant/2.2.19/vagrant_2.2.19_x86_64.dmg
######################################################################## 100.0%
==> Installing Cask vagrant
==> Running installer for vagrant; your password may be necessary.
Package installers may write to any location; options such as `--appdir` are ignored.
Password:
installer: Package name is Vagrant
installer: Installing at base path /
installer: The install was successful.
🍺  vagrant was successfully installed!_

**Initialize Vagrant**

_% vagrant init hashicorp/bionic64
A `Vagrantfile` has been placed in this directory. You are now
ready to `vagrant up` your first virtual environment! Please read
the comments in the Vagrantfile as well as documentation on
`vagrantup.com` for more information on using Vagrant._

Setup the provider (such as VirtualBox) which Vagrant can interact with. Install based on your operating system. [https://www.virtualbox.org/wiki/Downloads]

To access your virtual machine use `vagrant ssh` to gain CLI access

_% vagrant ssh

Welcome to Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-58-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Sat Feb 19 14:52:16 UTC 2022

  System load:  0.21              Processes:           92
  Usage of /:   2.5% of 61.80GB   Users logged in:     0
  Memory usage: 11%               IP address for eth0: 10.0.2.15
  Swap usage:   0%

 * Super-optimized for small spaces - read how we shrank the memory
   footprint of MicroK8s to make it the smallest full K8s around.

   https://ubuntu.com/blog/microk8s-memory-optimisation

0 packages can be updated.
0 updates are security updates.__

Please follow [https://app.datadoghq.eu/account/settings#agent/ubuntu]  the installation instructions for ubuntu to setup the Datadog agent locally into vagrant.

<img width="721" alt="datadog_agent_status" src="https://user-images.githubusercontent.com/57485310/154828943-31668fb6-7dcb-4a72-9508-4529ecd59418.png">

## Collecting Metrics

### Adding Tags in the Agent config

To add tags to the Agent config file, locate the file as per platform. More details in the document [https://docs.datadoghq.com/agent/guide/agent-configuration-files/?tab=agentv6v7]

Documentation on assigning tags can be found here [https://docs.datadoghq.com/getting_started/tagging/assigning_tags/?tab=noncontainerizedenvironments].

Over here we are going to create tags via commandline. Please note that as we have followed the easy install, most of the below steps have already been done. 

1) Open the configuration file 

_vi /etc/datadog-agent/datadog.yaml
_
Set the relevant tags that you need. 

<img width="821" alt="tags_config_file" src="https://user-images.githubusercontent.com/57485310/154828985-b55af8e2-399f-4d9a-a720-fb2ec4fa6932.png">

2) You will need to get your API key which can be found under Organization Settings[https://app.datadoghq.eu/organization-settings/api-keys]. API keys are unique to the organization. An API key is required by the Datadog Agent to submit metrics and events to Datadog.

Once you have the key, you need to put that into the agent config file. 

![api_key](https://user-images.githubusercontent.com/57485310/154829013-b3e39670-b758-4c54-b673-88fb1e31bcff.png)

<img width="582" alt="api_key_config_file" src="https://user-images.githubusercontent.com/57485310/154829017-761ac3e8-b1af-4a00-8485-9ddad7e13f32.png">

3) If you have registered to Datadog EU, you will need to set the 'site' and 'dd_url' accordingly, else the agent will experience problems authenticating with Datadog 

<img width="711" alt="site_location_config_file" src="https://user-images.githubusercontent.com/57485310/154829054-21a09798-a2fa-47f0-bfa1-64e2c194ff66.png">


4) After you have made the changes, you will need to restart the agent service for changes to take effect. More information on the commands can be found here [https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/?tab=agentv6v7]

_sudo service datadog-agent restart_

5) You can verify if the changes have been applied by checking the Host Map under Infrastructure [https://app.datadoghq.eu/infrastructure/map?fillby=avg%3Acpuutilization&groupby=availability-zone&host=171013805]

![tagging](https://user-images.githubusercontent.com/57485310/154829073-b7bedb5e-a354-4b14-aceb-eaf6f101a142.png)

### Install DB and its Integration 

1) We will install MySql DB on our VM. Update package information and then run the install command. 

_$ sudo apt update
_
_$ sudo apt install mysql-server
_
On completion, check the status of the mysql service: 

_$ sudo service mysql status
_

<img width="880" alt="mysql_status_cli" src="https://user-images.githubusercontent.com/57485310/154829094-720a1b1f-1fca-45e8-942d-5915a131efdc.png">

2) Now we can login into the Mysql as root. Follow the documentation [https://docs.datadoghq.com/integrations/mysql] for Integration and allow Datadog to collect metrics. 

We also need to create a conf.yaml file under /etc/datadog-agent/conf.d/mysql.d and change the host and update the password. After making the change, restart the datadog agent and check mysql status to verify if the monitoring is set correctly. 

_sudo service datadog-agent restart
_sudo datadog-agent status_

<img width="783" alt="agent_mysql_status_cli" src="https://user-images.githubusercontent.com/57485310/154829121-5f4657cd-e43a-47f2-9cf9-55b1c838fcf0.png">

3) Now as the Agent has been setup correctly, please ensure that we install Mysql integration in Datadog to start the monitoring for Mysql. Please refer [https://app.datadoghq.eu/account/settings#integrations/mysql]

![mysql_integration](https://user-images.githubusercontent.com/57485310/154829130-395cce47-7630-4783-9b54-4c9498450ebb.png)

4) Now you can view the MySql Dashboard. Dashboard > Dashboard List > MySQL - Overview 

Link to the dashboard - 
https://app.datadoghq.eu/dash/integration/9/mysql---overview?from_ts=1645285653726&to_ts=1645289253726&live=true

![mysql_dashboard](https://user-images.githubusercontent.com/57485310/154829143-7ed03d5f-6384-4924-a08b-f97571a40f88.png)

### Create custom Agent check 

We will create a custom agent check following the document [https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7] 
This agent will submit a custom metric called `my_metric` submitting a random values between `0` and `1000` running on set interval.

1) Create the script mymetric.py under _/etc/datadog-agent/checks.d_ directory

```python
import random
from checks import AgentCheck
class RandomCheck(AgentCheck):
 def check(self, instance):
   self.gauge('my_metric', random.randint(0, 1000))
```

2) Next you will create the mymetric.yaml file under _/etc/datadog-agent/conf.d_ directory which will define the interval when the value will be collected at. 

```yaml
init_config:

instances:
  - min_collection_interval: 45
```

3) Restart the agent. 

_sudo service datadog-agent restart_

4) You should be seeing "my_metric" in the Metric Explorer (Metrics > Explorer). Setting the Graph value to my_metric. 

Here is the link to the Metrics Explorer [https://app.datadoghq.eu/metric/explorer?from_ts=1645311533229&to_ts=1645313333229&live=true&tile_size=m&exp_metric=my_metric&exp_agg=avg&exp_row_type=metric]


<img width="1280" alt="my_metric_graph" src="https://user-images.githubusercontent.com/57485310/154829196-03c4afc6-89f5-47f6-b878-9aa48d59208b.png">

### Change checks collection interval

- If you would like to change this without modifying the Python check file, you can do it on the Datadog UI: 
- Datadog UI > Metrics > Summary. Link here for Metric Summary [https://app.datadoghq.eu/metric/summary?filter=my_me&metric=my_metric]
- Search the metric you are looking for (my_metric).
- Click edit on the window that pops up. 
- Set the Interval & Save. 
More information on Metric Summary can be found here [https://docs.datadoghq.com/metrics/summary/]

<img width="1422" alt="metric_summary_update_interval" src="https://user-images.githubusercontent.com/57485310/154829210-b159dd69-151c-424b-85eb-35a4028d7ea9.png">

Another way to change the interval is in the mymetric.yaml config file, without modifying the python file. 

```yaml
init_config:

instances:
  - min_collection_interval: 45
```

More information on updating collection interval can be found here [https://docs.datadoghq.com/developers/custom_checks/write_agent_check/#updating-the-collection-interval]

## Visualizing Data:

In this section we will visualize the data from our agents using the dashboard in the Datadog UI. Dashboard is Datadog’s tool for visually tracking, analyzing, and displaying key performance metrics, which enable you to monitor the health of your infrastructure. We will create a custom dashboard to capture metrics for our DB along with the custom metric "my_metric". 

### Create Dashboard 

You can create dashboard using the API. I went ahead with the Python exampple mentioned in the documentation [https://docs.datadoghq.com/api/latest/dashboards/]

1) In order to install Datadog Libraries run the below command - 
_pip3 install datadog
_
In order to install datadog api client run command - 
_pip3 install datadog-api-client_

2) You will need your API key and App key under the Organization Settings [https://app.datadoghq.eu/organization-settings/api-keys] [https://app.datadoghq.eu/organization-settings/application-keys]

3) We will create the dashboard to show 3 graphs:

- The custom metric "my_metric" scoped over the host.
- Any metric from the Integration on the Mysql Database with the anomaly function applied. Refer this doc for anomalies query [https://docs.datadoghq.com/dashboards/functions/algorithms/#anomalies] and detection algorithm is used as Basic via referring to this document [https://docs.datadoghq.com/monitors/create/types/anomaly/#anomaly-detection-algorithms]
- The custom metric "my_metric" with the rollup function applied to sum up all the points for the past hour into one bucket. Documentation [https://docs.datadoghq.com/dashboards/querying/#rollup-to-aggregate-over-time]


```python
from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.dashboards_api import DashboardsApi
from datadog_api_client.v1.model.dashboard import Dashboard
from datadog_api_client.v1.model.dashboard_layout_type import DashboardLayoutType
from datadog_api_client.v1.model.timeseries_widget_definition import TimeseriesWidgetDefinition
from datadog_api_client.v1.model.timeseries_widget_definition_type import TimeseriesWidgetDefinitionType
from datadog_api_client.v1.model.timeseries_widget_request import TimeseriesWidgetRequest
from datadog_api_client.v1.model.widget import Widget
from datadog_api_client.v1.model.widget_sort import WidgetSort
body = Dashboard(
    layout_type=DashboardLayoutType("ordered"),
    title="Sales Engineer Test Dashboard",
    widgets=[
        Widget(
            definition=TimeseriesWidgetDefinition(
                type=TimeseriesWidgetDefinitionType("timeseries"),
                title="Custom Metric",
                requests=[
                    TimeseriesWidgetRequest(
                        q="my_metric{host:vagrant}"
                        )
                ],
            )
        ),
        Widget(
            definition=TimeseriesWidgetDefinition(
                type=TimeseriesWidgetDefinitionType("timeseries"),
                title="Anomaly graph - Average MySQL CPU time (per sec)",
                requests=[
                    TimeseriesWidgetRequest(
                        q="anomalies(avg:mysql.performance.user_time{host:vagrant}, 'basic', 2)"
                        )
                ],
            )
        ),
        Widget(
            definition=TimeseriesWidgetDefinition(
                type=TimeseriesWidgetDefinitionType("query_value"),
                title="Custom Metric graph with rollup function to sum up all points in last hr",
                requests=[
                    TimeseriesWidgetRequest(
                        q="my_metric{host:vagrant}.rollup(sum,3600)"
                        )
                ],
            )
        )
    ],
)

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = DashboardsApi(api_client)
    response = api_instance.create_dashboard(body=body)

    print(response)
```

First install the library and its dependencies and then save the dashboard python code to dashboard.py and run following commands:

_export DD_SITE="datadoghq.eu" DD_API_KEY="<DD_API_KEY>" DD_APP_KEY="<DD_APP_KEY>" python3 "dashboard.py"
_

**Link to the Dashboard** (public sharing On)[https://p.datadoghq.eu/sb/5d1c77de-9192-11ec-9027-da7ad0900005-5f3ff30d21e983629a5a88f546231abf]

<img width="1427" alt="sales_engineer_dashboard" src="https://user-images.githubusercontent.com/57485310/154829339-918608b5-cf0b-4b0d-b3ea-4e6ad07743c5.png">

### Set the Timeboard's timeframe to the past 5 minutes

If you want to see what happened in the past 5 minutes in our graphs, you can go to the top right corner in the Datadog UI and set a custom time or select Past 5 minutes. More information on this can be found here [https://docs.datadoghq.com/dashboards/guide/custom_time_frames/]

<img width="1426" alt="five_min_timeframe" src="https://user-images.githubusercontent.com/57485310/154829350-9201cdd3-c2d6-4b5f-898d-ff80806f41e8.png">

### snapshot of this graph and use the @ notation to send it to yourself.

We will take the snapshot of the Anomalies graph. This can be done by clicking on the graph and press Send Snapshot button. 

<img width="1435" alt="send_snapshot" src="https://user-images.githubusercontent.com/57485310/154829366-8ee97648-426d-435b-8d5c-7274f0721f0f.png">

Then type your email address and press submit. Check your mail box now. 

![snapshot_email](https://user-images.githubusercontent.com/57485310/154829392-d5c84226-35df-4ed3-8160-c970051ae805.png)

### Bonus Question: What is the Anomaly graph displaying?

Anomaly graph helps in identifying if the metric is behaving differently than it has in the past. It helps you in providing deeper context, by analyzing the historical behavior. Anything marked in red should be investigated. 

<img width="635" alt="anomaly_graph_display" src="https://user-images.githubusercontent.com/57485310/154829402-6079d2b0-407f-4c10-b626-7017d25c3eac.png">

## Monitoring Data

Metric monitors are useful for a continuous stream of data. Any metric sent to Datadog can be alerted upon if they cross a threshold over a given period of time. In this section, we are going to create a Metric Monitor that watches the average of our "my_metric" and will alert based on threshold. More information in the Metric Monitor documentation [https://docs.datadoghq.com/monitors/create/types/metric/?tab=threshold]

In order to create one in the Datadog UI: [https://app.datadoghq.eu/monitors/create]

<img width="1408" alt="create_new_monitor" src="https://user-images.githubusercontent.com/57485310/154829411-82615efa-2628-4310-8575-9ffce1b0c80d.png">

Monitors > New Monitor 

This will bring you to a new window where you can define the metric and set threshold conditions:  

Warning threshold of 500
Alerting threshold of 800
Notification if there is No Data for this query in the past 10 minutes

Set yourself or the person you want to notify when an alert is triggered. This will send an email to the email address specified. 


<img width="1152" alt="metric_monitor_setup1" src="https://user-images.githubusercontent.com/57485310/154829429-9f515d03-d944-4a5d-8600-6d094b67b386.png">

<img width="1176" alt="metric_monitor_setup2" src="https://user-images.githubusercontent.com/57485310/154829432-b8753726-e58a-41ca-9d35-98da27d8d768.png">

<img width="1433" alt="metric_monitor_setup3" src="https://user-images.githubusercontent.com/57485310/154829454-c7cd32c7-52c1-4638-ad78-f311958133ce.png">

Now you can go to Manage Monitors [https://app.datadoghq.eu/monitors/manage] and see the new monitor you just created. [https://app.datadoghq.eu/monitors/4517869]

We will be adding additional logic to our monitors notification to have a better understanding on whats causing the trigger. The information we will add is - 

- Different message for 'Alert', 'Warning' and 'No Data'
- The 'metric'value that caused the notification
- The 'IP Address' of the host. 

In order to achieve this, you can use notification [https://docs.datadoghq.com/monitors/notifications/?tab=dashboards]. Updated notification that I have used - 

---
{{#is_alert}} Alert was triggered for my_metric. It has reached the 800 threshold in past 5 minutes {{/is_alert}} 
{{#is_warning}} Warning was triggered for my_metric. It has reached the 500 threshold in the past 5 minutes {{/is_warning}} 
{{#is_no_data}} No Data was sent for my_metric in the past 10 minutes {{/is_no_data}} 

Details: Metric Current Value is: {{value}} and Host IP is: {{host.ip}}

@virmani.gaurav@yahoo.com
----

Below is the screenshot of the warning email notification that the monitor sends. It includes the metric value which caused the monitor to trigger and the IP of the host. 

![warning_email_notification](https://user-images.githubusercontent.com/57485310/154829561-db512101-268a-4892-b780-02a3cfff67bd.png)

Now we want to take this to next level and ensure that we are not notified during out of office hours. So I will setup a Scheduled Downtime for this monitor.  

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor. More information in the documentation [https://docs.datadoghq.com/monitors/notify/downtimes/?tab=bymonitorname]. 

I will set the following parameters: 
- No notifications from 7pm to 9am daily on M-F. 
- No notifications on Sat-Sun.

You can go to Monitors > Manage Downtimes [https://app.datadoghq.eu/monitors#/downtime)] and click on Schedule Downtime on the top right corner. 

<img width="1433" alt="schedule_downtime_right_corner" src="https://user-images.githubusercontent.com/57485310/154829578-97fec156-4e35-4eb3-a902-5c220c1049a3.png">

Create the weekday downtime [https://app.datadoghq.eu/monitors/downtimes?id=96500141&sort=-start_dt]


<img width="856" alt="downtime_weekday1" src="https://user-images.githubusercontent.com/57485310/154829589-c819470c-a1f8-4b4f-8a0e-8542db630308.png">

<img width="866" alt="downtime_weekday2" src="https://user-images.githubusercontent.com/57485310/154829593-1db37f89-ecec-475d-b742-5ae5561ea636.png">

<img width="714" alt="downtime_weekday3" src="https://user-images.githubusercontent.com/57485310/154829595-6f5c6033-8b3b-4d64-860c-24e83467bb50.png">


Create the weekend downtime [https://app.datadoghq.eu/monitors/downtimes?id=96500775&sort=-start_dt]

<img width="925" alt="downtime_weekend1" src="https://user-images.githubusercontent.com/57485310/154829606-d0044811-ab09-4bf6-a37e-ab399ad8a72b.png">

<img width="865" alt="downtime_weekend2" src="https://user-images.githubusercontent.com/57485310/154829609-e723d680-2a17-4312-a93f-d3920104f2ba.png">

<img width="715" alt="downtime_weekend3" src="https://user-images.githubusercontent.com/57485310/154829614-65cd8729-cbf0-4161-bcc6-b466dab4bada.png">


The recipients will recieve email confirmation once this is completed. 

![downtime_weekday_confirmation](https://user-images.githubusercontent.com/57485310/154829626-d901421d-3467-4ecd-9798-c7533d824a5e.png)

![downtime_weekend_confirmation](https://user-images.githubusercontent.com/57485310/154829631-6644c177-d3e2-4f6e-a956-04a05bf21ce3.png)

_*NOTE* The weekend downtime cannot be scheduled in the past, so I have set the start date as 26 Feb 2022 (Saturday). 
_

## Collecting APM Data

In this section we will cover Application performance monitoring. [https://www.datadoghq.com/product/apm/]

### Setup the Dashboard and Collect APM Metrics

We will create a simple APM dashboard. The documentation [https://docs.datadoghq.com/getting_started/tracing/] guides us how APM is used to collect traces from the backend application code. We want to make sure that we see the Traces and those metrics are included in the Infrastructure metrics dashboard. 

- Verify if the APN is enabled (Note: For the latest versions of Agent v6 and v7, APM is enabled by default)

_sudo datadog-agent status
_

<img width="534" alt="apm_agent_status" src="https://user-images.githubusercontent.com/57485310/154829660-d216d18f-867e-4a67-b231-e53d45325e94.png">

- We will need to setup flask and ddtrace. For this purpose we will use pip. 

sudo apt update

sudo apt install -y python3-pip git

pip3 install --upgrade pip

pip3 install flask

pip3 install cmake ninja

pip3 install ddtrace


- We will create the flask_app using the code provided: 

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
    app.run(host='0.0.0.0', port='5050')
```

- We will need to define a service

_export DD_SERVICE=custom_service
_
- Now run the application using ddtrace which wil automatically instrument it to Datadog.

_ddtrace-run python3 flask_app.py
_
- If everything ran successfully you should see a message simialr to below

<img width="955" alt="app_successfull" src="https://user-images.githubusercontent.com/57485310/154829703-3d601eb4-b034-4fbd-b654-497f76649754.png">

- Verify that the application is running by doing a curl 

_vagrant ssh
curl http://0.0.0.0:5050/
OR
curl http://10.0.2.15:5050/_

This should give the following output: 
Entrypoint to the Application 

<img width="1433" alt="Entrypoint_to_the_app" src="https://user-images.githubusercontent.com/57485310/154829724-9e6fb707-4568-4973-97c8-c38c1578e05d.png">

<img width="1423" alt="debug" src="https://user-images.githubusercontent.com/57485310/154829747-8fae935e-59ba-4450-af76-ffa23c196db0.png">

### APM Services and Traces 

Now the flask application is running, we can go to the Datadog UI > APM services > Traces [https://app.datadoghq.eu/apm/traces]. Here you can check if you are recieving data from the host. 

Here is the URL after clicking into the Traces and then the specific Get request - 

https://app.datadoghq.eu/apm/traces?query=env%3Avagrant&cols=core_service%2Ccore_resource_name%2Clog_duration%2Clog_http.method%2Clog_http.status_code&historicalData=false&messageDisplay=inline&sort=desc&spanID=18198208225065098192&streamTraces=true&timeHint=1645328658154&trace=1182086653194275141318198208225065098192&traceID=11820866531942751413&start=1645327999676&end=1645328899676&paused=false

<img width="1422" alt="custom_service" src="https://user-images.githubusercontent.com/57485310/154829767-c30af059-892c-4476-aa88-c55c66e7ec73.png">

<img width="1423" alt="traces" src="https://user-images.githubusercontent.com/57485310/154829775-fe7a62f3-837f-4a67-b434-4b9f9f9a18e5.png">

### APM and Infrastructure Metrics - Dashboard

Create a new timeboard (Dashboard -> New Dashboard -> Timeboard). Export all the custom service metrics into this new Dashboard. 
For adding the App Metrics, edit any of the widgets on the Dashboard, select the correct flask metric whichever you need under "Graph your data", and save it as New Graph. 
Your Dashboard is ready !!

https://p.datadoghq.eu/sb/5d1c77de-9192-11ec-9027-da7ad0900005-6f8a4eb2ec65d25a5d8629c0f86cdfe7

![apm_infra_dashboard](https://user-images.githubusercontent.com/57485310/154829798-8dc96f06-cad0-4c00-b996-352c7beb05ed.png)

### Bonus Question: What is the difference between a Service and a Resource?
A Service is a process or a set of processes that work together to provide a feature set. Example: Nginx, Apache
A Resource is a function that would run on or use the service. Example: Web Request. 

Detailed information on Service and Resource: 
https://docs.datadoghq.com/tracing/visualization/#services
https://docs.datadoghq.com/tracing/visualization/#resources

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!
Is there anything creative you would use Datadog for?

>>> I am deep into Equity Research and Investing. Not everything is meant to be long term hold and I do frequent selling as well as some businesses are cyclic such as commodities (I am not a trader though). 
Given the amount of Historical data and lot of technical indicators we have, it would be exciting to build a solution that would execute your orders (Sell/Buy), based on those indicators (200DMA, RSI, etc). Datadog can be used to plot those metrics and implment such a solution which would save time for an investor/trader always looking into the Charts. This can further be enhanced to support Fibonacci retracement levels which are key indicators. 
