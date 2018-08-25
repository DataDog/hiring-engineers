# About Datadog

Datadog is a monitoring service for modern applications that combines both infrastructure monitoring (servers, containers, databases, etc.) as well as application performance monitoring through a SaaS-based service.

# The Technical Challenge 

## Prerequisites - Setup the environment

In order to have no interference with installed products on my laptop, I have chosen to use a Vagrant VM with Ubuntu 16.04.

The Vagrant file is very simple and uses an ubuntu/trusty64 image.

```
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
end
```

A trial version of datadog is available for 14 days via https://www.datadoghq.com/.

The installation of the datadog agent on Ubuntu is outlined in the documentation: https://docs.datadoghq.com/agent/basic_agent_usage/ubuntu/. It can be performed with a single command:

```
DD_API_KEY=YOUR_API_KEY bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

## Collecting Metrics

### Creating Tags

Tags allow the easy identifcation as well as filtering in the frontend. In order to add tags, the followig modifications have been done to ```/etc/datadog-agent/datadog.yaml```:

```
# Set the host's tags (optional)
tags:
  - instance:datadog_hiring
  - name:ubuntu_vm
  - env:dev
  - role:database
```

The Infrastructure Map shows the following details about the virtual machine (https://app.datadoghq.com/infrastructure/map?host=569857949&fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host):

![Screenshot Infrastructure Map](images/screenshot_host_with_tags.png)

### Integration for MongoDB

In order to demonstrate an integration, I have installed MongoDB as well as the Datadog Integration to monitor the database.

The necessary steps for MongoDB are:

```
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list
sudo apt-get update
sudo apt-get install -y mongodb-org
```

The installation of the MongoDB integration does not need additional steps, as it the code is already included in the datadog agent. The necessary configuration is well documented: https://docs.datadoghq.com/integrations/mongo/ and results in the following `/etc/datadog-agent/conf.d/mongo.d/conf.yaml`. As it is a demonstration system, no user authentication and authorization has been enforced in MongoDB. In a production environment, the `datadog` user should have read-only privileges in MongoDB aus outlined in the documentation:

```
init_config:

instances:
  # Specify the MongoDB URI, with database to use for reporting (defaults to "admin")
  # E.g. mongodb://datadog:LnCbkX4uhpuLHSUrcayEoAZA@localhost:27016/my-db
  - server: mongodb://localhost:27017/admin
```

As soon as the agent has been restarted (`sudo restart datadog-agent`), the MongoDB dashboard is available (https://app.datadoghq.com/screen/integration/13/mongodb?page=0&is_auto=false&from_ts=1535181360000&to_ts=1535184960000&live=true):

![Screenshot MongoDB Dashboard](images/screenshot_mongodb_dashboard.png)

### Collecting Custom Metrics via an Agent Check

An Agent Check allows for a straightforward integration of custom metrics. If metrics of a standard product should be integrated, it is advisable to create an Integration. New Integrations can be published and are easier to be reused.

Writing an Agent Check requires two files: `<CHECK_NAME>.yaml` for configuration as well as `<CHECK_NAME>.py` as the actual implementation. For the `my_metric` implementation, the following two files have been used. In order to use proper naming in the Datadog dashboards, the prefix `hiring` has been usded to identify the custom metric. Without a prefix a generic `no name` would have been shown, for example, as an application name in the host map.

`/etc/datadog-agent/conf.d/mycheck.yaml`:
```
init_config:

instances:
  - test:
    min_collection_interval: 45
```

`/etc/datadog-agent/checks.d/mycheck.py`:
```
from checks import AgentCheck
import random

# Custom Checks are inherit AgentCheck
class MyCheck(AgentCheck):
    
    # Automatically send a metric
    def check(self, instance):
     
        # We've chosen my_metric with a random value between 0 and 1000
        self.gauge('hiring.my_metric', random.randint(0, 1000))
