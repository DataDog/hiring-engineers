# Solutions Engineer Challenge for Datadog

### Prerequisites - Setting up the environment

1. Set up [Vagrant Ubuntu 12.04 VM](https://www.vagrantup.com/intro/getting-started/)
  - Downloaded the [proper package](https://www.vagrantup.com/downloads.html) for operating system
  - Run these commands in terminal to have fully a running virtual machine:
    `$ vagrant init hashicorp/precise64`
    `$ vagrant up`
2. Signed up for Datadog
  - Installed Datadog Agent for OSX
  - Run api key command in terminal
    `DD_API_KEY=4XXXXXXXXXXXXXXXX bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_mac_os.sh)"`

<p align="center"> <img src="/images/prereq-1.png" height=300> </p>

### Collecting Metrics

1. Added tags in Agent config file
  - #region:west-coast
  - #role:database-mongodb

<p align="center"> <img src="/images/collecting-metrics-2.png" height=300> </p>

2. Used [Datadog integration of MongoDB](https://docs.datadoghq.com/integrations/mongo/)


I ran into a lot of errors when trying to connect to mongoDB

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

=========
Collector
=========

  Running Checks
  ==============
    cpu
    ---
      Total Runs: 10
      Metrics: 6, Total Metrics: 54
      Events: 0, Total Events: 0
      Service Checks: 0, Total Service Checks: 0
      Average Execution Time : 0ms


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

    network
    -------
      Total Runs: 10
      Metrics: 30, Total Metrics: 300
      Events: 0, Total Events: 0
      Service Checks: 0, Total Service Checks: 0
      Average Execution Time : 10122ms


    ntp
    ---
      Total Runs: 10
      Metrics: 1, Total Metrics: 10
      Events: 0, Total Events: 0
      Service Checks: 1, Total Service Checks: 10
      Average Execution Time : 84ms


    uptime
    ------
      Total Runs: 10
      Metrics: 1, Total Metrics: 10
      Events: 0, Total Events: 0
      Service Checks: 0, Total Service Checks: 0
      Average Execution Time : 0ms


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


3. Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

I successfully created a custom Agent check called `my_metric` using the instructions from [Datadog Submit](https://datadog.github.io/summit-training-session/handson/customagentcheck/)

First, I created a `randomevalue.yaml` file in the `conf.d` directory and added the following code inside:

```
init_config:

instances:
  [{}]

```
