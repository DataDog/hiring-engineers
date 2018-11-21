# Solutions Engineering Technical Exercise
#### - Suzie Mae

-----
## Environment Setup
-----
_For this technical exercise, I chose to install my agent on Docker rather than vagrant because Docker is lighter weight and would have used less of my system's (rather limited) resources._

**Installation:**
I created my docker container (with the datadog agent) by running the command below. <br/>
> **Side note:** ``` -p 127.0.0.1:8126:8126/tcp```  is particularly important to bind the host port to the docker port; thereby enabling communication between the two machines.

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
Following this, I ran ``` docker exec -it <container_name> /opt/datadog-agent/bin/agent/agent status ``` to get information on my installation as well as to ensure my container was running without errors. An excerpt of the output is shown below:

```
==============
Agent (v6.6.0)
==============

  Status date: 2018-11-21 17:08:00.027401 UTC
  Pid: 341
  Python Version: 2.7.15
  Logs: /var/log/datadog/agent.log
  Check Runners: 4
  Log Level: debug

```

> **Side note:** Some important docker commands to understand the state of the cointainers can be [found here](https://docs.docker.com/engine/reference/commandline/docker/#child-commands).

-----
## Collecting Metrics
-----
#### Tagging

To edit the files within docker (which include the datadog-agent configuration file), there are two potential ways: <br/>

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
- Install the neccessary editor. 

I chose to install ```vim-tiny``` over ```vim``` since it contains all I needed for a basic editor and occupies less space. Running the commands below enabled this installation.


```
apt-get update
apt-get install -y vim-tiny

``` 
> **Side note 1:** The command when using ```vim-tiny``` to work with files is ```vim.tiny```
> **Side note 2:** Although I did most of my work form within the container, as this was more convient for me, all the subcommands run within the container can also be run from outside the container by using:<br/>
``` docker exec -it <container_name> <path to bin> <command>```

> For example:
> - To check the agent status from within the container, run: ``` /opt/datadog-agent/bin/agent/agent status ```
> - To check the status of the agent from the host, run: ``` docker exec -it <container_name> /opt/datadog-agent/bin/agent/agent status ```
> Other useful agent commands cona be [found here](https://docs.datadoghq.com/agent/faq/agent-commands/?tab=agentv6)
> 
> **_Fun tip_**: If you mess up your configuration file (like I did), and the container refuses to start with a  corrupted configuration file, all isn't lost and you don't have to spin up a new container. Create a new  configuration file (```datadog.yaml```) on the host and copy it, from the host into the right folder of the container (```/etc/datadog-agent/```) using **Method 1** above.


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

> **Side note**: To ensure the custom check is running as expected, run: <br/>
>```/opt/datadog-agent/bin/agent/agent check <check_name>```
>
> The output should be allong the following lines:
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
>
> where ``` my_check ``` is the name of your custom check.

#### Changing the collection interval without modifying the Python check file.

In programattically creating a custom check, two files are involved, a python file (ending in ```.py```) and a configuration file (ending in ```.yaml```). Both files must have the same name and be placed in the following folders:
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

More information can be found [here on custom metrics and their configuration](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6). 

-----
## Visualizing Data:
-----
#### Timeboard Scripts:
- [Script for creating a single graph timeboard](./create_timeboard_single.py)
- [Script for creating a multiple graph timeboard](./create_timeboard_multiple.py)

#### Timeboard - Snapshot of single graph over 5 minutes
![alt text][img2a]

[img2a]: ./images/timeboard_over_5_minutes.png "Timeboard - Snapshot of single graph over 5 minutes"


> **Note:** 
> I created a timeboard with multiple graphs in order to extract clearer details about the rollup sum function. <br/><br/>
> **Reason**: On the single graph, the rollup sum has values so high they cannot be accomodated comfortably with the other graphs. This means that either:
> -  the details of the rollup sum would be clear and the other plots (```my_metric average``` and ```postgresql rows returned```) will be too small to give useful information *or* 
> - the details of the my_metric average and postgresql plots will be clear and the rollup sum plot will be virtually non-existent. <br/>
> In additon, the hourly buckets of the rollup sum contribute to the "adequate information" issue because the rollup sum plot has much more points that are spread out than the average ```my_metric``` and ```postgresql rows returned``` plots -- only one data point per hour as opposed to the multiple data points for the other plots (See the two graphs below).

#### Timeboard - single graph (mulitple plots)
![alt text][img2b]

[img2b]: ./images/timeboard_over_x_hours.png "Single graph over 4 hours - to show the difference in values"

#### Timeboard - multiple graphs

![alt text][img2c]

[img2c]: ./images/timeboard_for_multiple_boards.png "Timeboard - multiple graphs"

<br/>
Thus, I created the multiple graph timeboard above to show the rollup sum clearly. 


### Anomaly Graph

The anomaly graph displays metrics/situations where the query returns values outside the historical/established norm. It highlights these areas in red as seen in the image below. For my choice of metric, it includes extreme and/or outlier values as well as unexpected behaviour (the area of minimal change). 

#### Timeboard - Highlighting the anomalies

![alt text][img2d]

[img2d]: ./images/anomalies_1.png "Timeboard - Highlighting the anomalies"

## Monitoring Data


#### Metric Monitor Configuration
**Steps to configure the monitor:** <br/> Choose **New Monitor** (under Monitors) ---> **Metric** (on the Select a monitor type page) and **Threshold Alert**. For a warning threshold of 500 and alert of 800 (over the last 5 minutes) as well as 'No data' (over 10 minutes), see the settings in the image below.

#### Metric monitor configuration snapshot

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
- #### Monitor Notification 1 (Warning)
![alt text][img3a]

[img3a]: ./images/monitor_alert_log_1.png "Monitor Notification 1 (Warning)"


- #### Monitor Notification 2 (Alert)

![alt text][img3b]

[img3b]: ./images/monitor_alert_log_2.png "Monitor Notification 2 (Alert)"

- #### Monitor Notification 3 (No Data)

![alt text][img3c]

[img3c]: ./images/no_data_alert.png "Monitor Notification 2 (No Data)"

#### Scheduling Downtimes

**Path**: Monitors --> Manage Downtime --> Schedule Downtime. Select monitor, configuration and create message. I have included snapshots of the various required settings below:


#### Sat - Sun scheduled configuration notification (recurrent)
![alt text][img4a]

[img4a]: ./images/weekly_downtime_schedule(recurrent).png "Sat - Sun scheduled downtime configuration (recurrent)"


#### Sat - Sun scheduled configuration notification (one-off)

![alt text][img4b]

[img4a]: ./images/weekly_downtime_schedule(one-off).png "Sat - Sun scheduled downtime configuration (one-off)"


#### Sat - Sun scheduled downtime notification
**Note:** I configurrd a one-off notification for this exercise)
![alt text][img4b]

[img4b]: ./images/scheduled_downtime_1.png "Sat - Sun scheduled downtime notification"


#### Expiration notification for  Sat - Sun scheduled downtime notification
![alt text][img4c]

[img4c]: ./images/downtime_expiry_1.png "Expiration notification for Sat - Sun scheduled downtime notification"


#### 7pm to 9am, Monday - Friday,  scheduled downtime configuration (recurrent)

![alt text][img4d]

[img4d]: ./images/daily_downtime_schedule.png "7pm to 9am, Monday - Friday, scheduled downtime configuration (recurrent)"

#### 7pm to 9am, Monday - Friday,  scheduled downtime notification

![alt text][img4e]

[img4e]: ./images/scheduled_downtime_2a.png "7pm to 9am, Monday - Friday,  scheduled downtime notification"

#### Expiration notification for 7pm to 9am, Monday - Friday,  scheduled downtime notification

![alt text][img4f]

[img4f]: ./images/downtime_expiry_2.png "Expiration notification for 7pm 7pm to 9am, Monday - Friday,  scheduled downtime notification"

-----
## Collecting APM Data:
-----

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


#### Service vs. Resource <br/>
A **Service** is a **_set of processes_** that perform the same job (for example a web application, or a database). An example of a Service in this technical exercise is my flask web application (shown as **flask-app** in the image below). <br/>

A **Resource**, on the other hand, is a particular **_action_** for a service. In the case of a database, this could be a query. For example: ```SELECT * FROM users WHERE id = ?```. In web applications, these could be canonical URLs (/users/status/) or handler functions/routes. On the APM interface, these resources can be found after clicking a particular service. (See image below). <br/>

> _NB: More information can be found in the reference section_

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


### Datadog - Creative Use:

Remembering how long I had to wait in line at a restaurant on a Thanksgiving weekend, it would be interesting to use Datadog to find out about traffic at my favorite restaurants. An extra benefit will be the predicitive aspect of datadog that could predict the pattern of traffic flow, and thus help me get in during the right window.

###

------
### References
------
1. [Agent Commands](https://docs.datadoghq.com/agent/faq/agent-commands/?tab=agentv6)
2. [Building a custom check agent(Hands on instructions)](https://datadog.github.io/summit-training-session/handson/customagentcheck/)
3. [Creating and configuring custom metrics](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6)
4. [Creating time boards](https://docs.datadoghq.com/api/?lang=python#timeboards)
5. [Distributed Tracing](https://docs.datadoghq.com/tracing/faq/distributed-tracing/)
6. [Downtimes](https://docs.datadoghq.com/monitors/downtimes/)
7. [Getting started with APM](https://docs.datadoghq.com/tracing/visualization/)
8. [Graphing](https://docs.datadoghq.com/graphing/)
9. [JSON Graphing Primer](https://docs.datadoghq.com/graphing/graphing_json/)
10. [Monitoring Docker - Datadog Training Site](https://datadog.github.io/summit-training-session/handson/monitordocker/)
11. [Monitoring Flask apps with Datadog](https://www.datadoghq.com/blog/monitoring-flask-apps-with-datadog/)
12. [Timeboards](https://docs.datadoghq.com/api/?lang=python#timeboards)
13. [Tracing Python Applications](https://docs.datadoghq.com/tracing/setup/python/)
14. [Tracing Docker Applications](https://docs.datadoghq.com/tracing/setup/docker/?tab=java#tracing-from-the-host)
15. [Rollup](https://docs.datadoghq.com/graphing/functions/rollup/)
16. [What is the Difference Between "Type", "Service", "Resource", and "Name"?](https://help.datadoghq.com/hc/en-us/articles/115000702546-What-is-the-Difference-Between-Type-Service-Resource-and-Name-)

