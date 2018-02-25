Your answers to the questions go here. (Solianne BELLAHOUEL solianne.bellahouel@epitech.eu)

## Prerequisites - Setup the environment

I decide to choose a fresh Ubuntu 12.04 VM, but i'm not using Viagrant.
I just downloaded the ISO on Ubuntu official web site, and install it on VirtualBox, after that I go to datadog official website, I follow the instruction for installing on my machine.

## Collecting Metrics:

1. Agent Config File :

For adding a host tags in the Agent, we need to edit the /etc/dd-agent/datadog.conf and add the tag property.
    ![tag image](screenshots/datadog-agent-host-conf.JPG)
    ![tag image](screenshots/datdadog-agent-host.JPG)

2. Database

I decide to choose a MongoDB database for Datadog.

![tag image](screenshots/install_db.JPG)
![tag image](screenshots/configure_db.JPG)

Integration in Datadog :

/etc/dd-agent/conf.d/mongo.yaml
```mongo.yaml
init_config:

instances:
#        - server: mongodb://datadog:HuXDlrOkrfFSi3wqGjnsow9k@127.0.0.1:27016
#          tags:
#              - soso
- server: mongodb://datadog:HuXDlrOkrfFSi3wqGjnsow9k@127.0.0.1:27017
tags:
- soso

logs:
- type: file
path: /var/log/mongodb/mongodb.log
service: mongo
source: mongodb
```

![tag image](screenshots/instance_mongo_check.JPG)

3. Custome Agent Check

For create your own agent check, we need to create two files like my_metric :

/etc/dd-agent/conf.d/my_metric.yaml
/etc/dd-agent/check.d/my_metric.py

``` my_metric.py
import random
from checks import AgentCheck

class MetricCheck(AgentCheck):
def check(self, instance):
self.gauge('my_metric', random.randint(1, 1000))
```

```my_metric.yaml
init_config:
- name: my_metric
- type: gauge
- active: yes
- min_collection_interval: 45

instances:
[{}]
```
![tag image](screenshots/metrics_agent.JPG)
![tag image](screenshots/my_metric2.JPG)
![tag image](screenshots/my_metric3.JPG)

**Bonus Question**
You can change the collection interval without modifying the Python check file,
By default, the datadog collection interval is 15s.
You can modify this value for changing the collection interval of all metrics.

## Visualizing Data:

1. The datadog API

To create my timeboard, I use Ruby and also Python, to try the difference between the 2 languages.

Ruby :

```my_timeboard.rub
require 'rubygems'
require 'dogapi'

api_key = '736b97f01509c71840ed1b7007c15c3d'
app_key = 'ccefaa0962b4e69865dc4f172f8ed91c2881eb55'

dog = Dogapi::Client.new(api_key, app_key)

# Create a new monitor
#options = {
#    'notify_no_data' => true,
#    'no_data_timeframe' => 20
#}
#tags = ['app:webserver', 'frontend']
#dog.monitor("metric alert", "avg(last_1h):my_metric{host:datadog}", : name => "average of my_metric on my host", : message => "metric on host", : tags => tags, : options => options)

# Create a timeboard.

title = 'My Timeboard'
description = 'Metrics and more'
graphs = [{
"definition" => {
"events" => [],
"requests" => [{
"q" => "avg:my_metric{*} by {host}"
}],
"viz" => "timeseries"
},
"title" => "Average of my metric on my host"
},
{
"definition" => {
"events" => [],
"requests" => [{
"q" => "anomalies(avg:mongodb.network.bytesinps{*}, 'agile', 2)"
}],
"viz" => "timeseries"
},
"title" => "Mongo network bytes anomalies"
},
{
"definition"=> {
"events" => [],
"requests" => [{
"q"=> "avg:my_metric{*}.rollup(sum,3600)"
}],
"viz" => "timeseries"
},
"title" => "my_metric sum rollup on 3600s"
}]
template_variables = [{
"name" => "host1",
"prefix" => "host",
"default" => "host:my-host"
}]

dog.create_dashboard(title, description, graphs, template_variables)
```
My Timeboard :

![tag image](screenshots/my_timeboard.JPG)

