# Datadog Deployment
This is an account of my test Datadog deployment

Graham Hares  
11th April 2020

## Environment
Testing was made with a number of environments;

* A Centos7 VM running on libvirtd fedora server hypervisor. Docker daemon was also configured on this instance to observe the containers extension of Datadog.
* Custom Centos7 with systemd docker image with Datadog driver script pre loaded and environment variables passed at runtime, this allowed quick testing of multiple agent extensions in their own docker container instance on a Mac. see: https://github.com/grahamnscp/ddagent-centos


## Exercises
The exercises covered in this test can be found here: https://github.com/DataDog/hiring-engineers/blob/solutions-engineer/README.md#the-exercise

## Agent deployment
The datadog agent is available in multiple deployment forms for a number of host OS platforms.
The official installation docs can be found here: https://docs.datadoghq.com/getting_started/agent/?tab=datadogussite#installation  
note: To view the detailed agent deployment instructions per OS you have to be an authenticated user, you can sign up for the free trial https://www.datadoghq.com/lpg/

### Linux VM datadog agent deployment
For the Linux VM host (dgagent.glocal.lab) the trial unique API ID was used to create environment variables used by the agent deployment script, along with a refernce to the agent version and the Datadog hosted backend SaaS instance, which in this case was **.eu**:
```
centos$ DD_AGENT_MAJOR_VERSION=7
centos$ DD_API_KEY=<Your DD API Key Value Here>
centos$ DD_SITE="datadoghq.eu"
```
Download and run the deployment script as follows:
```
centos$ curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh -o dd-agent-install_script.sh
centos$ chmod +x ./dd-agent-install_script.sh
centos$ sudo ./dd-agent-install_script.sh
```

The agent deployment script creates a package manager repository and installs the agent from a package, in this case an rpm repo was created:
```
centos$ $ cat /etc/yum.repos.d/datadog.repo
[datadog]
name = Datadog, Inc.
baseurl = https://yum.datadoghq.com/stable/7/x86_64/
enabled=1
gpgcheck=1
repo_gpgcheck=0
priority=1
gpgkey=https://yum.datadoghq.com/DATADOG_RPM_KEY_E09422B3.public

centos$ rpm -qf /opt/datadog-agent/
datadog-agent-7.18.1-1.x86_64
```

