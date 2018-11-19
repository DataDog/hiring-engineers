## Answers (Solutions Engineering Technical Exercise)
#### Suzie Mae


## Collecting Metrics:

- [x] Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

### Host Map
![alt text][img1]

[img1]: ./images/host_map.png "Host map"


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

#### Timeboard
Scripts:
- [Script for creating a single graph timeboard](./create_timeboard_single.py)
- [Script for creating a multiple graph timeboard](./create_timeboard_multiple.py)

![alt text][img2a]

[img2a]: ./images/timeboard_over_5_minutes.png "Timeboard - Snapshot of single graph over 5 minutes"



I created a timeboard with multiple graphs in order to extract clearer details about the rollup sum function. <br/>
On the single graph, the rollup sum had values so high they couldn't be accomodated comfortably with the other graphs... either the details of the rollup sum would be clear and the other graphs will be too small to give useful information, or the details of the other two plots will be clear and the rollup sum plot will be virtually non-existent. The hourly buckets of the roll-up sum also contributes to this, making the rollup sum plot far more discrete than the average metric and postgresql plots (See the two graphs below). I have included the muliple graph timeboard above to show the rollup sum clearly. 

![alt text][img2b]

[img2b]: ./images/timeboard_over_x_hours.png "Single graph over 4 hours - to show the difference in values"

<br/>
<br/>

![alt text][img2c]

[img2c]: ./images/timeboard_for_multiple_boards.png "Timeboard - multiple graphs"



### Bonus Question: What is the Anomaly graph displaying?

Metrics/situations where the query returns values outside the historical/established norm. (It highlights these areas in red as seen in the image below). for my example, it includes extreme/outlier values or areas of relatively minimal change. 

#### Timeboard - Highlighting the anomalies

![alt text][img2d]

[img2d]: ./images/anomalies_1.png "Timeboard - Highlighting the anomalies"

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


#### Monitor Alert 1 (Warning)
![alt text][img3a]

[img3a]: ./images/monitor_alert_log_1.png "Monitor Alert 1 (Warning)"


#### Monitor Alert 2 (No Data)

![alt text][img3b]

[img3b]: ./images/no_data_alert.png "Monitor Alert 2 (No Data)"

#### Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

- One that silences it from 7pm to 9am daily on M-F,
- And one that silences it all day on Sat-Sun.
- Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

#### Sat - Sun scheduled downtime notification
![alt text][img4a]

[img4a]: ./images/scheduled_down_time_1.png "Sat - Sun scheduled downtime notification"


#### Expiration notification for  Sat - Sun scheduled downtime notification
![alt text][img4b]

[img4b]: ./images/downtime_expiry_1.png "Expiration notification for Sat - Sun scheduled downtime notification"

#### 7pm to 9am, Monday - Friday,  scheduled downtime notification

![alt text][img5]

[img5a]: ./images/scheduled_down_time_2.png "7pm to 9am, Monday - Friday,  scheduled downtime notification"

[img5b]: ./images/scheduled_down_time_1.png "Sat - Sun scheduled downtime notification"


#### Expiration notification for 7pm to 9am, Monday - Friday,  scheduled downtime notification"

![alt text][img4b]

[img4b]: ./images/downtime_expiry_2.png "7pm to 9am, Monday - Friday,  scheduled downtime notification""


## Collecting APM Data:
#### APM Dashboard
![alt text][img7a]

[img7a]: ./images/apm_board.png "Snapshot of APM Board"


![alt text][img7b]

[img7b]: ./images/apm_dashboard_1.png "Snapshot of APM Dashboard-Services"


### APM Resource Stats
![alt text][img7c]

[img7c]: ./images/apm_resource_stats.png "Snapshot of APM Resource Stats"

<br/><br/>

![alt text][img7d]

[img7d]: ./images/individual_traces1.png "Snapshot of APM - Individual Traces with Flame"


https://app.datadoghq.com/apm/service/flask-app/flask.request?end=1542603832899&paused=false&start=1542517432899&env=prod

### Bonus Question: What is the difference between a Service and a Resource?<br/><br/>
A **Service** is a **_set of processes_** that do the same job (for example a web application, or a database), while a **Resource** is a particular **_action_** for a service. In the case of a database, this could be a query. For example: ```SELECT * FROM users WHERE id = ?```[4]

- [ x ] Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.<br/>
#### Infrastructure and APM Metrics


![alt text][img8a]

[img8a]: ./images/apm_infr_1.png "Infrastructure and APM Metrics"

#### Snapshot of APM - Individual Traces with Flame

![alt text][img8b]

[img8b]: ./images/apm_infr.png "Snapshot of APM - Individual Traces"




[link](https://app.datadoghq.com/apm/trace/1404380140091556782?spanID=6907584043438742536&env=dd_docker&sort=time&colorBy=service&graphType=span_list)

[Link to APM and Infrastructure Metrics Dashboard](https://app.datadoghq.com/apm/search?cols=%5B%22core_service%22%2C%22log_duration%22%2C%22log_http.method%22%2C%22log_http.status_code%22%5D&from_ts=1542642466428&graphType=span_list&index=trace-search&live=true&query=env%3Add_docker&saved_view=6953&spanID=15764508887163998640&stream_sort=desc&to_ts=1542646066428&trace)

- [ x ] Please include your fully instrumented app in your submission, as well.
[Fully instrumented app](./app1.py)
Note: Instruemtation could be done either by installing ddtace:
``` pip install ddtrace```



and then running the application as follows:
``` ddtrace-run python <app_name>.py```

Or by including a middle ware into the script. For this, I used the Flask middleware and instrumented it as follows:
``` 
    from ddtrace.contrib.flask import TraceMiddleware
    instrumented_app = TraceMiddleware(app, tracer, service="flask-app", distributed_tracing=False) 
```




### Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

###


### References

1. [Creating and configuring custom metrics](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6)
2. [Creating time boards](https://docs.datadoghq.com/api/?lang=python#timeboards)
3. [Rollup](https://docs.datadoghq.com/graphing/functions/rollup/)
4. [Getting started with APM](https://docs.datadoghq.com/tracing/visualization/)


[Monitoring Docker - Datadog Training Site](https://datadog.github.io/summit-training-session/handson/monitordocker/)
[Tracing Python Applications](https://docs.datadoghq.com/tracing/setup/python/)
[Monitoring Flask apps with Datadog](https://www.datadoghq.com/blog/monitoring-flask-apps-with-datadog/)
[What is the Difference Between "Type", "Service", "Resource", and "Name"?](https://help.datadoghq.com/hc/en-us/articles/115000702546-What-is-the-Difference-Between-Type-Service-Resource-and-Name-)
[Distributed Tracing](https://docs.datadoghq.com/tracing/faq/distributed-tracing/)