## Answers (Solutions Engineering Technical Exercise)
#### Suzie Mae

## Environment Setup

For this technical exercise, I chose to install my agent on Docker rather than vagrant because Docker is more light weight and would have used less of my system's (rather limited) resources.

Installation instructions:
I followed the installation instructions here. I included the .... as this was necessary to bind the host port to the docker port, thereby enabling communication between the two machines. So my container was created with:

```
docker run -d --name <container_name>
              -v /var/run/docker.sock:/var/run/docker.sock:ro \
              -v /proc/:/host/proc/:ro \
              -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
              -e DD_API_KEY=<YOUR_API_KEY> \
              -e DD_APM_ENABLED=true \
              -p 127.0.0.1:8126:8126/tcp \
              datadog/agent:latest

```

Some important docker commands to unerstand the state of the cointainers can be found [here].

To edit the docker files, there are two potential ways: <br/>

**Method 1:** 
- Copy the file to the host, edit on the host and copy back.
```
  docker cp <container_name>:<container filepath> <local filepath>
  vim <local filepath>
  docker cp <local file path> <container_name>:<Container file path>

```
**OR**

**Method 2:** <br/> 
- Log into the container ```docker exec -it <container_name> bash ``` 
- Install the neccessary editor. In my case, I chose "vim-tiny" to minimize the space taken up by the editor on docker. Also,  vim-tiny had everything I needed for basic editing. <br/>
I installed this on the debian version of linux, by running the following commands: 

```
apt-get update
apt-get install -y vim-tiny

``` 

**Note:** Although I did most of my work form within the container, as this was more convient for me, all the commands run in the container can also be run from outside the container by using:<br/>
``` docker exec -it <container_name> <path to bin> <command>```

For example:
- To check the agent status from within the container, run: ``` /opt/datadog-agent/bin/agent/agent status ```
- To check the status of the agent from the host, run: ``` docker exec -it <container_name> /opt/datadog-agent/bin/agent/agent status ```

> *_Fun tip_*: If you mess up your configuration file (like I did), and the container refuses to start with a  corrupted configuration file, all isn't lost and you don't have to spin up a new container. Create a new  configuration file (```datadog.yaml```) on the host and copy it, from the host into the right folder of the container (```/etc/datadog-agent/```) using **Method 1** above.

## Collecting Metrics
#### Tagging
I added my tags to the agent configuration file by execting ```vim.tiny /etc/datadog-agent/datadog.yaml``` (within the container). Then, I added the following lines to my datadog.yaml file:
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

***Note**: To ensure the custom sheck is running as expected, run: ```/opt/datadog-agent/bin/agent/agent check <check_name>```

The output should be mething like:
```
  Running Checks
  ==============
    
    my_check (1.0.0)
    ----------------
        Instance ID: my_check:5ba864f3937b5bad [OK]
        Total Runs: 1
        Metric Samples: 1, Total: 1
        Events: 0, Total: 0
        Service Checks: 0, Total: 0
        Average Execution Time : 0s
```

where ``` my_check ``` is the name of your custom check.

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
**Reason**: On the single graph, the rollup sum has values so high they cannot be accomodated comfortably with the other graphs. This means that either:
-  the details of the rollup sum would be clear and the other plots (my_etric average and postgresql) will be too small to give useful information *or* 
- the details of the my_metric average and postgresql plots will be clear and the rollup sum plot will be virtually non-existent. <br/>
In additon, the hourly buckets of the rollup sum contribute to the "adequate information issue" by making the rollup sum plot far more discrete than the average metric and postgresql plots. IN other words, only one data point per hour as opposed to the multiple data points for the other plots (See the two graphs below).

##### Timeboard - single graphs (mulitple plots)
![alt text][img2b]

[img2b]: ./images/timeboard_over_x_hours.png "Single graph over 4 hours - to show the difference in values"

##### Timeboard - multiple graphs

![alt text][img2c]

[img2c]: ./images/timeboard_for_multiple_boards.png "Timeboard - multiple graphs"


Thus, I created the multiple graph timeboard above to show the rollup sum clearly. 


### Anomaly Graph.

The anomaly graph displays metrics/situations where the query returns values outside the historical/established norm. It highlights these areas in red as seen in the image below. For my choice of metric, it includes extreme and/or outlier values as well as unexpected behaviour (the area of minimal change). 

###### Timeboard - Highlighting the anomalies

![alt text][img2d]

[img2d]: ./images/anomalies_1.png "Timeboard - Highlighting the anomalies"

## Monitoring Data


###### Metric Monitor Configuration
Configure the monitor by choosing **New Monitor** (under Monitors) ---> **Metric** (on the Select a monitor type page) and **Threshold Alert**. For a warning threshold of 500 and alert of 800 (ver the last 5 minutes) as well as 'No data' (ocver 10 minutes), see the settings in the image below.

![alt text][img3]

[img3]: ./images/metric_monitor_config.png "Metric monitor configuration"

#### Alert message configuration ####
```
{{#is_warning}}

@xidornx@aol.com 

Warning has been triggered on:

- **Host Name**: {{host.name}} 
- **IP Address**: {{host.ip}} 
- **Trigger Value**: {{value}}

{{/is_warning}}



{{#is_alert}}

@xidornx@aol.com 

Alert: Has been triggered on:

- **Host Name**: {{host.name}} 
- **IP Address**: {{host.ip}} 
- **Trigger Value**: {{value}}

{{/is_alert}} 



{{#is_no_data}}

@xidornx@aol.com 

No data: There has been no data on my_metric on:
  
- **Host Name**: {{host.name}} 
- **IP Address**: {{host.ip}} 
- **Trigger Value**: {{value}}

{{/is_no_data}}

```