The main agent deployment location is:
* /opt/datadog-agent - main agent deployment directory
* /etc/datadog-agent - agent configuration files, including inbuilt integration configuration samples
* /usr/lib/systemd - systemd service configuration files
* /etc/init - for use if the agent is started by the init process instead of systemd, rcX.d etc
* /usr/bin/datadog-agent - soft link to -> /opt/datadog-agent/bin/agent/agent (ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked (uses shared libs)

For configuration, the main file is; /etc/datadog-agent/datadog.yaml
'built-in' integration configuration files are enabled and configured as required by creating a yaml file under /etc/datadog-agent/conf.d/ directory. A number of sub directories are present from the package installation with example files.

On linux the agent runs can run as a systemd service, and therefore needs starting and configuring to start on host boot:
```
centos$ sudo systemctl enable datadog-agent
centos$ sudo systemctl start datadog agent

centos$ systemctl status datadog-agent

● datadog-agent.service - Datadog Agent
   Loaded: loaded (/usr/lib/systemd/system/datadog-agent.service; enabled; vendor preset: disabled)
   Active: active (running) since Fri 2020-04-10 19:54:28 UTC; 21h ago
 Main PID: 21806 (agent)
    Tasks: 11
   Memory: 50.0M
   CGroup: /system.slice/datadog-agent.service
           └─21806 /opt/datadog-agent/bin/agent/agent run -p /opt/datadog-agent/run/agent.pid

Apr 11 17:24:08 dgagent.glocal.lab agent[21806]: 2020-04-11 17:24:08 UTC | CORE | WARN | (pkg/collector/python/datadog_agent.go:118 in LogMessage) | d...
Apr 11 17:24:08 dgagent.glocal.lab agent[21806]: 2020-04-11 17:24:08 UTC | CORE | WARN | (pkg/collector/python/datadog_agent.go:118 in LogMess...d35e760'
Apr 11 17:24:23 dgagent.glocal.lab agent[21806]: 2020-04-11 17:24:23 UTC | CORE | WARN | (pkg/collector/python/datadog_agent.go:118 in LogMessage) | d...
Apr 11 17:24:23 dgagent.glocal.lab agent[21806]: 2020-04-11 17:24:23 UTC | CORE | WARN | (pkg/collector/python/datadog_agent.go:118 in LogMess...d35e760'
Apr 11 17:24:32 dgagent.glocal.lab agent[21806]: 2020-04-11 17:24:32 UTC | CORE | INFO | (pkg/serializer/serializer.go:346 in SendMetadata) | ...1 bytes.
Apr 11 17:24:32 dgagent.glocal.lab agent[21806]: 2020-04-11 17:24:32 UTC | CORE | INFO | (pkg/serializer/serializer.go:366 in SendJSONToV1Inta...4 bytes.
Apr 11 17:24:34 dgagent.glocal.lab agent[21806]: 2020-04-11 17:24:34 UTC | CORE | INFO | (pkg/metadata/host/host.go:161 in getNetworkMeta) | c...twork ID
Apr 11 17:24:34 dgagent.glocal.lab agent[21806]: 2020-04-11 17:24:34 UTC | CORE | INFO | (pkg/serializer/serializer.go:346 in SendMetadata) | ...2 bytes.
Apr 11 17:24:38 dgagent.glocal.lab agent[21806]: 2020-04-11 17:24:38 UTC | CORE | WARN | (pkg/collector/python/datadog_agent.go:118 in LogMessage) | d...
Apr 11 17:24:38 dgagent.glocal.lab agent[21806]: 2020-04-11 17:24:38 UTC | CORE | WARN | (pkg/collector/python/datadog_agent.go:118 in LogMess...d35e760'
Hint: Some lines were ellipsized, use -l to show in full.
```

Full agent logs can be obtained from journald:
```
centos$ journalctl -u datadog-agent | grep Starting | tail -1
Apr 10 19:54:28 dgagent.glocal.lab agent[21806]: 2020-04-10 19:54:28 UTC | CORE | INFO | (cmd/agent/app/run.go:180 in StartAgent) | Starting Datadog Agent v7.18.1
```
  
### Agent Tags
From the official docs on tagging: https://docs.datadoghq.com/tagging/  
"Tags are a way of adding dimensions to metrics, so they can be filtered, aggregated, and compared in Datadog visualizations. Using tags enables you to observe aggregate performance across a number of hosts and (optionally) narrow the set further based on specific elements. In summary, tagging is a method to observe aggregate data points."

There are a number of reserved tag name values which are potentially active by default, for example: host: these tags should not be configured in your personal tags.  Agent tags are added by uncommenting the tags: block in the agent or integration configuration file and restarting the agent.  

For example here are some tags added to the Linux VM (file: /etc/datadog-agent/datadog.yaml)
```
## @param tags  - list of key:value elements - optional
## List of host tags. Attached in-app to every metric, event, log, trace, and service check emitted by this Agent.
##
## Learn more about tagging: https://docs.datadoghq.com/tagging/
#
tags:
  - genv:dev_test
  - owner:grahamnscp
  - "qowner:grahamnscp"
  - spacetag: tag:with:space
#   - <TAG_KEY>:<TAG_VALUE>
```
And restarting the agent via systemd control:
```
centos$ sudo systemctl restart datadog-agent
```

The host agent tag values can be viewed in the Datadog console against the various agent instances:  

<img src="pictures/agent-tags.png" alt="agent_tags_example" width="900" title="Datadog agent tags example"/>

  
## Agent Integrations
The various platform Datadog agents have an extensive number of 'integrations' built in that can be enabled as required, there is a github repository here where they can be viewed: https://github.com/DataDog/integrations-core  
Custom integrations can be created, see some community contributed samples here: https://github.com/DataDog/integrations-extras  

There are two sides to enabling an integration, the agent needs to be configured to check the service's data, this is achieved by placing a configuration file in the /etc/datadog-agent/conf.d directory, see example for **MongoDB**:  

First install mongdb in Centos7:
```
# cat <<EOF>>/etc/yum.repos.d/mongodb.repo
[mongodb-org-3.2]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/\$releasever/mongodb-org/3.2/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-3.2.asc
EOF

# yum install mongodb-org -y
# cat <<EOF>> //etc/security/limits.d/mongod.conf
mongod soft nproc 64000
mongod hard nproc 64000
mongod soft nofile 64000
mongod hard nofile 64000
EOF

# sysctl -p

# systemctl start mongod

# mongo
use admin
db.createUser(
  {
    user: "datadog",
    pwd: "datadog123",
    roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
  }
)
show users
{
	"_id" : "admin.datadog",
	"user" : "datadog",
	"db" : "admin",
	"roles" : [
		{
			"role" : "userAdminAnyDatabase",
			"db" : "admin"
		}
	]
}
use mydb
db.createCollection("mycollection")
exit
```

Then enable the agent to observe mongodb:  

```
centos$ sudo cp /etc/datadog-agent/conf.d/mongo.d/conf.yaml.example /etc/datadog-agent/conf.d/mongo.d/conf.yaml
```

Modify the mongo integration config as required, add tags, enable log reading etc.  The connection string configured in this example was:

```
  - server: mongodb://datadog:datadog123@localhost:27016/admin
```

Restart the datadog agent and check integration is loaded:

```
centos$ sudo systemctl restart datadog-agent
centos$ journalctl -u datadog-agent | grep mongo
Apr 11 18:13:06 dgagent.glocal.lab agent[32367]: 2020-04-11 18:13:06 UTC | CORE | WARN | (pkg/collector/python/check.go:256 in Configure) | passing `agentConfig` to the constructor is deprecated, please use the `get_config` function from the 'datadog_agent' package (mongo).
Apr 11 18:13:06 dgagent.glocal.lab agent[32367]: 2020-04-11 18:13:06 UTC | CORE | INFO | (pkg/collector/scheduler/scheduler.go:83 in Enter) | Scheduling check mongo with an interval of 15s
Apr 11 18:13:07 dgagent.glocal.lab agent[32367]: 2020-04-11 18:13:07 UTC | CORE | INFO | (pkg/collector/runner/runner.go:261 in work) | Running check mongo
```

Next add the mondodb integration into the Datadog dashboard, this is done by navigating to the Integrations side tab, searching for mongodb and clicking Install..  

<img src="pictures/mongodb-integration-install.png" alt="mongodb_agent_extension_install" width="900" title="Datadog agent mongodb integration install example"/>  
  
Scroll to the bottom of the instructions popup dialogue, checking you have configured things the way you want them and click on 'Install Integration':  

<img src="pictures/mongodb-integration-install2.png" alt="mongodb_agent_extension_install" width="900" title="Datadog agent mongodb integration install example"/>  
  
Navigate back to the main Integrations screen and the new active integration can be seen in the list Installed list now:  

<img src="pictures/mongodb-integration-install3.png" alt="mongodb_agent_extension_install" width="900" title="Datadog agent mongodb integration install example"/>  
  
A new MongoDB dashboard is now available:  

<img src="pictures/mongodb-dashboard-list.png" alt="mongodb_agent_extension_install" width="900" title="Datadog agent mongodb integration install example"/>  
-  
<img src="pictures/mongodb-dashboard.png" alt="mongodb_agent_extension_install" width="900" title="Datadog agent mongodb integration install example"/>  
Notice above that there is 1 host available to observe.  

  
## Custom Agent Check
**Requirement:** 
* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.  
* Change your check's collection interval so that it only submits the metric once every 45 seconds.

Custom Agent Checks can be created to collect metrics independently from Datadog agent updates.

Official docs here: https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6v7

A custom check script is placed in the /etc/datadog-agent/checks.d/ directory and a configuration **with the same name** placed in the /etc/datadog-agent/conf.d directory.

/etc/datadog-agent/checks.d/mycheck.py:
```
from datadog_checks.base import AgentCheck
from checks import AgentCheck
import random

class MyCheck(AgentCheck):
  def check(self, instance):
    self.gauge('mycheck', random.randrange(1000))
```

/etc/datadog-agent/conf.d/mycheck.yaml:
```
init_config:

instances:
  - min_collection_interval: 45

```
Note: The **min_collection_interval** option was added to indicate that the check should be collected every 45 seconds.

Test that the new check is active:
```
centos$ sudo systemctl restart datadog-agent  

centos$ journalctl -u datadog-agent | grep mycheck
Apr 11 19:25:18 dgagent.glocal.lab agent[17130]: 2020-04-11 19:25:18 UTC | CORE | INFO | (pkg/collector/runner/runner.go:261 in work) | Running check mycheck
Apr 11 19:25:18 dgagent.glocal.lab agent[17130]: 2020-04-11 19:25:18 UTC | CORE | INFO | (pkg/collector/runner/runner.go:327 in work) | Done running check mycheck
Apr 11 19:25:41 dgagent.glocal.lab agent[17713]: 2020-04-11 19:25:41 UTC | CORE | INFO | (pkg/collector/scheduler/scheduler.go:83 in Enter) | Scheduling check mycheck with an interval of 45s
```

## Visualizing Data

**Requirement:**  

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Created *my_metric* agent check to capture more data.  
Reference docs: https://docs.datadoghq.com/developers/metrics/agent_metrics_submission

Agent check /etc/datadog-agent/checks.d/my_metric.py:
```
from datadog_checks.base import AgentCheck
from checks import AgentCheck
import random

class MyMetric(AgentCheck):
  def check(self, instance):
    self.count( "my_metric.count", 2, tags=["env:dev","metric_submission_type:count"])
    self.count( "my_metric.decrement", -1, tags=["env:dev","metric_submission_type:count"])
    self.count( "my_metric.increment", 1, tags=["env:dev","metric_submission_type:count"])
    self.rate( "my_metric.rate", 1, tags=["env:dev","metric_submission_type:rate"])
    self.gauge('my_metric.gauge', random.randrange(1000), tags=["env:dev","metric_submission_type:gauge"])
    self.monotonic_count( "my_metric.monotonic_count", 2, tags=["env:dev","metric_submission_type:monotonic_count"])

    # Calling the functions below twice simulates several metrics submissions during one Agent run:
    self.histogram( "my_metric.histogram", random.randrange(1000), tags=["env:dev","metric_submission_type:histogram"])
    self.histogram( "my_metric.histogram", random.randrange(1000), tags=["env:dev","metric_submission_type:histogram"])
```

Agent config /etc/datadog-agent/conf.d/my_check.d/conf.yaml:
```
init_config:

instances:
  - min_collection_interval: 45
```

Quick Test with dd-agent utility:
```
# sudo -u dd-agent -- datadog-agent check my_metric
...
=== Series ===
{
  "series": [
    {
      "metric": "my_metric.gauge",
      "points": [
        [
          1586774815,
          770
        ]
      ],
      "tags": [
        "env:dev",
        "metric_submission_type:gauge"
      ],
      "host": "dgagent.glocal.lab",
      "type": "gauge",
      "interval": 0,
      "source_type_name": "System"
    },
    {
      "metric": "my_metric.histogram.max",
      "points": [
        [
          1586774815,
          769
        ]
      ],
      "tags": [
        "env:dev",
        "metric_submission_type:histogram"
      ],
      "host": "dgagent.glocal.lab",
      "type": "gauge",
      "interval": 0,
      "source_type_name": "System"
    },
    {
      "metric": "my_metric.histogram.median",
      "points": [
        [
          1586774815,
          433
        ]
      ],
      "tags": [
        "env:dev",
        "metric_submission_type:histogram"
      ],
      "host": "dgagent.glocal.lab",
      "type": "gauge",
      "interval": 0,
      "source_type_name": "System"
    },
    {
      "metric": "my_metric.histogram.avg",
      "points": [
        [
          1586774815,
          601
        ]
      ],
      "tags": [
        "env:dev",
        "metric_submission_type:histogram"
      ],
      "host": "dgagent.glocal.lab",
      "type": "gauge",
      "interval": 0,
      "source_type_name": "System"
    },
    {
      "metric": "my_metric.histogram.count",
      "points": [
        [
          1586774815,
          2
        ]
      ],
      "tags": [
        "env:dev",
        "metric_submission_type:histogram"
      ],
      "host": "dgagent.glocal.lab",
      "type": "rate",
      "interval": 0,
      "source_type_name": "System"
    },
    {
      "metric": "my_metric.histogram.95percentile",
      "points": [
        [
          1586774815,
          769
        ]
      ],
      "tags": [
        "env:dev",
        "metric_submission_type:histogram"
      ],
      "host": "dgagent.glocal.lab",
      "type": "gauge",
      "interval": 0,
      "source_type_name": "System"
    },
    {
      "metric": "my_metric.count",
      "points": [
        [
          1586774815,
          2
        ]
      ],
      "tags": [
        "env:dev",
        "metric_submission_type:count"
      ],
      "host": "dgagent.glocal.lab",
      "type": "count",
      "interval": 0,
      "source_type_name": "System"
    },
    {
      "metric": "my_metric.decrement",
      "points": [
        [
          1586774815,
          -1
        ]
      ],
      "tags": [
        "env:dev",
        "metric_submission_type:count"
      ],
      "host": "dgagent.glocal.lab",
      "type": "count",
      "interval": 0,
      "source_type_name": "System"
    },
    {
      "metric": "my_metric.increment",
      "points": [
        [
          1586774815,
          1
        ]
      ],
      "tags": [
        "env:dev",
        "metric_submission_type:count"
      ],
      "host": "dgagent.glocal.lab",
      "type": "count",
      "interval": 0,
      "source_type_name": "System"
    }
  ]
}
=========
Collector
=========

  Running Checks
  ==============

    my_metric (unversioned)
    -----------------------
      Instance ID: my_metric:5ba864f3937b5bad [OK]
      Configuration Source: file:/etc/datadog-agent/conf.d/my_metric.d/conf.yaml
      Total Runs: 1
      Metric Samples: Last Run: 8, Total: 8
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 0, Total: 0
      Average Execution Time : 2ms
      Last Execution Date : 2020-04-13 10:46:55.000000 UTC
      Last Successful Execution Date : 2020-04-13 10:46:55.000000 UTC

Check has run only once, if some metrics are missing you can try again with --check-rate to see any other metric if available.
```

my_metric Timeboard:  
<img src="pictures/my_metric-timeboard.png" alt="my_metric" width="900" title="Datadog agent my_metric"/>

my_metric Anomaly Monitor:  
<img src="pictures/my_metric-anomaly-monitor.png" alt="my_metric" width="900" title="Datadog agent my_metric"/>

Sample email notification from the monitor trigger:  
<img src="pictures/my_metric-anomaly-monitor-notification.png" alt="my_metric" width="900" title="Datadog agent my_metric"/>
 
Sample API script to create an example timeboard:
```
!#/bin/bash
api_key=<Your Datadog API Key value here>
app_key=13969b2a81854ff84b1705865086b4418830f0fb

curl -X POST -H "Content-type: application/json" \
-d '{
        "width": 1024,
        "height": 768,
        "board_title": "dogapi my_metric",
        "widgets": [
            {
              "type": "image",
              "height": 20,
              "width": 32,
              "y": 7,
              "x": 32,
              "url": "https://thumbs.dreamstime.com/b/teacher-programming-icon-isolated-white-background-teacher-programming-icon-119030737.jpg"
            }
        ]
}' \
"https://api.datadoghq.eu/api/v1/screen?api_key=${api_key}&application_key=${app_key}"
```
More study would be involved in mapping the specific metrics via this API to create detailed timeboard content!  

Round tripping the dashboard is useful, create it initially, edit via the UI to change the metric display a bit and capture the JSON view details to put back into the python source, delete the dashboard and recreate..  

Here's a sample dashboard created via the API with python:

```
from datadog import initialize, api

options = {
  'api_key': '<Your Datadog API Key value here>',
  'app_key': '13969b2a81854ff84b1705865086b4418830f0fb',
  'api_host': 'https://api.datadoghq.eu'
}

initialize(**options)

title = "Metric Timeboard"
description = "my_metric timeboard."

a_graph = {
  "title": "my_metric",
  "definition": {
    "events": [],
    "requests": [
      {"q": "my_metric.gauge{*}"}
    ],
    "viz": "timeseries"
  }
}

anomaly_graph = {
  "title": "Metric anomaly graph",
  "definition": {
    "events": [],
    "requests": [
      {"q": "anomalies(avg:my_metric.gauge{*}.as_count(), 'basic', 2)"}
    ],
    "viz": "timeseries"
  }
}

rollup_graph = {
  "title": "Metric over one hour",
  "definition": {
    "events": [],
    "requests": [
      {"q": "avg:my_metric.gauge{*}.rollup(avg, 3600)"}
    ],
    "viz": "query_value"
  }
}

graphs = []
graphs.append(a_graph)
graphs.append(anomaly_graph)
graphs.append(rollup_graph)

host_variables = [{
  "name": "dgagent.glocal.lab",
  "prefix": "host",
  "default": "hosts:dgagent.glocal.lab"
}]

read_only = True

print(api.Timeboard.create(title=title,
                           description=description,
                           graphs=graphs,
                           template_variables=host_variables,
                           read_only=read_only))

```

Loading:
```
# python3 my_metric_timeboard.py
{'dash': {'read_only': True, 'graphs': [{'definition': {'viz': 'timeseries', 'requests': [{'q': 'my_metric.gauge{*}'}], 'events': []}, 'title': 'my_metric'}, {'definition': {'viz': 'timeseries', 'requests': [{'q': "anomalies(avg:mysql.performance.cpu_time{*}.as_count(), 'basic', 2)"}], 'events': []}, 'title': 'Metric anomaly graph'}, {'definition': {'precision': 2, 'viz': 'query_value', 'requests': [{'q': 'avg:my_metric.gauge{*}.rollup(sum, 3600)'}], 'events': []}, 'title': 'Metric over one hour'}], 'template_variables': [{'default': 'hosts:dgagent.glocal.lab', 'prefix': 'host', 'name': 'dgagent.glocal.lab'}], 'description': 'my_metric timeboard.', 'title': 'Metric timeboard', 'created': '2020-04-13T13:26:58.748888+00:00', 'new_id': '3h5-ciz-mxd', 'id': 22008, 'created_by': {'disabled': False, 'handle': 'graham@buildsi.com', 'name': 'Graham Hares', 'title': 'Solutions Engineer', 'is_admin': True, 'role': 'Solutions Engineer', 'access_role': 'adm', 'verified': True, 'email': 'graham@buildsi.com', 'icon': 'https://secure.gravatar.com/avatar/d2b40107d5c189d6ed1f9ea968582440?s=48&d=retro'}, 'modified': '2020-04-13T13:26:58.748888+00:00'}, 'url': '/dash/22008/metric-timeboard', 'resource': '/api/v1/dash/22008'}
```
Resultant dashboard:
<img src="pictures/my_metric-timeboard-python.png" alt="mongodb_agent_extension_install" width="900" title="Datadog agent mongodb integration install example"/>


## Anomaly Monitor

Docs reference: https://docs.datadoghq.com/monitors/monitor_types/anomaly/   

"Anomaly detection is an algorithmic feature that identifies when a metric is behaving differently than it has in the past, taking into account trends, seasonal day-of-week, and time-of-day patterns. It is well-suited for metrics with strong trends and recurring patterns that are hard to monitor with threshold-based alerting."

## Collecting APM Data:

Docs for APM are here: https://app.datadoghq.eu/apm/docs?architecture=host-based&language=python

Run sample Flask web application..

Setup Flask environment on centos 7:
```
# yum install -y python3-pip
# pip3 install Flask
```

Test application flaskapp.py:
```
#!/opt/datadog-agent/embedded/bin/python3

import sys
import logging

sys.path.append('/opt/datadog-agent/embedded/lib/python3.8/site-packages')
#import tracer
from ddtrace import tracer

from flask import Flask

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
    return 'Entrypoint to the Application\n'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
```

Run in background using the ddtrace-run wrapper utility to launch:
```
# ln -s /opt/datadog-agent/embedded/bin/ddtrace-run /usr/local/bin/ddtrace-run
# export PATH=$PATH:/usr/local/bin

# ddtrace-run python flaskapp.py
 * Serving Flask app "ddtrace" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
2020-04-13 14:47:42,737 INFO [werkzeug] [_internal.py:113] -  * Running on http://0.0.0.0:5050/ (Press CTRL+C to quit)
2020-04-13 14:47:42,737 - werkzeug - INFO -  * Running on http://0.0.0.0:5050/ (Press CTRL+C to quit)

```

Quick CLI test to trigger some events (repeat a few times, or hit it from cron):
```
# curl http://localhost:5050
2020-04-13 14:48:40,185 DEBUG [ddtrace.tracer] [tracer.py:409] - Updating constant tags ['lang:python', 'lang_interpreter:CPython', 'lang_version:3.6.8', 'tracer_version:0.32.2', 'service:flask']
2020-04-13 14:48:40,185 - ddtrace.tracer - DEBUG - Updating constant tags ['lang:python', 'lang_interpreter:CPython', 'lang_version:3.6.8', 'tracer_version:0.32.2', 'service:flask']
2020-04-13 14:48:40,190 DEBUG [ddtrace.tracer] [tracer.py:533] - writing 8 spans (enabled:True)
2020-04-13 14:48:40,190 - ddtrace.tracer - DEBUG - writing 8 spans (enabled:True)
2020-04-13 14:48:40,190 DEBUG [ddtrace.tracer] [tracer.py:535] -
      name flask.request
        id 9565534702208706408
  trace_id 11513901572202687956
 parent_id None
   service flask
  resource GET /
      type web
     start 1586789320.184602
       end 1586789320.19029
  duration 0.005688s
     error 0
      tags
           flask.endpoint:api_entry
           flask.url_rule:/
           flask.version:1.1.2
           http.method:GET
           http.status_code:200
           http.url:http://localhost:5050/
           system.pid:32101
2020-04-13 14:48:40,190 - ddtrace.tracer - DEBUG -
      name flask.request
        id 9565534702208706408
  trace_id 11513901572202687956
 parent_id None
   service flask
  resource GET /
      type web
     start 1586789320.184602
       end 1586789320.19029
  duration 0.005688s
     error 0
      tags
           flask.endpoint:api_entry
           flask.url_rule:/
           flask.version:1.1.2
           http.method:GET
           http.status_code:200
           http.url:http://localhost:5050/
           system.pid:32101
2020-04-13 14:48:40,193 INFO [werkzeug] [_internal.py:113] - 127.0.0.1 - - [13/Apr/2020 14:48:40] "GET / HTTP/1.1" 200 -
2020-04-13 14:48:40,193 - werkzeug - INFO - 127.0.0.1 - - [13/Apr/2020 14:48:40] "GET / HTTP/1.1" 200 -
Entrypoint to the Application
2020-04-13 14:48:40,844 DEBUG [ddtrace.api] [api.py:236] - reported 1 traces in 0.00807s
2020-04-13 14:48:40,844 - ddtrace.api - DEBUG - reported 1 traces in 0.00807s
2020-04-13 14:48:40,845 DEBUG [ddtrace.sampler] [sampler.py:53] - initialized RateSampler, sample 100% of traces
2020-04-13 14:48:40,845 - ddtrace.sampler - DEBUG - initialized RateSampler, sample 100% of traces
```

Example Timeseries Dashboard showing some of the *trace.flask.request.x* events available:  

<img src="pictures/apm-flashapp-dashboard.png" alt="mongodb_agent_extension_install" width="900" title="Datadog agent mongodb integration install example"/>  

More examples for tracing in python (and other languages) can be found here: https://github.com/DataDog/trace-examples/blob/master/python/flask/app/app.py


## Bonus Question: What is the difference between a Service and a Resource?

APM Glossary doc reference: https://docs.datadoghq.com/tracing/visualization/

Concept | Definition
-|-
Service  | Services are the building blocks of modern microservice architectures. A service groups together endpoints, queries, or jobs for the purposes of scaling instances
Resource | Resources represent a particular domain of an application. For example; an instrumented web endpoint, database query, or background job


## Final Question: Something creative to use Datadog for?

It would be interesting to create an edge agent that could be used with IoT devices, some large edge devices like wind turbines as well as small processing applications like connected car which would present large volumes of clients.  It would be useful to use the powerful observability capabilities of the platform to perform predictive fault analysis to identify potential problems before a failure occurs.


