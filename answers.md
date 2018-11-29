# Submission for Datadog Tech Exercise - Anders Iderström, late Nov 2018

# Table of contents
- [Introduction](#Introduction)
- [Prerequisites](#Prerequisites---Setup-the-environment)
  * [Setup Postgres container](#step-1-%E2%80%94-create-a-docker-container-running-postgres-with-a-service-user-for-datadog-prepared)
  * [Setup Datadog Agent container](#step-2-%E2%80%94-create-a-datadog-agent-container-with-the-postgres-integration-enabled-using-auto-discovery)
  * [Verify that the postgres integration is working](#step-3-—-Verify-that-the-postgres-integration-is-working)
- [Collecting metrics](#Collecting-Metrics)
  * [Add tags](#Add-tags)
  * [Install a database integration](#Install-a-database-integration)
  * [Create a Custom Agent Check](#Custom-Agent-Checks)
  * [Change your check’s collection interval](#Metric-collection-intervals)
  * [**Bonus question**](#Bonus-Question---Can-you-change-the-collection-interval-without-modifying-the-Python-check-file-you-created)
- [Visualizing Data](#Visualizing-Data)
  * [Utilize the Datadog API to create a Timeboard](#Utilize-the-Datadog-API-to-create-a-Timeboard)
  * [Set the Timeboard’s timeframe to the past 5 minutes](#Set-the-Timeboard’s-timeframe-to-the-past-5-minutes)
  * [Take a snapshot of this graph and use the @ notation to send it to yourself](#Take-a-snapshot-of-this-graph-and-use-the--notation-to-send-it-to-yourself)
  * [**Bonus Question**: What is the Anomaly graph displaying?](#Bonus-Question-What-is-the-Anomaly-graph-displaying)
- [Monitoring Data](#Monitoring-Data)
    * [Create a new Metric Monitor](#Create-a-new-Metric-Monitor)
    * [Further configuring the monitor’s message](#Further-configuring-the-monitor’s-message)
    * [Create different messages depending on a monitor's state](#Create-different-messages-based-on-whether-the-monitor-is-in-an-Alert-Warning-or-No-Data-state)
    * [**Bonus Question**](#Bonus-Question)
- [Collecting APM Data](#Collecting-APM-Data)
    * [Preparations](#Preparations)
    * [**Bonus Question**](#Bonus-Question-What-is-the-difference-between-a-Service-and-a-Resource)
    * [Link and a screenshot of a Dashboard with both APM and Infrastructure Metrics](#Link-and-a-screenshot-of-a-Dashboard-with-both-APM-and-Infrastructure-Metrics)
__________

# Introduction
This document covers how to set up monitoring of a test environment using Datadog and how to explore the feature set of the product.

This content is the author's submission of answers to the questions in the Datadog Tech Exercise.

Some basic prerequisites are not covered in this document since they are already well documented elsewhere:
- [Creating a Datadog trial account](https://app.datadoghq.com/signup)
- Setting up a linux host in a [public cloud free tier](https://aws.amazon.com/free/)
- [Installing Docker on your linux Docker host](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)
- [Installing the Datadog agent on your linux Docker host](https://app.datadoghq.com/account/settings#agent) (Optional, but we use this agent as the example in one exercise)

In the test environment, I have chosen to use commonly used platforms and technologies to compose a modern environment that you can set up quickly and recreate easily. Using this approach multiple pre-existing Datadog integrations can also be leveraged for inspiration and to speed up the process of creating meaningful dashboards.

I have chosen to use an AWS EC2 instance, running Ubuntu linux 18.04. This instance acts as the host for three Docker containers -  a postgres database server, a Datadog Agent container, and a small python application that provides an HTTP endpoint using Flask.


# Prerequisites - Setup the environment

To successfully complete this technical exercise, we will have set up an environment that consists of three Docker containers:
- Datadog agent (dd-agent)
- Postgres (postgres)
- Python with Flask (dd-flask)

## step 1 — create a Docker container running postgres with a service user for Datadog prepared


1. Create the shell script ``/tmp/postgres/init_datadog_user.sh`` with the content below, to be used to create a service user account:
```sh
#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" << EOSQL
        -- create the service user needed for the postgres integration in Datadog
        create user datadog with password 'Agnzr5uEKeLrt81ZRhucdjqc';
        -- grant access to a default/built-in database in postgres
        grant SELECT ON pg_stat_database to datadog;
EOSQL
```

2. Start the postgres container, making sure it can reach and reference the shell script you created by use of the -v flag. (The Postgres database runs in this container)

```sh
docker run --name postgres -v /tmp/postgres/init_datadog_user.sh:/docker-entrypoint-initdb.d/init_datadog.sh -e POSTGRES_PASSWORD=anyrandompassword -d postgres
```

## step 2 —  create a Datadog agent container with the postgres integration enabled using auto-discovery

1. Create ``/tmp/datadog/conf.d/postgres.yaml`` with the following content, to enable the postgres integration for all containers matching the specified autodiscovery identifier. Use the credentials created in step 1.

```yaml
# set the identifier used to match container image name
ad_identifiers:
   -  postgres
init_config:

# pass the credentials needed for the postgres integration service user. 
instances:
   -   host: "%%host%%"
       port: 5432
       username: datadog
       password: Agnzr5uEKeLrt81ZRhucdjqc
       tags:
            - postgres-in-a-container-in-aws
            - labcontainer
```


2. Start the Datatdog agent container
```sh
docker run -d --name dd-agent -p 8126:8126 -v /tmp/datadog/conf.d:/conf.d/ -v /tmp/datadog/checks.d:/checks.d/ -v /var/run/docker.sock:/var/run/docker.sock:ro -v /proc/:/host/proc/:ro -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro -e DD_APM_ENABLED=true —e DD_APM_NON_LOCAL_TRAFFIC=true DD_API_KEY=d554d99611a2acc7ae655efc22d2ceae datadog/agent:latest
```

Note: Here we also enable Application Performance Management which will be used later.

Note: *you must* update DD_API_KEY= to reflect *your* API key, you can find yours in the Datadog user interface, under [Integrations – APIs](https://app.datadoghq.com/account/settings#api)

## step 3 —  Verify that the postgres integration is working

1. You should now be able to list both of your currently running containers, with TCP/UDP ports allocated, using the ``docker ps`` command.
Expect this output:
```sh
ubuntu@ubuntu-1804-ec2:~$ docker ps
CONTAINER ID        IMAGE                  COMMAND                  CREATED              STATUS                                 PORTS                              NAMES
42dc97f2779a        datadog/agent:latest   "/init"                  About a minute ago   Up About a minute (health: starting)   8125/udp, 0.0.0.0:8126->8126/tcp   dd-agent
2848b08b6b06        postgres               "docker-entrypoint.s…"   6 days ago           Up 6 days                              5432/tcp                           postgres
```

2. Start a shell on the postgres container and verify connectivity and authorization locally:
Attach to the postgres container and start a shell there:
```sh
docker exec -it postgres /bin/bash
```
Run the SQL command and return OK if it exits successfully:
```sh
psql -h localhost -U datadog postgres -c "select * from pg_stat_database LIMIT(1);" && echo -e "Postgres connection - OK" || echo -e "Cannot connect to Postgres"
```

3. Using the agent's info command, fetch the agent status and look for a section regarding postgres in the Running Checks section of the returned output.
```sh
docker exec -it dd-agent agent status
```

Expect this output:
```sh
    postgres (2.2.3)
    ----------------
        Instance ID: postgres:f967211eb970e767 [OK]
        Total Runs: 15
        Metric Samples: 14, Total: 210
        Events: 0, Total: 0
        Service Checks: 1, Total: 15
        Average Execution Time : 15ms
```

4. Attach to the Datadog agent container and check the log for successfull payload delivery entries:
```sh
docker exec -it dd-agent /bin/bash
grep -i payload /var/log/datadog/agent.log
```
Expected this output:
```sh
2018-11-20 16:51:48 UTC | INFO | (transaction.go:193 in Process) | Successfully posted payload to "https://6-6-0-app.agent.datadoghq.com/intake/?api_key=*************************2ceae", the agent will only log transaction success every 20 transactions
2018-11-20 16:54:02 UTC | INFO | (transaction.go:198 in Process) | Successfully posted payload to "https://6-6-0-app.agent.datadoghq.com/api/v1/series?api_key=*************************2ceae"
```


# Collecting Metrics:

## Add tags

Using Datadog you are likely to be looking at metrics from multiple sources. Here tags are very useful since they give you a chance to select a scope for the data you a working with (like filtering in only hosts/containers of a specific environment, role or system-id). Aggregation is fundamental in Datadog and well implemented throughout the feature set, so you can expect to need tags.

How you can utilize tags in the different views and features is documented here:
https://docs.datadoghq.com/tagging/

Tags at AWS EC2 Docker host (Ubuntu 18.04): ``/etc/datadog-agent/datadog.yaml:``

```yaml
# Set the host's tags (optional)
tags:
  - systemid:3511
  - env:prod-pubcloud1
  - role:docker-host
```

In the screenshot below we can see the tags we set as well as tags automatically set by Datadog or detected by installed integrations (like the AWS EC2 integration). Tags can also be added using the user interface.
![Tags collected from AWS EC2 docker host](https://i.imgur.com/W4515fM.png)


## Install a database integration

In the [Datadog UI](https://app.datadoghq.com)
- Install the [PostgreSQL integration](https://app.datadoghq.com/account/settings#integrations/postgres) by selecting the integration tab and clicking the 'Install Integration'-button.
The status of the integration is indicated by the status bar visible when exploring the integration. Expect it to turn green and report back "This integration is working properly." within around 5 minutes.
- Verify that you can see postgres specific metrics in at least one of the two dashboards that come with the integration:
 
[Postgres - Overview](https://app.datadoghq.com/screen/integration/235/postgres---overview)
[Postgres - Metrics](https://app.datadoghq.com/dash/integration/17/postgres---metrics)

Look for a non-zero value in the ‘Postgres - Overview’ dashboard, ‘Connections’ column, ‘Max connections in use’ graph.
 
In the screenshots below we can see the Configuration tab and Install Integration button of the postgres integration.
![](https://i.imgur.com/bpW41Mu.png)
![](https://i.imgur.com/nFecfXh.png)



## Custom Agent Checks
Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

Define a template in ``/tmp/datadog/conf.d/my_custom_agent_check.yaml``:
```yaml
instances: [{}]
```

Define your check in ``/tmp/datadog/checks.d/my_custom_agent_check.py``:

```python
# the following try/except block will make the custom check compatible with any Agent version
try:
    # first, try to import the base class from old versions of the Agent...
    from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck

from random import random

# content of the special variable __version__ will be shown in the Agent status page
__version__ = "1.0.0"


class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_custom_agent_check_metric.random', random() * 1000)
```

### Verify that the custom agent check is reporting metrics as expected
``docker exec -it dd-agent agent status``

Expect this output:
```sh

    my_custom_agent_check (1.0.0)
    -----------------------------
        Instance ID: my_custom_agent_check:d884b5186b651429 [OK]
        Total Runs: 37
        Metric Samples: 1, Total: 37
        Events: 0, Total: 0
        Service Checks: 0, Total: 0
        Average Execution Time : 0s
```

## Metric collection intervals
Change your check's collection interval so that it only submits the metric once every 45 seconds.

Edit ``/tmp/datadog/conf.d/my_custom_agent_check.yaml`` and add the minimum collection interval variable:

```yaml
init_config:
  min_collection_interval: 45

instances:
    [{}]
```

Verify: ``docker exec -it dd-agent agent configcheck|grep -n6 -i interval``
Expect this output:
```sh
=== my_custom_agent_check check ===
Source: File
Instance ID: my_custom_agent_check:708819f59dba2721
{}
~
Init Config:
min_collection_interval: 45
===
```

## Bonus Question - Can you change the collection interval without modifying the Python check file you created?
Yes, the setting is applied through editing the configuration file (.yaml), not the .py script. See [Metric collection intervals](#Metric-collection-intervals) above.

# Visualizing Data:

## Utilize the Datadog API to create a Timeboard

Run the provided script create_timeboard.py.

Note: You must edit the script and set both the keys to your keys. Keylength may vary.

```sh
root@ubuntu-1804-ec2:~# python /tmp/scripts/create_timeboard.py
```
Expect this output:
```sh
{u'dash': {u'read_only': True, u'description': u'created by anders.iderstrom@gmail.com via API', u'created': u'2018-11-28T15:14:19.718395+00:00', u'title': u'Visualizing Data (Timeboard)', u'modified': u'2018-11-28T15:14:19.749883+00:00', u'created_by': {u'handle': u'anders.iderstrom@gmail.com', u'name': u'Anders Iderstr\xf6m', u'access_role': u'adm', u'verified': True, u'disabled': False, u'is_admin': True, u'role': None, u'email': u'anders.iderstrom@gmail.com', u'icon': u'https://secure.gravatar.com/avatar/e68fadd03c8d535cf34ab8abe175a63e?s=48&d=retro'}, u'graphs': [{u'definition': {u'status': u'done', u'viz': u'timeseries', u'requests': [{u'q': u'avg:my_custom_agent_check_metric.random{host:ubuntu-1804-ec2}', u'aggregator': u'avg', u'style': {u'width': u'normal', u'palette': u'dog_classic', u'type': u'solid'}, u'type': u'line', u'conditional_formats': []}], u'autoscale': u'true'}, u'title': u'my_custom_agent_check_metric.random scoped over docker host'}, {u'definition': {u'viz': u'timeseries', u'requests': [{u'q': u"anomalies(avg:postgresql.percent_usage_connections{*}, 'basic', 2)", u'aggregator': u'avg', u'style': {u'width': u'normal', u'palette': u'dog_classic', u'type': u'solid'}, u'type': u'line', u'conditional_formats': []}], u'autoscale': u'true'}, u'title': u'Avg of postgres max connections - anomaly applied'}, {u'definition': {u'viz': u'timeseries', u'requests': [{u'q': u'avg:my_custom_agent_check_metric.random{*}.rollup(sum, 3600)', u'aggregator': u'avg', u'style': {u'width': u'normal', u'palette': u'dog_classic', u'type': u'solid'}, u'type': u'line', u'conditional_formats': []}], u'autoscale': u'true'}, u'title': u'my_custom_agent_check_metric  - rollup sum past 1 hour'}], u'template_variables': [{u'default': u'host:my-host', u'prefix': u'host', u'name': u'host1'}], u'id': 1003175}, u'url': u'/dash/1003175/visualizing-data-timeboard', u'resource': u'/api/v1/dash/1003175'}
```
In the screenshot below we can see the result - [a Timeboard](https://app.datadoghq.com/dash/997294/visualizing-data-timeboard?page=0&is_auto=false&from_ts=1542886561000&to_ts=1543085281000&live=false&tv_mode=false) that contains:
- My custom metric scoped over my host.
- A metric from the Integration on my Database with the anomaly function applied.
- My custom metric with the rollup function applied to sum up all the points for the past hour into one bucket.
![Timeboard created via API](https://i.imgur.com/mInqCDM.png)


## Set the Timeboard's timeframe to the past 5 minutes

Click the keyboard icon to overview shortcuts. Use the zoom-command to zoom to 5 min. Graph size can be also be adjusted with the keyboard or by selecting size under the cogwheel/settings for the Timeboard.

Note: On macOS with Swedish keyboard layout the zoom in key combination 'alt + ]' will both zoom and resize the graphs when you try to zoom.

In the screenshot below a 5-minute range is set, and Large graph size selected.
![5 min range selected](https://i.imgur.com/lqj1eJt.png)


## Take a snapshot of this graph and use the @ notation to send it to yourself.
Click the camera icon to capture and annotate a graph. You can use @ notations. When you press enter, your comment is saved with the screenshot.

In the screenshot below we can see the message field and the @ notation being used. 
![Graph screenshot zoomed captured annotated with e-mail tagging](https://i.imgur.com/zIz7t5Y.png)


## Bonus Question: What is the Anomaly graph displaying?
The anomaly function will make the graph indicate what is considered to be within set bounds, i.e normal deviations, and highlight heavy deviations, helping you to spot (or monitor) when something isn’t quite right.

This blog article covers it in more detail, explaining amongst other things how this smart function can handle seasonality:
[Introducing anomaly detection](https://www.datadoghq.com/blog/introducing-anomaly-detection-datadog/)

In the screenshot below we can see the anomaly function enabled on a metric. The grey area indicates what values that would be considered to be within set bounds. The red part of the blue line indicates a detected anomaly.
![](https://i.imgur.com/iACmxum.png)


# Monitoring Data

## Create a new Metric Monitor
Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

- Warning threshold of 500
- Alerting threshold of 800
- And also ensure that it will notify you if there is No Data for this query over the past 10m.

In the screenshot below we can see the above specification can be set using step 1-3 in the configuration page for new monitors.
![](https://i.imgur.com/CBeWGKq.png)


## Further configuring the monitor’s message
Please configure the monitor’s message so that it will:
- Send you an email whenever the monitor triggers.
- Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.

In the screenshot below we can see the above requirements can be met using step 4-5 in the configuration page for new monitors. 
![](https://i.imgur.com/2Dw6XB3.png)

Now also configure the monitor’s message so that it will:
- Create different messages based on whether the monitor is in an Alert, Warning, or No Data state
- Include the metric value that caused the monitor to trigger and host IP when the Monitor triggers an Alert state.


Configure custom messaging to meet these requirements using the ‘Say what’s happening’ textboxes (subject and message)

#### Subject textbox:
```My custom metric is high```

#### Message textbox:
```
{{#is_alert}} Alert! My custom metric is: {{value}} {{/is_alert}}
{{#is_warning}} Warning. My custom metric has reached {{value}} on {{host.ip}} {{/is_warning}}
{{#is_no_data}} No data has been received for My custom metric on {{host.name}} ({{host.ip}}) in the last 10 minutes. {{/is_no_data}}
{{#is_recovery}} My custom metric has recovered. {{/is_recovery}}
@anders.iderstrom@gmail.com
```

In the screenshot below you can see how the e-mail sent by this monitor looks like.
![E-mail alert with variables](https://i.imgur.com/yuRAWr3.png)


## Bonus Question
Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:
- One that silences it from 7 pm to 9 am daily on M-F,
- And one that silences it all day on Sat-Sun.

Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.

In the four screenshots below you can see how to meet the requirements above and what the notification will look like.
![Scheduling downtime 1](https://i.imgur.com/1PKc11u.png)
![Scheduling downtime 2 -All day weeeknds](https://i.imgur.com/ysNppXF.png)
![Scheduling downtime 3 - Notification configuration](https://i.imgur.com/cq7cap3.png)
![Scheduling downtime 4 - Notification e-mail](https://i.imgur.com/g5Fk4Ly.png)


# Collecting APM Data:

## Preparations
Let's prepare to try out Datadog APM. To have something to monitor we will create an application container that is running a little WSGI application written in Python using the web framework Flask. The application provides an HTTP endpoint with some resources we can query.

Preferably start with a fresh build directory.


- Instrument the Python application by creating a ``Dockerfile`` for the flask app and wrapping the command with ``ddtrace-run`` to enable APM:

```
FROM python:3.5
ADD main.py /
RUN pip install datadog ddtrace flask
ENTRYPOINT [ "ddtrace-run" ]
CMD [ "python3", "main.py" ]
```

This is documented at https://docs.datadoghq.com/tracing/setup/python/

- Create a main.py file with the code provided from https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md

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

- Build a docker image
```sh
docker build -t dd-flask .
```

- Run the container you built in daemon mode. Expose the port used by the application on the Docker host and set destination for traces (to the gateway address of the Datadog Agent container):
```sh
docker run --name dd-flask -d -e DATADOG_TRACE_AGENT_HOSTNAME=172.17.0.1 -p 5050:5050 dd-flask
```

- Verify that the application is working and that you are not getting errors from ddtrace:
```sh
docker logs dd-flask`
``` 

Expect this output:
``
DEBUG:ddtrace.api:reported 2 services
``

Note: A couple of “HTTP error status 400” errors are expected

- Now generate some traces by hitting the HTTP resources with some tool like curl or links (where you can easily generate multiple requests with CTRL-R).
```sh
links http://localhost:5050
links http://localhost:5050/api/apm
links http://localhost:5050/api/trace
links http://localhost:5050/api/does_not_exist_in_API
```

- Now let's verify traces are successfully being delivered to Datadog API:
```sh
docker logs dd-agent
```

Expect this output:
```
[ TRACE ] 2018-11-27 13:40:48 INFO (trace_writer.go:97) - flushed trace payload to the API, time:371.367127ms, size:717 bytes
```


## Bonus Question: What is the difference between a Service and a Resource?
A Service typically represents an application or several processes that provide some feature.
A Resource is typically a query/call to a specific part/subset of a Service.

## Link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
A Timeboard was composed exporting graphs from [‘APM  - Services’](https://app.datadoghq.com/apm/services) and from two relevant Infrastructure integrations for the flask app - AWS EC2 and Docker Overview. By cloning these default dashboards the json for widgets can easily be copied and reused in a custom dashboard.
Link: https://app.datadoghq.com/dash/1001399/combining-apm--infrastructure-timeboard?page=0&is_auto=false&from_ts=1543330740000&to_ts=1543334340000&live=false&tile_size=m

In the screenshot below we can see a basic Timeboard combining APM and Infrastructure metrics from relevant integrations with load and system memory usage across all environments and platforms.
![](https://i.imgur.com/qXZ7sds.png)


# Final Question:

## Is there anything creative you would use Datadog for?
If major mobile telephone network operators (like Tele2) would utilize Datadog and its functions to find and address general problem areas, the quality of service on calls, message delivery, and data transfer can be improved. By adding geo-tagging on top of that, specific problem areas can be ranked/found and the customer satisfaction baseline can be raised significantly as well.

# Feedback:
If you are running a Python app in a Docker container, https://docs.datadoghq.com/tracing/setup/python/ combined with https://docs.datadoghq.com/tracing/setup/docker/?tab=python
may lead you to believe the app needs BOTH wrapping with ddtrace-run AND configuration of tracing in the application code). This can be made more clear in the first webpage, by complementing the example of how to wrap your python app with ddtrace-run, with an example of how to alternatively set the destination using environment variables when starting the Python application container.