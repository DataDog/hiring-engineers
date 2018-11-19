# Answers (Solutions Engineering Technical Exercise)
### Suzie Mae


## Collecting Metrics:

- [x] Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

![alt text][img]

[img]: ./images/host_map.png "Host map"


- [x] Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
- [x] Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
- [x] Change your check's collection interval so that it only submits the metric once every 45 seconds.
- [x] Bonus Question Can you change the collection interval without modifying the Python check file you created?

- #### Answer to bonus question:
In programattically creating a custom check, two files are involved, a python file (ending in .py) and a configuration file (ending in .yaml). Both must have the same name and be placed in the following folders:
```
Config file: /etc/datadog-agent/conf.d/
Python file: /etc/datadog-agent/checks.d/
```

Within the configuration file, a dictionary of instances can be declared stating the `min_collection_interval`. In this case, 45 seconds. The syntax for configuration file content stating 45 seconds collection interval is shown below:

```
init_config:

instances:
    - min_collection_interval: 45
```

More information can be found here on custom metrics and their configuration can be found in the relevant reference section below.


## Visualizing Data:

[x] Utilize the Datadog API to create a Timeboard that contains:

- Your custom metric scoped over your host.
- Any metric from the Integration on your Database with the anomaly function applied.
- Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket
Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Once this is created, access the Dashboard from your Dashboard List in the UI:

- Set the Timeboard's timeframe to the past 5 minutes
- Take a snapshot of this graph and use the @ notation to send it to yourself.

#### Host Map

![alt text][img1]

[img1]: ./images/host_map.png "Host map"


### Bonus Question: What is the Anomaly graph displaying?






## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

[x] Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

- Warning threshold of 500
- Alerting threshold of 800
- And also ensure that it will notify you if there is No Data for this query over the past 10m.


Please configure the monitor’s message so that it will:

- Send you an email whenever the monitor triggers.

Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

- Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

- When this monitor sends you an email notification, take a screenshot of the email that it sends you.

![alt text][img2]

[img2]: ./images/monitor_alert_log_1.png "Monitor alert 1"

Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

One that silences it from 7pm to 9am daily on M-F,
And one that silences it all day on Sat-Sun.
Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

#### Sat - Sun scheduled downtime notification
![alt text][img3]

[img3]: ./images/scheduled_down_time_1.png "Sat - Sun scheduled downtime notification"


#### 7pm to 9am, Monday - Friday,  scheduled downtime notification

![alt text][img4]

[img4]: ./images/host_map.png "7pm to 9am, Monday - Friday,  scheduled downtime notification"

## Collecting APM Data:
### APM Dashboard
![alt text][img5]

[img5]: ./images/apm_dashboard.png "Snapshot of APM Dashboard"


### APM Resource Stats
![alt text][img6]

[img6]: ./images/apm_resource_stats.png "Snapshot of APM Resource Stats"

- [x] Bonus Question: What is the difference between a Service and a Resource?
A **Service** is a **__set of processes__** that do the same job, while a **Resource** is a particular **__action__** for a service

- [ x ] Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.

- [ x ] Please include your fully instrumented app in your submission, as well.

- [ x ] Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?


### References

1. Creating and configuring custom metrics: https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6
2. Creating time boards: https://docs.datadoghq.com/api/?lang=python#timeboards
3. Rollup: https://docs.datadoghq.com/graphing/functions/rollup/


Monitoring Docker - Datadog Training Site: https://datadog.github.io/summit-training-session/handson/monitordocker/