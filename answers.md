# Datadog Demo

## Introduction
Datadog is a monitoring service for different architecture layres, either in cloud or on premises. Both infrastructure and middleware layers are monitored, providing insights of servers, databases, applications and tools through its data analytics platform.

This guide will use the Datadog Agent to monitor a server (that is the local workstation), a local MySQL database, a custom metric and a python application, to simulate a real and complete monitoring service.

## Environmet 
For this demo, the environment will be based on Linux containers, using the Docker image format, which is the most used format for running Linux containers. Nowaddays, organization are following the digital trasformation using the Linux container to ship their application on the cloud. As such, an environment based on this technology is a better fit for demo also in terms of portability and ease of replication.

However, Datadog supports the following platform:
![Supported platforms](images/dd-envs.png)

## Prerequisites
The host, the server running the demo, it must have access to internet (directly or via proxy), to be able to connect to the Docker public registry. The internet connection is also used to download and install other tools needed by the Datadog Agent. Last, but not least, a trial license to run the platform on the Datadog cloud environment.
In the next paragraphs are listed the required and optional softwares to run the demo.

### Required
* Docker; 
* Python 3, python3-setuptools, easy_install3, pip
* Python Datadog Agent package;

### Optional 
* Git;
* 

### Datadog trial
Open the browser to the Datadog site and click on the "Free trial" button, at the following link:
[https://www.datadoghq.com/](https://www.datadoghq.com/)

Signup as per the following image:
![Signed up](images/01-signup-2.png)

Once registerred, a confirmationemail is sent as follows:
![Signed up](images/01-signup.png)

The signup rpocess also provides a API KEY belongs to the account and which is used to run the Datadog Agent on the system.

## Docker
Docker is a piece of software that lets you create Linux containers with a specific image format, that is, the Docker image format.
Linux containers are a mash-up of functionalities available with the Linux kernel (that's why you often hear the phrase, Containers are Linux). Linux containers provide a lot of flexibility in regards to application deployment. As matter of fact, not just the application gets deployed, but the entire software stack. And the software stack is made of the application itself, its dependencies, the operative system, and the tools and processes running in the operative system. Freezing the complete software stack gives tremendous portability capability.
Docker brought Linux containers to a large scale, providing a toolkit for developers and administrators.

Docker can be installed following the instructions described in the [https://www.docker.com](https://www.docker.com) site. There is a Docker software bundle specific for each platfrom such as Linux (Debian and Red Hat based), Windows, and Mac OS.

### Datadog Agent
Datadog provides a Docker container image that can be used by anyone, and once Docker is installed, the Datadog Docker image can be discovered issuing the following command in a terminal window:

```bash
# docker search datadog
NAME                                  DESCRIPTION                                     STARS               OFFICIAL            AUTOMATED
datadog/docker-dd-agent               Docker container for the Datadog Agent.         85                                      [OK]
datadog/agent                         Docker container for the new Datadog Agent      28
datadog/squid                         Squid proxy configurable container.             14
tutum/datadog-agent                   Datadog agent inside a container optimized f…   4
datadog/cluster-agent                 Docker container for the new Datadog Cluster…   3
datadog/docker-dogstatsd              DogStatsD Dockerfile for Trusted Builds.        3                                       [OK]
datadog/agent-dev                     Development builds for the Datadog Agent 6      2
datadog/dev-dd-agent                  Development and test builds for docker-dd-ag…   2                                       [OK]
datadog/docker-library                TBD                                             1                                       [OK]
datadog/dogstatsd                     Standalone DogStatsD image for custom metric…   1
datadog/docker-filter                 Filtering proxy for a read-only access to th…   1                                       [OK]
gridx/datadog-agent-arm32v7                                                           0
janeczku/datadog-rancher-init         Sidekick image for deploying DataDog Agent i…   0                                       [OK]
opendoor/datadog-agent                                                                0
pasientskyhosting/datadog-agent       Custom Datadog Agent                            0                                       [OK]
csdisco/datadog-docker-dd-agent       Storing the 'latest' datadog docker dd-agent…   0
mozorg/datadog-agent                  Datadog agent for use with Mozilla Deis clus…   0
goldstar/datadog                                                                      0
datadog/cluster-agent-dev             Datadog Cluster Agent - DCA | Dev images        0
cfgarden/datadog-event-resource                                                       0
datadog/datadog-agent-runner-circle   CircleCI test runner/builder (debian)           0                                       [OK]
concourse/datadog-event-resource                                                      0
datadog/dogstatsd-dev                 Development builds for DogStatsD 6              0
tinklabs/datadog-agent                                                                0
datadog/tokumx                        Tokumx image for testing the datadog integra…   0
```

And the Docker container image for the new Datadog Agent is named "datadog/agent". Before the Docker image can be run as container needs to be pulled locally, as follows:
```bash
# docker pull datadog/agent
```

Once the "datadog/agent" is downloaded and stored locally on the host, the container can be run.
To properly run the "datadog/Agent", a list of parameters need to be set, such as DD_API_KEY, DD_HOSTNAME, DD_TAGS, DD_APM_ENABLED.
* DD_API_KEY - Your Datadog API key (required);
* DD_HOSTNAME - Hostname to use for metrics (if autodetection fails);
* DD_TAGS - Host tags separated by spaces;
* DD_APM_ENABLED - Enable trace collection with the trace Agent.

The Datadog Agent can be run as container as follows:
```bash
# docker run -it --rm=true --hostname=datadog.foogaro.com --name dd-agent -v `pwd`/mysql.conf.yaml:/etc/datadog-agent/conf.d/mysql.d/conf.yaml:rw -v `pwd`/randomcheck.py:/etc/datadog-agent/checks.d/randomcheck.py:rw -v `pwd`/randomcheck.yaml:/etc/datadog-agent/conf.d/randomcheck.yaml:rw -v /var/run/docker.sock:/var/run/docker.sock:ro -v /proc/:/host/proc/:ro -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro -e DD_API_KEY=329e0c344a47864d92ae0342f3797b3b -e DD_TAGS=name\:luigi -e DD_TAGS=lastname\:fugaro -e DD_APM_ENABLED=true
```

The above command also includes some settings (such as configuration files, MySQL database integrations that are explained later in this guide) and environment variables, that are placed into the main configuration file, locate by defaut at the following path: ```/etc/datadog-agent/datadog.yaml```


### MySQL Database
MySQL database can be run in a different server, in the cloud or locally. To ease the example, MySQL will be installed locally along side the Datadog agent.

To install MySQL the following commands can be issued in a terminal window:
```bash
# wget –c https://dev.mysql.com/get/mysql-apt-config_0.8.11-1_all.deb
# sudo dpkg –i mysql-apt-config_0.8.10-1_all.deb
# sudo apt-get update
# sudo apt-get install mysql-server
```

This kind of setup sets an auto-generated root password, which can be retrieved as follows:

```bash
# cat /var/log/mysqld.log
2019-07-08T21:08:16.573123Z 0 [System] [MY-013169] [Server] /usr/sbin/mysqld (mysqld 8.0.16) initializing of server in progress as process 72
2019-07-08T21:08:18.544871Z 5 [Note] [MY-010454] [Server] A temporary password is generated for root@localhost: dbdp1uJ(S/gt
2019-07-08T21:08:20.241957Z 0 [System] [MY-013170] [Server] /usr/sbin/mysqld (mysqld 8.0.16) initializing of server has completed
```

Once the root password is revealed, it can be used to integrate the Datadopg Agent. Eventually, MySQL root password can be changed to something more mnemonic, as follows:

```bash
# ALTER USER 'root'@'localhost' IDENTIFIED BY 'dataDog.2019';
```

The Datadog Agent needs to be able to read special tables on the database, and for such reason a specific user with specific grants needs to be created as follows:
```bash
CREATE USER 'datadog'@'localhost' IDENTIFIED WITH mysql_native_password by 'dataDog.2019';
ALTER USER 'datadog'@'localhost' WITH MAX_USER_CONNECTIONS 5;
GRANT REPLICATION CLIENT ON *.* TO 'datadog'@'localhost';
GRANT PROCESS ON *.* TO 'datadog'@'localhost';
GRANT SELECT ON performance_schema.* TO 'datadog'@'localhost';
```

Now that the database is ready to accept a user authenticaed as "datadog", the Datadog Agent itself needs the integration, that is needs to know how to connect to the MySQL database.
As stated before, the database is running locally, therefore the integration will point to MySQL running on "localhost" listening on its default port which is 3306.
Datadog Agent relies on a specif folder to read all its integration points.
By default the folder with all the configuration is located at the following path: ```/etc/datadog-agent/conf.d```
For MySQL there is the subfolder ```mysql.d``` which contains the configuration file.
The configuration file named "conf.yaml" looks like the following:

```bash
init_config:

instances:
  - server: 127.0.0.1
    user: datadog # datadog
    pass: 'dataDog.2019' # from the CREATE USER step earlier
    port: 3306 # e.g. 3306
    options:
        replication: false
        galera_cluster: true
        extra_status_metrics: true
        extra_innodb_metrics: true
        extra_performance_metrics: true
        schema_size_metrics: false
        disable_innodb_metrics: false
```

The Datadog Agent needs to be restarted in order for the new configuration to take effect, and it can be restarted as follows:

```bash
kill -9 $(pidof process-agent)
s6-svstat /var/run/s6/services/process/
```

Once the main process is stopped, it is automatically rescheduled and a new process with a new process ID is generated.


## Collecting Metrics
Next paragraphs will focus on how to implement a python script which automatically generates some random value to be used for a metric called "my_metric". As described at the beginning, the purpose of the demo is to monitor a server, a database, a metric and an application. The metric can be thought as a service which is pulled by the Datadog Agent to read the metric.

### Implementation details
A metric sending a random integer value between "0" (zero) "1000" (one thousand).

#### Script Python
```python
from random import randint
from checks import AgentCheck
class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(0,1000))
```
The script is also available here [randomcheck.py](https://github.com/foogaro/hiring-engineers/blob/master/files/randomcheck.py).

The script must be located in the folder ```/etc/datadog-agent/checks.d```.

#### Integration
The integration, as previously described for the MySQL database, is triggered by a file in the YAML format into the ```/etc/datadog-agent/conf.d``` folder, the file filename must be the same as its script, except for the file extension.
In this case:
* ```/etc/datadog-agent/checks.d/randomcheck.py```.
* ```/etc/datadog-agent/conf.d/randomcheck.yaml```.

The metric might need to be submitted at regural intervals, which by default are every 15 seconds. The value could be changed based on requirements, for example the metric needs to submitted once every 45 seconds.
The resulting YaML file would look like the following:
```yaml
init_config:

instances:
  - min_collection_interval: 45
```

The YAML file provides separation of concern between implementation details and configuration, so that for example the interval can be changed without modifyng the Pythin script at all. This kind of separation comes in hand for providng different behavoiur for dirrente environments, and the configuration can be put in place while provisiong the platform.

It's now time to really check what the Datadog Agent is collecting from the metric, the dataabase and the host.

## Visualizing data
To visualize some data, connect to the Datadog site and login using the credentials provided during the Sgnup process.
Once logged connect to the following URL: [https://app.datadoghq.com/infrastructure/map](https://app.datadoghq.com/infrastructure/map)

### Host
The platform should display the host generic view with the tags previously configured, as follows:
![Tags](images/02-host-tags.png)

### Database
The platform should display the host generic view with the tags previously configured, as follows:
![MySQL](images/04-host-mysql.png)

The database Integration should also be visible as validated in the integration section at the following URL: [https://app.datadoghq.com/account/settings#integrations/mysql](https://app.datadoghq.com/account/settings#integrations/mysql)
And the page should look like the following:
![MySQL](images/03-mysql.png)

### Metric host scoped
The platform should display the host generic view with the metric previously configured, as follows:
![Metric](images/03-host-metrics.png)

The metricshould also be visible in the metric section at the following URL: [https://app.datadoghq.com/metric/explorer](https://app.datadoghq.com/metric/explorer)
And the page should look like the following:
![Metric](images/04-metrics.png)

However, all the above single information can be grouped into a single view to better monitor the situation of the database and the metric.
In the next paragraph will be described how to create a single view called Timeboard, to show the state of the metric and the databse in a timeseries scenario.

### Timeboard
A Timeboard can be created using the platform or its createiong can be scripted in favor of automation, using the Datadog API.
For the above reasons a Python script will be used to create the Timeboard, which will graphically represent:
* The custom metric scoped over the host.
* Any metric from the Integration on the MySQL database with the anomaly function applied.
* The custom metric with the rollup function applied to sum up all the points for the past hour into one bucket.

And the script is the following:

```python
from Datadog import initialize, api

options = {
    'api_key': '329e0c344a47864d92ae0342f3797b3b',
    'app_key': 'a57a258b956ff7a5486da53dcb2c92c6e0926867'
}

initialize(**options)

title = "Hiring Engineer Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:datadog.foogaro.com}"}
        ],
        "viz": "timeseries"
    },
    "title": "Avg of my_metric over host:datadog.foogaro.com"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:datadog.foogaro.com}.rollup(sum, 3600)"}
        ],
        "viz": "query_value"
    },
    "title": "custom metric with the rollup function applied, 1 hour"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.net.connections{host:datadog.foogaro.com}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Avg of mysql.net.connections, with anomaly detection applied"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:datadog"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
```

The Python script to create the Timeboard, it is available for download at the following link:
[https://github.com/foogaro/hiring-engineers/blob/master/files/timeboard.py](https://github.com/foogaro/hiring-engineers/blob/master/files/timeboard.py).

The script can be launched in a terminal windows with the following command:
```bash
# python3 timeboard.py
```

The above command should create the dashboard that can be viewed at the following link:
[https://app.datadoghq.com/dashboard/lists](https://app.datadoghq.com/dashboard/lists)

A list of available dashboards should appear, as depicted below:
![Dashboard List](images/dashboard-list.png)

Click on the "Hiring Engineer Timeboard", and the resulting dashboard should look like the following:
![Timeboard](images/timeboard.png)

The Timeboard, as its name suggests, shows metric's values overtime, and this time can also be adjust to have insight for a specific period, like for example the lst 5 minutes, as shown below:
![Timeboard](images/timeboard-5min.png)

In case the insight shows up something important that needs to be shared, the user can take a snapshot and use the @ notation to send it to other people of the team, as shown below:
![Timeboard](images/timeboard-snapshot.png)


## Monitoring Data
Looking at a dashboard overtime can be tediuos and the team in charge of looking at the graphs can do other task and be more productive. For this case the Datadog platform provide an automatic mechanism to minotr the data based on threshold, on which some actions might be taken.

The platform can create a new Metric Monitor that watches the average of the custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:
* Warning threshold of 500
* Alerting threshold of 800
* Notify if there is No Data for this query over the past 10m.

### Threshold
The threshold can be set in the Monitor section at the following URL: [https://app.datadoghq.com/monitors#create/metric](https://app.datadoghq.com/monitors#create/metric)
And the configuration is the followings:
![Timeboard](images/metric-monitor-1.png)
![Timeboard](images/metric-monitor-2.png)

Furthermore, the Monitor feature provides the capability to send custom email to notify the user about the value of the metric.

### Notification
For example, the monitor can be configured the monitor’s message so that it will:
* Send an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

The message configuration is the following:
```
Hi @l.fugaro@gmail.com

The APM states:
{{#is_alert}}
The alert with threshold {{threshold}} was notified because the value was {{value}} from the host with IP {{host.ip}} at {{last_triggered_at}}.
{{/is_alert}}
{{#is_warning}}
The warning with threshold {{warn_threshold}} was notified because the value was {{value}} from the host with IP {{host.ip}} at {{last_triggered_at}}.
{{/is_warning}}
{{#is_no_data}}
No value detected within the last 10 minutes from the host with IP {{host.ip}} at {{last_triggered_at}}.
{{/is_no_data}}

Good luck.
```

#### Email
Whenever the monitor is triggered and the conditions are met, it will send an email, as the following:
![Notification](images/notification-warn.png)

#### Alternatives
However, notification are meant to be usefull whenever someone on the team can react to a problem. Nonetheless, notification can be sent only in a certain period, and silenced in a different period, or during a scheduled downtime. For example the monitor can be configured such that:
* silences it from 7pm to 9am daily on M-F,
* silences it all day on Sat-Sun.

And here are the relative configuration:
![Silence](images/silence-5days.png)
![Silence](images/silence-2days.png)

A reminder is sent via email when the downtime is triggered (started or stopped), as shown below for the two abovementioned cases:
![Notification](images/notification-downtime-1.png)
![Notification](images/notification-downtime-2.png)

## Collecting APM Data
As described at the beginning, Datadog Agent can collect metrics in a full-stack fashion, top-down, from the host to the application level, to check, verify and detect performance issues.
Transaction traces, app health, throughput, latency, can be collected and monitor with Datadog APM.

### Flask Application
A REST application can be monitored/traced using the Datadog Trace capabilities. Given the following Flask app instrument this using Datadog’s APM solution:

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

### ddtrace-run
The application can be monitored by running the application with Python and Datadog Trace, as follows:
```bash
# ddtrace-run python3 apm_flask.py
```

### Dashboard
The application Flask cna be dowloaded from the following URL:
[https://github.com/foogaro/hiring-engineers/blob/master/files/apm_flask.py](https://github.com/foogaro/hiring-engineers/blob/master/files/apm_flask.py).

The application REST API can be invoked using cURL from a terminal window to quickly repeat the call, as follows:
```bash
# curl http://localhost:5050/api/apm
```

The trace of the application collected by the Datadog platform can be viewed also with other metrics, for example with the custom metric, as shown below:
![APM](images/apm.png)


## Conclusion
Datadog monitoring provides a full set of features such as Analytics, Infrastructure Monitoring, and APM.
The scenario in which the patform can be adopted and promoted are really heteregenous, from the industry sector to the manufacturing sector, weather, IoT, really any scenrio.
The Datadog platform could be also used to monitor buildings, by a domotic point of view. As ingle apartment or a building composed by several apartments and lofts, can monitor:
* energy efficiency
* set threshold to automatically switch on or off devices (such as eater, air conditioning, and so on)
* resource consumption;

Everything could be automated to prevent waste of money and resources, to less impact on the environment and contribute for a green environment.

















## Not just for IT environments
## Domotic

Use cases

## Your answers to the questions go here.

If you want to apply as a solutions engineer at [Datadog](http://Datadog.com) you are in the right spot. Read on, it's fun, I promise.

<a href="http://www.flickr.com/photos/alq666/10125225186/" title="The view from our roofdeck">
<img src="http://farm6.staticflickr.com/5497/10125225186_825bfdb929.jpg" width="500" height="332" alt="_DSC4652"></a>

## The Exercise

Don’t forget to read the [References](https://github.com/Datadog/hiring-engineers/blob/solutions-engineer/README.md#references)

## Questions

Please provide screenshots and code snippets for all steps.

## Prerequisites - Setup the environment

You can utilize any OS/host that you would like to complete this exercise. However, we recommend one of the following approaches:

* You can spin up a fresh linux VM via Vagrant or other tools so that you don’t run into any OS or dependency issues. [Here are instructions](https://github.com/Datadog/hiring-engineers/blob/solutions-engineer/README.md#vagrant) for setting up a Vagrant Ubuntu VM. We strongly recommend using minimum `v. 16.04` to avoid dependency issues.
* You can utilize a Containerized approach with Docker for Linux and our dockerized Datadog Agent image.

Then, sign up for Datadog (use “Datadog Recruiting Candidate” in the “Company” field), get the Agent reporting metrics from your local machine.


Signed up as follows:
![Signed up](images/01-signup.png)

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.
![Tags](images/02-host-tags.png)

* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.
![MySQL](images/03-mysql.png)
![MySQL](images/06-mysql-dashboard.png)

* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.
```python
from random import randint
from checks import AgentCheck
class RandomCheck(AgentCheck):
    def check(self, instance):
        self.gauge('my_metric', randint(0,1000))
```

[randomcheck.py](https://github.com/foogaro/hiring-engineers/blob/master/files/randomcheck.py).

* Change your check's collection interval so that it only submits the metric once every 45 seconds.
```yaml
init_config:

instances:
  - min_collection_interval: 45
```
[randomcheck.yaml](https://github.com/foogaro/hiring-engineers/blob/master/files/randomcheck.yaml).

* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?
* **Bonus Answer** Short answer is, yes I can. Simply update the yaml file with a different interval.

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

```python
from Datadog import initialize, api

options = {
    'api_key': '329e0c344a47864d92ae0342f3797b3b',
    'app_key': 'a57a258b956ff7a5486da53dcb2c92c6e0926867'
}

initialize(**options)

title = "Hiring Engineer Timeboard"
description = "An informative timeboard."
graphs = [{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:Datadog.foogaro.com}"}
        ],
        "viz": "timeseries"
    },
    "title": "Avg of my_metric over host:Datadog.foogaro.com"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "avg:my_metric{host:Datadog.foogaro.com}.rollup(sum, 3600)"}
        ],
        "viz": "query_value"
    },
    "title": "custom metric with the rollup function applied, 1 hour"
},
{
    "definition": {
        "events": [],
        "requests": [
            {"q": "anomalies(avg:mysql.net.connections{host:Datadog.foogaro.com}, 'basic', 2)"}
        ],
        "viz": "timeseries"
    },
    "title": "Avg of mysql.net.connections, with anomaly detection applied"
}]

template_variables = [{
    "name": "host1",
    "prefix": "host",
    "default": "host:879843aa76e1"
}]

read_only = True
api.Timeboard.create(title=title,
                     description=description,
                     graphs=graphs,
                     template_variables=template_variables,
                     read_only=read_only)
```
[timeboard.py](https://github.com/foogaro/hiring-engineers/blob/master/files/timeboard.py).

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

Once this is created, access the Dashboard from your Dashboard List in the UI:
![Timeboard](images/timeboard.png)

* Set the Timeboard's timeframe to the past 5 minutes
![Timeboard](images/timeboard-5min.png)

* Take a snapshot of this graph and use the @ notation to send it to yourself.
![Timeboard](images/timeboard-snapshot.png)

* **Bonus Question**: What is the Anomaly graph displaying?
* **Bonus Answer**: The Anomaly graph displaying lower and higher spike of the custom mectric.


## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.
![Timeboard](images/metric-monitor-1.png)
![Timeboard](images/metric-monitor-2.png)

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.
```
Hi @l.fugaro@gmail.com

The APM states:
{{#is_alert}}
The alert with threshold {{threshold}} was notified because the value was {{value}} from the host with IP {{host.ip}} at {{last_triggered_at}}.
{{/is_alert}}
{{#is_warning}}
The warning with threshold {{warn_threshold}} was notified because the value was {{value}} from the host with IP {{host.ip}} at {{last_triggered_at}}.
{{/is_warning}}
{{#is_no_data}}
No value detected within the last 10 minutes from the host with IP {{host.ip}} at {{last_triggered_at}}.
{{/is_no_data}}

Good luck.
```

* When this monitor sends you an email notification, take a screenshot of the email that it sends you.
![Notification](images/notification-warn.png)


* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
![Silence](images/silence-5days.png)

  * And one that silences it all day on Sat-Sun.
![Silence](images/silence-2days.png)
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
![Notification](images/notification-downtime-1.png)
![Notification](images/notification-downtime-2.png)

## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

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

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

* **Bonus Question**: What is the difference between a Service and a Resource?
* **Bonus Answer**: A Resource is a particular action for a service. A service is a set of processes that do the same job.

Provide a link and a screenshot of a Dashboard with both APM and Infrastructure Metrics.
![APM](images/apm.png)


Please include your fully instrumented app in your submission, as well.
[apm_flask.py](https://github.com/foogaro/hiring-engineers/blob/master/files/apm_flask.py).

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

* **Final Answer**: Domotic might be a good use case, monitoring your house and all its devices can be really usefull and a lots of fun. Suppose monitoring all those Arduino like devices.
It should be also easy, as the main languange is python.

## Instructions

If you have a question, create an issue in this repository.

To submit your answers:

* Fork this repo.
* Answer the questions in answers.md
* Commit as much code as you need to support your answers.
* Submit a pull request.
* Don't forget to include links to your dashboard(s), even better links and screenshots. We recommend that you include your screenshots inline with your answers.

## References

### How to get started with Datadog

* [Datadog overview](https://docs.Datadoghq.com/)
* [Guide to graphing in Datadog](https://docs.Datadoghq.com/graphing/)
* [Guide to monitoring in Datadog](https://docs.Datadoghq.com/monitors/)

### The Datadog Agent and Metrics

* [Guide to the Agent](https://docs.Datadoghq.com/agent/)
* [Datadog Docker-image repo](https://hub.docker.com/r/Datadog/docker-dd-agent/)
* [Writing an Agent check](https://docs.Datadoghq.com/developers/write_agent_check/)
* [Datadog API](https://docs.Datadoghq.com/api/)

### APM

* [Datadog Tracing Docs](https://docs.Datadoghq.com/tracing)
* [Flask Introduction](http://flask.pocoo.org/docs/0.12/quickstart/)

### Vagrant

* [Setting Up Vagrant](https://www.vagrantup.com/intro/getting-started/)

### Other questions:

* [Datadog Help Center](https://help.Datadoghq.com/hc/en-us)