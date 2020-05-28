Your answers to the questions go here.

## Pre-reqs:
  1. Decided to have a little fun with this and went the vagrant route, as I had a bit of experience here. I decided to install kube,     docker, and then use minikube to create a 'hello-world'-esque web application to better mimic monitoring a real world app.
 * Vagrant <img src="/Prereqs/pre-req-vagrant.png?raw=true" width="1000" height="332"></a>
 * Docker <img src="/Prereqs/docker_install.png?raw=true" width="1000" height="332"></a>
 * Minikube <img src="/Prereqs/minikube.png?raw=true" width="1000" height="332"></a>
 * Container monitoring in datadog after configuring docker agent conf.d yaml file: <img src="/Prereqs/minikube%20container%20monitoring.png?raw=true"></a>

## Collecting Metrics
#### Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
  <img src="/CollectingMetrics/tags-datadog.png?raw=true"></a>
  <img src="/CollectingMetrics/Agent_tags.png?raw=true"></a>
#### Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
 * Went with postgres here, install went off without a hitch. Added the datadog user and edited config file to give permissions required. Did run into an issue with the dd-agent user accessing the conf.d directory, strangely, so I _cheated_ and just gave global permissions via chmod.
  <img src="/CollectingMetrics/troubleshooting-postgres.png?raw=true"></a>
  <img src="/CollectingMetrics/troubleshooting-postgres-fixed.png?raw=true"></a>

 * And here it is in the UI:

  <img src="/CollectingMetrics/postgres-db.png?raw=true"></a>

#### Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

  <img src="/CollectingMetrics/metric_config_yaml_interval.png?raw=true"></a>
  <img src="/CollectingMetrics/agentcheck_status_and_code.png?raw=true"></a>
  <img src="/CollectingMetrics/my_metric_showing.png?raw=true"></a>
  <img src="/CollectingMetrics/my_metric_showing2.png?raw=true"></a>

#### Change your check's collection interval so that it only submits the metric once every 45 seconds.
#### Bonus Question Can you change the collection interval without modifying the Python check file you created?
   * For the bonus I changed the metrics_example.yaml file (what I used for the agent check) and added the line
  ```
  - min_collection_interval: 45
  ```
  <img src="/CollectingMetrics/csv_time_validation.png?raw=true"></a>

### Utilize the Datadog API to create a Timeboard that contains:
#### Your custom metric scoped over your host.
#### Any metric from the Integration on your Database with the anomaly function applied.
#### Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

<img src="/VisualizingData/vis_dash_1.png?raw=true"></a>
<img src="/VisualizingData/postgres_anomaly_creation.png"></a>

