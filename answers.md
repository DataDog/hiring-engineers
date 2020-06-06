Your answers to the questions go here.

## Prerequisites - Setup the environment
The Agent reporting metrics from my local machine (which is using a linux VM vis Vagrant).

I setup a Ubuntu agent with this command once I spun up my Vagrant linux VM (Ubuntu):
```
DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=MY_API_KEY bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"

```

Here is the agent status metrics:

![Agent Status](/images/running_agent_vm.png)

## Collecting Metrics
* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

In the datadog.yaml, added the following tags:
```
tags:
    - state:MA
    - city:Canton
    - agent:Ubuntu
    - os:Ubuntu_18.04.3_LTS
    - candidate-type:SalesEngineer
    - candidate-name:JoseBrache
```
![Tags in datadog.yaml](/images/agent_tags.png)

This host map can be seen here:
https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host&host=2551253227

![Tags on the Host Map Page](/images/vagrant_host.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

Installed mysql on my ubuntu VM
```
sudo apt install mysql-server
```

Installed the DataDog integration for MySQL, following these instructions (https://docs.datadoghq.com/integrations/mysql/)

Added this configuration block to my mysql.d/conf.yaml to collect MySQL metrics:
```
init_config:

instances:
  - server: 127.0.0.1
    user: datadog
    pass: "ILikeDataDog"
    port: "3306"
    tags:
      - MySQL:JoseBrache
    options:
      replication: false
      galera_cluster: true
      extra_status_metrics: true
      extra_innodb_metrics: true
      extra_performance_metrics: true
      schema_size_metrics: false
      disable_innodb_metrics: false

```

Was able to see the captured metrics in DataDog here:
https://app.datadoghq.com/infrastructure/map?fillby=avg%3Acpuutilization&sizeby=avg%3Anometric&groupby=availability-zone&nameby=name&nometrichosts=false&tvMode=false&nogrouphosts=true&palette=green_to_orange&paletteflip=false&node_type=host&host=2551253227

![MySQL Metrics on Host Map Page](/images/vagrant_host_mysql.png)

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

First created a custom_randomcheck.yaml in ‘/etc/datadog-agent/conf.d/custom_randomcheck.d’
This was in the contents:
```
instances: [{}]
```

Then created a [custom_randomcheck.py](https://gist.github.com/jbrache/a823c37c147c20ceab8afdb521672d43) in: **/etc/datadog-agent/checks.d**

With this code:
```python
import random

# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from new versions of the Agent...
    from datadog_checks.base import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version < 6.6.0
    from checks import AgentCheck

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"

class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('mymetric', random.randint(0,1000), tags=['metric_submission_type:gauge'])
```

After restarting the agent, I was able to find this metric being reported, graph shown below with the link here:
https://app.datadoghq.com/metric/explorer?from_ts=1591331546799&to_ts=1591335146799&live=true&page=0&is_auto=false&tile_size=m&exp_metric=mymetric&exp_agg=avg&exp_row_type=metric

![mymetric in Metrics Explorer](/images/mymetric_explorer.png)

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

I added the ‘min_configuration_interval’ field in custom_randomcheck.yaml, so it looks like this (following these(https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7) instructions):
```
init_config:
 
instances:
  - min_collection_interval: 45
```

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

**Answer**: Yes, looking at the documentation (https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7) you can change the collection interval of a check, by adjusting **min_collection_interval** field in the configuration file. A user may be able to add a sleep method in the custom agent check python file, i.e. the one I had was **custom_randomcheck.py** so I believe you could add a sleep function in there to modify the collection interval. Alternatively, using that min_collection_interval is a nice configuration to be able to manipulate.

## Visualizing Data
Utilize the Datadog API to create a Timeboard that contains:
* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket.

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

**Answer**: For the graph view below, I used the log y scale to visualize these metrics a bit clearer because they have different scales. Below is the link to the Dashboard, with all these 3 metrics:
https://app.datadoghq.com/dashboard/tr8-2j6-8wj/se-candidate-dashboard---via-api?from_ts=1591403007342&live=true&to_ts=1591406607342

Here’s the python script used to create this Dashboard (API keys have been revmoved):
https://gist.github.com/jbrache/bd59966d92de9c7aeb3dd15b7f9d197b

![mymetric in Metrics Explorer](/images/timeboard_with_mymetric_mymetric-rollup_mysql-anomaly.png)

Once this is created, access the Dashboard from your Dashboard List in the UI:
* Set the Timeboard's timeframe to the past 5 minutes
* Take a snapshot of this graph and use the @ notation to send it to yourself.

**Answer**: Below is a screenshot of the email with the timeboard set to the past 5 minutes with my mention.

![Timeboard email snapshot](/images/datadog_snapshot.png)

* **Bonus Question**: What is the Anomaly graph displaying?

**Answer**: The anomaly graph is displaying behavior for a metric which may be abnormal by analyzing the historical data for that metric. It displays what looks normal as well as what looks like anomalies (with red lines). There are some additional settings you can adjust based on the type of algorithm used for tracking trends as well as the ‘bounds’ parameter which allows you to adjust the tolerances.

## Monitoring Data
Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.
Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

**Answer**: below are the message conditions
![mymetric monitor conditions](/images/mymetric_monitor_conditions.png)

Please configure the monitor’s message so that it will:
* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
When this monitor sends you an email notification, take a screenshot of the email that it sends you.

**Answer**: Here is the message configuration with this these conditions:
![mymetric monitor message config](/images/mymetric_monitor_message.png)

**Answer**: Here is the email notification I received:
![mymetric monitor email](/images/mymetric_monitor_email_warn.png)

**Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

* One that silences it from 7pm to 9am daily on M-F,
![7pm to 9am daily on M-F](/images/downtime_summary_m-f.png)

* And one that silences it all day on Sat-Sun.
![Sat-Sun](/images/downtime_summary_s-s.png)

* Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
Email notification for M-F downtime:
![Downtime Email M-F](/images/downtime_m-f.png)

Email notification for Sat-Sun downtime:
![Downtime Email Sat-Sun](/images/downtime_weekend.png)

## Collecting APM Data
Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:
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
Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

Please include your fully instrumented app in your submission, as well.

**Answer**:
* I modified slightly the provided flask app to enable App analytics. The code for this flask app (flask_app.py) is here:
https://gist.github.com/jbrache/04b914cfb0f6b785756e56a14e34e855

* Next, I started the above [flask app](https://gist.github.com/jbrache/04b914cfb0f6b785756e56a14e34e855) with this command on my VM:
```
FLASK_APP=flask_app.py DATADOG_ENV=flask_test DD_RUNTIME_METRICS_ENABLED=true DD_TRACE_ANALYTICS_ENABLED=true ddtrace-run flask run --port=5050 --host=0.0.0.0
```

* Next, I created another client app that called the resources on the flask app. I called this [call_flask_app.py](https://gist.github.com/jbrache/ce316dbcb02935da26e58d89394cf012). All this python script does is call each resource with a 5 second delay for each. The code for this python script is here, I simply ran this on the same VM while the flask app was running to start getting APM metrics:
https://gist.github.com/jbrache/ce316dbcb02935da26e58d89394cf012

The link to this APM and Infrastructure metrics dashboard can be seen here:
https://app.datadoghq.com/dashboard/puy-qw4-6dv/apm-dashboard?from_ts=1591366562751&live=true&to_ts=1591380962751&tv_mode=false

![APM and Infrastructure Dashboard](/images/apm_infra_dashboard.png)

* **Bonus Question**: What is the difference between a Service and a Resource?

**Answer**: A **service** is a set of processes that accomplish the same job or task, for example a service can be a flask app or a database. A **resource** can be an action for a provided service, like accessing an app endpoint or a query. For example, in the linked flask app service, the resource '/api/trace' may be accessable by a client loading the url:
```
"http://127.0.0.1:5050/api/trace"
```

## Final Question
Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

**Answer**: There's a lot of potential here, thinking along the lines of an IoT device to monitor the connection to a security system.

My family has a farm and I recently setup a gate control system that's far away from the main house. This is a gate control system that includes:
* An intercom (It's a SIP intercom setup to call the main house when someone pushes the button)
* Security video (2 Cameras)
* The ability to open/close the main gate from the intercom on granted access
* Antenna to connect to the main house
* Network switch

It's setup with a system of long range antenna connected to the main house for network connectivity. You can see how these antennas are set up below, the main house (Point A) connects to the gate (Point C) via a relay station (Point B) to avoid trees and hills.
![Gate Antenna System](/images/antenna_stations.png)

This has been running fairly well but because it's setup in a rural environment I have some challenges understanding when I loose connection, due to a power outage or the antennas themselves have a problem with connectivity. Funny enough the power goes out all the time and growing up you learned to entertain yourself by being outside!

The gate where I would like to track some information is here, you can see the antenna that connects to the main house:
![Gate Monitoring](/images/antenna_stations.png)

My main issue is that I'm having a hard time tracking when the system goes offline. This is bad because:
1. You can't see who's at the gate via the security cameras
2. You can't open/close the main gate from the main house

I'm working on at least fixing the power outage issue by installing a battery backup but there is still the problem if the link between antennas drop (which sadly has happened). After doing this excercise, I realized I could drop in a Raspberry Pi or another type of single board computer at and send metrics to Datadog to let me know if the system is offline! At that point, I should be able to capture a ton of other metrics on whether the gate is open or closed, or if someone is at the front gate with a sensor and send an alert. There's a ton of stuff I could set up to capture data to understand what is happeneing and when someone should manually check it when it's offline.
