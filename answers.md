Your answers to the questions go here.

### Environment

* VMware is making a pushing into the Modern Application space.  This leverages containers and Kubernetes, so I chose to use Docker containers for the examples.  The containers used where:

* **datadog/agent     latest**
* **postgres          latest**
* **vmwareebc         latest**
* **Ubuntu (virtual machine)** *Victor explained that using the Docker run command was not widely implemented*

## Collecting Metrics:

* **Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.**

**Why use tags?**
* As developers and companies move to use containers (and Kubernetes for container orchestration) machines may be transient.  Adding tags provides
the appropriate information as to what part of the infrastructure generated the information.

### Approach #1 (Not a great approach *but was the only one I could get to work for Docker containers.  *It was suggested that I use Kubernetes or Linux agent*)
* Because I chose to use containers, I decided that the best way to add the tags would be to use the REST API capabilities.  To make this more scalable, there should be a script that allows for host and tags as input, that would iterate over the hosts and add the appropriate tags.  For sake of the excercise, I've just use a curl command to add the tags.

Use this call in script to list hosts:
```
curl -X GET "https://api.datadoghq.com/api/v1/hosts" \
 -H "Content-Type: application/json" \
 -H "DD-API-KEY: $DD_API_KEY" \
 -H "DD-APPLICATION-KEY: $DD_APPLICATION_KEY"
```
Found hostname *docker-desktop*
```
curl -X POST "https://api.datadoghq.com/api/v1/tags/hosts/docker-desktop" \
 -H "Content-Type: application/json" \
 -H "DD-API-KEY: $DD_API_KEY" \
 -H "DD-APPLICATION-KEY: $DD_APPLICATION_KEY" \
 -d '{ "host": "docker-desktop", "tags": ["environment:development", "vmwareebc"] }'
```
![AddTag](https://github.com/scotcurry/hiring-engineers/blob/master/Images/AddTag.png)

### Approach #2 (*Much simplifed approach using Linux Agent*)

All that was required for the Linux implementation was to edit the **conf.yaml** file in the /etc/datadog-agent folder. Below are the lines that 
were modified to enable the tags.

```
## @param tags  - list of key:value elements - optional
## List of host tags. Attached in-app to every metric, event, log, trace, and service check emitted by this Agent.
##
## Learn more about tagging: https://docs.datadoghq.com/tagging/
#
tags:
   - environment:dev
   - curryware:ddagent
```
Once the tags information was added to the conf.yaml file, a simple restart **(sudo systemctl restart datadog-agent)** and the tags were added.

![UbuntuAddTag](https://github.com/scotcurry/hiring-engineers/blob/master/Images/TagScreenshot.png)

* **Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.**

* The first thing I wanted to do was to validate that the integration was working on the host.  To do this I ran **sudo datadog-agent status**, which yielded the following for PostgreSQL.

```
postgres (5.4.0)
    ----------------
      Instance ID: postgres:9609e5da7813af1d [OK]
      Configuration Source: file:/etc/datadog-agent/conf.d/postgres.d/conf.yaml
      Total Runs: 266
      Metric Samples: Last Run: 30, Total: 7,980
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 1, Total: 266
      Average Execution Time : 19ms
      Last Execution Date : 2021-04-18 15:12:28 EDT / 2021-04-18 19:12:28 UTC (1618773148000)
      Last Successful Execution Date : 2021-04-18 15:12:28 EDT / 2021-04-18 19:12:28 UTC (1618773148000)
      metadata:
        version.major: 13
        version.minor: 2
        version.patch: 0
        version.raw: 13.2 (Ubuntu 13.2-1.pgdg20.04+1)
        version.scheme: semver
```

Also checked to see if the Custom check was running as expected:

```
curryware (0.1.0)
    -----------------
      Instance ID: curryware:5ba864f3937b5bad [OK]
      Configuration Source: file:/etc/datadog-agent/conf.d/curryware.d/curryware.yaml
      Total Runs: 599
      Metric Samples: Last Run: 2, Total: 1,198
      Events: Last Run: 0, Total: 0
      Service Checks: Last Run: 0, Total: 0
      Average Execution Time : 0s
      Last Execution Date : 2021-04-18 21:34:43 EDT / 2021-04-19 01:34:43 UTC (1618796083000)
      Last Successful Execution Date : 2021-04-18 21:34:43 EDT / 2021-04-19 01:34:43 UTC (1618796083000)
```
* While I currently use Firebase Realtime Database for the application I use Datadog for, I may at some point move the data storage to
Postgres.

**Postgres Integration Screenshot**
![PostgresIntegration](https://github.com/scotcurry/hiring-engineers/blob/master/Images/IntegrationsInstalled.png)

**Postgres Overview Screenshot**
![PostgresOverview](https://github.com/scotcurry/hiring-engineers/blob/master/Images/PostgressOverview.png)

* **Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.**

I wanted to have two Agent check values to put on the same graph.  Below is the Agent check code, and just below that is the YAML file
that initiates the Agent check.

**curryware.py script**
```
import random

from datadog_checks.base import AgentCheck


__version__ = "0.1.0"


class CurrywareCheck(AgentCheck):
    def check(self, instance):
        random_value = random.randint(0, 1000)
        curryware_value = random.randint(0, 1000)
        self.gauge('my_metric', random_value)
        self.gauge('curryware_metric', curryware_value)
```

* **Change your check's collection interval so that it only submits the metric once every 45 seconds.**
* *This configuration file below, addresses the bonus question of changing the collection time to 45 seconds*

```
init_config:


instances:
  - min_collection_interval: 45
```

**Custom Agent Check Screenshot**
![CustomAgentCheck](https://github.com/scotcurry/hiring-engineers/blob/master/Images/AgentCheck.png)


**Notes**

*Observation* - I wasn't able to correctly obtain Postgres metrics using the Docker configuration instructions. I've included it below in the hopes I can get a better understanding of how this should be implemented.

```
docker run -d --name datadog-agent -v /var/run/docker.sock:/var/run/docker.sock:ro -v /proc/:/host/proc/:ro -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
  -e DD_API_KEY=<Datadog Key> \
  -l com.datadoghq.ad.check_names='["postgres"]' \
  -l com.datadoghq.ad.init_configs='[{}]' \
  -l com.datadoghq.ad.instances='[{"host":"localhost", "port":5432,"username":"datadog","password":"AirWatch1"}]' \
  gcr.io/datadoghq/agent:7
  ```

## Visualizing Data:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Please note that the examples below are based on information running in containers that may not always be running.  Please 
contact Scot Curry at 312-489-1056 if the data is not populating.

[Curryware Timeboard](https://p.datadoghq.com/sb/s680qmbidyyypnvm-0d6eef751ed1027ddd547bcdd764d9ea)

![Curryware Timeboard Screenshot](https://github.com/scotcurry/hiring-engineers/blob/master/Timeboard.png)

[Link to Timeboard Creation Python Script](https://github.com/scotcurry/hiring-engineers/blob/master/buildtimeline.py)

  
* **Set the Timeboard's timeframe to the past 5 minutes**
  
This was a simple dropdown.
![Timeboard timeframe dropdown](https://github.com/scotcurry/hiring-engineers/blob/master/TimeDropDown.png)
  
* **Take a snapshot of this graph and use the @ notation to send it to yourself.**

The only way I was able to find to take a snapshot was via API, so based on the instructions that this would be done via the
console, I'm uncertain how to complete this task.

* **What is the Anomaly graph displaying?**

Anomaly detection distinguishes between normal and abnormal metric trends.  This is extremely helpful when building monitors and alerts.  This can
account for seasonality and show trends.

## Monitoring Data:

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

Definition of the monitor:
![Monitor Definition](https://github.com/scotcurry/hiring-engineers/blob/master/MetricDefinition.png)

Messages with variable information:
![Message Definition](https://github.com/scotcurry/hiring-engineers/blob/master/NotificationSettings.png)

Email Message for Monitor:
![Email Message](https://github.com/scotcurry/hiring-engineers/blob/master/EmailMessage.png)

**Notes**

*Question* - I don't seem to be handling the variables correctly.  The email should show the hostname, but it currently isn't.

## Collecting APM Data:

For this exercise I went a bit off script.  I got started with the Datadog technology for a real project.  I had created a site to automate some of the processes my company uses for performing Executive Briefings, so I didn't use the sample provided.

This is the snippet of code that initialized the Datadog trace.  There is a link to the fully instrumented coded below.

```
from ddtrace import tracer

app = Flask(__name__)
# This is a requirement if you are every going to use POSTs and forms.
app.secret_key = os.urandom(24)

setproctitle('vmwareebc')
tracer.configure(hostname='datadog-agent', port='8126')

FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
          '[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s '
          'dd.span_id=%(dd.span_id)s] ' '- %(message)s')

logFormatter = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
```

APM Screenshot 1:
![APM Screenshot 1](https://github.com/scotcurry/hiring-engineers/blob/master/APMScreenshot.png)

APM Screenshot 2:
![APM Screenshot 2](https://github.com/scotcurry/hiring-engineers/blob/master/APMScreenshot2.png)

Link to the instrumented app.py file:
[Link to app](https://github.com/scotcurry/MobileFlowsCalls/blob/master/app.py)

## Final Question:

* **Is there anything creative you would use Datadog for?**

While I haven't seen this capability, what I have seen a demand for is the ability to injest the kinds of data that Datadog currently obtains for infrastructure from mobile devices.  I currently work with two major grocery chains that have seen a need to understand what is going on with their mobile fleet.  They are in reactive mode ("it's a network issue, no it's an app issue").  They are both looking for a solution where the Ops team would be notified (store 10 is having latency issues, we should give them a call) when thing aren't working as expected.  This is exactly what Datadog does.