* Additionally, the instructions asked for a timeboard but the documentation showed that as deprecated, so I used the dashboard API. All of my work can be found in the associated timeboard.py file. Code below as well.
```
from datadog import initialize, api

options = {
    'api_key': '91300d2d9cd0ccf8b22dbd46124c3102',
    'app_key': '4d6730f87624f71e8dac1817951f3a1d35e0e8d0'
}

initialize(**options)

# Create a new monitor
monitor_options = {
    "notify_no_data": True,
    "no_data_timeframe": 20
}
tags = ["app:minikube", "vagrant"]
api.Monitor.create(
    type="query alert",
    query="avg(last_4h):anomalies(avg:postgresql.max_connections{host:vagrant,env:ddogeval}, 'basic', 2, direction='both', alert_window='last_15m', interval=60, count_default_zero='true') >= 1",
    name="Postgresql sync time",
    message="IDK this is a demo.",
    tags=tags,
    options=monitor_options
)

title = 'JRath My_Metric_Final'
widgets = [{
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{host:vagrant}'}
        ],
        'title': 'Value (Gauge)'
    }
},
    {
    'definition': {
        'type': 'alert_graph',
        'alert_id': '18827755', #Used a previously created monitor here (see above for how it was done programmatically)
        'viz_type': 'timeseries',
        'title': 'Postgresql max connections with alert graph'
    }
},
    {
    'definition': {
        'type': 'timeseries',
        'requests': [
            {'q': 'avg:my_metric{host:vagrant}.rollup(sum, 3600)'}
        ],
        'title': 'Rollup - Summed over 1 hour'
    }
}]

layout_type = 'ordered'
description = 'A dashboard with custom metric info.'
is_read_only = True
notify_list = ['john.rath202@gmail.com']
template_variables = [{
    'name': 'vagrant',
    'prefix': 'host',
    'default': 'vagrant'
}]

saved_view = [{
    'name': 'Saved views for my_metric',
    'template_variables': [{'name': 'host', 'value': 'vagrant'}]}
]

api.Dashboard.create(title=title,
                     widgets=widgets,
                     layout_type=layout_type,
                     description=description,
                     is_read_only=is_read_only,
                     notify_list=notify_list,
                     template_variables=template_variables,
                     template_variable_presets=saved_view)
```
#### Set the Timeboard's timeframe to the past 5 minutes
#### Take a snapshot of this graph and use the @ notation to send it to yourself.
* This one was tricky despite sounding easy. Maybe I overlooked something obvious but the only way I could get the specific 5 minute window was to select one graph and drag a 5 minute window, which sets the time universally to 5 minutes for each dashlet.
<img src="/VisualizingData/5_minute_dash.png?raw=true></a>"
<img src="/VisualizingData/annotated_snapshot.png"></a>
<img src="/VisualizingData/email.png"></a>
#### Bonus Question: What is the Anomaly graph displaying?
```
It appears to be showing the current data (as I selected timeseries for viz_type) and the status of the monitor (ok,trigged [alert, warn, no data(?)]) in the same pane.
```

# Monitoring Data
### Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
####  Warning threshold of 500
####  Alerting threshold of 800
####  And also ensure that it will notify you if there is No Data for this query over the past 10m.

<img src="/MonitoringData/settings.png?raw=true"></a>

### Please configure the monitor’s message so that it will:
####  Send you an email whenever the monitor triggers.
####  Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

* Alert
```
{{#is_alert}}
@john.rath202@gmail.com
Host {{host.name}} with IP [{{host.ip}}] is experiencing a severe performance degradation.
Current value is {{value}} which violates the alert threshold of {{threshold}}. This is a violation of over {{eval "int(value) - int(threshold)"}}.
{{/is_alert}}
```

* Warning
```
{{#is_warning}}
@john.rath202@gmail.com
Host {{host.name}} is experiencing a severe performance degradation.
Current value is {{value}} which violates the warning threshold of {{warn_threshold}}. This is a violation of over {{eval "int(value) - int(warn_threshold)"}}.
{{/is_warning}}
```

* No Data
```
{{#is_no_data}}
@john.rath202@gmail.com
No data received for 10 or more minutes.
{{/is_no_data}}
```

#### Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
```
Host {{host.name}} with IP [{{host.ip}}] is experiencing a severe performance degradation.
```

#### When this monitor sends you an email notification, take a screenshot of the email that it sends you.

<img src="/MonitoringData/test_alert.png?raw=true"></a>
<img src="/MonitoringData/test_alert.png?raw=true"></a>

### Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
#### One that silences it from 7pm to 9am daily on M-F,

<img src="/MonitoringData/downtime_1.png?raw=true"></a>

#### And one that silences it all day on Sat-Sun.
<img src="/MonitoringData/downtime_2.png?raw=true"></a>

* Monitoring notification markdown below, in full.
```
Alert!

{{#is_alert}}
@john.rath202@gmail.com
Host {{host.name}} with IP [{{host.ip}}] is experiencing a severe performance degradation.
Current value is {{value}} which violates the alert threshold of {{threshold}}. This is a violation of over {{eval "int(value) - int(threshold)"}}.
{{/is_alert}}

{{#is_warning}}
@john.rath202@gmail.com
Host {{host.name}} is experiencing a severe performance degradation.
Current value is {{value}} which violates the warning threshold of {{warn_threshold}}. This is a violation of over {{eval "int(value) - int(warn_threshold)"}}.
{{/is_warning}}

{{#is_no_data}}
@john.rath202@gmail.com
No data received for 10 or more minutes.
{{/is_no_data}}
```
