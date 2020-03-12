My answers to the questions are here !!!

# Prerequisites - Setup the environment
Prior to the interview I had already signed up for Datadog to play along the tool and interfaces with my own company name Cogitos Consulting. After the interview I have changed the company name to “Datadog Recruiting Candidate” and start to write down this document.

I've gone with the ready captive environmet of mine and used one of my linux installs with Ubuntu distrubution with version 18.04 Bionic on VirtualBox.

# Collecting Metrics:

* Adding tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

My host shown on the Datadog Inventory Hostmap page prior to adding tags

<img src="https://live.staticflickr.com/65535/49649359148_8620b9abcb_c.jpg" width="800" height="403"></a>

I remove the comment out and added three tags to my host via editing datadog.yaml file

```
## @param tags  - list of key:value elements - optional
## List of host tags. Attached in-app to every metric, event, log, trace, and service check emitted by this Agent.
##
## Learn more about tagging: https://docs.datadoghq.com/tagging/
#
tags:
         - environment:dev
         - hostdbapp:pgsql
         - hostwebapp:tomcat
```


<img src="https://live.staticflickr.com/65535/49649939656_36421f2927_c.jpg" width="800" height="121"></a>

My Datadog web page after adding tags:

<img src="https://live.staticflickr.com/65535/49649511328_a7dbd50269_c.jpg" width="800" height="405"></a>

# * Installing a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

installed PostgreSQL

```
      cogito@devops01:~$ sudo apt update
      cogito@devops01:~$ sudo apt install postgresql postgresql-contrib
      cogito@devops01:~$ sudo -u postgres psql
      [sudo] password for cogito:
      psql (10.12 (Ubuntu 10.12-0ubuntu0.18.04.1))
      Type "help" for help.
      postgres=#

```
Installed PostgreSQL Integration using detailed descriptions on the Integration Menu. 

* Created PostgreSQL user "datadog" for Datadog, 
* Granted pg_monitor permissions for the user and check the permissions. 
* Edited /etc/datadog-agent/conf.d/postgres.d/conf.yaml file and entered the user credidentials created in the previous step to file.
* Restarted the Datadog Agent on server

<img src="https://live.staticflickr.com/65535/49649548993_0e8b934f61_c.jpg" width="800" height="403"></a>





Used pgbench to create some metrics

```
      postgres@devops01:~$ pgbench -c 25 -T 60 -S -n
      transaction type: <builtin: select only>
      scaling factor: 1
      query mode: simple
      number of clients: 25
      number of threads: 1
      duration: 60 s
      number of transactions actually processed: 411962
      latency average = 3.643 ms
      tps = 6861.908486 (including connections establishing)
      tps = 6862.216178 (excluding connections establishing)
      postgres@devops01:~$
```

Here we go, we have some meaningfull info on the Datadog page for PostgreSQL

<img src="https://live.staticflickr.com/65535/49650123566_d62bcab201_c.jpg" width="800" height="403">


# * Createing a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

1. Created the directory metrics_example.d/ in the conf.d/ folder at the root of your Agent’s configuration directory.
2. In metrics_example.d/ folder, created an empty configuration file named metrics_example.yaml with the following content:
```
instances: [{}]
```
3. Up one level from the conf.d/ folder, went to the checks.d/ folder. Created a custom check file named metrics_example.py with the content below:

```
import random

from datadog_checks.base import AgentCheck

__version__ = "1.0.0"

class MyClass(AgentCheck):
    def check(self, instance):
        self.gauge(
            "my_metric.gauge",
            random.randint(0, 1001),
            tags=["env:dev","metric_submission_type:gauge","hostname:devops01","environment:dev"],
        )
```
4. Restart the Agent and cheked if the service started correctly

```

sudo systemctl stop datadog-agent
sudo systemctl start datadog-agent

sudo systemctl status datadog-agent
  datadog-agent.service - Datadog Agent
   Loaded: loaded (/lib/systemd/system/datadog-agent.service; enabled; vendor preset: enabled)
   Active: active (running) since Thu 2020-03-12 02:24:26 UTC; 15min ago
 Main PID: 18050 (agent)
    Tasks: 8 (limit: 4660)
   CGroup: /system.slice/datadog-agent.service
           └─18050 /opt/datadog-agent/bin/agent/agent run -p /opt/datadog-agent/run/agent.pid



```
5. Checked the agent status for newly added metric
```
sudo datadog-agent status
```
In the result of the command above, looked for the Collector and Running Checks

```
=========
Collector
=========

  Running Checks
  ==============

    metrics_example (1.0.0)
    -----------------------
      Instance ID: metrics_example:d884b5186b651429 [OK]
      Configuration Source: file:/etc/datadog-agent/conf.d/metrics_example.d/metrics_example.yaml
      Total Runs: 1
      Metric Samples: Last Run: 1, Total: 1
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 0, Total: 0
      Average Execution Time : 2ms

```

Newly added "my_metric" is present on the Host Map Menu

<img src="https://live.staticflickr.com/65535/49650279746_4e246fe57c_c.jpg" width="800" height="407">


cont...


