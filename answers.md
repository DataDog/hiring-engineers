## Answers (Solutions Engineering Technical Exercise)
#### Suzie Mae

#### Set up
For this technical exercise, I chose to install my agent on Docker rather than vagrant because Docker is more light weight and would have used less of my system's (rather limited) resources.

Installation instructions:
I followed the installation instructions here. I included the .... as this was necessary to bind the host port to the docker port, thereby enabling communication between the two machines. So my container was run with:
```

```

Some important docker commands to unerstand the state of the cointainers can be found here.

To edit the doocker files, there are two potential ways: 
Step 1: Copy the file to the host, edit on the host and copy back.
```
  docker cp <container_name>:<container filepath> <local filepath>
  vim <local filepath>
  docker cp <local file path> <container_name>:<Container file path>

```

Step 2: or else log into the container ```docker exec -it <container_name> bash ``` 

install the neccessary. In my case, on the debian version of linux, this was 

```
apt-get update
apt-get install -y vim-tiny

``` 

I chose "vim-tiny" to minimize the space taken up by the program, and vim-tiiny had everything I needed to edit files.

I found step 2 more convenient, so I went with it. HOwever, all teh commands run in the container can be run from outside the container by using:
``` docker exec -it <container_name> <path to bin> <command>```

For example, in the container, to check the agent status, run: ``` /opt/datadog-agent/bin/agent/agent status ```

From the host, run: ``` docker exec -it <container_name> /opt/datadog-agent/bin/agent/agent status ```

Fun tip: If you mess up your configuration file (like I did), the container would not start with a corrupted configuration file. However, all isn't lost and you don't have to spin up a new container. Create a new configuration file and copy it into the system from the host file using Step 1 above.

Running ```vim.tiny /etc/datadog-agent/datadog.yaml```, I added the following tags to my datadog.yaml file:
```
tags:
  - host_tag
  - env:prod
  - role:database
```

#### Host map with added tags

![alt text][img1]

[img1]: ./images/host_map_1.png "Host map"


#### Creating a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

- [Custom check python file](./my_check.py) <br/>
- [Custom check configuration file](./my_check.yaml)


#### Changing the collection interval without modifying the Python check file.

In programattically creating a custom check, two files are involved, a python file (ending in .py) and a configuration file (ending in .yaml). Both files must have the same name and be placed in the following folders:
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

More information can be found [here on custom metrics and their configuration](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6). (Also listed in the reference section below.


## Visualizing Data:

#### Timeboard
Scripts:
- [Script for creating a single graph timeboard](./create_timeboard_single.py)
- [Script for creating a multiple graph timeboard](./create_timeboard_multiple.py)

![alt text][img2a]

[img2a]: ./images/timeboard_over_5_minutes.png "Timeboard - Snapshot of single graph over 5 minutes"


**Note:** 
I created a timeboard with multiple graphs in order to extract clearer details about the rollup sum function. <br/><br/>
**Reason**: On the single graph, the rollup sum has values so high they cannot be accomodated comfortably with the other graphs. Either the details of the rollup sum would be clear and the other plots (my_etric average and postgresql) will be too small to give useful information or the details of the my_metric average and postgresql plots will be clear and the rollup sum plot will be virtually non-existent. <br/>

In additon, the hourly buckets of the rollup sum contribute to this by making the rollup sum plot far more discrete than the average metric and postgresql plots (See the two graphs below).

###### "Timeboard - single graphs (mulitple plots)"
![alt text][img2b]

[img2b]: ./images/timeboard_over_x_hours.png "Single graph over 4 hours - to show the difference in values"


###### "Timeboard - multiple graphs"

![alt text][img2c]

[img2c]: ./images/timeboard_for_multiple_boards.png "Timeboard - multiple graphs"


Thus, I created the multiple graph timeboard above to show the rollup sum clearly. 


### Anomaly graph display.

The anomaly function/plot displays metrics/situations where the query returns values outside the historical/established norm. It highlights these areas in red as seen in the image below. For my example, it includes extreme/outlier values or areas of relatively minimal change. 

###### Timeboard - Highlighting the anomalies

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

![alt text][img4c]

[img4c]: ./images/scheduled_downtime_2.png "7pm to 9am, Monday - Friday,  scheduled downtime notification"



#### Expiration notification for 7pm to 9am, Monday - Friday,  scheduled downtime notification"

![alt text][img4d]

[img4d]: ./images/downtime_expiry_2.png "Expiration notification for 7pm 7pm to 9am, Monday - Friday,  scheduled downtime notification""


## Collecting APM Data:
#### APM Dashboard
![alt text][img7a]

[img7a]: ./images/apm_board_1.png "Snapshot of APM Board"


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

[img8b]: ./images/apm_infr_2.png "Snapshot of APM - Individual Traces"




[link](https://app.datadoghq.com/apm/trace/1404380140091556782?spanID=6907584043438742536&env=dd_docker&sort=time&colorBy=service&graphType=span_list)

[Link to APM and Infrastructure Metrics Dashboard](https://app.datadoghq.com/apm/search?cols=%5B%22core_service%22%2C%22log_duration%22%2C%22log_http.method%22%2C%22log_http.status_code%22%5D&from_ts=1542642466428&graphType=span_list&index=trace-search&live=true&query=env%3Add_docker&saved_view=6953&spanID=15764508887163998640&stream_sort=desc&to_ts=1542646066428&trace)

- [ x ] Please include your fully instrumented app in your submission, as well.
[Fully instrumented app](./app.py)
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