#### Output
-  #### Monitor Alert 1 (Warning)
![alt text][img3a]

[img3a]: ./images/monitor_alert_log_1.png "Monitor Alert 1 (Warning)"


- #### Monitor Alert 2 (No Data)

![alt text][img3b]

[img3b]: ./images/no_data_alert.png "Monitor Alert 2 (No Data)"

#### Scheduling Downtimes

- One that silences it from 7pm to 9am daily on M-F,
- And one that silences it all day on Sat-Sun.
- Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

#### Sat - Sun scheduled downtime notification
![alt text][img4a]

[img4a]: ./images/scheduled_downtime_1.png "Sat - Sun scheduled downtime notification"


#### Expiration notification for  Sat - Sun scheduled downtime notification
![alt text][img4b]

[img4b]: ./images/downtime_expiry_1.png "Expiration notification for Sat - Sun scheduled downtime notification"

#### 7pm to 9am, Monday - Friday,  scheduled downtime notification

![alt text][img4c]

[img4c]: ./images/scheduled_downtime_2.png "7pm to 9am, Monday - Friday,  scheduled downtime notification"



#### Expiration notification for 7pm to 9am, Monday - Friday,  scheduled downtime notification"

![alt text][img4d]

[img4d]: ./images/downtime_expiry_2.png "Expiration notification for 7pm 7pm to 9am, Monday - Friday,  scheduled downtime notification"


## Collecting APM Data:

#### APM Dashboard
![alt text][img7a]

[img7a]: ./images/apm_board_1.png "Snapshot of APM Board"

#### Snapshot of APM Dashboard-Services"

![alt text][img7b]

[img7b]: ./images/apm_dashboard_1.png "Snapshot of APM Dashboard-Services"


#### Snapshot of APM Resource Stats
![alt text][img7c]

[img7c]: ./images/apm_resource_stats.png "Snapshot of APM Resource Stats"

#### Snapshot of APM - Individual Traces with Flame

![alt text][img7d]

[img7d]: ./images/individual_traces1.png "Snapshot of APM - Individual Traces with Flame"


https://app.datadoghq.com/apm/service/flask-app/flask.request?end=1542603832899&paused=false&start=1542517432899&env=prod

#### Service vs. Resource<br/>
A **Service** is a **_set of processes_** that do the same job (for example a web application, or a database). An example of a Service is my flask web application (shown as **flask-app** in the image below). <br/><br/>

A **Resource**, on the other hand, is a particular **_action_** for a service. In the case of a database, this could be a query. For example: ```SELECT * FROM users WHERE id = ?```. In web applications, these could be canonical URLs (/users/status/) or handler functions/routes. On the APM interface, these resources can be found after clicking a particular service. (See image below). <br/>
_NB: More information can be found in the Reference section_

#### Infrastructure and APM Metrics


![alt text][img8a]

[img8a]: ./images/apm_infra_1.png "Infrastructure and APM Metrics"

#### Snapshot of APM - Individual Traces with Flame

![alt text][img8b]

[img8b]: ./images/apm_infr_2.png "Snapshot of APM - Individual Traces"


[Link to APM and Infrastructure Metrics Dashboard](https://app.datadoghq.com/apm/search?cols=%5B%22core_service%22%2C%22log_duration%22%2C%22log_http.method%22%2C%22log_http.status_code%22%5D&from_ts=1542642466428&graphType=span_list&index=trace-search&live=true&query=env%3Add_docker&saved_view=6953&spanID=15764508887163998640&stream_sort=desc&to_ts=1542646066428&trace)


[Fully instrumented app](./app.py)<br/><br/>
**Note:** Instrumentation could be done by either:
- Installing ```ddtace``` and running the application as follows::

``` pip install ddtrace
    ddtrace-run python <app_name>.py
```
**OR**
- Including a middleware in the script. <br/>
For my instrumentation, I used the Flask middleware and instrumented it as follows:
``` 
    from ddtrace.contrib.flask import TraceMiddleware
    instrumented_app = TraceMiddleware(app, tracer, service="flask-app", distributed_tracing=False) 
```


### Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

###

------
### References
------
1. [Creating and configuring custom metrics](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6)
2. [Creating time boards](https://docs.datadoghq.com/api/?lang=python#timeboards)
3. [Rollup](https://docs.datadoghq.com/graphing/functions/rollup/)
4. [Getting started with APM](https://docs.datadoghq.com/tracing/visualization/)
5. [Monitoring Docker - Datadog Training Site](https://datadog.github.io/summit-training-session/handson/monitordocker/)
6. [Tracing Python Applications](https://docs.datadoghq.com/tracing/setup/python/)
7. [Monitoring Flask apps with Datadog](https://www.datadoghq.com/blog/monitoring-flask-apps-with-datadog/)
8. [What is the Difference Between "Type", "Service", "Resource", and "Name"?](https://help.datadoghq.com/hc/en-us/articles/115000702546-What-is-the-Difference-Between-Type-Service-Resource-and-Name-)
9. [Distributed Tracing](https://docs.datadoghq.com/tracing/faq/distributed-tracing/)