```

The `min_collection_interval` allows to configure that the metric is not sent to Datadog every 15-20 seconds (which is the standard interval of sending metrics - depending on the amount of metrcis to be sent by the agent). The minimal collection intervall ensures that during the first execution (at second 15, counter is 0 seconds) the metric is sent. In the second iteration, the current time is 30 seconds, which is less than the minimun interval of 45 seconds - therefore, no metric is sent. In the third execution, the counter is at 45 seconds, which leads to another execution of the agent check and sends a new value to Datadog.

After restarting the datadog agent, the `hiring` app shows up in the host map and some values are transferred:

![Screenshot Agent Check](images/screenshot_host_map_hiring_app.png)

## Visualizing Data

The Datadog API allows to automate any interaction which is very useful for automation, especially in large environments.

In order to solve the challenge, I leveraged the python API. This resulted in the following script to create the timeboard `initialize_new_timeboard.py`:

```python
from datadog import initialize, api

options = {
    'api_key': 'XXXXXXdfef6bec6dcfc6f15a8d4ec379',
    'app_key': 'XXXXXXccf02dccbf91c631eabf8391e29081adc7'
}

initialize(**options)

title = "Hiring Timeboard"
description = "A Dashboard with custom metric from agent check as well as anomaly function for MongoDB."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {
                "q": "avg:hiring.my_metric{host:vagrant-ubuntu-trusty-64}",
                "type": "line",
                "metadata": {
                    "avg:hiring.my_metric{host:vagrant-ubuntu-trusty-64}": {
                      "alias": "my_metric"
                    }
                },
                "style": {
                    "palette": "grey",
                    "type": "solid",
                    "width": "normal"
                }
            },
            {
                "q": "avg:hiring.my_metric{host:vagrant-ubuntu-trusty-64}.rollup(sum, 3600)",
                "type": "bars",
                "metadata": {
                    "avg:hiring.my_metric{host:vagrant-ubuntu-trusty-64}.rollup(sum, 3600)": {
                        "alias": "my_metric_sum_by_hour"
                     }
                },
                "style": {
                    "palette": "cool",
                    "type": "solid",
                    "width": "normal"
                }
            },
            {
                "q": "anomalies(avg:mongodb.connections.totalcreated{host:vagrant-ubuntu-trusty-64}, 'basic', 1)",
                "type": "line",
                "metadata": {
                    "anomalies(avg:mongodb.connections.totalcreated{host:vagrant-ubuntu-trusty-64}, 'basic', 1)": {
                        "alias": "mongodb_connections_anomalies"
                     }
                }
            }

        ],
        "viz": "timeseries"
    },
    "title": "My Metric and MongoDB Connections Created"
}]

template_variables = []

read_only = True

result = api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)

print (result)
```

The necessary API and App keys can be found and generated in the account settings: https://app.datadoghq.com/account/settings#api.

I have chosen to display all three metrics in one time series to show how combined graphs can be created. Please find the dashboard here: https://app.datadoghq.com/dash/896649/hiring-timeboard?live=true&page=0&is_auto=false&from_ts=1535013798779&to_ts=1535186598779&tile_size=m.

The collaboration feature allows to take shanpshots of graphs, annotate them, and add collaborators with the `@<EMAIL_ADDRESS>` syntax. They get automaticall notified via email as the screenshot below shows:

![Screenshot Email Collaboration](images/screenshot_collaboration.png)

As an alternative, the three metrics can be shown individually, please see the dashboard here: https://app.datadoghq.com/dash/897488/hiring-timeboard---three-graphs?live=true&page=0&is_auto=false&from_ts=1535013848866&to_ts=1535186648866&tile_size=m

![Screenshot More Detailled Metrics](images/screenshot_hiring_timeboard_three_graphs.png)

### Anomaly Function

The latter screenshot above shows the anomaly function for the total number of opened connections to MongoDB. This value is constantly increasing. 

An anomaly functions applies algorithms to a metric in order to determine a corridor of normal behaviour. The breath of the corridor, i.e. the standard deviation from the normal value, can be adjusted. Three different algorithms can be chosen: "Basic" uses an algorithm that does not consider seasonal patterns. "Agile" includes the most recent changes of a metric. "Robust" considers a seasonal trend decompositiong algorithm. The screenshot below summarizes the explanation and shows the metric value, the automatically calcualted bands of normal behavior as well as an anomaly - the metric leaves the corridor of normal behavior.

![Anomaly](images/screenshot_anomaly.png)

## Monitoring Data

The monitor on `my_metric` has been created with the following text in order to send different email notifications if it is a warning, an error, or a no-data notification:

```
Please double-check the application, as my_metric is suspicious.

