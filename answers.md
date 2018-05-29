# Solutions Engineer Challenge for Datadog

## Prerequisites - Setting up the environment

1. Set up [Vagrant Ubuntu 12.04 VM](https://www.vagrantup.com/intro/getting-started/)
  - I downloaded the [proper package](https://www.vagrantup.com/downloads.html) for the operating system
  - I ran the following commands in terminal to have fully a running virtual machine:
    - `$ vagrant init hashicorp/precise64`
    - `$ vagrant up`

2. Signed up for Datadog
  - Installed Datadog Agent for OSX
  - Run api key command in terminal
    `DD_API_KEY=4XXXXXXXXXXXXXXXX bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_mac_os.sh)"`

<p align="center"> <img src="/images/prereq-1.png" height=300> </p>

## Collecting Metrics

> Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

I added the following tags in Agent config file:
  - #region:west-coast
  - #role:database-mongodb

<p align="center"> <img src="/images/collecting-metrics-2.png" height=300> </p>

> Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

 I used MongoDB and the [Datadog integration of MongoDB](https://docs.datadoghq.com/integrations/mongo/)


After several attempts and research, I was not able to connect to MongoDB successfully.  

```
==============
Agent (v6.2.0)
==============

  Status date: 2018-05-27 10:44:46.301892 UTC
  Pid: 82003
  Python Version: 2.7.10
  Logs:
  Check Runners: 1
  Log Level: info

  Paths
  =====
    Config File: /opt/datadog-agent/etc/datadog.yaml
    conf.d: /opt/datadog-agent/etc/conf.d
    checks.d: /opt/datadog-agent/etc/checks.d

.............................
.............................

    mongo
    -----
      Total Runs: 10
      Metrics: 0, Total Metrics: 0
      Events: 0, Total Events: 0
      Service Checks: 1, Total Service Checks: 10
      Average Execution Time : 30228ms
      Error: localhost:27016: [Errno 61] Connection refused
      Traceback (most recent call last):
        File "/opt/datadog-agent/bin/agent/dist/checks/__init__.py", line 332, in run
          self.check(copy.deepcopy(self.instances[0]))
        File "/opt/datadog-agent/embedded/lib/python2.7/site-packages/datadog_checks/mongo/mongo.py", line 754, in check
          status = db.command('serverStatus', tcmalloc=collect_tcmalloc_metrics)
        File "/opt/datadog-agent/embedded/lib/python2.7/site-packages/pymongo/database.py", line 513, in command
          with client._socket_for_reads(read_preference) as (sock_info, slave_ok):
        File "/opt/datadog-agent/embedded/lib/python2.7/contextlib.py", line 17, in __enter__
          return self.gen.next()
        File "/opt/datadog-agent/embedded/lib/python2.7/site-packages/pymongo/mongo_client.py", line 904, in _socket_for_reads
          with self._get_socket(read_preference) as sock_info:
        File "/opt/datadog-agent/embedded/lib/python2.7/contextlib.py", line 17, in __enter__
          return self.gen.next()
        File "/opt/datadog-agent/embedded/lib/python2.7/site-packages/pymongo/mongo_client.py", line 868, in _get_socket
          server = self._get_topology().select_server(selector)
        File "/opt/datadog-agent/embedded/lib/python2.7/site-packages/pymongo/topology.py", line 214, in select_server
          address))
        File "/opt/datadog-agent/embedded/lib/python2.7/site-packages/pymongo/topology.py", line 189, in select_servers
          self._error_message(selector))
      ServerSelectionTimeoutError: localhost:27016: [Errno 61] Connection refused

.............................
.............................

  Config Errors
  ==============
    disk
    ----
      yaml: unmarshal errors:
  line 14: cannot unmarshal !!map into []check.ConfigRawMap

  Loading Errors
  ==============
    apm
    ---
      Core Check Loader:
        Could not configure check APM Agent: APM agent disabled through main configuration file

      JMX Check Loader:
        check is not a jmx check, or unable to determine if it's so

      Python Check Loader:
        No module named apm

========
JMXFetch
========

  Initialized checks
  ==================
    no checks

  Failed checks
  =============
    no checks

=========
Forwarder
=========

  CheckRunsV1: 29
  IntakeV1: 2
  RetryQueueSize: 0
  Success: 60
  TimeseriesV1: 29

  API Keys status
  ===============
    https://6-2-0-app.agent.datadoghq.com,*************************39bad: API Key valid

==========
Logs Agent
==========

  mongo
  -----
    Type: file
    Path: /var/log/mongodb/mongodb.log
    Status: Error: File /var/log/mongodb/mongodb.log does not exist

.............................
.............................

  ```

> Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

I successfully created a custom Agent check called `my_metric` using the instructions from [Datadog Submit](https://datadog.github.io/summit-training-session/handson/customagentcheck/)

Since the names of the configuration and check files must match, I named the files `randomvalue.yaml` and `randomvalue.py`.

First, I created a `randomvalue.yaml` file in the `conf.d` directory and added the following code inside:

```
init_config:

instances:
  [{}]

```

Then, I created a `randomevalue.py` file in `/etc/checks.d` and added the following code:

```
import random
from checks import AgentCheck
class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', random.randint(0, 1000))

```

I restarted the Agent and got the new metric to show up successfully in the Metric Summary.

<p align="center"> <img src="/images/my-metric.png" height=300> </p>


> Change your check's collection interval so that it only submits the metric once every 45 seconds.

In the `randomvalue.yaml` file, I added the following snippet of code to change the default check of every 15 seconds to 45 seconds:

```
init_config:
  min_collection_interval: 45

instances:
  [{}]
```

> Bonus Question Can you change the collection interval without modifying the Python check file you created?

Yes, the respective `.yaml` file can be modified and the python check file can be left untouched.

## Visualizing Data

> Utilize the Datadog API to create a Timeboard that contains:

>  Your custom metric scoped over your host.
>  Any metric from the Integration on your Database with the anomaly function applied.
>  Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

To utilize the Datadog API, I ran `brew upgrade coreutils` since it was already installed in my computer.
I then created a new Timeseries dashboard by simply inputting the Metric name, host name, rollup sum, and time interval. The json tab creates the requests desired.


JSON created:
```
{
  "requests": [
    {
      "q": "avg:my_metric{host:StacyStacesMBP.lan}.rollup(sum, 3600)",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      },
      "conditional_formats": [],
      "aggregator": "avg"
    },
    {
      "q": "per_hour(avg:my_metric{host:StacyStacesMBP.lan})",
      "type": "line",
      "style": {
        "palette": "dog_classic",
        "type": "solid",
        "width": "normal"
      }
    }
  ],
  "viz": "timeseries",
  "autoscale": true,
  "status": "done"
}

```
<p align="center"> <img src="/images/timeboard.png" height=300> </p>


> Once this is created, access the Dashboard from your Dashboard List in the UI:

> Set the Timeboard's timeframe to the past 5 minutes
 Take a snapshot of this graph and use the @ notation to send it to yourself.
 Bonus Question: What is the Anomaly graph displaying?


Last 5 minutes screenshot emailed using `@` notation:

<p align="center"> <img src="/images/metric_5mins.png" height=300> </p>

>Bonus Question: What is the Anomaly graph displaying?

The [Anomaly graph](https://www.datadoghq.com/blog/introducing-anomaly-detection-datadog/) detects any unusual activity by analyzing the metrics's history behavior and by following the trends in some timeseries.


## Monitoring Data

>Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

>Warning threshold of 500
Alerting threshold of 800
And also ensure that it will notify you if there is No Data for this query over the past 10m.

By clicking on the `Create Monitor` tab of the `my_metric` graph, I was able to set the alert conditions as shown below.

<p align="center"> <img src="/images/metric_conditions.png" height=300> </p>

I then configured the monitor's message so that a more descriptive notification of the problem would be emailed.

<p align="center"> <img src="/images/alerts_mymetric.png" height=300> </p>


Email received from Datadog about status:

<p align="center"> <img src="/images/email_warning.png" height=300> </p>

Within a minute, I received another email notifying me that the status has been **recovered**.
(And then several after that)

<p align="center"> <img src="/images/email_recovered.png" height=300> </p>



> Bonus Question: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office.

I configured the notifications of the monitor to be silenced from **7:00pm to 9:00am Monday - Friday**

<p align="center"> <img src="/images/schedule_downtime.png" height=400> </p>

After configuration, I received an email about the change.

<p align="center"> <img src="/images/email_downtimeMF.png" height=300> </p>

I then configured the notifcations of the monitor to be silenced from **12:00AM Saturday to 12:00AM**

<p align="center"> <img src="/images/schedule_downtime2.png" height=400> </p>

<p align="center"> <img src="/images/email_downtimeSS.png" height=300> </p>



## Collecting APM Data

I ran into errors in collecting APM data, as shown in the image below.

First, I installed the Python client in the terminal:
`pip install ddtrace`

I ran into a few errors and had to run `pip install blinker` to clear one of the errors in the console.

I installed blinker `pip install blinker`

Error I received:

<p align="center"> <img src="/images/apm_error.png" height=300> </p>


>Bonus Question: What is the difference between a Service and a Resource?

A **service** is a set of processes that do the same job and work together to provide a feature set. This may entail a database, a web-application, queries, etc. A web application may have several services, depending on the complexity of the application.

A **resource** is an action that is called with whatever the service provide - such as an endpoint or query. For example: `/user/home`.


## Final Question

>Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!
Is there anything creative you would use Datadog for?

As a tennis player, I would love to use Datadog to check out any open public courts and see if they are in use. This would save time and disappointment of getting ready and traveling to the courts only to find that they are taken by other tennis players. With the help of Datadog and the integration of the Raspberry Pi to sensor movement, this would save tennis players time.