```my_timeboard.py
from datadog import initialize, api

options = { 'api_key' : '736b97f01509c71840ed1b7007c15c3d',
'app_key' : 'ccefaa0962b4e69865dc4f172f8ed91c2881eb55'
}

initialize(**options)

# Create a new monitor
#options = {
#    'notify_no_data' : true,
#    'no_data_timeframe' : 20
#}
#tags = ['app:webserver', 'frontend']
#dog.monitor("metric alert", "avg(last_1h):my_metric{host:datadog}", : name : "average of my_metric on my host", : message : "metric on host", : tags : tags, : options : options)

# Create a timeboard.

title = 'My Timeboard'
description = 'Metrics and more'
graphs = [{
"definition" : {
"events" : [],
"requests" : [{
"q" : "avg:my_metric{*} by {host}"
}],
"viz" : "timeseries"
},
"title" : "Average of my metric on my host"
},
{
"definition" : {
"events" : [],
"requests" : [{
"q" : "anomalies(avg:mongodb.network.bytesinps{*}, 'agile', 2)"
}],
"viz" : "timeseries"
},
"title" : "Mongo network bytes anomalies"
},
{
"definition": {
"events" : [],
"requests" : [{
"q": "avg:my_metric{*}.rollup(sum,3600)"
}],
"viz" : "timeseries"
},
"title" : "my_metric sum rollup on 3600s"
}]
template_variables = [{
"name" : "host1",
"prefix" : "host",
"default" : "host:my-host"
}]

read_only = True
api.Timeboard.create(title=title,
description=description,
graphs=graphs,
template_variables=template_variables,
read_only=read_only)
```
Snapshot @notation

![tag image](screenshots/mentions.png)

![tag image](screenshots/mentions_mail.png)

**Bonus Question**
By analyzing a metric’s historical behavior, anomaly detection distinguishes between normal and abnormal metric trends.
if we see an unexpected drop in request throughput, which is quickly flagged as an anomaly.
Here I decided to monitor the Mongo network bytes anomalies.

## Monitoring Data

You can create a new Metric monitor by using api or by the UI interface

1. By the API :

```monitor.py
from datadog import initialize, api

options = { 'api_key' : '736b97f01509c71840ed1b7007c15c3d',
'app_key' : 'ccefaa0962b4e69865dc4f172f8ed91c2881eb55'
}

initialize(**options)

#Create a new monitor
options = {
'notify_no_data' : True,
'no_data_timeframe' : 10,
'thresholds' : {'critical' : 800 , 'warning' : 500},
'renotify_interval' : 5,
'escalation_message' : '@event-3ti8vwpk'
}
tags = ['app:webserver', 'frontend']
api.Monitor.create(
type="metric alert",
query="avg(last_5m):my_metric{host:datadog}",
name="avg metric alert 800 on datadaog",
message="metric alert 800 on datadog.",
tags=tags,
options=options
)
options = {
'notify_no_data' : True,
'no_data_timeframe' : 10,
'thresholds' : {'critical' : 4 , 'warning' : 2},
'renotify_interval' : 5,
'escalation_message' : '@event-3ti8vwpk'
}
tags = ['app:webserver', 'frontend']
api.Monitor.create(
type="metric alert",
query="avg(last_5m):system.net.udp.in_datagrams{host:datadog}",
name="avg sytem udp on host",
message="avg alart system udp on datadog.",
tags=tags,
options=options
)
```
2. By the UI :

Choose the detection method :
![tag image](screenshots/datadog_create_metric_1.JPG)

Set the Alert Condition :
![tag image](screenshots/datadog_create_metric_2.JPG)

Email configuration :
![tag image](screenshots/datadog_create_metric_3.JPG)

Email Reiceved :
![tag image](screenshots/datadog_metric_email.JPG)

**Bonus Question**:

silences it all day on Sat-Sun :
![tag image](screenshots/week-end_silence_metrics.JPG)

silences it from 7pm to 9am daily on M-F :
![tag image](screenshots/weekly_silence_metrics.JPG)

Email :
![tag image](screenshots/week-end_silence_metrics-emails_downtime.JPG)

UI :
![tag image](screenshots/metric_downtime.JPG)

## Collecting APM Data:

APM enabled in datadog.conf :

![tag image](screenshots/apm_agent.JPG)

Flask install :

![tag image](screenshots/flask_dd_trace_install.JPG)

Run dd-agent :

![tag image](screenshots/dd_trace_run.JPG)

## Final Question:

I would use datadog for analyse the QoS of Uber.
I want to analyse with datadog the avaibilty and the price rate of Uber in worlwide in real time, and make some statistics like :

The availability rate of Uber by months, years.

Because Uber, applied surge prices depending on demand for rides.
I want to know :
The average price of a ride by months and by years.