{{#is_warning}} This is just a warning, so take action to reduce the value. {{/is_warning}}

{{#is_alert}} Please take immediate action to avoid application outages.

Host IP: {{host.ip}} My Metric value: {{hiring.my_metric}} {{/is_alert}}

{{#is_no_data}} There has not been data for 10 minutes. Please double-check the system. {{/is_no_data}}

@<EMAIL_TO_BE_NOTIFIED>
```

The monitor (https://app.datadoghq.com/monitors/6082465) is configured as following:
![Monitoring Configuration](images/screenshot_monitoring.png)

A notification is sent our frequently, the screenshot shows a warning, as the value of my_metric went above 500:
![Monitoring Notification](images/screenshot_monitor_notification.png)

The downtime allows to snooze notifications. There are two downtimes configured - one for weekdays from 7pm to 9am as well as for the whole day on Sat and Sun. It works well as the email below shows the notification for downtime during the night of weekdays:
![Monitoring Downtime Notification](images/screenshot_downtime_notification_weekdays.png)

## Collecting APM Data

In order to trace the flask app, I integrated the Flask tracing middleware into the Python code itself as documented in https://docs.datadoghq.com/tracing/setup/python/. In addition, the following lines needed to be modified in the `datadog.yaml` file to enable tracing:

```
# Trace Agent Specific Settings
apm_config:
  enabled: true
  receiver_port: 8126
```

In order to get more information in the diagrams in Datadog, some sleep statements have been added as well as an additional function call. The full source code can be found in `flask_app.py`:

```python
from flask import Flask
import logging
import sys

import time

import blinker as _
from ddtrace import tracer
from ddtrace.contrib.flask import TraceMiddleware

main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

tracer.configure(hostname='localhost')
app = Flask(__name__)
traced_app = TraceMiddleware(app, tracer, service="hiring-flask-app", distributed_tracing=False)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    # Let's wait a few ms to show some "action" in the graphs
    time.sleep(0.2)
    apm_worker()
    time.sleep(0.3)
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

# Let's add a worker method that sleeps for a while and returns something.
# Just to have an example of tracing for submethods.
@tracer.wrap(name='apm_worker')
def apm_worker():
    time.sleep(0.5)
    return 'asdf'
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
```

An exmaple call of the resource `/api/apm` is shown in the following screenshot. One can clearly see the latency included by the sleep statements as well as the additional method call:
![Web Service Call](images/screenshot_flask_sevice_resource_call.png)

Datadog distinguished between *Services* and *Resources*. A Service summarizes processes that perform the same job, e.g. a web application, database server, caches, etc. A Resource is a particular function that is called inside of the Service. The example above shows the distinction very well: The flask web application is a service, whereas the individual RESTful endpoints are Resources, i.e. functions of the web service.

A summary dashboard can be found here: https://app.datadoghq.com/screen/419219/hardware--webapp?page=0&is_auto=false&from_ts=1535018400000&to_ts=1535191200000&live=true. The screenshot below shows some executions of the webservice and hardware metrics.
![APM and Infrastructure Dashboard](images/screenshot_dashboard_apm_hardware.png)

## Final Question
One of the major problems in Munich is too much traffic - and therefore also not enough parking spaces. The smart city startups leverage sensors to feed apps with information on free parking spaces that are large enough for your own car. There should be a public solution that aggregates the information on multi-story car parks, parking lots in the streets as well as parking lots and traffic information for park and ride spots a bit outside of the city. This would allow to identify the best way to work, and where to efficiently park the car. 

Based on the anomaly function, outstanding events (like Oktoberfest or just an accident) can be identified and the monitoring allows to identify a more efficient way to get to Munich by car - or leverage a park and ride option.


